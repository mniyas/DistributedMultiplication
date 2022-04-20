import os
import grpc
import time
import math
import matrix_pb2_grpc
from matrix_pb2 import MatrixRequest


class StubPool:
    """
    Create a stub pool with 4 stubs.
    """
    def __init__(self):
        grpc1 = os.getenv("ENV_GRPC1", "0.0.0.0")
        grpc2 = os.getenv("ENV_GRPC2", "0.0.0.0")
        grpc3 = os.getenv("ENV_GRPC3", "0.0.0.0")
        listeners = [f'{grpc1}:8000', f'{grpc2}:8000', f'{grpc3}:8000']
        self.stubs = []
        for address in listeners:
            channel = grpc.insecure_channel(address)
            stub = matrix_pb2_grpc.MatrixServiceStub(channel)
            self.stubs.append(stub)
        self.stub_idx = 0

    def get_stub(self, servers=None):
        """
        Get a stub from the pool in round robin fashion.
        """
        if not servers:
            servers = len(self.stubs)
        self.stub_idx = (self.stub_idx + 1) % servers
        return self.stubs[self.stub_idx]

    def close(self):
        """
        Close all channels.
        """
        for channel in self.channels:
            channel.close()


def multiply_indvidual_block(stub, a, b):
    """
    Multiply blocks of 2x2.
    """    
    result = stub.MultiplyBlock(MatrixRequest(a00=a[0][0], a01=a[0][1], a10=a[1][0], a11=a[1][1],
                    b00=b[0][0], b01=b[0][1], b10=b[1][0], b11=b[1][1]))
    return result


def block_multiply(stubs, servers, row, col):
    """
    Multiply two lists of 2x2 matrix blocks and add them.
    """
    out = None
    for item in zip(row, col):
        a, b = item
        stub = stubs.get_stub(servers)
        mult = multiply_indvidual_block(stub, a, b)
        if out:
            stub = stubs.get_stub(servers)
            add = stub.AddBlock(MatrixRequest(a00=out[0][0], a01=out[0][1], a10=out[1][0], a11=out[1][1], b00=mult.c00, b01=mult.c01, b10=mult.c10, b11=mult.c11))
            out = [[add.c00, add.c01], [add.c10, add.c11]]
        else:
            out = [[mult.c00, mult.c01], [mult.c10, mult.c11]]
    return out


def get_number_of_servers(stubs, a, b, blocks, deadline):
    """
    Get the number of servers.
    """
    start_time = time.time()
    stub = stubs.get_stub(1)
    mult = multiply_indvidual_block(stub, a, b)
    end_time = time.time()
    footprint = end_time - start_time
    block_calls = blocks * 2
    servers = footprint * block_calls / deadline
    return math.ceil(servers)

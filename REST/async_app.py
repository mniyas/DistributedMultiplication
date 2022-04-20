from __future__ import print_function
import logging

from fastapi import FastAPI, UploadFile
from async_grpcClient import StubPool, block_multiply, get_number_of_servers
import numpy as np
import asyncio

GRPC_SERVERS = 3
app = FastAPI()
stub_pool = StubPool()


def parse_matrix(iput_file):
    """
    parse matrix from input file
    """
    # read file
    content = iput_file.file.read().decode("utf-8")
    # split matrix into lines
    lines = content.strip().split("\n")
    # split lines into numbers
    matrix = [line.split(" ") for line in lines]
    # convert numbers to int
    matrix = [[int(number.strip()) for number in line if number] for line in matrix]
    return matrix


@app.get("/")
def read_root():
    return {"Hello": """This is a REST interface for distriubted matrix multiplication.
                        Check /docs to see how to use it."""}


# add router to upload text files and compute the result
@app.post("/matrix")
async def matrix_file(A: UploadFile, B: UploadFile, deadline: float = 0.03):
    '''
    This function takes two text files and returns the result of matrix addition and multiplication.
    '''
    A = parse_matrix(A)
    B = parse_matrix(B)
    # check if matrix is square
    if ((len(A) % 2 != 0) or (len(B) % 2 != 0) or (
        sum([len(line) for line in A]) % 2 != 0) or (sum([len(line) for line in B]) % 2 != 0)):
            return {"error": "Matrix A and B must be square"}

    # check if matrices are valid for multiplication
    if (len(A) != len(B)) or len(A[0]) != len(B[0]) or len(A) != len(A[0] or len(B) != len(B[0])):
        return {"error": "Matrix A and B must have same dimensions"}
    
    # split the matrix into 2x2 blocks
    A = np.array(A)
    B = np.array(B)

    # split the matrix into 2x2 blocks row by row
    row_blocks = [[A[i:i+2, j:j+2] for j in range(0, len(A), 2)] for i in range(0, len(A), 2)]
    # split the matrix into 2x2 blocks column by column
    col_blocks = [[B[i:i+2, j:j+2] for i in range(0, len(B), 2)] for j in range(0, len(B), 2)]
    
    # calculate number of servers required for the opration
    servers = await get_number_of_servers(stub_pool, row_blocks[0][0], col_blocks[0][0], len(A), deadline)
    if servers > GRPC_SERVERS:
        servers = GRPC_SERVERS
        logging.info(f"""Not enough servers available to do the multiplication.
                         Required servers: {servers}. Going with best-effort scheme""")
    
    # calculate multiplication of each block
    coros = [block_multiply(stub_pool, servers, row_blocks[i], col_blocks[j])
                for i in range(len(row_blocks)) for j in range(len(col_blocks))]
    # wait for all blocks to finish
    result = await asyncio.gather(*coros)
    # flatten the matrix
    result = [x for sublist in result for item in sublist for x in item]
    # reshape the matrix
    result = [result[i: i + len(A)] for i in range(0, len(A)*len(A), len(A))]
    return {'result': result}

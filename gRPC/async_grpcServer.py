from concurrent import futures
import logging
import argparse
import os

import asyncio
import grpc
import matrix_pb2
import matrix_pb2_grpc

class MatrixService(matrix_pb2_grpc.MatrixServiceServicer):

    async def MultiplyBlock(self, request, context):
        C00 = request.a00 * request.b00 + request.a01 * request.b10
        C01 = request.a00 * request.b01 + request.a01 * request.b11
        C10 = request.a10 * request.b00 + request.a11 * request.b10
        C11 = request.a10 * request.b01 + request.a11 * request.b11
        return matrix_pb2.MatrixReply(c00=C00, c01=C01, c10=C10, c11=C11)


    async def AddBlock(self, request, context):
        C00 = request.a00 + request.b00
        C01 = request.a01 + request.b01
        C10 = request.a10 + request.b10
        C11 = request.a11 + request.b11
        return matrix_pb2.MatrixReply(c00=C00, c01=C01, c10=C10, c11=C11)

async def serve(port):
    server = grpc.aio.server()
    matrix_pb2_grpc.add_MatrixServiceServicer_to_server(MatrixService(), server)
    host = os.getenv("ENV_HOST", "0.0.0.0")
    port = os.getenv("ENV_PORT", port)
    server.add_insecure_port(f'{host}:{port}')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--port', default=8000, type=int, help='The port to listen on.')
    args = argparser.parse_args()
    logging.info('Starting server on port {}.'.format(args.port))
    asyncio.run(serve(args.port))

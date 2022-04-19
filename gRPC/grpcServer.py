from concurrent import futures
import logging
import argparse
import grpc
import matrix_pb2
import matrix_pb2_grpc

class MatrixService(matrix_pb2_grpc.MatrixServiceServicer):

    def MultiplyBlock(self, request, context):
        C00 = request.a00 * request.b00 + request.a01 * request.b10
        C01 = request.a00 * request.b01 + request.a01 * request.b11
        C10 = request.a10 * request.b00 + request.a11 * request.b10
        C11 = request.a10 * request.b01 + request.a11 * request.b11
        return matrix_pb2.MatrixReply(c00=C00, c01=C01, c10=C10, c11=C11)


    def AddBlock(self, request, context):
        C00 = request.a00 + request.b00
        C01 = request.a01 + request.b01
        C10 = request.a10 + request.b10
        C11 = request.a11 + request.b11
        return matrix_pb2.MatrixReply(c00=C00, c01=C01, c10=C10, c11=C11)

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    matrix_pb2_grpc.add_MatrixServiceServicer_to_server(MatrixService(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--port', default=50051, type=int, help='The port to listen on.')
    args = argparser.parse_args()
    logging.info('Starting server on port {}.'.format(args.port))
    serve(args.port)

FROM python

RUN mkdir /service
COPY protos/ /service/protos/
COPY gRPC/ /service/gRPC/
WORKDIR /service/gRPC
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protos --python_out=. \
           --grpc_python_out=. ../protos/matrix.proto

EXPOSE 8000
ENTRYPOINT [ "python", "async_grpcServer.py" ]


# Build the image
# docker build . -f gRPC/Dockerfile -t grpc-server

# Run the image
# docker run -p 0.0.0.0:8000:8000/tcp grpc-server
# docker run -p 0.0.0.0:8000:8000/tcp --network microservices --name matrix_multiply_service grpc-server
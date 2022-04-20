FROM python

RUN mkdir /REST
COPY protos/ /REST/protos/
COPY REST/ /REST/FastAPI/
WORKDIR /REST/FastAPI
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protos --python_out=. \
           --grpc_python_out=. ../protos/matrix.proto

EXPOSE 8010
ENTRYPOINT [ "uvicorn", "async_app:app", "--host=0.0.0.0", "--port=8010" ]


# Build the image
# docker build . -f REST/Dockerfile -t rest-server

# Run the image
# docker run -p 0.0.0.0:8010:8010/tcp rest-server 
# docker run -p 127.0.0.1:8010:8010/tcp --network microservices -e ENV_HOST=matrix_multiply_service rest-server

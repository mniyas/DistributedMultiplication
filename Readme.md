# Distributed Matrix Multiplication
This project involves the use of REST interface and gRPC based services to allow matrix multiplication to be split among
multiple machines. Block Matrix multiplication is a method for multiplying matrices which is useful in distributed systems as it can easily split the calculations among mutiple machines.

# Architecture

- This project involves 3 components
    - a REST interface to upload matrix as input files. I'm using FastAPI for this.
    - Async gRPC Servers to do the matrix multiplication and addition
    - Async gRPC Clients

# Setup with Docker

- Running `docker-compose up` should run 1 REST container and 3 gRPC server containers.
- Visit `http://0.0.0.0:8010/docs` to access the API

# Setup without Docker
- Install the dependencies
    - `pip install -r gRPC/requirements.txt`
    - `pip install -r REST/requirements.txt`
- Run 3 gRPC Servers on different ports
    - Sample: `python async_grpcServer.py --port=8000`
- Modify the client listeners in `REST/async_grpcClient.py` file to point to the running gRPC servers.
- Run FastAPI app
    - `uvicorn async_app:app --port=8010`
- Visit `http://0.0.0.0:8010/docs` to access the API
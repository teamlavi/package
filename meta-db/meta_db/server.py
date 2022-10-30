from concurrent import futures
import signal
import sys

import grpc

protos, services = grpc.protos_and_services("protobuf/helloworld.proto")


def exit_handler(_signo, _stack_frame):
    """Gracefully handle exit."""
    sys.exit(0)


class Greeter(services.GreeterServicer):

    def SayHello(self, request, context):
        return protos.HelloReply(message=f"Hello, {request.name}!")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handler)
    serve()

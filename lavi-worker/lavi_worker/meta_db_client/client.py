import grpc
import grpc.experimental

protos, services = grpc.protos_and_services("protobuf/meta_db.proto")


def get_greeting(name: str) -> str:
    """Get a greeting from the grpc server."""
    req = protos.HelloRequest(name=name)
    resp = services.Greeter.SayHello(req, "meta-db:80", insecure=True)
    return resp.message

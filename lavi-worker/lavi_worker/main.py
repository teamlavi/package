from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from lavi_worker import config
from lavi_worker.meta_db_client import get_greeting
from lavi_worker.meta_db_client.client import protos

app = FastAPI(root_path=config.EXPECTED_PREFIX)


@app.get("/ping", response_class=PlainTextResponse)
def ping() -> str:
    """Ping pong."""
    return "pong"


@app.get("/greeting", response_class=PlainTextResponse)
def greeting(name: str) -> str:
    """Get a greeting from the meta db grpc server."""
    return get_greeting(name=name)


@app.get("/test", response_class=PlainTextResponse)
def test() -> str:
    """Testing code."""
    return str(dir(protos))

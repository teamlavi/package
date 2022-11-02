from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from lavi_worker import config

app = FastAPI(root_path=config.EXPECTED_PREFIX)


@app.get("/ping", response_class=PlainTextResponse)
def ping() -> str:
    """Ping pong."""
    return "pong"

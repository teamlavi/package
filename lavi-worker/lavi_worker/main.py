from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.get("/ping", response_class=PlainTextResponse)
def ping() -> str:
    """Ping pong."""
    return "pong"

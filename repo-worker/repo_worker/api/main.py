from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from repo_worker import config


# Create the app
app = FastAPI(
    root_path=config.EXPECTED_PREFIX,
    title="Repo API",
    description="The API layer to allow manual scrape triggers",
)


# Basic liveness ping
@app.get("/ping", response_class=PlainTextResponse, tags=["maintenance"])
def ping() -> str:
    """Ping pong."""
    return "pong"

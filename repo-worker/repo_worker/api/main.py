from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse

from repo_worker import config
from repo_worker.core.redis_wq import get_redis_wq


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


# Trigger manual tree generation
@app.post("/generate_tree", tags=["triggers"])
def trigger_generate_tree(repo: str, package: str, version: str) -> Response:
    """Trigger tree generation."""
    out_wq = get_redis_wq("to_generate_tree")
    out_wq.insert((repo, package, version))
    return Response(status_code=200)

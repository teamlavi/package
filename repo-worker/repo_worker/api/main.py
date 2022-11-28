from typing import List, Tuple

from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse

from repo_worker import config
from repo_worker.core.redis_wq import get_redis_wq, known_queue_sizes


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


@app.get("/failures", tags=["maintenance"])
def get_failures(queue_name: str) -> List[Tuple[str, ...]]:
    """Get enumerated failures given a queue name."""
    if queue_name not in known_queue_sizes:
        raise Exception(f"Unknown queue: {queue_name}")
    wq = get_redis_wq(queue_name)
    failures = wq.get_failures()
    return failures


@app.post("/flushall", tags=["maintenance"])
def flush_all() -> Response:
    """Flush the whole redis db."""
    # Just use a wq object to get the db for us, kinda a hack
    wq = get_redis_wq("to_list_versions")
    wq.db.flushall()
    return Response(status_code=200)


@app.get("/metrics", tags=["maintenance"])
def get_metrics(queue_name: str) -> List[Tuple[int, int]]:
    """Get all metrics from the given queue."""
    if queue_name not in known_queue_sizes:
        raise Exception(f"Unknown queue: {queue_name}")
    wq = get_redis_wq(queue_name)
    return wq.get_metrics()


# Trigger manual tree generation
@app.post("/generate_tree", tags=["triggers"])
def trigger_generate_tree(repo: str, package: str, version: str) -> Response:
    """Trigger tree generation."""
    out_wq = get_redis_wq("to_generate_tree")
    out_wq.insert((repo, package, version))
    return Response(status_code=200)


@app.get("/generate_tree")
def generate_tree_status(repo: str, package: str, version: str) -> str:
    """Get the status of the given job."""
    wq = get_redis_wq("to_generate_tree")
    return wq.get_status((repo, package, version))


@app.post("/list_packages", tags=["triggers"])
def list_packages(repo: str, run_full: bool):
    """Trigger package listing."""
    wq = get_redis_wq("to_list_packages")
    wq.insert((repo, str(run_full)))
    return Response(status_code=200)

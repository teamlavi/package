from typing import Any

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from psycopg.types.json import set_json_dumps, set_json_loads
import orjson

from lavi_worker import config
from lavi_worker.routers import external, internal


# Create the app
app = FastAPI(root_path=config.EXPECTED_PREFIX)


# Configure psycopg json funcs
def json_dumps(data: Any) -> str:
    return orjson.dumps(data).decode("utf-8")


set_json_dumps(json_dumps)
set_json_loads(orjson.loads)

# Add routers
app.include_router(external.router)
app.include_router(internal.router, prefix="/internal")


# App startup script
@app.on_event("startup")
async def app_startup() -> None:
    """Verify config."""
    # Valiadte env vars set
    if any([var is None for var in config.REQUIRED_ENV_FOR_DEPLOY]):
        raise Exception(f"Missing required env vars: {config.REQUIRED_ENV_FOR_DEPLOY}")


# Basic liveness ping
@app.get("/ping", response_class=PlainTextResponse)
def ping() -> str:
    """Ping pong."""
    return "pong"


# Basic health ping
@app.get("/healthy", response_class=PlainTextResponse)
def healthy() -> str:
    """Check if wired in."""
    # TODO: check can connect to db
    return "true"

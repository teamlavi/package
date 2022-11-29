from typing import Any

from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse
from psycopg.types.json import set_json_dumps, set_json_loads
import orjson

from utils import config
from internal import updates
from routers import analysis, external, internal


# Create the app
app = FastAPI(
    root_path=config.EXPECTED_PREFIX,
    title="LAVI API",
    description="The API layer for clients of LAVI",
)


# Configure psycopg json funcs
def json_dumps(data: Any) -> str:
    return orjson.dumps(data).decode("utf-8")


set_json_dumps(json_dumps)
set_json_loads(orjson.loads)

# Add routers
app.include_router(analysis.router, prefix="/analysis")
app.include_router(external.router)
app.include_router(internal.router, prefix="/internal")


# App startup script
@app.on_event("startup")
async def app_startup() -> None:
    """Verify config, check if db initialized."""
    # Validate env vars set
    if any([var is None for var in config.REQUIRED_ENV_FOR_DEPLOY]):
        raise Exception(f"Missing required env vars: {config.REQUIRED_ENV_FOR_DEPLOY}")

    # Wait for database to come up
    await updates.wait_for_live()

    # Check if db initialized
    if not await updates.is_db_initialized():
        await updates.initialize_database()


# Basic liveness ping
@app.get("/ping", response_class=PlainTextResponse, tags=["maintenance"])
def ping() -> str:
    """Ping pong."""
    return "ponggy"


# Basic health ping
@app.get("/healthy", response_class=PlainTextResponse, tags=["maintenance"])
async def healthy() -> Response:
    """Check if wired in."""
    if not await updates.is_db_initialized():
        return Response(status_code=503)
    return Response(status_code=200)

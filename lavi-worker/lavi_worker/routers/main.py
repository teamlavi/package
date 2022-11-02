from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from lavi_worker import config
from lavi_worker.routers import external, internal


app = FastAPI(root_path=config.EXPECTED_PREFIX)

# Add routers
app.include_router(external.router)
app.include_router(internal.router, prefix="/internal")


@app.get("/ping", response_class=PlainTextResponse)
def ping() -> str:
    """Ping pong."""
    return "pong"

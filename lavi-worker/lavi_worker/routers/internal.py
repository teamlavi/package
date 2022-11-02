from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse

from lavi_worker.internal import updates
from lavi_worker.routers import api_models


router = APIRouter(tags=["internal"])


@router.post("/trigger_scraper")
async def trigger_scraper() -> Response:
    """Trigger the scraper to refresh the database."""
    # TODO: trigger the scraper
    return Response(status_code=200)


@router.post("/insert_vuln")
async def insert_vuln(insert_vuln_request: api_models.InsertVulnRequest) -> Response:
    """Insert a single vulnerability."""
    await updates.insert_single_vulnerability(**insert_vuln_request.dict())
    return Response(status_code=200)


@router.post("/delete_vuln")
async def delete_vuln(delete_vuln_request: api_models.DeleteVulnRequest) -> Response:
    """Delete a single vulnerability."""
    await updates.delete_single_vulnerability(**delete_vuln_request.dict())
    return Response(status_code=200)


@router.post("/database/clear")
async def clear_database() -> Response:
    """Clear all rows of the database tables."""
    await updates.clear_database()
    return Response(status_code=200)


@router.post("/database/nuke")
async def nuke_database() -> Response:
    """Completely delete all our database tables."""
    await updates.nuke_database()
    return Response(status_code=200)


@router.post("/database/init")
async def initialize_database() -> Response:
    """Freshly initialize the database."""
    await updates.initialize_database()
    return Response(status_code=200)


@router.get("/database/init", response_class=PlainTextResponse)
async def get_database_initialized() -> str:
    """Check whether the database is initialized."""
    return "true" if await updates.is_db_initialized() else "false"  # no cap


@router.get("/database/size", response_class=PlainTextResponse)
async def get_database_size() -> str:
    """Get the size of the database."""
    size = await updates.database_size(table="cves")
    return str(size)
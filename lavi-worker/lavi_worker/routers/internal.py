from fastapi import APIRouter, Response


router = APIRouter()


@router.post("/trigger_db_init")
async def trigger_db_init() -> Response:
    """Trigger the db to initialize."""
    # TODO: check if db initialized
    # TODO: if not, initialize it
    return Response(status_code=200)


@router.post("/trigger_scraper")
async def trigger_scraper() -> Response:
    """Trigger the scraper to refresh the database."""
    # TODO: trigger the scraper
    return Response(status_code=200)

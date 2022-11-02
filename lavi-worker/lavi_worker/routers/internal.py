from fastapi import APIRouter, Response


router = APIRouter()


@router.post("/trigger_scraper")
async def trigger_scraper() -> Response:
    """Trigger the scraper to refresh the database."""
    # TODO: trigger the scraper
    return Response(status_code=200)

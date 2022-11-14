from fastapi import APIRouter

from lavi_worker.routers import api_models


router = APIRouter(tags=["analysis"])

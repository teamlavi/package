from fastapi import APIRouter
from fastapi.responses import PlainTextResponse


router = APIRouter(tags=["scrapers"])


@router.post("/trigger/list_packages", response_class=PlainTextResponse)
def trigger_list_packages(repo_name: str, partial: bool) -> str:
    """Trigger listing package names given a repo name."""
    ...


@router.post("/trigger/list_versions", response_class=PlainTextResponse)
def trigger_list_versions(repo_name: str, package_name: str) -> str:
    """Trigger listing versions given a repo name and package name."""
    ...


@router.post("/trigger/generate_tree", response_class=PlainTextResponse)
def trigger_generate_tree(repo_name: str, package_name: str, version: str) -> str:
    """Trigger generating tree, given repo, package, version."""
    ...

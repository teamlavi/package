from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from internal.queues import QueueName, get_queue
from internal import scraping


router = APIRouter(tags=["scrapers"])


@router.post("/trigger/list_packages", response_class=PlainTextResponse)
def trigger_list_packages(repo_name: str, partial: bool) -> str:
    """Trigger listing package names given a repo name."""
    job = get_queue(QueueName.to_list_packages).enqueue(
        scraping.list_packages, repo_name, partial
    )
    return job.get_id()  # type: ignore


@router.post("/trigger/list_versions", response_class=PlainTextResponse)
def trigger_list_versions(repo_name: str, package_name: str) -> str:
    """Trigger listing versions given a repo name and package name."""
    job = get_queue(QueueName.to_list_versions).enqueue(
        scraping.list_package_versions, repo_name, package_name
    )
    return job.get_id()  # type: ignore


@router.post("/trigger/generate_tree", response_class=PlainTextResponse)
def trigger_generate_tree(repo_name: str, package_name: str, version: str) -> str:
    """Trigger generating tree, given repo, package, version."""
    job = get_queue(QueueName.to_generate_tree).enqueue(
        scraping.generate_tree, repo_name, package_name, version
    )
    return job.get_id()  # type: ignore

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from internal import scraping
from internal.queues import QueueName, get_queue
from routers.dependencies import verify_code


router = APIRouter(dependencies=[Depends(verify_code)], tags=["scrapers"])


@router.post("/trigger/get_cves", response_class=PlainTextResponse)
def trigger_get_cves(repo_name: str) -> str:
    """Trigger getting cves from gh advisories."""
    job = get_queue(QueueName.to_get_cves).enqueue(
        scraping.get_cves, repo_name, job_timeout=7200
    )
    return job.get_id()  # type: ignore


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

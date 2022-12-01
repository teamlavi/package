from typing import Any

from fastapi import APIRouter

from internal import queries
from internal.queues import QueueName, get_queue
from routers import api_models
from utils import utils

router = APIRouter(tags=["analysis"])


# 1.) affectedCount - For vulnerabilities found in queried packages
# return a list with the number of packages affected by each vulnerability.
@router.post("/affected_count")
async def post_affected_count(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    """Check to make sure repo was sent"""
    if not lava_request.repo:
        return api_models.lava_failure("Error! LavaRequest did not recieve a repo!")

    if not lava_request.packages:
        return api_models.lava_failure("Error! No package list was given!")

    return api_models.LavaResponse(
        status=utils.ResponseEnum.complete,
        error=None,
        result=api_models.AffectedCountResponse(
            pkgsAffected=await queries.get_affected_packages(
                lava_request.repo, lava_request.packages
            )
        ),
    )


@router.get("/affected_count")
async def get_affected_count(jobID: str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)


# 2.) Count - Number of packages.
@router.post("/count")
async def post_count(lava_request: api_models.LavaRequest) -> api_models.LavaResponse:
    """Check to make sure repo was sent"""
    if not lava_request.repo:
        return api_models.lava_failure("Error! LavaRequest did not recieve a repo!")

    job = get_queue(QueueName.analysis).enqueue(
        queries.get_package_count,
        lava_request.repo,
        job_timeout=3600,
        result_ttl=3600,
    )

    return api_models.lava_pending(job.get_id())

    return api_models.LavaResponse(
        status=utils.ResponseEnum.complete,
        error=None,
        result=api_models.CountResponse(
            count=await queries.get_package_count(lava_request.repo)
        ),
    )


@router.get("/count")
async def get_count(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.CountResponse(count=job_result)

    job = get_queue(QueueName.analysis).fetch_job(jobID)
    status = job.get_status()
    if status in ["queued", "started", "deferred", "scheduled"]:
        return api_models.lava_pending(jobID)
    elif status in ["stopped", "cancelled", "failed"]:
        return api_models.lava_failure(str(job.exc_info))
    elif status == "finished":
        return api_models.lava_success(parse_result(job.result))
    else:
        return api_models.lava_failure(f"Unrecognized job status: {status}")


# 3.) countDependencies - Returns list of how many other packages each package
# relies on.
@router.post("/count_dependencies")
async def post_count_dependencies(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    if not lava_request.packages:
        return api_models.lava_failure("Error! No package list was given!")

    return api_models.LavaResponse(
        status=utils.ResponseEnum.complete,
        error=None,
        result=api_models.CountDepResponse(
            depList=await queries.get_num_dependencies(lava_request.packages)
        ),
    )


@router.get("/count_dependencies")
async def get_count_dependencies(jobID: str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)


# 4.) countVul - Number of vulnerable packages.
@router.post("/count_vul")
async def post_count_vul(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    """Check to make sure repo was sent"""
    if not lava_request.repo:
        return api_models.lava_failure("Error! LavaRequest did not recieve a repo!")

    return api_models.LavaResponse(
        status=utils.ResponseEnum.complete,
        error=None,
        result=api_models.CountVulResponse(
            vulCount=await queries.get_vulnerable_package_count(lava_request.repo)
        ),
    )


@router.get("/count_vul")
async def get_count_vul(jobID: str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)


# 5.) Depth - Returns list of how deep each vulnerability was from the top level
# package (how many dependencies deep).
@router.post("/depth")
async def post_depth(lava_request: api_models.LavaRequest) -> api_models.LavaResponse:
    if not lava_request.packages:
        return api_models.lava_failure("Error! No package list was given!")

    return api_models.LavaResponse(
        status=utils.ResponseEnum.complete,
        error=None,
        result=api_models.DepthResponse(
            vulDepth=await queries.get_vulnerability_depths(lava_request.packages)
        ),
    )


@router.get("/depth")
async def get_depth(jobID: str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)


# 6.) numDownloads - Returns a list with the number of downloads for each
# package included.
@router.post("/num_downloads")
async def post_num_downloads(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    if not lava_request.packages:
        return api_models.lava_failure("Error! No package list was given!")

    return api_models.LavaResponse(
        status=utils.ResponseEnum.complete,
        error=None,
        response=api_models.NumDownloadsResponse(
            downloads=await queries.get_num_downloads(lava_request.packages)
        ),
    )


@router.get("/num_downloads")
async def get_num_downloads(jobID: str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)


# 7.) Severities - Return list of vulnerable packages and severity for each
# vulnerability.
@router.post("/severities")
async def post_severities(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    if not lava_request.packages:
        return api_models.lava_failure("Error! No package list was given!")

    return api_models.LavaResponse(
        status=utils.ResponseEnum.complete,
        error=None,
        result=api_models.SeveritiesResponse(
            sevList=await queries.get_pkg_severity(lava_request.packages)
        ),
    )


@router.get("/severities")
async def get_severities(jobID: str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)


# 8.) Types - Returns CSV with CWEs and a count of how many vulnerabilities for each CWE
@router.post("/types")
async def post_types(lava_request: api_models.LavaRequest) -> api_models.LavaResponse:
    if not lava_request.packages:
        return api_models.lava_failure("Error! No package list was given!")

    return api_models.LavaResponse(
        status=utils.ResponseEnum.complete,
        error=None,
        result=api_models.TypesResponse(
            cweList=await queries.get_num_types(lava_request.packages)
        ),
    )


@router.get("/types")
async def get_types(jobID: str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)


# 9.) vulnerablePackages - Return list of vulnerable packages.
@router.post("/vulnerable_packages")
async def post_vulnerable_packages(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    """Check to make sure repo was sent"""
    if not lava_request.repo:
        return api_models.lava_failure("Error! LavaRequest did not recieve a repo!")

    return api_models.LavaResponse(
        status=utils.ResponseEnum.complete,
        error=None,
        result=api_models.VulPackagesResponse(
            vulList=await queries.get_all_vulnerable_packages(lava_request.repo)
        ),
    )


@router.get("/vulnerable_packages")
async def get_vulnerable_packages(jobID: str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)

from typing import Any, Callable

from fastapi import APIRouter

from internal import queries
from internal.queues import QueueName, get_queue
from routers import api_models

router = APIRouter(tags=["analysis"])


def _handle_enqueue(func: Callable[..., Any], *args: Any) -> api_models.LavaResponse:
    """Handle enqueueing a function, return pending response."""
    job = get_queue(QueueName.analysis).enqueue(
        func,
        *args,
        job_timeout=3600,
        result_ttl=3600,
    )

    return api_models.lava_pending(job.get_id())


def _handle_get_job(
    job_id: str, result_parser: Callable[[Any], Any]
) -> api_models.LavaResponse:
    """Handle checking a job's status and returning as appropriate."""
    job = get_queue(QueueName.analysis).fetch_job(job_id)
    status = job.get_status()
    if status in ["queued", "started", "deferred", "scheduled"]:
        return api_models.lava_pending(job_id)
    elif status in ["stopped", "cancelled", "failed"]:
        return api_models.lava_failure(str(job.exc_info))
    elif status == "finished":
        return api_models.lava_success(result_parser(job.result))
    else:
        return api_models.lava_failure(f"INTERNAL: Unrecognized job status: {status}")


# 1.) affectedCount - For vulnerabilities found in queried packages
# return a list with the number of packages affected by each vulnerability.
@router.post("/affected_count")
def post_affected_count(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    """Check to make sure repo was sent"""
    if not lava_request.repo:
        return api_models.lava_failure("Error! LavaRequest did not recieve a repo!")

    if not lava_request.packages:
        return api_models.lava_failure("Error! No package list was given!")

    return _handle_enqueue(
        queries.get_affected_packages, lava_request.repo, lava_request.packages
    )


@router.get("/affected_count")
def get_affected_count(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.AffectedCountResponse(pkgsAffected=job_result)

    return _handle_get_job(jobID, parse_result)


# 2.) Count - Number of packages.
@router.post("/count")
def post_count(lava_request: api_models.LavaRequest) -> api_models.LavaResponse:
    """Check to make sure repo was sent"""
    if not lava_request.repo:
        return api_models.lava_failure("Error! LavaRequest did not recieve a repo!")

    return _handle_enqueue(queries.get_package_count, lava_request.repo)


@router.get("/count")
def get_count(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.CountResponse(count=job_result)

    return _handle_get_job(jobID, parse_result)


# 3.) countDependencies - Returns list of how many other packages each package
# relies on.
@router.post("/count_dependencies")
def post_count_dependencies(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    if not lava_request.packages:
        return api_models.lava_failure("Error! No package list was given!")

    return _handle_enqueue(queries.get_num_dependencies, lava_request.packages)


@router.get("/count_dependencies")
def get_count_dependencies(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.CountDepResponse(depList=job_result)

    return _handle_get_job(jobID, parse_result)


# 4.) countVul - Number of vulnerable packages.
@router.post("/count_vul")
def post_count_vul(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    """Check to make sure repo was sent"""
    if not lava_request.repo:
        return api_models.lava_failure("Error! LavaRequest did not recieve a repo!")

    return _handle_enqueue(queries.get_vulnerable_package_count, lava_request.repo)


@router.get("/count_vul")
def get_count_vul(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.CountVulResponse(vulCount=job_result)

    return _handle_get_job(jobID, parse_result)


# 5.) Depth - Returns list of how deep each vulnerability was from the top level
# package (how many dependencies deep).
@router.post("/depth")
def post_depth(lava_request: api_models.LavaRequest) -> api_models.LavaResponse:
    if not lava_request.packages:
        return api_models.lava_failure("Error! No package list was given!")

    return _handle_enqueue(queries.get_vulnerability_depths, lava_request.packages)


@router.get("/depth")
def get_depth(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.DepthResponse(vulDepth=job_result)

    return _handle_get_job(jobID, parse_result)


# 6.) numDownloads - Returns a list with the number of downloads for each
# package included.
@router.post("/num_downloads")
def post_num_downloads(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    if not lava_request.packages:
        return api_models.lava_failure("Error! No package list was given!")

    return _handle_enqueue(queries.get_num_downloads, lava_request.packages)


@router.get("/num_downloads")
def get_num_downloads(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.NumDownloadsResponse(downloads=job_result)

    return _handle_get_job(jobID, parse_result)


# 7.) Severities - Return list of vulnerable packages and severity for each
# vulnerability.
@router.post("/severities")
def post_severities(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    if not lava_request.packages:
        return api_models.lava_failure("Error! No package list was given!")

    return _handle_enqueue(queries.get_pkg_severity, lava_request.packages)


@router.get("/severities")
def get_severities(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.SeveritiesResponse(sevList=job_result)

    return _handle_get_job(jobID, parse_result)


# 8.) Types - Returns CSV with CWEs and a count of how many vulnerabilities for each CWE
@router.post("/types")
def post_types(lava_request: api_models.LavaRequest) -> api_models.LavaResponse:
    if not lava_request.packages:
        return api_models.lava_failure("Error! No package list was given!")

    return _handle_enqueue(queries.get_num_types, lava_request.packages)


@router.get("/types")
def get_types(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.TypesResponse(cweList=job_result)

    return _handle_get_job(jobID, parse_result)


# 9.) vulnerablePackages - Return list of vulnerable packages.
@router.post("/vulnerable_packages")
def post_vulnerable_packages(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    """Check to make sure repo was sent"""
    if not lava_request.repo:
        return api_models.lava_failure("Error! LavaRequest did not recieve a repo!")

    return _handle_enqueue(queries.get_all_vulnerable_packages, lava_request.repo)


@router.get("/vulnerable_packages")
def get_vulnerable_packages(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.VulPackagesResponse(vulList=job_result)

    return _handle_get_job(jobID, parse_result)


# 10.)
@router.post("/vulnerability_paths")
def post_vulnerability_paths(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    if not lava_request.repo:
        return api_models.lava_failure("Error! LavaRequest did not recieve a repo!")
    if not lava_request.packages:
        return api_models.lava_failure("Error! No package list was given!")

    return _handle_enqueue(queries.get_vulnerability_paths, lava_request.packages)


@router.get("/vulnerability_paths")
def get_vulnerability_paths(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.VulPathResponse(vulPath=job_result)

    return _handle_get_job(jobID, parse_result)


# 11.) allPackages - Return list of all packages.
@router.post("/all_packages")
def post_all_pkgs() -> api_models.LavaResponse:

    return _handle_enqueue(queries.get_all_pkgs)


@router.get("/all_packages")
def get_all_pkgs(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.AllPackagesResponse(pkgs=job_result)

    return _handle_get_job(jobID, parse_result)


# 12.) treeDepth - Return the depth of the dependency tree.
@router.post("/tree_depth")
def post_tree_depth(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    """Check to make sure hash was sent"""
    if not lava_request.packages:
        return api_models.lava_failure("Error! LavaRequest did not recieve a package!")

    return _handle_enqueue(queries.get_tree_depth, lava_request.packages)


@router.get("/tree_depth")
def get_tree_depth(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.TreeDepthsResponse(depths=job_result)

    return _handle_get_job(jobID, parse_result)


@router.post("/all_package_dependency_count")
def post_all_package_dependency_count(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:

    return _handle_enqueue(queries.get_all_package_dependency_num)


@router.get("/all_package_dependency_count")
def get_tree_depth(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.allPackageDependenciesResponse(depCount=job_result)

    return _handle_get_job(jobID, parse_result)


# 13.) treeBreadth - Return the breadth of the dependency tree.
@router.post("/tree_breadth")
def post_tree_breadth(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    """Check to make sure hash was sent"""
    if not lava_request.packages:
        return api_models.lava_failure("Error! LavaRequest did not recieve a package!")

    return _handle_enqueue(queries.get_tree_breadth, lava_request.packages)


@router.get("/tree_breadth")
def get_tree_breadth(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.TreeBreadthsResponse(breadths=job_result)

    return _handle_get_job(jobID, parse_result)


@router.post("/dependency_stats")
def post_dependency_stats(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    """Check to make sure repo was sent"""
    if not lava_request.repo:
        #return _handle_enqueue(queries.get_dependency_stats_all)
        return api_models.lava_failure("Error! LavaRequest did not recieve a repo!")

    return _handle_enqueue(queries.get_dependency_stats, lava_request.repo)


@router.get("/dependency_stats")
def get_vulnerable_packages(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.DependencyStats(stats=job_result)

    return _handle_get_job(jobID, parse_result)



@router.post("/num_downloads")
def post_num_downloads(
    lava_request: api_models.LavaRequest,
) -> api_models.LavaResponse:
    """Check to make sure hash was sent"""
    if not lava_request.packages:
        return api_models.lava_failure("Error! LavaRequest did not recieve a package!")

    return _handle_enqueue(queries.get_num_downloads, lava_request.packages)


@router.get("/num_downloads")
def get_num_downloads(jobID: str) -> api_models.LavaResponse:
    def parse_result(job_result: Any) -> Any:
        return api_models.NumDownloadsResponse(downloads=job_result)

    return _handle_get_job(jobID, parse_result)

from fastapi import APIRouter

from lavi_worker import internal
from lavi_worker.routers import api_models


router = APIRouter()


@router.post("/find_vulnerabilities")
def find_vulnerabilities(
    find_vuln_request: api_models.FindVulnRequest,
) -> api_models.FindVulnResponse:
    """Find vulnerabilities given a dependency and version."""
    # Get CVE ids from the database
    cve_ids = internal.find_vulnerabilities_simple(
        find_vuln_request.repo,
        find_vuln_request.package,
        find_vuln_request.version,
    )

    # Format response
    return api_models.FindVulnResponse(vulns=cve_ids)

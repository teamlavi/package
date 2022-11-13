from fastapi import APIRouter

from lavi_worker.internal import queries
from lavi_worker.routers import api_models


router = APIRouter(tags=["external"])


@router.post("/find_vulnerabilities")
async def find_vulnerabilities(
    find_vuln_request: api_models.FindVulnRequest,
) -> api_models.FindVulnResponse:
    """Find vulnerabilities given a dependency and version."""
    # Get CVE ids from the database
    cve_ids = await queries.find_vulnerabilities_simple(
        find_vuln_request.repo,
        find_vuln_request.package,
        find_vuln_request.version,
    )

    # Format response
    return api_models.FindVulnResponse(vulns=cve_ids)


@router.post("/find_vulnerable_versions")
async def find_vulnerable_versions(
    find_vuln_vers_request: api_models.FindVulnVersRequest,
) -> api_models.FindVulnVersResponse:
    """Find vulnerabilities given a dependency and version."""
    # Get CVE ids from the database
    versions = await queries.find_vuln_versions(
        find_vuln_vers_request.repo,
        find_vuln_vers_request.package,
    )
    print("empty" if not versions else type(versions[0]))
    # Format response
    return api_models.FindVulnVersResponse(vers=versions)

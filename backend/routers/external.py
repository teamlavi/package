from fastapi import APIRouter

from internal import queries
from routers import api_models
from typing import List

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

    # Format response
    return api_models.FindVulnVersResponse(vers=versions)


@router.post("/find_vulnerabilities_id_list")
async def find_vulnerabilities_id_list(
    find_all_vuln_request: api_models.FindVulnsIdListRequest,
) -> api_models.FindVulnsIdListResponse:
    """Find all vulnerabilities given a list of package universal hash ids."""

    # get CVE data from the database
    async def format_cve(pkgId: str) -> List[api_models.CveResponse]:
        cves = await queries.find_full_vulnerabilities_id(pkgId)
        return [
            api_models.CveResponse(
                cveId=cve.cve_id,
                severity=cve.severity,
                url=cve.url,
                title=cve.description,
                patchedIn=cve.first_patched_vers,
            )
            for cve in cves
        ]

    return api_models.FindVulnsIdListResponse(
        vulns={i: await format_cve(i) for i in find_all_vuln_request.ids}
    )

from fastapi import APIRouter


from lavi_worker.routers import api_models


router = APIRouter()


@router.post("/find_vulnerability")
def find_vulnerability(
    find_vuln_request: api_models.FindVulnRequest,
) -> api_models.FindVulnResponse:
    """Find vulnerabilities given a dependency and version."""
    return api_models.FindVulnResponse(vulns=[])

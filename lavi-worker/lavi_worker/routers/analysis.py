from fastapi import APIRouter

from lavi_worker.routers import api_models

router = APIRouter(tags=["analysis"])

#1.) ===== affectedCount - For vulnerabilities found in queried packages return a list with the number of packages affected by each vulnerability. =====
@router.post("/affected_count")
async def affected_count(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/affected_count")
async def affected_count(jobID : str) -> api_models.AffectedCountResponse:
    return api_models.AffectedCountResponse(pkgsAffected={"dumbCVEId": 0})



#2.) ===== Count - Number of packages. =====
@router.post("/count")
async def count(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/count")
async def count(jobID : str) -> api_models.CountResponse:
    return api_models.CountResponse(count=0)



#3.) ===== countDependencies - Returns list of how many other packages each package relies on. =====
@router.post("/count_dependencies")
async def count_dependencies(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/count_dependencies")
async def count_dependencies(jobID : str) -> api_models.CountDepResponse:
    return api_models.CountDepResponse(depList={"packageID123": 0})



#4.) ===== countVul - Number of vulnerable packages. =====
@router.post("/count_vul")
async def count_vul(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/count_vul")
async def count_vul(jobID : str) -> api_models.CountVulResponse:
    return api_models.CountVulResponse(vulCount=0)



#5.) ===== Depth - Returns list of how deep each vulnerability was from the top level package (how many dependencies deep). =====
@router.post("/depth")
async def depth(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/depth")
async def depth(jobID : str) -> api_models.DepthResponse:
    return api_models.DepthResponse(vulDepth={"Some CVE ID": 0})



#6.) ===== numDownloads - Returns a list with the number of downloads for each package included. =====
@router.post("/num_downloads")
async def num_downloads(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/num_downloads")
async def num_downloads(jobID : str) -> api_models.NumDownloadsResponse:
    return api_models.NumDownloadsResponse(downloads={"Some package ID" : 0})



#7.) ===== Severities - Return list of vulnerable packages and severity for each vulnerability. =====
@router.post("/severities")
async def severities(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/severities")
async def severities(jobID : str) -> api_models.SeveritiesResponse:
    return api_models.SeveritiesResponse(sevList={"vulPackageId": "severityType"})


#8.) ===== Types - Returns CSV with CWEs and a count of how many vulnerabilities for each CWE =====
@router.post("/types")
async def types(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/types")
async def types(jobID : str) -> api_models.TypesResponse:
    return api_models.TypesResponse(cweList={"CWEID":0})


#9.) ===== vulnerablePackages - Return list of vulnerable packages. =====
@router.post("/vulnerable_packages")
async def vulnerable_packages(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/vulnerable_packages")
async def vulnerable_packages(jobID : str) -> api_models.VulPackagesResponse:
    return api_models.VulPackagesResponse(vulList=["thisPackageIsVulID"])






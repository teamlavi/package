from fastapi import APIRouter

from lavi_worker.routers import api_models
from lavi_worker import utils

router = APIRouter(tags=["analysis"])

#1.) ===== affectedCount - For vulnerabilities found in queried packages return a list with the number of packages affected by each vulnerability. =====
@router.post("/affected_count")
async def affected_count(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/affected_count")
async def affected_count(jobID : str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)



#2.) ===== Count - Number of packages. =====
@router.post("/count")
async def count(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/count")
async def count(jobID : str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)




#3.) ===== countDependencies - Returns list of how many other packages each package relies on. =====
@router.post("/count_dependencies")
async def count_dependencies(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/count_dependencies")
async def count_dependencies(jobID : str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)




#4.) ===== countVul - Number of vulnerable packages. =====
@router.post("/count_vul")
async def count_vul(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/count_vul")
async def count_vul(jobID : str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)




#5.) ===== Depth - Returns list of how deep each vulnerability was from the top level package (how many dependencies deep). =====
@router.post("/depth")
async def depth(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/depth")
async def depth(jobID : str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)




#6.) ===== numDownloads - Returns a list with the number of downloads for each package included. =====
@router.post("/num_downloads")
async def num_downloads(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/num_downloads")
async def num_downloads(jobID : str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)




#7.) ===== Severities - Return list of vulnerable packages and severity for each vulnerability. =====
@router.post("/severities")
async def severities(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/severities")
async def severities(jobID : str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)



#8.) ===== Types - Returns CSV with CWEs and a count of how many vulnerabilities for each CWE =====
@router.post("/types")
async def types(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/types")
async def types(jobID : str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)



#9.) ===== vulnerablePackages - Return list of vulnerable packages. =====
@router.post("/vulnerable_packages")
async def vulnerable_packages(lava_request : api_models.LavaRequest) -> str:
    return "job ID"

@router.get("/vulnerable_packages")
async def vulnerable_packages(jobID : str) -> api_models.LavaResponse:
    return api_models.LavaResponse(status=utils.ResponseEnum.pending)

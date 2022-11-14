from fastapi import APIRouter

from lavi_worker.routers import api_models

router = APIRouter(tags=["analysis"])

#1.) affectedCount - For vulnerabilities found in queried packages return a list with the number of packages affected by each vulnerability.


#2.) Count - Number of packages.


#3.) countDependencies - Returns list of how many other packages each package relies on.


#4.) countVul - Number of vulnerable packages.


#5.) Depth - Returns list of how deep each vulnerability was from the top level package (how many dependencies deep).


#6.) numDownloads - Returns a list with the number of downloads for each package included.


#7.) Severities - Return list of vulnerable packages and severity for each vulnerability.


#8.) Types - Returns CSV with CWEs and a count of how many vulnerabilities for each CWE


#9.) vulnerablePackages - Return list of vulnerable packages.






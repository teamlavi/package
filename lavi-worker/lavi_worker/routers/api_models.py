from typing import List, Dict

from pydantic import BaseModel


from lavi_worker.utils import RepoEnum


class DeleteVulnRequest(BaseModel):
    repo_name: str
    pkg_name: str
    pkg_vers: str
    cve_id: str

    class Config:
        schema_extra = {
            "example": {
                "repo_name": "pip",
                "pkg_name": "django",
                "pkg_vers": "3.2.0",
                "cve_id": "CVE-2022-41323",
            }
        }


class FindVulnRequest(BaseModel):
    repo: RepoEnum
    package: str
    version: str

    class Config:
        schema_extra = {
            "example": {
                "repo": "pip",
                "package": "django",
                "version": "3.2.0",
            }
        }


class FindVulnVersRequest(BaseModel):
    repo: RepoEnum
    package: str


class FindVulnResponse(BaseModel):
    vulns: List[str]  # List of CVE id strings


class FindVulnVersResponse(BaseModel):
    vers: List[str]  # List of vulnerable versions


class PackageVers(BaseModel):
    repo_name: str
    pkg_name: str
    major_vers: int
    minor_vers: int
    patch_vers: int
    num_downloads: int
    s3_bucket: str

    class Config:
        schema_extra = {
            "example": {
                "repo_name": "test",
                "pkg_name": "test",
                "major_vers": 1,
                "minor_vers": 1,
                "patch_vers": 1,
                "num_downloads": 0,
                "s3_bucket": "0",
            }
        }


class FindVulnsIdListRequest(BaseModel):
    ids: List[str]


class CveResponse(BaseModel):
    cveId: str
    severity: str | None
    url: str


class FindVulnsIdListResponse(BaseModel):
    vulns: Dict[str, List[CveResponse]]


class InsertVulnRequest(BaseModel):
    cve_id: str
    url: str
    repo_name: str
    pkg_name: str
    pkg_vers: str
    severity: str | None = None
    description: str | None = None
    cwe: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "cve_id": "CVE-2022-41323",
                "url": "https://github.com/advisories/GHSA-qrw5-5h28-6cmg",
                "repo_name": "pip",
                "pkg_name": "django",
                "pkg_vers": "3.2.0",
                "severity": "High",
                "description": "DOS vulnerability in internationalized URLs",
                "cwe": None,
            }
        }

#analysis.py Models:

#LAVA Request
class LavaRequest(BaseModel):
    repo: RepoEnum
    packages: List[str] | None  #Query with only a packages in list. Can optionally include a version number. If no version number is included, the most recent release will be used.
    offset: int | None          #offset on how many results the user wants to skip(ex: offset=2 would skip the first 2 results)
    limit: int | None           #limit on how many results the user wants to display (ex: limit=5 would only show the next 5 results)
    minDownloads: int | None    #only include packages with minDownloads package downloads and above (inclusive)
    level: LevelEnum | None     #include direct, indirect, or all vulnerabilities.Includes ALL by default if None
    status: StatusEnum | None   #include active, patched or all vulnerabilities. Includes only ACTIVE vulnerabilities by default if None

#LAVA Responses

#GET Response
class LavaResponse(BaseModel):
    status: ResponseEnum    #Options: complete, failure, or pending
    error: str | None       #returns error message in case status=failure
    result: Any             #If status=complete, will return job response. will be one of the responses below  

#job finished successfully Responses
class AffectedCountResponse(BaseModel):
    pkgsAffected: Dict[str, int]  #CVE id -> Number of packages affected

class CountResponse(BaseModel):
    count: int #Total number of packages in LAVI database

class CountDepResponse(BaseModel):
    depList: Dict[str, int] #package id -> Number of dependencies for this package

class CountVulResponse(BaseModel):
    vulCount: int #Total number of Vulnerabilities found in the packages in our database

class DepthResponse(BaseModel):
    vulDepth: Dict[str, int] #CVE id -> Vulnerability depth from root package

class NumDownloadsResponse(BaseModel):
    downloads: Dict[str, int] #Package id -> Number of package downloads

class SeveritiesResponse(BaseModel):
    sevList: Dict[str, str] #Vulnerable package id -> CVE Serverity type

class TypesResponse(BaseModel):
    cweList: Dict[str, int] #CWE id -> how many Vulnerabilities for this CWE

class VulPackagesResponse(BaseModel):
    vulList: List[str] #List of all the package ids that are vulnerable in our database


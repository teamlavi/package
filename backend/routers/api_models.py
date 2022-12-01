from typing import Any

from pydantic import BaseModel

from utils.utils import LevelEnum, RepoEnum, ResponseEnum, StatusEnum


class InsertTreeData(BaseModel):
    tree: str


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
    vulns: list[str]  # List of CVE id strings


class FindVulnVersResponse(BaseModel):
    vers: list[str]  # List of vulnerable versions


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
    ids: list[str]


class CveResponse(BaseModel):
    cveId: str
    severity: str | None
    url: str
    title: str | None
    patched_in: str | None


class FindVulnsIdListResponse(BaseModel):
    vulns: dict[str, list[CveResponse]]


class InsertVulnRequest(BaseModel):
    cve_id: str
    url: str
    repo_name: str
    pkg_name: str
    pkg_vers: str
    severity: str | None = None
    description: str | None = None
    cwe: str | None = None
    first_patched_vers: str | None = None

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


# analysis.py Models:

# LAVA Request
class LavaRequest(BaseModel):
    # repo
    repo: RepoEnum
    # Query with only a packages in list.
    # Can optionally include a version number.
    # If no version number is included, the most recent release will be used.
    packages: list[str] | None
    # offset on how many results the user wants to
    # skip(ex: offset=2 would skip the first 2 results)
    offset: int | None
    # limit on how many results the user wants to
    # display (ex: limit=5 would only show the next 5 results)
    limit: int | None
    # only include packages with minDownloads package downloads
    # and above (inclusive)
    minDownloads: int | None
    # include direct, indirect, or all vulnerabilities.
    # Includes ALL by default if None
    level: LevelEnum | None
    # include active, patched or all vulnerabilities.
    # Includes only ACTIVE vulnerabilities by default if None
    status: StatusEnum | None


# LAVA Responses

# GET Response
class LavaResponse(BaseModel):
    # Options: complete, failure, or pending
    status: ResponseEnum
    # returns error message in case status=failure
    error: str | None
    # If status=complete, will return job response. will be one of the responses below
    result: Any


def lava_failure(error_text: str) -> LavaResponse:
    return LavaResponse(status=ResponseEnum.failure, error=error_text, result=None)


# job finished successfully Responses
class AffectedCountResponse(BaseModel):
    # CVE id -> Number of packages affected
    pkgsAffected: dict[str, int]


class CountResponse(BaseModel):
    # Total number of packages in LAVI database
    count: int


class CountDepResponse(BaseModel):
    # package id -> Number of dependencies for this package
    depList: dict[str, int]


class CountVulResponse(BaseModel):
    # Total number of Vulnerabilities found in the packages in our database
    vulCount: int


class DepthResponse(BaseModel):
    # CVE id -> Vulnerability depth from root package
    vulDepth: dict[str, dict[str, list[int]]]


class NumDownloadsResponse(BaseModel):
    # Package id -> Number of package downloads
    downloads: dict[str, int]


class SeveritiesResponse(BaseModel):
    # Vulnerable package id -> CVE Serverity type
    sevList: dict[str, list[str]]


class TypesResponse(BaseModel):
    # CWE id -> how many Vulnerabilities for this CWE
    cweList: dict[str, int]


class VulPackagesResponse(BaseModel):
    # List of all the package ids that are vulnerable in our database
    vulList: list[str]

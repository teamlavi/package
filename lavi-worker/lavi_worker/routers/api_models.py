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


class FindVulnResponse(BaseModel):
    vulns: List[str]  # List of CVE id strings


class PackageVersRange(BaseModel):
    repo_name: str
    pkg_name: str
    vers_range: str

    class Config:
        schema_extra = {
            "example": {
                "repo_name": "npm",
                "pkg_name": "lodash",
                "vers_range": ">= 0.0.1",
            },
        }


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

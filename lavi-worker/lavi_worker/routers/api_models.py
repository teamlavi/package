from typing import List

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

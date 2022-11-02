from typing import List

from pydantic import BaseModel


from lavi_worker.utils import RepoEnum


class Vuln(BaseModel):
    cve_id: str
    severity: str


class FindVulnRequest(BaseModel):
    repo: RepoEnum
    package: str
    version: str


class FindVulnResponse(BaseModel):
    vulns: List[Vuln]

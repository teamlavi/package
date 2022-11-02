from typing import List

from pydantic import BaseModel


from lavi_worker.utils import RepoEnum


class FindVulnRequest(BaseModel):
    repo: RepoEnum
    package: str
    version: str


class FindVulnResponse(BaseModel):
    vulns: List[str]  # List of CVE id strings

from base64 import b64decode
from typing import Dict, List

from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse
import orjson

from lavi_worker.internal import updates
from lavi_worker.routers import api_models


router = APIRouter(tags=["internal"])


@router.post("/trigger_vuln_scraper")
async def trigger_vuln_scraper() -> Response:
    """Trigger the scraper to refresh the database."""
    await updates.scrape_vulnerabilities()
    return Response(status_code=200)


@router.post("/insert_vuln")
async def insert_vuln(insert_vuln_request: api_models.InsertVulnRequest) -> bool:
    """Insert a single vulnerability."""
    return await updates.insert_single_vulnerability(**insert_vuln_request.dict())


@router.post("/insert_vers")
async def insert_vers(package_ver_request: api_models.PackageVers) -> Response:
    await updates.insert_single_package_version(**package_ver_request.dict())
    return Response(status_code=200)


@router.get("/query_vers")
async def query_vers(repo_name: str, pkg_name: str, vers_range: str) -> list[str]:
    lst = await updates.vers_range_to_list(repo_name, pkg_name, vers_range)
    lst.sort()  # not necessary for most operation but nice for display
    return lst


@router.post("/delete_vuln")
async def delete_vuln(delete_vuln_request: api_models.DeleteVulnRequest) -> Response:
    """Delete a single vulnerability."""
    await updates.delete_single_vulnerability(**delete_vuln_request.dict())
    return Response(status_code=200)


@router.post("/trigger_npm_scrapper")
async def trigger_npm_scrapper() -> Response:
    await updates.scrape_npm_packages()
    return Response(status_code=200)


@router.post("/trigger_pip_scrapper")
async def trigger_pip_scrapper() -> Response:
    await updates.scrape_pip_packages()
    return Response(status_code=200)


@router.post("/database/clear")
async def clear_database() -> Response:
    """Clear all rows of the database tables."""
    await updates.clear_database()
    return Response(status_code=200)


@router.post("/database/nuke")
async def nuke_database() -> Response:
    """Completely delete all our database tables."""
    await updates.nuke_database()
    return Response(status_code=200)


@router.post("/database/init")
async def initialize_database() -> Response:
    """Freshly initialize the database."""
    await updates.initialize_database()
    return Response(status_code=200)


@router.get("/database/init", response_class=PlainTextResponse)
async def get_database_initialized() -> str:
    """Check whether the database is initialized."""
    return "true" if await updates.is_db_initialized() else "false"  # no cap


@router.get("/database/size", response_class=PlainTextResponse)
async def get_table_size(table: str = "cves") -> str:
    """Get the size of the database."""
    size = await updates.table_size(table=table)
    return str(size)


@router.post("/insert_tree")
async def insert_tree(
    tree: api_models.InsertTreeData,
    repo: str,
    package: str,
    major_vers: str,
    minor_vers: str,
    patch_vers: str,
) -> Response:
    """Insert a tree into the database"""
    unpacked: Dict[str, List[str]] 
    unpacked = orjson.loads(b64decode(tree.tree.encode()).decode())
    print(f"LOOK HERE DUMMY {unpacked}")
    return Response(status_code=200)

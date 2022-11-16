from base64 import b64decode
from typing import Dict, List

from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse
import orjson

from lavi_worker.internal import updates
from lavi_worker.routers import api_models
from lavi_worker.utils import compress_tree, decompress_tree


router = APIRouter(tags=["internal"])


@router.post("/trigger_vuln_scraper")
async def trigger_vuln_scraper(repository: str) -> Response:
    """Trigger the scraper to refresh the database."""
    await updates.scrape_vulnerabilities(repository)
    return Response(status_code=200)


@router.post("/insert_vuln")
async def insert_vuln(insert_vuln_request: api_models.InsertVulnRequest) -> bool:
    """Insert a single vulnerability."""
    return await updates.insert_single_vulnerability(**insert_vuln_request.dict())


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


@router.post("/database/clear")
async def clear_database(verify_code: str) -> Response:
    """Clear all rows of the database tables."""
    if verify_code != "for real clear":
        raise Exception("Invalid verify code")
    await updates.clear_database()
    return Response(status_code=200)


@router.post("/database/nuke")
async def nuke_database(verify_code: str) -> Response:
    """Completely delete all our database tables."""
    if verify_code != "for real nuke":
        raise Exception("Invalid verify code")
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
    print(f"insert tree endpoint got tree with {len(unpacked)} nodes")

    compressed_tree = compress_tree(unpacked)
    await updates.insert_single_dependency_tree(
        repo, package, f"{major_vers}.{minor_vers}.{patch_vers}", compressed_tree
    )
    return Response(status_code=200)


@router.get("/get_tree")
async def get_tree(repo: str, package: str, version: str) -> str | None:
    compressed_tree = await updates.get_single_dependency_tree(repo, package, version)
    if compressed_tree is None:
        return None
    else:
        return str(decompress_tree(compressed_tree))


@router.get("/get_table_storage_size")
async def get_table_storage_size(table_name: str = "dependencies") -> str:
    return await updates.get_table_storage_size(table_name)

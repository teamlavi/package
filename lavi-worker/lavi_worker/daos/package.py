from lavi_worker.daos.database import Transaction
import httpx
import json
from typing import List


class SemVer:
    major_vers: int
    minor_vers: int
    patch_vers: int

    def __init__(
        self, major_vers: int | str, minor_vers: int | str, patch_vers: int | str
    ):
        self.major_vers = int(major_vers)
        self.minor_vers = int(minor_vers)
        self.patch_vers = int(patch_vers)

    def __repr__(self):
        return f"{self.major_vers}.{self.minor_vers}.{self.patch_vers}"


async def create(
    tx: Transaction,
    repo_name: str,
    pkg_name: str,
    major_vers: int,
    minor_vers: int,
    patch_vers: int,
    num_downloads: int | None,
    s3_bucket: str | None,
) -> None:
    return


async def list_package_versions_npm(
    package: str, limit: int | None = None
) -> List[SemVer]:
    """Given a repository and package, return a list of available versions."""
    try:
        resp = httpx.get(
            f"https://registry.npmjs.org/{package}",
        )
        resp.raise_for_status()
        version_list = list(json.loads(resp.text)["versions"])
        if isinstance(version_list, str) and "-" in version_list:
            return []
        elif isinstance(version_list, str):
            version_list = [version_list]
        elif isinstance(version_list[0], list):
            version_list = version_list[0]

        res_versions: List[SemVer] = []

        for vers in version_list:
            if limit is not None and len(res_versions) >= limit:
                break
            elif vers.replace(".", "").isnumeric():
                # checks if there are characters in version number
                while vers.count(".") < 2:
                    # if no minor or patch version included
                    vers += ".0"
                res_versions.append(*vers.split("."))
        return res_versions
    except Exception as e:
        print(f"Unable to interpret versions for {package}", e)
        return []


async def list_package_versions_pip(
    package: str, limit: int | None = None
) -> List[SemVer]:
    """Given a repository and package, return a list of available versions."""
    page2 = f"https://pypi.org/pypi/{package}/json"

    all_versions = json.loads(httpx.get(page2).text)["releases"].keys()
    res_versions: List[str] = []
    for vers in all_versions:
        if limit is not None and len(res_versions) >= limit:
            break
        elif vers.replace(".", "").isnumeric():
            # checks if there are characters in version number
            while vers.count(".") < 2:
                # if no minor or patch version included
                vers += ".0"
            res_versions.append(vers)
    return res_versions


async def get_vers_less_than_eql(
    tx: Transaction | None,
    repo_name: str,
    pkg_name: str,
    major_vers: int | str,
    minor_vers: int | str,
    patch_vers: int | str,
) -> list[str]:
    if repo_name == "npm":
        all_vers = await list_package_versions_npm(pkg_name)
    elif repo_name == "pip":
        all_vers = await list_package_versions_npm(pkg_name)
    else:
        all_vers = []
    res: List[str] = []
    for vers in all_vers:
        if vers.major_vers < int(major_vers):
            res.append(str(vers))
        elif vers.major_vers == int(major_vers) and vers.minor_vers < int(minor_vers):
            res.append(str(vers))
        elif (
            vers.major_vers == int(major_vers)
            and vers.minor_vers == int(minor_vers)
            and vers.patch_vers < int(patch_vers)
        ):
            res.append(str(vers))
    return res


async def get_vers_less_than(
    tx: Transaction,
    repo_name: str,
    pkg_name: str,
    major_vers: str,
    minor_vers: str,
    patch_vers: str,
) -> list[str]:
    return []


async def get_vers_greater_than_eql(
    tx: Transaction,
    repo_name: str,
    pkg_name: str,
    major_vers: str,
    minor_vers: str,
    patch_vers: str,
) -> list[str]:
    return []


async def get_vers_greater_than(
    tx: Transaction,
    repo_name: str,
    pkg_name: str,
    major_vers: str,
    minor_vers: str,
    patch_vers: str,
) -> list[str]:
    return []


async def vers_exists(
    tx: Transaction,
    repo_name: str,
    pkg_name: str,
    major_vers: str | int,
    minor_vers: str | int,
    patch_vers: str | int,
) -> bool:
    return []


async def get_row_count(tx: Transaction) -> int:
    async with tx.cursor() as cur:
        await cur.execute("SELECT COUNT(*) FROM package")
        row = await cur.fetchone()
        return row[0]  # type: ignore


async def drop_all_rows(tx: Transaction) -> None:
    """Drop all table rows."""
    async with tx.cursor() as cur:
        await cur.execute("TRUNCATE package RESTART IDENTITY CASCADE")


async def get_table_storage_size(tx: Transaction) -> str:
    async with tx.cursor() as cur:
        await cur.execute("SELECT pg_size_pretty(pg_total_relation_size('package'))")
        row = await cur.fetchone()
        return row[0]  # type: ignore

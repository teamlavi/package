from typing import List

from repo_worker.utils import TreeNode
from repo_worker.utils import generate_dependency_tree
import json
import httpx
import os


class PipScraper(object):
    @staticmethod
    def list_packages(limit: int | None = None) -> List[str]:
        """Given a repository, return a list of its packages."""
        packages: List[str] = []
        client = httpx.Client(follow_redirects=True)
        page = client.get(
            "https://pypi.org/simple"
        )  # Getting page HTML through request
        # print(page.text)
        stringHelper = page.text.replace(" ", "")
        links = stringHelper.split("\n")
        for pkg_name in links[7:-2]:  # -2 for this
            if limit is not None and len(packages) >= limit:
                break
            try:
                # E203: formatter puts whitespace before : but flake8 doesn't want it
                pkg_name = pkg_name[
                    pkg_name.find(">") + 1 : pkg_name.rfind("<")  # noqa: E203
                ]
                packages.append(pkg_name)
            except Exception:
                pass
        return packages

    @staticmethod
    def list_package_versions(package: str, limit: int | None = None) -> List[str]:
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

    @staticmethod
    def generate_dependency_tree(package: str, version: str) -> TreeNode:
        """Given a repository, package, and version, return a conflict-free dep tree."""
        cmd = f'lavi poetry --package="{package}" --version="{version}" --no-scan -w'
        # TODO if poetry fails try running with pip
        result = os.popen(cmd).read()
        print(result)
        if "open poetry.lock: no such file or directory" in result:
            # TODO: what to return?
            return TreeNode(package="", repo="", version="")
        with open("cds.json") as f:
            cds = json.loads(f.read())
        return generate_dependency_tree(cds)

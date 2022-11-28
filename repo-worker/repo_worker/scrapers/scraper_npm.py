from typing import List

from repo_worker.utils import TreeNode
from repo_worker.utils import generate_dependency_tree
import os
import json
import httpx


class NpmScraper(object):
    @staticmethod
    def list_packages(limit: int | None = None) -> List[str]:
        """Given a repository, return a list of its packages."""
        if limit == 1000:
            # Just get top packages for now
            with open("repo_worker/data/top_npm.txt", "r") as top_file:
                packages = top_file.readlines()
            packages = [package.strip() for package in packages if package.strip()]
        else:
            # install all the package names
            os.system("npm i -g all-the-package-names")
            packages = os.popen("all-the-package-names").read().split()
        if limit is None:
            return packages
        else:
            return packages[:limit]

    @staticmethod
    def list_package_versions(package: str, limit: int | None = None) -> List[str]:
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

            res_versions: List[str] = []

            for vers in version_list:
                if limit is not None and len(res_versions) >= limit:
                    break
                elif vers.replace(".", "").isnumeric():
                    # checks if there are characters in version number
                    while vers.count(".") < 2:
                        # if no minor or patch version included
                        vers += ".0"
                    res_versions.append(vers)
            return res_versions
        except Exception as e:
            print(f"Unable to interpret versions for {package}", e)
            return []

    @staticmethod
    def generate_dependency_tree(package: str, version: str) -> TreeNode:
        """Given a repository, package, and version, return a conflict-free dep tree."""

        cmd = f'lavi npm --package="{package}" --version="{version}" --no-scan -w'
        os.popen(cmd).read()
        with open("cds.json") as f:
            cds = json.loads(f.read())
        return generate_dependency_tree(cds)

from typing import List

from repo_worker.utils import TreeNode
import os
import json

class NpmScraper(object):
    @staticmethod
    def list_packages(limit: int | None = None) -> List[str]:
        """Given a repository, return a list of its packages."""
        # install all the package names
        os.system('npm i -g all-the-package-names')
        package_list = os.popen('all-the-package-names').read().split()
        if limit is None:
            return package_list
        else:
            return package_list[:limit]

    @staticmethod
    def list_package_versions(package: str, limit: int | None = None) -> List[str]:
        """Given a repository and package, return a list of available versions."""
        try:
            cmd = "npm view " + package + "@* version --json"
            request = os.popen(cmd).read()
            version_list = json.loads(request)
            if isinstance(version_list, str) and "-" in version_list:
                return []
            elif isinstance(version_list, str):
                version_list = [version_list]
            elif isinstance(version_list[0], list):
                version_list = version_list[0]

            res_versions:List[str] = []

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
        raise NotImplementedError

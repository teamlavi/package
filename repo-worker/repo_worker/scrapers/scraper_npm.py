from typing import List

from repo_worker.utils import TreeNode


class NpmScraper(object):
    @staticmethod
    def list_packages(limit: int | None = None) -> List[str]:
        """Given a repository, return a list of its packages."""
        raise NotImplementedError

    @staticmethod
    def list_package_versions(package: str, limit: int | None = None) -> List[str]:
        """Given a repository and package, return a list of available versions."""
        raise NotImplementedError

    @staticmethod
    def generate_dependency_tree(package: str, version: str) -> TreeNode:
        """Given a repository, package, and version, return a conflict-free dep tree."""
        # TODO: install lavi-cli
        for pkg_name in ["lodash"]:
            pkg_vers = await get_most_recent_vers("npm", pkg_name)
            cmd = f'lavi npm --package="{pkg_name}" --version="{pkg_vers}" -w'
            request = os.popen(cmd).read()
            print(request)
            with open("cds.json") as f:
                print(f.read())
                await insert_single_dependency_tree("npm", pkg_name, pkg_vers, f.read())

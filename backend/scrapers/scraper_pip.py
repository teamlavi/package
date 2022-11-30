import json
import os
import sys

import httpx

from utils.tree_node import TreeNode, generate_dependency_tree


class PipScraper(object):
    @staticmethod
    def list_packages(partial: bool) -> list[str]:
        """Given a repository, return a list of its packages."""
        packages: list[str]
        if partial:
            # Just get top packages for now
            with open("data/top_pip.txt", "r") as top_file:
                packages = top_file.readlines()
            packages = [package.strip() for package in packages if package.strip()]
        else:
            packages = []
            client = httpx.Client(follow_redirects=True)
            page = client.get(
                "https://pypi.org/simple"
            )  # Getting page HTML through request
            # print(page.text)
            stringHelper = page.text.replace(" ", "")
            links = stringHelper.split("\n")
            for pkg_name in links[7:-2]:  # -2 for this
                try:
                    # E203: formatter puts whitespace before : but flake8 doesn't like
                    pkg_name = pkg_name[
                        pkg_name.find(">") + 1 : pkg_name.rfind("<")  # noqa: E203
                    ]
                    packages.append(pkg_name)
                except Exception:
                    pass
        return packages

    @staticmethod
    def list_package_versions(package: str, limit: int | None = None) -> list[str]:
        """Given a repository and package, return a list of available versions."""
        page2 = f"https://pypi.org/pypi/{package}/json"

        all_versions = json.loads(httpx.get(page2).text)["releases"].keys()
        res_versions: list[str] = []
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
    def generate_dependency_tree(
        package: str, version: str, use_poetry: bool = True
    ) -> TreeNode:
        """Given a repository, package, and version, return a conflict-free dep tree."""
        if use_poetry:
            cmd = (
                f'lavi poetry --package="{package}" --version="{version}" --no-scan -w'
            )
        else:
            cmd = (
                f'lavi pip --python={sys.executable} --package="{package}" '
                f'--version="{version}" --no-scan -w'
            )

        os.popen(cmd).read()

        try:
            with open("cds.json") as f:
                cds = json.loads(f.read())
        except FileNotFoundError:
            if use_poetry:
                return PipScraper.generate_dependency_tree(
                    package, version, use_poetry=False
                )
            else:
                return TreeNode(package="", repo="", version="")

        dependency_tree = generate_dependency_tree(cds)
        os.remove("cds.json")
        return dependency_tree
#!/usr/bin/env python3

import argparse
from typing import Dict, List, Protocol

from repo_worker.scrape_dud import DudScraper
from repo_worker.utils import TreeNode


class RepoScraper(Protocol):
    @staticmethod
    def list_packages(repo: str) -> List[str]:
        """Given a repository, return a list of its packages."""

    @staticmethod
    def list_package_versions(repo: str, package: str) -> List[str]:
        """Given a repository and package, return a list of available versions."""

    @staticmethod
    def generate_dependency_tree(repo, package, version) -> TreeNode:
        """Given a repository, package, and version, return a conflict-free dep tree."""


supported_repos: Dict[str, RepoScraper] = {
    "dud": DudScraper,
}


def parse_cmd_args():
    """Parse command-line arguments."""
    # Main parser
    parser = argparse.ArgumentParser(prog="entrypoint")
    parser.add_argument("-m", "--mode", choices=["cli", "redis"], required=True)
    subparsers = parser.add_subparsers(help="sub-command help", dest="command")

    # list-packages subcommand - List packages for a given repository
    list_packages = subparsers.add_parser("list-packages", help="list-packages help")
    # TODO add options here dynamically from supported_repos
    list_packages.add_argument("-r", "--repo", action="store", required=True)

    # list-package-versions subcommand - List versions a stream of (repo, package)
    subparsers.add_parser(
        "list-package-versions", help="list-package-versions help"
    )

    # generate-tree subcommand - Generate a conflict-free dep tree given all data
    subparsers.add_parser("generate-tree", help="generate-tree help")

    # Do the parse
    return parser.parse_args()


def main() -> None:
    """Accept command-line args, run as requested."""
    args = parse_cmd_args()

    if args.command is None:
        raise Exception("No command provided")

    if args.mode == "cli":
        # Pull from stdin and push to stdout
        # Runs a single time
        print("Running in cli mode")
    elif args.mode == "redis":
        # Pull and push data to redis store
        # Runs list-packages once, or the other commands on loop
        print("Running in redis mode")
    else:
        raise Exception(f"Unrecognized execution mode: {args.mode}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import logging

from repo_worker.config import REQUIRED_ENV_FOR_LAVI_DB, REQUIRED_ENV_FOR_REDIS
from repo_worker.core import cli_funcs, redis_funcs
from repo_worker.scrapers import repo_scrapers


logging.basicConfig(
    level=logging.INFO,
    datefmt="%H:%M:%S",
    format="[%(asctime)s]  %(levelname)-10s%(message)s",
)


def parse_cmd_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # Main parser
    parser = argparse.ArgumentParser(prog="entrypoint")
    parser.add_argument("-m", "--mode", choices=["cli", "redis"], required=True)
    subparsers = parser.add_subparsers(help="sub-command help", dest="command")

    # list-packages subcommand - List packages for a given repository
    list_packages = subparsers.add_parser("list-packages", help="list-packages help")
    # TODO add options here dynamically from supported_repos
    list_packages.add_argument("-r", "--repo", action="store", required=True)
    # CLI-only args
    list_packages.add_argument("-l", "--limit", action="store")

    # list-packages-worker subcommand - List packages given repo (redis-only)
    subparsers.add_parser("list-packages-worker", help="list-packages-worker help")

    # list-package-versions subcommand - List versions given (repo, package)
    list_package_versions = subparsers.add_parser(
        "list-package-versions", help="list-package-versions help"
    )
    # CLI-only args
    list_package_versions.add_argument("-r", "--repository", action="store")
    list_package_versions.add_argument("-p", "--package", action="store")
    list_package_versions.add_argument("-l", "--limit", action="store")

    # generate-tree subcommand - Generate a conflict-free dep tree given all data
    generate_tree = subparsers.add_parser("generate-tree", help="generate-tree help")
    # CLI-only args
    generate_tree.add_argument("-r", "--repository", action="store")
    generate_tree.add_argument("-p", "--package", action="store")
    generate_tree.add_argument("-V", "--version", action="store")

    # db-sync-versions subcommand - Send version entries to lavi db (redis-only)
    subparsers.add_parser("db-sync-versions", help="db-sync-versions help")

    # db-sync-trees subcommand - Send tree entries to lavi db (redis-only)
    subparsers.add_parser("db-sync-trees", help="db-sync-trees help")

    # refresh-queues subcommand - Refresh lost work in the queues
    subparsers.add_parser("refresh-queues", help="refresh-queues help")

    # Do the parse
    return parser.parse_args()


def main() -> None:
    """Accept command-line args, run as requested."""
    args = parse_cmd_args()

    # Verify stuff
    if args.command is None:
        raise Exception("No command provided")

    redis_only_commands = ["list-packages-worker", "db-sync-versions", "db-sync-trees"]
    if args.mode != "redis" and args.command in redis_only_commands:
        raise Exception(f"Can only run {args.command} command in redis-mode")

    lavi_db_commands = ["db-sync-versions", "db-sync-trees"]
    if args.command in lavi_db_commands and any(
        [var is None for var in REQUIRED_ENV_FOR_LAVI_DB]
    ):
        raise Exception(f"Missing required lavi env vars: {REQUIRED_ENV_FOR_LAVI_DB}")

    if args.mode == "redis" and any([var is None for var in REQUIRED_ENV_FOR_REDIS]):
        raise Exception(f"Missing required redis env vars: {REQUIRED_ENV_FOR_REDIS}")

    cli_only_args = ["limit", "repository", "package", "version"]
    for arg_name in cli_only_args:
        if args.mode == "redis" and getattr(args, arg_name, None) is not None:
            logging.info(f"Using {arg_name} in redis mode is meaningless")

    # Execute in CLI mode - pull from stdin and push to stdout
    if args.mode == "cli":
        logging.info("Running in cli mode")

        # CLI list-packages command
        if args.command == "list-packages":
            if args.repo not in repo_scrapers:
                raise Exception(f"Unrecognized repository: {args.repo}")
            logging.info("Running cli-mode list-packages")
            cli_funcs.list_packages(args.repo, int(args.limit) if args.limit else None)

        # CLI list-package-versions command
        elif args.command == "list-package-versions":
            if not args.repository or not args.package:
                raise Exception("repository and package required")
            if args.repository not in repo_scrapers:
                raise Exception(f"Unrecognized repository: {args.repository}")
            logging.info("Running cli-mode list-package-versions")
            cli_funcs.list_package_versions(
                args.repository, args.package, int(args.limit) if args.limit else None
            )

        # CLI generate-tree command
        elif args.command == "generate-tree":
            if not args.repository or not args.package or not args.version:
                raise Exception("repository, package, and version required")
            if args.repository not in repo_scrapers:
                raise Exception(f"Unrecognized repository: {args.repository}")
            logging.info("Running cli-mode generate-tree")
            cli_funcs.generate_tree(args.repository, args.package, args.version)

    # Execute in Redis mode - pull data from and push data to redis queues
    elif args.mode == "redis":
        # Runs list-packages once, or the other commands on loop
        logging.info("Running in redis mode")

        # Redis list-packages command
        if args.command == "list-packages":
            if args.repo not in repo_scrapers:
                raise Exception(f"Unrecognized repository: {args.repo}")
            logging.info("Running redis-mode list-packages")
            redis_funcs.list_packages(args.repo)

        # Redis list-packages-worker command
        if args.command == "list-packages-worker":
            logging.info("Running redis-mode list-packages-worker")
            redis_funcs.list_packages_worker()

        # Redis list-package-versions command
        if args.command == "list-package-versions":
            logging.info("Running redis-mode list-package-versions")
            redis_funcs.list_package_versions()

        # Redis generate-tree command
        if args.command == "generate-tree":
            logging.info("Running redis-mode generate-tree")
            redis_funcs.generate_tree()

        # Redis db-sync-trees command
        if args.command == "db-sync-trees":
            logging.info("Running redis-mode db-sync-trees")
            redis_funcs.db_sync_trees()

        # Redis refresh-queues command
        if args.command == "refresh-queues":
            logging.info("Running redis-mode refresh-queues")
            redis_funcs.refresh_queues()

    else:
        raise Exception(f"Unrecognized execution mode: {args.mode}")


if __name__ == "__main__":
    main()

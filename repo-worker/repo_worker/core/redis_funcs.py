import logging
import traceback
from typing import Dict, Tuple

import httpx

from repo_worker.config import LAVI_API_URL  # Only used if triggered
from repo_worker.core.redis_wq import get_redis_wq
from repo_worker.scrapers import repo_scrapers
from repo_worker.utils import get_recent_version, parse_version


def list_packages(repo: str) -> None:
    """Handle redis runs of list-packages."""
    scraper = repo_scrapers[repo]
    out_wq = get_redis_wq("to_list_versions")

    logging.info(f"Scraping package names for {repo}")
    packages = scraper.list_packages()

    logging.info("Inserting scraped package names")
    for package in packages:
        out_wq.insert((repo, package))
    logging.info("Done inserting scraped package names")


def list_package_versions(lease_time: int = 120) -> None:
    """Handle redis runs of list-package-versions."""
    in_wq = get_redis_wq("to_list_versions")
    out_versions_wq = get_redis_wq("to_insert_versions")
    out_recent_wq = get_redis_wq("to_generate_tree")

    while True:
        try:
            item: Tuple[str, str] | None = in_wq.lease(lease_time, 10)  # type: ignore
            if not item:
                logging.info("No work received, waiting")
                continue
            repo, package = item

            logging.info(f"Scraping package versions for {repo} - {package}")
            scraper = repo_scrapers[repo]
            versions = scraper.list_package_versions(package=package)
            if not versions:
                logging.info("No versions to insert")
                continue

            logging.info(f"Inserting {len(versions)} scraped package versions")
            for version in versions:
                out_versions_wq.insert((repo, package, version))
            logging.info("Done inserting scraped package versions")

            recent_version = get_recent_version(versions)
            logging.info(f"Inserting most recent package version {recent_version}")
            out_recent_wq.insert((repo, package, recent_version))
            logging.info("Done inserting most recent package version")

        except Exception:
            traceback.print_exc()


def generate_tree(lease_time: int = 120) -> None:
    """Handle redis runs of generate-tree."""
    in_wq = get_redis_wq("to_generate_tree")
    out_wq = get_redis_wq("to_insert_tree")

    while True:
        try:
            item: Tuple[str, str, str] | None
            item = in_wq.lease(lease_time, 10)  # type: ignore
            if not item:
                logging.info("No work received, waiting")
                continue
            repo, package, version = item

            logging.info(f"Generating tree for {repo} - {package} - {version}")
            scraper = repo_scrapers[repo]
            tree = scraper.generate_dependency_tree(package=package, version=version)

            logging.info("Inserting tree")
            out_wq.insert((repo, package, version, tree.as_json_b64()))
            logging.info("Done inserting tree")

        except Exception:
            traceback.print_exc()


def db_sync_versions(lease_time: int = 120) -> None:
    """Insert items from versions queue in lavi db."""
    in_wq = get_redis_wq("to_insert_versions")

    while True:
        try:
            item: Tuple[str, str, str] | None
            item = in_wq.lease(lease_time, 10)  # type: ignore
            if not item:
                logging.info("No work received, waiting")
                continue
            repo, package, version = item
            parsed_version = parse_version(version)
            if parsed_version is None:
                logging.info("Failed to parse version, skipping")
                continue
            major, minor, patch = parsed_version

            logging.info(f"Sending version to lavi db: {repo} - {package} - {version}")
            body = {
                "repo_name": repo,
                "pkg_name": package,
                "major_vers": major,
                "minor_vers": minor,
                "patch_vers": patch,
                "num_downloads": 0,
                "s3_bucket": "0",
            }
            resp = httpx.post(f"{LAVI_API_URL}/internal/insert_vers", json=body)
            resp.raise_for_status()
            logging.info("Succesfully sent version to db")

        except Exception:
            traceback.print_exc()


def db_sync_trees(lease_time: int = 120) -> None:
    """Insert items from trees queue in lavi db."""
    in_wq = get_redis_wq("to_insert_tree")

    while True:
        try:
            item: Tuple[str, str, str, str] | None
            item = in_wq.lease(lease_time, 10)  # type: ignore
            if not item:
                logging.info("No work received, waiting")
                continue
            repo, package, version, tree = item
            parsed_version = parse_version(version)
            if parsed_version is None:
                logging.info("Failed to parse version, skipping")
                continue
            major, minor, patch = parsed_version

            logging.info(f"Sending tree to lavi db: {repo} - {package} - {version}")
            query_params: Dict[str, str] = {
                "repo": repo,
                "package": package,
                "major_vers": str(major),
                "minor_vers": str(minor),
                "patch_vers": str(patch),
            }
            logging.critical(tree)
            resp = httpx.post(
                f"{LAVI_API_URL}/internal/insert_tree",
                params=query_params,
                json={"tree": tree},
            )
            resp.raise_for_status()
            logging.info("Succesfully sent tree to db")

        except Exception:
            traceback.print_exc()
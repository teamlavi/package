import logging
import traceback
import time
from typing import Dict, Tuple

import httpx

from repo_worker.config import LAVI_API_URL  # Only used if triggered
from repo_worker.core.redis_wq import get_redis_wq, known_queue_sizes
from repo_worker.scrapers import repo_scrapers
from repo_worker.utils import get_recent_version, parse_version, timeout


def refresh_queues() -> None:
    """Refresh all the work queues with dropped tasks."""
    wqs = [get_redis_wq(name) for name in known_queue_sizes]
    for wq in wqs:
        wq.refresh()


def list_packages(repo: str) -> None:
    """Handle redis runs of list-packages."""
    # Takes 1-5 seconds, but lease time unnecessary bc we're only using output queues
    scraper = repo_scrapers[repo]
    out_wq = get_redis_wq("to_list_versions")

    logging.info(f"Scraping package names for {repo}")
    packages = scraper.list_packages()

    logging.info(f"Inserting scraped {len(packages)} package names")
    for package in packages:
        out_wq.insert((repo, package))
    logging.info("Done inserting scraped package names")


def list_package_versions(lease_time: int = 30) -> None:
    """Handle redis runs of list-package-versions."""
    in_wq = get_redis_wq("to_list_versions")
    out_recent_wq = get_redis_wq("to_generate_tree")

    while True:
        try:
            with timeout(lease_time + 10):
                item: Tuple[str, str] | None
                item = in_wq.lease(lease_time, 10)  # type: ignore
                if not item:
                    logging.info("No work received, waiting")
                    continue
                repo, package = item
                start_t = time.time()

                logging.info(f"Scraping package versions for {repo} - {package}")
                scraper = repo_scrapers[repo]
                versions = scraper.list_package_versions(package=package)
                if not versions:
                    logging.info("No versions to insert")
                    continue

                in_wq.complete(item)
                elapsed_t = int(1000 * (time.time() - start_t))
                in_wq.save_metrics(elapsed_t, len(versions))

                recent_version = get_recent_version(versions)
                logging.info(f"Inserting most recent package version {recent_version}")
                out_recent_wq.insert((repo, package, recent_version))
                logging.info("Done inserting most recent package version")

        except Exception:
            traceback.print_exc()


def generate_tree(lease_time: int = 300) -> None:
    """Handle redis runs of generate-tree."""
    in_wq = get_redis_wq("to_generate_tree")
    out_wq = get_redis_wq("to_insert_tree")

    while True:
        try:
            with timeout(lease_time + 10):
                item: Tuple[str, str, str] | None
                item = in_wq.lease(lease_time, 10)  # type: ignore
                if not item:
                    logging.info("No work received, waiting")
                    continue
                repo, package, version = item
                start_t = time.time()

                logging.info(f"Generating tree for {repo} - {package} - {version}")
                scraper = repo_scrapers[repo]
                tree = scraper.generate_dependency_tree(
                    package=package, version=version
                )

                in_wq.complete(item)
                elapsed_t = int(1000 * (time.time() - start_t))
                in_wq.save_metrics(elapsed_t, 1)

                logging.info("Inserting tree")
                out_wq.insert((repo, package, version, tree.as_json_b64()))
                logging.info("Done inserting tree")

        except Exception:
            traceback.print_exc()


def db_sync_trees(lease_time: int = 30) -> None:
    """Insert items from trees queue in lavi db."""
    in_wq = get_redis_wq("to_insert_tree")

    while True:
        try:
            with timeout(lease_time + 10):
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
                start_t = time.time()

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

                in_wq.complete(item)
                elapsed_t = int(1000 * (time.time() - start_t))
                in_wq.save_metrics(elapsed_t, len(tree))

        except Exception:
            traceback.print_exc()

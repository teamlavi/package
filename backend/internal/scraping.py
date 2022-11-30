from internal import updates
from internal.queues import QueueName, get_queue
from scrapers import repo_scrapers
from utils.utils import compress_tree, get_recent_version


def list_packages(repo: str) -> None:
    """List packages given a repo."""
    scraper = repo_scrapers[repo]
    packages = scraper.list_packages()

    # Insert into next queue
    # TODO pipeline batch insert for performance
    for package in packages:
        get_queue(QueueName.to_list_versions).enqueue(
            list_package_versions, repo, package
        )


def list_package_versions(repo: str, package: str) -> None:
    """List versions given repo, package name."""
    scraper = repo_scrapers[repo]
    versions = scraper.list_package_versions(package)
    if not versions:
        return
    recent_version = get_recent_version(versions)

    # Insert into next queue
    get_queue(QueueName.to_generate_tree).enqueue(
        generate_tree, repo, package, recent_version
    )


async def generate_tree(repo: str, package: str, version: str) -> None:
    """Generate a dependency tree given repo, package, version."""
    scraper = repo_scrapers[repo]
    tree = scraper.generate_dependency_tree(package, version)

    # TODO change funcs available on tree to make this smoother
    all_nodes: dict[str, list[str]] = {}
    tree._as_json(all_nodes)
    compressed_tree = compress_tree(all_nodes)

    # Insert into database
    await updates.insert_single_dependency_tree(repo, package, version, compressed_tree)

import os
from typing import List, Tuple

import httpx


REPO_API_URL = os.getenv("REPO_API_URL") or "https://levi.lavi-lava.com/repo"


queue_names = [
    "to_list_versions",
    "to_generate_tree",
    "to_insert_tree",
]


def collect_metrics(queue_name: str) -> List[Tuple[int, int]]:
    """Collect metrics from the api server."""
    resp = httpx.get(f"{REPO_API_URL}/metrics", params={"queue_name": queue_name})
    resp.raise_for_status()
    raw = resp.json()
    return [(int(item[0]), int(item[1])) for item in raw]


def averages(metrics: List[Tuple[int, int]]) -> Tuple[int, int]:
    """Get average of each metric."""
    times, outs = list(zip(*metrics))
    return sum(times) / len(times), sum(outs) / len(outs)


def main() -> None:
    for queue_name in queue_names:
        metrics = collect_metrics(queue_name)
        if not metrics:
            print("No metrics found")
            return

        avg_time, avg_out = averages(metrics)
        print(
            f"{queue_name}  \tt={round(avg_time, 3)}ms"
            f"\to={round(avg_out, 3)}\tn={len(metrics)}"
        )


if __name__ == "__main__":
    main()

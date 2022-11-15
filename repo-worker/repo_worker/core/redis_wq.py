from base64 import b64decode, b64encode
import logging
from typing import List, Tuple

import redis

from repo_worker.config import REDIS_HOST, REDIS_PORT


known_queue_sizes = {
    "to_list_versions": 2,
    "to_generate_tree": 3,
    "to_insert_versions": 3,
    "to_insert_tree": 4,
}


def _serialize(items: Tuple[str, ...]) -> str:
    return ":".join(b64encode(item.encode()).decode() for item in items)


def _deserialize(packed: str) -> Tuple[str, ...]:
    return tuple(b64decode(item.encode()).decode() for item in packed.split(":"))


class RedisWQ(object):
    """Redis Finite Work Queue."""

    def __init__(
        self,
        queue_name: str,
        expected_tuple_size: int | None = None,
        attempt_limit: int = 3,
    ):
        """Initialize a work queue, use config from env vars."""
        assert REDIS_HOST is not None and REDIS_PORT is not None
        self.db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)  # type: ignore
        self.queue_name = queue_name
        self.processing_queue_name = queue_name + ":processing"
        self.failed_queue_name = queue_name + ":failed"
        self.metrics_store_name = queue_name + ":metrics"
        self.lease_queue_prefix = queue_name + ":leased:"
        self.attempts_prefix = queue_name + ":attempts:"
        self.expected_tuple_size = expected_tuple_size
        self.attempt_limit = attempt_limit

    def insert(self, item: Tuple[str, ...]) -> None:
        """Insert an item into the queue."""
        if len(item) != self.expected_tuple_size:
            raise Exception(
                f"Item {item} not of expected size {self.expected_tuple_size}"
            )
        packed_item = _serialize(item)
        if packed_item.encode() not in self.db.lrange(self.queue_name, 0, -1):
            self.db.lpush(self.queue_name, packed_item)
        else:
            logging.warning(f"Cannot re-insert into {self.queue_name} of {packed_item}")

    def lease(
        self, lease_duration: int = 60, timeout: int = 0
    ) -> Tuple[str, ...] | None:
        """Take an item off the work queue."""
        packed_item: bytes | None = self.db.blmove(
            self.queue_name,
            self.processing_queue_name,
            timeout,
            src="RIGHT",
            dest="LEFT",
        )
        if packed_item:
            packed_item_str = packed_item.decode("UTF-8")
            self.db.setex(self.lease_queue_prefix + packed_item_str, lease_duration, 1)
            self.db.incr(self.attempts_prefix + packed_item_str)
            item = _deserialize(packed_item_str)
            if len(item) != self.expected_tuple_size:
                raise Exception(
                    f"Item {item} not of expected size {self.expected_tuple_size}"
                )
            return item
        return None

    def complete(self, item: Tuple[str, ...]) -> None:
        """Mark a work item as completed."""
        if len(item) != self.expected_tuple_size:
            raise Exception(
                f"Item {item} not of expected size {self.expected_tuple_size}"
            )
        packed_item = _serialize(item)
        self.db.lrem(self.processing_queue_name, 0, packed_item)
        self.db.delete(self.lease_queue_prefix + packed_item)
        self.db.delete(self.attempts_prefix + packed_item)

    def refresh(self) -> None:
        """Refresh the work queue with dead items."""
        in_progress = self.db.lrange(self.processing_queue_name, 0, -1)
        dead_items = []  # Items to retry
        failed_items = []  # Items that passed the retry limit
        for packed_item in in_progress:
            packed_item_str = packed_item.decode("UTF-8")
            attempts = self._get_attempts_packed(packed_item_str)
            if not self.db.get(self.lease_queue_prefix + packed_item_str):
                if attempts < self.attempt_limit:
                    dead_items.append(packed_item_str)
                else:
                    failed_items.append(packed_item_str)
        for item in dead_items:
            # Only re-add to queue if it's still in processing
            # This will also prevent duplicate lost jobs being added to work queue
            if self.db.lrem(self.processing_queue_name, 0, item):
                self.db.lpush(self.queue_name, item)
        for item in failed_items:
            # Only re-add to queue if it's still in processing
            # This will also prevent duplicate lost jobs being added to failed queue
            if self.db.lrem(self.processing_queue_name, 0, item):
                self.db.lpush(self.failed_queue_name, item)
            self.db.delete(self.attempts_prefix + item)

    def _get_queue(self, queue: str) -> List[Tuple[str, ...]]:
        """Get the deserialized contents of a queue."""
        items: List[bytes] = self.db.lrange(queue, 0, -1)
        return [_deserialize(item.decode()) for item in items]

    def _get_attempts_packed(self, packed_item: str) -> int:
        """Get how many attempts have been begun against the given packed item."""
        return int(self.db.get(self.attempts_prefix + packed_item) or 0)

    def get_attempts(self, item: Tuple[str, ...]) -> int:
        """Get how many attempts have been begun against the given packed item."""
        return self._get_attempts_packed(_serialize(item))

    def get_failures(self) -> List[Tuple[str, ...]]:
        """Get failed items."""
        return self._get_queue(self.failed_queue_name)

    def get_status(self, item: Tuple[str, ...]) -> str:
        """Get the human-readable status string for a given item."""
        if item in self._get_queue(self.failed_queue_name):
            return "failed"

        elif item in self._get_queue(self.processing_queue_name):
            attempts = self.get_attempts(item)
            return f"processing - attempt {attempts}"

        elif item in self._get_queue(self.queue_name):
            return "queued"

        return "unknown/complete"

    def save_metrics(self, elapsed_time_ms: int, ouputs_per_input: int) -> None:
        """Save metrics to the store."""
        self.db.lpush(self.metrics_store_name, f"{elapsed_time_ms}:{ouputs_per_input}")

    def get_metrics(self) -> List[Tuple[int, int]]:
        """Get all metrics from the server."""
        raw_metrics = self.db.lrange(self.metrics_store_name, 0, -1)
        output = []
        for metric in raw_metrics:
            nums = metric.decode().split(":")
            output.append((nums[0], nums[1]))
        return output


def get_redis_wq(name: str) -> RedisWQ:
    """Get a redis queue with expected data."""
    if name not in known_queue_sizes:
        raise Exception(f"Unrecognized queue name {name}")
    return RedisWQ(name, expected_tuple_size=known_queue_sizes[name])

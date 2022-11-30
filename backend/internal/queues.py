from enum import Enum

from redis import Redis
from rq import Queue  # type: ignore

from utils import config


class QueueName(str, Enum):
    to_list_packages = "to_list_packages"
    to_list_versions = "to_list_versions"
    to_generate_tree = "to_generate_tree"


if config.REDIS_HOST is None:
    # Should have been checked by now, but just in case
    raise Exception("REDIS_HOST required")

queues: dict[QueueName, Queue] = {
    queue_name: Queue(
        queue_name.value,
        connection=Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0),
    )
    for queue_name in QueueName
}


def get_queue(queue_name: QueueName) -> Queue:
    """Get a work queue."""
    return queues[queue_name]

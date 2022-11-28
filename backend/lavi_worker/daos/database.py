from typing import Any

import psycopg

from lavi_worker import config


# Type alias for cleanliness
Transaction = psycopg.AsyncConnection[Any]


async def get_db_tx() -> Transaction:
    """Get a new db connection."""
    # Backstop to verify env vars again
    req_vars = [
        config.DB_USER,
        config.DB_PASS,
        config.DB_ADDRESS,
        config.DB_PORT,
        config.DB_NAME,
    ]
    if any([var is None for var in req_vars]):
        raise Exception(f"Missing db env vars: {req_vars}")

    # Create connection
    conn = await psycopg.AsyncConnection.connect(
        user=config.DB_USER,
        password=config.DB_PASS,
        host=config.DB_ADDRESS,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
    )

    return conn

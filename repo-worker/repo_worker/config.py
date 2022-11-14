import os

REDIS_HOST = os.getenv("REDIS_HOST")


REQUIRED_ENV_FOR_REDIS = [
    REDIS_HOST,
]

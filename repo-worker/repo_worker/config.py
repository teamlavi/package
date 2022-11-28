import os

CYCLE_TIME = int(os.getenv("CYCLE_TIME") or "5")
EXPECTED_PREFIX = os.getenv("EXPECTED_PREFIX") or ""
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
LAVI_API_URL = os.getenv("LAVI_API_URL")


REQUIRED_ENV_FOR_REDIS = [
    REDIS_HOST,
    REDIS_PORT,
]

REQUIRED_ENV_FOR_LAVI_DB = [
    LAVI_API_URL,
]

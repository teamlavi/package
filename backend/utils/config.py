import os

EXPECTED_PREFIX = os.getenv("EXPECTED_PREFIX") or ""
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_ADDRESS = os.getenv("DB_ADDRESS")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
GH_ACCESS_TOKEN = os.getenv("GH_ACCESS_TOKEN")


# Env vars required for a full deployment, checked in app_startup
REQUIRED_ENV_FOR_DEPLOY = [
    DB_USER,
    DB_PASS,
    DB_ADDRESS,
    DB_PORT,
    DB_NAME,
    GH_ACCESS_TOKEN,
]

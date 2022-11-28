import os

import httpx


def _check_dev_env(dev_user: str) -> str | None:
    """Check whether dev env is alive, return url if success."""
    url = f"https://{tmp}.lavi-lava.com/lavi"
    resp = httpx.get(f"{url}/ping")
    if resp.status_code == 200 and resp.text == "pong":
        return url
    return None


# Get the BASE_URL to hit with tests
# First check if base url directly given (i.e. in garden-managed test)
if tmp := os.getenv("BASE_URL"):
    BASE_URL = tmp
# Next check if the user might have a remote dev env
elif (tmp := os.getenv("LAVI_DEV_USER")) and (url := _check_dev_env(tmp)):
    BASE_URL = url
# Else fallback to local run
else:
    BASE_URL = "http://localhost:8080"

# Set insecure transport if necessary for oauthlib to shut up
if BASE_URL.startswith("http://"):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
elif not BASE_URL.startswith("https://"):
    raise Exception("Path must start with 'http://' or 'https://'")

from fastapi import HTTPException

from utils.config import AUTH_CODE


def verify_code(auth_code: str) -> None:
    """Verify that the given code is valid."""
    if auth_code != AUTH_CODE:
        raise HTTPException(status_code=401, detail="Invalid auth code")

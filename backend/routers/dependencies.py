from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from utils.config import AUTH_CODE


security = HTTPBearer()


def verify_code(credentials: HTTPAuthorizationCredentials = Security(security)) -> None:
    """Verify that the given code is valid."""
    print(credentials.scheme, credentials.credentials)
    if credentials.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="Use Bearer auth")
    if credentials.credentials != AUTH_CODE:
        raise HTTPException(status_code=401, detail="Invalid auth code")

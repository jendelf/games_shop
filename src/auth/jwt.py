from fastapi import Request, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param

async def get_token_from_request(request: Request) -> str:

    auth_header = request.headers.get("Authorization")
    if auth_header:
        scheme, token = get_authorization_scheme_param(auth_header)
        if scheme and scheme.lower() == "bearer":
            return token

    token = request.cookies.get("access_token")
    if token:
        return token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
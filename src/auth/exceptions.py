from fastapi import HTTPException, status

InvalidCredentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

RefreshTokenExpired = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refresh token expired",
)

InvalidRefreshToken = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid refresh token",
)

RefreshTokenNotFound = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refresh token not found",
)

NotAuthenticated = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)

InsufficientPermissions = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Insufficient permissions"
)

RefreshTokenMissing = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refresh token missing"
)

InactiveUser = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, 
    detail="Inactive user"
)

def UserAlreadyExists(email: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"User with '{email}' already exists",
    )

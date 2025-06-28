from datetime import timedelta
from typing import Annotated
from .constants import ACCESS_TOKEN_EXPIRE_MINUTES
from .schemas import Token, UserOut, EmailPasswordForm
from fastapi import Depends, HTTPException, status, APIRouter
from .dependencies import authenticate_user, get_current_active_user
from .service import create_access_token

router = APIRouter()

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[EmailPasswordForm, Depends()],
) -> Token:
    #TODO добавить рабочую бд
    user = authenticate_user(None, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=UserOut)
async def read_users_me(
    current_user: Annotated[UserOut, Depends(get_current_active_user)],
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[UserOut, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
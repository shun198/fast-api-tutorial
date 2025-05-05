from datetime import timedelta
from typing import Annotated

from config.dependency import get_user_usecase
from config.env import app_settings
from config.jwt import check_password, create_jwt_token, decode_jwt_token, hash_password
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from infrastructure.email import send_email
from jose import JWTError
from schemas.requests.auth_request_schema import (
    CreateUserRequest,
    EmailSchema,
    RefreshTokenRequest,
    TokenRequest,
)
from schemas.responses.auth_response_schema import TokenResponse
from usecases.user_usecase import UserUsecase

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user_request: CreateUserRequest,
    user_usecase: UserUsecase = Depends(get_user_usecase),
):
    hashed_password = hash_password(create_user_request.password)
    user = user_usecase.create_user(hashed_password, create_user_request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists",
        )
    return {"msg": "user created"}


def _authenticate_user(username: str, password: str, user_usecase: UserUsecase):
    user = user_usecase.get_user_by_username(username)
    if not user:
        return False
    if not check_password(password, user.password):
        return False
    return user


# OAuthを使って認証
@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_usecase: UserUsecase = Depends(get_user_usecase),
) -> TokenRequest:
    user = _authenticate_user(form_data.username, form_data.password, user_usecase)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_jwt_token(
        user.username,
        user.id,
        timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_jwt_token(
        user.username,
        user.id,
        timedelta(days=app_settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    return TokenRequest(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post("/refresh")
async def refresh_token(
    refresh_token_request: RefreshTokenRequest,
    user_usecase: UserUsecase = Depends(get_user_usecase),
) -> TokenResponse:
    try:
        decoded_token = decode_jwt_token(
            refresh_token_request.model_dump()["refresh_token"]
        )
        username: str = decoded_token.get("sub")
        user_id: int = decoded_token.get("iss")
        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        user = user_usecase.get_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        new_access_token = create_jwt_token(
            user.username,
            user.id,
            timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return TokenResponse(
            access_token=new_access_token,
            token_type="bearer",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )


@router.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """
    try:
        await send_email(email, html)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"msg": "email has been sent"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cannot send email: {e}",
        )


# TODO: メール送信ロジックを作成
# https://sabuhish.github.io/fastapi-mail/example/

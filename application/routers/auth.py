from datetime import timedelta
from typing import Annotated

from config.dependency import get_user_usecase
from config.env import app_settings
from config.jwt import check_password, create_jwt_token, decode_jwt_token, hash_password
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_csrf_protect import CsrfProtect
from infrastructure.emails.email import send_email
from jose import JWTError
from schemas.requests.auth_request_schema import CreateUserRequest
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
    context = {"name": user.username}
    try:
        await send_email(
            user.email, "welcome_email.html", subject="ようこそ", context=context
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cannot send email: {e}",
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
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_usecase: UserUsecase = Depends(get_user_usecase),
    csrf_protect: CsrfProtect = Depends()
) -> Response:
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
    _, signed_token = csrf_protect.generate_csrf_tokens()
    # https://fastapi.tiangolo.com/advanced/response-cookies/#use-a-response-parameter
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=app_settings.COOKIE_HTTP_ONLY,
        secure=app_settings.COOKIE_SECURE,
        samesite=app_settings.COOKIE_SAME_SITE,
        max_age=1800,
    )
    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        httponly=app_settings.COOKIE_HTTP_ONLY,
        secure=app_settings.COOKIE_SECURE,
        samesite=app_settings.COOKIE_SAME_SITE,
        max_age=86400,
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    response.status_code = status.HTTP_200_OK
    return response


@router.post("/logout")
def logout(response: Response, csrf_protect: CsrfProtect = Depends()):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    csrf_protect.unset_csrf_cookie(response)
    return {"msg": "Logged out"}


@router.post("/refresh")
async def refresh_token(
    request: Request,
    response: Response,
    user_usecase: UserUsecase = Depends(get_user_usecase),
) -> Response:
    try:
        decoded_token = decode_jwt_token(
            request.cookies.get("refresh_token").split("Bearer ")[1]
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
        response.set_cookie(
            key="access_token",
            value=f"Bearer {new_access_token}",
            httponly=app_settings.COOKIE_HTTP_ONLY,
            secure=app_settings.COOKIE_SECURE,
            samesite=app_settings.COOKIE_SAME_SITE,
            max_age=1800,
        )
        response.status_code = status.HTTP_200_OK
        return response
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
from database import db_dependency
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from models import Users
from schemas.auth import CreateUserRequest, CurrentUser, Token
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/api/auth", tags=["auth"])

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_DAYS = os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    hashed_password = bcrypt.hashpw(
        create_user_request.password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        is_admin=create_user_request.is_admin,
        password=hashed_password,
        phone_number=create_user_request.phone_number,
        is_active=True,
    )
    try:
        db.add(create_user_model)
        db.commit()
        return {"msg": "user created"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists",
        )


def authenticate_user(username: str, password: str, db):
    user = db.execute(
        select(Users).where(Users.username == username)
    ).scalar_one_or_none()
    if not user:
        return False
    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("iss")
        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return CurrentUser(username=username, id=user_id)
    except Exception:
        return None


def create_jwt_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "iss": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# OAuthを使って認証
@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_jwt_token(
        user.username,
        user.id,
        timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)),
    )
    refresh_token = create_jwt_token(
        user.username,
        user.id,
        timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS)),
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh")
async def refresh_token(db: db_dependency, refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("iss")
        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        user = db.execute(
            select(Users).where(Users.username == username)
        ).scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        new_access_token = create_jwt_token(
            user.username,
            user.id,
            timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)),
        )
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )


# TODO: メール送信ロジックを作成
# https://sabuhish.github.io/fastapi-mail/example/

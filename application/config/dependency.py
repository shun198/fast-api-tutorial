from typing import Annotated

from config.jwt import decode_jwt_token
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from infrastructure.database import get_db
from repositories.todo_repository import TodoRepository
from repositories.user_repository import UserRepository
from schemas.requests.auth_request_schema import CurrentUserRequest
from sqlalchemy.orm import Session
from usecases.todo_usecase import TodoUsecase

from application.usecases.user_usecase import UserUsecase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_todo_usecase(db: Session = Depends(get_db)) -> TodoUsecase:
    todo_repository = TodoRepository(db)
    return TodoUsecase(todo_repository)


def get_user_usecase(db: Session = Depends(get_db)) -> UserUsecase:
    user_repository = UserRepository(db)
    return UserUsecase(user_repository)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUserRequest:
    try:
        decoded_token = decode_jwt_token(token)
        username: str = decoded_token.get("sub")
        user_id: int = decoded_token.get("iss")
        if not username or not user_id:
            return None
        return CurrentUserRequest(username=username, id=user_id)
    except Exception:
        return None


user_dependency = Annotated[dict, Depends(get_current_user)]

db_dependency = Annotated[Session, Depends(get_db)]

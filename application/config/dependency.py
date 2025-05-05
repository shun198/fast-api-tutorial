from typing import Annotated, Optional

from config.jwt import decode_jwt_token
from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from infrastructure.database import get_db
from repositories.todo_repository import TodoRepository
from repositories.user_repository import UserRepository
from schemas.requests.auth_request_schema import CurrentUserRequest
from sqlalchemy.orm import Session
from usecases.todo_usecase import TodoUsecase
from usecases.user_usecase import UserUsecase


# https://zenn.dev/noknmgc/articles/fastapi-jwt-cookie
# https://github.com/fastapi/fastapi/issues/480
class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            authorization: str = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/auth/login")


def get_todo_usecase(db: Session = Depends(get_db)) -> TodoUsecase:
    todo_repository = TodoRepository(db)
    return TodoUsecase(todo_repository)


def get_user_usecase(db: Session = Depends(get_db)) -> UserUsecase:
    user_repository = UserRepository(db)
    return UserUsecase(user_repository)


async def get_current_user_from_cookie(
    token: str = Depends(oauth2_scheme),
) -> CurrentUserRequest:
    try:
        decoded_token = decode_jwt_token(token)
        username: str = decoded_token.get("sub")
        user_id: int = decoded_token.get("iss")
        if not username or not user_id:
            return None
        return CurrentUserRequest(username=username, id=user_id)
    except Exception:
        return None


user_dependency = Annotated[dict, Depends(get_current_user_from_cookie)]

db_dependency = Annotated[Session, Depends(get_db)]

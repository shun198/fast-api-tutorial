from models import Users
from repositories.user_repository import UserRepository
from schemas.requests.auth_request_schema import CreateUserRequest


class UserUsecase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_username(self, username: str) -> Users | None:
        return self.user_repository.find_by_username(username)

    def create_user(
        self, hashed_password: str, user_model: CreateUserRequest
    ) -> Users | None:
        return self.user_repository.create(hashed_password, user_model)

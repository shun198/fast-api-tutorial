from models import Users
from schemas.requests.auth_request_schema import CreateUserRequest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_username(self, username: str) -> Users:
        try:
            user = self.db.execute(
                select(Users).where(Users.username == username)
            ).scalar_one_or_none()
            return user
        except Exception:
            None

    def create(self, hashed_password: str, user_model: CreateUserRequest) -> Users:
        try:
            user_data = user_model.model_dump()
            user_data["password"] = hashed_password
            user = Users(**user_data)
            self.db.add(user)
            self.db.commit()
            return user
        except IntegrityError:
            self.db.rollback()
            return None

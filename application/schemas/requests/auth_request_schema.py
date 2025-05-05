from typing import List

from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    is_admin: bool
    phone_number: str


class TokenRequest(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class CurrentUserRequest(BaseModel):
    username: str
    id: int


class EmailSchema(BaseModel):
    email: List[EmailStr]

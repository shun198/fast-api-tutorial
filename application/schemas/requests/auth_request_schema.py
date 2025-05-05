from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    is_admin: bool
    phone_number: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class CurrentUserRequest(BaseModel):
    username: str
    id: int

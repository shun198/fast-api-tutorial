from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    is_admin: bool
    phone_number: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class CurrentUser(BaseModel):
    username: str
    id: int

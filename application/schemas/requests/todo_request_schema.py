from pydantic import BaseModel, Field


class UpdateTodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    is_starred: bool
    is_completed: bool


class CreateTodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    is_starred: bool

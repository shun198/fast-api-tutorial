from pydantic import BaseModel, Field


class TodoResponse(BaseModel):
    id: int = Field()
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    is_starred: bool
    is_completed: bool
    owner_id: int

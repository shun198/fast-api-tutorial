from usecases.todo_usecase import TodoUsecase
from repositories.todo_repository import TodoRepository
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from fastapi import Depends


def get_todo_usecase(db: Session = Depends(get_db)) -> TodoUsecase:
    todo_repository = TodoRepository(db)
    return TodoUsecase(todo_repository)

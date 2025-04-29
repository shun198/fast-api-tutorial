from usecases.todo_usecase import TodoUsecase
from infrastructure.database import db_dependency

def get_todo_usecase(db=db_dependency) -> TodoUsecase:
    return TodoUsecase(db)

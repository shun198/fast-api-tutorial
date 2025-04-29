from models import Users
from repositories.todo_repository import TodoRepository


class TodoUsecase:
    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def get_all_todos(self, user: Users):
        return self.todo_repository.find_all(user)

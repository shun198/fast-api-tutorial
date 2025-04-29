from models.todo import Todos
from models.user import Users
from repositories.todo_repository import TodoRepository
from schemas.todo_schema import CreateTodoModel, UpdateTodoModel


class TodoUsecase:
    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def get_all_todos(self, user: Users) -> list[Todos]:
        return self.todo_repository.find_all(user)

    def read_todo(self, user: Users, todo_id: int) -> Todos | None:
        return self.todo_repository.find_one(user, todo_id)

    def create_todo(self, user: Users, todo_model: CreateTodoModel) -> Todos:
        return self.todo_repository.create(user, todo_model)

    def update_todo(
        self, user: Users, todo_model: UpdateTodoModel, todo: Todos
    ) -> Todos:
        return self.todo_repository.update(user, todo_model, todo)

    def delete_todo(self, todo_id: Todos):
        return self.todo_repository.delete(todo_id)

    def bulk_delete_todo(self, user: Users):
        return self.todo_repository.bulk_delete(user)

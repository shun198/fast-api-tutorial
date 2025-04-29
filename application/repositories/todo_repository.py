from models.todo import Todos
from models.user import Users
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from schemas.todo_schema import (
    CreateTodoModel,
    UpdateTodoModel,
)


class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self, user: Users) -> list[Todos]:
        todos = self.db.scalars(
            select(Todos)
            .filter(Todos.owner_id == user.id, Todos.complete == False)
            .order_by(Todos.id)
        ).all()
        return todos

    def find_one(self, user: Users, todo_id: int) -> Todos | None:
        todo = self.db.scalars(
            select(Todos).filter(
                Todos.id == todo_id, Todos.owner_id == user.id, Todos.complete == False
            )
        ).first()
        return todo

    def create(self, user: Users, todo_model: CreateTodoModel) -> Todos:
        todo = Todos(**todo_model.model_dump(), owner_id=user.id)
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def update(self, user: Users, todo_model: UpdateTodoModel, todo: Todos) -> Todos:
        self.db.execute(
            update(Todos)
            .where(Todos.id == todo.id, Todos.owner_id == user.id)
            .values(**todo_model.model_dump())
        )
        self.db.commit()
        return todo

    def delete(self, todo: Todos):
        self.db.delete(todo)
        self.db.commit()

    def bulk_delete(self, user: Users):
        self.db.execute(delete(Todos).where(Todos.owner_id == user.id))
        self.db.commit()

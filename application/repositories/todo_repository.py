from models.todo import Todos
from models.user import Users
from sqlalchemy import select
from sqlalchemy.orm import Session
from abc import ABC


class AbstractTodoRepository(ABC):
    def __init__(self, db: Session):
        self.db = db


class TodoRepository(AbstractTodoRepository):
    def find_all(self, user: Users) -> Todos:
        todos = self.db.scalars(
            select(Todos)
            .filter(Todos.owner_id == user.id, Todos.complete == False)
            .order_by(Todos.id)
        ).all()
        return todos

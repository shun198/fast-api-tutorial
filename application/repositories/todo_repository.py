from typing import List

from models.todo import Todos
from models.user import Users
from sqlalchemy import select
from sqlalchemy.orm import Session


class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self, user: Users) -> List[Todos]:
        todos = self.db.scalars(
            select(Todos)
            .filter(Todos.owner_id == user.id, Todos.complete == False)
            .order_by(Todos.id)
        ).all()
        return todos

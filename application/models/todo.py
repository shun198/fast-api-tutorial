from infrastructure.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    is_starred = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

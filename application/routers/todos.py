from typing import Annotated, List

from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, status
from models import Todos
from routers.auth import get_current_user
from schemas.todos import TodoModel, TodoResponse
from sqlalchemy import select, update
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/todos", tags=["todos"])


# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/?h=get_db
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 依存性注入をすることでget_dbメソッドが自動的に呼ばるので毎回セッションインスタンスの生成やセッションを切る処理を書かずに済む
# Annotatedを使うことでDepends(get_db)がSession型だとわかる
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-session-dependency
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/?h=get_db#sub-dependencies-with-yield
# https://github.com/fastapi/fastapi/pull/9298
# FastAPI0.95.0以降の機能
@router.get("", response_model=List[TodoResponse])
async def read_todos(user: user_dependency, db: db_dependency):
    # https://docs.sqlalchemy.org/en/20/orm/quickstart.html#simple-select
    # https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalars
    # scalarsを使うことでTodosのインスタンスを返す
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    todos = db.scalars(select(Todos).order_by(Todos.id)).all()
    return todos


@router.get("/{todo_id}", response_model=TodoResponse)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    todo = db.get(Todos, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_model: TodoModel):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    # pydantic2ではdict()ではなく、model_dumpが使用されている
    # https://docs.pydantic.dev/latest/concepts/serialization/#modelmodel_dump
    todo = Todos(**todo_model.model_dump())
    # https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add
    db.add(todo)
    db.commit()
    # # refreshをすることでauto-incrementしたIDやcreated_atが反映されるようになる
    # # https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh
    db.refresh(todo)
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(user: user_dependency, db: db_dependency, todo_model: TodoModel, todo_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    todo = db.get(Todos, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    # https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update
    db.execute(
        update(Todos).where(Todos.id == todo_id).values(**todo_model.model_dump())
    )
    db.commit()
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    todo = db.get(Todos, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    # https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete
    db.delete(todo)
    db.commit()

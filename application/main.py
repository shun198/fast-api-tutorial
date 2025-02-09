from typing import Annotated, List

from database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, status
from models import Base, Todos
from schemas import TodoModel, TodoResponse
from sqlalchemy import select, update
from sqlalchemy.orm import Session

app = FastAPI()

# https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all
# テーブルを作成
Base.metadata.create_all(bind=engine)

# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/?h=get_db
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/api/health")
def health_check():
    return {"msg": "pass"}


# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/?h=get_db#sub-dependencies-with-yield
# https://github.com/fastapi/fastapi/pull/9298
# FastAPI0.95.0以降の機能
@app.get("/api/todos", response_model=List[TodoResponse])
# 依存性注入をすることでget_dbメソッドが自動的に呼ばるので毎回セッションインスタンスの生成やセッションを切る処理を書かずに済む
# Annotatedを使うことでDepends(get_db)がSession型だとわかる
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-session-dependency
def read_todos(db: db_dependency):
    # https://docs.sqlalchemy.org/en/20/orm/quickstart.html#simple-select
    # https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalars
    # scalarsを使うことでTodosのインスタンスを返す
    todos =  db.scalars(select(Todos).order_by(Todos.id)).all()
    return todos


@app.get("/api/todos/{todo_id}", response_model=TodoResponse)
def read_todo(db: db_dependency, todo_id: int):
    todo = db.get(Todos, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@app.post("/api/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(db: db_dependency, todo_model: TodoModel):
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


@app.put("/todo/{todo_id}", response_model=TodoResponse)
async def update_todo(db: db_dependency ,todo_model: TodoModel, todo_id: int):
    todo = db.get(Todos, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.execute(update(Todos).where(todo.id == todo_id).values(**todo_model.model_dump()))
    db.commit()
    return todo


@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int):
    todo = db.get(Todos, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    # https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete
    db.delete(todo)
    db.commit()

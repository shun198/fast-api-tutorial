from typing import Annotated

from database import SessionLocal, engine
from fastapi import Depends, FastAPI
from models import Base, Todos
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

@app.get("/api/health")
def health_check():
    return {"msg": "pass"}


# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/?h=get_db#sub-dependencies-with-yield
# https://github.com/fastapi/fastapi/pull/9298
# FastAPI0.95.0以降の機能
@app.get("/api/todos")
# 依存性注入をすることでget_dbメソッドが自動的に呼ばるので毎回セッションインスタンスの生成やセッションを切る処理を書かずに済む
# Annotatedを使うことでDepends(get_db)がSession型だとわかる
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-session-dependency
def read_todos(db: Annotated[Session, Depends(get_db)]):
    return db.query(Todos).all()

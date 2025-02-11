# from database import engine
from fastapi import FastAPI

# from models import Base
from routers import auth, todos

app = FastAPI()

# https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all
# テーブルを作成
# Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)


@app.get("/api/health")
def health_check():
    return {"msg": "pass"}

from fastapi import FastAPI
from routers import auth, todos

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)


@app.get("/api/health")
def health_check():
    return {"msg": "pass"}

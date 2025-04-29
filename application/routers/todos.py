from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from infrastructure.database import db_dependency
from models import Todos
from routers.auth import get_current_user
from schemas.todos import CreateTodoModel, TodoIsComplete, TodoResponse, UpdateTodoModel
from sqlalchemy import delete, select, update
from usercases.todo_usecase import TodoUsecase

router = APIRouter(prefix="/api/todos", tags=["todos"])


user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("", response_model=List[TodoResponse])
async def read_todos(user: user_dependency, db: db_dependency, todo_usecase: TodoUsecase):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    return todo_usecase.get_all_todos(user)


@router.get("/completed", response_model=List[TodoResponse])
async def read_completed_todos(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    todos = db.scalars(
        select(Todos)
        .filter(Todos.owner_id == user.id, Todos.complete == True)
        .order_by(Todos.id)
    ).all()
    return todos


@router.get("/{todo_id}", response_model=TodoResponse)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    todo = db.scalars(
        select(Todos).filter(
            Todos.id == todo_id, Todos.owner_id == user.id, Todos.complete == False
        )
    ).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.get("/completed/{todo_id}", response_model=TodoResponse)
async def read_completed_todo(user: user_dependency, db: db_dependency, todo_id: int):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    todo = db.scalars(
        select(Todos).filter(Todos.id == todo_id, Todos.owner_id == user.id),
        Todos.complete == True,
    ).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Completed todo not found"
        )
    return todo


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency, db: db_dependency, todo_model: CreateTodoModel
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    todo = Todos(**todo_model.model_dump(), owner_id=user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    user: user_dependency, db: db_dependency, todo_model: UpdateTodoModel, todo_id: int
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    todo = db.scalars(
        select(Todos).filter(Todos.id == todo_id, Todos.owner_id == user.id)
    ).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    db.execute(
        update(Todos)
        .where(Todos.id == todo_id, Todos.owner_id == user.id)
        .values(**todo_model.model_dump())
    )
    db.commit()
    return todo


@router.delete("/bulk_delete", status_code=status.HTTP_204_NO_CONTENT)
async def bulk_delete_todo(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    db.execute(delete(Todos).where(Todos.owner_id == user.id))
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    todo = db.scalars(
        select(Todos).filter(Todos.id == todo_id, Todos.owner_id == user.id)
    ).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    db.delete(todo)
    db.commit()


@router.patch(
    "/toggle_todo_complete/{todo_id}",
    status_code=status.HTTP_200_OK,
    response_model=TodoResponse,
)
async def toggle_todo_complete(
    user: user_dependency, db: db_dependency, todo_model: TodoIsComplete, todo_id: int
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    todo = db.scalars(
        select(Todos).filter(Todos.id == todo_id, Todos.owner_id == user.id)
    ).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    db.execute(
        update(Todos)
        .where(Todos.id == todo_id, Todos.owner_id == user.id)
        .values(**todo_model.model_dump())
    )
    db.commit()
    return todo


# ファイルアップロード機能
# https://github.com/minio/minio

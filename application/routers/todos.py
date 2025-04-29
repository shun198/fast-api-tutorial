from typing import List

from config.dependency import db_dependency, get_todo_usecase, user_dependency
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.todo_schema import CreateTodoModel, TodoResponse, UpdateTodoModel
from usecases.todo_usecase import TodoUsecase

router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.get("", response_model=List[TodoResponse])
async def read_todos(
    user: user_dependency, todo_usecase: TodoUsecase = Depends(get_todo_usecase)
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    return todo_usecase.get_all_todos(user)


@router.get("/{todo_id}", response_model=TodoResponse)
async def read_todo(
    user: user_dependency,
    todo_id: int,
    todo_usecase: TodoUsecase = Depends(get_todo_usecase),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    todo = todo_usecase.read_todo(user, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency,
    todo_model: CreateTodoModel,
    todo_usecase: TodoUsecase = Depends(get_todo_usecase),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    return todo_usecase.create_todo(user, todo_model)


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_model: UpdateTodoModel,
    todo_id: int,
    todo_usecase: TodoUsecase = Depends(get_todo_usecase),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    todo = todo_usecase.read_todo(user, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo_usecase.update_todo(user, todo_model, todo)


@router.delete("/bulk_delete", status_code=status.HTTP_204_NO_CONTENT)
async def bulk_delete_todo(
    user: user_dependency,
    todo_usecase: TodoUsecase = Depends(get_todo_usecase),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    todo_usecase.bulk_delete_todo(user)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    todo_id: int,
    todo_usecase: TodoUsecase = Depends(get_todo_usecase),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    todo = todo_usecase.read_todo(user, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    todo_usecase.delete_todo(todo)


# ファイルアップロード機能
# https://github.com/minio/minio

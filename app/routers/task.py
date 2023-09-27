from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.oauth2 import require_user
from app.models.task import TaskModel
from app.schemas.task import (
    TaskCreateSchema,
    TaskUpdateSchema,
    TaskResponse,
    TaskListResponse,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Retrieve all tasks
@router.get("/", response_model=TaskListResponse)
async def get_tasks(db: Session = Depends(get_db), user=Depends(require_user)):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user).all()
    return {"count": len(tasks), "tasks": tasks}


# Retrieve a specific task by id
@router.get("/{id}", response_model=TaskResponse)
async def get_task(id: str, db: Session = Depends(get_db), user=Depends(require_user)):
    task_model = db.query(TaskModel).filter(TaskModel.id == id).first()
    if not task_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found"
        )
    if task_model.user_id != user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized action"
        )
    return task_model


# Update a task
@router.put("/{id}", response_model=TaskResponse)
async def update_task(
    id: str,
    task: TaskUpdateSchema,
    db: Session = Depends(get_db),
    user=Depends(require_user),
):
    task_query = db.query(TaskModel).filter(TaskModel.id == id)
    task_model = task_query.first()
    if not task_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found"
        )
    if task_model.user_id != user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized action"
        )
    task_query.update(task.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return task_model


# Create a new task
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
async def create_task(
    task: TaskCreateSchema, db: Session = Depends(get_db), user=Depends(require_user)
):
    task_model = TaskModel(**task.model_dump())
    task_model.user_id = user
    db.add(task_model)
    db.commit()
    db.refresh(task_model)
    return task_model


# Delete a task
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, db: Session = Depends(get_db), user=Depends(require_user)):
    task_query = db.query(TaskModel).filter(TaskModel.id == id)
    task_model = task_query.first()
    if not task_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found"
        )
    if task_model.user_id != user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized action"
        )
    task_query.delete(synchronize_session=False)
    db.commit()
    return

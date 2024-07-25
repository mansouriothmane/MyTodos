from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_session
from app.oauth2 import require_user
from app.models.task import TaskOrm
from app.schemas.task import (
    TaskCreateSchema,
    TaskUpdateSchema,
    TaskResponse,
    TaskListResponse,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Retrieve all tasks
@router.get("/", response_model=TaskListResponse)
async def get_tasks(session: Session = Depends(get_session), user: str = Depends(require_user)):
    tasks = session.query(TaskOrm).filter(TaskOrm.user_id == user).all()
    return {"count": len(tasks), "tasks": tasks}


# Retrieve a specific task by id
@router.get("/{id}", response_model=TaskResponse)
async def get_task(
    id: str, session: Session = Depends(get_session), user: str = Depends(require_user)
):
    task_model = session.query(TaskOrm).filter(TaskOrm.id == id).first()
    if not task_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found"
        )
    if str(task_model.user_id) != user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized action"
        )
    return task_model


# Update a task
@router.put("/{id}", response_model=TaskResponse)
async def update_task(
    id: str,
    task: TaskUpdateSchema,
    session: Session = Depends(get_session),
    user: str = Depends(require_user),
):
    task_query = session.query(TaskOrm).filter(TaskOrm.id == id)
    task_model = task_query.first()
    if not task_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found"
        )
    if str(task_model.user_id) != user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized action"
        )
    task_query.update(task.model_dump(exclude_unset=True), synchronize_session=False)
    session.commit()
    return task_model


# Create a new task
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
async def create_task(
    task: TaskCreateSchema,
    session: Session = Depends(get_session),
    user: str = Depends(require_user),
):
    task_model = TaskOrm(**task.model_dump())
    task_model.user_id = user
    session.add(task_model)
    session.commit()
    session.refresh(task_model)
    return task_model


# Delete a task
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: str, session: Session = Depends(get_session), user: str = Depends(require_user)
):
    task_query = session.query(TaskOrm).filter(TaskOrm.id == id)
    task_model = task_query.first()
    if not task_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found"
        )
    if str(task_model.user_id) != user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized action"
        )
    task_query.delete(synchronize_session=False)
    session.commit()
    return

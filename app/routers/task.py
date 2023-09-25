from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task import TaskModel
from app.schemas.task import TaskCreateSchema, TaskUpdateSchema, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Retrieve all tasks
@router.get("/", response_model=List[TaskResponse])
async def get_tasks(db: Session = Depends(get_db)) -> List[TaskResponse]:
    tasks = db.query(TaskModel).all()
    return tasks


# Retrieve a specific task by id
@router.get("/{id}", response_model=TaskResponse)
async def get_task(id: str, db: Session = Depends(get_db)) -> TaskResponse:
    task = db.query(TaskModel).filter(TaskModel.id == id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found"
        )
    return task


# Update a task
@router.put("/{id}", response_model=TaskResponse)
async def update_task(
    id: str, task: TaskUpdateSchema, db: Session = Depends(get_db)
) -> TaskResponse:
    task_query = db.query(TaskModel).filter(TaskModel.id == id)
    updated_task = task_query.first()
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found"
        )
    task_query.update(task.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_task


# Create a new task
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
async def create_task(
    task: TaskCreateSchema, db: Session = Depends(get_db)
) -> TaskResponse:
    created_task = TaskModel(**task.model_dump())
    db.add(created_task)
    db.commit()
    db.refresh(created_task)
    return created_task


# Delete a task
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, db: Session = Depends(get_db)):
    task_query = db.query(TaskModel).filter(TaskModel.id == id)
    task_to_delete = task_query.first()
    if not task_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found"
        )
    task_query.delete(synchronize_session=False)
    db.commit()
    return

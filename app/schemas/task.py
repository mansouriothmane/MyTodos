from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, UUID4


class TaskBaseSchema(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskResponse(TaskBaseSchema):
    id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    count: int
    tasks: List[TaskResponse]


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[str] = None

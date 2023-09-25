from typing import Optional
from datetime import datetime

from pydantic import BaseModel, UUID4


class TaskBaseSchema(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False
    user_id: UUID4


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskResponse(TaskBaseSchema):
    id: UUID4
    created_at: datetime
    updated_at: datetime


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[str] = None

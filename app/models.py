from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from .database import TaskStatus

class TaskBase(BaseModel):
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING

class TaskCreate(TaskBase):
    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    model_config = ConfigDict(from_attributes=True)

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

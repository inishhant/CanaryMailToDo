from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# TAG SCHEMAS
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True  # 👈 Pydantic v2 compatible

# TASK SCHEMAS
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: date
    is_completed: Optional[bool] = False
    tags: Optional[List[str]] = []  # For incoming payload only

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    tags: List[Tag]  # 👈 Now returns full tag objects in responses

    class Config:
        from_attributes = True

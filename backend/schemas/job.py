from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobCreate(BaseModel):
    title: str
    description: str

class JobResponse(BaseModel):
    id: int
    recruiter_id: int
    title: str
    description: str
    requirements: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

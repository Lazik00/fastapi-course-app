from pydantic import BaseModel
from typing import Optional

class CourseCreate(BaseModel):
    title: str
    description: str
    category_id: int
    video_url: Optional[str] = None

class CourseOut(BaseModel):
    id: int
    title: str
    description: str
    video_url: Optional[str]
    category_id: int

    class Config:
        from_attributes = True

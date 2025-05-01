from pydantic import BaseModel
from typing import List, Optional

class CategoryBase(BaseModel):
    name: str
    description: Optional[str]

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(BaseModel):
    id: int
    name: str
    description: str
    image: str

    class Config:
        orm_mode = True


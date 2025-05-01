from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base  # TO‘G‘RI

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    courses = relationship("Course", back_populates="category")

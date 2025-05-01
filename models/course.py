from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base  # TO‘G‘RI: umumiy Base dan olinyapti

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    video_url = Column(String)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="courses")

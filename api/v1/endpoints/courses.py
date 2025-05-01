from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from models.course import Course
from models.category import Category
from schemas.course import CourseOut
from db.session import get_db
from core.security import get_current_user, admin_required
import os, shutil
from typing import Optional
UPLOAD_DIR = "videos/"

router = APIRouter(prefix="", tags=["Courses"])

@router.post("/create_course", response_model=CourseOut)
async def create_course(
    title: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    video_url: Optional[str] = Form(None),
    video_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)

):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Kategoriya topilmadi.")

    final_video_url = ""
    if video_file:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_location = os.path.join(UPLOAD_DIR, video_file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(video_file.file, buffer)
        final_video_url = file_location
    elif video_url:
        final_video_url = video_url

    course = Course(
        title=title,
        description=description,
        category_id=category_id,
        video_url=final_video_url
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

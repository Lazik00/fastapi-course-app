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
from typing import List
from fastapi import Query

@router.get("/courses", response_model=List[CourseOut])
async def get_all_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses


@router.get("/courses/{course_id}", response_model=CourseOut)
async def get_course_by_id(
    course_id: int,
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs topilmadi.")
    return course

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

from fastapi import Path

@router.put("/update_course/{course_id}", response_model=CourseOut)
async def update_course(
    course_id: int = Path(...),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    video_url: Optional[str] = Form(None),
    video_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs topilmadi.")

    if title:
        course.title = title
    if description:
        course.description = description
    if category_id:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Kategoriya topilmadi.")
        course.category_id = category_id

    if video_file:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_location = os.path.join(UPLOAD_DIR, video_file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(video_file.file, buffer)
        course.video_url = file_location
    elif video_url:
        course.video_url = video_url

    db.commit()
    db.refresh(course)
    return course

@router.delete("/delete_course/{course_id}")
async def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs topilmadi.")

    db.delete(course)
    db.commit()
    return {"detail": "Kurs muvaffaqiyatli o‘chirildi."}

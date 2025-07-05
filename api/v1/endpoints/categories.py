# routes/category.py
from fastapi import  HTTPException
from core.security import admin_required,get_current_user
from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
import shutil
import os
from db.session import get_db
from models.category import Category
from schemas.category import CategoryOut
from core.security import admin_required
router = APIRouter(prefix="", tags=["Categories"])


UPLOAD_DIR = "media/categories"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=CategoryOut)
def create_category(
    name: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    # 📁 Faylni saqlash
    folder_path = "media/categories"
    os.makedirs(folder_path, exist_ok=True)
    save_path = os.path.join(folder_path, image.filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    file_url = f"/media/categories/{image.filename}"

    db_category = Category(
        name=name,
        description=description,
        image=file_url
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/{category_id}/courses")
def get_courses_by_category(category_id: int, db: Session = Depends(get_db),current_user=Depends(get_current_user)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Kategoriya topilmadi!")
    return category.courses

from typing import Optional
from fastapi import Path

@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int = Path(...),
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Kategoriya topilmadi!")

    if name:
        category.name = name
    if description:
        category.description = description
    if image:
        # Yangi faylni saqlash
        folder_path = "media/categories"
        os.makedirs(folder_path, exist_ok=True)
        save_path = os.path.join(folder_path, image.filename)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        category.image = f"/media/categories/{image.filename}"

    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Kategoriya topilmadi!")

    db.delete(category)
    db.commit()
    return {"detail": "Kategoriya o‘chirildi."}

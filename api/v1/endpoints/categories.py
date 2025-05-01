# routes/category.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from models.category import Category
from schemas.category import CategoryCreate, CategoryOut
from core.security import admin_required,get_current_user

router = APIRouter(prefix="", tags=["Categories"])

@router.post("/", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db),current_user=Depends(admin_required)
):
    db_category = Category(**category.dict())
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
        raise HTTPException(status_code=404, detail="Kategoriya topilmadi.")
    return category.courses

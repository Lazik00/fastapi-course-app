import os
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from db.base import Base
from db.session import engine, SessionLocal
from core.security import get_password_hash
from models.user import User
from models.course import Course
from models.category import Category

from api.v1.endpoints import auth, courses, categories
from db.init_db import create_tables

def create_default_admin():
    db: Session = SessionLocal()
    admin_username = "admin"
    admin_password = "admin123"

    existing_admin = db.query(User).filter(User.username == admin_username).first()

    if not existing_admin:
        admin_user = User(
            username=admin_username,
            hashed_password=get_password_hash(admin_password),
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        print(f"✅ Admin foydalanuvchi yaratildi: {admin_username} / {admin_password}")
    else:
        print("ℹ️ Admin foydalanuvchi allaqachon mavjud.")
    db.close()

app = FastAPI()

# 🔐 OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

create_tables()
create_default_admin()

video_folder = "videos"
os.makedirs(video_folder, exist_ok=True)
app.mount("/videos", StaticFiles(directory=video_folder), name="videos")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])

@app.get("/")
def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "Bu himoyalangan yo‘l", "token": token}

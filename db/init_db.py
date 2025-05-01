# db/init_db.py
from db.base import Base
from db.session import engine

# Modellarni bu yerga import qilamiz
from models.user import User
from models.course import Course
from models.category import Category

def create_tables():
    print("📦 Jadval yaratish boshlandi...")
    Base.metadata.create_all(bind=engine)
    print("✅ Barcha jadvallar yaratildi.")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"  # yoki sening postgres urling

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # SQLite uchun
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 💥 Mana shu yerga qo‘shamiz:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

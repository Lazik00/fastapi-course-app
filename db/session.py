# db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"  # Postgres bo‘lsa, URL ni shu yerda almashtirasan

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Faqat SQLite uchun kerak
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

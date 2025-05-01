# db/init_db.py
from db.base import Base
from db.session import engine

def create_tables():
    Base.metadata.create_all(bind=engine)

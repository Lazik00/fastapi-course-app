from sqlalchemy import Column, Integer, String, Boolean
from db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)  # ❗️ username bor
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

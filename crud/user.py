from sqlalchemy.orm import Session
from models.user import User
from core.security import verify_password, get_password_hash
from schemas.user import UserCreate
def get_user_by_email(db: Session, email: str):

    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):

    user = db.query(User).filter(User.email == email).first()  # username -> email
    if not user:
        return None
    if not verify_password(password, user.hashed_password):  # password -> hashed_password
        return None
    return user



def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user_data: UserCreate):
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        hashed_password=hashed_password,
        is_admin=False  # ❗️ signup qilgan user admin emas!
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user



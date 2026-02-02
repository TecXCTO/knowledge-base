# Database helpers


from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext
from datetime import datetime
from jose import jwt, JWTError
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ------------------------------------------------------------------
# USER CRUD
# ------------------------------------------------------------------
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user_in: schemas.UserCreate):
    hashed_pw = pwd_context.hash(user_in.password)
    db_user = models.User(username=user_in.username, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_pwd: str, hashed_pwd: str):
    return pwd_context.verify(plain_pwd, hashed_pwd)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# ------------------------------------------------------------------
# ENTRY CRUD
# ------------------------------------------------------------------
def get_entries(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.KnowledgeEntry).offset(skip).limit(limit).all()

def get_entry(db: Session, entry_id: int):
    return db.query(models.KnowledgeEntry).filter(models.KnowledgeEntry.id == entry_id).first()

def create_entry(db: Session, entry_in: schemas.KnowledgeBaseEntryCreate, user_id: int):
    db_entry = models.KnowledgeEntry(
        title=entry_in.title,
        content=entry_in.content,
        category=entry_in.category,
        author_id=user_id,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def update_entry(db: Session, entry_id: int, entry_in: schemas.KnowledgeBaseEntryUpdate):
    db_entry = get_entry(db, entry_id)
    if not db_entry:
        return None
    db_entry.title = entry_in.title
    db_entry.content = entry_in.content
    db_entry.category = entry_in.category
    db.commit()
    db.refresh(db_entry)
    return db_entry

def delete_entry(db: Session, entry_id: int):
    db_entry = get_entry(db, entry_id)
    if db_entry:
        db.delete(db_entry)
        db.commit()
        return True
    return False


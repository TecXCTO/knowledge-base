# Pydantic DTOs


from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Users
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Knowledge
class KnowledgeBaseEntryBase(BaseModel):
    title: str = Field(..., max_length=200)
    content: str
    category: Optional[str] = None

class KnowledgeBaseEntryCreate(KnowledgeBaseEntryBase):
    pass

class KnowledgeBaseEntryUpdate(KnowledgeBaseEntryBase):
    pass

class KnowledgeBaseEntry(KnowledgeBaseEntryBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

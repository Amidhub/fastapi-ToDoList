from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

class Config:
    orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_done: bool
    owner_id: int

class Config:
    orm_mode = True
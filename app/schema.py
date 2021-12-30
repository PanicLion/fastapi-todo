# ./app/schema.py

from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class CurrentUser(UserBase):
    id: int

    class Config:
        orm_mode = True


class TodoCreate(BaseModel):
    text: str
    completed: bool


class TodoOut(TodoCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None

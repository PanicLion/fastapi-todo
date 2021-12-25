# ./app/schema.py

from typing import Optional
from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    first_name: str
    last_name: str
    password: str


class TodoCreate(BaseModel):
    text: str
    completed: bool


class TodoUpdate(TodoCreate):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None
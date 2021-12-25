# ./app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    todos = relationship("Todo", back_populates="user", cascade="all, delete-orphan")


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    completed = Column(Boolean, server_default='FALSE', nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    
    user = relationship("User", back_populates="todos")


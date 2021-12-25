# ./app/crud.py

from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from . import models, schema

def create_todo(db: Session, current_user: int, todo_data: schema.TodoCreate):
    todo = models.Todo(user_id=current_user.id, **todo_data.dict())
   
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def update_todo(db: Session, id: int, todo_data: schema.TodoUpdate):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    todo.text = todo_data.text
    todo.completed = todo_data.completed
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    db.delete(todo)
    db.commit()

def get_user_todos(db: Session, user_id: int):
    return db.query(models.Todo).filter(models.Todo.user_id == user_id).all()

def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_email(db: Session, email: EmailStr):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user_data: schema.UserCreate):
    user = models.User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=user_data.password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

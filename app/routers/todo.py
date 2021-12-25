from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from .. import oauth2, schema, crud
from ..db import get_db

router = APIRouter(tags=["Todos"])


@router.get("/api/mytodos")
def get_own_todos(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """Return a list of Todos owned by current user"""
    print(f"------------------------------{current_user.email}")
    todos = crud.get_user_todos(db, current_user.id)
    return todos

@router.post("/api/todos")
def add_a_todo(todo_data: schema.TodoCreate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """Add a Todo"""
    todo = crud.create_todo(db, current_user, todo_data)
    return todo

@router.put("/api/todos/{todo_id}")
def update_a_todo(todo_id: int, todo_data: schema.TodoUpdate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """Update and return Todo for given id"""
    updated_todo = crud.update_todo(db, todo_id, todo_data)
    return updated_todo

@router.delete("/api/todos/{todo_id}")
def delete_a_todo(todo_id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """Delete Todo of given todo_id"""
    crud.delete_todo(db, todo_id)
    return {"detail": "Todo deleted"}
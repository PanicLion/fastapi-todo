from typing import List
from fastapi import APIRouter, status
from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response
from .. import oauth2, schema, models
from ..db import get_db


router = APIRouter(
    tags=["Todos"]
)


@router.get("/todos", response_model=List[schema.TodoOut])
def get_todos(current_user: schema.CurrentUser = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """Return a list of Todos owned by current user"""
    # todos = crud.get_user_todos(db, current_user.id)
    todos = db.query(models.Todo).filter(models.Todo.user_id == current_user.id).all()
    return todos


@router.get("/todos/{todo_id}", response_model=schema.TodoOut)
def get_todo(todo_id: int, current_user: schema.CurrentUser = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """Return a Todo owned by current user"""
    # todo = crud.get_todo(db, todo_id)
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
        )

    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Todo not found"
        )

    return todo


@router.post("/todos", status_code=status.HTTP_201_CREATED, response_model=schema.TodoOut)
def add_a_todo(todo_data: schema.TodoCreate, current_user: schema.CurrentUser = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """Add a Todo"""
    # todo = crud.create_todo(db, current_user, todo_data)
    todo = models.Todo(user_id=current_user.id, **todo_data.dict())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.put("/todos/{todo_id}", response_model=schema.TodoOut)
def update_a_todo(todo_id: int, todo_data: schema.TodoCreate, current_user: schema.CurrentUser = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """Update and return Todo for given id"""
    # updated_todo = crud.update_todo(db, todo_id, todo_data)
    todo_query = db.query(models.Todo).filter(models.Todo.id == todo_id)
    todo = todo_query.first()

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"todo with id {todo_id} not found"
        )

    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this todo"
        )

    todo_query.update(todo_data.dict(), synchronize_session=False)
    db.commit()

    return todo


@router.delete("/todos/{todo_id}")
def delete_a_todo(todo_id: int, current_user: schema.CurrentUser = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """Delete Todo of given todo_id"""
    # crud.delete_todo(db, todo_id)
    todo_query = db.query(models.Todo).filter(models.Todo.id == todo_id)
    todo = todo_query.first()

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"todo with id {todo_id} not found"
        )

    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this todo"
        )

    todo_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
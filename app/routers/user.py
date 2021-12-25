from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .. import oauth2, schema, utils, crud
from ..db import get_db

router = APIRouter(tags=["Users"])

@router.get("/api/me")
def read_logged_in_user(current_user: int = Depends(oauth2.get_current_user)):
    """Return user settings for current user"""
    return current_user

@router.post("/api/users")
def signup(user_data: schema.UserCreate, db: Session = Depends(get_db)):
    """Create new User"""
    user = crud.get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data.password = utils.get_password_hash(user_data.password)

    signedup_user = crud.create_user(db, user_data)
    
    return signedup_user

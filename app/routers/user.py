from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app import oauth2, schema, utils, models
from ..db import get_db


router = APIRouter(
    tags=["Users"]
)


@router.get("/users/me", response_model=schema.CurrentUser)
def read_logged_in_user(current_user: schema.CurrentUser = Depends(oauth2.get_current_user)):
    """Return user settings for current user"""
    return current_user


@router.post("/users", response_model=schema.CurrentUser, status_code=status.HTTP_201_CREATED)
def signup(user_data: schema.UserCreate, db: Session = Depends(get_db)):
    """Create new User"""
    # user = crud.get_user_by_email(db, user_data.email)
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Email already registered"
        )

    user_data.password = utils.get_password_hash(user_data.password)

    # signedup_user = crud.create_user(db, user_data)
    signedup_user = models.User(**user_data.dict())
    db.add(signedup_user)
    db.commit()
    db.refresh(signedup_user)
    
    return signedup_user

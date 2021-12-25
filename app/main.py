# ./app/main.py

from fastapi import FastAPI
from . import models
from .db import engine
from app.routers import todo, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(todo.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
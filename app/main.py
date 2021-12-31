# ./app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from . import models
from .db import engine
from app.routers import todo, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
<!Doctype html>
    <html>
        <body>
            <h1>Todo API</h1>
            <div class="btn-group">
                <a href="/docs"><button>SwaggerUI</button></a>
                <a href="/redoc"><button>Redoc</button></a>
            </div>
        </body>
    </html>
"""
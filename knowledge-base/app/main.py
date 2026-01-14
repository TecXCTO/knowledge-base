# # FastAPI entrypoint

from fastapi import FastAPI
from . import routers
from .database import engine, Base
from .models import Base as SQLBase

# Create tables on startup
def init_db():
    SQLBase.metadata.create_all(bind=engine)

app = FastAPI(title="Domain Expert Knowledge Base", description="A tiny, secure KB for experts.", version="0.1.0")

# Include routers
app.include_router(routers.auth.router)
app.include_router(routers.knowledge.router)

# Create DB tables
@app.on_event("startup")
def on_startup():
    init_db()

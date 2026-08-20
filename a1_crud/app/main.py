from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.api import api_router

from app.db.database import supabase

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="CRUD using FastAPI",
    lifespan=lifespan
)

app.include_router(api_router)
@app.get("/")
def root():
    return {"message": "Welcome to the 1st Assignment"}

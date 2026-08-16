from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.api import api_router

import os
from dotenv import load_dotenv
from app.db.database import PostgresRepository

load_dotenv()
POSTGRES_URL = os.getenv("DATABASE_URL")


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = PostgresRepository(connection_url=POSTGRES_URL)
    yield

app = FastAPI(
    title="CRUD using FastAPI",
    lifespan=lifespan
)

app.include_router(api_router)
@app.get("/")
def root():
    return {"message": "Welcome to the 1st Assignment"}

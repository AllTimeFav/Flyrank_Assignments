from fastapi import APIRouter
from app.api.endpoints import health, tasks

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health")
api_router.include_router(tasks.router, prefix="/tasks")

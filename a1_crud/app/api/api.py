from fastapi import APIRouter
from app.api.endpoints import health, tasks, auth

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health")
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(tasks.router, prefix="/tasks")

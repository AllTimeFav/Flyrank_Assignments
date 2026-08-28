from fastapi import Header
from app.db.database import supabase
from fastapi import HTTPException
from fastapi import status
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.api.endpoints import health, tasks, auth

security = HTTPBearer()

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health")
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(tasks.router, prefix="/tasks")


@api_router.get("/public/info", summary="Get public info")
def get_public_info():
    return {status.HTTP_200_OK: {"message": "Welcome stranger! This info is public." }}

@api_router.get("/protected/profile", summary="Get protected profile info")
def get_protected_profile_info(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    response = supabase.auth.get_user(token) 
    if not response.user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {status.HTTP_200_OK: {"User": response.user}}
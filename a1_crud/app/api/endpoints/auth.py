from app.api.deps import get_current_user
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends
from app.db.database import supabase
from fastapi import status
from fastapi import HTTPException
from fastapi import APIRouter

security = HTTPBearer()


router = APIRouter(tags=["Auth"])

@router.post("/signup", summary="Sign up")
def signup(email: str, password: str):
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email and password are required"
        )
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        print(response)
        if not response.user:
            raise HTTPException(status_code=500, detail="Failed to create user")
        return {"User": response.user}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", summary="Login")
def login(email: str, password: str):
    if not email or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email and password are required")
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if not response.user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        return {"Access Token": response.session.access_token, "Refresh Token": response.session.refresh_token}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/protected/profile", summary="Get protected profile info")
def get_protected_profile_info(current_user: dict = Depends(get_current_user)):
    return {status.HTTP_200_OK: {"User": current_user}}

@router.get("/protected/dashboard", summary="Get protected dashboard info")
def get_protected_dashboard_info(current_user: dict = Depends(get_current_user)):
    return {status.HTTP_200_OK: {"Dashboard": "Protected Dashboard"}}
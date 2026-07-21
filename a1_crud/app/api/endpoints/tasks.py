from fastapi import APIRouter

router = APIRouter()

tasks = []

@router.get("/")
def get_tasks():
    return {"message": "List of tasks"}
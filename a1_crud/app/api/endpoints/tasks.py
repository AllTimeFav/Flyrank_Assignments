from fastapi import status
from fastapi import HTTPException
from fastapi import APIRouter

router = APIRouter()

tasks = [
    {"id": 1, "title": "First Book", "done": False},
    {"id": 2, "title": "Second Book", "done": False},
    {"id": 3, "title": "Third Book", "done": True}
]

@router.get("/")
def get_tasks():
    return {"tasks": tasks}

@router.get("/{id}")
def return_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return {"task": task}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found"
    )
from app.schemas.task import Task
from app.db.database import supabase
from fastapi import status
from fastapi import HTTPException
from fastapi import APIRouter

router = APIRouter(tags=["Tasks"])

@router.get("/", summary="Get all the tasks", response_model=list[Task])
def get_tasks():
    response = supabase.table("tasks").select("id, title, done").order("id").execute()
    rows = response.data
    return [Task(id=row["id"], title=row["title"], done=bool(row["done"])) for row in rows]

@router.get("/{id}", summary="Get a task by id", response_model=Task)
def return_task(id: int):
    response = supabase.table("tasks").select("id, title, done").eq("id", id).execute()
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found"
        )
    row = response.data[0]
    return Task(id=row["id"], title=row["title"], done=bool(row["done"]))

@router.post("/", summary="Add a new task", response_model=Task)
def add_task(title: str):
    if title.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Title is required"
        )
    response = supabase.table("tasks").insert({"title": title}).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to insert task")
    row = response.data[0]
    return Task(id=row["id"], title=row["title"], done=bool(row["done"]))

@router.put("/{id}", summary="Update a task by id", response_model=Task)
def update_task(id: int, title: str, done: bool):
    if title.strip() == "" or done == None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Title and done are required"
        )
    response = supabase.table("tasks").update({"title": title, "done": done}).eq("id", id).execute()
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found"
        )
    row = response.data[0]
    return Task(id=row["id"], title=row["title"], done=bool(row["done"]))

@router.delete("/{id}", summary="Delete a task by id")
def delete_task(id: int):
    response = supabase.table("tasks").delete().eq("id", id).execute()
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found"
        )
    return {"message": "Task deleted successfully"}
from app.schemas.task import Task
from app.db.database import get_db_connection
from fastapi import status
from fastapi import HTTPException
from fastapi import APIRouter

router = APIRouter(tags=["Tasks"])

tasks = [
    {"id": 1, "title": "First Book", "done": False},
    {"id": 2, "title": "Second Book", "done": False},
    {"id": 3, "title": "Third Book", "done": True}
]

@router.get("/", summary="Get all the tasks", response_model=list[Task])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    return [Task(id=row["id"], title=row["title"], done=bool(row["done"])) for row in rows]

@router.get("/{id}", summary="Get a task by id", response_model=Task)
def return_task(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found"
        )
    return Task(id=row["id"], title=row["title"], done=bool(row["done"]))


@router.post("/", summary="Add a new task")
def add_task(title: str):
    if title.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Title is required"
        )
    id = len(tasks) + 1
    task = {"id": id, "title": title, "done": False}
    tasks.append(task)
    raise HTTPException(
        status_code=status.HTTP_201_CREATED, detail={"task": task},
    )

@router.put("/{id}", summary="Update a task by id")
def update_task(id: int, title: str, done: bool):
    if title.strip() == "" or done == None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Title and done are required"
        )
    for task in tasks:
        if task["id"] == id:
            task["title"] = title
            task["done"] = done
            raise HTTPException(
                status_code=status.HTTP_200_OK, detail={"task": task}
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found"
    )

@router.delete("/{id}", summary="Delete a task by id")
def delete_task(id : int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            raise HTTPException(
                status_code=status.HTTP_200_OK, detail=f"Task {id} deleted successfully"
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found"
    )
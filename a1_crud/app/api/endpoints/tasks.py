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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,))
    row = cursor.fetchone()
    conn.close()
    return Task(id=row["id"], title=row["title"], done=bool(row["done"]))    

@router.put("/{id}", summary="Update a task by id")
def update_task(id: int, title: str, done: bool):
    if title.strip() == "" or done == None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Title and done are required"
        )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (title, done, id))
    conn.commit()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found"
        )
    return Task(id=row["id"], title=row["title"], done=bool(row["done"]))

@router.delete("/{id}", summary="Delete a task by id")
def delete_task(id : int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return {"message": "Task deleted successfully"}
    return {"message": "Task not deleted"}
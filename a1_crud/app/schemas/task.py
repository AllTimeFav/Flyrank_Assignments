from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    done: bool

class Task(TaskBase):
    id: int
    done: bool

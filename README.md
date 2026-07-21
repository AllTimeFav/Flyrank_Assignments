# Flyrank Assignments

This repository contains multiple assignments for Flyrank, including a modern, professional FastAPI project (`a1_crud`) demonstrating a CRUD application using SQLAlchemy, Pydantic V2, and Alembic.

## How to Install & Run

Navigate to the `a1_crud` directory and run the application using `uv`:

```bash
cd a1_crud
uv run uvicorn app.main:app --reload
```

## API Endpoints

Here is a list of all available endpoints in the application:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health/` | Health check endpoint |
| GET | `/tasks/` | Get all the tasks |
| GET | `/tasks/{id}` | Get a task by id |
| POST | `/tasks/` | Add a new task |
| PUT | `/tasks/{id}` | Update a task by id |
| DELETE | `/tasks/{id}` | Delete a task by id |

## Example Request

```http
$ curl -i http://127.0.0.1:8000/

HTTP/1.1 200 OK
date: Tue, 21 Jul 2026 16:44:51 GMT
server: uvicorn
content-length: 43
content-type: application/json

{"message":"Welcome to the 1st Assignment"}
```

## Swagger Screenshot

![alt text](assets/swagger_ui.


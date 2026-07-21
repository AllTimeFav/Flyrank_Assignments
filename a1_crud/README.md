# FastAPI Professional Project

This is a modern, professional FastAPI project structure, managed with `uv`.

## Features

- **FastAPI** framework
- **Pydantic V2** for data validation and settings management
- **SQLAlchemy 2.0** for database ORM
- **Alembic** for database migrations
- **uv** for fast package and project management
- Modular directory structure

## Quickstart

1. **Install dependencies** (if not already done):
   ```bash
   uv sync
   ```

2. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```

3. **Run the application**:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

4. Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

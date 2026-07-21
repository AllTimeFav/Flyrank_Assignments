from fastapi import FastAPI

from app.api.api import api_router


app = FastAPI(
    title="CRUD using FastAPI"
)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Welcome to the 1st Assignment"}

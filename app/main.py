from fastapi import FastAPI

from app.database import setup_db
from app.tasks.router import tasks_router

app = FastAPI(title="Task Management API", version="1.0.0")

app.include_router(tasks_router)


@app.on_event("startup")
async def init_db():
    await setup_db()

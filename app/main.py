from fastapi import FastAPI

from app.auth.router import auth_router
from app.database import setup_db
from app.tasks.router import tasks_router

app = FastAPI(title="Task Management API", version="1.0.0")

app.include_router(tasks_router)
app.include_router(auth_router)


@app.on_event("startup")
async def init_db():
    await setup_db()

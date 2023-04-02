from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import auth_router
from app.database import setup_db
from app.tasks.router import tasks_router

app = FastAPI(title="Task Management API", version="1.0.0")

app.include_router(tasks_router)
app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def init_db():
    await setup_db()


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(
#         "app.main:app",
#         port=8000,
#         host="0.0.0.0",
#         reload=True,
#         ssl_keyfile="fastapi-key.pem",
#         ssl_certfile="fastapi.pem",
#     )

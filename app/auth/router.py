from fastapi import APIRouter

from app.auth import service
from app.auth.schemas import RegisterDto
from app.database import db_deps
from app.users.schemas import UserDto

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", response_model=UserDto)
async def register(data: RegisterDto, db: db_deps):
    return await service.register(db, data)

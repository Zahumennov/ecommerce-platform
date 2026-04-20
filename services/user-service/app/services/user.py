import uuid

from fastapi import HTTPException, status

from app.models import User
from app.repositories.user import UserRepository
from app.schemas import UserRegister, UserUpdate
from app.services.auth import hash_password, verify_password


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register(self, data: UserRegister) -> User:
        if await self.repo.exists_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )
        hashed = hash_password(data.password)
        return await self.repo.create(data, hashed)

    async def authenticate(self, email: str, password: str) -> User:
        user = await self.repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is disabled",
            )
        return user

    async def get_by_id(self, user_id: uuid.UUID) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    async def update(self, user: User, data: UserUpdate) -> User:
        return await self.repo.update(user, data)

    async def delete(self, user: User) -> None:
        await self.repo.delete(user)
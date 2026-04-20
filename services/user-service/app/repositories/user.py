import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserRegister, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: UserRegister, hashed_password: str) -> User:
        user = User(
            email=data.email,
            hashed_password=hashed_password,
            first_name=data.first_name,
            last_name=data.last_name,
        )
        self.session.add(user)
        await self.session.flush()  # sends INSERT but doesn't commit yet
        await self.session.refresh(user)  # loads generated fields (id, created_at)
        return user

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def update(self, user: User, data: UserUpdate) -> User:
        update_data = data.model_dump(exclude_none=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.flush()

    async def exists_by_email(self, email: str) -> bool:
        result = await self.session.execute(
            select(User.id).where(User.email == email)
        )
        return result.scalar_one_or_none() is not None
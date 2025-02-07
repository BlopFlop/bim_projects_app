from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from repository import RepositoryBase
from users.auth import get_password_hash
from users.models import User
from users.schemas import UserRegisterSchema


class UserRepository(RepositoryBase):
    """User repostiory."""

    async def create(self, obj_in: UserRegisterSchema) -> User:
        obj_in.password = get_password_hash(obj_in.password)
        return await super().create(obj_in)

    async def change_password(self, db_obj: User, password: str) -> User:
        db_obj.password = get_password_hash(password)
        self.session.add(db_obj)

        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj


async def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserRepository:
    """Get User repository."""

    return UserRepository(User, session)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from users.models import User
from repository import RepositoryBase
from users.schemas import UserRegister
from users.auth import get_password_hash


class UserRepository(RepositoryBase):
    """User repostiory."""

    def create(self, obj_in: UserRegister):
        obj_in.password = get_password_hash(obj_in.password)
        return super().create(obj_in)


async def get_user_repository(
    session: AsyncSession = Depends(get_async_session)
) -> UserRepository:
    """Get User repository."""

    return UserRepository(User, session)

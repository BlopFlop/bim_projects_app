from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from users.models import User
from repository import RepositoryBase


class UserRepository(RepositoryBase):
    """User repostiory."""


async def get_user_repository(
    session: AsyncSession = Depends(get_async_session)
) -> UserRepository:
    """Get User repository."""

    return UserRepository(User, session)

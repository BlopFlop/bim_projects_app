from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from project.models import RevitServer
from repository import RepositoryBase


class RevitServerRepository(RepositoryBase):
    """RevitServer repository."""


async def get_revit_server_repository(
    session: AsyncSession = Depends(get_async_session)
) -> RevitServerRepository:
    """Create RevitServer repository."""

    return RevitServerRepository(RevitServer, session)

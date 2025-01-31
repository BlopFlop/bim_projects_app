from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from project.models import Project
from repository import RepositoryBase


class ProjectRepository(RepositoryBase):
    """Project repository."""


async def get_project_repository(
    session: AsyncSession = Depends(get_async_session)
) -> ProjectRepository:
    """Create project repository."""

    return ProjectRepository(Project, session)

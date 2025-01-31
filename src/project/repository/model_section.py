from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from project.models import ModelSection
from repository import RepositoryBase


class ModelSectionRepository(RepositoryBase):
    """ModelSection repository."""


async def get_model_section_repository(
    session: AsyncSession = Depends(get_async_session)
) -> ModelSectionRepository:
    """Create ModelSection repository."""

    return ModelSectionRepository(ModelSection, session)

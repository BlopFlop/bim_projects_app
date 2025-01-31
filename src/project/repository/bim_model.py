from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from project.models import BIMModel
from repository import RepositoryBase


class BIMModelRepository(RepositoryBase):
    """BIMModel repository."""


async def get_bim_model_repository(
    session: AsyncSession = Depends(get_async_session)
) -> BIMModelRepository:
    """Create BIMModel repository."""

    return BIMModelRepository(BIMModel, session)

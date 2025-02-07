from pathlib import Path

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from src.config import test_database_config
from src.database import Base, User, get_async_session
from src.main import app

engine_test = create_async_engine(
    test_database_config.database_url, poolclass=NullPool
)
async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False, autoflush=False
)

Base.metadata.bind = engine_test

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

pytest_plugins = [
    "tests.fixtures.users",
]


async def override_db():
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(loop_scope="session", scope="module", autouse=True)
async def init_db():
    yield
    async with engine_test.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())
        conn.commit()

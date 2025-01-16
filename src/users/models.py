from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from src.database.core import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """User model."""

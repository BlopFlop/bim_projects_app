from pydantic import Field
from pydantic_settings import BaseSettings

from src.constants import ENV_PATH


class SettingsTestDatabase(BaseSettings):
    """Settings for test database."""
    postgres_db: str = Field(alias="TEST_DB")
    postgres_user: str = Field(alias="TEST_DB_USER")
    postgres_password: str = Field(alias="TEST_DB_PASSWORD")
    db_host: str = Field(alias="TEST_DB_SERVER")
    db_port: str = Field(alias="TEST_DB_PORT")

    @property
    def database_url(self) -> str:
        """Return database url from .env ."""
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.postgres_user,
            self.postgres_password,
            self.db_host,
            self.db_port,
            self.postgres_db,
        )

    class Config:
        """Config for the meta class in current settings."""

        env_file = ENV_PATH
        extra = "ignore"

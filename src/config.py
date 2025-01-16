from pydantic import Field
from pydantic_settings import BaseSettings

from .constants import ENV_PATH


class Settings(BaseSettings):
    """Settings for current project."""

    # FastAPI Project
    name_project: str = Field(alias="NAME_PROJECT")
    secret: str = Field(alias="SECRET")
    first_superuser_email: str = Field(alias="FIRST_SUPERUSER_EMAIL")
    first_superuser_password: str = Field(alias="FIRST_SUPERUSER_PASSWORD")

    # Database .evn
    postgres_db: str = Field(alias="POSTGRES_DB")
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    db_host: str = Field(alias="POSTGRES_SERVER")
    db_port: str = Field(alias="POSTGRES_PORT")

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


settings = Settings()

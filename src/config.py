from pydantic import Field
from pydantic_settings import BaseSettings

from constants import ENV_PATH


class _SettingsBase(BaseSettings):
    """Base settings."""

    class Config:
        """Config for the meta class in current settings."""

        env_file = ENV_PATH
        extra = "ignore"


class SettingsApp(_SettingsBase):
    """Settings FastApi application."""

    name_project: str = Field(alias="APP_NAME_PROJECT")
    secret: str = Field(alias="APP_SECRET")
    first_superuser_email: str = Field(alias="APP_FIRST_SUPERUSER_EMAIL")
    first_superuser_password: str = Field(alias="APP_FIRST_SUPERUSER_PASSWORD")


class SettingsDatabase(_SettingsBase):
    """Settings Database."""

    postgres_db: str = Field(alias="DB")
    postgres_user: str = Field(alias="DB_USER")
    postgres_password: str = Field(alias="DB_PASSWORD")
    db_host: str = Field(alias="DB_SERVER")
    db_port: str = Field(alias="DB_PORT")

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


class RabbitMQSettings(_SettingsBase):
    """Settings for RabbitMQ."""
    pass


application_config = SettingsApp()
database_config = SettingsDatabase()
rabbit_config = RabbitMQSettings()

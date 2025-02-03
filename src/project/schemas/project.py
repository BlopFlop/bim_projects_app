from datetime import datetime, timezone
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)


class ProjectSchemaBase(BaseModel):
    """Base schema for Project."""

    name: str = Field(
        min_length=1,
        max_length=150,
        title="Short name",
        description=(
            "Короткое внутреннее имя проекта."
            " Допустимая длина строки — от 1 до 150 символов включительно;"
        )
    )
    description: str = Field(
        min_length=1,
        max_length=350,
        title="Long name or description",
        description=(
            "Длинное имя(с адресом и т.д.) или описание проекта."
            " допустимая длина строки — от 1 до 350 символов включительно;"
        )
    )
    code: str = Field(
        min_length=1,
        max_length=50,
        title="Code",
        description=(
            "Код проекта, обязательное уникальное строковое поле, по данному"
            " коду будут искаться модели в директориях; допустимая длина "
            "строки - от 1 до 50 символов включительно."
        )
    )
    image: Optional[str] = Field(
        max_length=150,
        title="Image",
        description=(
            "Путь до изоображения;"
            " допустимая длина строки - от 0 до 150 символов включительно;"
        )
    )
    created_on: Optional[datetime] = Field(
        datetime.now(timezone.utc),
        title="Date created project",
        description="Дата и время создания проекта."
    )

    base_path: str = Field(
        min_length=1,
        max_length=200,
        title="Path base three",
        description=(
            "Путь до базовой директории, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 200 символов включительно;"
        ),
    )
    arch_path: str = Field(
        min_length=1,
        max_length=200,
        title="Path arch three",
        description=(
            "Путь до архивной директории, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 200 символов включительно;"
        )
    )
    ftp_path: str = Field(
        min_length=1,
        max_length=200,
        title="FTP path three",
        description=(
            "Путь до FTP директории, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 200 символов включительно;"
        ),
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "011_UNI_NIKT",
                "description": (
                    "Жилой дом с подземной автостоянкой"
                    " и нежилыми помещениями."
                ),
                "code": "NIKT",
                "image": "static_path",
                # "created_on": "2025-01-31 12:28:58.206249+00:00",
                "base_path": r"R:\101_BIM-Projects",
                "arch_path": r"R:\100_Archive",
                "ftp_path": r"\\l-ftp\Root\Unipro_FTP-01"
            }
        }


class ProjectSchemaCreate(ProjectSchemaBase):
    """Create schema for project."""


class ProjectSchemaUpdate(ProjectSchemaBase):
    """Update schema for project"""

    name: Optional[str] = Field(
        min_length=1,
        max_length=150,
        title="Short name",
        description=(
            "Короткое внутреннее имя проекта."
            " Допустимая длина строки — от 1 до 150 символов включительно;"
        )
    )
    description: Optional[str] = Field(
        min_length=1,
        max_length=350,
        title="Long name or description",
        description=(
            "Длинное имя(с адресом и т.д.) или описание проекта."
            " допустимая длина строки — от 1 до 350 символов включительно;"
        )
    )
    code: Optional[str] = Field(
        min_length=1,
        max_length=50,
        title="Code",
        description=(
            "Код проекта, обязательное уникальное строковое поле, по данному"
            " коду будут искаться модели в директориях; допустимая длина "
            "строки - от 1 до 50 символов включительно."
        )
    )
    image: Optional[str] = Field(
        max_length=150,
        title="Image",
        description=(
            "Путь до изоображения;"
            " допустимая длина строки - от 0 до 150 символов включительно;"
        )
    )

    base_path: Optional[str] = Field(
        min_length=1,
        max_length=200,
        title="Path base three",
        description=(
            "Путь до базовой директории, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 200 символов включительно;"
        ),
    )
    arch_path: Optional[str] = Field(
        min_length=1,
        max_length=200,
        title="Path arch three",
        description=(
            "Путь до архивной директории, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 200 символов включительно;"
        )
    )
    ftp_path: Optional[str] = Field(
        min_length=1,
        max_length=200,
        title="FTP path three",
        description=(
            "Путь до FTP директории, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 200 символов включительно;"
        ),
    )


class ProjectSchemaDB(ProjectSchemaBase):
    """Project DB schema."""

    id: int = Field(
        title="Id project in db",
        description="Id проекта в базе данных"
    )

    class Config:
        """Config class for this model."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "011_UNI_NIKT",
                "description": (
                    "Жилой дом с подземной автостоянкой"
                    " и нежилыми помещениями."
                ),
                "code": "NIKT",
                "image": "static_path",
                "created_on": "2025-01-31 12:28:58.206249+00:00",
                "base_path": r"R:\101_BIM-Projects",
                "arch_path": r"R:\100_Archive",
                "ftp_path": r"\\l-ftp\Root\Unipro_FTP-01"
            }
        }

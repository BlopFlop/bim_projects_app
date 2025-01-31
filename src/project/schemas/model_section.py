from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)


class ModelSectionBase(BaseModel):
    """Base schema for Seciton."""

    name: str = Field(
        max_length=1,
        min_length=150,
        title="Name",
        description=(
            "Уникальное название раздела, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 150 символов включительно;"
        ),
    )
    description: str = Field(
        max_length=1,
        min_length=350,
        title="Description",
        description=(
            "Описание имя раздела модели, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 350 символов включительно;"
        ),
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Архитектурный раздел",
                "description": (
                    "Раздел 'Архитектура' в проектной документации содержит "
                    "описание архитектурных решений, которые определяют облик "
                    "и функциональность объекта строительства."
                )
            }
        }


class ModelSectionCreate(ModelSectionBase):
    """Create schema for Seciton."""


class ModelSectionUpdate(ModelSectionBase):
    """Update schema for Seciton."""

    name: Optional[str] = Field(
        max_length=1,
        min_length=150,
        title="Name",
        description=(
            "Уникальное название раздела, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 150 символов включительно;"
        ),
    )
    description: Optional[str] = Field(
        max_length=1,
        min_length=350,
        title="Description",
        description=(
            "Описание имя раздела модели, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 350 символов включительно;"
        ),
    )


class ModelSectionDB(ModelSectionBase):
    """Base schema for Seciton."""

    id: int = Field(
        title="Id section in db",
        description="Id раздела модели в базе данных"
    )

    class Config:
        """Config class for this model."""

        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Архитектурный раздел",
                "description": (
                    "Раздел 'Архитектура' в проектной документации содержит "
                    "описание архитектурных решений, которые определяют облик "
                    "и функциональность объекта строительства."
                )
            }
        }

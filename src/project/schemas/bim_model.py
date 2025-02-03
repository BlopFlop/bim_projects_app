from datetime import datetime
from typing import Optional, Final

from fastapi.exceptions import HTTPException
from pydantic import (
    BaseModel,
    Field,
    field_validator,
)

from project.models import ModelTypeEnum


class BIMModelSchemaBase(BaseModel):
    """Base schema for Project."""

    name_file: str = Field(
        min_length=1,
        max_length=150,
        title="Name file(*whthout extention).",
        description=(
            "Название модели, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 150 символов включительно;"
        )
    )
    type: ModelTypeEnum = Field(
        default=ModelTypeEnum.SUPPORT,
        title="Model type",
        description="Тип модели."
    )
    version: int = Field(
        title="Version file",
        description=(
            "Версия Revit, обязательное целочисленное поле;"
            " допустимое значение от 2000 до 2100 включительно"
        )
    )
    extention: str = Field(
        min_length=1,
        max_length=10,
        title="Extention file",
        description=(
            "Расширение файла, обязательное строковое поле; "
            "Допустимая длина строки - от 1 до 10 включительно;"
        )
    )
    path: str = Field(
        min_length=1,
        max_length=200,
        title="Path file",
        description=(
            "Путь до файла, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 200 символов включительно;"
        )
    )
    created_on: Optional[datetime] = Field(
        title="Date created model.",
        description="Дата и время создания файла."
    )
    updated_on: Optional[datetime] = Field(
        title="Date updated model.",
        description="Дата и время обновления файла."
    )

    class Config:
        """Config class for this model."""

        json_schema_extra = {
            "example": {
                "name_file": "011_UNI_NIKT_AR_R22",
                "type": "Рабочая модель внутренняя",
                "version": 2022,
                "extention": "rvt",
                "path": "011_NIKT/011_01_WIP/01_AR",
                "created_on": "2025-01-31 12:28:58.206249+00:00",
                "updated_on": "2025-01-31 12:28:58.206249+00:00"
            }
        }

    @field_validator("version")
    def version_file_validator(cls, value: int) -> int:
        MIN_VER: Final = 2000
        MAX_VER: Final = 2100
        if not (MIN_VER <= value <= MAX_VER):
            except_msg = (
                f"Значение {value} должно быть в пределах"
                f" значений от {MIN_VER} до {MAX_VER} включительно.")
            raise HTTPException(400, detail=except_msg)
        return value


class BIMModelSchemaCreate(BIMModelSchemaBase):
    """Create schema for BIM model."""


class BIMModelSchemaUpdate(BIMModelSchemaBase):
    """Create schema for BIM model."""

    name_file: Optional[str] = Field(
        min_length=1,
        max_length=150,
        title="Name file(*whthout extention).",
        description=(
            "Название модели, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 150 символов включительно;"
        )
    )
    type: Optional[ModelTypeEnum] = Field(
        default=ModelTypeEnum.SUPPORT,
        title="Model type",
        description="Тип модели."
    )
    version: Optional[int] = Field(
        title="Version file",
        description=(
            "Версия Revit, обязательное целочисленное поле;"
            " допустимое значение от 2000 до 2100 включительно"
        )
    )
    extention: Optional[str] = Field(
        min_length=1,
        max_length=10,
        title="Extention file",
        description=(
            "Расширение файла, обязательное строковое поле; "
            "Допустимая длина строки - от 1 до 10 включительно;"
        )
    )
    path: Optional[str] = Field(
        min_length=1,
        max_length=200,
        title="Path file",
        description=(
            "Путь до файла, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 200 символов включительно;"
        )
    )


class BIMModelSchemaDB(BIMModelSchemaBase):
    """BIM model schema DB."""

    id: int = Field(
        title="Id BIM model in db",
        description="Id BIM модели в базе данных"
    )

    class Config:
        """Config class for this model."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name_file": "011_UNI_NIKT_AR_R22",
                "type": "Рабочая модель внутренняя",
                "version": 2022,
                "extention": "rvt",
                "path": "011_NIKT/011_01_WIP/01_AR",
                "created_on": "2025-01-31 12:28:58.206249+00:00",
                "updated_on": "2025-01-31 12:28:58.206249+00:00"
            }
        }

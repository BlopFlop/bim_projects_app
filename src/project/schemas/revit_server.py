from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator


class RevitServerBase(BaseModel):
    """Base schema for RevitServer."""

    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            ext_msg = "Field name cannot be empty."
            raise HTTPException(status_code=422, detail=ext_msg)
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "name": "10.10.1.30",
            }
        }


class RevitServerCreate(RevitServerBase):
    """Create schema for RevitServer."""


class RevitServerDB(RevitServerBase):
    """DB schema for RevitServer."""

    id: int = Field(
        title="Id RevitServer in db", description="Id Сервера в модели."
    )

    class Config:
        """Config class for this model."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "10.10.1.30",
            }
        }

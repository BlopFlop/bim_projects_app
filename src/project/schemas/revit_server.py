from pydantic import (
    BaseModel,
    Field,
)


class RevitServerBase(BaseModel):
    """Base schema for RevitServer."""

    name: str

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
        title="Id RevitServer in db",
        description="Id Сервера в модели."
    )

    class Config:
        """Config class for this model."""

        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "10.10.1.30",
            }
        }
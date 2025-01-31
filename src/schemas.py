from pydantic import BaseModel


class CreateSchemaType(BaseModel):
    """Type schema."""

    class Config:
        json_schema_extra = {
            "example": {
                "any": "test schema",
            }
        }


class UpdateSchemaType(CreateSchemaType):
    """Create schema for Seciton."""


class DBSchemaType(CreateSchemaType):
    """Create schema for Seciton."""

    class Config:
        """Config class for this model."""

        orm_mode = True
        json_schema_extra = {
            "example": {
                "any": "test schema",
            }
        }

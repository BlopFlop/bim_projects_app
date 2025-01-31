from http import HTTPStatus

from fastapi import HTTPException
from schemas import DBSchemaType, CreateSchemaType, UpdateSchemaType

from repository import RepositoryBase


async def check_fields_duplicate(
    schema: CreateSchemaType | UpdateSchemaType,
    fields_set: list[str],
    repository: RepositoryBase
) -> None | HTTPException:
    """Check duplicate unique field in DB."""
    elements: list[DBSchemaType] = await repository.get_multi()

    ununique_fields = {}
    for element in elements:
        for field in fields_set:
            schema_attr = getattr(schema, field)
            element_attr = getattr(element, field)
            if schema_attr and schema_attr == element_attr:
                ununique_fields[field] = schema_attr
        if ununique_fields:
            ununique_fields = ", ".join([
                f"{key} = {value}" for key, value in ununique_fields.items()
            ])
            exc_msg = (
                "Вы должны передать уникальные значения,"
                f" значения полей уже существуют: {ununique_fields} "
            )
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=exc_msg,
            )

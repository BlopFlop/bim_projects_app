from typing import Sequence
from http import HTTPStatus

from fastapi import HTTPException
from schemas import DBSchemaType, CreateSchemaType, UpdateSchemaType

from repository import RepositoryBase


async def check_email_duplicate(
    email: str,
    repository: RepositoryBase
) -> None | HTTPException:
    """Check duplicate email in DB."""
    element: DBSchemaType = await repository.get_obj_for_field_arg(
        "email", email, many=False
    )
    if element:
        exc_msg = "Пользователь с таким email уже существует."
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=exc_msg,
        )


async def check_number_duplicate(
    phone_number: str,
    repository: RepositoryBase
) -> None | HTTPException:
    """Check duplicate user number."""
    element: DBSchemaType = await repository.get_obj_for_field_arg(
        "phone_number", phone_number, many=False
    )
    if element:
        exc_msg = "Пользователь с таким номером уже существует."
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=exc_msg,
        )

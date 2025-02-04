from http import HTTPStatus

from fastapi import HTTPException
from pydantic import EmailStr

from repository import RepositoryBase
from users.models import User
from users.auth import verify_password


async def check_email_duplicate(
    email: str,
    repository: RepositoryBase
) -> None | HTTPException:
    """Check duplicate email in DB."""
    user: User = await repository.get_obj_for_field_arg(
        "email", email, many=False
    )
    if user:
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
    user: User = await repository.get_obj_for_field_arg(
        "phone_number", phone_number, many=False
    )
    if user:
        exc_msg = "Пользователь с таким номером уже существует."
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=exc_msg,
        )


async def validate_email_and_password(
    email: EmailStr,
    password: str,
    repository: RepositoryBase
) -> User:
    user: User = await repository.get_obj_for_field_arg(
        "email", arg=email, many=False
    )
    if user and verify_password(
        plain_password=password,
        hashed_password=user.password
    ):
        return user
    exc_msg = "Неверная почта или пароль."
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail=exc_msg,
    )

from fastapi import HTTPException, status
from pydantic import EmailStr

from repository import RepositoryBase
from users.auth import verify_password
from users.models import User


async def check_email_duplicate(
    email: str, repository: RepositoryBase
) -> None | HTTPException:
    """Check duplicate email in DB."""
    user: User = await repository.get_obj_for_field_arg(
        "email", email, many=False
    )
    if user:
        exc_msg = "Пользователь с таким email уже существует."
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc_msg,
        )


async def check_number_duplicate(
    phone_number: str, repository: RepositoryBase
) -> None | HTTPException:
    """Check duplicate user number."""
    user: User = await repository.get_obj_for_field_arg(
        "phone_number", phone_number, many=False
    )
    if user:
        exc_msg = "Пользователь с таким номером уже существует."
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc_msg,
        )


async def validate_email(email: EmailStr, repository: RepositoryBase) -> User:
    """Validate email has in DB."""
    user: User = await repository.get_obj_for_field_arg(
        "email", arg=email, many=False
    )
    if not user:
        exc_msg = "Неверная почта."
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc_msg,
        )
    return user


def validate_password(
    user: User,
    password: str,
) -> None:
    """Validate password has in DB."""
    if not verify_password(
        plain_password=password, hashed_password=user.password
    ):
        ext_msg = "Старый пароль неверный."
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=ext_msg
        )


async def validate_user_id(id: int, user_repository: RepositoryBase) -> User:
    """Validate user id has in DB."""
    user = await user_repository.get(id)
    if user:
        return user
    exc_msg = "Пользователя с данным id не существует."
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=exc_msg
    )

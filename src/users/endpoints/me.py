from fastapi import APIRouter, Depends

from schemas import MessageSchema
from users.models import User
from users.repository import UserRepository, get_user_repository
from users.schemas import (
    StatusCode201,
    StatusCode401,
    StatusCode409,
    StatusCode422,
    UserChangePassword,
    UserSchemaDB,
    UserUpdateSchema,
)
from users.utils import get_current_user
from users.validatiors import (
    check_email_duplicate,
    check_number_duplicate,
    validate_password,
)

router = APIRouter()


@router.get(
    "/",
    summary="Получить пользователя.",
    description="Получает текущего пользователя выполнившего запрос.",
    responses={
        200: {"model": UserSchemaDB},
        401: {"model": StatusCode401},
        409: {"model": StatusCode409},
        422: {"model": StatusCode422},
    },
)
async def get_me(user: User = Depends(get_current_user)) -> UserSchemaDB:
    return user


@router.patch(
    "/",
    summary="Изменить пользователя.",
    description="Изменяет текущего пользователя выполнившего запрос.",
    status_code=201,
    responses={
        201: {"model": UserSchemaDB},
        401: {"model": StatusCode401},
        409: {"model": StatusCode409},
        422: {"model": StatusCode422},
    },
)
async def change_me(
    user_update: UserUpdateSchema,
    user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserSchemaDB:
    await check_email_duplicate(
        email=user_update.email, repository=user_repository
    )
    await check_number_duplicate(
        phone_number=user_update.phone_number, repository=user_repository
    )
    return await user_repository.update(user, user_update)


@router.delete(
    "/",
    summary="Удалить пользователя.",
    description="Удаляет текущего пользователя выполнившего запрос.",
    status_code=204,
    responses={
        401: {"model": StatusCode401},
        409: {"model": StatusCode409},
        422: {"model": StatusCode422},
    },
)
async def change_me(
    user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
):
    await user_repository.remove(user)
    return MessageSchema(message="Вы были удалены.")


@router.patch(
    "/change_password/",
    summary="Изменить пароль пользователя.",
    description="Изменяет пароль текущего пользователя выполнившего запрос.",
    status_code=201,
    responses={
        201: {"model": StatusCode201},
        401: {"model": StatusCode401},
        409: {"model": StatusCode409},
        422: {"model": StatusCode422},
    },
)
async def change_password(
    change_pass_data: UserChangePassword,
    user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
) -> MessageSchema:
    validate_password(user=user, password=change_pass_data.old_password)
    await user_repository.change_password(
        db_obj=user, password=change_pass_data.new_password
    )
    return MessageSchema(message="Пароль успешно изменен.")

from fastapi import APIRouter, Depends

from schemas import MessageSchema
from users.models import User
from users.repository import UserRepository, get_user_repository
from users.schemas import (
    StatusCode400,
    StatusCode401,
    StatusCode403,
    StatusCode409,
    StatusCode422,
    UserSchemaDB,
    UserUpdateSchema,
)
from users.utils import get_current_admin_user
from users.validatiors import (
    check_email_duplicate,
    check_number_duplicate,
    validate_user_id,
)

router = APIRouter()


@router.get(
    "/",
    summary="Получить всех пользователей.",
    description=(
        "Получает всех пользователей если у вас есть права администратора."
    ),
    responses={
        200: {"model": list[UserSchemaDB]},
        401: {"model": StatusCode401},
        403: {"model": StatusCode403},
        409: {"model": StatusCode409},
        422: {"model": StatusCode422},
    },
)
async def get_all_users(
    current_user: User = Depends(get_current_admin_user),
    user_repository: UserRepository = Depends(get_user_repository),
) -> list[UserSchemaDB]:
    return await user_repository.get_multi()


@router.get(
    "/{user_id}/",
    summary="Получить пользователя по id",
    description=(
        "Получает пользователя по id если у вас есть права администратора."
    ),
    responses={
        200: {"model": UserSchemaDB},
        400: {"model": StatusCode400},
        401: {"model": StatusCode401},
        403: {"model": StatusCode403},
        409: {"model": StatusCode409},
        422: {"model": StatusCode422},
    },
)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserSchemaDB:
    return await validate_user_id(user_id, user_repository=user_repository)


@router.patch(
    "/{user_id}/",
    response_model=UserSchemaDB,
    summary="Изменить пользователя по id",
    description=(
        "Изменяет пользователя по id если у вас есть права администратора."
    ),
    status_code=201,
    responses={
        201: {"model": UserSchemaDB},
        400: {"model": StatusCode400},
        401: {"model": StatusCode401},
        403: {"model": StatusCode403},
        409: {"model": StatusCode409},
        422: {"model": StatusCode422},
    },
)
async def change_user(
    user_id: int,
    user_update: UserUpdateSchema,
    current_user: User = Depends(get_current_admin_user),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserSchemaDB:
    user = await validate_user_id(id=user_id, user_repository=user_repository)
    await check_email_duplicate(
        email=user_update.email, repository=user_repository
    )
    await check_number_duplicate(
        phone_number=user_update.phone_number, repository=user_repository
    )
    return await user_repository.update(user, user_update)


@router.delete(
    "/{user_id}/",
    summary="Удалить пользователя по id",
    description=(
        "Удаляет пользователя по id если у вас есть права администратора."
    ),
    status_code=204,
    responses={
        400: {"model": StatusCode400},
        401: {"model": StatusCode401},
        403: {"model": StatusCode403},
        409: {"model": StatusCode409},
        422: {"model": StatusCode422},
    },
)
async def delete_user(
    user_id: int,
    user: User = Depends(get_current_admin_user),
    user_repository: UserRepository = Depends(get_user_repository),
):
    user = await validate_user_id(id=user_id, user_repository=user_repository)
    await user_repository.remove(user)
    return MessageSchema(message="Пользователь удален.")

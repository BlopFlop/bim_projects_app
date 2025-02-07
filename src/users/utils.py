import contextlib

from fastapi import Depends, HTTPException, status

from config import application_config
from database.core import get_async_session
from users.auth import get_user_id_for_token
from users.models import User
from users.repository import UserRepository, get_user_repository
from users.schemas import UserRegisterSuperuserSchema

get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def get_current_user(
    user_id: int = Depends(get_user_id_for_token),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    user = await user_repository.get(user_id)
    if not user:
        ext_msg = "User not found"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=ext_msg
        )
    return user


async def get_current_admin_user(
    user: User = Depends(get_current_user),
) -> User:
    """Get administration user."""
    if user.is_admin or user.is_superuser:
        return user
    ext_msg = "Недостаточно прав!"
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ext_msg)


async def create_user(user: UserRegisterSuperuserSchema):
    """Create user item for DB."""
    async with get_async_session_context() as session:
        user_repository = await get_user_repository(session)

        user_db = await user_repository.get_obj_for_field_arg(
            User.email.key, arg=user.email, many=False
        )

        if not user_db:
            await user_repository.create(user)


async def create_first_superuser():
    """Autocreaete first superuser."""
    if (
        application_config.first_superuser_email is not None
        and application_config.first_superuser_password is not None
    ):
        user = UserRegisterSuperuserSchema(
            email=application_config.first_superuser_email,
            password=application_config.first_superuser_password,
            phone_number=application_config.first_superuser_phone,
            first_name=application_config.first_superuser_first_name,
            last_name=application_config.first_superuser_last_name,
        )
        await create_user(user)

import contextlib
from contextlib import suppress

from fastapi_users.exceptions import UserAlreadyExists

from config import application_config
from database.core import get_async_session


from users.models import User
from users.repository import get_user_repository
from users.routers import router as user_router
from users.schemas import UserRegisterSuperuserSchema


get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def create_user(user: UserRegisterSuperuserSchema):
    """Create user item for DB."""
    with suppress(UserAlreadyExists):
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
        application_config.first_superuser_email is not None and
        application_config.first_superuser_password is not None
    ):
        user = UserRegisterSuperuserSchema(
            email=application_config.first_superuser_email,
            password=application_config.first_superuser_password,
            phone_number=application_config.first_superuser_phone,
            first_name=application_config.first_superuser_first_name,
            last_name=application_config.first_superuser_last_name
        )
        await create_user(user)

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from src.users.repository import get_user_repository
from src.users.schemas import UserRegisterAdminSchema, UserRegisterSchema
from src.users.utils import get_current_admin_user
from tests.conftest import User, app, get_async_session, override_db

superuser = User(
    id=1,
    phone_number="+8921301203",
    first_name="test_email1",
    last_name="test_email1",
    email="test_email1@gmail.com",
    is_user=True,
    is_admin=True,
    is_superuser=True,
)

user = User(
    id=2,
    phone_number="+8921012063",
    first_name="test_email2",
    last_name="test_email2",
    email="test_email2@gmail.com",
    is_user=True,
    is_admin=False,
    is_superuser=False,
)


@pytest.mark.asyncio
@pytest_asyncio.fixture(loop_scope="session", scope="module")
async def superuser_db() -> User:
    session = await override_db().__anext__()
    user_repository = await get_user_repository(session=session)
    data = {
        "phone_number": "+8921301203",
        "first_name": "test_email1",
        "last_name": "test_email1",
        "email": "test_email13141@gmail.com",
        "password": "tesstyeret345",
        "is_user": True,
        "is_admin": True,
        "is_superuser": True,
    }
    user_schema = UserRegisterAdminSchema(**data.copy())
    user = await user_repository.get_obj_for_field_arg(
        "email", user_schema.email, many=True
    )
    if not user:
        user = await user_repository.create(user_schema)
    await session.aclose()
    return UserRegisterAdminSchema(**data)


@pytest.mark.asyncio
@pytest_asyncio.fixture(loop_scope="session", scope="module")
async def user_db():
    session = await override_db().__anext__()
    user_repository = await get_user_repository(session=session)
    data = {
        "phone_number": "+892130123403",
        "first_name": "test_emai56l1",
        "last_name": "test_emai7l1",
        "email": "test_email41232@gmail.com",
        "password": "tesstyeret345",
    }
    user_schema = UserRegisterSchema(**data.copy())
    user = await user_repository.get_obj_for_field_arg(
        "email", user_schema.email, many=True
    )
    if not user:
        user = await user_repository.create(user_schema)
    await session.aclose()
    return UserRegisterSchema(**data)


@pytest.fixture(scope="session")
def test_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def admin_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    app.dependency_overrides[get_current_admin_user] = lambda: superuser
    with TestClient(app) as client:
        yield client


valid_user_data_1 = {
    "phone_number": "+892101206783",
    "first_name": "test_email4",
    "last_name": "test_email4",
    "email": "test_email4@gmail.com",
    "password": "super_password",
}
valid_user_data_2 = {
    "phone_number": "+892101204356",
    "first_name": "test_email5",
    "last_name": "test_email5",
    "email": "test_email5@gmail.com",
    "password": "super_password",
}
valid_user_data_3 = {
    "phone_number": "+89210120536783",
    "first_name": "test_email6",
    "last_name": "test_email6",
    "email": "test_email6@gmail.com",
    "password": "super_password",
}
valid_user_data_4 = {
    "phone_number": "+8921012806783",
    "first_name": "test_email4",
    "last_name": "test_email4",
    "email": "test_email34@gmail.com",
    "password": "super_password",
}
valid_user_data_5 = {
    "phone_number": "+8921091204356",
    "first_name": "test_email5",
    "last_name": "test_email5",
    "email": "test_email250@gmail.com",
    "password": "super_password",
}
valid_user_data_6 = {
    "phone_number": "+892130120536783",
    "first_name": "test_email8",
    "last_name": "test_email9",
    "email": "test_email20@gmail.com",
    "password": "super_password",
}
valid_user_data_7 = {
    "phone_number": "+392101206783",
    "first_name": "test_email4",
    "last_name": "test_email4",
    "email": "test_email4@gmail.com",
    "password": "super_password",
}
valid_user_data_8 = {
    "phone_number": "+492101204356",
    "first_name": "test_email78",
    "last_name": "test_email85",
    "email": "test_emai56@gmail.com",
    "password": "super_password",
}
valid_user_data_9 = {
    "phone_number": "+5210120536783",
    "first_name": "test_email66",
    "last_name": "test_emai9l6",
    "email": "test_e9mail6@gmail.com",
    "password": "super_password",
}

invalid_user_data_1 = {
    "phone_number": "89210120536783",
    "first_name": "test_email7",
    "last_name": "test_email7",
    "email": "test_email7@gmail.com",
    "password": "super_password",
}
invalid_user_data_2 = {
    "phone_number": "+a89210120536783",
    "first_name": "test_email8",
    "last_name": "test_email8",
    "email": "test_email8@gmail.com",
    "password": "super_password",
}
invalid_user_data_3 = {
    "phone_number": "+892101205436783",
    "first_name": "1 ",
    "last_name": "test_email9",
    "email": "test_email9@gmail.com",
    "password": "super_password",
}
invalid_user_data_4 = {
    "phone_number": "+8921012053436783",
    "first_name": "test_email10",
    "last_name": "1 ",
    "email": "test_email11@gmail.com",
    "password": "super_password",
}
invalid_user_data_5 = {
    "phone_number": "+892101205346783",
    "first_name": "test_email12",
    "last_name": "test_email12",
    "email": "test_email12 ",
    "password": "super_password",
}
invalid_user_data_6 = {
    "phone_number": "+892101204236783",
    "first_name": "test_email16",
    "last_name": "test_email16",
    "email": "$#@#!test_email16@gmail.com",
    "password": "super_password",
}
invalid_user_data_7 = {
    "phone_number": "+892101205367583",
    "first_name": "test_email36",
    "last_name": "test_email36",
    "email": "test_email36@gmail.com",
    "password": "^",
}
invalid_user_data_8 = {
    "phone_number": "+892101205362783",
    "first_name": "test_email46",
    "last_name": "test_email46",
    "email": "test_email46@gmail.com",
    "password": " ",
}

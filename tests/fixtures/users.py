import pytest
from tests.conftest import (
    app,
    get_async_session,
    override_db,
    User
)
from fastapi import HTTPException
from fastapi.testclient import TestClient

from src.users.auth import get_current_admin_user, get_current_user

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


@pytest.fixture(scope="class")
def user_client():
    def raise_forbidden():
        raise HTTPException(status_code=403, detail="Forbidden")

    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_current_admin_user] = lambda: raise_forbidden()
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    with TestClient(app) as client:
        yield client


@pytest.fixture
def superuser_client():
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
    "password": "super_password"
}
valid_user_data_2 = {
    "phone_number": "+892101204356",
    "first_name": "test_email5",
    "last_name": "test_email5",
    "email": "test_email5@gmail.com",
    "password": "super_password"
}
valid_user_data_3 = {
    "phone_number": "+89210120536783",
    "first_name": "test_email6",
    "last_name": "test_email6",
    "email": "test_email6@gmail.com",
    "password": "super_password"
}

ivalid_user_data_1 = {
    "phone_number": "89210120536783",
    "first_name": "test_email7",
    "last_name": "test_email7",
    "email": "test_email7@gmail.com",
    "password": "super_password"
}
ivalid_user_data_2 = {
    "phone_number": "+a89210120536783",
    "first_name": "test_email8",
    "last_name": "test_email8",
    "email": "test_email8@gmail.com",
    "password": "super_password"
}
ivalid_user_data_3 = {
    "phone_number": "+892101205436783",
    "first_name": "1 ",
    "last_name": "test_email9",
    "email": "test_email9@gmail.com",
    "password": "super_password"
}
ivalid_user_data_4 = {
    "phone_number": "+8921012053436783",
    "first_name": "test_email10",
    "last_name": "1 ",
    "email": "test_email11@gmail.com",
    "password": "super_password"
}
ivalid_user_data_5 = {
    "phone_number": "+892101205346783",
    "first_name": "test_email12",
    "last_name": "test_email12",
    "email": "test_email12 ",
    "password": "super_password"
}
ivalid_user_data_6 = {
    "phone_number": "+892101204236783",
    "first_name": "test_email16",
    "last_name": "test_email16",
    "email": "$#@#!test_email16@gmail.com",
    "password": "super_password"
}
ivalid_user_data_7 = {
    "phone_number": "+892101205367583",
    "first_name": "test_email36",
    "last_name": "test_email36",
    "email": "test_email36@gmail.com",
    "password": "^"
}
ivalid_user_data_8 = {
    "phone_number": "+892101205362783",
    "first_name": "test_email46",
    "last_name": "test_email46",
    "email": "test_email46@gmail.com",
    "password": " "
}

from typing import Any

import pytest

from fastapi.testclient import TestClient

from tests.fixtures.users import (
    valid_user_data_1,
    valid_user_data_2,
    valid_user_data_3,

    ivalid_user_data_1,
    ivalid_user_data_2,
    ivalid_user_data_3,
    ivalid_user_data_4,
    ivalid_user_data_5,
    ivalid_user_data_6,
    ivalid_user_data_7,
    ivalid_user_data_8,
)


REGISTER_URL = "/api/v1/auth/register/"


@pytest.mark.parametrize(
    "user_data",
    (
        valid_user_data_1,
        valid_user_data_2,
        valid_user_data_3,
    )
)
def test_register(test_client: TestClient, user_data: dict[str: Any]):
    response = test_client.post(REGISTER_URL, json=user_data)
    assert response.status_code == 201, (
        "Проверьте статус ответа API: при регистрации пользователя "
        f"корректный POST-запрос к эндпоинту {REGISTER_URL} "
        "должен вернуть ответ со статусом 201."
    )
    data = response.json()
    expected_keys = {
        "email",
        "first_name",
        "id",
        "is_admin",
        "is_superuser",
        "last_name",
        "phone_number"
    }
    missing_keys = expected_keys - data.keys()
    assert not missing_keys, (
        f"В ответе на корректный POST-запрос к эндпоинту `{REGISTER_URL}` не "
        f'хватает следующих ключей: `{"`, `".join(missing_keys)}`'
    )
    user_data = {
        "phone_number": user_data.get("phone_number"),
        "first_name": user_data.get("first_name"),
        "last_name": user_data.get("last_name"),
        "email": user_data.get("email"),
        "is_admin": False,
        "is_superuser": False,
    }
    data.pop("id")
    assert data == user_data, (
        "При регистрации пользователя тело ответа"
        " API отличается от ожидаемого."
    )


@pytest.mark.parametrize(
    "user_data",
    (
        ivalid_user_data_1,
        ivalid_user_data_2,
        ivalid_user_data_3,
        ivalid_user_data_4,
        ivalid_user_data_5,
        ivalid_user_data_6,
        ivalid_user_data_7,
        ivalid_user_data_8,
    )
)
def test_register_invalid_data(
    user_client: TestClient,
    user_data: dict[str: Any]
):
    response = user_client.post(REGISTER_URL, json=user_data)
    assert response.status_code == 422, (
        "Проверьте статус ответа API: "
        "при регистрации пользователя некорректный POST-запрос "
        f"к эндпоинту`{REGISTER_URL}` должен вернуть ответ со статусом 422."
    )
    data = response.json()
    assert list(data.keys()) == ["detail"], (
        "Убедитесь, что в ответе на некорректный POST-запрос "
        f"к эндпоинту `{REGISTER_URL}` есть ключ `detail`."
    )
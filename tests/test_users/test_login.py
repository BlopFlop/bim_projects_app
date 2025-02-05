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


LOGIN_URL = "/api/v1/auth/login/"
REGISTER_URL = "/api/v1/auth/register/"


@pytest.mark.parametrize(
    "user_data",
    (
        valid_user_data_1,
        valid_user_data_2,
        valid_user_data_3,
    )
)
def test_login(test_client: TestClient, user_data: dict[str: Any]):
    response = test_client.post(REGISTER_URL, json=user_data)
    user_data = {
        "email": user_data.get("email"),
        "password": user_data.get("password")
    }
    response = test_client.post(LOGIN_URL, json=user_data)
    assert response.status_code == 200, (
        "Проверьте статус ответа API: при логировании пользователя "
        f"корректный POST-запрос к эндпоинту {LOGIN_URL} "
        "должен вернуть ответ со статусом 200."
    )
    data = response.json()
    expected_keys = {
        "access_token",
        "refresh_token"
    }
    missing_keys = expected_keys - data.keys()
    assert not missing_keys, (
        f"В ответе на корректный POST-запрос к эндпоинту `{LOGIN_URL}` не "
        f'хватает следующих ключей: `{"`, `".join(missing_keys)}`'
    )


@pytest.mark.parametrize(
    "user_data",
    (
        valid_user_data_1,
        valid_user_data_2,
        valid_user_data_3,
        ivalid_user_data_6
    )
)
def test_login_invalid_data(test_client: TestClient, user_data: dict[str: Any]):
    user_data = {
        "email": user_data.get("email"),
        "password": "kjkjjkljjlkllk"
    }
    response = test_client.post(LOGIN_URL, json=user_data)
    assert response.status_code == 401, (
        "Проверьте статус ответа API: при логировании пользователя "
        f"корректный POST-запрос к эндпоинту {LOGIN_URL} "
        "должен вернуть ответ со статусом 401."
    )


@pytest.mark.parametrize(
    "user_data",
    (
        ivalid_user_data_6,
        ivalid_user_data_7,
    )
)
def test_login_invalid_data(
    user_client: TestClient,
    user_data: dict[str: Any]
):
    response = user_client.post(LOGIN_URL, json=user_data)
    assert response.status_code == 422, (
        "Проверьте статус ответа API: "
        "при регистрации пользователя некорректный POST-запрос "
        f"к эндпоинту`{LOGIN_URL}` должен вернуть ответ со статусом 422."
    )

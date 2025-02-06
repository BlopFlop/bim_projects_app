from typing import Any

import pytest
import pytest_asyncio

from fastapi.testclient import TestClient

from tests.fixtures.users import (
    valid_user_data_1,
    valid_user_data_2,
    valid_user_data_3,
    valid_user_data_4,
    valid_user_data_5,
    valid_user_data_6,
    valid_user_data_7,
    valid_user_data_8,
    valid_user_data_9,

    invalid_user_data_1,
    invalid_user_data_2,
    invalid_user_data_3,
    invalid_user_data_4,
    invalid_user_data_5,
    invalid_user_data_6,
    invalid_user_data_7,
    invalid_user_data_8
)


REGISTER_URL = "/api/v1/auth/register/"
LOGIN_URL = "/api/v1/auth/login/"
LOGOUT_URL = "/api/v1/auth/logout/"
REGISTER_URL = "/api/v1/auth/register/"
ME_URL = "/api/v1/auth/me/"
CHANGE_PASS_URL = "/api/v1/auth/me/change_password/"
USERS_URL = "/api/v1/auth/users/"


def register_and_login_client(
    test_client: TestClient,
    user_data: dict[str: Any]
):
    test_client.post(REGISTER_URL, json=user_data)
    user_data = {
        "email": user_data.get("email"),
        "password": user_data.get("password")
    }
    test_client.post(LOGIN_URL, json=user_data)
    return test_client.post(LOGIN_URL, json=user_data)


def login_client(client: TestClient, email: str, password: str):
    user_data = {
        "email": email,
        "password": password
    }
    return client.post(LOGIN_URL, json=user_data)


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
        invalid_user_data_1,
        invalid_user_data_2,
        invalid_user_data_3,
        invalid_user_data_4,
        invalid_user_data_5,
        invalid_user_data_6,
        invalid_user_data_7,
        invalid_user_data_8,
    )
)
def test_register_invalid_data(
    test_client: TestClient,
    user_data: dict[str: Any]
):
    response = test_client.post(REGISTER_URL, json=user_data)
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
    assert response.status_code == 201, (
        "Проверьте статус ответа API: при логировании пользователя "
        f"корректный POST-запрос к эндпоинту {LOGIN_URL} "
        "должен вернуть ответ со статусом 201."
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
        invalid_user_data_5,
        invalid_user_data_6,
        invalid_user_data_7,
        invalid_user_data_8
    )
)
def test_login_invalid_data(
    test_client: TestClient,
    user_data: dict[str: Any]
):
    user_data = {
        "email": user_data.get("email"),
        "password": user_data.get("password")
    }
    response = test_client.post(LOGIN_URL, json=user_data)
    assert response.status_code == 422, (
        "Проверьте статус ответа API: при логировании пользователя "
        f"корректный POST-запрос к эндпоинту {LOGIN_URL} "
        "должен вернуть ответ со статусом 422."
    )


@pytest.mark.parametrize(
    "user_data",
    (
        valid_user_data_1,
        valid_user_data_2,
        valid_user_data_3,
    )
)
def test_get_me(test_client: TestClient, user_data: dict[str: Any]):
    register_and_login_client(test_client, user_data)

    response = test_client.get(ME_URL)
    assert response.status_code == 200, (
        "Проверьте статус ответа API: при получении данных пользователя "
        f"корректный GET-запрос к эндпоинту {ME_URL} "
        "должен вернуть ответ со статусом 200."
    )
    data: dict[str, Any] = response.json()
    data.pop("id")
    user_data = user_data.copy()
    user_data.pop("password")
    user_data["is_admin"] = False
    user_data["is_superuser"] = False

    missing_keys = user_data.keys() - data.keys()
    assert not missing_keys, (
        f"В ответе на корректный POST-запрос к эндпоинту `{ME_URL}` не "
        f'хватает следующих ключей: `{"`, `".join(missing_keys)}`'
    )
    assert data == user_data, (
        "При получении данных пользователя тело ответа"
        " API отличается от ожидаемого."
    )


@pytest.mark.parametrize(
    "user_data",
    (
        valid_user_data_1,
        valid_user_data_2,
        valid_user_data_3,
    )
)
def test_logout(test_client: TestClient, user_data: dict[str: Any]):
    register_and_login_client(test_client, user_data)
    response = test_client.post(LOGOUT_URL)
    assert response.status_code == 200, (
        "Проверьте статус ответа API: при логировании пользователя "
        f"корректный POST-запрос к эндпоинту {LOGOUT_URL} "
        "должен вернуть ответ со статусом 200."
    )
    response = test_client.get(ME_URL)
    assert response.status_code == 401, (
        "Проверьте статус ответа API: при получении данных пользователя "
        f"вышедшего из системы корректный GET-запрос к эндпоинту {ME_URL} "
        "должен вернуть ответ со статусом 401."
    )


def test_get_me_unregister(test_client: TestClient):
    test_client.post(LOGOUT_URL)
    response = test_client.get(ME_URL)
    assert response.status_code == 401, (
        "Проверьте статус ответа API: при получении данных пользователя "
        "незарегестированного пользователя корректный GET-запрос к "
        f"эндпоинту {ME_URL} должен вернуть ответ со статусом 401."
    )


@pytest.mark.parametrize(
    "user_data, change_user_data, status_code",
    (
        (valid_user_data_1, valid_user_data_4, 201),
        (valid_user_data_2, valid_user_data_5, 201),
        (valid_user_data_3, valid_user_data_6, 201),
        (valid_user_data_1, invalid_user_data_1, 422),
        (valid_user_data_2, invalid_user_data_2, 422),
        (valid_user_data_3, invalid_user_data_3, 422),
        (valid_user_data_3, invalid_user_data_4, 422),
        (valid_user_data_3, invalid_user_data_5, 422),
        (valid_user_data_3, invalid_user_data_6, 422),
    )
)
def test_change_me(
    test_client: TestClient,
    user_data: dict[str: Any],
    change_user_data: dict[str: Any],
    status_code: int
):
    register_and_login_client(test_client, user_data)

    change_user_data = change_user_data.copy()
    user_data = user_data.copy()

    user_data.pop("password")
    change_user_data.pop("password")
    response = test_client.patch(ME_URL, json=change_user_data)

    assert response.status_code == status_code, (
        "Проверьте статус ответа API: при получении данных пользователя "
        f"корректный GET-запрос к эндпоинту {ME_URL} "
        f"должен вернуть ответ со статусом {status_code}."
    )
    response = test_client.get(ME_URL)
    data: dict[str, Any] = response.json()
    data.pop("id")

    missing_keys = change_user_data.keys() - data.keys()
    assert not missing_keys, (
        f"В ответе на корректный PATCH-запрос к эндпоинту `{ME_URL}` не "
        f'хватает следующих ключей: `{"`, `".join(missing_keys)}`'
    )
    data.pop("is_admin")
    data.pop("is_superuser")

    if status_code == 201:
        assert data == change_user_data, (
            "При корректном изменении данных пользователя тело ответа"
            " API должно быть равным измененным данным."
        )
    else:
        assert data == user_data, (
            "При некорректном изменении данных пользователя тело ответа"
            " API должно быть равным первоначальным данным."
        )


@pytest.mark.parametrize(
    "user_data",
    (
        valid_user_data_7,
        valid_user_data_8,
        valid_user_data_9,
    )
)
def test_change_password(
    test_client: TestClient,
    user_data: dict[str: Any],
):
    register_and_login_client(test_client, user_data)

    new_password = "new" + user_data.get("password")
    change_data = {
        "old_password": user_data.get("password"),
        "new_password": new_password,
    }
    user_data["password"] = new_password
    response = test_client.patch(CHANGE_PASS_URL, json=change_data)

    assert response.status_code == 201, (
        "Проверьте статус ответа API: при получении данных пользователя "
        f"корректный GET-запрос к эндпоинту {ME_URL} "
        f"должен вернуть ответ со статусом 201."
    )

    user_data = {
        "email": user_data.get("email"),
        "password": new_password
    }
    response = test_client.post(LOGIN_URL, json=user_data)

    assert response.status_code == 201, (
        "Проверьте статус ответа API: при логировании пользователя "
        f"по новому паролю корректный POST-запрос к эндпоинту {REGISTER_URL} "
        "должен вернуть ответ со статусом 201."
    )


@pytest.mark.parametrize(
    "user_data",
    (
        valid_user_data_7,
        valid_user_data_8,
        valid_user_data_9,
    )
)
def test_delete_me(
    test_client: TestClient,
    user_data: dict[str: Any],
):
    register_and_login_client(test_client, user_data)
    delete_data = {
        "email": user_data.get("email"),
        "password": user_data.get("password")
    }
    response = test_client.delete(ME_URL)

    assert response.status_code == 204, (
        "Проверьте статус ответа API: при получении данных пользователя "
        f"корректный DELETE-запрос к эндпоинту {ME_URL} "
        f"должен вернуть ответ со статусом 204."
    )
    response = test_client.post(LOGIN_URL, json=delete_data)
    assert response.status_code == 401, (
        "Проверьте статус ответа API: при получении данных пользователя "
        f"который удалил себя корректный POST-запрос к эндпоинту {LOGIN_URL} "
        "должен вернуть ответ со статусом 401."
    )


@pytest.mark.parametrize(
    "user_data",
    (
        valid_user_data_7,
        valid_user_data_8,
        valid_user_data_9,
    )
)
def test_login_unregister_user(
    test_client: TestClient,
    user_data: dict[str: Any]
):
    user_data = {
        "email": user_data.get("email"),
        "password": user_data.get("password")
    }
    response = test_client.post(LOGIN_URL, json=user_data)
    assert response.status_code == 401, (
        "Проверьте статус ответа API: при логировании пользователя "
        f"корректный POST-запрос к эндпоинту {LOGIN_URL} "
        "должен вернуть ответ со статусом 401."
    )


@pytest.mark.asyncio
async def test_get_all_users(test_client: TestClient, superuser_db):
    users_data = (
        valid_user_data_1,
        valid_user_data_2,
        valid_user_data_3,
        valid_user_data_4,
        valid_user_data_5,
        valid_user_data_6,
        valid_user_data_7,
        valid_user_data_8,
        valid_user_data_9,
    )
    for data in users_data:
        register_and_login_client(test_client, data)

    login_client(
        client=test_client,
        email=superuser_db.email,
        password=superuser_db.password
    )
    response = test_client.get(USERS_URL)
    assert response.status_code == 200, (
        "Проверьте статус ответа API: при получении всех пользователей "
        f"админом на корректный GET-запрос к эндпоинту {USERS_URL} должен"
        " вернуть всех пользователей."
    )
    data = response.json()

    assert len(data) == len(users_data), (
        "Количество пользователей не соответствует количеству созданных "
        f"пользователей {len(data)} != {len(users_data)}."
    )
    keys = {
        "id",
        "phone_number",
        "first_name",
        "last_name",
        "email",
        "is_admin",
        "is_superuser",
    }
    for user_data in data:
        missing_keys = keys - user_data.keys()
        assert not missing_keys, (
            f"В ответе на корректный POST-запрос к эндпоинту `{REGISTER_URL}` не "
            f'хватает следующих ключей: `{"`, `".join(missing_keys)}`'
        )


@pytest.mark.asyncio
async def test_get_all_users_not_admin_user(
    test_client: TestClient,
    user_db
):
    login_client(
        client=test_client,
        email=user_db.email,
        password=user_db.password
    )
    response = test_client.get(USERS_URL)
    assert response.status_code == 403, (
        "Проверьте статус ответа API: при получении всех пользователей "
        "обычного пользователя на корректный GET-запрос к эндпоинту "
        f"{USERS_URL} должен вернуть 403 код."
    )


@pytest.mark.asyncio
async def test_get_one_user(test_client: TestClient, superuser_db):
    users_data = (
        valid_user_data_1,
        valid_user_data_2,
        valid_user_data_3,
        valid_user_data_4,
        valid_user_data_5,
        valid_user_data_6,
        valid_user_data_7,
        valid_user_data_8,
        valid_user_data_9,
    )
    for data in users_data:
        register_and_login_client(test_client, data)

    login_client(
        client=test_client,
        email=superuser_db.email,
        password=superuser_db.password
    )
    response = test_client.get(USERS_URL)
    data = response.json()[0]
    id_ = data.get("id")

    url = USERS_URL + f"{id_}/"
    response = test_client.get(url)

    assert response.status_code == 200, (
        "Проверьте статус ответа API: при получении одного пользователя "
        f"админом на корректный GET-запрос к эндпоинту {USERS_URL} должен"
        " вернуть 200 код."
    )
    keys = {
        "id",
        "phone_number",
        "first_name",
        "last_name",
        "email",
        "is_admin",
        "is_superuser",
    }
    missing_keys = keys - data.keys()
    assert not missing_keys, (
        f"В ответе на корректный POST-запрос к эндпоинту `{REGISTER_URL}` не "
        f'хватает следующих ключей: `{"`, `".join(missing_keys)}`'
    )


@pytest.mark.asyncio
async def test_get_one_user_invalid_id(
    test_client: TestClient,
    superuser_db
):
    login_client(
        client=test_client,
        email=superuser_db.email,
        password=superuser_db.password
    )
    invalid_id = 912391203
    url = USERS_URL + f"{invalid_id}/"
    response = test_client.get(url)

    assert response.status_code == 400, (
        "Проверьте статус ответа API: при получении одного пользователя "
        "по несуществующему id админом на корректный GET-запрос к "
        f"эндпоинту {url} должен вернуть 400 код."
    )


@pytest.mark.asyncio
async def test_get_one_user_not_admin_user(
    test_client: TestClient,
    user_db
):
    login_client(
        client=test_client,
        email=user_db.email,
        password=user_db.password
    )
    url = USERS_URL + "1/"
    response = test_client.get(USERS_URL)
    assert response.status_code == 403, (
        "Проверьте статус ответа API: при получении одного пользователя "
        "по id не админом на корректный GET-запрос к "
        f"эндпоинту {url} должен вернуть 403 код."
    )


@pytest.mark.asyncio
async def test_update_user(test_client: TestClient, superuser_db, user_db):
    users_data = (
        valid_user_data_1,
        valid_user_data_2,
        valid_user_data_3,
        valid_user_data_4,
        valid_user_data_5,
        valid_user_data_6,
        valid_user_data_7,
        valid_user_data_8,
        valid_user_data_9,
    )
    for data in users_data:
        register_and_login_client(test_client, data)

    login_client(
        client=test_client,
        email=superuser_db.email,
        password=superuser_db.password
    )
    response = test_client.get(USERS_URL)
    data = response.json()

    for item in data:
        if (
            user_db.email == item.get("email") or
            item.get("email") == superuser_db.email
        ):
            continue
        id_ = item.get("id")
        change_data = {
            "email": "new" + item.get("email"),
            "first_name": "new" + item.get("first_name"),
            "last_name": "new" + item.get("last_name"),
            "phone_number": item.get("phone_number") + "0"
        }
        url = USERS_URL + f"{id_}/"
        response = test_client.patch(url, json=change_data)
        assert response.status_code == 201, (
            "Проверьте статус ответа API: при изменени пользователя "
            f"админом корректный PATCH-запрос к эндпоинту {url} "
            "должен вернуть ответ со статусом 201."
        )
        data = response.json()
        response = test_client.get(url)
        data_get = response.json()
        assert data == data_get, (
            "После изменения пользователя, и получения этого же пользователя "
            "по id изменненные данные должны быть идентичны "
            f"{data} != {data_get}"
        )


@pytest.mark.asyncio
async def test_update_user_invalid_id(
    test_client: TestClient,
    superuser_db
):
    login_client(
        client=test_client,
        email=superuser_db.email,
        password=superuser_db.password
    )
    change_data = {
        "email": valid_user_data_1.get("email"),
        "first_name": valid_user_data_1.get("first_name"),
        "last_name": valid_user_data_1.get("last_name"),
        "phone_number": valid_user_data_1.get("phone_number")
    }
    url = USERS_URL + "3452899/"
    response = test_client.patch(url, json=change_data)
    assert response.status_code == 400, (
        "Проверьте статус ответа API: при изменнеи одного пользователя "
        "по несуществующем id админом на корректный patch-запрос к "
        f"эндпоинту {url} должен вернуть 400 код."
    )


@pytest.mark.asyncio
async def test_update_user_not_admin_user(
    test_client: TestClient,
    user_db
):
    login_client(
        client=test_client,
        email=user_db.email,
        password=user_db.password
    )
    change_data = {
        "email": valid_user_data_1.get("email"),
        "first_name": valid_user_data_1.get("first_name"),
        "last_name": valid_user_data_1.get("last_name"),
        "phone_number": valid_user_data_1.get("phone_number")
    }
    url = USERS_URL + "1/"
    response = test_client.patch(url, json=change_data)
    assert response.status_code == 403, (
        "Проверьте статус ответа API: при изменнеи одного пользователя "
        "по id не админом на корректный POST-запрос к "
        f"эндпоинту {url} должен вернуть 403 код."
    )


@pytest.mark.asyncio
async def test_delete_user(
    test_client: TestClient,
    superuser_db,
    user_db
):
    users_data = (
        valid_user_data_1,
        valid_user_data_2,
        valid_user_data_3,
        valid_user_data_4,
        valid_user_data_5,
        valid_user_data_6,
        valid_user_data_7,
        valid_user_data_8,
        valid_user_data_9,
    )
    for data in users_data:
        register_and_login_client(test_client, data)

    login_client(
        client=test_client,
        email=superuser_db.email,
        password=superuser_db.password
    )
    response = test_client.get(USERS_URL)
    data = response.json()

    for item in data:
        if (
            item.get("email") == superuser_db.email or
            user_db.email == item.get("email")
        ):
            continue
        id_ = item.get("id")

        url = USERS_URL + f"{id_}/"
        response = test_client.delete(url)
        assert response.status_code == 204, (
            "Проверьте статус ответа API: при изменени пользователя "
            f"админом корректный DELETE-запрос к эндпоинту {url} "
            "должен вернуть ответ со статусом 204."
        )
        response = test_client.get(url)
        assert response.status_code == 400, (
            "После удаления пользователя, и получения этого же пользователя "
            "по id, должен быть выдан код 400."
        )


@pytest.mark.asyncio
async def test_delete_user_invalid_id(
    test_client: TestClient,
    superuser_db
):
    login_client(
        client=test_client,
        email=superuser_db.email,
        password=superuser_db.password
    )
    url = USERS_URL + "3452899/"
    response = test_client.delete(url)
    assert response.status_code == 400, (
        "Проверьте статус ответа API: при изменнеи одного пользователя "
        "по несуществующем id админом на корректный delete-запрос к "
        f"эндпоинту {url} должен вернуть 400 код."
    )


@pytest.mark.asyncio
async def test_delete_user_not_admin_user(
    test_client: TestClient,
    user_db
):
    login_client(
        client=test_client,
        email=user_db.email,
        password=user_db.password
    )
    url = USERS_URL + "1/"
    response = test_client.delete(url)
    assert response.status_code == 403, (
        "Проверьте статус ответа API: при изменнеи одного пользователя "
        "по id не админом на корректный POST-запрос к "
        f"эндпоинту {url} должен вернуть 403 код."
    )

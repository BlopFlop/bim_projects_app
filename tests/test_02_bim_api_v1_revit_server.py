from typing import Any

import pytest
from fastapi import Response
from fastapi.testclient import TestClient

from tests.fixtures.revit_server import (
    correct_revit_server_1,
    correct_revit_server_2,
    incorrect_data_rs_1,
    incorrect_data_rs_2,
    incorrect_data_rs_3,
    incorrect_data_rs_4,
    incorrect_data_rs_5,
)
from tests.test_01_users_api import login_client

REVIT_SERVER_URL = "/api/v1/bim/servers/"


@pytest.mark.parametrize(
    "data_rs, status_code",
    (
        (correct_revit_server_1, 201),
        (correct_revit_server_2, 201),
        (incorrect_data_rs_1, 422),
        (incorrect_data_rs_2, 422),
        (incorrect_data_rs_3, 422),
        (incorrect_data_rs_4, 422),
        (incorrect_data_rs_5, 422),
    ),
)
def test_create_rs(
    test_client: TestClient,
    superuser_db,
    data_rs: dict[str, Any],
    status_code: int,
):
    login_client(test_client, superuser_db.email, superuser_db.password)

    response: Response = test_client.post(REVIT_SERVER_URL, json=data_rs)

    assert response.status_code == status_code, (
        f"POST запрос на url {REVIT_SERVER_URL} с json {data_rs} "
        f"должен вернуть status code {status_code}"
    )

    if response.status_code == 201:
        data = response.json()
        data.pop("id")

        missing_keys = data_rs.keys() - data.keys()
        assert not missing_keys, (
            f"В ответе на корректный POST-запрос к эндпоинту "
            f"`{REVIT_SERVER_URL}` не хватает следующих ключей"
            f": `{'`, `'.join(missing_keys)}`"
        )
        assert data == data_rs, (
            "При создании RevitServer тело ответа"
            " API отличается от ожидаемого."
        )


def test_get_all(test_client: TestClient, superuser_db):
    login_client(test_client, superuser_db.email, superuser_db.password)

    response: Response = test_client.get(REVIT_SERVER_URL)

    assert (
        response.status_code == 200
    ), f"GET запрос на url {REVIT_SERVER_URL} должен вернуть 200 status code."

    data = response.json()

    assert (
        len(data) == 2
    ), f"json ответа должен возвращать 2 объекта, а не {len(data)}"

    for rs_data in data:
        rs_data.pop("id")

        missing_keys = rs_data.keys() - correct_revit_server_1.keys()
        assert not missing_keys, (
            f"В ответе на корректный POST-запрос к эндпоинту "
            f"`{REVIT_SERVER_URL}` не хватает следующих ключей"
            f": `{'`, `'.join(missing_keys)}`"
        )


def test_get_for_id(test_client: TestClient, superuser_db):
    login_client(test_client, superuser_db.email, superuser_db.password)

    response: Response = test_client.get(REVIT_SERVER_URL)

    all_rs_data = response.json()

    for rs_data in all_rs_data:
        id_ = rs_data.pop("id")
        url = f"{REVIT_SERVER_URL}{id_}/"
        response: Response = test_client.get(url)

        assert response.status_code == 200, (
            f"GET запрос на url {url} " f"должен вернуть 200 status code."
        )

        missing_keys = rs_data.keys() - correct_revit_server_1.keys()
        assert not missing_keys, (
            f"В ответе на корректный get-запрос к эндпоинту "
            f"`{url}` не хватает следующих ключей"
            f": `{'`, `'.join(missing_keys)}`"
        )


@pytest.mark.parametrize("id_", (9999, 1999, 99999))
def test_get_invalid_id(test_client: TestClient, id_: int):
    url = f"{REVIT_SERVER_URL}{id_}/"
    response: Response = test_client.get(url)

    assert response.status_code == 400, (
        f"GET запрос на url {url} на несуществующий id"
        f"должен вернуть 400 status code."
    )


def test_delete_for_id(test_client: TestClient, superuser_db):
    login_client(test_client, superuser_db.email, superuser_db.password)
    response: Response = test_client.get(REVIT_SERVER_URL)

    all_rs_data = response.json()

    for rs_data in all_rs_data:
        id_ = rs_data.pop("id")
        url = f"{REVIT_SERVER_URL}{id_}/"
        response: Response = test_client.delete(url)

        assert response.status_code == 204, (
            f"Delete запрос на url {url} " f"должен вернуть 204 status code."
        )

        response: Response = test_client.delete(url)
        assert response.status_code == 400, (
            f"Повторный DELETE запрос на url {url} "
            f"должен вернуть 400 status code."
        )


@pytest.mark.parametrize("id_", (9999, 1999, 99999))
def test_delete_invalid_id(test_client: TestClient, id_: int, superuser_db):
    login_client(test_client, superuser_db.email, superuser_db.password)
    url = f"{REVIT_SERVER_URL}{id_}/"
    response: Response = test_client.delete(url)

    assert response.status_code == 400, (
        f"Delete запрос на url {url} на несуществующий id"
        f"должен вернуть 400 status code."
    )


def test_get_all_not_admin_user(test_client: TestClient, user_db):
    login_client(test_client, user_db.email, user_db.password)

    response: Response = test_client.get(REVIT_SERVER_URL)
    assert response.status_code == 403, (
        f"GET запрос на url {REVIT_SERVER_URL} не администратором"
        f"должен вернуть 403 status code."
    )


def test_get_for_id_not_admin_user(test_client: TestClient, user_db):
    login_client(test_client, user_db.email, user_db.password)

    url = REVIT_SERVER_URL + "21/"
    response: Response = test_client.get(REVIT_SERVER_URL)
    assert response.status_code == 403, (
        f"GET запрос на url {url} не администратором"
        f" должен вернуть 403 status code."
    )


def test_create_not_admin_user(test_client: TestClient, user_db):
    login_client(test_client, user_db.email, user_db.password)

    response: Response = test_client.post(
        REVIT_SERVER_URL, json=correct_revit_server_2
    )
    assert response.status_code == 403, (
        f"POST запрос на url {REVIT_SERVER_URL} не администратором"
        f" должен вернуть 403 status code."
    )


def test_get_for_id_not_admin_user(test_client: TestClient, user_db):
    login_client(test_client, user_db.email, user_db.password)

    url = REVIT_SERVER_URL + "21/"
    response: Response = test_client.delete(url)
    assert response.status_code == 403, (
        f"DELETE запрос на url {url} не администратором"
        f" должен вернуть 403 status code."
    )

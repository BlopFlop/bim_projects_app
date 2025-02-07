from typing import Any

import pytest
from fastapi import Response
from fastapi.testclient import TestClient

from tests.fixtures.model_section import (
    all_empty,
    architectural_section,
    construction_plan_section,
    ecological_section,
    economic_section,
    empty_description,
    empty_name,
    engineering_section,
    long_description,
    long_name,
    missing_description,
    missing_name,
    null_description,
    null_name,
    structural_section,
)
from tests.test_01_users_api import login_client

SECTIONS_URL = "/api/v1/bim/sections/"


@pytest.mark.parametrize(
    "data_sections, status_code",
    (
        (architectural_section, 201),
        (structural_section, 201),
        (engineering_section, 201),
        (construction_plan_section, 201),
        (economic_section, 201),
        (ecological_section, 201),
        (missing_description, 422),
        (missing_name, 422),
        (empty_name, 422),
        (empty_description, 422),
        (long_description, 422),
        (long_name, 422),
        (null_description, 422),
        (null_name, 422),
        (all_empty, 422),
    ),
)
def test_create_sections(
    test_client: TestClient,
    superuser_db,
    data_sections: dict[str, Any],
    status_code: int,
):
    login_client(test_client, superuser_db.email, superuser_db.password)

    response: Response = test_client.post(SECTIONS_URL, json=data_sections)

    assert response.status_code == status_code, (
        f"POST запрос на url {SECTIONS_URL} с json {data_sections} "
        f"должен вернуть status code {status_code}"
    )

    if response.status_code == 201:
        data = response.json()
        data.pop("id")

        missing_keys = data_sections.keys() - data.keys()
        assert not missing_keys, (
            f"В ответе на корректный POST-запрос к эндпоинту "
            f"`{SECTIONS_URL}` не хватает следующих ключей"
            f": `{'`, `'.join(missing_keys)}`"
        )
        assert data == data_sections, (
            "При создании SECTIONS тело ответа"
            " API отличается от ожидаемого."
        )


def test_get_all(test_client: TestClient, superuser_db):
    login_client(test_client, superuser_db.email, superuser_db.password)

    response: Response = test_client.get(SECTIONS_URL)

    assert (
        response.status_code == 200
    ), f"GET запрос на url {SECTIONS_URL} должен вернуть 200 status code."

    data = response.json()

    assert (
        len(data) == 6
    ), f"json ответа должен возвращать 6 объекта, а не {len(data)}"

    for rs_data in data:
        rs_data.pop("id")

        missing_keys = rs_data.keys() - architectural_section.keys()
        assert not missing_keys, (
            f"В ответе на корректный POST-запрос к эндпоинту "
            f"`{SECTIONS_URL}` не хватает следующих ключей"
            f": `{'`, `'.join(missing_keys)}`"
        )


def test_update_sections(
    test_client: TestClient,
    superuser_db,
):
    login_client(test_client, superuser_db.email, superuser_db.password)

    response: Response = test_client.get(SECTIONS_URL)

    data_sections = response.json()

    for section in data_sections:
        id_ = section.pop("id")
        url = SECTIONS_URL + f"{id_}/"
        update_data = {
            "description": "new" + section.get("description"),
            "name": "new" + section.get("name"),
        }
        response: Response = test_client.patch(url, json=update_data)
        assert response.status_code == 201, (
            f"PATCH запрос на url {url} с json {update_data} "
            f"должен вернуть status code 201."
        )

        data = response.json()
        data.pop("id")

        missing_keys = update_data.keys() - data.keys()
        assert not missing_keys, (
            f"В ответе на корректный POST-запрос к эндпоинту "
            f"`{SECTIONS_URL}` не хватает следующих ключей"
            f": `{'`, `'.join(missing_keys)}`"
        )
        assert data == update_data, (
            "При создании SECTIONS тело ответа"
            " API отличается от ожидаемого."
        )


def test_get_for_id(test_client: TestClient, superuser_db):
    login_client(test_client, superuser_db.email, superuser_db.password)

    response: Response = test_client.get(SECTIONS_URL)

    all_sections_data = response.json()

    for sections_data in all_sections_data:
        id_ = sections_data.pop("id")
        url = f"{SECTIONS_URL}{id_}/"
        response: Response = test_client.get(url)

        assert response.status_code == 200, (
            f"GET запрос на url {url} " f"должен вернуть 200 status code."
        )

        missing_keys = sections_data.keys() - architectural_section.keys()
        assert not missing_keys, (
            f"В ответе на корректный get-запрос к эндпоинту "
            f"`{url}` не хватает следующих ключей"
            f": `{'`, `'.join(missing_keys)}`"
        )


@pytest.mark.parametrize("id_", (9999, 1999, 99999))
def test_get_invalid_id(test_client: TestClient, id_: int):
    url = SECTIONS_URL + f"{id_}/"
    response: Response = test_client.get(url)

    assert response.status_code == 400, (
        f"GET запрос на url {url} на несуществующий id"
        f" должен вернуть 400 status code."
    )


def test_delete_for_id(test_client: TestClient, superuser_db):
    login_client(test_client, superuser_db.email, superuser_db.password)
    response: Response = test_client.get(SECTIONS_URL)

    all_rs_data = response.json()

    for rs_data in all_rs_data:
        id_ = rs_data.pop("id")
        url = f"{SECTIONS_URL}{id_}/"
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
    url = f"{SECTIONS_URL}{id_}/"
    response: Response = test_client.delete(url)

    assert response.status_code == 400, (
        f"Delete запрос на url {url} на несуществующий id "
        f"должен вернуть 400 status code."
    )


def test_get_all_not_admin_user(test_client: TestClient, user_db):
    login_client(test_client, user_db.email, user_db.password)

    response: Response = test_client.get(SECTIONS_URL)
    assert response.status_code == 403, (
        f"GET запрос на url {SECTIONS_URL} не администратором "
        f"должен вернуть 403 status code."
    )


def test_get_for_id_not_admin_user(test_client: TestClient, user_db):
    login_client(test_client, user_db.email, user_db.password)

    url = SECTIONS_URL + "21/"
    response: Response = test_client.get(SECTIONS_URL)
    assert response.status_code == 403, (
        f"GET запрос на url {url} не администратором "
        f" должен вернуть 403 status code."
    )


def test_create_not_admin_user(test_client: TestClient, user_db):
    login_client(test_client, user_db.email, user_db.password)

    response: Response = test_client.post(SECTIONS_URL, json=economic_section)
    assert response.status_code == 403, (
        f"POST запрос на url {SECTIONS_URL} не администратором "
        f" должен вернуть 403 status code."
    )


def test_update_not_admin_user(test_client: TestClient, user_db):
    login_client(test_client, user_db.email, user_db.password)

    url = SECTIONS_URL + "21/"
    response: Response = test_client.patch(url, json=economic_section)
    assert response.status_code == 403, (
        f"POST запрос на url {SECTIONS_URL} не администратором "
        f" должен вернуть 403 status code."
    )


def test_get_for_id_not_admin_user(test_client: TestClient, user_db):
    login_client(test_client, user_db.email, user_db.password)

    url = SECTIONS_URL + "21/"
    response: Response = test_client.delete(url)
    assert response.status_code == 403, (
        f"DELETE запрос на url {url} не администратором "
        f" должен вернуть 403 status code."
    )

from typing import Any

import pytest

from conftest import async_session_maker
from fastapi.testclient import TestClient
from fastapi import Response

from src.project.repository import get_revit_server_repository
from src.project.schemas import RevitServerDB

from fixtures.revit_server import (
    correct_revit_server_1,
    correct_revit_server_2,

    incorrect_data_rs_1,
    incorrect_data_rs_2,
    incorrect_data_rs_3,
    incorrect_data_rs_4,
    incorrect_data_rs_5,
)

REVIT_SERVER_URL = "/api/v1/bim/servers/"

import asyncio # noqa


pytest_plugins = ('pytest_asyncio',)


@pytest.mark.parametrize(
    "data_rs, status_code",
    (
        (correct_revit_server_1, 201),
        (correct_revit_server_2, 201),

        (incorrect_data_rs_1, 422),
        (incorrect_data_rs_2, 400),
        (incorrect_data_rs_3, 422),
        (incorrect_data_rs_4, 422),
        (incorrect_data_rs_5, 422),
    )
)
def test_create_rs(
    test_client: TestClient,
    data_rs: dict[str, Any],
    status_code: int
):
    response: Response = test_client.post(REVIT_SERVER_URL, json=data_rs)

    assert response.status_code == status_code, (
        f"POST запрос на url {REVIT_SERVER_URL} с json {data_rs} "
        f"должен вернуть status code {status_code}"
    )

    if response.status_code == 201:
        data = response.json()
        for key in data_rs:
            assert key in data, f"json ответа не содержат поле {key}"
            assert data_rs[key] == data[key], (
                f"Поле {key} json ответа {data_rs[key]} != {data[key]}"
            )


def test_get_all(test_client: TestClient):
    response: Response = test_client.get(REVIT_SERVER_URL)

    assert response.status_code == 200, (
        f"GET запрос на url {REVIT_SERVER_URL} должен вернуть 200 status code."
    )

    data = response.json()

    assert len(data) == 2, (
        f"json ответа должен возвращать 2 объекта, а не {len(data)}"
    )

    for obj in data:
        for key in correct_revit_server_1:
            assert key in obj, f"json ответа не содержат поле {key}"


@pytest.mark.parametrize(
    "id, status_code",
    (
        (1, 200),
        (2, 200)
        (30, 400)
        (999, 400)
    )
)
def test_get(test_client: TestClient, id: int, status_code: int):
    url = f"{REVIT_SERVER_URL}{id}/"
    response: Response = test_client.get(url)

    assert response.status_code == status_code, (
        f"GET запрос на url {REVIT_SERVER_URL} "
        f"должен вернуть {status_code} status code."
    )

    if response.status_code == 200:
        data = response.json()
        for key in correct_revit_server_1:
            assert key in data, f"json ответа не содержат поле {key}"


@pytest.mark.parametrize(
    "id, status_code",
    (
        (1, 204),
        (2, 204)
        (30, 400)
        (999, 400)
    )
)
def test_delete_rs(test_client: TestClient, id: int, status_code: int):
    url = f"{REVIT_SERVER_URL}{id}/"
    response: Response = test_client.delete(url)

    assert response.status_code == status_code, (
        f"DELETE запрос на url {REVIT_SERVER_URL} "
        f"должен вернуть {status_code} status code."
    )

    response: Response = test_client.delete(url)
    assert response.status_code == 400, (
        f"Повторный DELETE запрос на url {REVIT_SERVER_URL} "
        f"должен вернуть 400 status code."
    )

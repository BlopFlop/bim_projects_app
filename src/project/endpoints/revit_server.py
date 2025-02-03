from fastapi import APIRouter, Depends

from project.models import RevitServer
from project.schemas import (
    RevitServerCreate,
    RevitServerDB
)
from project.repository import (
    RevitServerRepository,
    get_revit_server_repository
)

# from project.validatiors import check_fields_duplicate

router = APIRouter()


@router.get(
    "/",
    response_model=list[RevitServerDB],
    summary="Получить все ревит серверы.",
    description="Получает все ревит серверы из базы данных.",
)
async def get_all_revit_servers(
    revit_server_repository: RevitServerRepository = Depends(
        get_revit_server_repository
    ),
) -> list[RevitServer]:
    return await revit_server_repository.get_multi()


@router.get(
    "/{revit_server_id}",
    response_model=list[RevitServerDB],
    summary="Получить ревит сервер по id.",
    description="Получает ревит сервер по id из базы данных.",
)
async def get_revit_servers(
    revit_server_id: int,
    revit_server_repository: RevitServerRepository = Depends(
        get_revit_server_repository
    ),
) -> list[RevitServer]:
    return await revit_server_repository.get(obj_id=revit_server_id)


@router.post(
    "/",
    response_model=RevitServerDB,
    summary="Создает ревит сервер.",
)
async def create_revit_server(
    revit_server: RevitServerCreate,
    revit_server_repository: RevitServerRepository = Depends(
        get_revit_server_repository
    ),
) -> RevitServerDB:
    new_revit_server = await revit_server_repository.create(
        obj_in=revit_server
    )
    return new_revit_server


@router.delete(
    "/{revit_server_id}",
    response_model=RevitServerDB,
    summary="Удалить ревит сервер.",
)
async def delete_revit_server(
    revit_server_id: int,
    bim_model_repository: RevitServerRepository = Depends(
        get_revit_server_repository
    ),
) -> RevitServer:
    revit_server = await bim_model_repository.get(obj_id=revit_server_id)
    return await bim_model_repository.remove(db_obj=revit_server)

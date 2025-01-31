from fastapi import APIRouter, Depends

from project.models import RevitServer
from project.schemas import (
    RevitServerCreate,
    RevitServerDB
)
from project.repository import (
    ModelSectionRepository,
    get_model_section_repository
)

# from project.validatiors import check_fields_duplicate

router = APIRouter()


@router.get(
    "/",
    response_model=list[RevitServerDB],
    summary="Получить все ревит серверы.",
    description="Получает все ревит серверы из базы данных.",
)
async def get_all_bim_models(
    bim_model_repository: ModelSectionRepository = Depends(
        get_model_section_repository
    ),
) -> list[RevitServer]:
    return await bim_model_repository.get_multi()


@router.post(
    "/",
    response_model=RevitServerDB,
    summary="Создает ревит сервер.",
)
async def create_bim_model(
    bim_model: RevitServerCreate,
    bim_model_repository: ModelSectionRepository = Depends(
        get_model_section_repository
    ),
) -> RevitServerDB:
    new_project = await bim_model_repository.create(obj_in=bim_model)
    return new_project


@router.delete(
    "/{bim_model_id}",
    response_model=RevitServerDB,
    summary="Удалить ревит сервер.",
)
async def delete_bim_model(
    bim_model_id: int,
    bim_model_repository: ModelSectionRepository = Depends(
        get_model_section_repository
    ),
) -> RevitServer:
    bim_model = await bim_model_repository.get(obj_id=bim_model_id)
    return await bim_model_repository.remove(db_obj=bim_model)

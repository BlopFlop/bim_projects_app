from fastapi import APIRouter, Depends

from project.models import BIMModel
from project.schemas import (
    BIMModelSchemaCreate,
    BIMModelSchemaUpdate,
    BIMModelSchemaDB
)
from project.repository import (
    BIMModelRepository,
    get_bim_model_repository
)

# from project.validatiors import check_fields_duplicate

router = APIRouter()


@router.get(
    "/",
    response_model=list[BIMModelSchemaDB],
    summary="Получить все BIM модели",
    description="Получает BIM модели из базы данных.",
)
async def get_all_bim_models(
    bim_model_repository: BIMModelRepository = Depends(
        get_bim_model_repository
    ),
) -> list[BIMModel]:
    return await bim_model_repository.get_multi()


@router.post(
    "/",
    response_model=BIMModelSchemaDB,
    summary="Создать BIM модель.",
)
async def create_bim_model(
    bim_model: BIMModelSchemaCreate,
    bim_model_repository: BIMModelRepository = Depends(
        get_bim_model_repository
    ),
) -> BIMModelSchemaDB:
    new_project = await bim_model_repository.create(obj_in=bim_model)
    return new_project


@router.delete(
    "/{bim_model_id}",
    response_model=BIMModelSchemaDB,
    summary="Удалить BIM модель.",
)
async def delete_bim_model(
    bim_model_id: int,
    bim_model_repository: BIMModelRepository = Depends(
        get_bim_model_repository
    ),
) -> BIMModel:
    bim_model = await bim_model_repository.get(obj_id=bim_model_id)
    return await bim_model_repository.remove(db_obj=bim_model)


@router.patch(
    "/{bim_model_id}",
    response_model=BIMModelSchemaDB,
    summary="Изменить BIM модель.",
)
async def change_bim_model(
    bim_model_id: int,
    obj_in: BIMModelSchemaUpdate,
    bim_model_repository: BIMModelRepository = Depends(
        get_bim_model_repository
    ),
) -> BIMModel:
    bim_model = await bim_model_repository.get(obj_id=bim_model_id)
    return await bim_model_repository.update(bim_model, obj_in)

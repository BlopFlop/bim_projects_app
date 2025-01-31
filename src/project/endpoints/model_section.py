from fastapi import APIRouter, Depends

from project.models import ModelSection
from project.schemas import (
    ModelSectionCreate,
    ModelSectionUpdate,
    ModelSectionDB
)
from project.repository import (
    ModelSectionRepository,
    get_model_section_repository
)

# from project.validatiors import check_fields_duplicate

router = APIRouter()


@router.get(
    "/",
    response_model=list[ModelSectionDB],
    summary="Получить все разделы проектирования",
    description="Получает разделы проектирования из базы данных.",
)
async def get_all_bim_models(
    bim_model_repository: ModelSectionRepository = Depends(
        get_model_section_repository
    ),
) -> list[ModelSection]:
    return await bim_model_repository.get_multi()


@router.post(
    "/",
    response_model=ModelSectionDB,
    summary="Создает раздел проектирования.",
)
async def create_bim_model(
    bim_model: ModelSectionCreate,
    bim_model_repository: ModelSectionRepository = Depends(
        get_model_section_repository
    ),
) -> ModelSectionDB:
    new_project = await bim_model_repository.create(obj_in=bim_model)
    return new_project


@router.delete(
    "/{bim_model_id}",
    response_model=ModelSectionDB,
    summary="Удалить раздел проектирования.",
)
async def delete_bim_model(
    bim_model_id: int,
    bim_model_repository: ModelSectionRepository = Depends(
        get_model_section_repository
    ),
) -> ModelSection:
    bim_model = await bim_model_repository.get(obj_id=bim_model_id)
    return await bim_model_repository.remove(db_obj=bim_model)


@router.patch(
    "/{bim_model_id}",
    response_model=ModelSectionDB,
    summary="Изменить раздел проектирования.",
)
async def change_bim_model(
    bim_model_id: int,
    obj_in: ModelSectionUpdate,
    bim_model_repository: ModelSectionRepository = Depends(
        get_model_section_repository
    ),
) -> ModelSection:
    bim_model = await bim_model_repository.get(obj_id=bim_model_id)
    return await bim_model_repository.update(bim_model, obj_in)

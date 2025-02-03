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
async def get_all_model_sections(
    model_section_repository: ModelSectionRepository = Depends(
        get_model_section_repository
    ),
) -> list[ModelSection]:
    return await model_section_repository.get_multi()


@router.get(
    "/{model_section_id}",
    response_model=ModelSectionDB,
    summary="Получить раздел проектирования по id",
    description="Получает раздел проектирования по id из базы данных.",
)
async def get_model_section(
    model_section_id: int,
    model_section_repository: ModelSectionRepository = Depends(
        get_model_section_repository
    ),
) -> list[ModelSection]:
    return await model_section_repository.get(obj_id=model_section_id)


@router.post(
    "/",
    response_model=ModelSectionDB,
    summary="Создает раздел проектирования.",
)
async def create_model_section(
    model_section: ModelSectionCreate,
    model_section_repository: ModelSectionRepository = Depends(
        get_model_section_repository
    ),
) -> ModelSectionDB:
    new_project = await model_section_repository.create(obj_in=model_section)
    return new_project


@router.delete(
    "/{model_section_id}",
    response_model=ModelSectionDB,
    summary="Удалить раздел проектирования.",
)
async def delete_model_section(
    model_section_id: int,
    model_section_repository: ModelSectionRepository = Depends(
        get_model_section_repository
    ),
) -> ModelSection:
    model_section = await model_section_repository.get(obj_id=model_section_id)
    return await model_section_repository.remove(db_obj=model_section)


@router.patch(
    "/{model_section_id}",
    response_model=ModelSectionDB,
    summary="Изменить раздел проектирования.",
)
async def change_model_section(
    model_section_id: int,
    obj_in: ModelSectionUpdate,
    model_section_repository: ModelSectionRepository = Depends(
        get_model_section_repository
    ),
) -> ModelSection:
    model_section = await model_section_repository.get(obj_id=model_section_id)
    return await model_section_repository.update(model_section, obj_in)

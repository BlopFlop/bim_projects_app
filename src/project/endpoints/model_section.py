from fastapi import APIRouter, Depends

from project.models import ModelSection
from project.repository import ModelSectionRepository, get_section_repo
from project.schemas import (
    ModelSectionCreate,
    ModelSectionDB,
    ModelSectionUpdate,
)
from project.validatiors import validate_object_for_id
from users import get_current_admin_user
from users.models import User

router = APIRouter()


@router.get(
    "/",
    response_model=list[ModelSectionDB],
    summary="Получить все разделы проектирования",
    description="Получает разделы проектирования из базы данных.",
)
async def get_all_model_sections(
    user: User = Depends(get_current_admin_user),
    section_repo: ModelSectionRepository = Depends(get_section_repo),
) -> list[ModelSection]:
    return await section_repo.get_multi()


@router.get(
    "/{model_section_id}",
    response_model=ModelSectionDB,
    summary="Получить раздел проектирования по id",
    description="Получает раздел проектирования по id из базы данных.",
)
async def get_model_section(
    model_section_id: int,
    user: User = Depends(get_current_admin_user),
    section_repo: ModelSectionRepository = Depends(get_section_repo),
):
    await validate_object_for_id(model_section_id, section_repo)
    return await section_repo.get(obj_id=model_section_id)


@router.post(
    "/",
    response_model=ModelSectionDB,
    summary="Создает раздел проектирования.",
    status_code=201,
)
async def create_model_section(
    model_section: ModelSectionCreate,
    user: User = Depends(get_current_admin_user),
    section_repo: ModelSectionRepository = Depends(get_section_repo),
):
    new_project = await section_repo.create(obj_in=model_section)
    return new_project


@router.delete(
    "/{model_section_id}",
    summary="Удалить раздел проектирования.",
    status_code=204,
)
async def delete_model_section(
    model_section_id: int,
    user: User = Depends(get_current_admin_user),
    section_repo: ModelSectionRepository = Depends(get_section_repo),
):
    await validate_object_for_id(model_section_id, section_repo)
    model_section = await section_repo.get(obj_id=model_section_id)
    await section_repo.remove(db_obj=model_section)
    return


@router.patch(
    "/{model_section_id}",
    response_model=ModelSectionDB,
    summary="Изменить раздел проектирования.",
    status_code=201,
)
async def change_model_section(
    model_section_id: int,
    obj_in: ModelSectionUpdate,
    user: User = Depends(get_current_admin_user),
    section_repo: ModelSectionRepository = Depends(get_section_repo),
) -> ModelSection:
    await validate_object_for_id(model_section_id, section_repo)
    model_section = await section_repo.get(obj_id=model_section_id)
    return await section_repo.update(model_section, obj_in)

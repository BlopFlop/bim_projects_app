from fastapi import APIRouter, Depends

from project.models import Project
from project.schemas import (
    ProjectSchemaCreate,
    ProjectSchemaUpdate,
    ProjectSchemaDB
)
from project.repository import (
    ProjectRepository,
    get_project_repository
)

# from project.validatiors import check_fields_duplicate

router = APIRouter()


@router.get(
    "/",
    response_model=list[ProjectSchemaDB],
    summary="Получить все BIM проекты",
    description="Получает BIM проекты из базы данных.",
)
async def get_all_projects(
    project_repositiory: ProjectRepository = Depends(get_project_repository),
) -> list[Project]:
    return await project_repositiory.get_multi()


@router.post(
    "/",
    response_model=ProjectSchemaDB,
    summary="Создать проект.",
    description="Создает проект.",
)
async def create_project(
    charity_project: ProjectSchemaCreate,
    project_repository: ProjectRepository = Depends(get_project_repository),
) -> Project:
    new_project = await project_repository.create(obj_in=charity_project)
    return new_project


@router.delete(
    "/{project_id}",
    response_model=ProjectSchemaDB,
    summary="Удалить проект.",
    description="Удаляет проект.",
)
async def delete_project(
    project_id: int,
    project_repository: ProjectRepository = Depends(get_project_repository),
) -> Project:
    project = await project_repository.get(obj_id=project_id)
    return await project_repository.remove(db_obj=project)


@router.patch(
    "/{project_id}",
    response_model=ProjectSchemaDB,
    summary="Изменить проект.",
)
async def change_charity_project(
    project_id: int,
    obj_in: ProjectSchemaUpdate,
    project_repository: ProjectRepository = Depends(get_project_repository),
) -> Project:
    project = await project_repository.get(obj_id=project_id)
    return await project_repository.update(project, obj_in)

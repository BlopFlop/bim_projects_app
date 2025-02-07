from fastapi import APIRouter, Depends

from project.models import Project
from project.repository import ProjectRepository, get_project_repository
from project.schemas import (
    ProjectSchemaCreate,
    ProjectSchemaDB,
    ProjectSchemaUpdate,
)
from project.validatiors import check_fields_duplicate

router = APIRouter()


@router.get(
    "/",
    response_model=list[ProjectSchemaDB],
    summary="Получить все проекты.",
    description="Получает проекты из базы данных.",
)
async def get_all_projects(
    project_repositiory: ProjectRepository = Depends(get_project_repository),
) -> list[Project]:
    return await project_repositiory.get_multi()


@router.get(
    "/{project_id}",
    response_model=ProjectSchemaDB,
    summary="Получить проект по id.",
    description="Получает проект по id из базы данных.",
)
async def get_all_projects(
    project_id: int,
    project_repositiory: ProjectRepository = Depends(get_project_repository),
) -> list[Project]:
    return await project_repositiory.get(obj_id=project_id)


@router.post(
    "/",
    response_model=ProjectSchemaDB,
    summary="Создать проект.",
    description="Создает проект.",
    status_code=201,
)
async def create_project(
    project: ProjectSchemaCreate,
    project_repository: ProjectRepository = Depends(get_project_repository),
):
    await check_fields_duplicate(
        schema=project,
        fields_set=Project.get_unique_fields(),
        repository=project_repository,
    )
    new_project = await project_repository.create(obj_in=project)
    return new_project


@router.delete(
    "/{project_id}",
    summary="Удалить проект.",
    description="Удаляет проект.",
    status_code=204,
)
async def delete_project(
    project_id: int,
    project_repository: ProjectRepository = Depends(get_project_repository),
):
    project = await project_repository.get(obj_id=project_id)
    await project_repository.remove(db_obj=project)
    # return Message()


@router.patch(
    "/{project_id}",
    response_model=ProjectSchemaDB,
    summary="Изменить проект.",
)
async def change_charity_project(
    project_id: int,
    obj_in: ProjectSchemaUpdate,
    project_repository: ProjectRepository = Depends(get_project_repository),
):
    await check_fields_duplicate(
        schema=obj_in,
        fields_set=Project.get_unique_fields(),
        repository=project_repository,
    )
    project = await project_repository.get(obj_id=project_id)
    return await project_repository.update(project, obj_in)

from fastapi import APIRouter, Depends

from project.models import RevitServer
from project.repository import RevitServerRepository, get_rs_repository
from project.schemas import RevitServerCreate, RevitServerDB
from project.validatiors import validate_object_for_id
from schemas import MessageSchema
from users import get_current_admin_user
from users.models import User

router = APIRouter()


@router.get(
    "/",
    response_model=list[RevitServerDB],
    summary="Получить все ревит серверы.",
    description="Получает все ревит серверы из базы данных.",
)
async def get_all_revit_servers(
    admin_user: User = Depends(get_current_admin_user),
    rs_repo: RevitServerRepository = Depends(get_rs_repository),
) -> list[RevitServer]:
    return await rs_repo.get_multi()


@router.get(
    "/{revit_server_id}/",
    response_model=RevitServerDB,
    summary="Получить ревит сервер по id.",
    description="Получает ревит сервер по id из базы данных.",
)
async def get_revit_server(
    revit_server_id: int,
    admin_user: User = Depends(get_current_admin_user),
    rs_repo: RevitServerRepository = Depends(get_rs_repository),
):
    return await validate_object_for_id(revit_server_id, rs_repo)


@router.post(
    "/",
    response_model=RevitServerDB,
    summary="Создает ревит сервер.",
    status_code=201,
)
async def create_revit_server(
    revit_server: RevitServerCreate,
    admin_user: User = Depends(get_current_admin_user),
    rs_repo: RevitServerRepository = Depends(get_rs_repository),
):
    new_revit_server = await rs_repo.create(obj_in=revit_server)
    return new_revit_server


@router.delete(
    "/{revit_server_id}/", summary="Удалить ревит сервер.", status_code=204
)
async def delete_revit_server(
    revit_server_id: int,
    admin_user: User = Depends(get_current_admin_user),
    rs_repo: RevitServerRepository = Depends(get_rs_repository),
):
    revit_server = await validate_object_for_id(revit_server_id, rs_repo)
    await rs_repo.remove(db_obj=revit_server)
    return MessageSchema(
        message=f"RevitServer по id {revit_server_id} удален."
    )

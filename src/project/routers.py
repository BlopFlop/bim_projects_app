from fastapi import APIRouter

from project.endpoints import (
    project_router,
    bim_model_router,
    revit_server_router,
    model_section_router
)

router = APIRouter()
router.include_router(
    project_router,
    prefix="/projects",
    tags=["Project"]
)
router.include_router(
    bim_model_router,
    prefix="/models",
    tags=["Bim model"]
)
router.include_router(
    revit_server_router,
    prefix="/servers",
    tags=["Revit server"]
)
router.include_router(
    model_section_router,
    prefix="/sectons",
    tags=["Sections"]
)
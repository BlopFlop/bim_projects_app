from fastapi import APIRouter

from project.api import router as bim_router


main_api_v1_router = APIRouter()
main_api_v1_router.include_router(
    bim_router, prefix="/bim", tags=("BIM",)
)

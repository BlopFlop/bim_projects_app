from fastapi import APIRouter

from project.routers import router as bim_router
from users.routers import router as user_router


main_api_v1_router = APIRouter()
main_api_v1_router.include_router(
    bim_router, prefix="/bim", tags=("BIM",)
)
main_api_v1_router.include_router(
    user_router, prefix="/auth", tags=("Auth",)
)

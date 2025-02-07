from fastapi import APIRouter

from users.endpoints import auth_router, me_router, users_router

router = APIRouter()
router.include_router(
    auth_router,
    prefix="/auth",
)
router.include_router(
    me_router,
    prefix="/users/me",
)
router.include_router(users_router, prefix="/users")

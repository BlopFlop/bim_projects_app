from fastapi import APIRouter, HTTPException, status, Depends

from users.repository import UserRepository, get_user_repository
from users.schemas import UserRegister
from users.validatiors import check_email_duplicate, check_number_duplicate


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post(
    "/register/",
    summary="Регистрация пользователя.",
    description="Регистрирует вас как нового пользователя."
)
async def register_user(
    user: UserRegister,
    user_repository: UserRepository = Depends(get_user_repository)
) -> dict:
    await check_email_duplicate(
        email=user.email,
        repository=user_repository
    )
    await check_number_duplicate(
        phone_number=user.phone_number,
        repository=user_repository
    )
    await user_repository.create(user)
    return {'message': 'Вы успешно зарегистрированы!'}
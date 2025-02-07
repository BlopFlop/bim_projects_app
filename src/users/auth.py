from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import application_config
from constants import ALGORITHM_KEY, SECRET_KEY, USER_ACCESS_TOKEN_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Make hashed password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare between str pass and hashed pass."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Create jwt token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = application_config.get_auth_data
    encode_jwt = jwt.encode(
        to_encode, auth_data[SECRET_KEY], algorithm=auth_data[ALGORITHM_KEY]
    )
    return encode_jwt


def get_token(request: Request) -> str:
    """Get jwt token from cookies."""
    token = request.cookies.get(USER_ACCESS_TOKEN_KEY)
    if token:
        return token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
    )


async def get_user_id_for_token(
    token: str = Depends(get_token),
) -> int:
    """Get user from database and jwt token from cookies."""
    try:
        auth_data = application_config.get_auth_data
        payload = jwt.decode(
            token, auth_data[SECRET_KEY], algorithms=[auth_data[ALGORITHM_KEY]]
        )
    except JWTError:
        ext_msg = "Токен не валидный!"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=ext_msg
        )

    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        ext_msg = "Токен истек"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=ext_msg
        )

    user_id = payload.get("sub")
    if not user_id:
        ext_msg = "Не найден ID пользователя"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=ext_msg
        )

    return int(user_id)

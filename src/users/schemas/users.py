import re
from typing import Optional

from fastapi.exceptions import HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator


class JwtTokenSchema(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]


class UserRegisterSchema(BaseModel):
    email: EmailStr = Field(
        min_length=6,
        max_length=256,
        title="Email",
        description=(
            "Номер пользователя, уникальное строковое поле;"
            " Допустимая длина строки - от 7 до 18 символов включительно;"
        ),
    )
    password: str = Field(
        min_length=5,
        max_length=50,
        title="Password",
        description="Пароль, поле длинной от 5 до 50 символов влючительно.",
    )
    phone_number: str = Field(
        min_length=7,
        max_length=18,
        title="Phone number",
        description=(
            "Номер телефона в международном формате, начинающийся с '+'"
            " уникальное строковое поле; допустимая длина"
            " строки - от 7 до 18 символов включительно;"
        ),
    )
    first_name: str = Field(
        min_length=3,
        max_length=256,
        description=(
            "Имя пользователя, строковое поле; "
            "Допустимая длина строки - от 3 до 256 символов включительно;"
        ),
    )
    last_name: str = Field(
        min_length=3,
        max_length=256,
        description=(
            "Фамилия пользователя, строковое поле; "
            "Допустимая длина строки - от 3 до 256 символов включительно;"
        ),
    )

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str | HTTPException:
        if not re.match(r"^\+\d{5,16}$", value):
            ext_msg = (
                "Номер телефона должен начинаться с"
                " '+' и содержать от 5 до 16 цифр"
            )
            raise HTTPException(422, ext_msg)
        return value

    class Config:
        """Config class for this model."""

        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "super_password",
                "phone_number": "+874493831",
                "first_name": "Алексей",
                "last_name": "Яковенко",
            }
        }


class UserRegisterAdminSchema(UserRegisterSchema):

    is_admin: bool = Field(
        True,
        comment="Булево значение, определяющее пользователя администратора.",
    )


class UserRegisterSuperuserSchema(UserRegisterAdminSchema):

    is_superuser: bool = Field(
        True, comment="Булево значение, определяющее пользователя суперюзера."
    )


class UserAuthSchema(BaseModel):
    email: EmailStr = Field(
        min_length=6,
        max_length=256,
        title="Email",
        description=(
            "Номер пользователя, уникальное строковое поле;"
            " Допустимая длина строки - от 7 до 18 символов включительно;"
        ),
    )
    password: str = Field(
        min_length=5,
        max_length=50,
        title="Password",
        description="Пароль, поле длинной от 5 до 50 символов влючительно.",
    )

    class Config:
        """Config class for this model."""

        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "super_password",
            }
        }


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = Field(
        None,
        min_length=6,
        max_length=256,
        title="Email",
        description=(
            "Номер пользователя, уникальное строковое поле;"
            " Допустимая длина строки - от 7 до 18 символов включительно;"
        ),
    )
    phone_number: Optional[str] = Field(
        None,
        min_length=7,
        max_length=18,
        title="Phone number",
        description=(
            "Номер телефона в международном формате, начинающийся с '+'"
            " уникальное строковое поле; допустимая длина"
            " строки - от 7 до 18 символов включительно;"
        ),
    )
    first_name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=256,
        description=(
            "Имя пользователя, строковое поле; "
            "Допустимая длина строки - от 3 до 256 символов включительно;"
        ),
    )
    last_name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=256,
        description=(
            "Фамилия пользователя, строковое поле; "
            "Допустимая длина строки - от 3 до 256 символов включительно;"
        ),
    )

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str | HTTPException:
        if not re.match(r"^\+\d{5,16}$", value):
            ext_msg = (
                "Номер телефона должен начинаться с"
                " '+' и содержать от 5 до 16 цифр"
            )
            raise HTTPException(422, ext_msg)
        return value

    class Config:
        """Config class for this model."""

        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "phone_number": "+874493831",
                "first_name": "Алексей",
                "last_name": "Яковенко",
            }
        }


class UserUpdateRolesSchema(UserAuthSchema):
    is_admin: Optional[bool] = Field(
        title="Is Admin",
        comment="Булево значение, определяющее пользователя администратора.",
    )
    is_superuser: Optional[bool] = Field(
        title="Is Superuser",
        comment="Булево значение, определяющее пользователя суперюзера.",
    )

    class Config:
        """Config class for this model."""

        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "super_password",
            }
        }


class UserChangePassword(BaseModel):
    old_password: str = Field(
        min_length=5,
        max_length=50,
        title="Old Password",
        description=(
            "Старый пароль, поле длинной от 5 до 50 символов влючительно."
        ),
    )
    new_password: str = Field(
        min_length=5,
        max_length=50,
        title="New Password",
        description=(
            "Новый пароль, поле длинной от 5 до 50 символов влючительно."
        ),
    )

    class Config:
        """Config class for this model."""

        json_schema_extra = {
            "example": {
                "old_password": "old_password",
                "new_password": "new_password",
            }
        }


class UserSchemaDB(BaseModel):
    id: int = Field(title="Id", description="Айди пользователя в бд")
    email: EmailStr = Field(
        min_length=6,
        max_length=256,
        title="Email",
        description=(
            "Номер пользователя, уникальное строковое поле;"
            " Допустимая длина строки - от 7 до 18 символов включительно;"
        ),
    )
    phone_number: str = Field(
        min_length=7,
        max_length=18,
        title="Phone number",
        description=(
            "Номер телефона в международном формате, начинающийся с '+'"
            " уникальное строковое поле; допустимая длина"
            " строки - от 7 до 18 символов включительно;"
        ),
    )
    first_name: str = Field(
        min_length=3,
        max_length=256,
        description=(
            "Имя пользователя, строковое поле; "
            "Допустимая длина строки - от 3 до 256 символов включительно;"
        ),
    )
    last_name: str = Field(
        min_length=3,
        max_length=256,
        description=(
            "Фамилия пользователя, строковое поле; "
            "Допустимая длина строки - от 3 до 256 символов включительно;"
        ),
    )
    is_admin: bool = Field(
        True,
        comment="Булево значение, определяющее пользователя администратора.",
    )
    is_superuser: bool = Field(
        True, comment="Булево значение, определяющее пользователя суперюзера."
    )

    class Config:
        """Config class for this model."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "phone_number": "+874493831",
                "first_name": "Алексей",
                "last_name": "Яковенко",
                "is_admin": False,
                "is_superuser": False,
            }
        }

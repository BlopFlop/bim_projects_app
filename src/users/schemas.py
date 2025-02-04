from fastapi.exceptions import HTTPException

from pydantic import (
    BaseModel,
    EmailStr,
    Field, 
    field_validator,
    model_validator
)
import re


class UserRegister(BaseModel):
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
        description="Пароль, поле длинной от 5 до 50 символов влючительно."
    )
    phone_number: str = Field(
        min_length=7,
        max_length=18,
        title="Phone number",
        description=(
            "Номер телефона в международном формате, начинающийся с '+'"
            " уникальное строковое поле; допустимая длина"
            " строки - от 7 до 18 символов включительно;"
        )
    )
    first_name: str = Field(
        min_length=3,
        max_length=256,
        description=(
            "Имя пользователя, строковое поле; "
            "Допустимая длина строки - от 3 до 256 символов включительно;"
        )
    )
    last_name: str = Field(
        min_length=3,
        max_length=256,
        description=(
            "Фамилия пользователя, строковое поле; "
            "Допустимая длина строки - от 3 до 256 символов включительно;"
        )
    )

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str | HTTPException:
        if not re.match(r'^\+\d{5,16}$', value):
            ext_msg = (
                "Номер телефона должен начинаться с"
                " '+' и содержать от 5 до 16 цифр"
            )
            raise HTTPException(422, ext_msg)
        return value

    @model_validator(mode="before")
    def validate_not_equal_email_and_password(self) -> HTTPException:

        if self["email"] == self["password"]:
            ext_msg = "Почта и пароль не могут быть одинаковыми."
            raise HTTPException(422, ext_msg)
        return self

    class Config:
        """Config class for this model."""

        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "super_password",
                "phone_number": "+874493831",
                "first_name": "Алексей",
                "last_name": "Яковенко"
            }
        }


class UserAuth(BaseModel):
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
        description="Пароль, поле длинной от 5 до 50 символов влючительно."
    )

    class Config:
        """Config class for this model."""

        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "super_password",
            }
        }

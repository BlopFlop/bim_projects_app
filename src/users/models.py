from sqlalchemy import String, CheckConstraint, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    """User model."""

    phone_number: Mapped[str] = mapped_column(
        String(18),
        CheckConstraint(
            "7 <= LENGTH(phone_number) <= 18",
            name="check_len_phone_number"
        ),
        unique=True,
        nullable=False,
        comment=(
            "Номер пользователя, уникальное обязательное строковое поле;"
            " допустимая длина строки - от 7 до 18 символов включительно;"
        )
    )
    first_name: Mapped[str] = mapped_column(
        String(256),
        CheckConstraint(
            "3 <= LENGTH(first_name) <= 256",
            name="check_len_first_name"
        ),
        nullable=False,
        comment=(
            "Имя пользователя, обязательное строковое поле;"
            " допустимая длина строки - от 3 до 256 символов включительно;"
        )
    )
    last_name: Mapped[str] = mapped_column(
        String(256),
        CheckConstraint(
            "3 <= LENGTH(last_name) <= 256",
            name="check_len_last_name"
        ),
        nullable=False,
        comment=(
            "Фамилия пользователя, обязательное строковое поле;"
            " допустимая длина строки - от 3 до 256 символов включительно;"
        )
    )
    email: Mapped[str] = mapped_column(
        String(256),
        CheckConstraint(
            "6 <= LENGTH(email) <= 256",
            name="check_len_email"
        ),
        unique=True,
        nullable=False,
        comment=(
            "email пользователя, уникальное обязательное строковое поле;"
            " допустимая длина строки - от 6 до 256 символов включительно;"
        )
    )
    password: Mapped[str] = mapped_column(
        String,
        unique=False,
        nullable=False,
        comment=(
            "Хешированный пароль пользователя, обязательное строковое поле;"
        )
    )

    is_user: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
        nullable=False,
        comment=(
            "Булево значение, определяющее зарегестрированного пользователя."
        )
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("false"),
        nullable=False,
        comment=(
            "Булево значение, определяющее пользователя администратора."
        )
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("false"),
        nullable=False,
        comment=(
            "Булево значение, определяющее пользователя суперюзера."
        )
    )

    extend_existing = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.first_name} {self.last_name}"

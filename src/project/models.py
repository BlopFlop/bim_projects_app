from datetime import datetime, timezone
from typing import Final
import enum

from sqlalchemy import CheckConstraint, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Project(Base):
    """BIM Project model."""

    name: Mapped[str] = mapped_column(
        String(150),
        CheckConstraint(
            "0 < LENGTH(name) <= 150",
            name="check_len_name_project"
        ),
        unique=True,
        nullable=False,
        comment=(
            "Уникальное название проекта, обязательное строковое поле;"
            " Допустимая длина строки — от 1 до 150 символов включительно;"
        ),
    )
    description: Mapped[str] = mapped_column(
        String(350),
        CheckConstraint(
            "0 < LENGTH(description) <= 350",
            name="check_len_desc_project"
        ),
        nullable=False,
        comment=(
            "Описание/Полное имя проекта, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 350 символов включительно;"
        ),
    )
    code: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "0 < LENGTH(code) <= 50",
            name="check_len_code"
        ),
        nullable=False,
        unique=True,
        comment=(
            "Код проекта, обязательное уникальное строковое поле;"
            " допустимая длина строки - от 1 до 50 символов включительно."
        )
    )
    image: Mapped[str] = mapped_column(
        String(150),
        CheckConstraint(
            "0 <= LENGTH(image) <= 150",
            name="check_len_image"
        ),
        nullable=True,
        comment=(
            "Путь до изоображения, строковое поле;"
            " допустимая длина строки - от 0 до 150 символов включительно;"
        )
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        comment="Дата и время создания проекта."
    )

    base_path: Mapped[str] = mapped_column(
        String(200),
        CheckConstraint(
            "1 < LENGTH(base_path) <= 200",
            name="check_len_base_path"
        ),
        nullable=True,
        comment=(
            "Путь до базовой директории, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 200 символов включительно;"
        ),
    )
    arch_path: Mapped[str] = mapped_column(
        String(200),
        CheckConstraint(
            "0 < LENGTH(arch_path) <= 200",
            name="check_len_arch_path"
        ),
        nullable=True,
        comment=(
            "Путь до архивной директории, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 200 символов включительно;"
        ),
    )
    ftp_path: Mapped[str] = mapped_column(
        String(200),
        CheckConstraint(
            "0 < LENGTH(ftp_path) <= 200",
            name="check_len_ftp_path"
        ),
        nullable=True,
        comment=(
            "Путь до файла, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 200 символов включительно;"
        ),
    )

    # related fields
    models: Mapped[list["BIMModel"]] = relationship(
        "BIMModel",
        back_populates="project",
        cascade="all, delete-orphan"
    )


class RevitServer(Base):
    """RevitServer model."""

    __tablename__: Final[str] = "revit_server"

    name: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "0 < LENGTH(name) <= 50",
            name="check_len_name_revitserver"
        ),
        unique=True,
        nullable=False,
        comment=(
            "Уникальное название RevitServer, обязательное строковое поле;"
            " допустимая длина строки - от 1 до 50 символов включительно."
        )
    )

    models: Mapped[list["BIMModel"]] = relationship(
        "BIMModel",
        back_populates="server",
        cascade="all, delete-orphan"
    )


class ModelSection(Base):
    """Model section engeneer systems in project."""

    __tablename__: Final[str] = "model_section"

    name: Mapped[str] = mapped_column(
        String(150),
        CheckConstraint(
            "0 < LENGTH(name) <= 150",
            name="check_len_name_section"
        ),
        unique=True,
        nullable=False,
        comment=(
            "Уникальное название раздела, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 150 символов включительно;"
        ),
    )
    description: Mapped[str] = mapped_column(
        String(350),
        CheckConstraint(
            "0 < LENGTH(description) <= 350",
            name="check_len_desc_section"
        ),
        nullable=False,
        comment=(
            "Описание имя раздела модели, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 350 символов включительно;"
        ),
    )

    # relation fields
    models: Mapped[list["BIMModel"]] = relationship(
        "BIMModel",
        back_populates="section",
        cascade="save-update"
    )


class ModelTypeEnum(str, enum.Enum):
    """Type bim model."""

    WORK_INNER = "Рабочая модель внутренняя"
    WORK_OUTER = "Рабочая модель внешняя"
    ANALYZE = "Аналитическая модель"
    SUPPORT = "Вспомогательная модель"


class BIMModel(Base):
    """Revit or Navis or IFC model."""

    __tablename__: Final[str] = "bim_model"

    name_file: Mapped[str] = mapped_column(
        String(150),
        CheckConstraint(
            "0 < LENGTH(name_file) <= 150",
            name="check_len_name_file"
        ),
        nullable=False,
        comment=(
            "Название модели, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 150 символов включительно;"
        ),
    )
    type: Mapped[ModelTypeEnum] = mapped_column(
        default=ModelTypeEnum.SUPPORT,
        comment="Тип модели."
    )
    version: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            "2000 <= version <= 2100",
            name="check_version_file"
        ),
        nullable=False,
        comment=(
            "Версия Revit, обязательное целочисленное поле;"
            " допустимое значение от 2000 до 2100 включительно"
        )
    )
    extention: Mapped[str] = mapped_column(
        String(10),
        CheckConstraint(
            "1 < LENGTH(extention) <= 10",
            name="check_len_extention"
        ),
        unique=False,
        nullable=False,
        comment=(
            "Расширение файла, обязательное строковое поле; "
            "Допустимая длина строки - от 1 до 10 включительно;"
        )
    )
    path: Mapped[str] = mapped_column(
        String(200),
        CheckConstraint(
            "1 < LENGTH(path) <= 200",
            name="check_len_path"
        ),
        nullable=False,
        comment=(
            "Путь до файла, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 200 символов включительно;"
        ),
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        comment="Дата и время создания файла."
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        comment="Дата и время обновления файла."
    )

    # relation fields
    section_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("model_section.id"),
        nullable=True,
    )
    section: Mapped[ModelSection] = relationship(
        "ModelSection",
        back_populates="models"
    )

    server_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("revit_server.id"),
    )
    server: Mapped[RevitServer] = relationship(
        "RevitServer",
        back_populates="models"
    )

    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("project.id")
    )
    project: Mapped[Project] = relationship(
        "Project",
        back_populates="models"
    )

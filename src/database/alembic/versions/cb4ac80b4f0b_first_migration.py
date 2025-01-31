"""First migration

Revision ID: cb4ac80b4f0b
Revises: 
Create Date: 2025-01-31 13:00:35.719403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb4ac80b4f0b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('model_section',
    sa.Column('name', sa.String(length=150), nullable=False, comment='Уникальное название раздела, обязательное строковое поле; допустимая длина строки — от 1 до 150 символов включительно;'),
    sa.Column('description', sa.String(length=350), nullable=False, comment='Описание имя раздела модели, обязательное строковое поле; допустимая длина строки — от 1 до 350 символов включительно;'),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='Номер в базе данных'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('project',
    sa.Column('name', sa.String(length=150), nullable=False, comment='Уникальное название проекта, обязательное строковое поле; допустимая длина строки — от 1 до 150 символов включительно;'),
    sa.Column('description', sa.String(length=350), nullable=False, comment='Описание/Полное имя проекта, обязательное строковое поле; допустимая длина строки — от 1 до 350 символов включительно;'),
    sa.Column('code', sa.String(length=50), nullable=False, comment='Код проекта, обязательное уникальное строковое поле; допустимая длина строки - от 1 до 50 символов включительно.'),
    sa.Column('image', sa.String(length=150), nullable=True, comment='Путь до изоображения, строковое поле; допустимая длина строки - от 0 до 150 символов включительно;'),
    sa.Column('created_on', sa.DateTime(), nullable=False, comment='Дата и время создания проекта.'),
    sa.Column('base_path', sa.String(length=200), nullable=False, comment='Путь до базовой директории, обязательное строковое поле; допустимая длина строки — от 1 до 200 символов включительно;'),
    sa.Column('arch_path', sa.String(length=200), nullable=False, comment='Путь до файла, обязательное строковое поле; допустимая длина строки — от 1 до 200 символов включительно;'),
    sa.Column('ftp_path', sa.String(length=200), nullable=False, comment='Путь до файла, обязательное строковое поле; допустимая длина строки — от 1 до 200 символов включительно;'),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='Номер в базе данных'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('name')
    )
    op.create_table('revit_server',
    sa.Column('name', sa.String(length=50), nullable=False, comment='Уникальное название RevitServer, обязательное строковое поле; допустимая длина строки - от 1 до 50 символов включительно.'),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='Номер в базе данных'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('bim_model',
    sa.Column('name_file', sa.String(length=150), nullable=False, comment='Название модели, обязательное строковое поле; допустимая длина строки — от 1 до 150 символов включительно;'),
    sa.Column('type', sa.Enum('WORK_INNER', 'WORK_OUTER', 'ANALYZE', 'SUPPORT', name='modeltypeenum'), nullable=False, comment='Тип модели.'),
    sa.Column('version', sa.Integer(), nullable=False, comment='Версия Revit, обязательное целочисленное поле; допустимое значение от 2000 до 2100 включительно'),
    sa.Column('extention', sa.String(length=10), nullable=False, comment='Расширение файла, обязательное строковое поле; Допустимая длина строки - от 1 до 10 включительно;'),
    sa.Column('path', sa.String(length=200), nullable=False, comment='Путь до файла, обязательное строковое поле; допустимая длина строки — от 1 до 200 символов включительно;'),
    sa.Column('created_on', sa.DateTime(), nullable=False, comment='Дата и время создания файла.'),
    sa.Column('updated_on', sa.DateTime(), nullable=False, comment='Дата и время обновления файла.'),
    sa.Column('section_id', sa.Integer(), nullable=True),
    sa.Column('server_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='Номер в базе данных'),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.ForeignKeyConstraint(['section_id'], ['model_section.id'], ),
    sa.ForeignKeyConstraint(['server_id'], ['revit_server.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bim_model')
    op.drop_table('revit_server')
    op.drop_table('project')
    op.drop_table('model_section')
    # ### end Alembic commands ###

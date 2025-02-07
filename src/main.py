from fastapi import FastAPI

from api import main_api_v1_router
from config import application_config
from constants import (
    DATE_FORMAT,
    DESCRITPION_FAST_API_APP,
    LOG_DIR,
    LOG_FORMAT,
)
from logging_ import configure_logging
from users import create_first_superuser

configure_logging(
    log_dir=LOG_DIR,
    name_app=application_config.name_app,
    date_format=DATE_FORMAT,
    log_format=LOG_FORMAT,
)


async def lifespan(app: FastAPI):
    await create_first_superuser()
    yield


app = FastAPI(
    title=application_config.name_app,
    description=DESCRITPION_FAST_API_APP,
    lifespan=lifespan,
)
app.include_router(main_api_v1_router, prefix="/api/v1")

from fastapi import FastAPI

from config import application_config
from logging_ import configure_logging
from constants import (
    DESCRITPION_FAST_API_APP,
    LOG_DIR,
    LOG_FORMAT,
    DATE_FORMAT
)
from api import main_api_v1_router


configure_logging(
    log_dir=LOG_DIR,
    name_app=application_config.name_app,
    date_format=DATE_FORMAT,
    log_format=LOG_FORMAT
)


app = FastAPI(
    title=application_config.name_app,
    description=DESCRITPION_FAST_API_APP,
)
app.include_router(
    main_api_v1_router,
    prefix="/api/v1"
)

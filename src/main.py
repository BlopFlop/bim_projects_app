from fastapi import FastAPI

from src.config import settings
from src.logging import configure_logging
from src.constants import DESCRITPION_FAST_API_APP


configure_logging()


app = FastAPI(
    title=settings.name_project,
    description=DESCRITPION_FAST_API_APP,
)

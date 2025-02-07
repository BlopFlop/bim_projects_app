from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

LOG_DIR: Final[Path] = BASE_DIR / "logs"
LOG_FILE: Final[Path] = LOG_DIR / "bim_project_app_logging.log"
DATE_FORMAT: Final[str] = "%Y-%m-%d"
LOG_FORMAT: Final[str] = '"%(asctime)s - [%(levelname)s] - %(message)s"'

ENV_PATH: Final[Path] = BASE_DIR / r"infra/.env"

STATIC_PATH: Final[Path] = BASE_DIR / "static"

DESCRITPION_FAST_API_APP: Final[str] = """Описание проекта."""

#  token constants
COOKIE_KEY: Final[str] = ""
USER_ACCESS_TOKEN_KEY: Final[str] = "users_access_token"
ACCESS_TOKEN_KEY: Final[str] = "access_token"
REFRESH_TOKEN_KEY: Final[str] = "refresh_token"
SECRET_KEY: Final[str] = "secret_key"
ALGORITHM_KEY: Final[str] = "algorithm"

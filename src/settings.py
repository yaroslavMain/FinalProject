from pathlib import Path
from passlib.context import CryptContext

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .types import Settings

SETTINGS = Settings()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(
    directory=BASE_DIR / 'templates'
)

static = StaticFiles(directory=BASE_DIR / 'static')
media = StaticFiles(directory=BASE_DIR / 'media')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
templating = Jinja2Templates(directory='templates')

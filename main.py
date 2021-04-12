import os
from pathlib import Path

from app import create_app

BASE_DIR = Path(__file__).resolve().parent

settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

username = 'sangeeky'
password = 'uimi2312'


class Config:
    SECRET_KEY = 'developer'
    BOOTSTRAP_SERVE_LOCAL = True
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{username}:{password}@localhost:5432/uimidb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# config/prod.py

from .default import *


SECRET_KEY = 'SUPER_SECRET'

APP_ENV = APP_ENV_PRODUCTION

SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@host:port/db_name'

# config/default.py

from os.path import abspath, dirname

BASE_DIR = dirname(dirname(abspath(__file__)))

# from pathlib import Path
#
# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'SUPER_SECRET_KEY'

# Database configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Bootstrap local
BOOTSTRAP_SERVE_LOCAL = True


# App environments
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''
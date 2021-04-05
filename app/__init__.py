"""
 Create App
 Add DB

 add Config Flask

 register blueprints

"""
# Flask Libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

# Config Files
from .config import Config, BASE_DIR


def create_app():
    # Crear y Configurar Flask App
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)  # Configurar App
    bootstrap = Bootstrap(app)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

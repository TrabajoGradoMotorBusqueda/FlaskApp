"""
 Create App
 Add DB

 add Config Flask

 register blueprints

"""
# Flask Libraries
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

# Config Files
from .config import Config, BASE_DIR

db = SQLAlchemy()


def create_app():
    # Crear y Configurar Flask App
    app = Flask(__name__, instance_relative_config=True)
    # Cargar configuracion
    app.config.from_object(Config)  # Configurar App

    # Registra Tablas en la BD
    db.init_app(app)

    # Agregamos Bootstrap a la app
    bootstrap = Bootstrap(app)

    # Registro de los blueprints
    from .public import public_bp
    app.register_blueprint(public_bp)

    return app


def register_error_handlers(app):
    pass
    # @app.errorhandler(500)
    # def base_error_handler(e):
    #     return render_template('500.html'), 500
    #
    # @app.errorhandler(404)
    # def error_404_handler(e):
    #     return render_template('404.html'), 404
    #
    # @app.errorhandler(401)
    # def error_404_handler(e):
    #     return render_template('401.html'), 401

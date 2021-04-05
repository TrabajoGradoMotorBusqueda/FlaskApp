# Modulo Ontologia
import inspect
import os
import sys

# Flask Libraries
from flask import render_template, jsonify, redirect, url_for

# App Modules
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.forms import SearchForm

# UIMI Modules
import uimi

# Json Dumps
from json import dumps

# Importar Ontologia
# current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# Agregar Ontologia como modulo

# TODO: Agregaar Fixmi como modulo


# migrate = Migrate(app, db)

from app import create_app, BASE_DIR
sys.path.insert(1, BASE_DIR / 'ontologia')
sys.path.insert(1, BASE_DIR / 'uimi')


app = create_app()

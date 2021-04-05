# Modulo Ontologia
import inspect
import os
import sys

# Flask Libraries
from flask import render_template, jsonify, redirect, url_for

# App Modules
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app import create_app, BASE_DIR
from app.forms import SearchForm

# UIMI Modules
import uimi

# Json Dumps
from json import dumps

# Importar Ontologia
# current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# Agregar Ontologia como modulo
sys.path.insert(1, BASE_DIR / 'ontologia')
# TODO: Agregaar Fixmi como modulo


app = create_app()  # Iniciamos la aplicacion de Flas
db = SQLAlchemy(app)
# migrate = Migrate(app, db)

from database.models import Investigacion, DiccionarioLema


@app.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    context = {
        'search_form': search_form
    }

    if search_form.validate_on_submit():
        query = search_form.searchbar.data
        # return render_template('results.html', query=query)
        return redirect(url_for('busqueda', query=query))

    return render_template('index.html', **context)


@app.route('/busqueda/<query>', methods=['GET'])
def busqueda(query):
    resultados = uimi.search_engine(query)
    resultados = construir_resultados(resultados)
    # print(resultados)
    # for i in range(len(resultados)):
    #     titulo = resultados[i]['titulo']
    #     print(f'({str(i)}) {titulo.capitalize()} \n')
    # return jsonify(resultados)
    return render_template('results.html', resultados=dumps(resultados))


def construir_resultados(lista_resultados):
    resultados = {}
    for i, proyecto in enumerate(lista_resultados):
        id_proyecto = proyecto.get_id_proyecto_investigacion()[0]
        titulo = proyecto.get_titulo_proyecto_investigacion()[0]
        resumen = proyecto.get_resumen_proyecto_investigacion()[0]
        palabras_clave = proyecto.get_palabras_clave()
        tipo = proyecto.get_tipo_proyecto_investigacion()[0]
        estado = proyecto.get_estado_proyecto_investigacion()[0]
        resultados[i] = {
            "id": id_proyecto,
            "titulo": titulo,
            "resumen": resumen,
            "palabras_clave": palabras_clave,
            "tipo": tipo,
            "estado": estado
        }

    return resultados



# Modulo Ontologia
import inspect
import os
import sys

# Flask Libraries
from flask import render_template, jsonify, redirect, url_for

# App Modules
from app import create_app
from app.forms import SearchForm

# UIMI Modules
import uimi

#Json Dumps
from json import dumps

#Importar Ontologia
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(1, current_dir + '/ontologia')

app = create_app()  # Iniciamos la aplicacion de Flask


@app.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    context = {
        'search_form': search_form
    }

    if search_form.validate_on_submit():
        return redirect(url_for('busqueda', query=search_form.searchbar.data))

    return render_template('index.html', **context)


@app.route('/busqueda/<query>', methods=['GET', 'POST'])
def busqueda(query):
    resultados = uimi.search_engine(query)
    resultados = construir_resultados(resultados)
    return render_template('results.html', resultados=dumps(resultados))


def construir_resultados(lista_resultados):
    resultados = {}
    for i, proyecto in enumerate(lista_resultados):
        id_proyecto = proyecto.get_id_proyecto_investigacion()
        titulo = proyecto.get_titulo_proyecto_investigacion()
        resumen = proyecto.get_resumen_proyecto_investigacion()
        palabras_clave = proyecto.get_palabras_clave()
        tipo = proyecto.get_tipo_proyecto_investigacion()
        estado = proyecto.get_estado_proyecto_investigacion()
        resultados[i] = {
            "id": id_proyecto,
            "titulo": titulo[0],
            "resumen": resumen[0],
            "palabras_clave": palabras_clave,
            "tipo": tipo[0],
            "estado": estado[0]
        }

    return resultados

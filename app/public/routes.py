"""
Routes
1. Index - Busqueda
2. Resultados
3. Consulta de Documentos
"""
import json

from flask import url_for, render_template, jsonify, json as fjson
from flask import redirect

from . import public_bp

from uimi import search_engine

from json import dumps

from .forms import SearchForm


@public_bp.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    context = {
        'search_form': search_form
    }

    if search_form.validate_on_submit():
        query = search_form.searchbar.data
        if query == 'fixmi':
            import fixmi
            fixmi.iniciar_fixmi()
            return "YAAAA"
        return redirect(url_for('public.busqueda', query=query))

    return render_template('public/index.html', **context)


@public_bp.route('/busqueda/<query>', methods=['GET'])
def busqueda(query):
    resultados = search_engine(query)
    # resultados = construir_resultados(resultados)
    # print(resultados)
    # for i in range(len(resultados)):
    #     titulo = resultados[i]['titulo']
    #     print(f'({str(i)}) {titulo.capitalize()} \n')
    return jsonify(investigaciones=resultados, total=len(resultados))
    # return render_template('public/results.html', resultados=dumps(resultados))


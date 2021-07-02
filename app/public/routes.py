"""
Routes
1. Index - Busqueda
2. Resultados
3. Consulta de Documentos
"""
import json

from flask import url_for, render_template, jsonify
from flask import redirect, request

from . import public_bp

from uimi import search_engine, investigaciones_relacionadas

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
        return redirect(url_for('public.resultados', query=query))

    return render_template('public/index.html', **context)


@public_bp.route('/resultados', methods=['GET'])
def resultados():
    return render_template('public/results.html', query=request.args.get('query'))


@public_bp.route('/busqueda/<query>', methods=['GET'])
def busqueda(query):
    resultados_investigaciones = search_engine(query)

    return jsonify(investigaciones=resultados_investigaciones, total=len(resultados_investigaciones))
    # return render_template('public/results.html', resultados=dumps(resultados))


@public_bp.route('/relacionados/<int:investigacion>', methods=['GET'])
def relacionados(investigacion):
    resultados_investigaciones, investigacion_original = investigaciones_relacionadas(investigacion)

    return jsonify(relacionados=resultados_investigaciones, investigacion=investigacion_original)

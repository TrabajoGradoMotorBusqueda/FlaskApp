"""
Routes
1. Index - Busqueda
2. Resultados
3. Consulta de Documentos
"""
from flask import url_for, render_template
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
        # if query == 'fixmi':
        #     # import fixmi
        #     fixmi.iniciar_fixmi()
        #     return "YAAAA"
        return redirect(url_for('public.busqueda', query=query))

    return render_template('public/index.html', **context)


@public_bp.route('/busqueda/<query>', methods=['GET'])
def busqueda(query):
    resultados = search_engine(query)
    resultados = construir_resultados(resultados)
    # print(resultados)
    # for i in range(len(resultados)):
    #     titulo = resultados[i]['titulo']
    #     print(f'({str(i)}) {titulo.capitalize()} \n')
    # return jsonify(resultados)
    return render_template('public/results.html', resultados=dumps(resultados))


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

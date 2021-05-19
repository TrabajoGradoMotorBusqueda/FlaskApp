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
        if query == 'fixmi':
            import fixmi
            fixmi.iniciar_fixmi()
            return "YAAAA"
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
        id_proyecto = proyecto.get_id_proyecto_investigacion()[0]  # atributo
        titulo = proyecto.get_titulo_proyecto_investigacion()[0]  # atributo
        resumen = proyecto.get_resumen_proyecto_investigacion()[0]  # atributo
        palabras_clave = proyecto.get_palabras_clave()  # atributo en lista
        facultades = proyecto.pi_se_asocia_facultad  # instancia
        programas = proyecto.pi_se_asocia_programa  # instancia
        lineas_investigacion = proyecto.pi_pertenece_li  # instancia
        grupos_investigacion = [linea.li_pertenece_gi[0] for linea in lineas_investigacion]  # instancia
        # viis = proyecto.pi_pertenece_viis.get_nombre_VIIS()[0]  # atributo
        # universidad = proyecto.pi_pertenece_viis.viis_pertenece_universidad.get_nombre_universidad()[0] # atributo
        convocatoria = proyecto.pi_pertenece_convocatoria  # instancia
        # tipo_convocatoria = convocatoria.get_tipo_convocatoria()[0]  # atributo
        # anio_convocatoria = convocatoria.get_anio_convocatoria()[0]  # atributo
        tipo_investigacion = proyecto.get_tipo_proyecto_investigacion()[0]  # atributo
        if tipo_investigacion.strip() == "Docente":
            autores = proyecto.pi_tiene_autor_docente  # instancias
        else:
            autores = proyecto.pi_tiene_autor_estudiante  # instancias
        asesores = proyecto.pi_es_asesorado_docente  # instancias

        resultados[i] = {
            "id": id_proyecto,
            "tipo_investigacion": tipo_investigacion,
            "titulo": titulo,
            "resumen": resumen,
            "palabras_clave": palabras_clave,
            "autores": [autor.nombres_investigador[0] + " " + autor.apellidos_investigador[0] for autor in autores],
            "asesores": [asesor.get_nombres_investigador()[0] + " " + asesor.get_apellidos_investigador()[0] for asesor in asesores],
            # "universidad": universidad,
            "facultades": [facultad.get_nombre_facultad()[0] for facultad in facultades],
            "programas": [programa.get_nombre_programa()[0] for programa in programas],
            "grupos_investigacion": [grupo.get_nombre_grupo_investigacion()[0] for grupo in grupos_investigacion],
            "lineas_investigacion": [linea.get_nombre_linea_investigacion()[0] for linea in lineas_investigacion]
            # "viis": viis,
            # "tipo_convocatoria": tipo_convocatoria,
            # "anio_convocatoria": anio_convocatoria
        }

    # nombres_investigador, apellidos_investigador
    return resultados


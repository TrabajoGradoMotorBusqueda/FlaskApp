# ElasticSearch
from elasticmi import ElasticSearchEngine

# Cargar ElasticSearch
elasticsearch = ElasticSearchEngine()

# Palabras
from .words import palabras_similares
# Documentos
from .docs import documentos_recomendados
# Busqueda Ontologia
from ontologia.busqueda_ontologia import ranking_documentos_ontologia, busqueda_lista_documentos

modelo = None


def search_engine(palabras):
    # Busqueda W2V de Palabras recomendadas
    palabras_recomendadas, palabras_limpias = palabras_similares(palabras)
    if palabras_recomendadas is None:
        return None

    # Busqueda de documentos en Ontologia
    documentos_ontologia, id_documentos_ontologia = ranking_documentos_ontologia(palabras_recomendadas)

    id_documentos_d2v = documentos_recomendados(palabras_limpias, topn=len(id_documentos_ontologia))
    documentos_d2v = busqueda_lista_documentos(id_documentos_d2v)

    ranking_final_documentos = []
    for ontologia_doc, d2v_doc in zip(documentos_ontologia, documentos_d2v):
        if ontologia_doc == d2v_doc:
            ranking_final_documentos.append(ontologia_doc)
        else:
            if (ontologia_doc not in ranking_final_documentos) and (d2v_doc not in ranking_final_documentos):
                ranking_final_documentos.append(d2v_doc)
                ranking_final_documentos.append(ontologia_doc)

    # Busqueda Elastic Doc2Vec
    # id_documentos_d2v = elasticsearch.busqueda_d2v(modelo.infer_vector([' '.join(palabras)]),
    #                                               len(documentos_ontologia))
    #
    # documentos_d2v = busqueda_lista_documentos(id_documentos_d2v)  # Documentos Restantes D2V
    #
    # ranking_final_documentos = []
    # for ontologia_doc, d2v_doc in zip(documentos_ontologia, documentos_d2v):
    #     if ontologia_doc == d2v_doc:
    #         ranking_final_documentos.append(ontologia_doc)
    #     else:
    #         if (ontologia_doc not in ranking_final_documentos) and (d2v_doc not in ranking_final_documentos):
    #             ranking_final_documentos.append(ontologia_doc)
    #             ranking_final_documentos.append(d2v_doc)

    return construir_resultados(ranking_final_documentos)
    # return ranking_final_documentos


def construir_resultados(lista_resultados):
    resultados = []
    for i, proyecto in enumerate(lista_resultados):
        id_proyecto = proyecto.get_id_proyecto_investigacion()[0]  # atributo
        titulo = proyecto.get_titulo_proyecto_investigacion()[0]  # atributo
        resumen = proyecto.get_resumen_proyecto_investigacion()[0]  # atributo
        palabras_clave = proyecto.get_palabras_clave()  # atributo en lista
        facultades = proyecto.pi_se_asocia_facultad  # instancia
        programas = proyecto.pi_se_asocia_programa  # instancia
        lineas_investigacion = proyecto.pi_pertenece_li  # instancia
        grupos_investigacion = [linea.li_pertenece_gi[0] for linea in lineas_investigacion]  # instancia
        convocatoria = proyecto.pi_pertenece_convocatoria[0]  # instancia
        tipo_convocatoria = convocatoria.get_tipo_convocatoria()[0]  # atributo
        try:
            anio_convocatoria = convocatoria.get_anio_convocatoria()[0]  # atributo
        except IndexError:
            anio_convocatoria = None  # atributo
        if tipo_convocatoria.strip() == "Docente":
            autores = proyecto.pi_tiene_autor_docente  # instancias
            tipo_investigacion = "Docente"  # atributo
        else:
            autores = proyecto.pi_tiene_autor_estudiante  # instancias
            tipo_investigacion = "Estudiantil"  # atributo

        asesores = proyecto.pi_es_asesorado_docente  # instancias

        resultados.append({
            "id": id_proyecto,
            "tipo_investigacion": tipo_investigacion,
            "titulo": titulo,
            "resumen": resumen,
            "palabras_clave": palabras_clave,
            "autores": [f"{autor.nombres_investigador[0]} {autor.apellidos_investigador[0]}" for autor in autores],
            "asesores": [f"{asesor.get_nombres_investigador()[0]} {asesor.get_apellidos_investigador()[0]}" for asesor
                         in asesores],
            "facultades": [facultad.get_nombre_facultad()[0] for facultad in facultades],
            "programas": [programa.get_nombre_programa()[0] for programa in programas],
            "grupos_investigacion": [grupo.get_nombre_grupo_investigacion()[0] for grupo in grupos_investigacion],
            "lineas_investigacion": [linea.get_nombre_linea_investigacion()[0] for linea in lineas_investigacion],
            "tipo_convocatoria": tipo_convocatoria,
            "anio_convocatoria": anio_convocatoria
        })

        if len(asesores) == 0:
            del resultados[i]['asesores']

    return resultados

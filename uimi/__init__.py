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
    # global modelo
    # if modelo is None:
    #     # Gensim DOC2VEC
    #     from doc2vec import cargar_modelo
    #     # Modelo Doc2Vec
    #     modelo = cargar_modelo()

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

    # construir_resultados(ranking_final_documentos)

    return ranking_final_documentos
    # return ranking_final_documentos

#
# def construir_resultados(lista_resultados):
#     resultados = {}
#     for i, proyecto in enumerate(lista_resultados):
#         id_proyecto = proyecto.get_id_proyecto_investigacion()[0]  # atributo
#         titulo = proyecto.get_titulo_proyecto_investigacion()[0]  # atributo
#         resumen = proyecto.get_resumen_proyecto_investigacion()[0]  # atributo
#         palabras_clave = proyecto.get_palabras_clave()  # atributo en lista
#         facultades = proyecto.pi_se_asocia_facultad  # instancia
#         programas = proyecto.pi_se_asocia_programa  # instancia
#         lineas_investigacion = proyecto.pi_pertenece_li  # instancia
#         grupos_investigacion = [linea.li_pertenece_gi[0] for linea in lineas_investigacion]  # instancia
#         viis = proyecto.pi_pertenece_viis.get_nombre_VIIS()[0]  # atributo
#         universidad = proyecto.pi_pertenece_viis.viis_pertenece_universidad.get_nombre_universidad()[0] # atributo
#         convocatoria = proyecto.pi_pertenece_convocatoria  # instancia
#         tipo_convocatoria = convocatoria.get_tipo_convocatoria()[0]  # atributo
#         anio_convocatoria = convocatoria.get_anio_convocatoria()[0]  # atributo
#         tipo_investigacion = proyecto.get_tipo_proyecto_investigacion()[0]  # atributo
#         if tipo_investigacion is "Docente":
#             autores = proyecto.pi_tiene_autor_docente  # instancias
#         else:
#             autores = proyecto.pi_tiene_autor_estudiante  # instancias
#         asesores = proyecto.pi_es_asesorado_docente  # instancias
#
#         resultados[i] = {
#             "id": id_proyecto,
#             "tipo_investigacion": tipo_investigacion,
#             "titulo": titulo,
#             "resumen": resumen,
#             "palabras_clave": palabras_clave,
#             "autores": [autor.get_nombres_investigador + " " + autor.get_apellidos_investigador for autor in autores],
#             "asesores": [asesor.get_nombres_investigador + " " + asesor.get_apellidos_investigador for asesor in asesores],
#             "universidad": universidad,
#             "facultades": [facultad.get_nombre_facultad()[0] for facultad in facultades],
#             "programas": [programa.get_nombre_programa()[0] for programa in programas],
#             "grupos_investigacion": [grupo.get_nombre_grupo_investigacion()[0] for grupo in grupos_investigacion],
#             "lineas_investigacion": [linea.get_nombre_linea_investigacion()[0] for linea in lineas_investigacion],
#             "viis": viis,
#             "tipo_convocatoria": tipo_convocatoria,
#             "anio_convocatoria": anio_convocatoria
#         }
#
#     # nombres_investigador, apellidos_investigador
#     return resultados

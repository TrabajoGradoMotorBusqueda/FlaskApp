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

    return ranking_final_documentos
    # return ranking_final_documentos

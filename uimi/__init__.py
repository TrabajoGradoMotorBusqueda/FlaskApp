import os

root_folder = os.path.dirname(os.path.abspath(__file__))

# Gensim DOC2VEC
from .modelos import Models

modelos = Models()

# ElasticSearch
from .elastic import ElasticSearchEngine

elasticsearch = ElasticSearchEngine()

# Palabras
from .words import palabras_similares

# Busqueda Ontologia
from .busqueda_ontologia import ranking_documentos_ontologia, busqueda_lista_documentos


# Ontologia

def search_engine(palabras):
    # Busqueda Elastic Palabras similares
    palabras_relacionadas = palabras_similares(palabras)
    # Busqueda de documentos en Ontologia
    documentos_ontologia, id_documentos_ontologia = ranking_documentos_ontologia(palabras_relacionadas)

    # Busqueda Elastic Doc2Vec
    id_documentos_d2v = elasticsearch.busqueda_d2v(
        modelos.modeloD2V.infer_vector([' '.join(palabras)]),  # Parametro 1
        len(documentos_ontologia))  # Parametro 2

    documentos_d2v = busqueda_lista_documentos(id_documentos_d2v)  # Documentos Restantes D2V

    ranking_final_documentos = []
    for ontologia_doc, d2v_doc in zip(documentos_ontologia, documentos_d2v):
        if ontologia_doc == d2v_doc:
            ranking_final_documentos.append(ontologia_doc)
        else:
            if (ontologia_doc not in ranking_final_documentos) and (d2v_doc not in ranking_final_documentos):
                ranking_final_documentos.append(ontologia_doc)
                ranking_final_documentos.append(d2v_doc)

    return ranking_final_documentos

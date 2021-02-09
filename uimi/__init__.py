import os

root_folder = os.path.dirname(os.path.abspath(__file__))

# Gensim
from .modelos import Models

# ElasticSearch
from .elastic import ElasticSearchEngine

elasticsearch = ElasticSearchEngine()

# Palabras
from .words import palabras_similares

# Busqueda Ontologia
from .busqueda_ontologia import ranking_documentos_ontologia

# Doc2Vec
modelos = Models()
D2V = modelos.modeloD2V


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

    ranking_busqueda_id = []
    for ontologia_id, d2v_id in zip(id_documentos_ontologia, id_documentos_d2v):
        if ontologia_id == d2v_id:
            ranking_busqueda_id.append(ontologia_id)
        else:
            if (ontologia_id not in ranking_busqueda_id) and (d2v_id not in ranking_busqueda_id):
                ranking_busqueda_id.append(ontologia_id)
                ranking_busqueda_id.append(d2v_id)

    return ranking_busqueda_id

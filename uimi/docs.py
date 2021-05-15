# Docs Recomendados
# from doc2vec import cargar_modelo

from doc2vec import modelo


def documentos_recomendados(palabras_limpias, topn=50):
    # global modelo
    # modelo = modelo or cargar_modelo()

    vector_busqueda = modelo.infer_vector(palabras_limpias)
    documentos = modelo.docvecs.most_similar([vector_busqueda], topn=topn)

    return [documento[0] for documento in documentos]

# Docs Recomendados
from doc2vec import cargar_modelo

modelo = None


def documentos_recomendados(palabras_limpias):
    global modelo
    modelo = modelo or cargar_modelo()

    vector_busqueda = modelo.infer_vector(palabras_limpias)
    documentos = modelo.docvecs.most_similar([vector_busqueda])

    return [documento[0] for documento in documentos]

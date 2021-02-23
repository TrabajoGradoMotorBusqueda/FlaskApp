from collections import Counter
from itertools import chain

from ontologia import ontologia


def ranking_documentos_ontologia(palabras):
    instancias_palabras = []
    documentos = []

    # Buscamos documentos que tengan esas palabras
    for palabra in palabras:
        instancia = ontologia.search(descripcion_palabra=palabra)
        instancias_palabras.extend(instancia)

    for instancia in instancias_palabras:
        for documento in instancia.palabra_describe_pi:
            documentos.append(documento)

    # Ordenando en base a la frecuencia de documentos
    ranking_busqueda = list(chain(i for i, c in Counter(documentos).most_common()))
    ranking_busqueda_id = [id_pi.get_id_proyecto_investigacion()[0] for id_pi in ranking_busqueda]

    return ranking_busqueda, ranking_busqueda_id


def busqueda_lista_documentos(docs_id):
    documentos = []

    # Buscamos documentos que tengan esas palabras
    for doc in docs_id:
        documento = ontologia.search(id_proyecto_investigacion=doc)
        documentos.append(documento[0])

    return documentos

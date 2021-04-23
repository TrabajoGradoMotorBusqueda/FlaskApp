import difflib
from . import elasticsearch
from app.models import DiccionarioLema
from fixmi import corpus as clean


lemas = None


def palabras_similares(palabras):
    # TODO: limpiar palabras y traer lemas palabras a sus lemas
    # TODO: Manejar Palabras de Nombres de Autores

    global lemas
    lemas = lemas or DiccionarioLema.get_lemas()

    # limpiar palabras
    _, palabras_limpias = clean.limpieza_corpus(palabras)()

    # Lema de Palabra para buscar
    palabras_busqueda = []
    # Nombres de Autores
    palabras_nombres = []
    # Palabras en plural o muy similares
    palabras_adicionales = []
    for palabra in palabras_limpias.split():
        adicionales = difflib.get_close_matches(palabra, lemas, n=5, cutoff=0.90)
        if len(adicionales) != 0:
            palabras_busqueda.append(adicionales[0])
            palabras_adicionales.extend(adicionales[1:])
        else:
            palabras_nombres.append(palabra)

    # Llegan las palabras
    # palabras = palabras.split()
    if len(palabras_nombres) == 0 or len(palabras_adicionales) > 0:
        palabras_relacionadas = elasticsearch.most_similar_words(palabras_busqueda)
        # Agregamos palabras
        palabras_relacionadas.extend(palabras_adicionales)
        palabras_relacionadas.extend(palabras_nombres)
    else:
        palabras_busqueda.extend(palabras_nombres)
        return palabras_busqueda

    return palabras_relacionadas

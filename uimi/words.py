import difflib
from . import elasticsearch
from app.models import DiccionarioLema


lemas = None


def palabras_similares(palabras):
    # TODO: limpiar palabras y traer lemas palabras a sus lemas
    # TODO: Manejar Palabras de Nombres de Autores

    global lemas
    lemas = lemas or DiccionarioLema.get_lemas()

    # Llegan las palabras
    palabras = palabras.split()

    palabras_relacionadas = elasticsearch.most_similar_words(palabras)

    # Palabras en plural o muy similares
    palabras_adicionales = []
    for palabra in palabras:
        adicionales = difflib.get_close_matches(palabra, lemas, n=5, cutoff=0.90)
        palabras_adicionales.extend(adicionales[1:])

    # Agregamos palabras
    palabras_relacionadas.extend(palabras_adicionales)

    return palabras_relacionadas

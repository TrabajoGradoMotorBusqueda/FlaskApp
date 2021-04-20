import difflib
from . import elasticsearch
from main import BASE_DIR
from app.models import DiccionarioLema

# Lectura de lemas
import json

with open(BASE_DIR / 'uimi/vocabulario/diccionario-lemas.json', 'r') as f:
    diccionario_lemas = json.loads(f.read())

# TODO: Cambiar por consulta en DB
# lemas = DiccionarioLema.get_lemas()


def palabras_similares(palabras):
    # TODO: limpiar palabras y traer lemas palabras a sus lemas
    # TODO: Manejar Palabras de Nombres de Autores

    # Llegan las palabras
    palabras = palabras.split()

    palabras_relacionadas = elasticsearch.most_similar_words(palabras)

    # Palabras en plural o muy similares
    palabras_adicionales = []
    for palabra in palabras:
        adicionales = difflib.get_close_matches(palabra, diccionario_lemas.keys(), n=5, cutoff=0.90)
        palabras_adicionales.extend(adicionales[1:])

    # Agregamos palabras
    palabras_relacionadas.extend(palabras_adicionales)

    return palabras_relacionadas

import difflib
from . import elasticsearch, root_folder

# Lectura de lemas
import json

with open(root_folder+'/vocabulario/diccionario-lemas.json', 'r') as f:
    diccionario_lemas = json.loads(f.read())

def palabras_similares(palabras):
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

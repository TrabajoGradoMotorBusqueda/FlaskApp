# Diccionario de Lemas
import difflib
from app.models import DiccionarioLema
# Limpieza de Busqueda
from fixmi import corpus as clean
import re
# Palabras Recomendadas
from doc2vec import cargar_modelo

# from . import elasticsearch


lemas = None
modelo = None
regex = re.compile(r'\d+')


def palabras_similares(palabras):
    global lemas
    lemas = lemas or DiccionarioLema.get_lemas()

    global modelo
    modelo = modelo or cargar_modelo()

    # Numeros
    palabras_numeros = regex.findall(palabras)
    # limpiar palabras
    palabras_limpias = clean.limpieza_corpus(palabras)()

    # Palabras para encontrar recomendaciones en w2v
    palabras_w2v = []
    # Palabras a buscar en la ontologia
    palabras_busqueda = []
    for palabra in palabras_limpias:
        adicionales = difflib.get_close_matches(palabra, lemas, n=5, cutoff=0.90)
        if len(adicionales) != 0:
            palabras_w2v.append(palabra)
            palabras_busqueda.extend(adicionales)
        elif palabra in modelo.wv.vocab:
            palabras_w2v.append(palabra)

    if len(palabras_w2v) == 0:
        return palabras_limpias
    # Llegan las palabras
    # palabras_relacionadas = elasticsearch.most_similar_words(palabras_busqueda) # Implementacion w2v in ElasticSearch
    palabras_recomendaciones = modelo.wv.most_similar(palabras_w2v, topn=50)
    palabras_busqueda.extend([similar[0] for similar in palabras_recomendaciones])
    palabras_busqueda.extend(palabras_numeros)

    return palabras_busqueda, palabras_limpias

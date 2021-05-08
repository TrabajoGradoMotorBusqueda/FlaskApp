import difflib
from . import elasticsearch
from app.models import DiccionarioLema
from fixmi import corpus as clean
from doc2vec import cargar_modelo


lemas = None
modelo = None


def palabras_similares(palabras):
    global lemas
    lemas = lemas or DiccionarioLema.get_lemas()

    global modelo
    modelo = modelo or cargar_modelo()

    # limpiar palabras
    _, palabras_limpias, _ = clean.limpieza_corpus(palabras)()

    # Lema de Palabra para buscar
    palabras_busqueda = []
    palabras_busqueda_w2v = []
    # Nombres de Autores
    palabras_nombres = []
    # Palabras en plural o muy similares
    palabras_adicionales = []
    for palabra in palabras_limpias.split():
        adicionales = difflib.get_close_matches(palabra, lemas, n=5, cutoff=0.90)
        if len(adicionales) != 0:
            palabras_busqueda_w2v.append(palabra)
            palabras_adicionales.extend(adicionales)
            # palabras_busqueda.append(adicionales[0])
            # palabras_adicionales.extend(adicionales[1:])
        elif palabra in modelo.wv.vocab:
            palabras_busqueda_w2v.append(palabra)
        else:
            palabras_busqueda.append(palabra)
            # palabras_nombres.append(palabra)

    # Llegan las palabras
    # palabras = palabras.split()
    palabras_relacionadas = modelo.wv.most_similar(palabras_busqueda_w2v, topn=50)
    palabras_adicionales.extend([similar[0] for similar in palabras_relacionadas])
    # palabras_busqueda_w2v.extend(palabras_adicionales)

    # if len(palabras_nombres) == 0 or len(palabras_adicionales) > 0:
    #     palabras_relacionadas = elasticsearch.most_similar_words(palabras_busqueda)
    #     # Agregamos palabras
    #     palabras_relacionadas.extend(palabras_adicionales)
    #     palabras_relacionadas.extend(palabras_nombres)
    # else:
    #     palabras_busqueda.extend(palabras_nombres)
    #     return palabras_busqueda

    return palabras_adicionales

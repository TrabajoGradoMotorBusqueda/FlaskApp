# Modulos DB
from app.models import Investigacion, DiccionarioLema


def almacenar_resumen(resumenes, tipo_resumen):
    # Resumenes Docentes Agregando Data a la BD
    for i, resumen in resumenes.iterrows():
        investigacion = Investigacion.__get_by_id_investigacion__(resumen['id_investigacion'])
        if investigacion is None:
            # Almacenar un nuevo Resumen
            resumen['tipo_resumen'] = tipo_resumen
            investigacion = Investigacion(resumen)  # Creamos el Objeto
        else:
            # Update Resumenes
            # resumen['tipo_resumen'] = tipo_resumen
            investigacion.tipo_resumen = tipo_resumen
            # investigacion.__attributes_setter__(resumen)
        investigacion.__save__()

    print('Base de datos con Resumenes' + tipo_resumen)


def construir_corpus():
    from .lemas import lematizar_corpus, diccionario_lemas
    from .corpus import construccion_corpus
    investigaciones = tuple(Investigacion.__get_all__())
    for investigacion in investigaciones:
        print(investigacion.id)
        corpus, corpus_limpio, autores = construccion_corpus(**vars(investigacion))
        corpus_lemas = lematizar_corpus(corpus_limpio)
        investigacion.corpus = corpus
        investigacion.corpus_palabras = corpus_limpio
        investigacion.corpus_lemas = corpus_lemas
        investigacion.corpus_lemas_autores = corpus_lemas + " " + autores
        investigacion.__save__()
        print('Investigacion: ' + str(investigacion.id) + ' Completo')
    print('Corpus Añadidos !')

    # Construir el vocabulario
    almacenar_vocabulario(diccionario_lemas)


def almacenar_vocabulario(diccionario):

    for key, value in diccionario.items():
        palabra = DiccionarioLema.get_by_lema(key)
        if palabra is None:
            palabra = DiccionarioLema(key, value)
        else:
            palabra.palabras = value
            palabra.save(update=True)
            continue
        palabra.save()

    print('Vocabulario Construdio')

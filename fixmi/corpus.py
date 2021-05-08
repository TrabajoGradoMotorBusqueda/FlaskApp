import re
from helpers import normalizar, stopwords

columns = ['palabra', 'facultad', 'programa', 'grupo', 'linea']
data = {}


def clean_text(text):
    """Make text lowercase,
    remove text in square brackets,
    remove punctuation and remove words
    containing numbers."""

    text = text.lower()
    text = re.sub(r'\d', '', text)
    text = re.sub(r'\.', '', text)
    pattern = re.compile(r"""                  # Flag para iniciar el modo verbose
              #(?:[A-Za-z]\.|\'|[A-Za-z])+     # Hace match con abreviaciones como U.S.A. o Nombre's
              #(?:[A-Za-z]\.)+                 # Hace match con abreviaciones como U.S.A.        
               \w+(?:\w+)*                     # Hace match con palabras completas
              # | \w+(?:-\w+)*                 # Hace match con palabras que pueden tener un guión interno
              # \$?\d+(?:\.\d+)?%?             # Hace match con dinero o porcentajes como $15.5 o 100%
              # \.\.\.                         # Hace match con puntos suspensivos
              # [][.,;"'?():-_`]               # Hace match con signos de puntuación
              """, re.X)

    resultado = pattern.findall(text)  # Encuentra las ocurrencias y las retorna como lista
    return resultado


def filtered_columns(column, nombres=False):
    regex = re.compile(column)
    filtered = list(filter(regex.match, data.keys()))
    values = []
    for item in filtered:
        value = data[item]
        if value is not None:
            values.append(value)

    return set(values) if not nombres else values


def corpus_original(campos):
    def wrapper(*args, **kargs):
        # Obtenemos los Valores de la Fila
        valores = campos(*args, **kargs)
        global data
        data = valores

        titulo = data['titulo_investigacion']
        resumen = data['resumen_investigacion']
        palabras_clave = filtered_columns(columns[0])
        facultad = filtered_columns(columns[1])
        programa = filtered_columns(columns[2])
        grupo_investigacion = filtered_columns(columns[3])
        linea_investigacion = filtered_columns(columns[4])
        tipo_convocatoria = data['tipo_convocatoria']

        corpus = \
            titulo + " " + \
            resumen + " " + \
            " ".join(palabras_clave) + " " + \
            " ".join(facultad) + " " + \
            " ".join(programa) + " " + \
            " ".join(grupo_investigacion) + " " + \
            " ".join(linea_investigacion) + " " + \
            tipo_convocatoria

        nombres = filtered_columns('nombres', True)
        apellidos = filtered_columns('apellidos', True)
        asesores = filtered_columns('asesor', True)

        # Trayendo nombres de autores
        autores = ""
        for nombre, apellido in zip(nombres, apellidos):
            autores += " " + nombre + " " + apellido

        autores += " " + " ".join(asesores)
        autores = autores.lstrip()
        autores = autores.rstrip()

        return corpus, autores.translate(normalizar).lower()

    return wrapper


def limpieza_corpus(corpus_inicial):
    def wrapper(*args, **kwargs):
        if callable(corpus_inicial):
            corpus = corpus_inicial(*args, **kwargs)
            palabras_limpias = clean_text(corpus[0])
            busqueda = False
        else:
            corpus = corpus_inicial.translate(normalizar)
            palabras_limpias = clean_text(corpus)
            busqueda = True

        palabras_limpias = [palabra for palabra in palabras_limpias
                            if palabra not in stopwords and len(palabra) > 2]

        if busqueda:
            return palabras_limpias

        corpus_limpio = ' '.join(palabras_limpias)
        return corpus, corpus_limpio, corpus[1]

    return wrapper


@limpieza_corpus
@corpus_original
def construccion_corpus(**campos):
    return campos

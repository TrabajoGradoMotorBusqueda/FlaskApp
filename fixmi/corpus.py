import re

stopwords = ["de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con", "no", "una", "su", "al", "lo", "como", "m\u00e1s", "pero", "sus", "le", "ya", "o", "este", "s\u00ed", "porque", "esta", "entre", "cuando", "muy", "sin", "sobre", "tambi\u00e9n", "me", "hasta", "hay", "donde", "quien", "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto", "m\u00ed", "antes", "algunos", "qu\u00e9", "unos", "yo", "otro", "otras", "otra", "\u00e9l", "tanto", "esa", "estos", "mucho", "quienes", "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros", "mi", "mis", "t\u00fa", "te", "ti", "tu", "tus", "ellas", "nosotras", "vosotros", "vosotras", "os", "m\u00edo", "m\u00eda", "m\u00edos", "m\u00edas", "tuyo", "tuya", "tuyos", "tuyas", "suyo", "suya", "suyos", "suyas", "nuestro", "nuestra", "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras", "esos", "esas", "estoy", "est\u00e1s", "est\u00e1", "estamos", "est\u00e1is", "est\u00e1n", "est\u00e9", "est\u00e9s", "estemos", "est\u00e9is", "est\u00e9n", "estar\u00e9", "estar\u00e1s", "estar\u00e1", "estaremos", "estar\u00e9is", "estar\u00e1n", "estar\u00eda", "estar\u00edas", "estar\u00edamos", "estar\u00edais", "estar\u00edan", "estaba", "estabas", "est\u00e1bamos", "estabais", "estaban", "estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron", "estuviera", "estuvieras", "estuvi\u00e9ramos", "estuvierais", "estuvieran", "estuviese", "estuvieses", "estuvi\u00e9semos", "estuvieseis", "estuviesen", "estando", "estado", "estada", "estados", "estadas", "estad", "he", "has", "ha", "hemos", "hab\u00e9is", "han", "haya", "hayas", "hayamos", "hay\u00e1is", "hayan", "habr\u00e9", "habr\u00e1s", "habr\u00e1", "habremos", "habr\u00e9is", "habr\u00e1n", "habr\u00eda", "habr\u00edas", "habr\u00edamos", "habr\u00edais", "habr\u00edan", "hab\u00eda", "hab\u00edas", "hab\u00edamos", "hab\u00edais", "hab\u00edan", "hube", "hubiste", "hubo", "hubimos", "hubisteis", "hubieron", "hubiera", "hubieras", "hubi\u00e9ramos", "hubierais", "hubieran", "hubiese", "hubieses", "hubi\u00e9semos", "hubieseis", "hubiesen", "habiendo", "habido", "habida", "habidos", "habidas", "soy", "eres", "es", "somos", "sois", "son", "sea", "seas", "seamos", "se\u00e1is", "sean", "ser\u00e9", "ser\u00e1s", "ser\u00e1", "seremos", "ser\u00e9is", "ser\u00e1n", "ser\u00eda", "ser\u00edas", "ser\u00edamos", "ser\u00edais", "ser\u00edan", "era", "eras", "\u00e9ramos", "erais", "eran", "fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron", "fuera", "fueras", "fu\u00e9ramos", "fuerais", "fueran", "fuese", "fueses", "fu\u00e9semos", "fueseis", "fuesen", "sintiendo", "sentido", "sentida", "sentidos", "sentidas", "siente", "sentid", "tengo", "tienes", "tiene", "tenemos", "ten\u00e9is", "tienen", "tenga", "tengas", "tengamos", "teng\u00e1is", "tengan", "tendr\u00e9", "tendr\u00e1s", "tendr\u00e1", "tendremos", "tendr\u00e9is", "tendr\u00e1n", "tendr\u00eda", "tendr\u00edas", "tendr\u00edamos", "tendr\u00edais", "tendr\u00edan", "ten\u00eda", "ten\u00edas", "ten\u00edamos", "ten\u00edais", "ten\u00edan", "tuve", "tuviste", "tuvo", "tuvimos", "tuvisteis", "tuvieron", "tuviera", "tuvieras", "tuvi\u00e9ramos", "tuvierais", "tuvieran", "tuviese", "tuvieses", "tuvi\u00e9semos", "tuvieseis", "tuviesen", "teniendo", "tenido", "tenida", "tenidos", "tenidas", "tened"]

columns = ['palabra', 'facultad', 'programa', 'grupo', 'linea']
data = {}

normalizar = str.maketrans('áéíóúüàèìòù', 'aeiouuaeiou')

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

        return corpus, autores.translate(normalizar).lower()
    return wrapper


def limpieza_corpus(corpus_inicial):
    def wrapper(*args, **kwargs):
        corpus, autores = corpus_inicial(*args, **kwargs) if callable(corpus_inicial) else corpus_inicial, ""
        palabras_limpias = clean_text(corpus)
        palabras_limpias = [palabra for palabra in palabras_limpias
                            if palabra not in stopwords and len(palabra) > 2]

        corpus_limpio = ' '.join(palabras_limpias)
        return corpus, corpus_limpio, autores
    return wrapper


@limpieza_corpus
@corpus_original
def construccion_corpus(**campos):
    return campos

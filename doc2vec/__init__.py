# Tabla Investigaciones
from app.models import Investigacion
from main import BASE_DIR

# Python
import multiprocessing
from time import time

# Gensim
from gensim import utils
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

modelo = None


class Corpus(object):
    def __init__(self, autores=False):
        self.corpus_autores = autores
        if not autores:
            self.corpus_investigaciones = Investigacion.__get_corpus_lemas__()
        else:
            self.corpus_investigaciones = Investigacion.__get_corpus_lemas_autores__()

    def __iter__(self):
        for corpus in self.corpus_investigaciones:
            if not self.corpus_autores:
                palabras = utils.simple_preprocess(corpus.corpus_lemas)
            else:
                palabras = utils.simple_preprocess(corpus.corpus_lemas_autores)

            yield TaggedDocument(palabras, [corpus.id])


def entrenamiento_d2v(autores=False):
    corpus = Corpus(autores)
    d2v = Doc2Vec(vector_size=300,  # Dimensionalidad Palabras Vector
                  window=5,  # Contexto, distancia entre palabras predichas
                  min_count=1,  # Minimo de palabras a buscar
                  workers=2,  # En mi CPU
                  dm=0,  # Usamos el Modelo PV-DBOW analogo a SkipGram
                  dbow_words=1,  # Entrenar el skip gram y documentos
                  hs=0,  # Cero para negative sampling, castigo a neurona
                  negative=20,  # Palabras irrelevantes para el muestreo negativo
                  ns_exponent=-0.5,  # Muestrea frecuencias por igual,
                  alpha=0.015,  # Tasa de aprendizaje
                  min_alpha=0.0001,  # Tasa que se reducira durante el train
                  seed=25,  # Semilla generar hash para palabras
                  max_vocab_size=None,  # Dependera de la maquina 10M -> 1GB
                  sample=5,  # Reduccion para palabras con alta frecuencia
                  epochs=150,  # Epocas, valores altos sobreentreno )?
                  )

    # Entrenamiento del modelo
    t = time()
    d2v.build_vocab(corpus,  # Oraciones nuevas
                    # update=True, #Agregar nuevo vocabulario
                    progress_per=100000  # Palabras para procesar con antecipacion
                    )  # prepare the model vocabulary
    print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))
    t = time()
    d2v.train(corpus, total_examples=d2v.corpus_count, epochs=d2v.epochs, report_delay=3)
    print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))
    if not autores:
        d2v.save(str(BASE_DIR / "FILES/modelos/modeloD2V.model"))
    else:
        d2v.save(str(BASE_DIR / "FILES/modelos/modeloD2V_autores.model"))
    print(d2v.wv.most_similar(['inteligencia']))
    global modelo
    modelo = d2v
    modelo.wv.init_sims()


def cargar_modelo():
    global modelo
    try:
        modelo = Doc2Vec.load(str(BASE_DIR / "FILES/modelos/modeloD2V_autores.model"))
        # modelo.wv.init_sims()
        return modelo
    except:
        return None

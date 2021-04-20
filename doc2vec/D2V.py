from gensim import utils
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import multiprocessing
from time import time
from main import BASE_DIR

from app.models import Investigacion


class ModeloD2V:
    # cores = multiprocessing.cpu_count()  # cuenta el nro de nucles de la pc
    d2v = Doc2Vec(vector_size=300,  # Dimensionalidad Palabras Vector
                  window=5,  # Contexto, distancia entre palabras predichas
                  min_count=1,  # Minimo de palabras a buscar
                  workers=multiprocessing.cpu_count(),  # En mi CPU
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

    def __init__(self, corpus=None):
        # Entrenamiento del modelo
        t = time()
        self.d2v.build_vocab(corpus,  # Oraciones nuevas
                             # update=True, #Agregar nuevo vocabulario
                             progress_per=100000  # Palabras para procesar con antecipacion
                             )  # prepare the model vocabulary
        print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))
        t = time()
        self.d2v.train(corpus, total_examples=self.d2v.corpus_count, epochs=self.d2v.epochs, report_delay=3)
        print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))


class Corpus(object):
    corpus_investigaciones = Investigacion.__get_corpus_lemas__()
    corpus_investigaciones = sorted(corpus_investigaciones, key=lambda item: item[0])

    def __iter__(self):
        for corpus in self.corpus_investigaciones:
            palabras = utils.simple_preprocess(corpus.corpus_lemas)
            yield TaggedDocument(palabras, [corpus.id, corpus.id_investigacion])

from .D2V import ModeloD2V, Corpus
from main import BASE_DIR
from gensim.models.doc2vec import Doc2Vec

modelo = None

def cargar_modelo():
    global modelo
    try:
        modelo = Doc2Vec.load(str(BASE_DIR / "FILES/modelos/modeloD2V.model"))
        modelo.wv.init_sims()
        return modelo
    except:
        return None


def entrenar_d2v():
    global modelo
    modelo = ModeloD2V(Corpus())
    modelo.d2v.save(str(BASE_DIR / "FILES/modelos/modeloD2V.model"))
    print(modelo.d2v.wv.most_similar(['inteligencia']))




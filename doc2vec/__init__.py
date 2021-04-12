from .D2V import ModeloD2V, Corpus
from main import BASE_DIR
from gensim.models.doc2vec import Doc2Vec


def entrenar_d2v():
    # modelo = ModeloD2V(Corpus())
    modelo = Doc2Vec.load(str(BASE_DIR / 'doc2vec/modeloD2V.model'))
    # modelo.d2v.save(str(BASE_DIR / "doc2vec/modeloD2V.model"))
    modelo.save(str(BASE_DIR / "doc2vec/modeloD2V.model"))
    # print(modelo.d2v.wv.most_similar(['inteligencia']))

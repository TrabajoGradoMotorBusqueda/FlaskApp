# Gensim
from gensim.models.doc2vec import Doc2Vec
from . import root_folder



class Models:

    modeloD2V = Doc2Vec.load(root_folder+'/modelos/d2v.model')

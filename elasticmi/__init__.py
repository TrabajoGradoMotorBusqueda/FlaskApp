from elasticsearch import Elasticsearch, RequestError
import numpy as np


class ElasticSearchEngine:

    def __init__(self):
        self.es = Elasticsearch()

    def crear_index_palabras(self):
        try:
            mapping_palabras = """
            {
                "mappings":{
                    "properties":{
                        "index":{"type": "integer"},
                        "palabra":{"type": "keyword"},
                        "vector":{
                            "type": "dense_vector",
                            "dims": 300
                        },
                        "norm_vec":{
                            "type": "dense_vector",
                            "dims": 300
                        }
                    }
                }
            }
            """
            # es.indices.delete(index='palabras')
            self.es.indices.create(body=mapping_palabras, index='palabras')
        except RequestError as e:
            print(e.error.lower())
            return None

    def creat_index_documentos(self):
        try:
            mapping_docs = """
            {
                "mappings":{
                    "properties":{
                        "tag":{"type": "integer"},
                        "vector":{
                            "type": "dense_vector",
                            "dims": 300
                        },
                        "norm_vec":{
                            "type": "dense_vector",
                            "dims": 300
                        }
                    }
                }
            }
            """
            # es.indices.delete(index='documentos')
            self.es.indices.create(body=mapping_docs, index='documentos')
        except RequestError as e:
            print(e.error.lower())
            return None

    def almacenar_palabras(self, modelo):
        for key, value in modelo.wv.vocab.items():
            index = value.index
            vector = modelo.wv.vectors[index]
            vector_norm = modelo.wv.vectors_norm[index]
            data = {
                "doc": {
                    "index": index,
                    "palabra": key,
                    "vector": vector,
                    "norm_vec": vector_norm
                }
            }

            self.es.index(index="palabras", body=data, id=index)
            self.es.update(index="palabras", body=data, id=index)

        print(self.es.count(index='palabras'))

    def almacenar_documentos(self, modelo):
        for i, (vector, vector_norm) in enumerate(zip(modelo.docvecs.vectors_docs,
                                                      modelo.docvecs.vectors_docs_norm)):
            data = {
                "tag": i + 1,
                "vector": vector,
                "norm_vec": vector_norm
            }

            self.es.index(index="documentos", body=data, id=i + 1)

        print(self.es.count(index='documentos'))

    def most_similar_words(self, palabras):
        # Construccion de Query
        keywords = []
        for word in palabras:
            term = {"term": {"palabra": ""}}
            term['term']['palabra'] = word
            keywords.append(term)

        # Vectores de las palabras clave
        query_vectores = {
            "query": {
                "bool": {
                    "should": keywords
                }
            },
            "_source": ["palabra", "norm_vec"]
        }
        vectores = self.es.search(index='palabras', body=query_vectores)['hits']['hits']
        norm_vectors = [vector['_source']['norm_vec'] for vector in vectores]
        vector_media = np.array(norm_vectors).mean(axis=0)
        vector_unitario = vector_media / np.linalg.norm(vector_media)

        # Most similar Words
        query_similares = {
            "query": {
                "script_score": {
                    "query": {
                        "match_all": {}
                    },
                    "script": {
                        "id": "dot_product",
                        "params": {
                            "query_vector": vector_unitario
                        }
                    }
                }
            },
            "size": 50,
            "_source": ["palabra", "index"]
        }
        palabras_similares_result = self.es.search(index='palabras', body=query_similares)['hits']['hits']
        palabras_similares = [palabra['_source']['palabra'] for palabra in palabras_similares_result]

        return palabras_similares

    def busqueda_d2v(self, vector_inferido, limite_documentos):
        vector_media_doc = np.array([vector_inferido]).mean(axis=0)
        vector_unitario = vector_media_doc / np.linalg.norm(vector_media_doc)

        query_sims_docs = {
            "query": {
                "script_score": {
                    "query": {
                        "match_all": {}
                    },
                    "script": {
                        "id": "dot_product",
                        "params": {
                            "query_vector": vector_unitario
                        }
                    }
                }
            },
            "size": limite_documentos,
            "_source": ["tag"]
        }

        documentos_similares = \
            self.es \
                .search(index='documentos', body=query_sims_docs)['hits']['hits']
        ranking_busqueda_id = [doc['_source']['tag'] for doc in documentos_similares]
        return ranking_busqueda_id

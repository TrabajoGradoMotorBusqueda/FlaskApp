from elasticsearch import Elasticsearch
import numpy as np


class ElasticSearchEngine:
    elasticsearch = Elasticsearch()

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
        vectores = self.elasticsearch.search(index='palabras', body=query_vectores)['hits']['hits']
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
            "size": 20,
            "_source": ["palabra", "index"]
        }
        palabras_similares_result = self.elasticsearch.search(index='palabras', body=query_similares)['hits']['hits']
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
            self.elasticsearch. \
            search(index='documentos', body=query_sims_docs)['hits']['hits']
        ranking_busqueda_id = [doc['_source']['tag'] for doc in documentos_similares]
        return ranking_busqueda_id

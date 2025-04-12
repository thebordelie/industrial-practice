from model.establishment import Establishment
from model.recommendation_strategy import Strategy
from repository.establishment_repository import DataProvider
from service.recommender_system import RecommenderSystem
import json
import math
import os
from collections import defaultdict

import torch
from transformers import AutoTokenizer, AutoModel
import requests
from opensearchpy import OpenSearch


class ContentBaseSystem(RecommenderSystem):
    def __init__(self, repository: DataProvider):
        super().__init__(Strategy.CONTENT_BASED, repository)
        self.client = Search()

    def get_recommendations(self, user_id: int, count_of_establishments: int) -> list[Establishment]:
        print(
            self.client.search_similar(70000001086985695)
        )
        return []

host = 'localhost'
port = 9200

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


# native opensearch rrf pipeline (works only with 60 constant
def create_search_pipeline():
    return requests.put(
        url='http://localhost:9200/_search/pipeline/rrf-pipeline',

        json={
            "description": "Post processor for hybrid RRF search",

            "phase_results_processors": [
                {
                    "score-ranker-processor": {
                        "combination": {
                            "technique": "rrf",
                            "rank_constant": 60
                        }
                    }
                }
            ]
        }
    )


def rrf_function(*list_of_list_ranks, rank_constant=60):
    """
    Merge ranks from multiple rankers.
    """

    rrf_map = defaultdict(float)

    for rank_list in list_of_list_ranks:
        for rank, item in enumerate(rank_list, 1):
            rrf_map[item] += 1 / (rank + rank_constant)

    sorted_items = sorted(rrf_map.items(), key=lambda x: x[1], reverse=True)

    return sorted_items[:5]


# coordinates distance to kilometers
def filter_distance(list, distance, source_item):
    result = [
        i for i in
        list['hits']['hits'] if
        ((float(i['_source']['coordinates'][0]) - float(source_item['coordinates'][0])) * 110.574) ** 2
        + ((float(i['_source']['coordinates'][1]) - float(source_item['coordinates'][1]))
           * 111.320 * math.cos(
                    (float(i['_source']['coordinates'][0]) + float(source_item['coordinates'][0])) / 2
                )
           ) ** 2 < distance ** 2
    ]

    return result


class Search:

    def __init__(self):

        self.client = OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_compress=True,  # enables gzip compression for request bodies
            use_ssl=False,
        )

        self.tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny2")
        self.model = AutoModel.from_pretrained("cointegrated/rubert-tiny2")

    def embed_bert_cls(self, text):
        t = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**{k: v.to(self.model.device) for k, v in t.items()})
        embeddings = model_output.last_hidden_state[:, 0, :]
        embeddings = torch.nn.functional.normalize(embeddings)
        return embeddings[0].cpu().numpy()

    def get_document_by_twogisitemid(self, twogisitemid: int):
        query = {
            "query": {
                "term": {
                    "twogisitemid": {
                        "value": twogisitemid
                    }
                }
            }
        }

        resp = self.client.search(body=query)

        return resp

    def semantic_search(self, source_item, size=1000):

        search_query = {
            "size": size,
            "_source": {
                "exclude": [
                    "embedding"
                ]
            },
            "query": {
                "bool": {
                    "should": {
                        "knn": {
                            "embedding": {
                                "vector": source_item['embedding'],
                                "k": 1000
                            }
                        }
                    },
                    "must_not": {
                        "term": {
                            "twogisitemid": {
                                "value": source_item['twogisitemid']
                            }
                        }
                    }
                }

            }
        }

        # print(search_query)

        results = self.client.search(index='practice-index', body=search_query)

        return results

    def fulltext_search(self, source_item, size=1000):

        search_query = {
            "size": size,
            "_source": {
                "exclude": [
                    "embedding"
                ]
            },
            "query": {

                "bool": {
                    "should": [
                        {
                            "match": {
                                "content": f"{c}"
                            }
                        } for c in source_item['content']
                    ],
                    "must_not": {
                        "term": {
                            "twogisitemid": {
                                "value": source_item['twogisitemid']
                            }
                        }
                    }
                }

            }
        }

        results = self.client.search(index='practice-index', body=search_query)

        return results

    def search_similar(self, twogisitemid: int):

        resp = self.get_document_by_twogisitemid(twogisitemid)

        source_item = resp['hits']['hits'][0]['_source']

        results_fulltext = filter_distance(
            self.fulltext_search(source_item),
            5,
            source_item
        )

        results_semantic = filter_distance(
            self.semantic_search(source_item),
            5,
            source_item
        )

        print(results_fulltext)
        print(results_semantic)

        return (
            rrf_function(
                [hit['_source']['twogisitemid'] for hit in results_fulltext],
                [hit['_source']['twogisitemid'] for hit in results_semantic],
            )
        )

    def create_index(self):

        self.client.indices.delete(
            index='practice-index',
            ignore_unavailable=True
        )

        self.client.indices.create(
            'practice-index',
            body={
                "settings": {

                    "index": {
                        "similarity": {
                            "custom_similarity": {
                                "type": "BM25",
                                "k1": 1.2,
                                "b": 0.75,
                            }
                        }
                    },

                    "index.knn": True,

                    "analysis": {

                        "filter": {
                            "russian_stop_filter": {
                                "type": "stop",
                                "stopwords": "_russian_"
                            },
                            "russian_stem_filter": {
                                "type": "stemmer",
                                "language": "russian"
                            },
                            "english_stop_filter": {
                                "type": "stop",
                                "stopwords": "_english_"
                            },
                            "english_stem_filter": {
                                "type": "stemmer",
                                "language": "english"
                            }
                        },

                        "analyzer": {

                            "default": {
                                "type": "custom",
                                "tokenizer": "standard",
                                "filter": [
                                    "lowercase",
                                    "russian_stop_filter",
                                    "russian_stem_filter"
                                ]
                            },

                            "default_en": {
                                "type": "custom",
                                "tokenizer": "standard",
                                "filter": [
                                    "lowercase",
                                    "english_stop_filter",
                                    "english_stem_filter"
                                ]
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "embedding": {
                            "type": "knn_vector",
                            "dimension": 312,
                            "space_type": "cosinesimil"
                        },
                        "coordinates": {
                            "type": "knn_vector",
                            "dimension": 2,
                            "space_type": "l2"
                        }
                    },
                    "dynamic_templates": [
                        {
                            "fields": {
                                "mapping": {
                                    "type": "text"
                                },
                                "match_mapping_type": "string",
                                "path_match": "*"
                            }
                        }
                    ]
                }
            }
        )

    def insert_documents(self, docs):

        bulk_operations = []

        batch_counter = 0

        for document in docs:
            batch_counter += 1

            bulk_operations.append('{ "create": {} }')

            new_document = {

                'embedding': (
                    self.embed_bert_cls(
                        f'{document['name']} {document['addressname']} '
                        f'{'; '.join([f'{key}: {', '.join(value)}'
                                      for key, value in document.items()
                                      if type(value) == list])}'
                    ).tolist()),

                'name': document['name'],
                'address': document['addressname'],
                'coordinates': list(map(float, document['coordinates'])),
                'twogisitemid': document['twogisitemid'],
                'content': [f'{key}: {', '.join(value)}'
                            for key, value in document.items()
                            if type(value) == list and key != 'coordinates']
            }

            bulk_operations.append(
                json.dumps(
                    new_document,
                    ensure_ascii=False
                )
            )

            if batch_counter % 100 == 0:
                bulk_operations.append('')

                self.client.bulk(index='practice-index', body='\n'.join(bulk_operations))
                # print(batch_counter)
                bulk_operations = []

        bulk_operations.append('')

        self.client.bulk(index='practice-index', body='\n'.join(bulk_operations))

    def insert_documents_from_df(self, df):

        data = json.loads(
            df[['course', 'skills']]
            .to_json(orient='records')
        )

        bulk_operations = []

        for document in data:
            bulk_operations.append('{ "create": {} }')
            document['embedding'] = (
                self.embed_bert_cls(
                    fr'{document['course']} {document['skills']}'
                ).tolist())

            document['name'] = document.pop('course')

            document['content'] = {
                'en': document['skills']
            }

            document.pop('skills')

            bulk_operations.append(
                json.dumps(
                    document,
                    ensure_ascii=False
                )
            )

        bulk_operations.append('')

        return self.client.bulk(index='practice-index', body='\n'.join(bulk_operations))

    def reindex(self):
        self.create_index()

        with open(
                f'{ROOT_DIR}/data/twogis/final_data.json', 'rt',
                encoding='utf-8'
        ) as f:
            documents = json.loads(f.read())

        self.insert_documents(documents)

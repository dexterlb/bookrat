from elasticsearch import Elasticsearch
from elasticsearch import helpers

class Search:
    def __init__(self):
        self.es = Elasticsearch()
        self.index = "books"
        self.type = "book"

    def delete(self):
        self.es.indices.delete(index=self.index, ignore=[400, 404])

    def create_action(self, book):
        return {
            "_index": self.index,
            "_type": self.type,
            "_id": book.book_id,
            "_source": {
                "words" : book.words
                }
            }

    def insert(self, books):
        self.delete()

        actions = map(self.create_action, books)
        print('Bulk insert')
        helpers.bulk(self.es, actions)

    def top_words(self, book_id):
        result = self.es.get(index=self.index, id=book_id)
        if result["found"]:
            return result['_source']['words']

    def search(self, keywords, exclude_ids=[]):
        hits = self.es.search(
            index=self.index,
            body={
                "query": {
                    "bool": {
                        "must": {
                            "match": {
                                "words": " ".join(keywords)
                            }
                        },
                        "must_not": {
                            "ids": {
                                "values": exclude_ids
                            }
                        }
                    }
                }
            }
        )["hits"]["hits"]

        return [
            {
                "id":hit["_id"] ,
                "score": hit["_score"],
                "matches": list(set(hit["_source"]["words"]) & set(keywords))
            } for hit in hits
        ]
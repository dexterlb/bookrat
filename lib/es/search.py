from elasticsearch import Elasticsearch
from elasticsearch import helpers

class Search:
    def __init__(self):
        self.es = Elasticsearch()
        self.index = "books"
        self.type = "book"

    def delete(self):
        self.es.delete(index=self.index)

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

        actions = map(create_action, books)
        print('Bulk insert')
        if len(actions) > 0:
            helpers.bulk(es, actions)

    def search(self, keywords):
        hits = self.es.search(
            index=self.index,
            body={
                "query": {
                    "match": {
                        "words": " ".join(keywords)
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
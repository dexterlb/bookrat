from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch()

actions = []

for j in range(0, 10):
    action = {
        "_index": "books",
        "_type": "book",
        "_id": j,
        "_source": {
            "words" : ["foo" + str(j), "bar", "baz"]
            }
        }

    actions.append(action)

if len(actions) > 0:
    helpers.bulk(es, actions)

es.search(index="books", body={"query": {"match": {"words": "foo1 bar"}}}))

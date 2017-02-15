import os, os.path
import random
import string
import json

import cherrypy


from . import get_pic
from .. import megatron



class Server(object):
    def __init__(self, db):
        super(Server, self).__init__()
        self.db = db
        self.megatron = megatron.Megatron(db)

    @cherrypy.expose
    def index(self):
        with open(os.path.join(
            os.path.abspath(os.path.dirname(os.path.realpath(__file__))),
            'web',
            'index.html'
            )) as f:

            return f.read()

    @cherrypy.expose
    def get_picture(self, url=""):
        return get_pic.base64_picture(url)


    def json_result(self, search_result):
        book = search_result.book
        score = search_result.num_matches
        return {"title": book.title, "author": book.author, "url": book.chitanka_id, "score": score}

    @cherrypy.expose
    def search(self, query):
        recommendations = self.megatron.search.search(query.split())
        responce = self.megatron.book_controller.recommendations_to_books(recommendations)
        return json.dumps(responce)

    @cherrypy.expose
    def search(self, query, is_keyword=False):
        if is_keyword and is_keyword == "true":
            return self.search_by_keywords(query)
        else:
            return self.search_by_book(query)


    def recommendation_to_book(self, recommendation):
        return {
            "score": recommendation.num_matches,
            "matches": recommendation.common_words[0:10],
        #    "top_words": recommendation.top_words,
            "title": recommendation.book.title,
            "author": recommendation.book.author,
            "url": recommendation.book.chitanka_id
        }

    def recommendations_to_books(self, recommendations):
        return [self.recommendation_to_book(r) for r in recommendations]


    def search_by_book(self, query):
        book = self.megatron.book_controller.search(query)

        if not book:
            return json.dumps({"book": {"title": None, "author": None, "url": None},
                "recommended":[]})

        print('found book: ' + book.title)

        recommendations = self.megatron.tf_idf_controller.recommendations(book.id)

        return json.dumps({"book": self.megatron.book_controller.json_book(book),
         "recommended":
            self.recommendations_to_books(recommendations)
        })

    def search_by_keywords(self, query):
        r = self.megatron.tf_idf_controller.keyword_recommendations(query.split())

        return json.dumps({
            "recommended":self.recommendations_to_books(r)
        })

def main(db):
    conf = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(
                os.path.abspath(os.path.dirname(os.path.realpath(__file__))),
                'web'
            )
        },
    }
    cherrypy.quickstart(Server(db), '/', conf)

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
        if is_keyword:
            return self.search_by_keywords(query)
        else:
            return self.search_by_book(query)

    def search_by_book(self, query):
        book = self.megatron.book_controller.search(query)

        if not book:
            return json.dumps({"book": {"title": None, "author": None, "url": None},
                "recommended":[]})

        print('found book: ' + book.title)

        top_words = self.megatron.search.top_words(book.id)

        r = self.megatron.search.search(top_words)

        return json.dumps({"book": self.megatron.book_controller.json_book(book),
         "recommended":self.megatron.book_controller.recommendations_to_books(r)})

    def search_by_keywords(self, query):
        r = self.megatron.search.search(query.split())

        return json.dumps({
            "recommended":self.megatron.book_controller.recommendations_to_books(r)
        })

    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']

    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']


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

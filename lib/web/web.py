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


    def json_book(self, book):
        return {"title": book.title, "author": book.author, "url": book.chitanka_id}

    def json_result(self, search_result):
        book = search_result.book
        score = search_result.num_matches
        return {"title": book.title, "author": book.author, "url": book.chitanka_id, "score": score}

    @cherrypy.expose
    def test(self, query):
        return json.dumps(self.megatron.search.search(query.split()))

    @cherrypy.expose
    def search(self, query):
        print('searching for ' + query)
        book = self.megatron.book_controller.search(query)
        if book:
            print('found book: ' + book.title)
            gs = list(self.megatron.tf_idf_controller.recommendations(book.id))
            return json.dumps({"book": self.json_book(book),
             "recommended":[self.json_result(b) for b in gs] })
        else:
            print('not found')
            return json.dumps({"book": {"title": None, "author": None, "url": None},
                "recommended":[]})

    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']

    @cherrypy.expose
    def search_keywords(self, query):
        gs = list(self.megatron.tf_idf_controller.keyword_recommendations(query))
        return json.dumps({"book": {"title": "-", "author": "-", "url": None},
            "recommended":[self.json_result(b) for b in gs] })

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

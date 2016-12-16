import os, os.path
import random
import string
import json

import cherrypy


from . import get_pic



class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head>
            <link href="/static/css/style.css" rel="stylesheet">
          </head>
          <body>
          wrong page
          </body>
        </html>"""

    @cherrypy.expose
    def get_picture(self, url=""):
        return get_pic.base64_picture(url)

    @cherrypy.expose
    def search(self, query):
        return json.dumps({"book": {"title":"Gs", "author":"Bash Gs"},
        "recommended":[{"title":"Gs1", "author":"Bash Gs1"}, {"title":"Gs2", "author":"Bash Gs2"}]})

    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(
                os.path.abspath(os.path.dirname(os.path.realpath(__file__))),
                'web'
            )
        },
    }
    cherrypy.quickstart(StringGenerator(), '/', conf)

from . import database
from .es import search

class Megatron:
    def __init__(self, url):
        self.database = database.Database(url)

        self.word_controller = database.WordController(self.database)
        self.book_controller = database.BookController(self.database)
        self.work_controller = database.WorkController(self.database)
        self.tf_idf_controller = database.TfIdfController(self.database)
        self.word_book_controller = database.WordBookController(self.database)
        self.search = search.Search()
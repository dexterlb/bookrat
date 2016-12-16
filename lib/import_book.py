from . import database
from . import parse_book
import os

class BookImporter:
    def __init__(self, megatron):
        self.megatron = megatron

    def _parse_from(self, dir):
        files = list(all_in_dir(dir))
        for file in files:
            book_parser = parse_book.BookParser(file)
            yield(book_parser.parse())

    def import_from(self, dir, progress=None):
        if progress:
            books = progress(self._parse_from(dir))
        else:
            books = self._parse_from(dir)
        self.megatron.book_controller.add_many(books)

def all_in_dir(dirname):
    for dirName, subdirList, fileList in os.walk(dirname):
        for fname in fileList:
            yield os.path.join(dirName, fname)
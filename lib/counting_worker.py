from threading import Thread
from queue import Queue
import time
import random
import os

from .stemmer import Stemmer, load_dictionary
from . import parse_text
from .stemmer.cache import LimitedCache
from . import database

class BookGetter(Thread):
    def __init__(self, input_books, megatron):
        super(BookGetter, self).__init__()
        self.input_books = input_books
        self.megatron = megatron

    def run(self):
        for book in self.megatron.work_controller.yield_book():
            self.input_books.put(book)
            print("+ Taking from databae: " + book.title)
        self.input_books.put(None)
        print("+ Took all.")

class WordCounter(Thread):
    def __init__(self, input_books, output_books, megatron):
        super(WordCounter, self).__init__()
        self.input_books, self.output_books = input_books, output_books
        self.megatron = megatron
        self.stemmer = Stemmer(
            rules_file=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'stemmer',
                'bulgarian_grammar.pl'  # TODO: make this configurable
            ),
            dictionary=load_dictionary(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'stemmer',
                    'bulgarian_words.json'  # TODO: this as well
                )
            ),
            cache=LimitedCache(limit=200000)
        )
        self.text_parser = parse_text.TextParser(self.stemmer)

    def run(self):
        book = self.input_books.get()
        while book:
            counted_words = self.text_parser.count_stemmed_words(book)
            self.output_books.put((book, counted_words))
            print("- Finished with book: " + book.title)
            book = self.input_books.get()
        self.output_books.put(None)

class ResultSetter(Thread):
    def __init__(self, output_books, megatron):
        super(ResultSetter, self).__init__()
        self.output_books = output_books
        self.megatron = megatron

    def yield_from_book(self, counted_book):
        book, words = counted_book
        for word, count in words.items():
            yield database.WordBook(book_id=book.id, word=word, count=count)


    def run(self):
        while True:
            counted_book = self.output_books.get()
            if counted_book:
                started = time.time()
                self.megatron.word_book_controller.add_many(
                    self.yield_from_book(counted_book)
                )
                print("pushed into db in: " + str(time.time() - started))
            else:
                break


def run(megatron):
    megatron.work_controller.update_ids()
    input_books = Queue(maxsize=1)
    output_books = Queue(maxsize=1)

    book_getter = BookGetter(input_books, megatron)
    word_counter = WordCounter(input_books, output_books, megatron)
    result_setter = ResultSetter(output_books, megatron)

    book_getter.start()
    result_setter.start()
    word_counter.run()

    book_getter.join()
    result_setter.join()

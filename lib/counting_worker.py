from threading import Thread
from queue import Queue
import time
import random
import os

from .stemmer import Stemmer
from . import parse_text

class BookGetter(Thread):
    def __init__(self, input_books, megatron):
        print("creating book getter")
        super(BookGetter, self).__init__()
        self.input_books = input_books
        self.megatron = megatron
        print("created book getter")

    def run(self):
        print("book getter started")
        for book in self.megatron.work_controller.yield_book():
            self.input_books.put(book)
            print("+ Taking from databae: " + book.title)
        self.input_books.put(None)
        print("+ Took all.")

class WordCounter(Thread):
    def __init__(self, input_books, output_books, megatron):
        print("creating word counter")
        super(WordCounter, self).__init__()
        self.input_books, self.output_books = input_books, output_books
        self.megatron = megatron
        self.stemmer = Stemmer(
            rules_file=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "stemmer",
                'bulgarian_grammar.pl'  # TODO: make this configurable
            ),
            dictionary=self.megatron.word_controller.get_all()
        )
        self.text_parser = parse_text.TextParser(self.stemmer)
        print("created word counter")

    def run(self):
        print("word counter started")

        book = self.input_books.get()
        while book:
            print("Word counter taking book")
            counted_words = self.text_parser.count_stemmed_words(book)
            self.output_books.put((book, counted_words))
            print("- Finished with book: " + book.title)
            book = self.input_books.get()
        self.output_books.put(None)
        print("- Finished with all")

class ResultSetter(Thread):
    def __init__(self, output_books, megatron):
        super(ResultSetter, self).__init__()
        self.output_books = output_books
        self.megatron = megatron

    def yield_from_book(self, counted_book):
        book, words = counted_book
        for word, count in words.items():
            yield WordBook(book_id=book.id, word=word, count=count)                


    def run(self):
        print("result setter started")

        while True:
            counted_book = self.output_books.get()
            if counted_book:
                self.megatron.word_book_controller.add_many(
                    self.yield_from_book(counted_book)
                )
                print("x Pushed into database: " + counted_book[0].title)
            else:
                break
            print("x Pushed all")



def run(megatron):
    megatron.work_controller.update_ids()
    print("updated ids")
    input_books = Queue(maxsize=1)
    output_books = Queue(maxsize=1)
    print("made queues")

    book_getter = BookGetter(input_books, megatron)
    word_counter = WordCounter(input_books, output_books, megatron)
    result_setter = ResultSetter(output_books, megatron)
    print("created workers")

    book_getter.start()
    word_counter.start()
    result_setter.start()

    book_getter.join()
    word_counter.join()
    result_setter.join()

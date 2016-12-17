from threading import Thread
from queue import Queue
import time
import random

from .stemmer import Stemmer

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
                'bulgarian_grammar.pl'  # TODO: make this configurable
            ),
            dictionary=self.megatron.word_controller.get_all()
        )


    def run(self):
        book = self.input_books.get()
        while book:
            time.sleep(random.randint(1, 10)/10)
            print("- Finished with: " + book.title)
            book = self.input_books.get()
        print("- Finished with all.")

class ResultSetter(Thread):
    def __init__(self, output_books, megatron):
        super(ResultSetter, self).__init__()
        self.output_books = output_books
        self.megatron = megatron

    def run(self):
        pass

def run(megatron):
    input_books = Queue(maxsize=1)
    output_books = Queue(maxsize=1)

    book_getter = BookGetter(input_books, megatron)
    word_counter = WordCounter(input_books, output_books, megatron)
    result_setter = ResultSetter(output_books, megatron)

    book_getter.start()
    word_counter.start()
    result_setter.start()

    book_getter.join()
    word_counter.join()
    result_setter.join()

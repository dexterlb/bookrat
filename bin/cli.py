import click
import sys
from ..lib import import_book
from ..lib import parse_dictionary
from ..lib import megatron
from ..lib import counting_worker
from ..lib import tf_idf
from ..lib.web import web
import progressbar
import os
from ..lib import parse_book

@click.group()
def main():
    pass

@click.command(help='import books from a folder')
@click.option('--db', help='database URN', required=True)
@click.argument('dir')
def import_books(db, dir):
    m = megatron.Megatron(db)
    importer = import_book.BookImporter(m)

    progress = progressbar.ProgressBar()
    importer.import_from(dir, progress)

@click.command(help='import books from a folder')
@click.option('--db', help='database URN', required=True)
@click.argument('book_id', required=False)
def count(db, book_id):
    if book_id == 'none':
        book_id = None
    m = megatron.Megatron(db)
    counting_worker.run(m, book_id)


@click.command(help='import words from json dictionary file')
@click.option('--db', help='database URN', required=True)
@click.argument('dict')
def parse_dict(db, dict):
	m = megatron.Megatron(db)
	parser = parse_dictionary.DictionaryParser(m)
	parser.parse_dictionary_from(dict)



@click.command(help='create the database')
@click.option('--db', help='database URN', required=True)
def createdb(db):
    m = megatron.Megatron(db)
    m.database.create_database()
    click.echo('Created the database')

@click.command(help='drop the database')
@click.option('--db', help='database URN', required=True)
def dropdb(db):
    m = megatron.Megatron(db)
    m.database.drop_all()
    click.echo('Dropped the database')

@click.command(help='compute idf')
@click.option('--db', help='database URN', required=True)
def idf(db):
    m = megatron.Megatron(db)
    tfidf = tf_idf.TFIDF(m)
    tfidf.compute_idf()

@click.command(help='compute idf')
@click.option('--db', help='database URN', required=True)
def tfidf(db):
    m = megatron.Megatron(db)
    tfidf = tf_idf.TFIDF(m)
    tfidf.compute_tfidf()

@click.command(help='compute idf')
@click.option('--db', help='database URN', required=True)
def top(db):
    m = megatron.Megatron(db)
    tfidf = tf_idf.TFIDF(m)
    tfidf.compute_top_words()

@click.command(help='precompute all the info')
@click.option('--db', help='database URN', required=True)
@click.argument('dir')
def precompute(db, dir):
    m = megatron.Megatron(db)
    m.database.drop_all()
    m.database.create_database()

    importer = import_book.BookImporter(m)
    progress = progressbar.ProgressBar()
    importer.import_from(dir, progress)

    counting_worker.run(m)

    tfidf = tf_idf.TFIDF(m)
    tfidf.compute_idf()

    tfidf.compute_tfidf()

    tfidf.compute_top_words()


@click.command(help='precompute just one book')
@click.option('--db', help='database URN', required=True)
@click.argument('book_url')
def precompute_one(db, book_url):
    m = megatron.Megatron(db)

    book_parser = parse_book.BookParser(book_url)
    book = book_parser.parse()
    book_id = m.book_controller.add_one(book)

    counting_worker.run(m, book_id)

    tfidf = tf_idf.TFIDF(m)

    tfidf.compute_idf()

    tfidf.compute_tfidf()

    tfidf.compute_top_words()

@click.command(help='get recommendations for a book_id')
@click.option('--db', help='database URN', required=True)
@click.argument('book_id', required=True)
def recommend_by_id(db, book_id):
    m = megatron.Megatron(db)
    print(str(list(m.tf_idf_controller.recommendations(int(book_id)))))

@click.command(help='get recommendations for a book')
@click.option('--db', help='database URN', required=True)
@click.argument('title', required=True)
def recommend(db, title):
    m = megatron.Megatron(db)
    book = m.book_controller.search(title)
    if book:
        print("book: " + book.title + " recommendations: " + str(list(m.tf_idf_controller.recommendations(book.id))))
    else:
        return None

@click.command(help='get recommendations for a book')
@click.option('--db', help='database URN', required=True)
@click.argument('keywords', required=True)
def keyword_recommend(db, keywords):
    m = megatron.Megatron(db)
    print(" recommendations: " + str(list(m.tf_idf_controller.keyword_recommendation(keywords))))

@click.command(help='return book by title')
@click.option('--db', help='database URN', required=True)
@click.argument('title', required=True)
def search(db, title):
    m = megatron.Megatron(db)
    print(m.book_controller.search(title))



@click.command(help='serve the server')
@click.option('--db', help='database URN', required=True)
def serve(db):
    web.main(db)



main.add_command(import_books)
main.add_command(parse_dict)
main.add_command(createdb)
main.add_command(dropdb)
main.add_command(count)
main.add_command(idf)
main.add_command(tfidf)
main.add_command(top)
main.add_command(precompute)
main.add_command(precompute_one)
main.add_command(serve)
main.add_command(recommend)
main.add_command(keyword_recommend)
main.add_command(recommend_by_id)
main.add_command(search)

if __name__ == '__main__':
    main()

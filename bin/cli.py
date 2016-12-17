import click
import sys
from ..lib import import_book
from ..lib import parse_dictionary
from ..lib import megatron
from ..lib import counting_worker
from ..lib import tf_idf
import progressbar

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
def count(db):
    m = megatron.Megatron(db)
    counting_worker.run(m)


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


main.add_command(import_books)
main.add_command(parse_dict)
main.add_command(createdb)
main.add_command(dropdb)
main.add_command(count)
main.add_command(idf)
main.add_command(tfidf)
main.add_command(top)

if __name__ == '__main__':
    main()

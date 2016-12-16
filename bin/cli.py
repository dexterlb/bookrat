import click
import sys
from ..lib import import_book
from ..lib import database
import progressbar

@click.group()
def main():
    pass

@click.command(help='import books from a folder')
@click.option('--db', help='database URN', required=True)
@click.argument('dir')
def import_books(db, dir):
    db = database.Database(db)
    db.create_database()
    importer = import_book.BookImporter(db)

    progress = progressbar.ProgressBar()
    importer.import_from(dir, progress)

@click.command(help='create the database')
@click.option('--db', help='database URN', required=True)
def createdb():
    click.echo('Dropped the database')

@click.command(help='drop the database')
@click.option('--db', help='database URN', required=True)
def dropdb():
    click.echo('Dropped the database')

main.add_command(import_books)
main.add_command(createdb)
main.add_command(dropdb)

if __name__ == '__main__':
    main()

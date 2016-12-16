import sys
from ..lib import import_book
from ..lib import database
import progressbar

def mаin():
	dir = sys.argv[1]
	db = database.Database("postgres://do@localhost/book-rat-test")
	db.create_database()
	importer = import_book.BookImporter(db)
	
	progress = progressbar.ProgressBar()
	importer.import_from(dir, progress)

if __name__ == '__main__':
	mаin()
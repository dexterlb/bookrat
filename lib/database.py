import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, Numeric, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class Database:
    def __init__(self, url):
        self.engine = create_engine(url)
        self.make_session = sessionmaker()
        self.make_session.configure(bind=self.engine)
        
    def create_database(self):
        Base.metadata.create_all(self.engine)

    def drop_all(self):
        Base.metadata.drop_all(self.engine)

class Controller:
    def __init__(self, database):
        self.database = database

    def make_session(self):
        return self.database.make_session()

    def add_one(self, item):
        session = self.database.make_session()
        session.add(item)
        session.commit()

    def add_many(self, items):
        session = self.database.make_session()
        session.add_all(items)
        session.commit()


class WordController(Controller):
    def get_all(self):
        words = []
        session = self.make_session()
        for word in session.query(Word).all():
            words.append(word)
        session.commit()
        return words

class WorkController(Controller):
    def update_ids(self):
        self.database.engine.execute(
            '''
            insert into work(book_id, taken, finished)
            select id, false, false from book
            where id not in (select book_id from work);
            '''
        )

    def get_all(self):
        works = []
        session = self.make_session()
        for work in session.query(Work).all():
            works.append(work)
        session.commit()
        return works


    def yield_book(self):
        while True:
            book = self.lock_book()
            if book:
                yield book
            else:
                break

    def lock_book(self):
        print("trying to take book")
        record = self.database.engine.execute(
            '''
            update work set taken=true
            where book_id = (
                select book_id from work
                where bool(taken) = false
                order by random() limit 1
            )
            returning book_id;
            '''
        ).first()
        print("took book")
        if record:
            book_id = record[0]
            session = self.make_session()
            book = session.query(Book).filter(Book.id == book_id).first()
            return book
        else:
            return None


class BookController(Controller):
    def get_all(self):
        books = []
        session = self.make_session()
        for book in session.query(Book).all():
            books.append(book)
        session.commit()
        return books

class WordBookController(Controller):
    def add(self, word, book_id):
        session = self.make_session()
        counters = session.query(WordBook).filter(WordBook.book_id == book_id, WordBook.word_id == word_id).all()
        if len(counters) > 1:
            print("Too many")
        if len(counters) == 0:
            session.add(WordBook(word = word, book_id=book_id, count=1))
        else:
            counters[0].count += 1        
        session.commit()

    def get_all(self):
        counters = []
        session = self.make_session()
        for counter in session.query(WordBook).all():
            counters.append(counter)
        session.commit()
        return counters

class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    type = Column(String)
    from_dictionary = Column(Boolean)
    def __repr__(self):
       return "<Word(id='%s', text='%s', type='%s', from_dictionary='%s')>" % (
                            self.id, self.text, self.type, self.from_dictionary)

class Work(Base):
    __tablename__ = 'work'
    book_id = Column(Integer, primary_key=True)
    taken = Column(Boolean)
    finished = Column(Boolean)
    def __repr__(self):
       return "<Work(book_id='%s', taken='%s', finished='%s')>" % (
                            self.book_id, self.taken, self.finished)


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)
    text = Column(Text)
    chitanka_id = Column(String)

    def __repr__(self):
        return "<Book(id='%s', title='%s', author='%s', year='%s', chitanka_id='%s')>" % (
                            self.id, self.title, self.author, self.year, self.chitanka_id)


class WordBook(Base):
    __tablename__ = 'wordbook'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    word = Column(String, nullable=False)
    count = Column(Integer)
    def __repr__(self):
        return "<WordBook(book_id='%s', word='%s', count='%s')>" % (
                            self.book_id, self.word, self.count)

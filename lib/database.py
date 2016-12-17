import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, Float, ForeignKey, Text, ARRAY
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

class TfIdfController(Controller):
    def compute_idf(self):
        self.database.engine.execute(
            '''
            insert into idf(word, idf_score)
            select word, log(1 + (select count(*) from book) :: float / count(book_id)) as idf_score
            from wordbook group by word;
            '''
        )

    def compute_tfidf(self):
        self.database.engine.execute(
            '''
            insert into tfidf(book_id, word, tfidf_score)
            select book_id, wordbook.word as word,
            ((0.5 + 0.5 * (count :: float / t.mc)) * (idf.idf_score) ) as tfidf_score
            from wordbook
            join 
                (select book_id as bid, max(count) as mc
                 from wordbook group by book_id
                ) as t on t.bid = book_id
            join idf on wordbook.word = idf.word;
            '''
        )

    def compute_top_words(self):
        self.database.engine.execute(
            '''
            insert into topwords(book_id, words)  
            select b.id as book_id,
            array(select word from tfidf where book_id = b.id
            order by tfidf_score desc limit 10) as words from book as b;
            '''
        )

class WordBookController(Controller):
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
    taken = Column(Boolean, index=True)
    finished = Column(Boolean, index=True)
    def __repr__(self):
       return "<Work(book_id='%s', taken='%s', finished='%s')>" % (
                            self.book_id, self.taken, self.finished)

class Idf(Base):
    __tablename__ = 'idf'
    word = Column(String, primary_key=True)
    idf_score = Column(Float)
    def __repr__(self):
       return "<idf(word='%s', idf_score='%s')>" % (
        self.word, self.idf_score)

class Tfidf(Base):
    __tablename__ = 'tfidf'
    book_id = Column(Integer, primary_key=True, index=True)
    word = Column(String, primary_key=True, index=True)
    tfidf_score = Column(Float, index=True)
    def __repr__(self):
       return "<tfidf(book_id='%s', word='%s', tfidf_score='%s')>" % (
        self.book_id, self.word, self.tfidf_score)

class TopWords(Base):
    __tablename__ = 'topwords'
    book_id = Column(Integer, primary_key=True)
    words = Column(ARRAY(String))
    def __repr__(self):
       return "<topwords(book_id='%s', words='%s' )>" % (
        self.book_id, self.word, self.tfidf_score)


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
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False, index=True)
    word = Column(String, nullable=False, index=True)
    count = Column(Integer)
    def __repr__(self):
        return "<WordBook(book_id='%s', word='%s', count='%s')>" % (
                            self.book_id, self.word, self.count)



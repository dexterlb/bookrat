import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, Float, ForeignKey, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import psycopg2

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
        print(item.id)
        return item.id

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
        try:
            self.database.engine.execute(
                '''
                insert into work(book_id, taken, finished)
                select id, false, false from book
                where id not in (select book_id from work);
                '''
            )
        except:
            print('warning: race condition in update_ids. Probably harmless.')
            pass

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

    def get_by_id(self, book_id):
        record = self.database.engine.execute(
        '''
            update work set taken=true
            where book_id = {} returning book_id;'''.format(book_id)
        ).first()

        if record:
            book_id = record[0]
            session = self.make_session()
            book = session.query(Book).filter(Book.id == book_id).first()
            return book
        else:
            return None

        book = session.query(Book).filter(Book.id == book_id).first()

class BookController(Controller):
    def get_all(self):
        books = []
        session = self.make_session()
        for book in session.query(Book).all():
            books.append(book)
        session.commit()
        return books

    def search(self, query):
        keywords = query.split()
        session = self.make_session()

        query_obj = session.query(Book)
        for k in keywords:
            query_obj = query_obj.filter(Book.title.like('%{0}%'.format(k)))

        book = query_obj.first()

        session.commit()

        return book


class TfIdfController(Controller):
    def create_tables(self):
        Idf.__table__.create(self.database.engine)
        Tfidf.__table__.create(self.database.engine)
        TopWords.__table__.create(self.database.engine)
        TopBookWordCount.__table__.create(self.database.engine)


    def drop_tables(self):
        Idf.__table__.drop(self.database.engine)
        Tfidf.__table__.drop(self.database.engine)
        TopWords.__table__.drop(self.database.engine)
        TopBookWordCount.__table__.drop(self.database.engine)

    def compute_idf(self):
        self.database.engine.execute(
            '''
            insert into idf(word, idf_score)
            select word, log(1 + (select count(*) from book) :: float / count(book_id)) as idf_score
            from wordbook group by word;
            '''
        )

    def compute_tfidf(self):
        Tfidf.__table__.drop(self.database.engine)
        self.database.engine.execute(
            '''
            create table tfidf(book_id, word, tfidf_score) as
            select w.book_id, w.word as word,
                ((0.5 + 0.5 * (count :: float / t.top_count)) * (idf.idf_score) ) as tfidf_score
            from wordbook w
            join topbookwordcount t
            on t.book_id = w.book_id
            join idf on w.word = idf.word
            with data;
            '''
        )

    def add_idf_indices(self):
        self.database.engine.execute(
            '''
            create index idf_word on idf(word);
            create index top_book_word_count_book_id on topbookwordcount(book_id);
            '''
        )

    def add_tfidf_indices(self):
         self.database.engine.execute(
            '''
            create index tfidf_book_id_index on tfidf(book_id);
            create index tfidf_word_index on tfidf(word);
            create index tfidf_score_index on tfidf(tfidf_score);
            '''
    )

    def compute_top_words(self):
        self.database.engine.execute(
            '''
            create table topwords(book_id, words) as
            select b.id as book_id,
            array(select word from tfidf where book_id = b.id
            order by tfidf_score desc limit 100) as words from book as b
            with data;
            '''
        )

    def compute_top_book_word_count(self):
        TopBookWordCount.__table__.drop(self.engine)
        self.database.engine.execute(
            '''
            create table topbookwordcount(book_id, top_count) as
            select book.id, max_term.count from book
            join lateral (
                select book_id, count
                from wordbook where book_id = book.id
                order by count desc limit 1
            ) as max_term on true
            with data;
            '''
        )

    def recommendations(self, book_id):
        session = self.make_session()
        top = session.query(TopWords).filter(TopWords.book_id == book_id).first()
        words = top.words

        results = session.execute(
            '''
            select f.book_id, (select count(*) from unnest(f.words) u(w) where u.w = any (:words :: varchar[])) as number
            from topwords f
            where f.book_id != :id and f.words && (:words :: varchar[])
            order by number desc limit 5;
            ''',
            {
                'id': book_id,
                'words': words
            }
        )

        for result in results:
            book = session.query(Book).filter(Book.id == result[0]).first()
            yield SearchResult(book, int(result[1]))

        session.commit()

class SearchResult:
    def __init__(self, book, matches):
        self.book = book
        self.matches = matches

    def __repr__(self):
        return self.book.title + ' [' + str(self.matches) + ']'

class WordBookController(Controller):
    def get_all(self):
        counters = []
        session = self.make_session()
        for counter in session.query(WordBook).all():
            counters.append(counter)
        session.commit()
        return counters

    def add_indices(self):
        self.database.engine.execute(
            '''
            create index book_id_index on wordbook(book_id);
            create index word_index on wordbook(word);
            '''
        )

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

class Idf(Base):
    __tablename__ = 'idf'
    word = Column(String, primary_key=True)
    idf_score = Column(Float)
    def __repr__(self):
       return "<idf(word='%s', idf_score='%s')>" % (
        self.word, self.idf_score)

class Tfidf(Base):
    __tablename__ = 'tfidf'
    book_id = Column(Integer, primary_key=True)
    word = Column(String, primary_key=True)
    tfidf_score = Column(Float)
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

class TopBookWordCount(Base):
    __tablename__ = 'topbookwordcount'
    book_id = Column(Integer, primary_key=True)
    top_count = Column(Integer)
    def __repr__(self):
       return "<topbookwordcount(book_id='%s', top_count='%s' )>" % (
        self.book_id, self.top_count)

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



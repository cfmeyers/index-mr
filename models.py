#http://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine 

Base = declarative_base()

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    url = Column(String(250))
    author = Column(String(250))
    title = Column(String(250))
    date = Column(Date)

class Link(Base):
    __tablename__ = 'link'

    id = Column(Integer, primary_key=True)
    href = Column(String(250))
    amazon = Column(Boolean)

    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship(Post, backref='links')

    book = relationship('Book', uselist=False, backref='link')

class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    author = Column(String(250))
    image_url = Column(String(250))

    link_id = Column(Integer, ForeignKey('link.id'))

class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    browse_node_id = Column(String(250))

    book_id = Column(Integer, ForeignKey('book.id'))
    book = relationship(Book, backref='genres')




engine = create_engine('sqlite:///mr_posts.db')
 
# Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
Base.metadata.create_all(engine)

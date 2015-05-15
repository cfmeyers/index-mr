from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Post, Link, Base
# from sqlalchemy_declarative import Post, Link

engine = create_engine('sqlite:///mr_posts.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

new_post = Post(text='hello world', url='www.google.com', author='steve', date=date.today())
session.add(new_post)
session.commit()

new_link1 = Link(href='bob.com', amazon=False)
new_link1.post = new_post
new_link2 = Link(href='amazon.com', amazon=True)
new_link2.post = new_post

session.add_all([new_link1, new_link2])
session.commit()


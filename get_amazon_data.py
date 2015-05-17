import os, re
from amazon.api import AmazonAPI

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Post, Link, Book, Genre, Base

def connect_to_db(db_address):
    engine = create_engine(db_address)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

session = connect_to_db('sqlite:///mr_posts.db')
amazon_links = session.query(Link).filter(Link.amazon == True).all()
# has_asins = [href for href in hrefs if re.search(r"[\dA-Z]{10}",href) ]

AMAZON_ACCESS_KEY = os.environ['AMAZON_ACCESS_KEY']
AMAZON_SECRET_KEY = os.environ['AMAZON_SECRET_KEY']
AMAZON_ASSOC_TAG = os.environ['AMAZON_ASSOC_TAG']

amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)
for link in amazon_links[:8]:
    if re.search(r"[\dA-Z]{10}", link.href):
        asin = re.search(r"[\dA-Z]{10}", link.href).group()
        product = amazon.lookup(ItemId=asin)
        # print product.title
        # print product.author
        # print product.medium_image_url
        # print product.get_attribute('ProductGroup') #e.g. Book, DVD, etc

        for node in product.browse_nodes:
            if session.query(Genre).filter(Genre.browse_node_id==node.id).first():
                genre = session.query(Genre).filter(Genre.browse_node_id==node.id).first()
            else:
                genre = Genre(name=node.name, browse_node_id=node.id)

            print node.name
            print node.id



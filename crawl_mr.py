from datetime import date, datetime
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Post, Link, Book, Genre, Base

from bs4 import BeautifulSoup
import urllib2

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def download_page(url, hdr):
    req = urllib2.Request(url, headers=hdr)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page.read())
    return soup

def connect_to_db(db_address):
    engine = create_engine(db_address)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

def get_content(soup):
    content = soup.find("div", {"class": "format_text entry-content"})
    content.findAll('p')[-1].extract() #get rid of final comments paragraph
    return content

def get_date(soup):
    headline_text = soup.find('div', {'class':'headline_area'}).p.text
    date_string = headline_text.split(' on ')[1].split('at')[0].strip()
    post_date = datetime.strptime(date_string,'%B %d, %Y' ).date()
    return post_date

def get_links(content, post):
    new_links = []

    for link in content.findAll('a'):
        if link.get('href'):
            href = link.get('href').strip()
            isAmazon = 'amazon' in href
            new_link = Link(href=href, amazon=isAmazon)
            new_link.post = post
            new_links.append(new_link)

    return new_links






session = connect_to_db('sqlite:///mr_posts.db')


count = 0

# url = 'http://marginalrevolution.com/marginalrevolution/2013/10/cohorts-born-in-the-late-1930s-and-40s-did-especially-well.html'
url = 'http://marginalrevolution.com/marginalrevolution/2013/11/boonton-defends-aca.html'


while url:
    time.sleep(3)
    try:
        soup = download_page(url, hdr)
        url = ''
    except:
        print 'failed to download:', url

    try:
        url = soup.find('a', {'rel':'next'})['href']
    except:
        print 'failed to get next url for:', url

    try:
        content = get_content(soup)
    except:
        print 'failed to get content for:', url

    try:
        title = soup.find('h1', {'class': 'entry-title'}).text
        author = soup.find('a', {'rel':'author'}).text
        post_date = get_date(soup)
    except:
        print 'failed to get title, author, or post_date for:', url

    try:
        new_post = Post(text=content.text.strip(), url=url, title=title, author=author, date=post_date)
        session.add(new_post)

    except:
        print 'failed to build new post for:', url

    try:
        new_links = get_links(content, new_post)
        session.add_all(new_links)
    except:
        print 'failed to get links for:', url

    session.commit()

    count += 1
    if count%50==0: print count, post_date
    




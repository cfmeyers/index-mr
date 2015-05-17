from datetime import date, datetime
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Post, Link, Book, Genre, Base

from bs4 import BeautifulSoup
import urllib2

engine = create_engine('sqlite:///mr_posts.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

count = 0

with open('failed4.txt') as f:
    rows = f.readlines()
    for row in rows:
        count += 1
        time.sleep(3)
        url = row.strip()
        try:
            req = urllib2.Request(url, headers=hdr)
            page = urllib2.urlopen(req)
            soup = BeautifulSoup(page.read())

            content = soup.find("div", {"class": "format_text entry-content"})
            content.findAll('p')[-1].extract() #get rid of final comments paragraph

            title = soup.find('h1', {'class': 'entry-title'}).text
            author = soup.find('a', {'rel':'author'}).text

            #get the date
            headline_text = soup.find('div', {'class':'headline_area'}).p.text
            date_string = headline_text.split(' on ')[1].split('at')[0].strip()
            post_date = datetime.strptime(date_string,'%B %d, %Y' ).date()


            new_post = Post(text=content.text.strip(), url=url, title=title, author=author, date=post_date)
            session.add(new_post)

            for link in content.findAll('a'):
                if link.get('href'):
                    href = link.get('href').strip()
                    isAmazon = 'amazon' in href
                    new_link = Link(href=href, amazon=isAmazon)
                    new_link.post = new_post
                    session.add(new_link)


            session.commit()
            if count%100==0:
                print count, date_string
        except:
            print 'failed:', url




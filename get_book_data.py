#!/usr/bin/env python3
""" get_book_data.py

    Usage:
        ./get_book_data.py

    This script is me learning how to extract books-read information from
    goodreads. This is intended to be used in a book visualization project I'm
    working on with Giulia.
"""

# TODO
#  * Parse the date string we receive for date added.
#  * Perform extra requests to get the genres for these books; ensure cached.
#  * Save parsed data out to a nice json file.
#  * Do this for several users so we have different data points.

# ______________________________________________________________________
# Imports

import base64
import re
import warnings
from pathlib import Path
from urllib import request

import bs4 as bs


# ______________________________________________________________________
# Globals

test_url_1 = 'https://www.goodreads.com/review/list_rss/3534041?shelf=read'


# ______________________________________________________________________
# Classes

class Book:
    pass


# ______________________________________________________________________
# Functions

def get_w_cache(url):
    fname = Path('cache/' + base64.b32encode(url.encode()).decode())
    if fname.is_file():
        with fname.open() as f:
            return f.read()
    with request.urlopen(url) as f:
        data = f.read()
    with fname.open('wb') as f:
        f.write(data)
    return data

def ensure_no_cdata_wrapper(s):
    return re.sub(r'.*CDATA\[([^]]*)\]\]>', r'\1', s)

def parse_out_book_data(rss_xml):
    book_data = []
    soup = bs.BeautifulSoup(rss_xml, 'html.parser')
    for item in soup.find_all('item'):
        book = Book()

        book.title      = ensure_no_cdata_wrapper(item.title.contents[0])
        book.author     = item.author_name.get_text()
        book.id         = int(item.book_id.get_text())
        book.num_pages  = int(item.book.num_pages.get_text())

        raw_date_str    = item.user_date_added.get_text()
        book.date_added = ensure_no_cdata_wrapper(raw_date_str)

        book_data.append(book)
    return book_data

def print_book_data(book_data):
    for book in book_data:
        print('\n' + '_' * 70)
        print(f'id:{book.id:10d} {book.title} by {book.author}')
        print(f'{book.num_pages} pages')
        print(f'Added {book.date_added}')


# ______________________________________________________________________
# Main

warnings.filterwarnings(action='ignore', category=bs.XMLParsedAsHTMLWarning)

rss_xml = get_w_cache(test_url_1)
book_data = parse_out_book_data(rss_xml)
print_book_data(book_data)

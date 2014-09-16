'''
bootstrapify
===================================
This plugin modifies article and page html to use bootstrap classes, i.e tables (and later more)
'''

from pelican import signals, contents
from bs4 import BeautifulSoup
import re

def replace_tables(soup, attributes=['table',' table-striped', 'table-hover']):
    for tbl in soup.findAll('table'):
        tbl.attrs['class'] = list(set(tbl.attrs.get('class', []) + attributes))
        print(repr(tbl.attrs.get('class')))

def replace_images(soup, attributes=['img-responsive']):
    for img in soup.findAll('img'):
        img.attrs['class'] = list(set(img.attrs.get('class', []) + attributes))


def bootstrapify(content):
    if isinstance(content, contents.Static):
        return

    soup = BeautifulSoup(content._content)
    replace_tables(soup)
    replace_images(soup)


    content._content = soup.decode()#prettify?

def register():
    signals.content_object_init.connect(bootstrapify)

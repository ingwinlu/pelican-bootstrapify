'''
bootstrapify
===================================
This pelican plugin modifies article and page html to use bootstrap's default classes. This is especially handy if you want to write tables in markdown, since the attr_list extension does not play nice with tables
'''

from pelican import signals, contents
from bs4 import BeautifulSoup

def replace(searchterm, soup, attributes):
    for item in soup.findAll(searchterm):
        item.attrs['class'] = list(set(item.attrs.get('class', []) + attributes))

def replace_tables(soup, attributes=['table',' table-striped', 'table-hover']):
    replace('table', soup, attributes)

def replace_images(soup, attributes=['img-responsive']):
    replace('img', soup, attributes)


def bootstrapify(content):
    if isinstance(content, contents.Static):
        return

    soup = BeautifulSoup(content._content, 'html.parser')
    replace_tables(soup)
    replace_images(soup)

    content._content = soup.decode()

def register():
    signals.content_object_init.connect(bootstrapify)

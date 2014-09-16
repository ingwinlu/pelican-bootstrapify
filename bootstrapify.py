'''
bootstrapify
===================================
This plugin modifies article and page html to use bootstrap classes, i.e tables (and later more)
'''

from pelican import signals, contents
from bs4 import BeautifulSoup
import re

def bootstrapify(content):
    #dropout if contents.static
    if isinstance(content, contents.Static):
        return

    soup = BeautifulSoup(content._content)
    for header in soup.findAll(re.compile("^h\d")):
        toc = toc + [header.prettify(formatter="html")]

    content.toc = toc


def register():
    signals.content_object_init.connect(bootstrapify)

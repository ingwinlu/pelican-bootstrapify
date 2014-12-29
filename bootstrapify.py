'''
bootstrapify
===================================
This pelican plugin adds css classes to nonstatic html output.

This is especially useful if you want to use bootstrap and want
to add its default classes to your tables and images.
'''

from bs4 import BeautifulSoup
from pelican import signals, contents


def replace(searchterm, soup, attributes):
    for item in soup.select(searchterm):
        attribute_set = set(item.attrs.get('class', []) + attributes)
        item.attrs['class'] = list(attribute_set)


def bootstrapify(content):
    if isinstance(content, contents.Static):
        return

    # Define default behavior for backward compatibility
    default_options = {
            'table': ['table', 'table-striped', 'table-hover'],
            'img': ['img-responsive']
        }

    soup = BeautifulSoup(content._content, 'html.parser')

    # Retrieve bootstrapify settings
    replacements = content.settings.get('BOOTSTRAPIFY', default_options)

    for selector, classes in replacements.items():
        replace(selector, soup, classes)

    content._content = soup.decode()


def register():
    signals.content_object_init.connect(bootstrapify)

'''
bootstrapify
===================================
This pelican plugin modifies article and page html to use bootstrap's default
classes. This is especially handy if you want to write tables in markdown,
since the attr_list extension does not play nice with tables.
'''

from bs4 import BeautifulSoup
from pelican import signals, contents


def replace(searchterm, soup, attributes):
    for item in soup.select(searchterm):
        item.attrs['class'] = list(set(item.attrs.get('class', []) +
                                       attributes))


def bootstrapify(content):
    if isinstance(content, contents.Static):
        return

    # Define default behavior for backward compatibility
    default = {'table': ['table', 'table-striped', 'table-hover'],
               'img': ['img-responsive']}

    soup = BeautifulSoup(content._content, 'html.parser')

    # Retrieve bootstrapify settings
    replacements = content.settings.get('BOOTSTRAPIFY', default)

    for selector, classes in replacements.items():
        replace(selector, soup, classes)

    content._content = soup.decode()


def register():
    signals.content_object_init.connect(bootstrapify)

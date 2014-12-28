# -*- coding: utf-8 -*-
"""
bootstrapify test
=================
Unit test for the bootstrapify plugin
"""

from __future__ import unicode_literals

import unittest

from bs4 import BeautifulSoup

from pelican.contents import Page, Static
from pelican.tests.support import get_settings

from bootstrapify import bootstrapify


class TestBootstrapify(unittest.TestCase):
    def test_default(self):
        html_doc = """
        <html><body>
        <p></p>
        <a href=""></a>
        <table></table>
        <img href="">
        </body></html>
        """

        content = Page(content=html_doc, settings=get_settings())
        bootstrapify(content)

        soup = BeautifulSoup(content._content, 'html.parser')

        self.assertItemsEqual(soup.select('table')[0].attrs['class'],
                              ['table', 'table-striped', 'table-hover'])
        self.assertItemsEqual(soup.select('img')[0].attrs['class'],
                              ['img-responsive'])
        self.assertEqual(soup.select('p')[0].attrs.keys(), [])
        self.assertEqual(soup.select('a')[0].attrs.keys(), ['href'])

    def test_append_class(self):
        html_doc = """
        <html><body>
        <p></p>
        <a href=""></a>
        <table></table>
        <img href="" class="testing">
        </body></html>
        """

        content = Page(content=html_doc, settings=get_settings())
        bootstrapify(content)

        soup = BeautifulSoup(content._content, 'html.parser')

        self.assertItemsEqual(soup.select('table')[0].attrs['class'],
                              ['table', 'table-striped', 'table-hover'])
        self.assertItemsEqual(soup.select('img')[0].attrs['class'],
                              ['testing', 'img-responsive'])
        self.assertEqual(soup.select('p')[0].attrs.keys(), [])
        self.assertEqual(soup.select('a')[0].attrs.keys(), ['href'])

    def test_settings(self):
        html_doc = """
        <html><body>
        <p></p>
        <a href=""></a>
        <table></table>
        <img href="" class="testing">
        </body></html>
        """

        settings = get_settings()
        settings['BOOTSTRAPIFY'] = {'p': ['pclass'],
                                    'a': ['aclass1', 'aclass2']}
        content = Page(content=html_doc, settings=settings)
        bootstrapify(content)

        soup = BeautifulSoup(content._content, 'html.parser')

        self.assertItemsEqual(soup.select('p')[0].attrs['class'], ['pclass'])
        self.assertItemsEqual(soup.select('a')[0].attrs['class'],
                              ['aclass1', 'aclass2'])
        self.assertItemsEqual(soup.select('img')[0].attrs['class'],
                              ['testing'])

    def test_selectors(self):
        html_doc = """
        <html><body>
        <p></p>
        <p></p>
        <p></p>
        <a href=""></a>
        <a href="" class="menu"></a>
        <table></table>
        <table id="bootstrapThis"></table>
        <img href="">
        </body></html>
        """

        settings = get_settings()
        settings['BOOTSTRAPIFY'] = {'p:nth-of-type(3)': ['third'],
                                    'a.menu': ['btn', 'btn-lg'],
                                    'table[id]': ['table', 'table-striped']}
        content = Page(content=html_doc, settings=settings)
        bootstrapify(content)

        soup = BeautifulSoup(content._content, 'html.parser')

        self.assertEqual(soup.select('p')[0].attrs.keys(), [])
        self.assertEqual(soup.select('p')[1].attrs.keys(), [])
        self.assertItemsEqual(soup.select('p')[2].attrs['class'], ['third'])
        self.assertEqual(soup.select('a')[0].attrs.keys(), ['href'])
        self.assertItemsEqual(soup.select('a')[1].attrs['class'],
                              ['menu', 'btn', 'btn-lg'])
        self.assertEqual(soup.select('table')[0].attrs.keys(), [])
        self.assertItemsEqual(soup.select('table')[1].attrs['class'],
                              ['table', 'table-striped'])
        self.assertEqual(soup.select('table')[1].attrs['id'], 'bootstrapThis')

    def test_static(self):
        html_doc = """
        <html><body>
        <p></p>
        <a href=""></a>
        <table></table>
        <img href="" class="testing">
        </body></html>
        """

        settings = get_settings()
        settings['BOOTSTRAPIFY'] = {'p': ['pclass'],
                                    'a': ['aclass1', 'aclass2']}
        content = Static(content=html_doc, settings=settings)
        bootstrapify(content)

        soup = BeautifulSoup(content._content, 'html.parser')

        self.assertEqual(content._content, html_doc)


if __name__ == '__main__':
    unittest.main()

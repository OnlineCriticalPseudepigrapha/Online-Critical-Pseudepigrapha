### Test script for adding/removing div elements

from itertools import izip
import os
import shutil
import sys
import unittest

from lxml import etree

from docs.expected_1En import book_1, book_2

# Set up directories and files
# Use modified versions of 1En.xml for test documents
TEST_DOC_1 = '1En_test_1.xml'
TEST_DOC_2 = '1En_test_2.xml'
DTD_NAME = 'grammateus.dtd'

app_root = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]
modules_dir = os.path.join(app_root, 'modules')
docs_dir = os.path.join(app_root, 'test/docs')

dtd_file = os.path.join(app_root, 'static/docs/%s' % DTD_NAME)

# Make sure we can import our modules
if modules_dir not in sys.path:
    sys.path.append(modules_dir)

from parse import Book


# Set this to True if a test fails and the output is too long
MAX_DIFF = False

class TestBookParser(unittest.TestCase):
    '''
    Test cases for parsing a book.
    '''

    def setUp(self):

        self.maxDiff = MAX_DIFF


    def test_parse_book_1(self):
        '''
        Parse a book with no textStructure attribute in the <book> element.
        '''

        doc_file = os.path.join(docs_dir, TEST_DOC_1)

        book = Book(doc_file)

        self.assertEqual(book.structure, book_1)


    def test_parse_book_2(self):
        '''
        Parse a book with a textStructure attribute in the <book> element.
        '''

        doc_file = os.path.join(docs_dir, TEST_DOC_2)

        book = Book(doc_file)

        self.assertEqual(book.structure, book_2)


if __name__ == '__main__':

    unittest.main()



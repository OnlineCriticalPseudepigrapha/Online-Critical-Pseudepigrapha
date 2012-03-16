### Test script for adding/removing div elements

from itertools import izip
import os
import shutil
import sys
import unittest

from lxml import etree


# Set up directories and files
# Use ApocrEzek for testing since it has a good variety of text structures
TEST_DOC = 'ApocrEzek.xml'
DTD_NAME = 'grammateus.dtd'
TEMP_DIR = '/tmp'

app_root = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]
modules_dir = os.path.join(app_root, 'modules')
docs_dir = os.path.join(app_root, 'test/docs')

dtd_file = os.path.join(app_root, 'static/docs/%s' % DTD_NAME)

# Make sure we can import our modules
sys.path.append(modules_dir)

from parse import Book, DivDoesNotExist, RemoveLastDivError


class TestDivAdd(unittest.TestCase):
    '''
    Test cases for adding a div to a book.
    '''

    def setUp(self):

        doc_file = os.path.join(docs_dir, TEST_DOC)

        # Work with a copy of the doc so that we don't change it. Make a copy of
        # the DTD file as well.
        shutil.copy(doc_file, TEMP_DIR)
        shutil.copy(dtd_file, TEMP_DIR)
        doc_file = os.path.join(TEMP_DIR, TEST_DOC)
        
        # Parse the doc
        self.book = Book(doc_file)


    def tearDown(self):

        # Delete the copies of the test doc and DTD files when we're finished
        os.remove(self.book.xml_file)
        os.remove(os.path.join(TEMP_DIR, DTD_NAME))

    
    ### Common test methods
    def _test_div_count(self, divs):
        '''
        Verify number of divs.
        '''

        count = len(divs)
        self.assertEqual(
            count,
            3,
            'Version should have 3 top level <div>s - got %s' %  count
        )
        

    def _test_div_numbers(self, divs, expected):
        '''
        Verify that each div in 'divs' has the correct number attribute.
        '''

        for d, e in zip(divs, expected):
            number = d.get('number')
            self.assertEqual(
                number,
                e,
                '<div> should have @number = "%s" - got %s' % (e, number)
            )
        

    def _test_div_structure(self, div, new_div):
        '''
        Verify that a new div has the correct structure.
        '''

        for descendant, expected in izip(div.iterdescendants(), new_div):
            # Is the descendant a <div> tag?
            tag = descendant.tag
            self.assertEqual(
                tag,
                'div',
                'Child element should be a <div> - got a <%s>' % tag
            )
            
            # Does the new <div> have the correct value for its @number attribute?
            actual = descendant.get('number')
            self.assertEqual(
                actual,
                expected,
                'New <div> should have number "%s" - got "%s"' % (expected, actual)
            )
    
            
    def _test_bottom_level_div_structure(self, div):
        '''
        Verify that a new bottom level div has no children.
        '''

        children = div.getchildren()
        self.assertEqual(
            len(children),
            0,
            'Bottom level <div> should have no children - got %s' % len(children)
        )


    def _test_div_exists(self, version, div):
        '''
        Verify that the new div exists in the xml tree and that it is unique.
        '''

        try:
            div = self.book.get_div(version, div)

        except DivDoesNotExist:
            self.fail(
                'New <div> does not exist.'
            )

        except MultipleDivsFound:
            self.fail(
                'New <div> is not unique.'
            )
    ### End common test methods
        

    def test_add_top_level_div_at_start(self):
        '''
        Add a top level div at the start of the <text> tag.
        '''

        version_title = 'Panarion (Frag. 1)'
        new_div = ['63', '1', '2']

        self.book.add_div(version_title, new_div)

        version = self.book.get_version(version_title)
        divs = version.xpath('text/div')
        
        # Have we got the correct number of <div>s?
        self._test_div_count(divs)
        
        # Does each <div> have the correct value for its @number attribute?
        expected = ('63', '64', '66')
        self._test_div_numbers(divs, expected)
        
        # Does the new <div> have the correct structure?
        div = divs[0]
        self._test_div_structure(div, new_div[1:])

        # Does new div exist?
        self._test_div_exists(version, new_div)


    def test_add_top_level_div_in_middle(self):
        '''
        Add a top level div in the middle of the <text> tag.
        '''

        version_title = 'Panarion (Frag. 1)'
        new_div = ['65', '1', '2']

        version = self.book.get_version(version_title)

        self.book.add_div(version_title, new_div)

        version = self.book.get_version(version_title)
        divs = version.xpath('text/div')
        
        # Have we got the correct number of <div>s?
        self._test_div_count(divs)
        
        # Does each <div> have the correct value for its @number attribute?
        expected = ('64', '65', '66')
        self._test_div_numbers(divs, expected)
        
        # Does the new <div> have the correct structure?
        div = divs[1]
        self._test_div_structure(div, new_div[1:])

        # Does new div exist?
        self._test_div_exists(version, new_div)


    def test_add_top_level_div_at_end(self):
        '''
        Add a top level div at the end of the <text> tag.
        '''

        version_title = 'Panarion (Frag. 1)'
        new_div = ['67', '1', '2']

        self.book.add_div(version_title, new_div)

        version = self.book.get_version(version_title)
        divs = version.xpath('text/div')
        
        # Have we got the correct number of <div>s?
        self._test_div_count(divs)
        
        # Does each <div> have the correct value for its @number attribute?
        expected = ('64', '66', '67')
        self._test_div_numbers(divs, expected)
        
        # Does the new <div> have the correct structure?
        div = divs[-1]
        self._test_div_structure(div, new_div[1:])

        # Does new div exist?
        self._test_div_exists(version, new_div)


    def test_add_second_level_div_at_start(self):
        '''
        Add a second level div at the start of the <text> tag.
        '''

        version_title = 'Panarion (Frag. 1)'
        new_div = ['64', '69', '1']

        self.book.add_div(version_title, new_div)

        version = self.book.get_version(version_title)
        divs = version.xpath('text/div[@number=64]/div')
        
        # Have we got the correct number of <div>s?
        self._test_div_count(divs)
        
        # Does each <div> have the correct value for its @number attribute?
        expected = ('69', '70', '72')
        self._test_div_numbers(divs, expected)
        
        # Does the new <div> have the correct structure?
        div = divs[0]
        self._test_div_structure(div, new_div[2:])

        # Does new div exist?
        self._test_div_exists(version, new_div)


    def test_add_second_level_div_in_middle(self):
        '''
        Add a second level div in the middle of the <text> tag.
        '''

        version_title = 'Panarion (Frag. 1)'
        new_div = ['64', '71', '1']

        self.book.add_div(version_title, new_div)

        version = self.book.get_version(version_title)
        divs = version.xpath('text/div[@number=64]/div')
        
        # Have we got the correct number of <div>s?
        self._test_div_count(divs)
        
        # Does each <div> have the correct value for its @number attribute?
        expected = ('70', '71', '72')
        self._test_div_numbers(divs, expected)
        
        # Does the new <div> have the correct structure?
        div = divs[1]
        self._test_div_structure(div, new_div[2:])

        # Does new div exist?
        self._test_div_exists(version, new_div)


    def test_add_second_level_div_at_end(self):
        '''
        Add a second level div at the end of the <text> tag.
        '''

        version_title = 'Panarion (Frag. 1)'
        new_div = ['64', '73', '1']

        self.book.add_div(version_title, new_div)

        version = self.book.get_version(version_title)
        divs = version.xpath('text/div[@number=64]/div')
        
        # Have we got the correct number of <div>s?
        self._test_div_count(divs)
        
        # Does each <div> have the correct value for its @number attribute?
        expected = ('70', '72', '73')
        self._test_div_numbers(divs, expected)
        
        # Does the new <div> have the correct structure?
        div = divs[-1]
        self._test_div_structure(div, new_div[2:])

        # Does new div exist?
        self._test_div_exists(version, new_div)


    def test_add_bottom_level_div_at_start(self):
        '''
        Add a bottom level div at the start of the <text> tag.
        '''

        version_title = 'Panarion (Frag. 1)'
        new_div = ['64', '70', '1']

        self.book.add_div(version_title, new_div)

        version = self.book.get_version(version_title)
        divs = version.xpath('text/div[@number=64]/div[@number=70]/div')
        
        # Have we got the correct number of <div>s?
        self._test_div_count(divs)
        
        # Does each <div> have the correct value for its @number attribute?
        expected = ('1', '5', '7')
        self._test_div_numbers(divs, expected)
        
        # Does the new <div> have the correct structure?
        div = divs[0]
        self._test_bottom_level_div_structure(div)

        # Does new div exist?
        self._test_div_exists(version, new_div)


    def test_add_bottom_level_div_in_middle(self):
        '''
        Add a bottom level div in the middle of the <text> tag.
        '''

        version_title = 'Panarion (Frag. 1)'
        new_div = ['64', '70', '6']

        self.book.add_div(version_title, new_div)

        version = self.book.get_version(version_title)
        divs = version.xpath('text/div[@number=64]/div[@number=70]/div')
        
        # Have we got the correct number of <div>s?
        self._test_div_count(divs)
        
        # Does each <div> have the correct value for its @number attribute?
        expected = ('5', '6', '7')
        self._test_div_numbers(divs, expected)
        
        # Does the new <div> have the correct structure?
        div = divs[1]
        self._test_bottom_level_div_structure(div)

        # Does new div exist?
        self._test_div_exists(version, new_div)


    def test_add_bottom_level_div_at_end(self):
        '''
        Add a bottom level div at the end of the <text> tag.
        '''

        version_title = 'Panarion (Frag. 1)'
        new_div = ['64', '70', '8']

        self.book.add_div(version_title, new_div)

        version = self.book.get_version(version_title)
        divs = version.xpath('text/div[@number=64]/div[@number=70]/div')
        
        # Have we got the correct number of <div>s?
        self._test_div_count(divs)
        
        # Does each <div> have the correct value for its @number attribute?
        expected = ('5', '7', '8')
        self._test_div_numbers(divs, expected)
        
        # Does the new <div> have the correct structure?
        div = divs[-1]
        self._test_bottom_level_div_structure(div)

        # Does new div exist?
        self._test_div_exists(version, new_div)


    def test_add_div_existing(self):
        '''
        Add a top level div when the div already exists.
        '''

        version_title = 'Panarion (Frag. 1)'
        new_div = ['64', '70', '5']

        self.assertRaises(
            ValueError,
            self.book.add_div,
            version_title, new_div
        )

    
class TestDivRemove(unittest.TestCase):
    '''
    Test cases for removing a div from a book.
    '''

    def setUp(self):

        doc_file = os.path.join(docs_dir, TEST_DOC)

        # Work with a copy of the doc so that we don't change it. Make a copy of
        # the DTD file as well.
        shutil.copy(doc_file, TEMP_DIR)
        shutil.copy(dtd_file, TEMP_DIR)
        doc_file = os.path.join(TEMP_DIR, TEST_DOC)
        
        # Parse the doc
        self.book = Book(doc_file)


    def tearDown(self):

        # Delete the copies of the test doc and DTD files when we're finished
        os.remove(self.book.xml_file)
        os.remove(os.path.join(TEMP_DIR, DTD_NAME))

    
    ### Common test methods
    def _test_div_count(self, divs):
        '''
        Verify number of divs.
        '''

        count = len(divs)
        self.assertEqual(
            count,
            1,
            'Should have 1 <div> - got %s' %  count
        )
        

    def _test_unit_numbers(self):
        '''
        Verify that the <unit>s have been renumbered correctly
        '''

        units = self.book.tree.xpath('//unit')
        numbers = xrange(1, len(units)+1)

        for actual, expected in zip(units, numbers):
            actual = int(actual.get('number'))
            self.assertEqual(
                actual,
                expected,
                'Unit number incorrect: expected %s - got %s' % (expected, actual)
            )


    def _test_div_removed(self, version, div):
        '''
        Verify that the div has been removed.
        '''

        self.assertRaises(
            DivDoesNotExist,
            self.book.get_div,
            version, div
        )
    ### End common test methods
        

    def test_remove_top_level_div(self):
        '''
        Remove a top level div.
        '''

        version_title = 'Panarion (Frag. 1)'
        div = ['64']

        self.book.remove_div(version_title, div)

        version = self.book.get_version(version_title)
        
        # Has the div been removed?
        self._test_div_removed(version, div)

        # Have we got the correct number of <div>s?
        divs = version.xpath('text')
        self._test_div_count(divs)
        
        # Have the <unit>s been correctly renumbered?
        self._test_unit_numbers()


    def test_remove_middle_level_div(self):
        '''
        Remove a middle level div.
        '''

        version_title = 'Panarion (Frag. 1)'
        div = ['64', '70']

        self.book.remove_div(version_title, div)

        version = self.book.get_version(version_title)
        
        # Has the div been removed?
        self._test_div_removed(version, div)

        # Have we got the correct number of <div>s?
        divs = version.xpath('text/div[@number=64]')
        self._test_div_count(divs)
        
        # Have the <unit>s been correctly renumbered?
        self._test_unit_numbers()


    def test_remove_bottom_level_div(self):
        '''
        Remove a bottom level div.
        '''

        version_title = 'Panarion (Frag. 1)'
        div = ['64', '70', '5']

        self.book.remove_div(version_title, div)

        version = self.book.get_version(version_title)
        
        # Has the div been removed?
        self._test_div_removed(version, div)

        # Have we got the correct number of <div>s?
        divs = version.xpath('text/div[@number=64]/div[@number=70]')
        self._test_div_count(divs)
        
        # Have the <unit>s been correctly renumbered?
        self._test_unit_numbers()


    def test_remove_last_top_level_div(self):
        '''
        Remove the last top level div.
        '''

        version_title = 'To the Romans'
        version = self.book.get_version(version_title)
        div = ['8']

        self.assertRaises(
            RemoveLastDivError,
            self.book.remove_div,
            version_title, div
        )


if __name__ == '__main__':

    unittest.main()



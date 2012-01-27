from collections import OrderedDict

from lxml import etree
import gluon


class BookParser(object):
    '''
    Parser for OCP XML files

    It provides methods for:

    book_info() - extract book information from xml
    render_html() - render a section of an xml document into HTML

    '''

    def __init__(self, xml_file):

        self.tree = etree.parse(xml_file)

        self.encoding = etree.DocInfo(self.tree).encoding

        self.book = self.tree.getroot()


    def book_info(self):
        '''
        Return a dictioanry containing information about the book's structure.
        '''

        info = {}

        info['title'] = self.book.xpath('/book/@title')[0]
        try:
            info['structure'] = self.book.xpath('/book/@textStructure')[0]
        except IndexError:
            info['structure'] = ''

        # Parse version tags
        info['versions'] = []

        for version in self.book.xpath('/book/version'):
            version_dict = {}
            version_dict.update((attr, version.xpath('@%s' % attr)[0]) for attr in ('title', 'author', 'language'))

            version_dict['organisation_levels'] = len(version.xpath('divisions/division'))

            version_dict['text_structure'] = self.text_structure(version.xpath('text')[0])
#            print version_dict['text_structure']

            info['versions'].append(version_dict)

        return info


    def text_structure(self, text):
        '''
        Extract the div structure from a given text tag.
        '''

        parent = OrderedDict()
        for div in text.xpath('div'):
            parent_key = div.xpath('@number')[0]
            
            children = OrderedDict()
            for child_div in div.xpath('div'):
                child_key = child_div.xpath('@number')[0]
                child_value = self.text_structure(child_div)

                children[child_key] = child_value

            if children.keys():
                parent[parent_key] = children
            else:
                parent[parent_key] = None

        if parent:
            return parent

        return None



    def render(self):
        '''

        '''

        pass


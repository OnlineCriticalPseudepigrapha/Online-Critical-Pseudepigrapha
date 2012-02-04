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

            info['versions'].append(version_dict)

        return info


    def text_structure(self, text, delimiter=':'):
        '''
        Extract the div structure from a given text tag.
        '''

        parent = OrderedDict()
        for div in text.xpath('div'):
            parent_key = div.xpath('@number')[0]

            children = OrderedDict()
            for child_div in div.xpath('div'):
                child_structure = self.text_structure(child_div)

                if child_structure:
                    for k, v in child_structure:
                        key = '%s%s%s' % (parent_key, delimiter, k)
                        parent[key] = v

                        # Remove child keys
                        del child_structure[k]

                else:
                    # Child div has no children so extract the unit data
                    readings = {}
                    for unit in child_div.xpath('unit'):
                        unit_dict = {}

                        unit_number = unit.xpath('@id')[0]

                        reading_dict = {}
                        for reading in unit.xpath('reading'):
                            mss = reading.xpath('@mss')[0]
                            for m in mss.strip().split():
                                reading_dict[m] = reading.text

                        readings[unit_number] = reading_dict

                    child_key = child_div.xpath('@number')[0]
                    key = '%s%s%s' % (parent_key, delimiter, child_key)
                    parent[key] = readings

        return parent


    def render(self):
        '''

        '''

        pass


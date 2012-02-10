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

        self.default_delimiter = '.'


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
            version_dict = OrderedDict()
            version_dict.update((attr, version.xpath('@%s' % attr)[0]) for attr in ('title', 'author', 'language'))

            divisions = version.xpath('divisions/division')
            version_dict['organisation_levels'] = len(divisions)

            # Extract division delimiters.
            # If there are none, use the default.
            delimiters = []
            for d in divisions[:-1]:
                delimiter = d.xpath('@delimiter')
                if delimiter:
                    delimiters.append(delimiter[0])
            if not delimiters:
                delimiters = [self.default_delimiter] * (len(divisions) - 1)

            version_dict['delimiters'] = delimiters
            
            mss = OrderedDict()
            for ms in version.xpath('manuscripts/ms'):
                ms_dict = OrderedDict()
                ms_dict= OrderedDict((attr, ms.xpath('@%s' % attr)[0]) for attr in ('abbrev', 'language'))
                ms_dict['name'] = ms.xpath('name')[0].text
                ms_dict['bibliography'] = ms.xpath('bibliography')[0].text

                mss[ms_dict['abbrev']] = ms_dict

            version_dict['manuscript'] = mss

            version_dict['text_structure'] = self.text_structure(version.xpath('text')[0], delimiters)

            info['versions'].append(version_dict)

        return info


    def text_structure(self, text, delimiters):
        '''
        Extract the div structure from a given text tag.
        '''

        parent = OrderedDict()
        for div in text.xpath('div'):
            parent_key = div.xpath('@number')[0]

            for child_div in div.xpath('div'):
                child_structure = self.text_structure(child_div, delimiters[1:])

                if child_structure:
                    for k, v in child_structure:
                        key = '%s%s%s' % (parent_key, delimiter, k)
                        parent[key] = v

                        # Remove child keys
                        del child_structure[k]

                else:
                    # Child div has no children so extract the unit data
                    readings = OrderedDict()
                    for unit in child_div.xpath('unit'):
                        unit_number = unit.xpath('@id')[0]

                        reading_dict = OrderedDict()
                        for reading in unit.xpath('reading'):
                            mss = reading.xpath('@mss')[0]
                            for m in mss.strip().split():
                                reading_dict[m] = reading.text

                        readings[unit_number] = reading_dict

                    child_key = child_div.xpath('@number')[0]
                    key = '%s%s%s' % (parent_key, delimiters[0], child_key)
                    parent[key] = readings

        return parent


    def render(self):
        '''

        '''

        pass

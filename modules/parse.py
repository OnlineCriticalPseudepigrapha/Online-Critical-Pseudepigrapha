from collections import OrderedDict
from itertools import izip_longest
from lxml import etree
import gluon


class BookParser(object):
    '''
    Parser for OCP XML files

    It provides methods for:

    book_info() - extract book information from xml
    get_reference() - extract readings given a version title and an iterable of
                      divisions
    '''

    def __init__(self, xml_file):

        self.xml_file = xml_file
        
        # Validate document against its schema
        parser = etree.XMLParser(dtd_validation=True)
        try:
            self.tree = etree.parse(xml_file, parser)
        except etree.XMLSyntaxError:
            print 'Document does not validate against its schema: %s' % xml_file
            raise   # Just reraise for now

        self.encoding = etree.DocInfo(self.tree).encoding

        self.book = self.tree.getroot()
        
        self.default_delimiter = '.'

        
    def book_info(self):
        '''
        Return a dictioanry containing information about the book's structure.
        '''

        info = {}

        info['title'] = unicode(self.book.xpath('/book/@title')[0])
        try:
            info['structure'] = unicode(self.book.xpath('/book/@textStructure')[0])
        except IndexError:
            info['structure'] = unicode('')

        # Parse version tags
        info['versions'] = []

        for version in self.book.xpath('/book/version'):
            version_dict = OrderedDict()
            version_dict.update((attr, unicode(version.xpath('@%s' % attr)[0])) for attr in ('title', 'author', 'language'))

            divisions = version.xpath('divisions/division')
            version_dict['organisation_levels'] = len(divisions)

            # Extract division delimiters.
            # If there are none, use the default.
            delimiters = []
            for d in divisions[:-1]:
                delimiter = d.xpath('@delimiter')
                if delimiter:
                    delimiters.append(unicode(delimiter[0]))
            if not delimiters:
                delimiters = [self.default_delimiter] * (len(divisions) - 1)

            version_dict['delimiters'] = delimiters

            mss = OrderedDict()
            for ms in version.xpath('manuscripts/ms'):
                ms_dict = OrderedDict((attr, unicode(ms.xpath('@%s' % attr)[0])) for attr in ('abbrev', 'language'))

                ms_dict['name'] = unicode(ms.xpath('name')[0].text.strip())

                ms_dict['bibliography'] = []
                bibliography = ms.xpath('bibliography')
                if bibliography:
                    ms_dict['bibliography'] = [unicode(b.text.strip()) for b in bibliography]

                mss[ms_dict['abbrev']] = ms_dict

            version_dict['manuscript'] = mss

            version_dict['text_structure'] = self.text_structure(version.xpath('text')[0], delimiters)

            info['versions'].append(version_dict)

        self.book_info = info

        return info


    def text_structure(self, text, delimiters):
        '''
        Extract the div structure from a given text tag.
        '''

        parent = OrderedDict()
        for div in text.xpath('div'):
            parent_key = unicode(div.xpath('@number')[0])

            child_structure = self.text_structure(div, delimiters[1:])

            if child_structure:
                for k, v in child_structure.items():
                    key = '%s%s%s' % (parent_key, delimiters[0], k)
                    parent[key] = v

                    # Remove child keys
                    del child_structure[k]

            else:
                # Child div has no children so extract the unit data
                readings = OrderedDict()
                for unit in div.xpath('unit'):
                    unit_number = unicode(unit.xpath('@id')[0])

                    reading_dict = OrderedDict()
                    for reading in unit.xpath('reading'):
                        mss = unicode(reading.xpath('@mss')[0])
                        for m in mss.strip().split():
                            reading_dict[m] = reading.text

                    readings[unit_number] = reading_dict

                parent[parent_key] = readings

        return parent


    def get_reference(self, version_title, divisions):
        '''
        Get the text referenced by the version title and division numbers.

        Divisions is an iterable of division numbers with the number of the top
        most levels preceding lower level numbers.

        Return an OrderedDict keyed by unit id. The values are an OrderedDict of
        manuscript, text pairs. If the snippet doesn't exist, return an empty
        OrderedDict.
        '''

        # Get the version from the book info
        version = None
        for v in self.book_info['versions']:
            if v['title'] == version_title:
                version = v
                break

        if not version:
            raise ValueError('ERROR: Book "%s" does not have a version with title "%s"'
                                % (self.book_info['title'], version_title))

        # Get text reference
        delimiters = version['delimiters']
        key = ''.join('%s%s' % (div, delim) for div, delim in izip_longest(divisions, delimiters, fillvalue=''))

        text = version['text_structure']
        try:
            reference = text[key]
        except KeyError:
            return OrderedDict()

        return reference



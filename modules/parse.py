from collections import OrderedDict
from itertools import izip_longest
from lxml import etree
import gluon


class VersionDoesNotExist(Exception):
    pass

class MultipleVersionsFound(Exception):
    pass

class DivDoesNotExist(Exception):
    pass

class MultipleDivsFound(Exception):
    pass

class RemoveLastDivError(Exception):
    pass


class Book(object):
    '''
    Parser for OCP XML files

    It provides methods for:

    book_info() - extract book structure information from xml
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
            raise   # Just reraise for now

        self.encoding = etree.DocInfo(self.tree).encoding

        self.book = self.tree.getroot()
        
        self.default_delimiter = '.'

        self.structure = self.book_info()

        
    def book_info(self):
        '''
        Return a dictionary containing information about the book's structure.
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

        self.structure = info

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


    def get_version(self, version_title):
        '''
        Return a version given its title.

        Arguments:
            version_title - the title of the required version.

        Raise VersionDoesNotExist if a version with the specified title does not
        exist.

        Raise MultipleVersionsFound if the book has more than one version with
        the specified title.
        '''

        version = self.book.xpath('/book/version[@title="%s"]' % version_title)

        if not version:
            raise VersionDoesNotExist(
                'ERROR: Book "%s" does not have a version with title "%s"'
                % (self.structure['title'], version_title)
            )
        
        if len(version) > 1:
            raise MultipleVersionsFound(
                'ERROR: Book "%s" has %d versions with title "%s"'
                % (self.book_info['title'], len(version), version_title)
            )

        return version[0]

    
    def get_div(self, version, divs):
        '''
        Return a div given a version and div numbers.

        Arguments:
            version - the version containg the required div.
            divs - an iterable of div numbers with the number of the top most
                   levels preceding lower level numbers.

        Raise DivDoesNotExist if the version does not contain a div with the
        given numbers.

        Raise MultipleDivsFound if the version contains more than one div with
        the given numbers.
        '''

        path = 'text/%s' % '/'.join('div[@number=%s]' % d for d in divs)
        div = version.xpath(path)

        if not div:
            raise DivDoesNotExist(
                'ERROR: Version "%s" does not have a div with numbers "%s"'
                % (version.get('title'), divs)
            )
        
        if len(div) > 1:
            raise MultipleDivsFound(
                'ERROR: Version "%s" has %d divs with numbers "%s"'
                % (version.get('title'), len(div), divs)
            )

        return div[0]

   
    def get_readings(self, units):
        '''
        Return the readings for each unit in units as an OrderedDict. The keys
        are unit @ids and the values are OrderedDicts of @mss/text pairs.
        
        Arguments:
            units - the result of calling xpath('unit') on a div element.
        '''

        results = OrderedDict()
        for unit in units:
            unit_number = unit.xpath('@id')[0]

            readings = OrderedDict()
            for reading in unit.xpath('reading'):
                mss = reading.xpath('@mss')[0]
                for m in mss.strip().split():
                    reading_dict[m] = reading.text

            results[unit_number] = readings

        return results


    def renumber_units(self):
        '''
        If we're adding or removing an element that contains units (a version,
        div or unit), all units that follow the affected units must be
        renumbered since all units in a document must be numbered consecutively.

        It may not be the most efficient way, but we just renumber all the units
        starting with 1.
        '''

        units = self.tree.xpath('//unit')
        for index, unit in enumerate(units):
            unit.set('number', unicode(index+1))


    def get_reference(self, version_title, divs):
        '''
        Get the text referenced by the version title and div numbers.

        Arguments:
            version_title - the title of the required version.
            divs - an iterable of div numbers with the number of the top most
                   levels preceding lower level numbers.

        Return an OrderedDict keyed by unit id. The values are an OrderedDict of
        manuscript, text pairs.
        '''

        version = self.get_version(version_title)

        div = self.get_div(version, divs)

        # Check that we have a bottom level div
        if not len(div):
            raise ValueError(
                'ERROR: Div %s is empty.'
                % divs
            )

        units = div.xpath('unit')
        if not units:
            raise ValueError(
                'ERROR: Div %s has no units.' 
                % divs
            )

        return self.get_readings(units)


    def find_insertion_point(self, parent, element, attr, values):
        '''
        Find where to insert a new child element within a parent element's
        children.

        Get all the parent's children where the attribute named by 'attr' has a
        value less than or equal to the first item in 'values'. In the case of
        multilevel elements like <div>, recurse down the tree until we find the
        insertion position.

        Arguments:
            parent - the element into which the new child is to be inserted.
            element - the tag of the child to be inserted.
            attr - the name of the child's attribute on which the search for the
                   insertion point will be performed.
            values - an iterable containing the values of the attribute to be
                     matched. Multiple values of the attribute are needed where
                     we have multiple levels of elements with the same name to
                     be searched e.g. div.
       
        Return a tuple containing the current parent element, the index at which
        to insert the new element and the unused portion of the values list.

        TODO: Allow for multiple attribute names each with multiple values
              (might be needed for adding units)?
        '''

        children = parent.xpath('%s[@%s<=%s]' % (element, attr, values[0]))
        if len(children):
            if children[-1].get(attr) == values[0]:
                parent, index, values = self.find_insertion_point(children[-1], element, attr, values[1:])
            else:
                index = len(children)

        else:
            index = 0

        return parent, index, values
    

    def write(self):
        '''
        Write xml tree to file.
        '''

        fp = open(self.xml_file, 'w')
        self.tree.write(fp)

    
    def add_div(self, version_title, new_div):
        '''
        Add a new div to the version with the given version title at the
        location given by the div numbers in div.

        Raise ValueError if the div already exists.

        Arguments:
            version_title - the title of the required version.
            new_div - an iterable of div numbers with the number of the top most
                      levels preceding lower level numbers. It defines the
                      location in the version's text element in which to insert
                      the new div.
        '''

        version = self.get_version(version_title)

        # Make sure div doesn't already exist
        div = None
        try:
            div = self.get_div(version, new_div)
        except DivDoesNotExist:
            pass
        except:
            raise

        if div is not None:
            raise ValueError(
                'ERROR: <div> %s already exists in <version> %s'
                % (','.join(new_div), version_title)
            )

        # Find out where to insert the new div
        text = version.xpath('text')[0]
        element, index, values = self.find_insertion_point(text, 'div', 'number', new_div)

        # Insert the new div and the required children
        while values:
            new = etree.Element('div')
            new.set('number', values[0])
            element.insert(index, new)
            element = element.xpath('div')[index]
            values = values[1:]
            index = 0

        # Rebuild book_info
        self.structure = self.book_info()

        # TODO: Update cache (when caching implemented)

        # Write to file
        self.write()


    def remove_div(self, version_title, divs):
        '''
        Remove the div referenced by the version title and div numbers.
        Do nothing if the <div> does not exist.

        Arguments:
            version_title - the title of the required version.
            divs - an iterable of div numbers with the number of the top most
                   levels preceding lower level numbers.
        '''

        version = self.get_version(version_title)

        # We cannot remove a top level div if it's the only one in the version's
        # <text> element since it must contain at least one <div> according to
        # the DTD.
        if len(divs) == 1:   # Removing a top level div
            num_divs = version.xpath('text/div')
            if len(num_divs) == 1:
                raise RemoveLastDivError('Attempt to remove the only <div> in version.')

        try:
            div = self.get_div(version, divs)
        except DivDoesNotExist:
            return

        # Remove div
        div.getparent().remove(div)

        # Renumber units in subsequent divs and versions
        self.renumber_units()

        # Rebuild book_info
        self.structure = self.book_info()
        
        # TODO: Update cache (when caching implemented)
        
        # Write to file
        self.write()




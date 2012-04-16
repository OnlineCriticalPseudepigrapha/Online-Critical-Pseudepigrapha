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


    ### Extraction methods

    def text_structure(self, text, delimiters):
        '''
        Extract the div structure from a given text tag.
        '''

        parent = OrderedDict()
        for div in text.xpath('div'):
            parent_attributes = [self._getattrs(div, ('number', 'fragment'))]

            parent_key = unicode(parent_attributes[0]['number'])

            child_structure = self.text_structure(div, delimiters[1:])

            if child_structure:
                for k, v in child_structure.items():
                    key = '%s%s%s' % (parent_key, delimiters[0], k)
                    parent[key] = v
                    attributes = parent_attributes + v['attributes']
                    parent[key]['attributes'] = attributes

                    # Remove child keys
                    del child_structure[k]

            else:
                # Child div has no children so extract the unit data
                readings = OrderedDict()
                units = []
                for u in div.xpath('unit'):
                    attributes = self._getattrs(u, ('id', 'group', 'parallel'))
                    if not attributes['group']:
                        attributes['group'] = '0'
                    units.append(attributes)

                    reading_dict = OrderedDict()
                    for reading in u.xpath('reading'):
                        attributes = self._getattrs(reading, ('option', 'mss', 'linebreak', 'indent'))

                        w_list = []
                        for w in reading.xpath('w'):
                            w_list.append(dict({
                                'attributes': self._getattrs(w, ('morph', 'lex', 'style', 'lang')),
                                'text': w.text
                            }))

                        mss = unicode(attributes['mss'].strip())
                        reading_dict[mss] = {
                            'attributes': attributes,
                            'text': reading.text.strip(),
                            'w': w_list,
                        }

                    readings[units[-1]['id']] = reading_dict

                parent[parent_key] = {'attributes': parent_attributes, 'units': units, 'readings': readings}

        return parent


    def _getattrs(self, element, attrs):
        '''
        Return an OrderedDict of an element's attributes/values. If the element
        does not have a requested attribute, add the attribute with an empty
        string as it's value.

        Arguments:
            element - the element from which we are extracting attributes.
            attrs - an iterable containing the names of the attributes we want
                    to extract from the element. This is usually a complete list
                    of the element's attributes according to the DTD, but it
                    doesn't have to be.
        '''

        attributes = OrderedDict(element.items())

        # If any attributes are missing assign them an empty string.
        attributes.update((attr, '') for attr in attrs if attr not in attributes)

        return attributes


    def get_divisions_info(self, divisions):
        '''
        Return a dictionary of lists of <divisions> tag attributes and text.

        Arguments:
            divisions - a list of <divisions> elements from which we are extracting data.
        '''

        data = {
            'labels': [],
            'delimiters': [],
            'text': [],
        }

        delimiters = []
        labels = []
        text = []

        for d in divisions:
            # Extract division delimiters and labels
            attributes = self._getattrs(d, ('label', 'delimiter'))
            labels.append(unicode(attributes['label']))
            delimiter = attributes['delimiter']
            if delimiter:
                delimiters.append(unicode(delimiter))

            # Extract text content
            text.append(unicode(d.text or ''))

        if not delimiters:
            delimiters = [self.default_delimiter] * (len(divisions) - 1)

        data['labels'] = labels
        data['delimiters'] = delimiters
        data['text'] = text

        return data


    def get_resources_info(self, resources):
        '''
        Return a list of dictionaries of <resource> tag attributes and text.

        Arguments:
            resources - a list of <resources> elements from which we are extracting data.
        '''

        data = []

        for res in resources:
            res_data = []
            for r in res.xpath('resource'):
                resource = {}

                resource['attributes'] = self._getattrs(r, ('name', ))
                resource['info'] = [unicode(i.text) for i in r.xpath('info')]
                url = r.xpath('URL')
                if url:
                    resource['url'] = unicode(url[0].text)
                else:
                    resource['url'] = ''

                res_data.append(resource)

            data.append(res_data)

        return data


    def get_manuscripts_info(self, manuscripts):
        '''
        Return a list of dictionaries of <manuscripts> tag attributes and text.

        Arguments:
            manuscripts - a list of <manuscripts> elements from which we are extracting data.
        '''

        data = []

        for manuscript in manuscripts:
            ms_data = OrderedDict()
            for ms in manuscript.xpath('ms'):
                ms_dict = {}
                ms_dict['attributes'] = OrderedDict((attr, unicode(ms.xpath('@%s' % attr)[0])) for attr in ('abbrev', 'language', 'show'))

                ms_dict['name'] = {}
                name = ms.xpath('name')[0]
                if name.text is not None:
                    ms_dict['name']['text'] = unicode(name.text.strip())
                else:
                    ms_dict['name']['text'] = ''

                ms_dict['name']['sup'] = [unicode(s.text.strip()) for s in name.xpath('sup')]

                ms_dict['bibliography'] = []
                for bib in ms.xpath('bibliography'):
                    bib_dict = {}
                    if bib.text:
                        bib_dict['text'] = unicode(bib.text.strip())
                    else:
                        bib_dict['text'] = []
                    bib_dict['booktitle'] = [unicode(b.text.strip()) for b in bib.xpath('booktitle')]

                    ms_dict['bibliography'].append(bib_dict)

                ms_data[ms_dict['attributes']['abbrev']] = ms_dict

            data.append(ms_data)

        return data


    def get_text_info(self, text, delimiters):
        '''
        Return a OrderedDict containing data from a <text> element.

        Arguments:
            text - the <text> element from which we are extracting data.
            delimiters - a list of the delimiters used to seperate a document's
                         divisions
        '''

        data = self.text_structure(text[0], delimiters)

        return data

    ### End extraction methods

    def book_info(self):
        '''
        Return a dictionary containing information about the book's structure.
        '''

        info = {}

        info['book'] = self._getattrs(self.book.xpath('/book')[0],
                                        ('filename', 'title', 'textStructure'))

        # Parse version tags
        info['version'] = []

        for version in self.book.xpath('/book/version'):
            version_dict = OrderedDict()
            version_dict['attributes'] = self._getattrs(version,
                                                        ('title', 'author', 'fragment', 'language'))

            divisions = version.xpath('divisions/division')
            version_dict['organisation_levels'] = len(divisions)

            version_dict['divisions'] = self.get_divisions_info(divisions)
            version_dict['resources'] = self.get_resources_info(version.xpath('resources'))
            version_dict['manuscripts'] = self.get_manuscripts_info(version.xpath('manuscripts'))
            version_dict['text_structure'] = self.get_text_info(version.xpath('text'),
                                                                version_dict['divisions']['delimiters'])

            info['version'].append(version_dict)

        self.structure = info

        return info


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


    def add_version(self, attrs, elements):
        '''
        Add a new version.

        Arguments:
            attrs - dictionary of the version element's attributes
            elements - dictionary defining the version element's elements
        '''

        pass



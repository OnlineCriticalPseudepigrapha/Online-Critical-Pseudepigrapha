# -*- coding: utf-8 -*-
from collections import namedtuple
from collections import OrderedDict
from datetime import datetime
import os

from lxml import etree

from gluon import A, DIV, SPAN, TAG

XML_FILE_STORAGE_PATH = "static/docs"
XML_FILE_BACKUP_STORAGE_PATH = "static/docs/backups"
XML_DRAFT_FILE_STORAGE_PATH = "static/docs/draft"
XML_DRAFT_FILE_BACKUP_STORAGE_PATH = "static/docs/draft/backups"

XML_DEFAULT_DOCINFO = {"encoding": "UTF-8",
                       "doctype": "<!DOCTYPE book SYSTEM 'grammateus.dtd'>",
                       "standalone": False}

Text = namedtuple("Text", "unit_id, language, readings_in_unit, text")
Reading = namedtuple("Reading", "mss, text")

## Common Exception classes


class InvalidDocument(Exception):
    pass


class ElementDoesNotExist(Exception):
    pass


class MultipleElementsReturned(Exception):
    pass


class ElementAlreadyExists(Exception):
    pass


class InvalidDIVPath(Exception):
    pass


class NotAllowedManuscript(Exception):
    pass


## Book class


class Book(object):
    """
    Parser and manipulator class for OCP XML files

    It provides methods for:

    book_info() - extract book structure information from xml
    get_reference() - extract readings given a version title and an iterable of
                      divisions
    """

    @staticmethod
    def open(xml_book_data):
        """
        Factory method for parsing a preloaded xml file

        :param xml_book_data: book structure wrapped into a file-like object
        :return: Book object
        """
        book = Book()
        try:
            if getattr(xml_book_data, "read"):
                tree = etree.parse(xml_book_data)
            else:
                tree = etree.parse(open(xml_book_data))
        except AttributeError:
            raise TypeError("Book() requires XML data in a file-like object")
        book._book = tree.getroot()
        book._docinfo.update({i: getattr(tree.docinfo, i) for i in XML_DEFAULT_DOCINFO.keys()})
        book._structure_info = book._get_book_info()
        return book

    @staticmethod
    def create(filename, title, frags=False):
        """
        Factory method for creating new book structure

        :param frags: boolean, when it's True the textStructure attribute of <book> will be "fragmentary"
        :param filename: string
        :param title: string
        :return: Book object
        """
        book = Book()
        attrib = {"filename": filename, "title": title}
        if frags:
            attrib["textStructure"] = "fragmentary"
        book._book = etree.Element("book", attrib=attrib)

        return book

    def __init__(self):
        self._book = None
        self._docinfo = XML_DEFAULT_DOCINFO
        self._structure_info = {}
        self.default_delimiter = '.'

    def validate(self, dtd_data):
        """Detached validation from parsing due to performance reasons."""
        try:
            dtd = etree.DTD(dtd_data)
        except AttributeError:
            raise TypeError("validate() requires DTD in a file-like object")
        if not dtd.validate(self._book):
            raise InvalidDocument(dtd.error_log.filter_from_errors()[0])

    def book_info(self):
        return self._structure_info

    def _getattrs(self, element, attrs):
        """
        Return an OrderedDict of an element's attributes/values. If the element
        does not have a requested attribute, add the attribute with an empty
        string as it's value.

        Arguments:
            element - the element from which we are extracting attributes.
            attrs - an iterable containing the names of the attributes we want
                    to extract from the element. This is usually a complete list
                    of the element's attributes according to the DTD, but it
                    doesn't have to be.
        """

        attributes = OrderedDict(element.items())

        # If any attributes are missing assign them an empty string.
        attributes.update((attr, '') for attr in attrs if attr not in attributes)

        return attributes

    def _get_book_info(self):
        """Return a dictionary containing information about the book's structure."""

        info = {'book': self._getattrs(self._book.xpath('/book')[0], ('filename', 'title', 'textStructure')),
                'version': []}

        # Parse version tags
        for version in self._book.xpath('/book/version'):
            version_dict = OrderedDict()
            version_dict['attributes'] = self._getattrs(version, ('title', 'author', 'fragment', 'language'))

            divisions = version.xpath('divisions/division')
            version_dict['organisation_levels'] = len(divisions)

            version_dict['divisions'] = self.get_divisions_info(divisions)
            version_dict['resources'] = self.get_resources_info(version.xpath('resources'))
            version_dict['manuscripts'] = self.get_manuscripts_info(version.xpath('manuscripts'))
            version_dict['text_structure'] = self.get_text_info(version.xpath('text'),
                                                                version_dict['divisions']['delimiters'])
            info['version'].append(version_dict)

        return info

    def get_divisions_info(self, divisions):
        """
        Return a dictionary of lists of <divisions> tag attributes and text.

        Arguments:
            divisions - a list of <divisions> elements from which we are extracting data.
        """

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
        """
        Return a list of dictionaries of <resource> tag attributes and text.

        Arguments:
            resources - a list of <resources> elements from which we are extracting data.
        """

        data = []

        for res in resources:
            res_data = []
            for r in res.xpath('resource'):
                resource = {'attributes': self._getattrs(r, ('name', )),
                            'info': [unicode(i.text) for i in r.xpath('info')]}
                url = r.xpath('URL')
                if url:
                    resource['url'] = unicode(url[0].text)
                else:
                    resource['url'] = ''

                res_data.append(resource)

            data.append(res_data)

        return data

    def get_manuscripts_info(self, manuscripts):
        """
        Return a list of dictionaries of <manuscripts> tag attributes and text.

        Arguments:
            manuscripts - a list of <manuscripts> elements from which we are extracting data.
        """

        data = []

        for manuscript in manuscripts:
            ms_data = OrderedDict()
            for ms in manuscript.xpath('ms'):
                ms_dict = {'attributes': OrderedDict(
                    (attr, unicode(ms.xpath('@%s' % attr)[0])) for attr in ('abbrev', 'language', 'show')), 'name': {}}

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
        """
        Return a OrderedDict containing data from a <text> element.

        Arguments:
            text - the <text> element from which we are extracting data.
            delimiters - a list of the delimiters used to seperate a document's
                         divisions
        """

        data = self.text_structure(text[0], delimiters)

        return data

    def text_structure(self, text, delimiters):
        """Extract the div structure from a given text tag."""

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
                    unit = {}
                    u_attributes = self._getattrs(u, ('id', 'group', 'parallel'))
                    if not u_attributes['group']:
                        u_attributes['group'] = '0'
                    unit['id'] = u_attributes['id']
                    unit['group'] = u_attributes['group']
                    unit['parallel'] = u_attributes['parallel']

                    reading_dict = OrderedDict()
                    for reading in u.xpath('reading'):
                        r_attributes = self._getattrs(reading, ('option', 'mss', 'linebreak', 'indent'))

                        w_list = []
                        for w in reading.xpath('w'):
                            w_list.append(dict({
                                'attributes': self._getattrs(w, ('morph', 'lex', 'style', 'lang')),
                                'text': w.text
                            }))

                        mss = unicode(r_attributes['mss'].strip())
                        reading_dict[mss] = {
                            'attributes': r_attributes,
                            'text': reading.text.strip() if reading.text else "",
                            #TODO: Integrate word list (parsed words) with text (unparsed text)
                            'w': w_list,
                        }
                    unit['readings'] = reading_dict

                    units.append(unit)

                parent[parent_key] = {'attributes': parent_attributes, 'units': units, 'readings': readings}

        return parent

    def _get(self, element_name, attribute, on_element=None):
        """
        Get back the requested element if it exists and there's one and only one with the given attribute
        """
        if attribute:
            xpath = "{}[@{}='{}']".format(element_name,
                                          attribute.keys()[0],
                                          attribute.values()[0])
            elements = on_element.xpath(xpath) if on_element is not None else self._book.xpath(xpath)
            if not elements:
                raise ElementDoesNotExist("<{}> element with {}='{}' does not exist".format(element_name,
                                                                                            attribute.keys()[0],
                                                                                            attribute.values()[0]))
            elif len(elements) > 1:
                raise MultipleElementsReturned("There are more <{}> elements with {}='{}'".format(element_name,
                                                                                                  attribute.keys()[0],
                                                                                                  attribute.values()[0]))
        else:
            xpath = element_name
            elements = on_element.xpath(xpath) if on_element else self._book.xpath(xpath)
            if not elements:
                raise ElementDoesNotExist("Element does not exist on this xpath <{}>".format(xpath))
            elif len(elements) > 1:
                raise MultipleElementsReturned("There are more elements on this xpath <{}>".format(xpath))

        return elements[0]

    def _renumber_units(self):
        """
        If we're adding or removing an element that contains units (a version,
        div or unit), all units that follow the affected units must be
        renumbered since all units in a document must be numbered consecutively.

        It may not be the most efficient way, but we just renumber all the units
        starting with 1.
        """
        for index, unit in enumerate(self._book.xpath("//unit"), 1):
            unit.set("id", str(index))

    def get_filename(self):
        return self._book.get("filename")

    # RI methods

    def get_text(self, version_title, text_type, start_div, end_div=None):

        version = self._get("version", {"title": version_title})

        manuscript = self._get("manuscripts/ms", {"abbrev": text_type}, version)
        if manuscript.get("show") == "no":
            raise NotAllowedManuscript

        reading_filter = "reading[re:test(@mss, '^{0} | {0} | {0}$|^{0}$')]".format(text_type)

        start_div_elements = []
        if start_div:
            base_element = version.xpath("text")[0]
            for div_number in start_div:
                try:
                    base_element = self._get("div", {"number": div_number}, base_element)
                    start_div_elements.append(base_element)
                except ElementDoesNotExist:
                    break  # we keep the last correct element

        end_div_elements = []
        if end_div:
            base_element = version.xpath("text")[0]
            for div_number in end_div:
                try:
                    base_element = self._get("div", {"number": div_number}, base_element)
                    end_div_elements.append(base_element)
                except ElementDoesNotExist:
                    break  # we keep the last correct element

        if start_div_elements:
            current_div = start_div_elements[-1]
            current_level = len(start_div_elements) - 1
        else:
            current_div = version.xpath("text/div")[0]
            current_level = 0

        if end_div_elements:
            last_div = end_div_elements[-1]
        else:
            last_div = version.xpath(".//{}[last()]".format(reading_filter))[0].getparent().getparent()

        # iterate through the <div> elements and search the required <reading>
        while end_div_elements and len(end_div_elements) > current_level and current_div == end_div_elements[current_level]:
            if current_div.getchildren():
                current_div = current_div.getchildren()[0]
                current_level += 1
            else:
                raise StopIteration
        while True:
            for reading in current_div.xpath(".//{}".format(reading_filter),
                                             namespaces={"re": "http://exslt.org/regular-expressions"}):
                yield Text(reading.getparent().get("id"),
                           version.get("language"),
                           len(reading.getparent().getchildren()),
                           reading.text.strip() if reading.text else "")

            if current_div == last_div:
                raise StopIteration

            while current_div.getnext() is not None and current_level > 0:
                current_div = current_div.getparent()
                current_level -= 1
                if current_div == last_div:
                    raise StopIteration

            if current_div.getnext() is not None:
                current_div = current_div.getnext()
                while end_div_elements and len(end_div_elements) > current_level and current_div == end_div_elements[current_level]:
                    if current_div.getchildren():
                        current_div = current_div.getchildren()[0]
                        current_level += 1
                    else:
                        raise StopIteration
            else:
                raise StopIteration

    def get_readings(self, unit_id):
        for reading in self._book.xpath("//unit[@id={}]/reading".format(unit_id)):
            yield Reading(reading.get("mss").strip(), reading.text.strip() if reading.text else "")

    # EI methods

    def add_version(self, version_title, language, author, mss=None):
        if self._book.xpath("version[@title='{}']".format(version_title)):
            raise ElementAlreadyExists("<version> element with title='{}' already exists")
        version = etree.SubElement(self._book,
                                   "version",
                                   attrib={"title": version_title,
                                           "author": author,
                                           "language": language})
        # add mandatory subelements
        etree.SubElement(version, "divisions")
        manuscripts = etree.SubElement(version, "manuscripts")
        if mss:
            if isinstance(mss, basestring):
                mss = mss.split()
                if len(mss) == 1:
                    mss = mss[0].split(",")
            for ms in mss:
                etree.SubElement(manuscripts,
                                 "ms",
                                 attrib={"abbrev": ms, "language": "", "show": ""}).append(etree.Element("name"))
        etree.SubElement(version, "text")

    def update_version(self, version_title, new_version_title=None, new_language=None, new_author=None):
        version = self._get("version", {"title": version_title})
        if new_version_title:
            version.set("title", new_version_title)
        if new_language:
            version.set("language", new_language)
        if new_author:
            version.set("author", new_author)

    def del_version(self, version_title):
        version = self._get("version", {"title": version_title})
        version.getparent().remove(version)

    def add_manuscript(self, version_title, abbrev, language, show=True):
        manuscripts = self._get("manuscripts", None, self._get("version", {"title": version_title}))
        etree.SubElement(manuscripts,
                         "ms", {"abbrev": abbrev,
                                "language": language,
                                "show": "yes" if show else "no"}).append(etree.Element("name"))

    def update_manuscript(self, version_title, abbrev, new_abbrev, new_language=None, new_show=None):
        ms = self._get("manuscripts/ms", {"abbrev": abbrev}, self._get("version", {"title": version_title}))
        if new_abbrev:
            ms.set("abbrev", new_abbrev)
        if new_language:
            ms.set("language", new_language)
        if new_show is not None:
            ms.set("show", "yes" if new_show else "no")

    def del_manuscript(self, version_title, abbrev):
        ms = self._get("manuscripts/ms", {"abbrev": abbrev}, self._get("version", {"title": version_title}))
        # ms = self._get("version", {"title": version_title}).xpath("manuscripts/ms[@abbrev='{}'".format(abbrev))
        ms.getparent().remove(ms)

    def add_bibliography(self, version_title, abbrev, text):
        ms = self._get("manuscripts/ms", {"abbrev": abbrev}, self._get("version", {"title": version_title}))
        etree.SubElement(ms, "bibliography").text = text

    def update_bibliography(self, version_title, abbrev, bibliography_pos, new_text):
        ms = self._get("manuscripts/ms", {"abbrev": abbrev}, self._get("version", {"title": version_title}))
        bibliography = self._get("bibliography[{}]".format(int(bibliography_pos) + 1), None, ms)
        bibliography.text = new_text

    def del_bibliography(self, version_title, abbrev, bibliography_pos):
        ms = self._get("manuscripts/ms", {"abbrev": abbrev}, self._get("version", {"title": version_title}))
        bibliography = self._get("bibliography[{}]".format(int(bibliography_pos) + 1), None, ms)
        bibliography.getparent().remove(bibliography)

    def add_div(self, version_title, div_name, div_parent_path, preceding_div=None):
        if div_parent_path:
            parent_xpath = "/".join(["text"] + ["div[@number='{}']".format(div_number) for div_number in div_parent_path])
            div_parent = self._get(parent_xpath, attribute=None, on_element=self._get("version", {"title": version_title}))
        else:
            div_parent = self._get("text", attribute=None, on_element=self._get("version", {"title": version_title}))
        if preceding_div:
            div_sibling = self._get("div", attribute={"number": preceding_div}, on_element=div_parent)
            div_sibling.addnext(etree.Element("div", {"number": str(div_name)}))
        else:
            div_parent.append(etree.Element("div", {"number": str(div_name)}))

    def update_div(self, version_title, div_path, new_div_name):
        div_xpath = "/".join(["text"] + ["div[@number='{}']".format(div_number) for div_number in div_path])
        div = self._get(div_xpath, attribute=None, on_element=self._get("version", {"title": version_title}))
        div.set("number", new_div_name)
        self._renumber_units()

    def del_div(self, version_title, div_path):
        div_xpath = "/".join(["text"] + ["div[@number='{}']".format(div_number) for div_number in div_path])
        div = self._get(div_xpath, attribute=None, on_element=self._get("version", {"title": version_title}))
        div.getparent().remove(div)
        self._renumber_units()

    def add_unit(self, version_title, div_path):
        parent_div_xpath = "/".join(["text"] + ["div[@number='{}']".format(div_number) for div_number in div_path])
        parent_div = self._get(parent_div_xpath,
                               attribute=None,
                               on_element=self._get("version", {"title": version_title}))
        etree.SubElement(parent_div, "unit", {"id": "0"}).append(etree.Element("reading"))
        self._renumber_units()

    def update_unit(self, version_title, unit_id, readings):
        unit = self._get("//unit", {"id": str(unit_id)}, self._get("version", {"title": version_title}))
        unit.clear()
        unit.set("id", unit_id)
        for index, reading in enumerate(readings):
            etree.SubElement(unit, "reading", {"option": str(index), "mss": reading[0]}).text = reading[1]

    def split_unit(self, version_title, unit_id, reading_pos, split_point):
        unit = self._get("//unit", {"id": str(unit_id)}, self._get("version", {"title": version_title}))
        reading_pos = int(reading_pos)
        if -1 < reading_pos < len(unit):
            reading = unit[reading_pos]
            if isinstance(split_point, basestring) and split_point in reading.text:
                reading_parts = reading.text.split(split_point)
                # prev elem
                prev_elem = etree.Element("reading", {"option": "0", "mss": reading.get("mss")})
                prev_elem.text = reading_parts[0]
                reading.addprevious(prev_elem)
                # current elem
                reading.text = split_point
                # next elem
                next_elem = etree.Element("reading", {"option": "0", "mss": reading.get("mss")})
                next_elem.text = reading_parts[1]
                reading.addnext(next_elem)
            elif isinstance(split_point, int):
                next_elem = etree.Element("reading", {"option": "0", "mss": reading.get("mss")})
                next_elem.text = reading.text[split_point:]
                reading.addnext(next_elem)
                reading.text = reading.text[:split_point]
            # renumbering the option attribute
            for index, reading in enumerate(unit):
                reading.set("option", str(index))
        else:
            raise ElementDoesNotExist('<unit id="{}"> has no reading at position {}'.format(unit_id, reading_pos))

    def del_unit(self, version_title, unit_id):
        unit = self._get("//unit", {"id": str(unit_id)}, self._get("version", {"title": version_title}))
        unit.getparent().remove(unit)
        self._renumber_units()

    def serialize(self, pretty=True):
        return etree.tostring(self._book,
                              xml_declaration=True,
                              pretty_print=pretty,
                              **self._docinfo)

    def save(self):
        BookManager._save(self)

## BookManager class


class BookManager(object):
    """
    Facade class for Books, it can
    - manage loading/saving books
    - manipulate more books in one step
    """

    xml_file_storage_path = XML_FILE_STORAGE_PATH
    xml_file_backup_storage_path = XML_FILE_BACKUP_STORAGE_PATH
    xml_draft_file_storage_path = XML_DRAFT_FILE_STORAGE_PATH
    xml_draft_file_backup_storage_path = XML_DRAFT_FILE_BACKUP_STORAGE_PATH

    @staticmethod
    def _load(book_name):
        """
        Load the given book from the draft folder

        :param book_name: the name of the book
        :return: file-like object
        """
        # TODO: add loading from cache option
        return open(("{}/{}.xml".format(BookManager.xml_draft_file_storage_path, book_name)), "r")

    @staticmethod
    def _save(book_object):
        """
        Save the given book to the draft folder with backup

        :param book_object: a Book instance
        """
        # TODO: add saving into cache option
        book_name = book_object.get_filename()
        new_file_path = "{}/{}.xml".format(BookManager.xml_draft_file_storage_path, book_name)
        if os.path.isfile(new_file_path):
            backup_file_path = "{}/{}_{}.xml".format(BookManager.xml_draft_file_backup_storage_path,
                                                     book_name,
                                                     datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
            os.rename(new_file_path, backup_file_path)
        f = open(new_file_path, "w")
        f.write(book_object.serialize())
        f.close()

    @staticmethod
    def get_text(text_positions, as_gluon=True):
        """
        Retrieving sections of text in running form

        :param text_positions: a list of dictionaries with the following key/value pairs
        {"book": <string, the file name of the requested xml file>
         "version": <string, the title of the requested version>
         "text_type": <string, type of the requested text>
         "start": <tuple, identifying the starting point of the requested text section>
         "end": <tuple, identifying the end point of the requested text section (optional)> }
        :param as_gluon: Be the items are wrapped into gluon objects or not?
        :return: dictionary with the following key/value pairs
        {"result": <list of reading fragments based on the arguments in the requested form>,
        "error": <list of error messages (as many items as text_positions has))>}
        """
        items = []
        errors = []
        for text_position in text_positions:
            try:
                book = Book.open(BookManager._load(text_position.get("book", "")))
                book_items = []
                for item in book.get_text(text_position.get("version", ""),
                                          text_position.get("text_type", ""),
                                          text_position.get("start"),
                                          text_position.get("end")):
                    if as_gluon:
                        item_text = item.text if item.text else "*"
                        book_items.append(SPAN(A(item_text, _href=str(item.readings_in_unit))
                                          if item.readings_in_unit > 1 else item_text,
                                          _id=item.unit_id,
                                          _class="{} {}".format(item.language, item.readings_in_unit)))
                    else:
                        book_items.append(item)
                if book_items:
                    if as_gluon:
                        items.append(DIV(book_items))
                    else:
                        items += book_items
            except IOError as e:
                errors.append(str(e))
            except ElementDoesNotExist as e:
                errors.append(e.message)
            except MultipleElementsReturned as e:
                errors.append(e.message)
            else:
                errors.append(None)
        return {"result": items, "error": errors}

    @staticmethod
    def get_readings(unit_descriptions, as_gluon=True):
        """
        Retrieving the text of all readings for one unit of the XML file

        :param unit_descriptions: a list of dictionaries with the following key/value pairs
        {"book": <string, the file name of the xml file to be read>
         "unit_id": <integer, identifier of the requested unit> )
        :param as_gluon: Be the items are wrapped into gluon objects or not?
        :return: dictionary with the following key/value pairs
        {"result": <list of reading fragments based on the arguments in the requested form>,
        "error": <list of error messages (as many items as unit_descriptions has))>}
        """
        items = []
        errors = []
        for unit_description in unit_descriptions:
            try:
                book = Book.open(BookManager._load(unit_description.get("book", "")))
                book_items = []
                for item in book.get_readings(unit_description.get("unit_id")):
                    if as_gluon:
                        book_items.append(TAG.dt(item.mss))
                        book_items.append(TAG.dd(item.text if item.text else "*"))
                    else:
                        book_items.append(item)
                if as_gluon:
                    items.append(TAG.dl(book_items))
                else:
                    items += book_items
            except IOError as e:
                errors.append(str(e))
            else:
                errors.append(None)
        return {"result": items, "error": errors}

    @staticmethod
    def create_book(book_name, book_title, frags=False):
        """
        Create and save a new book in the draft folder

        :param book_title:
        :param frags: When it's True, the textStructure attribute of <book> will be "fragmentary"
        :param book_name:
        :return:
        """
        Book.create(book_name, book_title, frags).save()

    @staticmethod
    def copy_book(book_name):
        """
        Copy a book from the main storage place to the draft folder

        :param book_name: string
        :return:
        """
        from_file_path = "{}/{}.xml".format(BookManager.xml_file_storage_path, book_name)
        to_file_path = "{}/{}.xml".format(BookManager.xml_draft_file_storage_path, book_name)
        if os.path.isfile(to_file_path):
            backup_to_file_path = "{}/{}_{}.xml".format(BookManager.xml_draft_file_backup_storage_path,
                                                        book_name,
                                                        datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
            os.rename(to_file_path, backup_to_file_path)
        f = open(to_file_path, "w")
        f.write(open(from_file_path).read())
        f.close()

    @staticmethod
    def publish_book(book_name):
        """
        Copy a book from draft folder to the main storage place

        :param book_name:
        :return:
        """
        from_file_path = "{}/{}.xml".format(BookManager.xml_draft_file_storage_path, book_name)
        to_file_path = "{}/{}.xml".format(BookManager.xml_file_storage_path, book_name)
        if os.path.isfile(to_file_path):
            backup_to_file_path = "{}/{}_{}.xml".format(BookManager.xml_file_backup_storage_path,
                                                        book_name,
                                                        datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
            os.rename(to_file_path, backup_to_file_path)
        f = open(to_file_path, "w")
        f.write(open(from_file_path).read())
        f.close()

    @staticmethod
    def add_version(book_name, version_title, language, author):
        """
        Add <version> node to the book structure with the given attributes

        :param book_name:
        :param version_title:
        :param language:
        :param author:
        """
        book = Book.open(BookManager._load(book_name))
        book.add_version(version_title, language, author)
        book.save()

    @staticmethod
    def update_version(book_name, version_title, new_version_title=None, new_language=None, new_author=None):
        """
        Update the given <version> node with the given attributes

        :param book_name:
        :param version_title:
        :param new_version_title:
        :param new_language:
        :param new_author:
        """
        book = Book.open(BookManager._load(book_name))
        book.update_version(version_title, new_version_title, new_language, new_author)
        book.save()

    @staticmethod
    def del_version(book_name, version_title):
        """
        Remove the given <version> node

        :param book_name:
        :param version_title:
        """
        book = Book.open(BookManager._load(book_name))
        book.del_version(version_title)
        book.save()

    @staticmethod
    def add_manuscript(book_name, version_title, abbrev, language, show=True):
        """
        Add <ms> node to the given <version>/<manuscripts> node

        :param book_name:
        :param version_title:
        :param abbrev:
        :param language:
        :param show:
        """
        book = Book.open(BookManager._load(book_name))
        book.add_manuscript(version_title, abbrev, language, show)
        book.save()

    @staticmethod
    def update_manuscript(book_name, version_title, abbrev, new_abbrev, new_language=None, new_show=None):
        """
        Update <ms> node under the given <version>/<manuscrips> with the given attributes

        :param book_name:
        :param version_title:
        :param abbrev:
        :param new_abbrev:
        :param new_language:
        :param new_show:
        """
        book = Book.open(BookManager._load(book_name))
        book.update_manuscript(version_title, abbrev, new_abbrev, new_language, new_show)
        book.save()

    @staticmethod
    def del_manuscript(book_name, version_title, abbrev):
        """
        Remove <ms> node from the given <version>/<manuscrips> node

        :param book_name:
        :param version_title:
        :param abbrev:
        """
        book = Book.open(BookManager._load(book_name))
        book.del_manuscript(version_title, abbrev)
        book.save()

    @staticmethod
    def add_bibliography(book_name, version_title, abbrev, text):
        """
        Add <bibliography> node to the given <version>/<manuscrips>/<ms> node

        :param book_name:
        :param version_title:
        :param abbrev:
        :param text:
        """
        book = Book.open(BookManager._load(book_name))
        book.add_bibliography(version_title, abbrev, text)
        book.save()

    @staticmethod
    def update_bibliography(book_name, version_title, abbrev, bibliography_pos, new_text):
        """
        Update <bibliography> node under the given <version>/<manuscrips>/<ms> node with the given attributes

        :param book_name:
        :param version_title:
        :param abbrev:
        :param bibliography_pos: zero based position of the bibliography node inside <ms> node
        :param new_text:
        """
        book = Book.open(BookManager._load(book_name))
        book.update_bibliography(version_title, abbrev, bibliography_pos, new_text)
        book.save()

    @staticmethod
    def del_bibliography(book_name, version_title, abbrev, bibliography_pos):
        """
        Remove <bibliography> node from the given <version>/<manuscrips>/<ms> node

        :param book_name:
        :param version_title:
        :param abbrev:
        :param bibliography_pos: zero based position of the bibliography node inside <ms> node
        """
        book = Book.open(BookManager._load(book_name))
        book.del_bibliography(version_title, abbrev, bibliography_pos)
        book.save()

    @staticmethod
    def add_div(book_name, version_title, div_name, div_parent_path, preceding_div):
        """
        Add new <div> node to a book under the given <version>/text/<div_parent_path> with the given div_name

        :param book_name: string
        :param version_title: string
        :param div_name: string, this is the 'number' attribute of the div
        :param div_parent_path: list, list of ancestor <div> nodes
        :param preceding_div:  string, insert the new <div> node after the <div> node with this name
        """
        book = Book.open(BookManager._load(book_name))
        book.add_div(version_title, div_name, div_parent_path, preceding_div)
        book.save()

    @staticmethod
    def update_div(book_name, version_title, div_path, new_div_name):
        """
        Update the <div> node at the last position of the div_path with the given new_div_name

        :param book_name:
        :param version_title:
        :param div_path: list, list of <div> nodes to the desired <div>
        :param new_div_name:
        """
        book = Book.open(BookManager._load(book_name))
        book.update_div(version_title, div_path, new_div_name)
        book.save()

    @staticmethod
    def del_div(book_name, version_title, div_path):
        """
        Remove the <div> node from the end of the given div_path

        :param book_name:
        :param version_title:
        :param div_path: list, list of <div> nodes to the desired <div>
        """
        book = Book.open(BookManager._load(book_name))
        book.del_div(version_title, div_path)
        book.save()

    @staticmethod
    def add_unit(book_name, version_title, div_path):
        """
        Add <unit> node to the given <version>/text/<div_path>

        :param book_name:
        :param version_title:
        :param div_path: list, list of <div> nodes to the desired <div>
        """
        book = Book.open(BookManager._load(book_name))
        book.add_unit(version_title, div_path)
        book.save()

    @staticmethod
    def update_unit(book_name, version_title, unit_id, readings):
        """
        Update <unit> node with the given <readings> elements.
        This method clears the existing <reading> nodes from the given <unit> before popuplates with the new <reading>s.

        :param book_name:
        :param version_title:
        :param unit_id: number in integer or string type
        :param readings: list of tuples, each of which represents one <reading> element in the <unit>. 
        Each tuple should contain two items: 
        1) a string representing the "mss” value of the updated <reading>
        2) a string representing the text content of that <reading>
        """
        book = Book.open(BookManager._load(book_name))
        book.update_unit(version_title, unit_id, readings)
        book.save()

    @staticmethod
    def split_unit(book_name, version_title, unit_id, reading_pos, split_point):
        """
        This actually splits a <reading> node under the given <unit> into 2 or 3 pieces.
        If this split_point argument is an integer, that should be interpreted as the index within 
        the text of the <reading> where the split should be made (a 2­way split). 
        If this argument is a string, that should be interpreted as the text to be contined
        in the middle <reading> of a 3­way split, with the preceding and following characters being moved 
        to the new <reading>s added before and after this middle <reading>.

        :param book_name:
        :param version_title:
        :param unit_id: number in integer or string type
        :param reading_pos: number in integer or string type
        :param split_point: integer or string
        """
        book = Book.open(BookManager._load(book_name))
        book.split_unit(version_title, unit_id, reading_pos, split_point)
        book.save()

    @staticmethod
    def del_unit(book_name, version_title, unit_id):
        """
        Remove <unit> node from the given <version> node

        :param book_name:
        :param version_title:
        :param unit_id: number in integer or string type
        """
        book = Book.open(BookManager._load(book_name))
        book.del_unit(version_title, unit_id)
        book.save()


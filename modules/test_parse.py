# -*- coding: utf-8 -*-

from StringIO import StringIO

import pytest

from modules.parse import Book
from modules.parse import InvalidDocumentException

XML_FILE = "test/docs/test.xml"
DTD_FILE = "static/docs/grammateus.dtd"


@pytest.fixture(scope="module")
def sample_book():
    return Book(open(XML_FILE))


def test_false_init():
    with pytest.raises(TypeError):
        Book(1)


def test_validation(sample_book):
    # validation without success
    book = Book(StringIO("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <!DOCTYPE book SYSTEM "grammateus.dtd">
        <book></book>"""))
    with pytest.raises(InvalidDocumentException):
        book.validate(open(DTD_FILE))
    # validation with success
    assert sample_book.validate(open(DTD_FILE)) is None

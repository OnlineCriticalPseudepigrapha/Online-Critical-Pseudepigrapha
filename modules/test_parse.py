# -*- coding: utf-8 -*-

from StringIO import StringIO
from collections import namedtuple

import pytest

from modules.parse import Book
from modules.parse import InvalidDocument

XML_FILE = "test/docs/test.xml"
DTD_FILE = "static/docs/grammateus.dtd"


@pytest.fixture(scope="module")
def test_book():
    return Book(open(XML_FILE))


def test_false_init():
    with pytest.raises(TypeError):
        Book(1)


def test_validation(test_book):
    # validation without success
    book = Book(StringIO("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <!DOCTYPE book SYSTEM "grammateus.dtd">
        <book></book>"""))
    with pytest.raises(InvalidDocument):
        book.validate(open(DTD_FILE))
    # validation with success
    assert test_book.validate(open(DTD_FILE)) is None


def test_gen_divpath_open_end():
    assert Book.gen_divpath(start_div=(1,)) == ["div[@number>=1]"]
    assert Book.gen_divpath(start_div=(1, 2)) == ["div[@number=1]/div[@number>=2]",
                                                  "div[@number>1]/div"]
    assert Book.gen_divpath(start_div=(1, 2, 3)) == ["div[@number=1]/div[@number=2]/div[@number>=3]",
                                                     "div[@number=1]/div[@number>2]/div",
                                                     "div[@number>1]/div/div"]


def test_gen_divpath_open_start():
    assert Book.gen_divpath(end_div=("7",)) == ["div[@number<=7]"]
    assert Book.gen_divpath(end_div=("7", "8")) == ["div[@number<7]/div",
                                                    "div[@number=7]/div[@number<=8]"]
    assert Book.gen_divpath(end_div=("7", "8", "9")) == ["div[@number<7]/div/div",
                                                         "div[@number=7]/div[@number<8]/div",
                                                         "div[@number=7]/div[@number=8]/div[@number<=9]"]


def test_gen_divpath_same_depth_1():
    assert Book.gen_divpath((1,), (1,)) == ["div[@number=1]"]
    assert Book.gen_divpath((1,), (2,)) == ["div[@number>=1 and @number<=2]"]
    assert Book.gen_divpath((1,), (3,)) == ["div[@number>=1 and @number<=3]"]


def test_gen_divpath_same_depth_2():
    assert Book.gen_divpath((1, 2), (1, 2)) == ["div[@number=1]/div[@number=2]"]
    assert Book.gen_divpath((1, 2), (1, 3)) == ["div[@number=1]/div[@number>=2 and @number<=3]"]
    assert Book.gen_divpath((1, 2), (1, 4)) == ["div[@number=1]/div[@number>=2 and @number<=4]"]
    # TODO: the second path is unnecessary, we should optimize it
    assert Book.gen_divpath((1, 2), (2, 4)) == ["div[@number=1]/div[@number>=2]",
                                                "div[@number>1 and @number<2]/div",
                                                "div[@number=2]/div[@number<=4]"]
    assert Book.gen_divpath((1, 2), (3, 4)) == ["div[@number=1]/div[@number>=2]",
                                                "div[@number>1 and @number<3]/div",
                                                "div[@number=3]/div[@number<=4]"]


def test_gen_divpath_same_depth_3():
    assert Book.gen_divpath((1, 2, 3), (1, 2, 3)) == ["div[@number=1]/div[@number=2]/div[@number=3]"]
    assert Book.gen_divpath((1, 2, 3), (1, 2, 4)) == ["div[@number=1]/div[@number=2]/div[@number>=3 and @number<=4]"]
    # TODO: the second path is unnecessary, we should optimize it
    assert Book.gen_divpath((1, 2, 3), (1, 3, 4)) == ["div[@number=1]/div[@number=2]/div[@number>=3]",
                                                      "div[@number=1]/div[@number>2 and @number<3]/div",
                                                      "div[@number=1]/div[@number=3]/div[@number<=4]"]
    assert Book.gen_divpath((1, 2, 3), (2, 3, 4)) == ["div[@number=1]/div[@number=2]/div[@number>=3]",
                                                      "div[@number=1]/div[@number>2]/div",
                                                      "div[@number>1 and @number<2]/div/div",
                                                      "div[@number=2]/div[@number<3]/div",
                                                      "div[@number=2]/div[@number=3]/div[@number<=4]"]


def test_gen_divpath_invalid_args():
    assert Book.gen_divpath((1, 2), (1,)) == []
    assert Book.gen_divpath((1, 2, 3), (1, 2)) == []
    assert Book.gen_divpath((2, 3), (1,)) == []
    assert Book.gen_divpath((2,), (1,)) == []
    assert Book.gen_divpath((2,), (1, 2)) == []
    assert Book.gen_divpath((2,), (1, 2, 3)) == []


def test_gen_divpath_diff_depth_1():
    assert Book.gen_divpath((1, 2), (3,)) == ["div[@number=1]/div[@number>=2]",
                                              "div[@number>1 and @number<=3]/div"]
    assert Book.gen_divpath((1, 2, 3), (4,)) == ["div[@number=1]/div[@number=2]/div[@number>=3]",
                                                 "div[@number=1]/div[@number>2]/div",
                                                 "div[@number>1 and @number<=4]/div/div"]
    assert Book.gen_divpath((1, 2, 3), (4, 5)) == ["div[@number=1]/div[@number=2]/div[@number>=3]",
                                                   "div[@number=1]/div[@number>2]/div",
                                                   "div[@number>1 and @number<4]/div/div",
                                                   "div[@number=4]/div[@number<=5]"]


def test_gen_divpath_diff_depth_2():
    assert Book.gen_divpath((1,), (1, 2)) == ["div[@number=1]/div[@number<=2]"]
    assert Book.gen_divpath((1,), (2, 3)) == ["div[@number>=1 and @number<2]",
                                              "div[@number=2]/div[@number<=3]"]
    assert Book.gen_divpath((1,), (3, 4)) == ["div[@number>=1 and @number<3]",
                                              "div[@number=3]/div[@number<=4]"]
    assert Book.gen_divpath((1,), (3, 4, 5)) == ["div[@number>=1 and @number<3]",
                                                 "div[@number=3]/div[@number<4]/div",
                                                 "div[@number=3]/div[@number=4]/div[@number<=5]"]
    assert Book.gen_divpath((1, 2), (3, 4, 5)) == ["div[@number=1]/div[@number>=2]",
                                                   "div[@number>1 and @number<3]/div",
                                                   "div[@number=3]/div[@number<4]/div",
                                                   "div[@number=3]/div[@number=4]/div[@number<=5]"]


def test_book_get_text(test_book):
    Reading = namedtuple("Reading", "unit_id, language, readings_in_unit, text")
    assert test_book.get_text("Greek", "TestOne", (1,)) == [Reading("812", "Greek", 3, u"ἰδοὺ ἦλθεν κύριος "),
                                                            Reading("815", "Greek", 3, u"ἐλέγξαι "),
                                                            Reading("816", "Greek", 2, u"πάντας τοὺς ἀσεβεῖς, ")]


def test_book_get_hidden_text(test_book):
    Reading = namedtuple("Reading", "unit_id, language, readings_in_unit, text")
    assert test_book.get_text("Greek", "TestTwo", (1,)) == []
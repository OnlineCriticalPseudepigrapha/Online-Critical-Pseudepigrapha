# -*- coding: utf-8 -*-
from collections import OrderedDict
import glob

import os
from StringIO import StringIO

import pytest

from parse import Text, Reading, W
from parse import Book, BookManager
from parse import ElementDoesNotExist, InvalidDIVPath, NotAllowedManuscript

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

XML_FILE_STORAGE_PATH = os.path.join(PROJECT_ROOT, "test/docs")
XML_FILE_BACKUP_STORAGE_PATH = os.path.join(PROJECT_ROOT, "test/docs/backups")
XML_DRAFT_FILE_STORAGE_PATH = os.path.join(PROJECT_ROOT, "test/docs/drafts")
XML_DRAFT_FILE_BACKUP_STORAGE_PATH = os.path.join(PROJECT_ROOT, "test/docs/drafts/backups")

TEST_XML_FILE = os.path.join(PROJECT_ROOT, "test/docs/drafts/test_parse.xml")
TEST_DTD_FILE = os.path.join(PROJECT_ROOT, "static/docs/grammateus.dtd")

BookManager.xml_file_storage_path = XML_FILE_STORAGE_PATH
BookManager.xml_file_backup_storage_path = XML_FILE_BACKUP_STORAGE_PATH
BookManager.xml_draft_file_storage_path = XML_DRAFT_FILE_STORAGE_PATH
BookManager.xml_draft_file_backup_storage_path = XML_DRAFT_FILE_BACKUP_STORAGE_PATH


@pytest.fixture(scope="module")
def test_book():
    return Book.open(open(TEST_XML_FILE))


@pytest.fixture()
def new_book():
    book = Book.create(filename="MyTest", title="My Test Book", frags=True)
    book.add_version(version_title="MyVersion", language="MyLanguage", author="Me")
    return book


def test_book_false_init():
    with pytest.raises(TypeError):
        Book.open(1)


def test_book_validation_w_dtd_invalid_doc():
    book = Book.open(StringIO("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <!DOCTYPE book SYSTEM "grammateus.dtd">
        <book></book>"""))
    assert book.validate(open(TEST_DTD_FILE)) is False


def test_book_validation_w_dtd_valid_and_semantically_invalid_doc(test_book):
    expected_errors = ["<version title='Qumran Aramaic'>//<unit id='684'> has wrong id. It should be '1'.",
                       "<version title='Latin Fragments'> has missing manuscript definition(s) which are in use: CB185,TertullianB",
                       "<version title='Latin Fragments'>//<unit id='755'> has wrong id. It should be '1'.",
                       "<version title='Greek'> has missing manuscript definition(s) which are in use: Gizeh*,Swete,F-R,Charles,Syncellus2,Black,Dindorf,Bonner,Lods,Ε,Goar,Dillman,Kenyon",
                       "<version title='Greek'>//<unit id='788'> has wrong id. It should be '1'.",
                       "<version title='Greek'/text/div number='107'> has <div> with not unique name (number)",
                       ]
    assert test_book.validate(open(TEST_DTD_FILE)) is False
    assert test_book.validation_errors == expected_errors


## Testing RI


def test_book_get_text(test_book):
    result_list = list(test_book.get_text("Greek", "TestOne", (107,)))
    expected_list = [Text(("107", "1"), "1347", "Greek", 1, "", "", None),
                     Text(("107", "2"), "1348", "Greek", 1, "", "", None),
                     Text(("107", "2"), "1349", "Greek", 1, "", "", None)]
    assert result_list == expected_list


def test_book_get_text_w_same_start_and_end_at_level_1(test_book):
    result_list = list(test_book.get_text("Greek", "TestOne", (1,), (1,)))
    expected_list = [Text(("1", "1"), "788", "Greek", 2, "", "", u"Λόγος"),
                     Text(("1", "2"), "789", "Greek", 1, "", "", None),
                     Text(("1", "2"), "790", "Greek", 1, "", "", None),
                     Text(("1", "2"), "791", "Greek", 1, "", "", None),
                     Text(("1", "2"), "792", "Greek", 2, "", "", None),
                     Text(("1", "2"), "793", "Greek", 1, "", "", None),
                     Text(("1", "2"), "794", "Greek", 1, "", "", None),
                     Text(("1", "2"), "795", "Greek", 1, "", "", None),
                     Text(("1", "2"), "796", "Greek", 1, "", "", None),
                     Text(("1", "3"), "797", "Greek", 1, "", "", None),
                     Text(("1", "3"), "798", "Greek", 1, "", "", None),
                     Text(("1", "4"), "799", "Greek", 1, "", "", None),
                     Text(("1", "4"), "800", "Greek", 1, "", "", None),
                     Text(("1", "4"), "801", "Greek", 1, "", "", None),
                     Text(("1", "5"), "802", "Greek", 1, "", "", None),
                     Text(("1", "5"), "803", "Greek", 2, "", "", None),
                     Text(("1", "5"), "804", "Greek", 1, "", "", None),
                     Text(("1", "6"), "805", "Greek", 1, "", "", None),
                     Text(("1", "6"), "806", "Greek", 2, "", "", None),
                     Text(("1", "6"), "807", "Greek", 1, "", "", None),
                     Text(("1", "7"), "808", "Greek", 1, "", "", None),
                     Text(("1", "8"), "809", "Greek", 1, "", "", None),
                     Text(("1", "8"), "810", "Greek", 2, "", "", None),
                     Text(("1", "8"), "811", "Greek", 1, "", "", None),
                     Text(("1", "9"), "812", "Greek", 3, "yes", "", u""),
                     Text(("1", "9"), "813", "Greek", 3, "", "", None),
                     Text(("1", "9"), "814", "Greek", 1, "", "", None),
                     Text(("1", "9"), "815", "Greek", 3, "", "yes", u"ἐλέγξαι "),
                     Text(("1", "9"), "816", "Greek", 1, "", "", u"πάντας τοὺς ἀσεβεῖς, "),
                     Text(("1", "9"), "817", "Greek", 2, "", "", None),
                     Text(("1", "9"), "818", "Greek", 1, "", "", None),
                     Text(("1", "9"), "819", "Greek", 2, "", "", None),
                     Text(("1", "9"), "820", "Greek", 1, "", "", None),
                     Text(("1", "9"), "821", "Greek", 2, "", "", None),
                     Text(("1", "9"), "822", "Greek", 2, "", "", None),
                     Text(("1", "9"), "823", "Greek", 1, "", "", None)]
    assert result_list == expected_list


def test_book_get_text_w_first_one(test_book):
    result_list = list(test_book.get_text("Greek", "TestOne", (1, 1), (1, 1)))
    expected_list = [Text(("1", "1"), "788", "Greek", 2, "", "", u"Λόγος")]
    assert result_list == expected_list


def test_book_get_text_w_last_one(test_book):
    result_list = list(test_book.get_text("Greek", "TestOne", (2, 2), (2, 2)))
    expected_list = [Text(("2", "2"), "826", "Greek", 1, "", "", None),
                     Text(("2", "2"), "827", "Greek", 3, "", "", None),
                     Text(("2", "2"), "828", "Greek", 2, "", "", ("Lorem ",
                                                                  W({"morph": "morph",
                                                                     "lex": "lex",
                                                                     "style": "style",
                                                                     "lang": "lang"}, "ipsum"),
                                                                  " dolor ",
                                                                  W({}, u"sit"),
                                                                  " amet"))]
    assert result_list == expected_list


def test_book_get_text_w_end(test_book):
    result_list = list(test_book.get_text("Greek", "TestOne", (1, 9), (2,)))
    expected_list = [Text(("1", "9"), "812", "Greek", 3, "yes", "", u""),
                     Text(("1", "9"), "813", "Greek", 3, "", "", None),
                     Text(("1", "9"), "814", "Greek", 1, "", "", None),
                     Text(("1", "9"), "815", "Greek", 3, "", "yes", u"ἐλέγξαι "),
                     Text(("1", "9"), "816", "Greek", 1, "", "", u"πάντας τοὺς ἀσεβεῖς, "),
                     Text(("1", "9"), "817", "Greek", 2, "", "", None),
                     Text(("1", "9"), "818", "Greek", 1, "", "", None),
                     Text(("1", "9"), "819", "Greek", 2, "", "", None),
                     Text(("1", "9"), "820", "Greek", 1, "", "", None),
                     Text(("1", "9"), "821", "Greek", 2, "", "", None),
                     Text(("1", "9"), "822", "Greek", 2, "", "", None),
                     Text(("1", "9"), "823", "Greek", 1, "", "", None),
                     Text(("2", "1"), "824", "Greek", 1, "", "", None),
                     Text(("2", "1"), "825", "Greek", 2, "", "", u"καὶ"),
                     Text(("2", "2"), "826", "Greek", 1, "", "", None),
                     Text(("2", "2"), "827", "Greek", 3, "", "", None),
                     Text(("2", "2"), "828", "Greek", 2, "", "", ("Lorem ",
                                                                  W({"morph": "morph",
                                                                     "lex": "lex",
                                                                     "style": "style",
                                                                     "lang": "lang"}, "ipsum"),
                                                                  " dolor ",
                                                                  W({}, u"sit"),
                                                                  " amet")),
                     Text(("2", "3"), "829", "Greek", 1, "", "", None)]
    assert result_list == expected_list


def test_book_get_text_w_invalid_start_and_end(test_book):
    result_list = list(test_book.get_text("Greek", "TestOne", (1, 9, 3, 4, 5), (2, 2, "X", "Y")))
    expected_list = [Text(("1", "9"), "812", "Greek", 3, "yes", "", u""),
                     Text(("1", "9"), "813", "Greek", 3, "", "", None),
                     Text(("1", "9"), "814", "Greek", 1, "", "", None),
                     Text(("1", "9"), "815", "Greek", 3, "", "yes", u"ἐλέγξαι "),
                     Text(("1", "9"), "816", "Greek", 1, "", "", u"πάντας τοὺς ἀσεβεῖς, "),
                     Text(("1", "9"), "817", "Greek", 2, "", "", None),
                     Text(("1", "9"), "818", "Greek", 1, "", "", None),
                     Text(("1", "9"), "819", "Greek", 2, "", "", None),
                     Text(("1", "9"), "820", "Greek", 1, "", "", None),
                     Text(("1", "9"), "821", "Greek", 2, "", "", None),
                     Text(("1", "9"), "822", "Greek", 2, "", "", None),
                     Text(("1", "9"), "823", "Greek", 1, "", "", None),
                     Text(("2", "1"), "824", "Greek", 1, "", "", None),
                     Text(("2", "1"), "825", "Greek", 2, "", "", u"καὶ"),
                     Text(("2", "2"), "826", "Greek", 1, "", "", None),
                     Text(("2", "2"), "827", "Greek", 3, "", "", None),
                     Text(("2", "2"), "828", "Greek", 2, "", "", ("Lorem ",
                                                                  W({"morph": "morph",
                                                                     "lex": "lex",
                                                                     "style": "style",
                                                                     "lang": "lang"}, "ipsum"),
                                                                  " dolor ",
                                                                  W({}, u"sit"),
                                                                  " amet"))]
    assert result_list == expected_list


def test_book_get_text_w_invalid_start_and_end_position_pair(test_book):
    with pytest.raises(InvalidDIVPath):
        list(test_book.get_text("Greek", "TestOne", (1, 2), (1, 1)))


def test_book_get_text_w_not_allowed_manuscript(test_book):
    with pytest.raises(NotAllowedManuscript):
        list(test_book.get_text("Greek", "TestTwo", (1,)))


def test_book_get_text_w_invalid_version(test_book):
    with pytest.raises(ElementDoesNotExist):
        list(test_book.get_text("XGreek", "TestOne", (1,)))


def test_book_get_text_w_invalid_text_type(test_book):
    with pytest.raises(ElementDoesNotExist):
        list(test_book.get_text("Greek", "XTestOne", (1,)))


def test_book_get_readings(test_book):
    result = list(test_book.get_readings("Greek", 812))
    expected = [Reading("Gizeh", u"ὅτι ἔρχεται"),
                Reading("Jude", u"ἰδοὺ ἦλθεν κύριος"),
                Reading("TestOne", u"")]
    assert result == expected


def test_book_get_readings_w_invalid_unit_id(test_book):
    result = list(test_book.get_readings("Greek", 2000))
    expected = []
    assert result == expected


def test_book_get_unit_group(test_book):
    result = list(test_book.get_unit_group("Greek", 812))
    expected = [10, 14]
    assert result == expected


def test_book_get_unit_group_w_invalid_unit_id(test_book):
    result = list(test_book.get_readings("Greek", 2000))
    expected = []
    assert result == expected


def test_book_get_group(test_book):
    result = test_book.get_group("Greek", 14)
    expected = OrderedDict({"812": [Reading("Gizeh", u"ὅτι ἔρχεται"),
                                    Reading("Jude", u"ἰδοὺ ἦλθεν κύριος"),
                                    Reading("TestOne", u"")],
                            "813": [Reading("Gizeh", u"σὺν ταῖς μυριάσιν αὐτοῦ καὶ τοῖς ἁγίοις αὐτοῦ,"),
                                    Reading("Jude", u"ἐν ἁγίαις μυριάσιν αὐτοῦ,"),
                                    Reading("TestTwo", u"ἐν ἁγίαις μυριάσιν αὐτοῦ,")],
                            "814": [Reading("Gizeh Jude", u"ποιῆσαι κρίσιν κατὰ πάντων, καὶ")]})
    assert result == expected


def test_book_get_group_w_invalid_group_id(test_book):
    result = test_book.get_group("Greek", "2000")
    expected = OrderedDict()
    assert result == expected


## BookManager tests


def test_bookman_get_text():
    result = BookManager.get_text([{"book": "test_parse", "version": "Greek", "text_type": "TestOne",
                                    "start": (1, 1), "end": (1, 1)},
                                   {"book": "test_parse", "version": "Greek", "text_type": "TestOne",
                                    "start": (1, 1), "end": (1, 1)}],
                                  as_gluon=False)
    expected = {"result": [Text(("1", "1"), "788", "Greek", 2, "", "", u"Λόγος"),
                           Text(("1", "1"), "788", "Greek", 2, "", "", u"Λόγος")],
                "error": [None, None]}
    assert result == expected


def test_bookman_get_text_w_invalid_book():
    result = BookManager.get_text([{"book": "Xtest_parse", "version": "Greek", "text_type": "TestOne", "start": (1,)}],
                                  as_gluon=False)
    expected = {"result": [],
                "error": ["[Errno 2] No such file or directory: '{}/Xtest_parse.xml'".format(
                    XML_DRAFT_FILE_STORAGE_PATH)]}
    assert result == expected


def test_bookman_get_text_w_invalid_version():
    result = BookManager.get_text([{"book": "test_parse", "version": "XGreek", "text_type": "TestOne", "start": (1,)}],
                                  as_gluon=False)
    expected = {"result": [],
                "error": ["<version> element with title='XGreek' does not exist"]}
    assert result == expected


def test_bookman_get_text_w_mixed_valid_and_invalid():
    result = BookManager.get_text([{"book": "test_parse", "version": "Greek", "text_type": "TestOne",
                                    "start": (1, 1), "end": (1, )},
                                   {"book": "Xtest_parse", "version": "Greek", "text_type": "TestOne",
                                    "start": (1,)},
                                   {"book": "test_parse", "version": "Greek", "text_type": "TestOne",
                                    "start": (2, ), "end": (2, )},
                                   {"book": "test_parse", "version": "XGreek", "text_type": "TestOne",
                                    "start": (1,)}],
                                  as_gluon=False)
    expected = {"result": [Text(("1", "1"), "788", "Greek", 2, "", "", u"Λόγος"),
                           Text(("1", "2"), "789", "Greek", 1, "", "", None),
                           Text(("1", "2"), "790", "Greek", 1, "", "", None),
                           Text(("1", "2"), "791", "Greek", 1, "", "", None),
                           Text(("1", "2"), "792", "Greek", 2, "", "", None),
                           Text(("1", "2"), "793", "Greek", 1, "", "", None),
                           Text(("1", "2"), "794", "Greek", 1, "", "", None),
                           Text(("1", "2"), "795", "Greek", 1, "", "", None),
                           Text(("1", "2"), "796", "Greek", 1, "", "", None),
                           Text(("1", "3"), "797", "Greek", 1, "", "", None),
                           Text(("1", "3"), "798", "Greek", 1, "", "", None),
                           Text(("1", "4"), "799", "Greek", 1, "", "", None),
                           Text(("1", "4"), "800", "Greek", 1, "", "", None),
                           Text(("1", "4"), "801", "Greek", 1, "", "", None),
                           Text(("1", "5"), "802", "Greek", 1, "", "", None),
                           Text(("1", "5"), "803", "Greek", 2, "", "", None),
                           Text(("1", "5"), "804", "Greek", 1, "", "", None),
                           Text(("1", "6"), "805", "Greek", 1, "", "", None),
                           Text(("1", "6"), "806", "Greek", 2, "", "", None),
                           Text(("1", "6"), "807", "Greek", 1, "", "", None),
                           Text(("1", "7"), "808", "Greek", 1, "", "", None),
                           Text(("1", "8"), "809", "Greek", 1, "", "", None),
                           Text(("1", "8"), "810", "Greek", 2, "", "", None),
                           Text(("1", "8"), "811", "Greek", 1, "", "", None),
                           Text(("1", "9"), "812", "Greek", 3, "yes", "", u""),
                           Text(("1", "9"), "813", "Greek", 3, "", "", None),
                           Text(("1", "9"), "814", "Greek", 1, "", "", None),
                           Text(("1", "9"), "815", "Greek", 3, "", "yes", u"ἐλέγξαι "),
                           Text(("1", "9"), "816", "Greek", 1, "", "", u"πάντας τοὺς ἀσεβεῖς, "),
                           Text(("1", "9"), "817", "Greek", 2, "", "", None),
                           Text(("1", "9"), "818", "Greek", 1, "", "", None),
                           Text(("1", "9"), "819", "Greek", 2, "", "", None),
                           Text(("1", "9"), "820", "Greek", 1, "", "", None),
                           Text(("1", "9"), "821", "Greek", 2, "", "", None),
                           Text(("1", "9"), "822", "Greek", 2, "", "", None),
                           Text(("1", "9"), "823", "Greek", 1, "", "", None),
                           Text(("2", "1"), "824", "Greek", 1, "", "", None),
                           Text(("2", "1"), "825", "Greek", 2, "", "", u"καὶ"),
                           Text(("2", "2"), "826", "Greek", 1, "", "", None),
                           Text(("2", "2"), "827", "Greek", 3, "", "", None),
                           Text(("2", "2"), "828", "Greek", 2, "", "", ("Lorem ",
                                                                        W({"morph": "morph",
                                                                           "lex": "lex",
                                                                           "style": "style",
                                                                           "lang": "lang"}, "ipsum"),
                                                                        " dolor ",
                                                                        W({}, u"sit"),
                                                                        " amet")),
                           Text(("2", "3"), "829", "Greek", 1, "", "", None)],
                "error": [None,
                          "[Errno 2] No such file or directory: '{}/Xtest_parse.xml'".format(
                              XML_DRAFT_FILE_STORAGE_PATH),
                          None,
                          "<version> element with title='XGreek' does not exist"]}
    assert result["result"] == expected["result"]
    assert result["error"] == expected["error"]


def test_bookman_get_text_as_gluon():
    result = BookManager.get_text([{"book": "test_parse", "version": "Greek", "text_type": "TestOne",
                                    "start": (1, 2), "end": (1, )},
                                   {"book": "test_parse", "version": "Greek", "text_type": "TestOne",
                                    "start": (1, ), "end": (1, )}],
                                  as_gluon=True)
    expected0 = '<div>' \
                '<span class="level-2" id="1">1</span>' \
                '<span class="delimiter-2" id="delimiter-2-1">.</span>' \
                '<span class="level-1" id="2">2</span>' \
                '<span class="unit Greek 1" id="789">†</span>' \
                '<span class="unit Greek 1" id="790">†</span>' \
                '<span class="unit Greek 1" id="791">†</span>' \
                '<span class="unit Greek 2" id="792"><a href="792">†</a></span>' \
                '<span class="unit Greek 1" id="793">†</span>' \
                '<span class="unit Greek 1" id="794">†</span>' \
                '<span class="unit Greek 1" id="795">†</span>' \
                '<span class="unit Greek 1" id="796">†</span>' \
                '<span class="level-1" id="3">3</span>' \
                '<span class="unit Greek 1" id="797">†</span>' \
                '<span class="unit Greek 1" id="798">†</span>' \
                '<span class="level-1" id="4">4</span>' \
                '<span class="unit Greek 1" id="799">†</span>' \
                '<span class="unit Greek 1" id="800">†</span>' \
                '<span class="unit Greek 1" id="801">†</span>' \
                '<span class="level-1" id="5">5</span>' \
                '<span class="unit Greek 1" id="802">†</span>' \
                '<span class="unit Greek 2" id="803"><a href="803">†</a></span>' \
                '<span class="unit Greek 1" id="804">†</span>' \
                '<span class="level-1" id="6">6</span>' \
                '<span class="unit Greek 1" id="805">†</span>' \
                '<span class="unit Greek 2" id="806"><a href="806">†</a></span>' \
                '<span class="unit Greek 1" id="807">†</span>' \
                '<span class="level-1" id="7">7</span>' \
                '<span class="unit Greek 1" id="808">†</span>' \
                '<span class="level-1" id="8">8</span>' \
                '<span class="unit Greek 1" id="809">†</span>' \
                '<span class="unit Greek 2" id="810"><a href="810">†</a></span>' \
                '<span class="unit Greek 1" id="811">†</span>' \
                '<span class="level-1" id="9">9</span>' \
                '<span class="unit Greek 3 linebreak_yes" id="812"><a href="812">*</a></span>' \
                '<span class="unit Greek 3" id="813"><a href="813">†</a></span>' \
                '<span class="unit Greek 1" id="814">†</span>' \
                '<span class="unit Greek 3 indent" id="815"><a href="815">ἐλέγξαι </a></span>' \
                '<span class="unit Greek 1" id="816">πάντας τοὺς ἀσεβεῖς, </span>' \
                '<span class="unit Greek 2" id="817"><a href="817">†</a></span>' \
                '<span class="unit Greek 1" id="818">†</span>' \
                '<span class="unit Greek 2" id="819"><a href="819">†</a></span>' \
                '<span class="unit Greek 1" id="820">†</span>' \
                '<span class="unit Greek 2" id="821"><a href="821">†</a></span>' \
                '<span class="unit Greek 2" id="822"><a href="822">†</a></span>' \
                '<span class="unit Greek 1" id="823">†</span>' \
                '</div>'
    expected1 = '<div>' \
                '<span class="level-2" id="1">1</span>' \
                '<span class="delimiter-2" id="delimiter-2-1">.</span>' \
                '<span class="level-1" id="1">1</span>' \
                '<span class="unit Greek 2" id="788"><a href="788">Λόγος</a></span>' \
                '<span class="level-1" id="2">2</span>' \
                '<span class="unit Greek 1" id="789">†</span>' \
                '<span class="unit Greek 1" id="790">†</span>' \
                '<span class="unit Greek 1" id="791">†</span>' \
                '<span class="unit Greek 2" id="792"><a href="792">†</a></span>' \
                '<span class="unit Greek 1" id="793">†</span>' \
                '<span class="unit Greek 1" id="794">†</span>' \
                '<span class="unit Greek 1" id="795">†</span>' \
                '<span class="unit Greek 1" id="796">†</span>' \
                '<span class="level-1" id="3">3</span>' \
                '<span class="unit Greek 1" id="797">†</span>' \
                '<span class="unit Greek 1" id="798">†</span>' \
                '<span class="level-1" id="4">4</span>' \
                '<span class="unit Greek 1" id="799">†</span>' \
                '<span class="unit Greek 1" id="800">†</span>' \
                '<span class="unit Greek 1" id="801">†</span>' \
                '<span class="level-1" id="5">5</span>' \
                '<span class="unit Greek 1" id="802">†</span>' \
                '<span class="unit Greek 2" id="803"><a href="803">†</a></span>' \
                '<span class="unit Greek 1" id="804">†</span>' \
                '<span class="level-1" id="6">6</span>' \
                '<span class="unit Greek 1" id="805">†</span>' \
                '<span class="unit Greek 2" id="806"><a href="806">†</a></span>' \
                '<span class="unit Greek 1" id="807">†</span>' \
                '<span class="level-1" id="7">7</span>' \
                '<span class="unit Greek 1" id="808">†</span>' \
                '<span class="level-1" id="8">8</span>' \
                '<span class="unit Greek 1" id="809">†</span>' \
                '<span class="unit Greek 2" id="810"><a href="810">†</a></span>' \
                '<span class="unit Greek 1" id="811">†</span>' \
                '<span class="level-1" id="9">9</span>' \
                '<span class="unit Greek 3 linebreak_yes" id="812"><a href="812">*</a></span>' \
                '<span class="unit Greek 3" id="813"><a href="813">†</a></span>' \
                '<span class="unit Greek 1" id="814">†</span>' \
                '<span class="unit Greek 3 indent" id="815"><a href="815">ἐλέγξαι </a></span>' \
                '<span class="unit Greek 1" id="816">πάντας τοὺς ἀσεβεῖς, </span>' \
                '<span class="unit Greek 2" id="817"><a href="817">†</a></span>' \
                '<span class="unit Greek 1" id="818">†</span>' \
                '<span class="unit Greek 2" id="819"><a href="819">†</a></span>' \
                '<span class="unit Greek 1" id="820">†</span>' \
                '<span class="unit Greek 2" id="821"><a href="821">†</a></span>' \
                '<span class="unit Greek 2" id="822"><a href="822">†</a></span>' \
                '<span class="unit Greek 1" id="823">†</span>' \
                '</div>'
    assert len(result["result"]) == 2
    assert str(result["result"][0]) == expected0
    assert str(result["result"][1]) == expected1
    assert result["error"] == [None, None]


def test_bookman_get_readings():
    result = BookManager.get_readings([{"book": "test_parse", "version": "Greek", "unit_id": 812},
                                       {"book": "test_parse", "version": "Greek", "unit_id": 812}],
                                      as_gluon=False)
    expected = {"result": [[Reading("Gizeh", u"ὅτι ἔρχεται"),
                            Reading("Jude", u"ἰδοὺ ἦλθεν κύριος"),
                            Reading("TestOne", u"")],
                           [Reading("Gizeh", u"ὅτι ἔρχεται"),
                            Reading("Jude", u"ἰδοὺ ἦλθεν κύριος"),
                            Reading("TestOne", u"")]],
                "error": [None, None]}
    assert result["result"] == expected["result"]
    assert result["error"] == expected["error"]


def test_bookman_get_readings_as_gluon():
    result = BookManager.get_readings([{"book": "test_parse", "version": "Greek", "unit_id": 812},
                                       {"book": "test_parse", "version": "Greek", "unit_id": 812}],
                                      as_gluon=True)
    html = '<dl>' \
           '<dt>Gizeh</dt><dd>ὅτι ἔρχεται</dd>' \
           '<dt>Jude</dt><dd>ἰδοὺ ἦλθεν κύριος</dd>' \
           '<dt>TestOne</dt><dd>*</dd>' \
           '</dl>'
    assert str(result["result"][0]) == html
    assert str(result["result"][1]) == html
    assert len(result["result"]) == 2
    assert result["error"] == [None, None]


def test_bookman_get_unit_group():
    result = BookManager.get_unit_group([{"book": "test_parse", "version": "Greek", "unit_id": 812},
                                         {"book": "test_parse", "version": "Greek", "unit_id": 813}])
    expected = {"result": [[10, 14], [14, 10]],
                "error": [None, None]}
    assert result["result"] == expected["result"]
    assert result["error"] == expected["error"]

def test_bookman_get_group():
    result = BookManager.get_group([{"book": "test_parse", "version": "Greek", "unit_group": 14},
                                    {"book": "test_parse", "version": "Greek", "unit_group": 14}],
                                   as_gluon=False)
    expected = {"result": [OrderedDict({"812": [Reading("Gizeh", u"ὅτι ἔρχεται"),
                                                Reading("Jude", u"ἰδοὺ ἦλθεν κύριος"),
                                                Reading("TestOne", u"")],
                                        "813": [Reading("Gizeh", u"σὺν ταῖς μυριάσιν αὐτοῦ καὶ τοῖς ἁγίοις αὐτοῦ,"),
                                                Reading("Jude", u"ἐν ἁγίαις μυριάσιν αὐτοῦ,"),
                                                Reading("TestTwo", u"ἐν ἁγίαις μυριάσιν αὐτοῦ,")],
                                        "814": [Reading("Gizeh Jude", u"ποιῆσαι κρίσιν κατὰ πάντων, καὶ")]}),
                           OrderedDict({"812": [Reading("Gizeh", u"ὅτι ἔρχεται"),
                                                Reading("Jude", u"ἰδοὺ ἦλθεν κύριος"),
                                                Reading("TestOne", u"")],
                                        "813": [Reading("Gizeh", u"σὺν ταῖς μυριάσιν αὐτοῦ καὶ τοῖς ἁγίοις αὐτοῦ,"),
                                                Reading("Jude", u"ἐν ἁγίαις μυριάσιν αὐτοῦ,"),
                                                Reading("TestTwo", u"ἐν ἁγίαις μυριάσιν αὐτοῦ,")],
                                        "814": [Reading("Gizeh Jude", u"ποιῆσαι κρίσιν κατὰ πάντων, καὶ")]})],
                "error": [None, None]}
    assert result["result"] == expected["result"]
    assert result["error"] == expected["error"]


def test_bookman_get_group_as_gluon():
    result = BookManager.get_group([{"book": "test_parse", "version": "Greek", "unit_group": 14},
                                    {"book": "test_parse", "version": "Greek", "unit_group": 14}],
                                   as_gluon=True)
    html = '<dl>' \
           '<dt>Gizeh</dt><dd>ὅτι ἔρχεται</dd>' \
           '<dt>Jude</dt><dd>ἰδοὺ ἦλθεν κύριος</dd>' \
           '<dt>TestOne</dt><dd>*</dd>' \
           '<dt>Gizeh</dt><dd>σὺν ταῖς μυριάσιν αὐτοῦ καὶ τοῖς ἁγίοις αὐτοῦ,</dd>' \
           '<dt>Jude</dt><dd>ἐν ἁγίαις μυριάσιν αὐτοῦ,</dd>' \
           '<dt>TestTwo</dt><dd>ἐν ἁγίαις μυριάσιν αὐτοῦ,</dd>' \
           '<dt>Gizeh Jude</dt><dd>ποιῆσαι κρίσιν κατὰ πάντων, καὶ</dd>' \
           '</dl>'
    assert str(result["result"][0]) == html
    assert str(result["result"][1]) == html
    assert len(result["result"]) == 2
    assert result["error"] == [None, None]


## Testing EI


def fix_doctype(xml_string):
    """
    There is a stupid bug somewhere and I don't want to spent my time to discover it.
    When I run the test script at first time the enclosing marks around grammateus.dtd is different
    than when I rerun the failed test cases again. Maybe PyCharm runtime env maybe something else...
    """
    return xml_string.replace('"grammateus.dtd"', "'grammateus.dtd'")  # TODO: find the reason of this


def test_book_create():
    book = Book.create(filename="MyTest", title="My Test Book")
    assert fix_doctype(
        book.serialize(False)) == "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
                                  "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
                                  '<book filename="MyTest" title="My Test Book"/>'


def test_book_add_version(new_book):
    result = fix_doctype(new_book.serialize(False))
    expected = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
               "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
               '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
               '<version author="Me" language="MyLanguage" title="MyVersion">' \
               '<divisions/>' \
               '<manuscripts/>' \
               '<text/>' \
               '</version>' \
               '</book>'
    assert result == expected


def test_book_add_version_w_mss(new_book):
    new_book.add_version(version_title="MyVersion2", language="MyLanguage2", author="Me", mss=["A", "B"])
    result = fix_doctype(new_book.serialize(False))
    expected = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
               "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
               '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
               '<version author="Me" language="MyLanguage" title="MyVersion">' \
               '<divisions/>' \
               '<manuscripts/>' \
               '<text/>' \
               '</version>' \
               '<version author="Me" language="MyLanguage2" title="MyVersion2">' \
               '<divisions/>' \
               '<manuscripts>' \
               '<ms abbrev="A" language="" show=""><name/></ms>' \
               '<ms abbrev="B" language="" show=""><name/></ms>' \
               '</manuscripts>' \
               '<text/>' \
               '</version>' \
               '</book>'
    assert result == expected


def test_book_update_version(new_book):
    new_book.update_version(version_title="MyVersion", new_version_title="MyVersion2", new_language="MyLanguage2")
    result = fix_doctype(new_book.serialize(False))
    expected = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
               "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
               '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
               '<version author="Me" language="MyLanguage2" title="MyVersion2">' \
               '<divisions/>' \
               '<manuscripts/>' \
               '<text/>' \
               '</version>' \
               '</book>'
    assert result == expected


def test_book_update_version_on_nonexisting_version(new_book):
    with pytest.raises(ElementDoesNotExist):
        new_book.update_version(version_title="XMyVersion", new_version_title="MyVersion2", new_language="MyLanguage2")


def test_book_del_version(new_book):
    new_book.del_version(version_title="MyVersion")
    result = fix_doctype(new_book.serialize(False))
    expected = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
               "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
               '<book filename="MyTest" textStructure="fragmentary" title="My Test Book"/>'
    assert result == expected


def test_book_del_version_on_nonexisting_version(new_book):
    with pytest.raises(ElementDoesNotExist):
        new_book.del_version(version_title="XMyVersion")


def test_book_add_manuscript(new_book):
    new_book.add_manuscript(version_title="MyVersion", abbrev="MyManuscript", language="MyLanguage")
    new_book.add_manuscript(version_title="MyVersion", abbrev="MyManuscript2", language="MyLanguage2", show=False)
    result = fix_doctype(new_book.serialize(False))
    expected = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
               "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
               '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
               '<version author="Me" language="MyLanguage" title="MyVersion">' \
               '<divisions/>' \
               '<manuscripts>' \
               '<ms abbrev="MyManuscript" language="MyLanguage" show="yes">' \
               '<name/>' \
               '</ms>' \
               '<ms abbrev="MyManuscript2" language="MyLanguage2" show="no">' \
               '<name/>' \
               '</ms>' \
               '</manuscripts>' \
               '<text/>' \
               '</version>' \
               '</book>'
    assert result == expected


def test_book_update_manuscript(new_book):
    new_book.add_manuscript(version_title="MyVersion", abbrev="MyManuscript", language="MyLanguage")
    new_book.add_manuscript(version_title="MyVersion", abbrev="MyManuscript2", language="MyLanguage2", show=False)
    new_book.update_manuscript(version_title="MyVersion", abbrev="MyManuscript2",
                               new_abbrev="MyManuscript3",
                               new_language="MyLanguage3",
                               new_show=True)
    result = fix_doctype(new_book.serialize(False))
    expected = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
               "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
               '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
               '<version author="Me" language="MyLanguage" title="MyVersion">' \
               '<divisions/>' \
               '<manuscripts>' \
               '<ms abbrev="MyManuscript" language="MyLanguage" show="yes">' \
               '<name/>' \
               '</ms>' \
               '<ms abbrev="MyManuscript3" language="MyLanguage3" show="yes">' \
               '<name/>' \
               '</ms>' \
               '</manuscripts>' \
               '<text/>' \
               '</version>' \
               '</book>'
    assert result == expected


def test_book_del_manuscript(new_book):
    new_book.add_manuscript(version_title="MyVersion", abbrev="MyManuscript", language="MyLanguage")
    new_book.add_manuscript(version_title="MyVersion", abbrev="MyManuscript2", language="MyLanguage2", show=False)
    new_book.update_manuscript(version_title="MyVersion", abbrev="MyManuscript2",
                               new_abbrev="MyManuscript3",
                               new_language="MyLanguage3",
                               new_show=True)
    new_book.del_manuscript(version_title="MyVersion", abbrev="MyManuscript3")
    result = fix_doctype(new_book.serialize(False))
    expected = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
               "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
               '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
               '<version author="Me" language="MyLanguage" title="MyVersion">' \
               '<divisions/>' \
               '<manuscripts>' \
               '<ms abbrev="MyManuscript" language="MyLanguage" show="yes">' \
               '<name/>' \
               '</ms>' \
               '</manuscripts>' \
               '<text/>' \
               '</version>' \
               '</book>'
    assert result == expected


def test_book_add_bibliography(new_book):
    new_book.add_manuscript(version_title="MyVersion", abbrev="MyManuscript", language="MyLanguage")
    new_book.add_bibliography(version_title="MyVersion", abbrev="MyManuscript", text="MyBibliography")
    new_book.add_bibliography(version_title="MyVersion", abbrev="MyManuscript", text="MyBibliography2")

    result = fix_doctype(new_book.serialize(False))
    expected = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
               "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
               '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
               '<version author="Me" language="MyLanguage" title="MyVersion">' \
               '<divisions/>' \
               '<manuscripts>' \
               '<ms abbrev="MyManuscript" language="MyLanguage" show="yes">' \
               '<name/>' \
               '<bibliography>MyBibliography</bibliography>' \
               '<bibliography>MyBibliography2</bibliography>' \
               '</ms>' \
               '</manuscripts>' \
               '<text/>' \
               '</version>' \
               '</book>'
    assert result == expected


def test_book_update_bibliography(new_book):
    new_book.add_manuscript(version_title="MyVersion", abbrev="MyManuscript", language="MyLanguage")
    new_book.add_bibliography(version_title="MyVersion", abbrev="MyManuscript", text="MyBibliography")
    new_book.add_bibliography(version_title="MyVersion", abbrev="MyManuscript", text="MyBibliography2")
    new_book.update_bibliography(version_title="MyVersion", abbrev="MyManuscript", bibliography_pos=0,
                                 new_text="MyBibliography1")

    result = fix_doctype(new_book.serialize(False))
    expected = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
               "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
               '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
               '<version author="Me" language="MyLanguage" title="MyVersion">' \
               '<divisions/>' \
               '<manuscripts>' \
               '<ms abbrev="MyManuscript" language="MyLanguage" show="yes">' \
               '<name/>' \
               '<bibliography>MyBibliography1</bibliography>' \
               '<bibliography>MyBibliography2</bibliography>' \
               '</ms>' \
               '</manuscripts>' \
               '<text/>' \
               '</version>' \
               '</book>'
    assert result == expected


def test_book_del_bibliography(new_book):
    new_book.add_manuscript(version_title="MyVersion", abbrev="MyManuscript", language="MyLanguage")
    new_book.add_bibliography(version_title="MyVersion", abbrev="MyManuscript", text="MyBibliography")
    new_book.add_bibliography(version_title="MyVersion", abbrev="MyManuscript", text="MyBibliography2")
    new_book.update_bibliography(version_title="MyVersion", abbrev="MyManuscript", bibliography_pos=0,
                                 new_text="MyBibliography1")
    new_book.del_bibliography(version_title="MyVersion", abbrev="MyManuscript", bibliography_pos=1)

    result = fix_doctype(new_book.serialize(False))
    expected = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
               "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
               '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
               '<version author="Me" language="MyLanguage" title="MyVersion">' \
               '<divisions/>' \
               '<manuscripts>' \
               '<ms abbrev="MyManuscript" language="MyLanguage" show="yes">' \
               '<name/>' \
               '<bibliography>MyBibliography1</bibliography>' \
               '</ms>' \
               '</manuscripts>' \
               '<text/>' \
               '</version>' \
               '</book>'
    assert result == expected


def test_book_add_div(new_book):
    # add div
    new_book.add_div(version_title="MyVersion", div_name="MyDiv1", div_parent_path=None)
    new_book.add_div(version_title="MyVersion", div_name="MyDiv1.1", div_parent_path=["MyDiv1"])
    new_book.add_div(version_title="MyVersion", div_name="MyDiv1.1.1", div_parent_path=["MyDiv1", "MyDiv1.1"])
    new_book.add_div(version_title="MyVersion", div_name="MyDiv1.1.3", div_parent_path=["MyDiv1", "MyDiv1.1"])
    ## with preceding
    new_book.add_div(version_title="MyVersion", div_name="MyDiv2", div_parent_path=None, preceding_div="MyDiv1")
    new_book.add_div(version_title="MyVersion", div_name="MyDiv1.1.2", div_parent_path=["MyDiv1", "MyDiv1.1"], preceding_div="MyDiv1.1.1")
    ## with exceptions
    with pytest.raises(ElementDoesNotExist):
        # non existing parent path
        new_book.add_div(version_title="MyVersion", div_name="MyDiv0", div_parent_path=["MyXDiv"])
    with pytest.raises(ElementDoesNotExist):
        # non existing preceding
        new_book.add_div(version_title="MyVersion", div_name="MyDiv0", div_parent_path=["MyXDiv1"], preceding_div="MyDiv1")
    result = fix_doctype(new_book.serialize(False))
    expected = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
               "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
               '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
               '<version author="Me" language="MyLanguage" title="MyVersion">' \
               '<divisions/>' \
               '<manuscripts/>' \
               '<text>' \
               '<div number="MyDiv1">' \
               '<div number="MyDiv1.1">' \
               '<div number="MyDiv1.1.1"/>' \
               '<div number="MyDiv1.1.2"/>' \
               '<div number="MyDiv1.1.3"/>' \
               '</div>' \
               '</div>' \
               '<div number="MyDiv2"/>' \
               '</text>' \
               '</version>' \
               '</book>'
    assert result == expected


def test_book_update_div(new_book):
    # prepering book
    new_book.add_div(version_title="MyVersion", div_name="MyDiv1", div_parent_path=None)
    # update div
    new_book.update_div(version_title="MyVersion", div_path=["MyDiv1"], new_div_name="MyDiv")
    result = fix_doctype(new_book.serialize(False))
    expected = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
               "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
               '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
               '<version author="Me" language="MyLanguage" title="MyVersion">' \
               '<divisions/>' \
               '<manuscripts/>' \
               '<text>' \
               '<div number="MyDiv"/>' \
               '</text>' \
               '</version>' \
               '</book>'
    assert result == expected


def test_book_del_div(new_book):
    # prepering book
    new_book.add_div(version_title="MyVersion", div_name="MyDiv1", div_parent_path=None)
    new_book.add_div(version_title="MyVersion", div_name="MyDiv1.1", div_parent_path=["MyDiv1"])
    new_book.add_div(version_title="MyVersion", div_name="MyDiv1.1.1", div_parent_path=["MyDiv1", "MyDiv1.1"])
    new_book.add_div(version_title="MyVersion", div_name="MyDiv1.1.2", div_parent_path=["MyDiv1", "MyDiv1.1"])
    new_book.add_div(version_title="MyVersion", div_name="MyDiv2", div_parent_path=None)
    # del div
    new_book.del_div(version_title="MyVersion", div_path=["MyDiv1", "MyDiv1.1"])
    new_book.del_div(version_title="MyVersion", div_path=["MyDiv2"])
    result = fix_doctype(new_book.serialize(False))
    expected = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
               "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
               '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
               '<version author="Me" language="MyLanguage" title="MyVersion">' \
               '<divisions/>' \
               '<manuscripts/>' \
               '<text>' \
               '<div number="MyDiv1"/>' \
               '</text>' \
               '</version>' \
               '</book>'
    assert result == expected


def test_book_add_unit(new_book):
    # prepering book
    new_book.add_div(version_title="MyVersion", div_name="1", div_parent_path=None)
    new_book.add_div(version_title="MyVersion", div_name="1.1", div_parent_path=["1"])
    new_book.add_div(version_title="MyVersion", div_name="1.1.1", div_parent_path=["1", "1.1"])
    new_book.add_div(version_title="MyVersion", div_name="1.1.2", div_parent_path=["1", "1.1"])
    # add unit
    new_book.add_unit(version_title="MyVersion", div_path=["1", "1.1", "1.1.2"])
    new_book.add_unit(version_title="MyVersion", div_path=["1", "1.1", "1.1.1"])
    new_book.add_unit(version_title="MyVersion", div_path=["1", "1.1", "1.1.1"])
    result_xml = fix_doctype(new_book.serialize(False))
    expected_xml = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
                   "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
                   '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
                   '<version author="Me" language="MyLanguage" title="MyVersion">' \
                   '<divisions/>' \
                   '<manuscripts/>' \
                   '<text>' \
                   '<div number="1">' \
                   '<div number="1.1">' \
                   '<div number="1.1.1">' \
                   '<unit id="1"><reading/></unit>' \
                   '<unit id="2"><reading/></unit>' \
                   '</div>' \
                   '<div number="1.1.2">' \
                   '<unit id="3"><reading/></unit>' \
                   '</div>' \
                   '</div>' \
                   '</div>' \
                   '</text>' \
                   '</version>' \
                   '</book>'
    assert result_xml == expected_xml


def test_book_update_unit(new_book):
    # prepering book
    new_book.add_div(version_title="MyVersion", div_name="1", div_parent_path=None)
    new_book.add_div(version_title="MyVersion", div_name="1.1", div_parent_path=["1"])
    new_book.add_div(version_title="MyVersion", div_name="1.1.1", div_parent_path=["1", "1.1"])
    new_book.add_div(version_title="MyVersion", div_name="1.1.2", div_parent_path=["1", "1.1"])
    new_book.add_unit(version_title="MyVersion", div_path=["1", "1.1", "1.1.2"])
    new_book.add_unit(version_title="MyVersion", div_path=["1", "1.1", "1.1.1"])
    new_book.add_unit(version_title="MyVersion", div_path=["1", "1.1", "1.1.1"])
    # update unit
    new_book.update_unit(version_title="MyVersion",
                         unit_id="2",
                         readings=(("MyMSS", u"Ütvefúró tükörfúrógép"), ("MyMSS", u"ἰδοὺ ἦλθεν κύριος")))
    result_xml = fix_doctype(new_book.serialize(False))
    expected_xml = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
                   "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
                   '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
                   '<version author="Me" language="MyLanguage" title="MyVersion">' \
                   '<divisions/>' \
                   '<manuscripts/>' \
                   '<text>' \
                   '<div number="1">' \
                   '<div number="1.1">' \
                   '<div number="1.1.1">' \
                   '<unit id="1"><reading/></unit>' \
                   '<unit id="2">' \
                   '<reading mss="MyMSS" option="0">Ütvefúró tükörfúrógép</reading>' \
                   '<reading mss="MyMSS" option="1">ἰδοὺ ἦλθεν κύριος</reading>' \
                   '</unit>' \
                   '</div>' \
                   '<div number="1.1.2">' \
                   '<unit id="3"><reading/></unit>' \
                   '</div>' \
                   '</div>' \
                   '</div>' \
                   '</text>' \
                   '</version>' \
                   '</book>'
    assert result_xml == expected_xml


def test_book_split_unit(new_book):
    # prepering book
    new_book.add_div(version_title="MyVersion", div_name="1", div_parent_path=None)
    new_book.add_div(version_title="MyVersion", div_name="1.1", div_parent_path=["1"])
    new_book.add_div(version_title="MyVersion", div_name="1.1.1", div_parent_path=["1", "1.1"])
    new_book.add_div(version_title="MyVersion", div_name="1.1.2", div_parent_path=["1", "1.1"])
    new_book.add_unit(version_title="MyVersion", div_path=["1", "1.1", "1.1.2"])
    new_book.add_unit(version_title="MyVersion", div_path=["1", "1.1", "1.1.1"])
    new_book.add_unit(version_title="MyVersion", div_path=["1", "1.1", "1.1.1"])
    new_book.update_unit(version_title="MyVersion",
                         unit_id="2",
                         readings=(("MyMSS1", u"Ütvefúró tükörfúrógép"), ("MyMSS2", u"ἰδοὺ ἦλθεν κύριος")))
    # split unit
    new_book.split_unit(version_title="MyVersion",
                        unit_id="2",
                        reading_pos=0,
                        split_point=9)
    new_book.split_unit(version_title="MyVersion",
                        unit_id="2",
                        reading_pos="1",
                        split_point=u"ἦλθεν")
    result_xml = fix_doctype(new_book.serialize(False))
    expected_xml = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
                   "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
                   '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
                   '<version author="Me" language="MyLanguage" title="MyVersion">' \
                   '<divisions/>' \
                   '<manuscripts/>' \
                   '<text>' \
                   '<div number="1">' \
                   '<div number="1.1">' \
                   '<div number="1.1.1">' \
                   '<unit id="1"><reading/></unit>' \
                   '<unit id="2">' \
                   '<reading mss="MyMSS1" option="0">Ütvefúró</reading>' \
                   '<reading mss="MyMSS2" option="1">ἰδοὺ</reading>' \
                   '</unit>' \
                   '<unit id="3">' \
                   '<reading mss="MyMSS1" option="0"></reading>' \
                   '<reading mss="MyMSS2" option="1">ἦλθεν</reading>' \
                   '</unit>' \
                   '<unit id="4">' \
                   '<reading mss="MyMSS1" option="0"></reading>' \
                   '<reading mss="MyMSS2" option="1">κύριος</reading>' \
                   '</unit>' \
                   '<unit id="5">' \
                   '<reading mss="MyMSS1" option="0">tükörfúrógép</reading>' \
                   '<reading mss="MyMSS2" option="1"></reading>' \
                   '</unit>' \
                   '</div>' \
                   '<div number="1.1.2">' \
                   '<unit id="6"><reading/></unit>' \
                   '</div>' \
                   '</div>' \
                   '</div>' \
                   '</text>' \
                   '</version>' \
                   '</book>'
    assert result_xml == expected_xml


def test_book_split_reading(new_book):
    # prepering book
    new_book.add_div(version_title="MyVersion", div_name="1", div_parent_path=None)
    new_book.add_div(version_title="MyVersion", div_name="1.1", div_parent_path=["1"])
    new_book.add_div(version_title="MyVersion", div_name="1.1.1", div_parent_path=["1", "1.1"])
    new_book.add_div(version_title="MyVersion", div_name="1.1.2", div_parent_path=["1", "1.1"])
    new_book.add_unit(version_title="MyVersion", div_path=["1", "1.1", "1.1.2"])
    new_book.add_unit(version_title="MyVersion", div_path=["1", "1.1", "1.1.1"])
    new_book.add_unit(version_title="MyVersion", div_path=["1", "1.1", "1.1.1"])
    new_book.update_unit(version_title="MyVersion",
                         unit_id="2",
                         readings=(("MyMSS1", u"Ütvefúró tükörfúrógép"), ("MyMSS2", u"ἰδοὺ ἦλθεν κύριος")))
    # split unit
    new_book.split_reading(version_title="MyVersion",
                           unit_id="2",
                           reading_pos=0,
                           split_point=9)
    new_book.split_reading(version_title="MyVersion",
                           unit_id="2",
                           reading_pos="2",
                           split_point=u"ἦλθεν")
    result_xml = fix_doctype(new_book.serialize(False))
    expected_xml = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
                   "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
                   '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
                   '<version author="Me" language="MyLanguage" title="MyVersion">' \
                   '<divisions/>' \
                   '<manuscripts/>' \
                   '<text>' \
                   '<div number="1">' \
                   '<div number="1.1">' \
                   '<div number="1.1.1">' \
                   '<unit id="1"><reading/></unit>' \
                   '<unit id="2">' \
                   '<reading mss="MyMSS1" option="0">Ütvefúró</reading>' \
                   '<reading mss="MyMSS1" option="1">tükörfúrógép</reading>' \
                   '<reading mss="MyMSS2" option="2">ἰδοὺ</reading>' \
                   '<reading mss="MyMSS2" option="3">ἦλθεν</reading>' \
                   '<reading mss="MyMSS2" option="4">κύριος</reading>' \
                   '</unit>' \
                   '</div>' \
                   '<div number="1.1.2">' \
                   '<unit id="3"><reading/></unit>' \
                   '</div>' \
                   '</div>' \
                   '</div>' \
                   '</text>' \
                   '</version>' \
                   '</book>'
    assert result_xml == expected_xml


def test_book_del_unit(new_book):
    # prepering book
    new_book.add_div(version_title="MyVersion", div_name="1", div_parent_path=None)
    new_book.add_div(version_title="MyVersion", div_name="1.1", div_parent_path=["1"])
    new_book.add_div(version_title="MyVersion", div_name="1.1.1", div_parent_path=["1", "1.1"])
    new_book.add_div(version_title="MyVersion", div_name="1.1.2", div_parent_path=["1", "1.1"])
    new_book.add_unit(version_title="MyVersion", div_path=["1", "1.1", "1.1.2"])
    new_book.add_unit(version_title="MyVersion", div_path=["1", "1.1", "1.1.1"])
    new_book.add_unit(version_title="MyVersion", div_path=["1", "1.1", "1.1.1"])
    # del unit
    new_book.del_unit(version_title="MyVersion", unit_id="2")
    result_xml = fix_doctype(new_book.serialize(False))
    expected_xml = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
                   "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
                   '<book filename="MyTest" textStructure="fragmentary" title="My Test Book">' \
                   '<version author="Me" language="MyLanguage" title="MyVersion">' \
                   '<divisions/>' \
                   '<manuscripts/>' \
                   '<text>' \
                   '<div number="1">' \
                   '<div number="1.1">' \
                   '<div number="1.1.1">' \
                   '<unit id="1"><reading/></unit>' \
                   '</div>' \
                   '<div number="1.1.2">' \
                   '<unit id="2"><reading/></unit>' \
                   '</div>' \
                   '</div>' \
                   '</div>' \
                   '</text>' \
                   '</version>' \
                   '</book>'
    assert result_xml == expected_xml


def test_bookman_create_publish_copy():
    # setup
    book_name = "MyNewBookTest"
    book_file_pattern = "{}/{}_????????_??????_??????.xml"
    files_to_remove = []
    for xml_folder in [XML_DRAFT_FILE_BACKUP_STORAGE_PATH,
                       XML_FILE_BACKUP_STORAGE_PATH]:
        files_to_remove += glob.glob(book_file_pattern.format(xml_folder, book_name))
    for xml_folder in [XML_DRAFT_FILE_STORAGE_PATH,
                       XML_FILE_STORAGE_PATH]:
        files_to_remove += glob.glob("{}/{}.xml".format(xml_folder, book_name))
    for file_path in files_to_remove:
        os.remove(file_path)

    # create new
    BookManager.create_book(book_name, "My new book")
    result_xml = fix_doctype(open("{}/{}.xml".format(XML_DRAFT_FILE_STORAGE_PATH, book_name)).read())
    expected_xml = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
                   "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
                   '<book filename="{}" title="My new book"/>\n'.format(book_name)
    assert result_xml == expected_xml

    # publish
    BookManager.publish_book(book_name)
    result_xml = fix_doctype(open("{}/{}.xml".format(XML_FILE_STORAGE_PATH, book_name)).read())
    assert result_xml == expected_xml

    # copy as draft
    BookManager.copy_book(book_name)
    result_xml = fix_doctype(open("{}/{}.xml".format(XML_DRAFT_FILE_STORAGE_PATH, book_name)).read())
    assert result_xml == expected_xml
    assert len(glob.glob(book_file_pattern.format(XML_DRAFT_FILE_BACKUP_STORAGE_PATH, book_name))) == 1

    # edit (add version)
    BookManager.add_version(book_name, "MyVersion", "MyLanguage", "Me")
    result_xml = fix_doctype(open("{}/{}.xml".format(XML_DRAFT_FILE_STORAGE_PATH, book_name)).read())
    expected_xml = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
                   "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
                   '<book filename="{}" title="My new book">\n' \
                   '  <version author="Me" language="MyLanguage" title="MyVersion">\n' \
                   '    <divisions/>\n' \
                   '    <manuscripts/>\n' \
                   '    <text/>\n' \
                   '  </version>\n' \
                   '</book>\n'.format(book_name)
    assert result_xml == expected_xml
    assert len(glob.glob(book_file_pattern.format(XML_DRAFT_FILE_BACKUP_STORAGE_PATH, book_name))) == 2

    # publish
    BookManager.publish_book(book_name)
    result_xml = fix_doctype(open("{}/{}.xml".format(XML_FILE_STORAGE_PATH, book_name)).read())
    assert result_xml == expected_xml
    assert len(glob.glob(book_file_pattern.format(XML_FILE_BACKUP_STORAGE_PATH, book_name))) == 1

    # teardown
    files_to_remove = []
    for xml_folder in [XML_DRAFT_FILE_BACKUP_STORAGE_PATH,
                       XML_FILE_BACKUP_STORAGE_PATH]:
        files_to_remove += glob.glob(book_file_pattern.format(xml_folder, book_name))
    for xml_folder in [XML_DRAFT_FILE_STORAGE_PATH,
                       XML_FILE_STORAGE_PATH]:
        files_to_remove += glob.glob("{}/{}.xml".format(xml_folder, book_name))
    for file_path in files_to_remove:
        os.remove(file_path)
#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
run tests from web2py root directory with:

    python2.7 -m pytest -xvvs applications/grammateus3/test/modules/test_parse.py
"""

from collections import OrderedDict
import difflib
import glob
from lxml import etree
import os
from parse import Text, Reading, W
from parse import Book, BookManager
from parse import ElementDoesNotExist, InvalidDIVPath, NotAllowedManuscript
from plugin_utils import check_path
from pprint import pprint
import pytest
from StringIO import StringIO

file_dir = os.path.join(os.path.dirname(__file__), os.pardir)
PROJECT_ROOT = os.path.join(file_dir, os.pardir)

XML_FILE_STORAGE_PATH = check_path(os.path.join(PROJECT_ROOT, "test", "docs"))
XML_FILE_BACKUP_STORAGE_PATH = check_path(os.path.join(PROJECT_ROOT, "test",
                                                       "docs", "backups"))
XML_DRAFT_FILE_STORAGE_PATH = check_path(os.path.join(PROJECT_ROOT, "test",
                                                      "docs", "drafts"))
XML_DRAFT_FILE_BACKUP_STORAGE_PATH = check_path(os.path.join(PROJECT_ROOT,
                                                             "test", "docs",
                                                             "drafts", "backups"))

TEST_XML_FILE = check_path(os.path.join(PROJECT_ROOT, "test", "docs", "drafts",
                                        "test_parse.xml"))
TEST_DTD_FILE = check_path(os.path.join(PROJECT_ROOT, "static", "docs",
                                        "grammateus.dtd"))

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
    book.add_version(version_title="MyVersion", language="MyLanguage",
                     author="Me")
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


# Testing RI
@pytest.mark.parametrize("myref,mylength,expected", [
    ((1,),  # case 1 ----------------------------------------------------
     1,
     [u'<div number="1">\n'
      u'        <div number="1">\n'
      u'          <unit id="788" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh "> Λόγος εὐλογίας Ἑνώχ, καθὼς εὐλόγησεν ἐκλεκτοὺς δικαίους οἵτινες ἔσονται εἰς ἡμέραν ἀνάγκης ἐξᾶραι πάντας τοὺς ἐχθρούς, καὶ σωθήσονται δίκαιοι. </reading>\n'
      u'            <reading option="1" mss="TestOne ">Λόγος</reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="2">\n'
      u'          <unit id="789" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">Καὶ ἀναλαβὼν </reading>\n'
      u'          </unit>\n'
      u'          <unit id="790" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">τὴν παραβολὴν αὐτοῦ εἶπεν </reading>\n'
      u'          </unit>\n'
      u'          <unit id="791" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">Ἑνώχ· Ἄνθρωπος δίκαιός ἐστιν, </reading>\n'
      u'          </unit>\n'
      u'          <unit id="792" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh "/>\n'
      u'            <reading option="1" mss="Black ">[ᾧ] </reading>\n'
      u'          </unit>\n'
      u'          <unit id="793" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">ὅρασις ἐκ τοῦ θεοῦ αὐτῷ ἀνεῳγμένη ἦν· ἔχων τὴν ὅρασιν τοῦ ἁγίου καὶ τοῦ οὐρανοῦ. ἔδειξέν μοι,</reading>\n'
      u'          </unit>\n'
      u'          <unit id="794" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">καὶ ἁγιολόγων ἁγίων ἤκουσα ἐγώ, καὶ ὡς ἤκουσα παρ᾽ αὐτῶν πάντα </reading>\n'
      u'          </unit>\n'
      u'          <unit id="795" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh "> καὶ ἔγνων ἐγὼ θεωρῶν· καὶ οὐκ</reading>\n'
      u'          </unit>\n'
      u'          <unit id="796" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">εἰς τὴν νῦν γενεὰν διενοούμην, ἀλλὰ ἐπὶ πόρρω οὖσαν ἐγὼ λαλῶ. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="3">\n'
      u'          <unit id="797" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">Καὶ περὶ τῶν ἐκλεκτῶν νῦν λέγω καὶ περὶ αὐτῶν ἀνέλαβον τὴν παραβολήν μου.</reading>\n'
      u'          </unit>\n'
      u'          <unit id="798" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">καὶ ἐξελεύσεται ὁ ἅγιός μου ὁ μέγας ἐκ τῆς κατοικήσεως αὐτοῦ, </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="4">\n'
      u'          <unit id="799" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">καὶ ὁ θεὸς τοῦ αἰῶνος ἐπὶ γῆν πατῆσει ἐπὶ τὸ Σεινὰ ὄρος καὶ φανήσεται ἐκ</reading>\n'
      u'          </unit>\n'
      u'          <unit id="800" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">τῆς παρεμβολῆς αὐτοῦ, καὶ φανήσεται ἐν τῇ δυνάμει τῆς ἰσχύος αὐτοῦ </reading>\n'
      u'          </unit>\n'
      u'          <unit id="801" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh "> ἀπὸ τοῦ οὐρανοῦ τῶν οὐρανῶν. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="5">\n'
      u'          <unit id="802" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">καὶ φοβηθήσονται πάντες καὶ πιστεύσουσιν οἱ ἐγρήγοροι, καὶ ᾄσουσιν ἀπόκρυφα ἐν πᾶσιν τοῖς ἄκροις τῆς </reading>\n'
      u'          </unit>\n'
      u'          <unit id="803" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh "/>\n'
      u'            <reading option="1" mss="Black ">[γῆς]</reading>\n'
      u'          </unit>\n'
      u'          <unit id="804" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">· καὶ σεισθήσονται πάντα τὰ ἄκρα τῆς γῆς, καὶ λήμψεται αὐτοὺς τρόμος καὶ φόβος μέγας μέχρι τῶν περάτων τῆς γῆς. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="6">\n'
      u'          <unit id="805" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">καὶ σεισθήσονται καὶ πεσοῦνται καὶ διαλυθήσονται ὄρη ὑψηλά, καὶ </reading>\n'
      u'          </unit>\n'
      u'          <unit id="806" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">ταπεινωθήσονται </reading>\n'
      u'            <reading option="1" mss="Gizeh* ">πεινωθησονται </reading>\n'
      u'          </unit>\n'
      u'          <unit id="807" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">βουνοὶ ὑψηλοὶ τοῦ διαρυῆναι ὄρη, καὶ τακήσονται ὡς κηρὸς ἀπὸ προσώπου πυρὸς ἐν φλογί. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="7">\n'
      u'          <unit id="808" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">καὶ διασχισθήσεται ἡ γῆ σχίσμα ῥαγάδι, καὶ πάντα ὅσα ἐστὶν ἐπὶ τῆς γῆς ἀπολεῖται, καὶ κρίσις ἔσται κατὰ πάντων. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="8">\n'
      u'          <unit id="809" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">καὶ μετὰ τῶν δικαίων τὴν εἰρήνην ποιήσει, καὶ ἐπὶ τοὺς ἐκλεκτοὺς ἔσται συντήρησις καὶ εἰρήνη, καὶ ἐπ᾽ αὐτοὺς </reading>\n'
      u'          </unit>\n'
      u'          <unit id="810" group="0" parallel="">\n'
      u'            <reading option="0" mss="Swete Charles Black Dindorf TestTwo">γενήσεται </reading>\n'
      u'            <reading option="1" mss="Gizeh ">γενηται </reading>\n'
      u'          </unit>\n'
      u'          <unit id="811" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">ἔλεος, καὶ ἔσονται πάντες τοῦ θεοῦ, καὶ τὴν εὐδοκίαν δώσει αὐτοῖς καὶ πάντας εὐλογήσει καὶ πάντων ἀντιλήμψεται καὶ βοηθήσει ἡμῖν, καὶ φανήσεται αὐτοῖς φῶς καὶ ποιήσει ἐπ᾽ αὐτοὺς εἰρήνην. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="9">\n'
      u'          <unit id="812" group="10 14" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">ὅτι ἔρχεται </reading>\n'
      u'            <reading option="1" mss="Jude ">ἰδοὺ ἦλθεν κύριος </reading>\n'
      u'            <reading option="2" mss="TestOne " linebreak="yes"/>\n'
      u'          </unit>\n'
      u'          <unit id="813" group="14 10" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">σὺν ταῖς μυριάσιν αὐτοῦ καὶ τοῖς ἁγίοις αὐτοῦ, </reading>\n'
      u'            <reading option="1" mss="Jude ">ἐν ἁγίαις μυριάσιν αὐτοῦ, </reading>\n'
      u'            <reading option="2" mss="TestTwo ">ἐν ἁγίαις μυριάσιν αὐτοῦ, </reading>\n'
      u'          </unit>\n'
      u'          <unit id="814" group="14" parallel="">\n'
      u'            <reading option="0" mss="Gizeh Jude ">ποιῆσαι κρίσιν κατὰ πάντων, καὶ </reading>\n'
      u'          </unit>\n'
      u'          <unit id="815" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">ἀπολέσει </reading>\n'
      u'            <reading option="1" mss="Jude ">ἐλέγξαι </reading>\n'
      u'            <reading option="2" mss="Jude TestOne " indent="yes">ἐλέγξαι </reading>\n'
      u'          </unit>\n'
      u'          <unit id="816" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh2 TestOne Jude ">πάντας τοὺς ἀσεβεῖς, </reading>\n'
      u'          </unit>\n'
      u'          <unit id="817" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">καὶ ἐλέγξει πᾶσαν σάρκα περὶ πάντων </reading>\n'
      u'            <reading option="1" mss="Jude ">περὶ πάντων τῶν </reading>\n'
      u'          </unit>\n'
      u'          <unit id="818" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh Jude ">ἔργων </reading>\n'
      u'          </unit>\n'
      u'          <unit id="819" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">τῆς </reading>\n'
      u'            <reading option="1" mss="Jude "/>\n'
      u'          </unit>\n'
      u'          <unit id="820" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh Jude ">ἀσεβείας αὐτῶν ὧν ἠσέβησαν καὶ </reading>\n'
      u'          </unit>\n'
      u'          <unit id="821" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh "/>\n'
      u'            <reading option="1" mss="Jude ">περὶ πάντων τῶν </reading>\n'
      u'          </unit>\n'
      u'          <unit id="822" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">σκληρῶν ὧν ἐλάλησαν λόγων, καὶ περὶ πάντων ὧν κατελάλησαν </reading>\n'
      u'            <reading option="1" mss="Jude ">σκληρῶν ὧν ἐλάλησαν </reading>\n'
      u'          </unit>\n'
      u'          <unit id="823" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh Jude ">κατ᾽ αὐτοῦ ἁμαρτωλοὶ ἀσεβεῖς.</reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'      </div>\n      '
      ]
     ),
    ((107, 1),
     2,
     [u'<div number="107">\n        <div number="1">\n          <unit id="1347" group="0" parallel="">\n            <reading option="0" mss="CB185 "> Τότε τεθέαμαι τὰ ἐγγεγραμμένα ἐπ᾽ αὐτῶν, ὅτι γενεὰ γενεᾶς κακ[ίων ἔσται], καὶ εἶδον τόδε μέχρις τοῦ ἀνασ[τῆναι] γενεὰν δικαιοσύνης καὶ ἡ κακία ἀπολεῖται καὶ ἡ ἁμαρτία ἀλλάξει ἀπὸ τῆς γῆς καὶ τὰ ἀγαθὰ ἥξει ἐπὶ τῆς γῆς ἐπ᾽ αὐτούς. </reading>\n          </unit>\n        </div>\n        <div number="2">\n          <unit id="1348" group="0" parallel="">\n            <reading option="0" mss="CB185 ">καὶ νῦν ἀπότρεχε τέκνον καὶ σήμανον Λάμεχ τῷ υἱῷ σου ὅτι τὸ παιδίον τοῦτο τὸ γεννηθὲν τέκνον αὐτοῦ ἐστιν δικαίως καὶ οὐ ψευδῶς. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="2">\n'  # FIXME: why is there a second div wrapping this?
      u'          <unit id="1349" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ ὅτε ἤκουσεν Μαθουσάλεκ τοὺς λόγους '
      u'Ἑνώχ τοῦ πατρὸς αὐτοῦ, μυστηριακῶς γὰρ ἐδήλωσεν αὐτῷ, [ἐπέστρεψεν καὶ '
      u'ἐδήλωσεν αὐτῷ.] καὶ ἐκλήθη τὸ ὄνομα αὐτοῦ Νῶε, εὐφραίνων τὴν γῆν ἀπὸ '
      u'τῆς ἀπωλείας. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'      </div>\n    ',
      u'<div number="1">\n'
      u'          <unit id="1347" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 "> Τότε τεθέαμαι τὰ ἐγγεγραμμένα ἐπ᾽ '
      u'αὐτῶν, ὅτι γενεὰ γενεᾶς κακ[ίων ἔσται], καὶ εἶδον τόδε μέχρις τοῦ '
      u'ἀνασ[τῆναι] γενεὰν δικαιοσύνης καὶ ἡ κακία ἀπολεῖται καὶ ἡ ἁμαρτία '
      u'ἀλλάξει ἀπὸ τῆς γῆς καὶ τὰ ἀγαθὰ ἥξει ἐπὶ τῆς γῆς ἐπ᾽ αὐτούς. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n        ']
     ),
])
def test_div_path_to_element_path(test_book, myref, mylength, expected):
    myversion = version = test_book._get("version", {"title": "Greek"})
    actual = test_book._div_path_to_element_path(myversion, myref)

    print len(actual), 'actual elements ---------------------------------------------'
    print actual
    for a in actual:
        print '--------------------------------'
        print etree.tostring(a, encoding='utf-8')

    assert len(actual) == mylength == len(expected)
    for idx, a in enumerate(actual):
        assert isinstance(a, etree._Element)
        a = etree.tostring(a, encoding='unicode')
        b = expected[idx]
        print 'item', idx, '-------------------'
        print u''.join(difflib.unified_diff(a, b))
        assert a == expected[idx]


@pytest.mark.parametrize("myref,mylength,mylevel,mydir,expected", [
    ((1,),  # case 1 ----------------------------------------------------
     1,
     0,  # mylevel
     'next',
     [u'<div number="2">\n'
      u'        <div number="1">\n'
      u'          <unit id="824" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh "> Κατανοήσατε πάντα τὰ ἔργα ἐν τῷ οὐρανῷ, πῶς οὐκ ἠλλοίωσαν τὰς ὁδοὺς αὐτῶν, καὶ τοὺς φωστῆρας τοὺς ἐν τῷ οὐρανῷ ὡς τὰ πάντα ἀνατέλλει καὶ δύνει, τεταγμένος ἕκαστος ἐν τῷ τεταγμένῳ καιρῷ, καὶ ταῖς ἑορταῖς αὐτῶν φαίνονται, </read'
      u'ing>\n'
      u'          </unit>\n'
      u'          <unit id="825" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">καὶ οὐ παραβαίνουσιν τὴν ἰδίαν τάξιν. </reading>\n'
      u'            <reading option="1" mss="TestOne">καὶ</reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="2">\n'
      u'          <unit id="826" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">ἴδετε τὴν γῆν καὶ διανοήθητε περὶ τῶν ἔργων τῶν ἐν αὐτῇ </reading>\n'
      u'          </unit>\n'
      u'          <unit id="827" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">γεινομενων </reading>\n'
      u'            <reading option="1" mss="Black ">γενομένων </reading>\n'
      u'            <reading option="2" mss="Swete Charles Dindorf ">γινομένων </reading>\n'
      u'          </unit>\n'
      u'          <unit id="828" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">ἀπ᾽ ἀρχῆς μέχρι τελειώσεως ὥς εἰσιν φθαρτά, ὡς οὐκ ἀλλοιοῦνται, οὐδὲν τῶν ἐπὶ γῆς, ἀλλὰ πάντα ἔργα θεοῦ ὑμῖν φαίνεται. </reading>\n'
      u'            <reading option="1" mss="TestOne ">Lorem <w lang="lang" morph="morph" lex="lex" style="style">ipsum</w> dolor <w>sit</w> amet</reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="3">\n'
      u'          <unit id="829" group="0" parallel="">\n'
      u'            <reading option="0" mss="Gizeh ">ἴδετε τὴν θερείαν καὶ τὸν χειμῶνα ...</reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'      </div>\n      '
      ]
     ),
    ((106, 1),
     2,
     0,  # mylevel
     'next',
     [u'<div number="107">\n'
      u'        <div number="1">\n'
      u'          <unit id="1347" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 "> Τότε τεθέαμαι τὰ ἐγγεγραμμένα ἐπ᾽ '
      u'αὐτῶν, ὅτι γενεὰ γενεᾶς κακ[ίων ἔσται], καὶ εἶδον τόδε μέχρις τοῦ '
      u'ἀνασ[τῆναι] γενεὰν δικαιοσύνης καὶ ἡ κακία ἀπολεῖται καὶ ἡ ἁμαρτία '
      u'ἀλλάξει ἀπὸ τῆς γῆς καὶ τὰ ἀγαθὰ ἥξει ἐπὶ τῆς γῆς ἐπ᾽ αὐτούς. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="2">\n'
      u'          <unit id="1348" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ νῦν ἀπότρεχε τέκνον '
      u'καὶ σήμανον Λάμεχ τῷ υἱῷ σου ὅτι τὸ παιδίον τοῦτο τὸ γεννηθὲν τέκνον '
      u'αὐτοῦ ἐστιν δικαίως καὶ οὐ ψευδῶς. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="2">\n'  # FIXME: why is there a second div wrapping this?
      u'          <unit id="1349" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ ὅτε ἤκουσεν Μαθουσάλεκ τοὺς λόγους '
      u'Ἑνώχ τοῦ πατρὸς αὐτοῦ, μυστηριακῶς γὰρ ἐδήλωσεν αὐτῷ, [ἐπέστρεψεν καὶ '
      u'ἐδήλωσεν αὐτῷ.] καὶ ἐκλήθη τὸ ὄνομα αὐτοῦ Νῶε, εὐφραίνων τὴν γῆν ἀπὸ '
      u'τῆς ἀπωλείας. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'      </div>\n    ',
      u'<div number="1">\n'
      u'          <unit id="1347" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 "> Τότε τεθέαμαι τὰ ἐγγεγραμμένα ἐπ᾽ '
      u'αὐτῶν, ὅτι γενεὰ γενεᾶς κακ[ίων ἔσται], καὶ εἶδον τόδε μέχρις τοῦ '
      u'ἀνασ[τῆναι] γενεὰν δικαιοσύνης καὶ ἡ κακία ἀπολεῖται καὶ ἡ ἁμαρτία '
      u'ἀλλάξει ἀπὸ τῆς γῆς καὶ τὰ ἀγαθὰ ἥξει ἐπὶ τῆς γῆς ἐπ᾽ αὐτούς. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n        ']
     ),
    ((106, 1),
     2,
     1,  # mylevel
     'next',
     [u'<div number="106">\n'
      u'        <div number="1">\n'
      u'          <unit id="1328" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">μετὰ δὲ χρόνον ἔλαβεν Μαθουσάλεκ τῷ υἱῷ μου γυναῖκα καὶ ἔτεκεν υἱὸν καὶ ἐκάλεσεν τὸ ὄνομα αὐτοῦ Λάμεχ. ἐταπεινώθη ἡ δικαιοσύνη μέχρι τῆς ἡμέρας ἐκείνης. καὶ ὅτε εἰς ἡλικίαν ἐπῆλθεν, ἔλαβεν αὐτῷ γυναῖκα καὶ ἔτεκεν αὐτῷ παιδίον, </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="2">\n'
      u'          <unit id="1329" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ ὅτε ἐγεννήθη τὸ παιδίον ἦν τὸ σῶμα λευκότερον χιόνος καὶ πυρρότερον ῥόδου, τὸ τρίχωμα πᾶν λευκὸν καὶ ὡς ἔρια λευκὰ καὶ οὖλον καὶ ἔνδοξον. καὶ ὅτε ἀνέῳξεν τοὺς ὀφθαλμούς, ἔλαμψεν ἡ οἰκία ὡσεὶ ἥλιος. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="3">\n'
      u'          <unit id="1330" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ ἀνέστη ἐκ τῶν χειρῶν τῆς μαίας καὶ ἀνέῳξεν τὸ στόμα καὶ εὐλόγησεν τῷ κυρίῳ·</reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="4">\n'
      u'          <unit id="1331" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ ἐφοβήθη Λάμεχ ἀπ᾽ αὐτοῦ καὶ ἔφυγεν καὶ ἦλθεν πρὸς Μαθουσάλεκ τὸν πατέρα αὐτοῦ καὶ εἶπεν αὐτῷ, </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="5">\n'
      u'          <unit id="1332" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">τέκνον ἐγεννήθη μου ἀλλοῖον, οὐχ ὅμοιον τοῖς ἀνθρώποις ἀλλὰ τοῖς τέκνοις τῶν ἀγγέλων τοῦ οὐρανοῦ, καὶ ὁ τύπος ἀλλοιότερος, οὐχ ὅμοιος ἡμῖν· τὰ ὄμματά ἐστιν ὡς ἀκτῖνες τοῦ ἡλίου, καὶ ἔνδοξον τὸ πρόσωπον· </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="6">\n'
      u'          <unit id="1333" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ ὑπολαμβάνω ὅτι οὐκ ἔστιν ἐξ ἐμοῦ ἀλλὰ ἐξ ἀγγέλου, καὶ εὐλαβοῦμαι αὐτὸν μήποτέ τι ἔσται ἐν ταῖς ἡμέραις αὐτοῦ ἐν τῇ γῇ. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="7">\n'
      u'          <unit id="1334" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ παραιτοῦμαι, π[άτερ, καὶ] δέομαι, βάδισον πρὸς Ἑνὼ[χ τὸν πατέρα ἡμῶν καὶ ἐρώτησον] . . . </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="8">\n'
      u'          <unit id="1335" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">. . . [ἦλθ]εν πρὸς ἐμὲ εἰς τὰ τέρματα τῆς γῆς οὗ [εἶδ]εν τότε εἶναι με καὶ εἶπέν μοι, πάτερ [μου] ἐπάκουσον τῆς φωνῆς μου καὶ ἧκε [πρὸς] ἐμέ. καὶ ἤκουσα τὴν φωνὴν αὐτοῦ καὶ ἦλθον πρὸς αὐτὸν καὶ εἶπα, ἰδοὺ πάρειμι τέκνον· διὰ τί ἐλήλυθας πρὸς ἐμέ, τέκνον; </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="9">\n'
      u'          <unit id="1336" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ ἀπεκρίθη λέγων, δι᾽ ἀνάγκην μεγάλην ἦλθον ὧδε, πάτερ· </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="10">\n'
      u'          <unit id="1337" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ νῦν ἐγεννήθη τέκνον Λάμεχ τῷ υἱῷ μου, καὶ ὁ τύπος αὐτοῦ καὶ ἡ εἰκὼν αὐτοῦ {οὐχ ὅμοιος ἀνθρώποις καὶ τὸ χρῶμα αὐτοῦ} λευκότερον χιόνος καὶ πυρρότερον ῥόδου, καὶ τὸ τρίχωμα τῆς κεφαλῆς αὐτοῦ λευκότερον ἐρίων λευκῶν, καὶ τὰ ὄμματα αὐτοῦ ἀφόμοια ταῖς τοῦ ἡλίου ἀκτῖσιν, </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="11">\n'
      u'          <unit id="1338" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ ἀνέστη ἀπὸ τῶν τῆς μαίας χειρῶν καὶ ἀνοίξας τὸ στόμα εὐλόγησεν τὸν κύριον τοῦ αἰῶνος· </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="12">\n'
      u'          <unit id="1339" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ ἐφοβήθη ὁ υἱός μου Λάμεχ, καὶ ἔφυγεν πρὸς ἐμέ, καὶ οὐ πιστεύει ὅτι υἱὸς αὐτοῦ ἐστιν, ἀλλὰ ὅτι ἐξ ἀγγέλων . . . τὴν ἀκρίβειαν ἣν ἔχεις καὶ τὴν ἀλήθειαν. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="13">\n'
      u'          <unit id="1340" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">τότε ἀπεκρίθην λέγων, ἀνακαινίσει ὁ κύριος πρόσταγμα ἐπὶ τῆς γῆς, καὶ τὸν αὐτὸν τρόπον τέκνον τεθέαμαι καὶ ἐσήμανά σοι· ἐν γὰρ τῇ γενεᾷ Ἰάρεδ τοῦ πατρός μου παρέβησαν τὸν λόγον κυρίου ἀπὸ τῆς διαθήκης τοῦ οὐρανοῦ. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="14">\n'
      u'          <unit id="1341" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ ἰδοὺ ἁμαρτάνουσιν καὶ παραβαίνουσιν τὸ ἔθος, καὶ μετὰ γυναικῶν συγγίνονται καὶ μετ᾽ αὐτῶν ἁμαρτάνουσιν καὶ ἔγημαν ἐξ αὐτῶν, 17a. καὶ τίκτουσιν οὐχ ὁμοίους πνεύμασιν ἀλλὰ σαρκίνους· </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="15">\n'
      u'          <unit id="1342" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ ἔσται ὀργὴ μεγάλη ἐπὶ τῆς γῆς καὶ κατακλυσμός, καὶ ἔσται ἀπώλεια μεγάλη ἐπὶ ἐνιαυτὸν ἕνα· </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="16">\n'
      u'          <unit id="1343" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ τόδε τὸ παιδίον τὸ γεννηθὲν καταλειφθήσεται, καὶ τρία αὐτοῦ͂ τέκνα σωθήσεται ἀποθανόντων τῶν ἐπὶ τῆς γῆς· </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="17b">\n'
      u'          <unit id="1344" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ πραϋνεῖ τὴν γῆν ἀπὸ τῆς οὔσης ἐν αὐτῇ φθορᾶς. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="18">\n'
      u'          <unit id="1345" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ νῦν λέγε Λάμεχ ὅτι τέκνον σου ἐστιν δικαίως καὶ ὁσίως, [καὶ] κάλεσον αὐτοῦ τὸ ὄνομα [Νῶε]· αὐτὸς γὰρ ἔσται ὑμῶν κατάλειμμα ἐφ᾽ οὗ ἂν καταπαύσητε καὶ {οἱ} υἱοὶ αὐτοῦ ἀπὸ τῆς φθορᾶς τῆς γῆς καὶ ἀπὸ πάντων τῶν ἁμαρτωλῶν καὶ ἀπὸ πασῶν τῶν συντελειῶν ἐπὶ τῆς γῆς . . . </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="19">\n'
      u'          <unit id="1346" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">ὑπέδειξέν μοι καὶ ἐμήνυσεν, καὶ ἐν ταῖς πλαξὶν τοῦ οὐρανοῦ ἀνέγνων αὐτά.</reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'      </div>\n      ',  # ==========================================
      u'<div number="2">\n'
      u'          <unit id="1329" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ ὅτε ἐγεννήθη τὸ παιδίον ἦν τὸ σῶμα λευκότερον χιόνος καὶ πυρρότερον ῥόδου, τὸ τρίχωμα πᾶν λευκὸν καὶ ὡς ἔρια λευκὰ καὶ οὖλον καὶ ἔνδοξον. καὶ ὅτε ἀνέῳξεν τοὺς ὀφθαλμούς, ἔλαμψεν ἡ οἰκία ὡσεὶ ἥλιος. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n        '
      ]
     ),
    ((107, 1),  # case 2 ------------------------------------------------
     2,
     0,  # mylevel
     'next',
     [u'<div number="107">\n'
      u'        <div number="1">\n'
      u'          <unit id="1347" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 "> Τότε τεθέαμαι τὰ ἐγγεγραμμένα ἐπ᾽ '
      u'αὐτῶν, ὅτι γενεὰ γενεᾶς κακ[ίων ἔσται], καὶ εἶδον τόδε μέχρις τοῦ '
      u'ἀνασ[τῆναι] γενεὰν δικαιοσύνης καὶ ἡ κακία ἀπολεῖται καὶ ἡ ἁμαρτία '
      u'ἀλλάξει ἀπὸ τῆς γῆς καὶ τὰ ἀγαθὰ ἥξει ἐπὶ τῆς γῆς ἐπ᾽ αὐτούς. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="2">\n'
      u'          <unit id="1348" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ νῦν ἀπότρεχε τέκνον '
      u'καὶ σήμανον Λάμεχ τῷ υἱῷ σου ὅτι τὸ παιδίον τοῦτο τὸ γεννηθὲν τέκνον '
      u'αὐτοῦ ἐστιν δικαίως καὶ οὐ ψευδῶς. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'        <div number="2">\n'  # FIXME: why is there a second div wrapping this?
      u'          <unit id="1349" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 ">καὶ ὅτε ἤκουσεν Μαθουσάλεκ τοὺς λόγους '
      u'Ἑνώχ τοῦ πατρὸς αὐτοῦ, μυστηριακῶς γὰρ ἐδήλωσεν αὐτῷ, [ἐπέστρεψεν καὶ '
      u'ἐδήλωσεν αὐτῷ.] καὶ ἐκλήθη τὸ ὄνομα αὐτοῦ Νῶε, εὐφραίνων τὴν γῆν ἀπὸ '
      u'τῆς ἀπωλείας. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n'
      u'      </div>\n    ',
      u'<div number="1">\n'
      u'          <unit id="1347" group="0" parallel="">\n'
      u'            <reading option="0" mss="CB185 "> Τότε τεθέαμαι τὰ ἐγγεγραμμένα ἐπ᾽ '
      u'αὐτῶν, ὅτι γενεὰ γενεᾶς κακ[ίων ἔσται], καὶ εἶδον τόδε μέχρις τοῦ '
      u'ἀνασ[τῆναι] γενεὰν δικαιοσύνης καὶ ἡ κακία ἀπολεῖται καὶ ἡ ἁμαρτία '
      u'ἀλλάξει ἀπὸ τῆς γῆς καὶ τὰ ἀγαθὰ ἥξει ἐπὶ τῆς γῆς ἐπ᾽ αὐτούς. </reading>\n'
      u'          </unit>\n'
      u'        </div>\n        ']
     ),
])
def test_get_next_or_prev(test_book, myref, mylength, mylevel, mydir, expected):
    myversion = version = test_book._get("version", {"title": "Greek"})
    edivs = test_book._div_path_to_element_path(myversion, myref)
    print len(edivs), 'elements from prior function ------------------------------------'
    print edivs
    for e in edivs:
        print '--------------------------------'
        print etree.tostring(e, encoding='utf-8')

    actual = test_book._get_next_or_prev(edivs, mylevel, direction=mydir)
    print len(actual), 'actual elements ---------------------------------------------'
    print actual
    for a in actual:
        print '--------------------------------'
        print etree.tostring(a, encoding='utf-8')

    assert len(actual) == mylength == len(expected)
    for idx, a in enumerate(actual):
        assert isinstance(a, etree._Element)
        a = etree.tostring(a, encoding='unicode')
        b = expected[idx]
        print 'item', idx, '-------------------'
        print u''.join(difflib.unified_diff(a, b))
        assert a == expected[idx]


@pytest.mark.parametrize("mystartref,myendref,mynext,myprev,expected_start_sel,"
                         "expected_end_sel,expected_list", [
    ((107,),  # case 1 ----------------------------------------------------
     None,  # myendref
     None,  # mynext
     None,  # myprev
     ('107', '1'),
     ('107', '2'),
     [Text(("107", "1"), "1347", "Greek", 1, "", "", None),
      Text(("107", "2"), "1348", "Greek", 1, "", "", None),
      Text(("107", "2"), "1349", "Greek", 1, "", "", None)]
     ),
    ((1,),  # same start and end at level 1 -----------------------------------
     (1,),
     None,  # mynext
     None,  # myprev
     ('1', '1'),
     ('1', '9'),
     [Text(("1", "1"), "788", "Greek", 2, "", "", u"Λόγος"),
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
     ),
    ((1, 1),  # first sub-div only
     (1, 1),
     None,  # mynext
     None,  # myprev
     ('1', '1'),
     ('1', '1'),
     [Text(("1", "1"), "788", "Greek", 2, "", "", u"Λόγος")]
     ),
    ((1, 1),  # next at level 0 -----------------------------------------------
     (1, 1),
     0,  # mynext
     None,  # myprev
     ('2', '1'),
     ('2', '3'),
     [Text(div_path=('2', '1'), unit_id='824', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('2', '1'), unit_id='825', language='Greek', readings_in_unit=2, linebreak='', indent='', text=u'\u03ba\u03b1\u1f76'),
      Text(div_path=('2', '2'), unit_id='826', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('2', '2'), unit_id='827', language='Greek', readings_in_unit=3, linebreak='', indent='', text=None),
      Text(div_path=('2', '2'), unit_id='828', language='Greek', readings_in_unit=2, linebreak='', indent='', text=('Lorem ', W(attributes={'lang': 'lang', 'lex': 'lex', 'style': 'style', 'morph': 'morph'}, text='ipsum'), ' dolor ', W(attributes={}, text='sit'), ' amet')),
      Text(div_path=('2', '3'), unit_id='829', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None)]
     ),
    ((2, 1),  # prev at level 0 -----------------------------------------------
     (2, 3),
     None,  # mynext
     0,  # myprev
     ('1', '1'),
     ('1', '9'),
     [Text(div_path=('1', '1'), unit_id='788', language='Greek', readings_in_unit=2, linebreak='', indent='', text=u'\u039b\u1f79\u03b3\u03bf\u03c2'),
      Text(div_path=('1', '2'), unit_id='789', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '2'), unit_id='790', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '2'), unit_id='791', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '2'), unit_id='792', language='Greek', readings_in_unit=2, linebreak='', indent='', text=None),
      Text(div_path=('1', '2'), unit_id='793', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '2'), unit_id='794', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '2'), unit_id='795', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '2'), unit_id='796', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '3'), unit_id='797', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '3'), unit_id='798', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '4'), unit_id='799', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '4'), unit_id='800', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '4'), unit_id='801', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '5'), unit_id='802', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '5'), unit_id='803', language='Greek', readings_in_unit=2, linebreak='', indent='', text=None),
      Text(div_path=('1', '5'), unit_id='804', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '6'), unit_id='805', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '6'), unit_id='806', language='Greek', readings_in_unit=2, linebreak='', indent='', text=None),
      Text(div_path=('1', '6'), unit_id='807', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '7'), unit_id='808', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '8'), unit_id='809', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '8'), unit_id='810', language='Greek', readings_in_unit=2, linebreak='', indent='', text=None),
      Text(div_path=('1', '8'), unit_id='811', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '9'), unit_id='812', language='Greek', readings_in_unit=3, linebreak='yes', indent='', text=''),
      Text(div_path=('1', '9'), unit_id='813', language='Greek', readings_in_unit=3, linebreak='', indent='', text=None),
      Text(div_path=('1', '9'), unit_id='814', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '9'), unit_id='815', language='Greek', readings_in_unit=3, linebreak='', indent='yes', text=u'\u1f10\u03bb\u1f73\u03b3\u03be\u03b1\u03b9 '),
      Text(div_path=('1', '9'), unit_id='816', language='Greek', readings_in_unit=1, linebreak='', indent='', text=u'\u03c0\u1f71\u03bd\u03c4\u03b1\u03c2 \u03c4\u03bf\u1f7a\u03c2 \u1f00\u03c3\u03b5\u03b2\u03b5\u1fd6\u03c2, '),
      Text(div_path=('1', '9'), unit_id='817', language='Greek', readings_in_unit=2, linebreak='', indent='', text=None),
      Text(div_path=('1', '9'), unit_id='818', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '9'), unit_id='819', language='Greek', readings_in_unit=2, linebreak='', indent='', text=None),
      Text(div_path=('1', '9'), unit_id='820', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '9'), unit_id='821', language='Greek', readings_in_unit=2, linebreak='', indent='', text=None),
      Text(div_path=('1', '9'), unit_id='822', language='Greek', readings_in_unit=2, linebreak='', indent='', text=None),
      Text(div_path=('1', '9'), unit_id='823', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None)]
     ),
    ((1, 1),  # next at level 1 -----------------------------------------------
     (1, 1),
     1,  # mynext
     None,  # myprev
     ('1', '2'),
     ('1', '2'),
     [Text(div_path=('1', '2'), unit_id='789', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '2'), unit_id='790', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '2'), unit_id='791', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '2'), unit_id='792', language='Greek', readings_in_unit=2, linebreak='', indent='', text=None),
      Text(div_path=('1', '2'), unit_id='793', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '2'), unit_id='794', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '2'), unit_id='795', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None),
      Text(div_path=('1', '2'), unit_id='796', language='Greek', readings_in_unit=1, linebreak='', indent='', text=None)
      ]
     ),
    ((1, 2),  # prev at level 1 -----------------------------------------------
     (1, 2),
     None,  # mynext
     1,  # myprev
     ('1', '1'),
     ('1', '1'),
     [Text(div_path=('1', '1'), unit_id='788', language='Greek', readings_in_unit=2, linebreak='', indent='', text=u'\u039b\u1f79\u03b3\u03bf\u03c2')
      ]
     ),
    ((2, 2),  # last sub-div in parent div -----------------------------------
     (2, 2),
     None,  # mynext
     None,  # myprev
     ('2', '2'),
     ('2', '2'),
     [Text(("2", "2"), "826", "Greek", 1, "", "", None),
      Text(("2", "2"), "827", "Greek", 3, "", "", None),
      Text(("2", "2"), "828", "Greek", 2, "", "", ("Lorem ",
                                                   W({"morph": "morph",
                                                      "lex": "lex",
                                                      "style": "style",
                                                      "lang": "lang"}, "ipsum"),
                                                   " dolor ",
                                                   W({}, u"sit"),
                                                   " amet"))]
     ),
    ((1, 9),  # incomplete end sel --------------------------------------------
     (2,),
     None,  # mynext
     None,  # myprev
     ('1', '9'),
     ('2', '3'),
     [Text(("1", "9"), "812", "Greek", 3, "yes", "", u""),
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
     ),
    ((1, 9, 3, 4, 5),  # invalid start and end -------------------------------
     (2, 2, "X", "Y"),
     None,  # mynext
     None,  # myprev
     ('1', '9'),
     ('2', '2'),
     [Text(("1", "9"), "812", "Greek", 3, "yes", "", u""),
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
     ),
    ])
def test_book_get_text(test_book, mystartref, myendref, mynext, myprev,
                       expected_start_sel, expected_end_sel, expected_list):
    result_iter, startsel, endsel = test_book.get_text("Greek", "TestOne",
                                                       mystartref, myendref,
                                                       next_level=mynext,
                                                       previous_level=myprev)
    actual_text = list(result_iter)
    print actual_text
    assert actual_text == expected_list
    assert startsel == expected_start_sel
    assert endsel == expected_end_sel


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
    result = test_book.get_readings("Greek", 812)
    expected = [Reading("7QEnoch", None),
                Reading("POxy2069", None),
                Reading("CB185", None),
                Reading("V1809", None),
                Reading("Gizeh", u"ὅτι ἔρχεται"),
                Reading("Gizeh2", None),
                Reading("Syncellus", None),
                Reading("Jude", u"ἰδοὺ ἦλθεν κύριος"),
                Reading("TestOne", u""),
                Reading("TestTwo", None)]
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
    expected = OrderedDict({"812": [Reading("7QEnoch", None),
                                    Reading("POxy2069", None),
                                    Reading("CB185", None),
                                    Reading("V1809", None),
                                    Reading("Gizeh", u"ὅτι ἔρχεται"),
                                    Reading("Gizeh2", None),
                                    Reading("Syncellus", None),
                                    Reading("Jude", u"ἰδοὺ ἦλθεν κύριος"),
                                    Reading("TestOne", u""),
                                    Reading("TestTwo", None)],
                            "813": [Reading("7QEnoch", None),
                                    Reading("POxy2069", None),
                                    Reading("CB185", None),
                                    Reading("V1809", None),
                                    Reading("Gizeh", u"σὺν ταῖς μυριάσιν αὐτοῦ καὶ τοῖς ἁγίοις αὐτοῦ,"),
                                    Reading("Gizeh2", None),
                                    Reading("Syncellus", None),
                                    Reading("Jude", u"ἐν ἁγίαις μυριάσιν αὐτοῦ,"),
                                    Reading("TestOne", None),
                                    Reading("TestTwo", u"ἐν ἁγίαις μυριάσιν αὐτοῦ,")],
                            "814": [Reading("7QEnoch", None),
                                    Reading("POxy2069", None),
                                    Reading("CB185", None),
                                    Reading("V1809", None),
                                    Reading("Gizeh2", None),
                                    Reading("Syncellus", None),
                                    Reading("TestOne", None),
                                    Reading("TestTwo", None),
                                    Reading("Gizeh Jude", u"ποιῆσαι κρίσιν κατὰ πάντων, καὶ")]})
    assert result == expected


def test_book_get_group_w_invalid_group_id(test_book):
    result = test_book.get_group("Greek", "2000")
    expected = OrderedDict()
    assert result == expected


# BookManager tests


@pytest.mark.parametrize("refdicts,as_gluon,expected", [
    ([{"book": "test_parse", "version": "Greek", "text_type": "TestOne",
       "start": (1, 1), "end": (1, 1)},
      {"book": "test_parse", "version": "Greek", "text_type": "TestOne",
       "start": (1, 1), "end": (1, 1)}
      ],
     False,  # as_gluon
     {"result": [([Text(div_path=('1', '1'), unit_id='788', language='Greek',
                       readings_in_unit=2, linebreak='', indent='',
                       text=u'\u039b\u1f79\u03b3\u03bf\u03c2')
                   ],
                  ('1', '1'),
                  ('1', '1')
                  ),
                 ([Text(div_path=('1', '1'), unit_id='788', language='Greek',
                       readings_in_unit=2, linebreak='', indent='',
                       text=u'\u039b\u1f79\u03b3\u03bf\u03c2')
                   ],
                  ('1', '1'),
                  ('1', '1')
                  ),
                 ],
      "error": [None, None]}
     ),
    ([{"book": "Xtest_parse",  # invalid book ------------------------------
       "version": "Greek", "text_type": "TestOne",
       "start": (1,)}],
     False,
     {"result": [],
      "error": ["[Errno 2] No such file or directory: '{}/Xtest_parse.xml'".format(
          XML_DRAFT_FILE_STORAGE_PATH)]}
     ),
    ([{"book": "test_parse",  # mixed valid and invalid ---------------------
       "version": "Greek", "text_type": "TestOne",
       "start": (1, 1), "end": (1, )},
      {"book": "Xtest_parse", "version": "Greek", "text_type": "TestOne",
       "start": (1,)},
      {"book": "test_parse", "version": "Greek", "text_type": "TestOne",
       "start": (2, ), "end": (2, )},
      {"book": "test_parse", "version": "XGreek", "text_type": "TestOne",
       "start": (1,)}
      ],
     False,  # as_gluon
     {"result": [([Text(("1", "1"), "788", "Greek", 2, "", "", u"Λόγος"),
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
                   ],
                  ('1', '1'),
                  ('1', '9')
                  ),
                 ([Text(("2", "1"), "824", "Greek", 1, "", "", None),
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
                   Text(("2", "3"), "829", "Greek", 1, "", "", None)
                   ],
                  ('2', '1'),
                  ('2', '3')
                  )
                 ],
                "error": [None,
                          "[Errno 2] No such file or directory: '{}/Xtest_parse.xml'".format(
                              XML_DRAFT_FILE_STORAGE_PATH),
                          None,
                          "<version> element with title='XGreek' does not exist"]}
     ),
])
def test_bookman_get_text(refdicts, as_gluon, expected):
    actual = BookManager.get_text(refdicts, as_gluon=as_gluon)

    assert actual['error'] == expected['error']
    if not all(a for a in actual['error'] if not a):
        for idx, r in enumerate(actual['result']):
            actual_text = list(r[0])
            print 'result', idx, '=================='
            pprint(actual_text)
            assert len(actual_text) == len(expected['result'][idx][0])
            assert actual_text == expected['result'][idx][0]
            assert r[1] == expected['result'][idx][1]
            assert r[2] == expected['result'][idx][2]
    else:
        assert actual['result'] == expected['result']


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
    result = BookManager.get_readings([{"book": "test_parse", "version": "Greek", "unit_id": 810},
                                       {"book": "test_parse", "version": "Greek", "unit_id": 812}],
                                      as_gluon=False)
    expected = {"result": [[Reading("7QEnoch", None),
                            Reading("POxy2069", None),
                            Reading("CB185", None),
                            Reading("V1809", None),
                            Reading("Gizeh", u"γενηται"),
                            Reading("Gizeh2", None),
                            Reading("Syncellus", None),
                            Reading("Jude", None),
                            Reading("TestOne", None),
                            Reading("Swete Charles Black Dindorf TestTwo", u"γενήσεται")],
                           [Reading("7QEnoch", None),
                            Reading("POxy2069", None),
                            Reading("CB185", None),
                            Reading("V1809", None),
                            Reading("Gizeh", u"ὅτι ἔρχεται"),
                            Reading("Gizeh2", None),
                            Reading("Syncellus", None),
                            Reading("Jude", u"ἰδοὺ ἦλθεν κύριος"),
                            Reading("TestOne", u""),
                            Reading("TestTwo", None)]],
                "error": [None, None]}
    assert result["result"][0] == expected["result"][0]
    assert result["result"][1] == expected["result"][1]
    assert result["error"] == expected["error"]


def test_bookman_get_readings_as_gluon():
    result = BookManager.get_readings([{"book": "test_parse", "version": "Greek", "unit_id": 810},
                                       {"book": "test_parse", "version": "Greek", "unit_id": 812}],
                                      as_gluon=True)
    expected = {"result": ['<dl>'
                           '<dt>7QEnoch</dt><dd>†</dd>'
                           '<dt>POxy2069</dt><dd>†</dd>'
                           '<dt>CB185</dt><dd>†</dd>'
                           '<dt>V1809</dt><dd>†</dd>'
                           '<dt>Gizeh</dt><dd>γενηται</dd>'
                           '<dt>Gizeh2</dt><dd>†</dd>'
                           '<dt>Syncellus</dt><dd>†</dd>'
                           '<dt>Jude</dt><dd>†</dd>'
                           '<dt>TestOne</dt><dd>†</dd>'
                           '<dt>Swete Charles Black Dindorf TestTwo</dt><dd>γενήσεται</dd>'
                           '</dl>',
                           '<dl>'
                           '<dt>7QEnoch</dt><dd>†</dd>'
                           '<dt>POxy2069</dt><dd>†</dd>'
                           '<dt>CB185</dt><dd>†</dd>'
                           '<dt>V1809</dt><dd>†</dd>'
                           '<dt>Gizeh</dt><dd>ὅτι ἔρχεται</dd>'
                           '<dt>Gizeh2</dt><dd>†</dd>'
                           '<dt>Syncellus</dt><dd>†</dd>'
                           '<dt>Jude</dt><dd>ἰδοὺ ἦλθεν κύριος</dd>'
                           '<dt>TestOne</dt><dd></dd>'
                           '<dt>TestTwo</dt><dd>†</dd>'
                           '</dl>'],
                "error": [None, None]}
    assert str(result["result"][0]) == str(expected["result"][0])
    assert str(result["result"][1]) == str(expected["result"][1])
    assert result["error"] == expected["error"]


def test_bookman_get_unit_group():
    result = BookManager.get_unit_group([{"book": "test_parse", "version": "Greek", "unit_id": 812},
                                         {"book": "test_parse", "version": "Greek", "unit_id": 813}])
    expected = {"result": [[10, 14], [14, 10]],
                "error": [None, None]}
    assert result["result"] == expected["result"]
    assert result["error"] == expected["error"]


def test_bookman_get_group():
    result = BookManager.get_group([{"book": "test_parse", "version": "Greek", "unit_group": 14},
                                    {"book": "test_parse", "version": "Greek", "unit_group": 10}],
                                   as_gluon=False)
    expected = {"result": [OrderedDict({"812": [Reading("7QEnoch", None),
                                                Reading("POxy2069", None),
                                                Reading("CB185", None),
                                                Reading("V1809", None),
                                                Reading("Gizeh", u"ὅτι ἔρχεται"),
                                                Reading("Gizeh2", None),
                                                Reading("Syncellus", None),
                                                Reading("Jude", u"ἰδοὺ ἦλθεν κύριος"),
                                                Reading("TestOne", u""),
                                                Reading("TestTwo", None)],
                                        "813": [Reading("7QEnoch", None),
                                                Reading("POxy2069", None),
                                                Reading("CB185", None),
                                                Reading("V1809", None),
                                                Reading("Gizeh", u"σὺν ταῖς μυριάσιν αὐτοῦ καὶ τοῖς ἁγίοις αὐτοῦ,"),
                                                Reading("Gizeh2", None),
                                                Reading("Syncellus", None),
                                                Reading("Jude", u"ἐν ἁγίαις μυριάσιν αὐτοῦ,"),
                                                Reading("TestOne", None),
                                                Reading("TestTwo", u"ἐν ἁγίαις μυριάσιν αὐτοῦ,")],
                                        "814": [Reading("7QEnoch", None),
                                                Reading("POxy2069", None),
                                                Reading("CB185", None),
                                                Reading("V1809", None),
                                                Reading("Gizeh2", None),
                                                Reading("Syncellus", None),
                                                Reading("TestOne", None),
                                                Reading("TestTwo", None),
                                                Reading("Gizeh Jude", u"ποιῆσαι κρίσιν κατὰ πάντων, καὶ")]}),
                           OrderedDict({"812": [Reading("7QEnoch", None),
                                                Reading("POxy2069", None),
                                                Reading("CB185", None),
                                                Reading("V1809", None),
                                                Reading("Gizeh", u"ὅτι ἔρχεται"),
                                                Reading("Gizeh2", None),
                                                Reading("Syncellus", None),
                                                Reading("Jude", u"ἰδοὺ ἦλθεν κύριος"),
                                                Reading("TestOne", u""),
                                                Reading("TestTwo", None)],
                                        "813": [Reading("7QEnoch", None),
                                                Reading("POxy2069", None),
                                                Reading("CB185", None),
                                                Reading("V1809", None),
                                                Reading("Gizeh", u"σὺν ταῖς μυριάσιν αὐτοῦ καὶ τοῖς ἁγίοις αὐτοῦ,"),
                                                Reading("Gizeh2", None),
                                                Reading("Syncellus", None),
                                                Reading("Jude", u"ἐν ἁγίαις μυριάσιν αὐτοῦ,"),
                                                Reading("TestOne", None),
                                                Reading("TestTwo", u"ἐν ἁγίαις μυριάσιν αὐτοῦ,")]})],
                "error": [None, None]}
    assert result["result"][0] == expected["result"][0]
    assert result["result"][1] == expected["result"][1]
    assert result["error"] == expected["error"]


def test_bookman_get_group_as_gluon():
    result = BookManager.get_group([{"book": "test_parse", "version": "Greek", "unit_group": 14},
                                    {"book": "test_parse", "version": "Greek", "unit_group": 10}],
                                   as_gluon=True)
    expected = {"result": ['<dl>'
                           '<dt>7QEnoch</dt><dd>†</dd>'
                           '<dt>POxy2069</dt><dd>†</dd>'
                           '<dt>CB185</dt><dd>†</dd>'
                           '<dt>V1809</dt><dd>†</dd>'
                           '<dt>Gizeh</dt><dd>ὅτι ἔρχεται</dd>'
                           '<dt>Gizeh2</dt><dd>†</dd>'
                           '<dt>Syncellus</dt><dd>†</dd>'
                           '<dt>Jude</dt><dd>ἰδοὺ ἦλθεν κύριος</dd>'
                           '<dt>TestOne</dt><dd></dd>'
                           '<dt>TestTwo</dt><dd>†</dd>'

                           '<dt>7QEnoch</dt><dd>†</dd>'
                           '<dt>POxy2069</dt><dd>†</dd>'
                           '<dt>CB185</dt><dd>†</dd>'
                           '<dt>V1809</dt><dd>†</dd>'
                           '<dt>Gizeh</dt><dd>σὺν ταῖς μυριάσιν αὐτοῦ καὶ τοῖς ἁγίοις αὐτοῦ,</dd>'
                           '<dt>Gizeh2</dt><dd>†</dd>'
                           '<dt>Syncellus</dt><dd>†</dd>'
                           '<dt>Jude</dt><dd>ἐν ἁγίαις μυριάσιν αὐτοῦ,</dd>'
                           '<dt>TestOne</dt><dd>†</dd>'
                           '<dt>TestTwo</dt><dd>ἐν ἁγίαις μυριάσιν αὐτοῦ,</dd>'

                           '<dt>7QEnoch</dt><dd>†</dd>'
                           '<dt>POxy2069</dt><dd>†</dd>'
                           '<dt>CB185</dt><dd>†</dd>'
                           '<dt>V1809</dt><dd>†</dd>'
                           '<dt>Gizeh2</dt><dd>†</dd>'
                           '<dt>Syncellus</dt><dd>†</dd>'
                           '<dt>TestOne</dt><dd>†</dd>'
                           '<dt>TestTwo</dt><dd>†</dd>'
                           '<dt>Gizeh Jude</dt><dd>ποιῆσαι κρίσιν κατὰ πάντων, καὶ</dd>'
                           '</dl>',
                           '<dl>'
                           '<dt>7QEnoch</dt><dd>†</dd>'
                           '<dt>POxy2069</dt><dd>†</dd>'
                           '<dt>CB185</dt><dd>†</dd>'
                           '<dt>V1809</dt><dd>†</dd>'
                           '<dt>Gizeh</dt><dd>ὅτι ἔρχεται</dd>'
                           '<dt>Gizeh2</dt><dd>†</dd>'
                           '<dt>Syncellus</dt><dd>†</dd>'
                           '<dt>Jude</dt><dd>ἰδοὺ ἦλθεν κύριος</dd>'
                           '<dt>TestOne</dt><dd></dd>'
                           '<dt>TestTwo</dt><dd>†</dd>'

                           '<dt>7QEnoch</dt><dd>†</dd>'
                           '<dt>POxy2069</dt><dd>†</dd>'
                           '<dt>CB185</dt><dd>†</dd>'
                           '<dt>V1809</dt><dd>†</dd>'
                           '<dt>Gizeh</dt><dd>σὺν ταῖς μυριάσιν αὐτοῦ καὶ τοῖς ἁγίοις αὐτοῦ,</dd>'
                           '<dt>Gizeh2</dt><dd>†</dd>'
                           '<dt>Syncellus</dt><dd>†</dd>'
                           '<dt>Jude</dt><dd>ἐν ἁγίαις μυριάσιν αὐτοῦ,</dd>'
                           '<dt>TestOne</dt><dd>†</dd>'
                           '<dt>TestTwo</dt><dd>ἐν ἁγίαις μυριάσιν αὐτοῦ,</dd>'
                           '</dl>'],
                "error": [None, None]}
    assert str(result["result"][0]) == str(expected["result"][0])
    assert str(result["result"][1]) == str(expected["result"][1])
    assert result["error"] == expected["error"]


# Testing EI


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
    # with preceding
    new_book.add_div(version_title="MyVersion", div_name="MyDiv2", div_parent_path=None, preceding_div="MyDiv1")
    new_book.add_div(version_title="MyVersion", div_name="MyDiv1.1.2", div_parent_path=["MyDiv1", "MyDiv1.1"], preceding_div="MyDiv1.1.1")
    # with exceptions
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
    book_file_pattern = "{}_????????_??????_??????.xml"
    files_to_remove = []
    for xml_folder in [XML_DRAFT_FILE_BACKUP_STORAGE_PATH,
                       XML_FILE_BACKUP_STORAGE_PATH]:
        files_to_remove += glob.glob(os.path.join(xml_folder, book_file_pattern.format(book_name)))
    for xml_folder in [XML_DRAFT_FILE_STORAGE_PATH,
                       XML_FILE_STORAGE_PATH]:
        files_to_remove += glob.glob(os.path.join(xml_folder, "{}.xml".format(book_name)))
    for file_path in files_to_remove:
        os.remove(file_path)

    # create new
    BookManager.create_book(book_name, "My new book")
    assert os.path.isfile(os.path.join(XML_DRAFT_FILE_STORAGE_PATH, "{}.xml".format(book_name)))
    result_xml = fix_doctype(open(os.path.join(XML_DRAFT_FILE_STORAGE_PATH, "{}.xml".format(book_name))).read())
    expected_xml = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n" \
                   "<!DOCTYPE book SYSTEM 'grammateus.dtd'>\n" \
                   '<book filename="{}" title="My new book"/>\n'.format(book_name)
    assert result_xml == expected_xml

    # publish
    BookManager.publish_book(book_name)
    assert os.path.isfile(os.path.join(XML_FILE_STORAGE_PATH, "{}.xml".format(book_name)))
    result_xml = fix_doctype(open(os.path.join(XML_FILE_STORAGE_PATH, "{}.xml".format(book_name))).read())
    assert result_xml == expected_xml

    # copy as draft
    BookManager.copy_book(book_name)
    result_xml = fix_doctype(open(os.path.join(XML_DRAFT_FILE_STORAGE_PATH, "{}.xml".format(book_name))).read())
    assert result_xml == expected_xml
    assert len(glob.glob(os.path.join(XML_DRAFT_FILE_BACKUP_STORAGE_PATH, book_file_pattern.format(book_name)))) == 1

    # edit (add version)
    BookManager.add_version(book_name, "MyVersion", "MyLanguage", "Me")
    result_xml = fix_doctype(open(os.path.join(XML_DRAFT_FILE_STORAGE_PATH, "{}.xml".format(book_name))).read())
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
    assert len(glob.glob(os.path.join(XML_DRAFT_FILE_BACKUP_STORAGE_PATH, book_file_pattern.format(book_name)))) == 2

    # publish
    BookManager.publish_book(book_name)
    result_xml = fix_doctype(open(os.path.join(XML_FILE_STORAGE_PATH, "{}.xml".format(book_name))).read())
    assert result_xml == expected_xml
    assert len(glob.glob(os.path.join(XML_FILE_BACKUP_STORAGE_PATH, book_file_pattern.format(book_name)))) == 1

    # teardown
    files_to_remove = []
    for xml_folder in [XML_DRAFT_FILE_BACKUP_STORAGE_PATH,
                       XML_FILE_BACKUP_STORAGE_PATH]:
        files_to_remove += glob.glob(os.path.join(xml_folder, book_file_pattern.format(book_name)))
    for xml_folder in [XML_DRAFT_FILE_STORAGE_PATH,
                       XML_FILE_STORAGE_PATH]:
        files_to_remove += glob.glob(os.path.join(xml_folder, "{}.xml".format(book_name)))
    for file_path in files_to_remove:
        os.remove(file_path)

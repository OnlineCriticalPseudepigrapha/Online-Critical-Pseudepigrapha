#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
run tests from web2py root directory with:

    python3.6 -m pytest -xvvs applications/grammateus3/test/modules/
    test_dts_server.py
"""

import os
from plugin_utils import check_path

file_dir = os.path.join(os.path.dirname(__file__), os.pardir)
PROJECT_ROOT = os.path.join(file_dir, os.pardir)

XML_FILE_STORAGE_PATH = check_path(os.path.join(PROJECT_ROOT, "test", "docs"))
XML_FILE_BACKUP_STORAGE_PATH = check_path(os.path.join(PROJECT_ROOT, "test",
                                                       "docs", "backups"))
XML_DRAFT_FILE_STORAGE_PATH = check_path(os.path.join(PROJECT_ROOT, "test",
                                                      "docs", "drafts"))
XML_DRAFT_FILE_BACKUP_STORAGE_PATH = check_path(os.path.join(PROJECT_ROOT,
                                                             "test", "docs",
                                                             "drafts",
                                                             "backups"))

TEST_XML_FILE = check_path(os.path.join(PROJECT_ROOT, "test", "docs", "drafts",
                                        "test_parse.xml"))
TEST_DTD_FILE = check_path(os.path.join(PROJECT_ROOT, "static", "docs",
                                        "grammateus.dtd"))

def test_collections_response():
    assert None

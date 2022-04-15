#!/usr/bin/env python

"""Tests for `acdh_collatex_utils` package."""

import glob
import unittest

import lxml.etree as ET

from acdh_collatex_utils.post_process import (
    make_full_tei_doc,
    merge_tei_fragments,
)

FILES = glob.glob(
    "./fixtures/collated/*.tei",
    recursive=False
)

INPUT_FILE = "./fixtures/collated/tmp.xml"


class TestAcdh_collatex_utils(unittest.TestCase):
    """Tests for `acdh_collatex_utils` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_merge_tei_fragments(self):
        full_doc = merge_tei_fragments(FILES)
        self.assertEqual(
            "{http://www.tei-c.org/ns/1.0}ab", f"{full_doc.tag}"
        )

    def test_002_make_full_tei_doc(self):
        full_doc = merge_tei_fragments(FILES)
        with open(INPUT_FILE, 'w') as f:
            f.write(ET.tostring(full_doc, encoding='UTF-8').decode('utf-8'))
        full_tei = make_full_tei_doc(INPUT_FILE)
        root = full_tei.tree
        self.assertEqual(
            "{http://www.tei-c.org/ns/1.0}TEI", f"{root.tag}"
        )
        full_tei.tree_to_file(INPUT_FILE)

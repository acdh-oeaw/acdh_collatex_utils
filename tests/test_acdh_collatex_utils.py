#!/usr/bin/env python

"""Tests for `acdh_collatex_utils` package."""

import glob
import os
import shutil
import unittest
import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader

from acdh_collatex_utils.acdh_collatex_utils import (
    chunks_to_df,
    CxReader,
    CxCollate
)

from acdh_collatex_utils.post_process import (
    make_full_tei_doc,
    merge_tei_fragments,
    merge_html_fragments,
    define_readings,
    make_positive_app
)

GLOB_PATTERN = "./fixtures/*__*.xml"

FILES = glob.glob(
    GLOB_PATTERN,
    recursive=False
)
INPUT_FILE = "./fixtures/tmp/tmp.xml"
FINAL = "./fixtures/tmp/tmp_final.xml"
TMP_DIR = './fixtures/tmp'


class TestAcdh_collatex_utils(unittest.TestCase):
    """Tests for `acdh_collatex_utils` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_char_limit(self):
        """Test char_limit."""
        for x in FILES:
            doc = CxReader(xml=x, char_limit=True)
            doc_no_limit = CxReader(xml=x)
            self.assertTrue(doc.plaint_text_len <= 5000)
            self.assertTrue(doc_no_limit.plaint_text_len >= 5000)

    def test_002_clean_string(self):
        """Check if all tei:hi elments are properly removed"""
        for x in FILES:
            doc = CxReader(xml=x)
            CxReader(xml=x)
            self.assertFalse('<lb break' in f"{doc.preprocess()}")
            self.assertTrue('<lb' in f"{doc.preprocess()}")

    def test_003_chunks_to_df(self):
        df = chunks_to_df(FILES)
        self.assertTrue('id' in df.keys())

    def test_004_collate_chunks(self):
        CxCollate(glob_pattern=GLOB_PATTERN, output_dir='./fixtures').collate()
        new_htmls = glob.glob(
            "./fixtures/*.html",
            recursive=False
        )
        self.assertTrue(len(new_htmls) == 3)

    def test_004_merge_tei_fragments(self):
        COL_FILES = glob.glob(
            "./fixtures/*.tei",
            recursive=False
        )
        os.makedirs(TMP_DIR, exist_ok=True)
        full_doc = merge_tei_fragments(COL_FILES)
        self.assertEqual(
            "{http://www.tei-c.org/ns/1.0}ab", f"{full_doc.tag}"
        )
        with open(INPUT_FILE, 'w') as f:
            f.write(ET.tostring(full_doc, encoding='UTF-8').decode('utf-8'))

    def test_005_make_full_tei_doc(self):
        full_tei = make_full_tei_doc(INPUT_FILE)
        root = full_tei.tree
        self.assertEqual(
            "{http://www.tei-c.org/ns/1.0}TEI", f"{root.tag}"
        )
        full_tei.tree_to_file(FINAL)
        shutil.rmtree(TMP_DIR)

    def test_006_merge_htmls(self):
        files = glob.glob('./fixtures/*.html')
        merged = merge_html_fragments(files)
        tag_name = merged.table.name
        self.assertTrue(tag_name, 'table')
        OUT_FILES = glob.glob(
            "./fixtures/out__*.*",
            recursive=False
        )
        for x in OUT_FILES:
            os.remove(x)

    def test_007_rdg_to_lem(self):
        input_file = './fixtures/full_tei.xml'
        rdg_wit_id = 'sfe-1901-01__1925.xml'
        crit_ap_with_rdgs = define_readings(input_file, rdg_wit_id)
        self.assertIn("<app><lem wit", f"{crit_ap_with_rdgs}")

    def test_008_positiv_app(self):
        input_file = './fixtures/full_tei.xml'
        positive_doc = make_positive_app(input_file)
        first_app = positive_doc.any_xpath('.//tei:app')[0]
        rdgs = len(first_app.xpath('./*'))
        self.assertTrue(rdgs, 3)
        negative_doc = TeiReader(input_file)
        first_app = negative_doc.any_xpath('.//tei:app')[0]
        rdgs = len(first_app.xpath('./*'))
        self.assertTrue(rdgs, 2)

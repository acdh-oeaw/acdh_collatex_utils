#!/usr/bin/env python

"""Tests for `acdh_collatex_utils` package."""

import glob
import os
import unittest
from click.testing import CliRunner

from acdh_collatex_utils.acdh_collatex_utils import *
from acdh_collatex_utils import cli

FILES = glob.glob(
    "./fixtures/*.xml",
    recursive=False
)

HTMLS = glob.glob(
    "./fixtures/*.html",
    recursive=False
)


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
            doc_no_limit = CxReader(xml=x)
            self.assertFalse('<lb break' in f"{doc.preprocess()}")
            self.assertTrue('<lb' in f"{doc.preprocess()}")

    def test_003_chunks_to_df(self):
        df = chunks_to_df(FILES)
        self.assertTrue('id' in df.keys())

    def test_004_collate_chunks(self):
        if len(HTMLS) > 0:
            for x in HTMLS:
                os.remove(x)
        out = CxCollate(output_dir='./fixtures').collate()
        new_htmls = glob.glob(
            "./fixtures/*.html",
            recursive=False
        )
        self.assertTrue(len(new_htmls) == 3)

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'acdh_collatex_utils.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

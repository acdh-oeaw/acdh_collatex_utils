#!/usr/bin/env python

"""Tests for `acdh_collatex_utils` package."""

import os
import unittest

from acdh_collatex_utils.chunks import get_chunks
from acdh_collatex_utils.acdh_collatex_utils import CHUNK_SIZE

file = os.path.join('.', 'fixtures', 'lorem_ipsum.txt')

with open(file) as f:
    lorem_ipsum = f.read()


class TestAcdh_collatex_utils(unittest.TestCase):
    """Tests for `acdh_collatex_utils` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_file_loading(self):
        self.assertTrue(type(lorem_ipsum), 'list')

    def test_0002_chunk_text(self):
        """ test chunk function """
        chunker = get_chunks(lorem_ipsum, CHUNK_SIZE, 'some_id.txt')
        chunks = [x for x in chunker]
        self.assertTrue(
            type(chunks),
            'list'
        )
        self.assertTrue(
            type(chunks[0]),
            'dict'
        )

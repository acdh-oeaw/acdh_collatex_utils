#!/usr/bin/env python

"""Tests for `acdh_collatex_utils` package."""


import unittest
from click.testing import CliRunner

from acdh_collatex_utils import acdh_collatex_utils
from acdh_collatex_utils import cli


class TestAcdh_collatex_utils(unittest.TestCase):
    """Tests for `acdh_collatex_utils` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'acdh_collatex_utils.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

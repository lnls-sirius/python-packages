#!/usr/bin/env python-sirius

"""Unittest module for search package."""

from unittest import TestCase

from siriuspy import util
from siriuspy import search

public_interface = (
    'PSSearch',
    'MASearch',
    'BPMSearch',
    'HLTimeSearch',
    'LLTimeSearch',
    'IDSearch',
)


class TestSearch(TestCase):
    """Test Search module."""

    def test_public_interface(self):
        """Test module's public interface."""
        valid = util.check_public_interface_namespace(search, public_interface)
        self.assertTrue(valid)

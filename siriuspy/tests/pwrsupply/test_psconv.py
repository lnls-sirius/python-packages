#!/usr/bin/env python-sirius
"""Test public API of PowerSupply/Magnet class."""

from unittest import TestCase

from siriuspy.pwrsupply import psconv
from siriuspy.util import check_public_interface_namespace


PUBLIC_INTERFACE = (
    'PSEpicsConn',
    'PUEpicsConn',
    'SConvEpics'
)


class TestModule(TestCase):
    """Test Module."""

    def test_public_interface(self):
        """Test module's public interface."""
        valid = check_public_interface_namespace(psconv, PUBLIC_INTERFACE)
        self.assertTrue(valid)
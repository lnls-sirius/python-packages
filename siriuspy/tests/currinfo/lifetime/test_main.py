#!/usr/bin/env python-sirius

"""Module to test CurrInfo Lifetime Soft IOC main module."""

import unittest
from unittest import mock
import siriuspy.util as util
from siriuspy.currinfo import SILifetimeApp


PUB_INTERFACE = (
    'pvs_database',
    'init_database',
    'process',
    'read',
    'write',
)


class TestASAPCurrInfoLifetimeMain(unittest.TestCase):
    """Test AS-AP-CurrInfo Lifetime Soft IOC."""

    def setUp(self):
        pv_patcher = mock.patch(
            "siriuspy.currinfo.lifetime.main._PV", autospec=True)
        self.addCleanup(pv_patcher.stop)
        self.mock_pv = pv_patcher.start()
        self.mock_pv.return_value.connected = False
        self.app = SILifetimeApp()

    def test_public_interface(self):
        """Test module's public interface."""
        valid = util.check_public_interface_namespace(
            SILifetimeApp, PUB_INTERFACE, print_flag=True)
        self.assertTrue(valid)

    def test_write_MinIntvlBtwSpl(self):
        """Test write MinIntvlBtwSmpl-SP."""
        self.app.write('MinIntvlBtwSpl-SP', -1)
        self.assertEqual(self.app._min_intvl_btw_spl, 0)

        self.app.write('MinIntvlBtwSpl-SP', 0)
        self.assertEqual(self.app._min_intvl_btw_spl, 0)

        self.app.write('MinIntvlBtwSpl-SP', 1)
        self.assertEqual(self.app._min_intvl_btw_spl, 1)

    def test_write_SplIntvl(self):
        """Test write MaxSplIntvl-SP."""
        self.app.write('MaxSplIntvl-SP', 100)
        self.assertEqual(self.app._sampling_interval, 100)

    def test_write_LtFitMode(self):
        """Test write LtFitMode-Sel."""
        self.app.write('LtFitMode-Sel', 1)
        self.assertEqual(self.app._mode, 1)

    def test_write_CurrOffset(self):
        """Test write CurrOffset-SP."""
        self.app.write('CurrOffset-SP', 1)
        self.assertEqual(self.app._current_offset, 1)


if __name__ == "__main__":
    unittest.main()

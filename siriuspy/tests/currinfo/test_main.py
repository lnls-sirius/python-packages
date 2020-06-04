#!/usr/bin/env python-sirius

"""Module to test AS-AP-CurrInfo Current Soft IOC main module."""

import unittest
from unittest import mock
import siriuspy.util as util
from siriuspy.currinfo.csdev import Const
from siriuspy.currinfo import SICurrInfoApp
from siriuspy.currinfo.main import _CurrInfoApp


PUB_INTERFACE_BASE = (
    'pvs_database',
    'init_database',
    'process',
    'read',
    'write',
    'close',
)

PUB_INTERFACE_SI = (
    'HARMNUM_RATIO',
    'CURR_THRESHOLD',
    'init_database',
    'read',
    'write',
)


class TestASAPCurrInfoCurrentMain(unittest.TestCase):
    """Test AS-AP-CurrInfo Soft IOC."""

    def setUp(self):
        """Set Up tests."""
        ca_patcher = mock.patch(
            "siriuspy.currinfo.main._ClientArch", autospec=True)
        self.addCleanup(ca_patcher.stop)
        self.mock_ca = ca_patcher.start()
        self.mock_ca.return_value.getData.return_value = None
        pv_patcher = mock.patch(
            "siriuspy.currinfo.main._PV", autospec=True)
        self.addCleanup(pv_patcher.stop)
        self.mock_pv = pv_patcher.start()
        self.mock_pv.return_value.connected = False
        self.app = SICurrInfoApp()

    def test_public_interface(self):
        """Test module's public interface."""
        valid = util.check_public_interface_namespace(
            _CurrInfoApp, PUB_INTERFACE_BASE, print_flag=True)
        self.assertTrue(valid)
        valid = util.check_public_interface_namespace(
            SICurrInfoApp, PUB_INTERFACE_SI, print_flag=True)
        self.assertTrue(valid)

    def test_write_DCCTFltCheck(self):
        """Test write DCCTFltCheck-Sel."""
        self.app.write('DCCTFltCheck-Sel', Const.DCCTFltCheck.On)
        self.assertEqual(self.app._dcctfltcheck_mode, Const.DCCTFltCheck.On)

    def test_write_DCCT_FltCheckOn(self):
        """Test write DCCT-Sel."""
        self.app._dcctfltcheck_mode = Const.DCCTFltCheck.On
        init_status = self.app._dcct_mode
        self.app.write('DCCT-Sel', Const.DCCT.Avg)
        self.app.write('DCCT-Sel', Const.DCCT.DCCT13C4)
        self.app.write('DCCT-Sel', Const.DCCT.DCCT14C4)
        end_status = self.app._dcct_mode
        self.assertEqual(init_status, end_status)

    def test_write_DCCT_FltCheckOff(self):
        """Test write DCCT-Sel."""
        self.app.write('DCCTFltCheck-Sel', Const.DCCTFltCheck.Off)
        self.app.write('DCCT-Sel', Const.DCCT.DCCT13C4)
        self.assertEqual(self.app._dcct_mode, Const.DCCT.DCCT13C4)


if __name__ == "__main__":
    unittest.main()

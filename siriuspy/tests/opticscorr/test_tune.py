#!/usr/bin/env python-sirius

"""Module to test AS-AP-TuneCorr Soft IOC main module."""

import unittest
from unittest import mock
import siriuspy.util as util
from siriuspy.opticscorr.csdev import Const
from siriuspy.opticscorr.tune import TuneCorrApp


PUB_INTERFACE = (
    'update_corrparams_pvs',
    'set_dtune_x',
    'set_dtune_y',
    'cmd_set_newref',
    'set_meas_config_dkl_qf',
    'set_meas_config_dkl_qd',
)


class TestASAPTuneCorrMain(unittest.TestCase):
    """Test AS-AP-TuneCorr Soft IOC."""

    def setUp(self):
        """Initialize Soft IOC."""
        self.q_ok = {
            'matrix': [
                [2.7280, 8.5894, 4.2995, 0.5377,
                 1.0906, 2.0004, 0.5460, 1.0012],
                [-1.3651, -3.5532, -1.7657, -2.3652,
                 -4.7518, -1.9781, -2.3601, -0.9839]],
            'nominal KLs': [0.7146, 1.2344, 1.2344, -0.2270,
                            -0.2809, -0.4783, -0.2809, -0.4783]}
        self.qfams = ['QFA', 'QFB', 'QFP',
                      'QDA', 'QDB1', 'QDB2', 'QDP1', 'QDP2']
        cs_patcher = mock.patch(
            "siriuspy.opticscorr.base._ConfigDBClient", autospec=True)
        self.addCleanup(cs_patcher.stop)
        self.mock_cs = cs_patcher.start()
        self.mock_cs.return_value.get_config_value.return_value = self.q_ok
        pv_patcher = mock.patch(
            "siriuspy.opticscorr.base._PV", autospec=True)
        self.addCleanup(pv_patcher.stop)
        self.mock_pv = pv_patcher.start()
        cnh_patcher = mock.patch(
            "siriuspy.opticscorr.base._HandleConfigNameFile",
            autospec=True)
        self.addCleanup(cnh_patcher.stop)
        self.mock_cnh = cnh_patcher.start()
        self.mock_cnh.return_value.get_config_name.return_value = \
            'SI.V24.04_S05.01'
        self.app = TuneCorrApp('SI')

    def test_public_interface(self):
        """Test module's public interface."""
        valid = util.check_public_interface_namespace(
            TuneCorrApp, PUB_INTERFACE, print_flag=True)
        self.assertTrue(valid)

    def test_write_ok_syncoff_Apply(self):
        """Test write on ApplyDelta-Cmd in normal operation, sync off."""
        self.app._sync_corr = Const.SyncCorr.Off

        self.app._status = 0b00000
        self.assertFalse(self.app.write('ApplyDelta-Cmd', 0))
        count = self.mock_pv.return_value.put.call_count
        self.assertEqual(count, len(self.qfams))

        self.app._status = 0b10000
        self.assertFalse(self.app.write('ApplyDelta-Cmd', 0))
        count = self.mock_pv.return_value.put.call_count
        self.assertEqual(count, 2*len(self.qfams))

    def test_write_ok_syncon_Apply(self):
        """Test write on ApplyDelta-Cmd in normal operation, sync on."""
        self.app._sync_corr = Const.SyncCorr.On
        self.app._status = 0b00000
        self.assertFalse(self.app.write('ApplyDelta-Cmd', 0))
        count = self.mock_pv.return_value.put.call_count
        self.assertEqual(count, 1+len(self.qfams))

    def test_write_err_syncon_Apply(self):
        """Test write on ApplyDelta-Cmd on status error."""
        self.app._sync_corr = Const.SyncCorr.On
        self.app._status = 0b10000
        self.assertFalse(self.app.write('ApplyDelta-Cmd', 0))
        self.mock_pv.return_value.put.assert_not_called()

    def test_write_CorrMeth(self):
        """Test write on CorrMeth-Sel."""
        self.assertTrue(self.app.write('CorrMeth-Sel', 1))
        self.assertEqual(self.app._corr_method, 1)

    def test_write_SyncCorr(self):
        """Test write on SyncCorr-Sel."""
        self.mock_pv.return_value.connected = True
        self.assertTrue(self.app.write('SyncCorr-Sel', 1))
        self.assertEqual(self.app._sync_corr, 1)

    def test_write_ok_ConfigPS(self):
        """Test write on ConfigPS-Cmd in normal operation."""
        self.mock_pv.return_value.connected = True
        self.assertFalse(self.app.write('ConfigPS-Cmd', 0))
        count = self.mock_pv.return_value.put.call_count
        self.assertEqual(count, 2*len(self.qfams))

    def test_write_err_ConfigPS(self):
        """Test write on ConfigPS-Cmd on connection error."""
        self.mock_pv.return_value.connected = False
        self.assertFalse(self.app.write('ConfigPS-Cmd', 0))
        self.mock_pv.return_value.put.assert_not_called()

    def test_write_ok_ConfigTI(self):
        """Test write on ConfigTiming-Cmd in normal operation."""
        self.mock_pv.return_value.connected = True
        self.assertFalse(self.app.write('ConfigTiming-Cmd', 0))
        count = self.mock_pv.return_value.put.call_count
        self.assertEqual(count, 9)

    def test_write_err_ConfigTI(self):
        """Test write on ConfigTiming-Cmd in connection error."""
        self.mock_pv.return_value.connected = False
        self.assertFalse(self.app.write('ConfigTiming-Cmd', 0))
        self.mock_pv.return_value.put.assert_not_called()

    def test_write_ok_SetNewRefKL(self):
        """Test write on SetNewRefKL-Cmd in normal operation."""
        self.mock_pv.return_value.get.return_value = 0.0
        self.app._status = 0
        self.assertFalse(self.app.write('SetNewRefKL-Cmd', 0))
        self.assertEqual(self.app._delta_tunex, 0)
        self.assertEqual(self.app._delta_tuney, 0)
        for fam in self.qfams:
            self.assertEqual(self.app._lastcalc_deltakl[fam], 0)

    def test_write_err_SetNewRefKL(self):
        """Test write on SetNewRefKL-Cmd on connection error."""
        self.app._status = 0b00001
        self.assertFalse(self.app.write('SetNewRefKL-Cmd', 0))
        self.mock_pv.return_value.get.assert_not_called()


if __name__ == "__main__":
    unittest.main()

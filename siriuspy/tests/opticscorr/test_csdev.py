#!/usr/bin/env python-sirius

"""Unittest module for opticscorr.py."""

from unittest import TestCase
from siriuspy import util
from siriuspy.opticscorr import csdev
from siriuspy.opticscorr.csdev import \
    get_chrom_database, \
    get_tune_database


PUB_INTERFACE = (
        'ETypes',
        'Const',
        'get_chrom_database',
        'get_tune_database',
    )


class TestOpticsCorrCSDevice(TestCase):
    """Test siriuspy.opticscorr.csdev module."""

    def test_public_interface(self):
        """Test module's public interface."""
        valid = util.check_public_interface_namespace(csdev, PUB_INTERFACE)
        self.assertTrue(valid)

    def test_get_chrom_database(self):
        """Test get_chrom_database."""
        for accelerator in ('SI', 'BO'):
            if accelerator == 'SI':
                sfams = ('SFA1', 'SFA2', 'SDA1', 'SDA2', 'SDA3',
                         'SFB1', 'SFB2', 'SDB1', 'SDB2', 'SDB3',
                         'SFP1', 'SFP2', 'SDP1', 'SDP2', 'SDP3')
            elif accelerator == 'BO':
                sfams = ('SF', 'SD')
            dbase = get_chrom_database(accelerator)
            self.assertIsInstance(dbase, dict)
            self.assertTrue('Version-Cte' in dbase)
            self.assertTrue('Log-Mon' in dbase)
            self.assertTrue('ChromX-SP' in dbase)
            self.assertTrue('ChromX-RB' in dbase)
            self.assertTrue('ChromY-SP' in dbase)
            self.assertTrue('ChromY-RB' in dbase)
            self.assertTrue('DeltaChromX-SP' in dbase)
            self.assertTrue('DeltaChromX-RB' in dbase)
            self.assertTrue('DeltaChromY-SP' in dbase)
            self.assertTrue('DeltaChromY-RB' in dbase)
            self.assertTrue('ChromY-Mon' in dbase)
            self.assertTrue('ChromY-Mon' in dbase)
            self.assertTrue('CalcChromX-Mon' in dbase)
            self.assertTrue('CalcChromY-Mon' in dbase)
            self.assertTrue('ApplyDelta-Cmd' in dbase)
            self.assertTrue('ConfigName-SP' in dbase)
            self.assertTrue('ConfigName-RB' in dbase)
            self.assertTrue('RespMat-Mon' in dbase)
            self.assertTrue('NominalChrom-Mon' in dbase)
            self.assertTrue('NominalSL-Mon' in dbase)
            self.assertTrue('ConfigPS-Cmd' in dbase)
            self.assertTrue('Status-Mon' in dbase)
            self.assertTrue('StatusLabels-Cte' in dbase)

            for fam in sfams:
                self.assertTrue('SL' + fam + '-Mon' in dbase)
                self.assertEqual(dbase['SL' + fam + '-Mon']['unit'], '1/m^2')
            if accelerator == 'SI':
                self.assertTrue('CorrMeth-Sel' in dbase)
                self.assertTrue('CorrMeth-Sts' in dbase)
                # self.assertTrue('SyncCorr-Sel' in dbase)
                # self.assertTrue('SyncCorr-Sts' in dbase)
                # self.assertTrue('ConfigTiming-Cmd' in dbase)

    def test_get_tune_database(self):
        """Test get_tune_database."""
        for accelerator in ('SI', 'BO'):
            if accelerator == 'SI':
                qfams = ('QFA', 'QFB', 'QFP',
                         'QDA', 'QDB1', 'QDB2', 'QDP1', 'QDP2')
            elif accelerator == 'BO':
                qfams = ('QF', 'QD')
            dbase = get_tune_database(accelerator)
            self.assertIsInstance(dbase, dict)
            self.assertTrue('Version-Cte' in dbase)
            self.assertTrue('Log-Mon' in dbase)
            self.assertTrue('DeltaTuneX-SP' in dbase)
            self.assertTrue('DeltaTuneX-RB' in dbase)
            self.assertTrue('DeltaTuneY-SP' in dbase)
            self.assertTrue('DeltaTuneY-RB' in dbase)
            self.assertTrue('ApplyDelta-Cmd' in dbase)
            self.assertTrue('RespMat-Mon' in dbase)
            self.assertTrue('NominalKL-Mon' in dbase)
            self.assertTrue('ConfigPS-Cmd' in dbase)
            self.assertTrue('Status-Mon' in dbase)
            self.assertTrue('StatusLabels-Cte' in dbase)

            for fam in qfams:
                self.assertTrue('RefKL'+fam+'-Mon' in dbase)
                self.assertEqual(dbase['RefKL'+fam+'-Mon']['unit'], '1/m')
                self.assertTrue('DeltaKL'+fam+'-Mon' in dbase)
                self.assertEqual(dbase['DeltaKL'+fam+'-Mon']['unit'], '1/m')
            if accelerator == 'SI':
                self.assertTrue('CorrMeth-Sel' in dbase)
                self.assertTrue('CorrMeth-Sts' in dbase)
                self.assertTrue('SyncCorr-Sel' in dbase)
                self.assertTrue('SyncCorr-Sts' in dbase)
                self.assertTrue('ConfigTiming-Cmd' in dbase)

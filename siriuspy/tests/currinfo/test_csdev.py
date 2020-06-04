#!/usr/bin/env python-sirius

"""Unittest module for currinfo.py."""

from unittest import TestCase
from siriuspy import util
from siriuspy.currinfo import csdev
from siriuspy.currinfo.csdev import \
    get_currinfo_database, \
    get_lifetime_database

PUB_INTERFACE = (
        'ETypes',
        'Const',
        'get_currinfo_database',
        'get_litbts_currinfo_database',
        'get_bo_currinfo_database',
        'get_si_currinfo_database',
        'get_lifetime_database'
    )


class TestCurrInfoCSDevice(TestCase):
    """Test siriuspy.currinfo.csdev module."""

    def test_public_interface(self):
        """Test module's public interface."""
        valid = util.check_public_interface_namespace(csdev, PUB_INTERFACE)
        self.assertTrue(valid)

    def test_get_currinfo_database(self):
        """Test get_currinfo_database."""

        # ---- SI ----
        dbase = get_currinfo_database('SI')
        self.assertIsInstance(dbase, dict)

        # PV names
        self.assertTrue('Version-Cte' in dbase)
        self.assertTrue('Current-Mon' in dbase)
        self.assertTrue('StoredEBeam-Mon' in dbase)
        self.assertTrue('DCCT-Sel' in dbase)
        self.assertTrue('DCCT-Sts' in dbase)
        self.assertTrue('DCCTFltCheck-Sel' in dbase)
        self.assertTrue('DCCTFltCheck-Sts' in dbase)
        self.assertTrue('Charge-Mon' in dbase)

        # PVs units
        self.assertEqual(dbase['Current-Mon']['unit'], 'mA')
        self.assertEqual(dbase['Charge-Mon']['unit'], 'A.h')

        # ---- BO ----
        dbase = get_currinfo_database('BO')
        self.assertIsInstance(dbase, dict)

        # PV names
        self.assertTrue('RawReadings-Mon' in dbase)
        self.assertTrue('Current150MeV-Mon' in dbase)
        self.assertTrue('Current1GeV-Mon' in dbase)
        self.assertTrue('Current2GeV-Mon' in dbase)
        self.assertTrue('Current3GeV-Mon' in dbase)
        self.assertTrue('Charge150MeV-Mon' in dbase)
        self.assertTrue('Charge1GeV-Mon' in dbase)
        self.assertTrue('Charge2GeV-Mon' in dbase)
        self.assertTrue('Charge3GeV-Mon' in dbase)
        self.assertTrue('RampEff-Mon' in dbase)

        # PVs units
        self.assertEqual(dbase['RawReadings-Mon']['unit'], 'mA')
        self.assertEqual(dbase['Current150MeV-Mon']['unit'], 'mA')
        self.assertEqual(dbase['Current1GeV-Mon']['unit'], 'mA')
        self.assertEqual(dbase['Current2GeV-Mon']['unit'], 'mA')
        self.assertEqual(dbase['Current3GeV-Mon']['unit'], 'mA')
        self.assertEqual(dbase['Charge150MeV-Mon']['unit'], 'nC')
        self.assertEqual(dbase['Charge1GeV-Mon']['unit'], 'nC')
        self.assertEqual(dbase['Charge2GeV-Mon']['unit'], 'nC')
        self.assertEqual(dbase['Charge3GeV-Mon']['unit'], 'nC')
        self.assertEqual(dbase['RampEff-Mon']['unit'], '%')

    def test_get_lifetime_database(self):
        """Test get_lifetime_database."""
        dbase = get_lifetime_database()
        self.assertIsInstance(dbase, dict)

        # PV names
        self.assertTrue('VersionLifetime-Cte' in dbase)
        self.assertTrue('LtFitMode-Sel' in dbase)
        self.assertTrue('LtFitMode-Sts' in dbase)
        self.assertTrue('MaxSplIntvl-SP' in dbase)
        self.assertTrue('MaxSplIntvl-RB' in dbase)
        self.assertTrue('SplIntvl-Mon' in dbase)
        self.assertTrue('SplIntvlBPM-Mon' in dbase)
        self.assertTrue('MinIntvlBtwSpl-SP' in dbase)
        self.assertTrue('MinIntvlBtwSpl-RB' in dbase)
        self.assertTrue('CurrOffset-SP' in dbase)
        self.assertTrue('CurrOffset-RB' in dbase)
        self.assertTrue('BuffRst-Cmd' in dbase)
        self.assertTrue('BuffAutoRst-Sel' in dbase)
        self.assertTrue('BuffAutoRst-Sts' in dbase)
        self.assertTrue('BuffAutoRstDCurr-SP' in dbase)
        self.assertTrue('BuffAutoRstDCurr-RB' in dbase)
        self.assertTrue('FrstSplTime-SP' in dbase)
        self.assertTrue('FrstSplTime-RB' in dbase)
        self.assertTrue('LastSplTime-SP' in dbase)
        self.assertTrue('LastSplTime-RB' in dbase)
        self.assertTrue('FrstSplTimeBPM-RB' in dbase)
        self.assertTrue('LastSplTimeBPM-RB' in dbase)
        self.assertTrue('Lifetime-Mon' in dbase)
        self.assertTrue('BuffSize-Mon' in dbase)
        self.assertTrue('BuffSizeTot-Mon' in dbase)
        self.assertTrue('BufferValue-Mon' in dbase)
        self.assertTrue('BufferTimestamp-Mon' in dbase)
        self.assertTrue('LifetimeBPM-Mon' in dbase)
        self.assertTrue('BuffSizeBPM-Mon' in dbase)
        self.assertTrue('BuffSizeTotBPM-Mon' in dbase)
        self.assertTrue('BufferValueBPM-Mon' in dbase)
        self.assertTrue('BufferTimestampBPM-Mon' in dbase)

        # PVs units
        self.assertEqual(dbase['MaxSplIntvl-SP']['unit'], 's')
        self.assertEqual(dbase['MaxSplIntvl-RB']['unit'], 's')
        self.assertEqual(dbase['SplIntvl-Mon']['unit'], 's')
        self.assertEqual(dbase['SplIntvlBPM-Mon']['unit'], 's')
        self.assertEqual(dbase['MinIntvlBtwSpl-SP']['unit'], 's')
        self.assertEqual(dbase['MinIntvlBtwSpl-RB']['unit'], 's')
        self.assertEqual(dbase['CurrOffset-SP']['unit'], 'mA')
        self.assertEqual(dbase['CurrOffset-RB']['unit'], 'mA')
        self.assertEqual(dbase['BuffAutoRstDCurr-SP']['unit'], 'mA')
        self.assertEqual(dbase['BuffAutoRstDCurr-RB']['unit'], 'mA')
        self.assertEqual(dbase['FrstSplTime-SP']['unit'], 's')
        self.assertEqual(dbase['FrstSplTime-RB']['unit'], 's')
        self.assertEqual(dbase['LastSplTime-SP']['unit'], 's')
        self.assertEqual(dbase['LastSplTime-RB']['unit'], 's')
        self.assertEqual(dbase['FrstSplTimeBPM-RB']['unit'], 's')
        self.assertEqual(dbase['LastSplTimeBPM-RB']['unit'], 's')
        self.assertEqual(dbase['Lifetime-Mon']['unit'], 's')
        self.assertEqual(dbase['LifetimeBPM-Mon']['unit'], 's')

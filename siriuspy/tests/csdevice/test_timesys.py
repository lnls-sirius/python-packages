#!/usr/bin/env python-sirius

"""Unittest module for ll_database.py."""

import unittest
# import re
# from unittest import mock

from siriuspy import util
from siriuspy.csdevice import timesys

mock_flag = True

public_interface = (
    'get_otp_database',
    'get_out_database',
    'get_afc_out_database',
    'get_evr_database',
    'get_eve_database',
    'get_afc_database',
    'get_fout_database',
    'get_event_database',
    'get_clock_database',
    'get_evg_database',
    'events_hl2ll_map',
    'events_ll2hl_map',
    'events_ll_tmp',
    'events_hl_pref',
    'events_ll_codes',
    'events_ll_names',
    'events_modes',
    'events_delay_types',
    'clocks_states',
    'clocks_ll_tmp',
    'clocks_hl_tmp',
    'clocks_hl_pref',
    'clocks_hl2ll_map',
    'clocks_ll2hl_map',
    'triggers_states',
    'triggers_intlk',
    'triggers_polarities',
    'triggers_delay_types',
    'triggers_src_ll',
)


class TestModule(unittest.TestCase):
    """Test module interface."""

    def test_public_interface(self):
        """Test module's public interface."""
        valid = util.check_public_interface_namespace(
                timesys,
                public_interface)
        self.assertTrue(valid)

    def test_get_otp_database(self):
        """Test get_otp_database."""
        # TODO: implement test!
        pass

    def test_get_out_database(self):
        """Test get_out_database."""
        # TODO: implement test!
        pass

    def test_get_afc_out_database(self):
        """Test get_afc_out_database."""
        # TODO: implement test!
        pass

    def test_get_evr_database(self):
        """Test get_evr_database."""
        # TODO: implement test!
        pass

    def test_get_eve_database(self):
        """Test get_eve_database."""
        # TODO: implement test!
        pass

    def test_get_afc_database(self):
        """Test get_afc_database."""
        # TODO: implement test!
        pass

    def test_get_fout_database(self):
        """Test get_fout_database."""
        # TODO: implement test!
        pass

    def test_get_event_database(self):
        """Test get_event_database."""
        # TODO: implement test!
        pass

    def test_get_clock_database(self):
        """Test get_clock_database."""
        # TODO: implement test!
        pass

    def test_get_evg_database(self):
        """Test get_evg_database."""
        # TODO: implement test!
        pass

    def test_events_hl2ll_map(self):
        """Test HL2LL_MAP."""
        # TODO: implement test!
        pass

    def test_events_ll2hl_map(self):
        """Test LL2HL_MAP."""
        # TODO: implement test!
        pass

    def test_events_ll_tmp(self):
        """Test LL_TMP."""
        # TODO: implement test!
        pass

    def test_events_hl_pref(self):
        """Test HL_PREF."""
        # TODO: implement test!
        pass

    def test_events_ll_codes(self):
        """Test LL_CODES."""
        # TODO: implement test!
        pass

    def test_events_ll_names(self):
        """Test LL_EVENTS."""
        # TODO: implement test!
        pass

    def test_events_modes(self):
        """Test MODES."""
        # TODO: implement test!
        pass

    def test_events_delay_types(self):
        """Test DELAY_TYPES."""
        # TODO: implement test!
        pass

    def test_clocks_states(self):
        """Test STATES."""
        # TODO: implement test!
        pass

    def test_clocks_ll_tmp(self):
        """Test LL_TMP."""
        # TODO: implement test!
        pass

    def test_clocks_hl_tmp(self):
        """Test HL_TMP."""
        # TODO: implement test!
        pass

    def test_clocks_hl_pref(self):
        """Test HL_PREF."""
        # TODO: implement test!
        pass

    def test_clocks_hl2ll_map(self):
        """Test HL2LL_MAP."""
        # TODO: implement test!
        pass

    def test_clocks_ll2hl_map(self):
            """Test LL2HL_MAP."""
            # TODO: implement test!
            pass

    def test_triggers_states(self):
        """Test STATES."""
        # TODO: implement test!
        pass

    def test_triggers_intlk(self):
        """Test INTLK."""
        # TODO: implement test!
        pass

    def test_triggers_polarities(self):
        """Test POLARITIES."""
        # TODO: implement test!
        pass

    def test_triggers_delay_types(self):
        """Test DELAY_TYPES."""
        # TODO: implement test!
        pass

    def test_triggers_src_ll(self):
        """Test SRC_LL."""
        # TODO: implement test!
        pass


if __name__ == "__main__":
    unittest.main()

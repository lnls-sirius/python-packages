"""PVs Configs Handler."""

import time as _time
import struct as _struct
import numpy as _np
from epics import get_pv as _get_pv

from . import ConfigDBDocument as _ConfigDBDocument


_TIMEOUT = 0.5


class PVsConfig(_ConfigDBDocument):
    """Class to handle PVs configurations."""

    PVs = dict()

    def __init__(self, config_type='global_config', name=None, url=None):
        """Init."""
        super().__init__(config_type, name=name, url=url)

    def connect(self):
        """Create PVs."""
        template = self.get_value_from_template()
        for pvn, _, _ in template['pvs']:
            self._get_pv(pvn)

    @property
    def connected(self):
        """."""
        template = self.get_value_from_template()
        for pvn, _, _ in template['pvs']:
            pvobj = self.PVs.get(pvn)
            if pvobj is None:
                return False
            elif not pvobj.connected:
                return False
        return True

    @property
    def pvs(self):
        """Return dict with PVs and values."""
        self.load()
        pvslist = self._value['pvs']
        pvsdict = {item[0]: item[1] for item in pvslist}
        return pvsdict

    def read(self, timeout=_TIMEOUT):
        """Read machine state."""
        new_config_value = dict()
        new_config_value['pvs'] = list()

        template = self.get_value_from_template()

        # connect
        self.connect()

        # read
        pvs_not_read = set()
        for pvn, defval, delay in template['pvs']:
            pvobj = self._get_pv(pvn)
            if pvobj.wait_for_connection(timeout):
                value = defval if pvn.endswith('-Cmd')\
                    else pvobj.get(timeout=timeout)
            else:
                pvs_not_read.add(pvn)
                value = 0
            new_config_value['pvs'].append([pvn, value, delay])

        if pvs_not_read:
            return False, pvs_not_read

        self.value = new_config_value
        return True, []

    def read_and_save(self, new_name=None):
        """Read machine state and save new configuration in config server."""
        status_ok, failed_list = self.read()
        if not status_ok:
            return False, failed_list
        self.save(new_name)
        return True, []

    def apply(self, timeout=_TIMEOUT):
        """Apply current config value to machine and check if implemented."""
        # connect
        self.connect()

        pvs_not_set = set()

        # set
        for pvn, value, delay in self._value['pvs']:
            pvobj = self._get_pv(pvn)
            try:
                pvobj.put(value)
                _time.sleep(delay)
            except TypeError:
                pvs_not_set.add(pvn)

        # wait
        _time.sleep(2.0)

        # check
        for pvn, value, delay in self._value['pvs']:
            if pvn in pvs_not_set:
                continue
            equal = self._check_pv(pvn, value, timeout=timeout)
            if not equal:
                pvs_not_set.add(pvn)

        if pvs_not_set:
            return False, pvs_not_set
        return True, []

    def load_and_apply(self, timeout=_TIMEOUT):
        """Load from server, apply to machine and check if implemented."""
        self.load()
        status_ok, failed_list = self.apply(timeout=timeout)
        if not status_ok:
            return False, failed_list
        return True, []

    # ---------- private methods ----------

    def _get_pv(self, pvname, timeout=_TIMEOUT):
        """Return PV object."""
        pvobj = self.PVs.get(pvname)
        if pvobj is None:
            pvobj = _get_pv(pvname, timeout=timeout)
            self.PVs[pvname] = pvobj
        return pvobj

    def _check_pv(self, pvname, value, timeout=_TIMEOUT):
        """Check PV value."""
        # NOTE: Is the function 'isclose' being used solely because
        # somes IOCs operate on single-precision floats? If this is
        # the case maybe we shoud convert float64 to float32 and
        # do a precise comparison.
        pvobj = self._get_pv(pvname)
        pvobj.wait_for_connection(timeout)
        curr_val = pvobj.get(timeout=timeout)
        if curr_val is None:
            return False
        elif isinstance(curr_val, (_np.ndarray, list, tuple)) or \
                isinstance(value, (_np.ndarray, list, tuple)):
            try:
                if len(curr_val) != len(value):
                    return False
            except TypeError:
                return False  # one of them is not an array
            if isinstance(curr_val[0], (float, _np.float64)):
                curr_val = _np.asarray(curr_val, dtype=_np.float32)
            if isinstance(value[0], (float, _np.float64)):
                value = _np.asarray(curr_val, dtype=_np.float32)
            # NOTE: benchmark
            #
            # size         isclose          array_equal
            #        (asarray_implicit) (asarray_explicit)
            #
            # 4            24.4 us            5.2 us
            # 4000         36.5 us            6.6 us
            return _np.array_equal(curr_val, value)
        elif isinstance(curr_val, float) or isinstance(value, float):
            # NOTE: benchmark
            #        isclose            struct.pack
            #        ~265 ns              ~170 ns
            return _struct.pack('f', curr_val) == _struct.pack('f', value)
        elif curr_val == value:
            return True
        return False

"""Definition module."""
import math as _math
import logging as _log
import numpy as _np

from ..callbacks import Callback as _Callback

from .csdev import SOFBFactory as _SOFBFactory, ConstTLines as _ConstTLines

_CSACCELS = {}


def _create_csorb(acc):
    csorb = _CSACCELS.get(acc)
    if csorb is None:
        csorb = _SOFBFactory.create(acc)
        _CSACCELS[acc] = csorb
    return csorb


class BaseClass(_Callback):
    """Base Class."""

    def __init__(self, acc, prefix='', callback=None):
        """Init method."""
        super().__init__(callback)
        self._csorb = _create_csorb(acc)
        self._prefix = prefix
        self._status = 0b0
        self._map2write = self.get_map2write()

    @property
    def prefix(self):
        """Prefix."""
        return self._prefix

    @property
    def acc(self):
        """Accelerator name."""
        return self._csorb.acc

    @property
    def acc_idx(self):
        """Accelerator index."""
        return self._csorb.acc_idx

    @property
    def isring(self):
        """Ring accelerator status."""
        return self._csorb.isring

    @property
    def status(self):
        """Status."""
        self._update_status()
        return self._status

    @property
    def csorb(self):
        """CSDevice SOFB definition."""
        return self._csorb

    def write(self, pvname, value):
        """."""
        pvname = pvname.replace(self.prefix, '')
        if isinstance(value, (_np.ndarray, list, tuple)):
            pval = f'{value[0]}...{value[-1]}'
        else:
            pval = f'{value}'
        _log.info(f'Write received for: {pvname} --> {pval}')
        if pvname in self._map2write:
            ret = self._map2write[pvname](value)
            if ret:
                _log.info(f'YES Write for: {pvname} --> {pval}')
            else:
                _log.info(f'NOT Write for: {pvname} --> {pval}')
            return ret
        else:
            _log.warning('PV %s does not have a set function.', pvname)
            return False

    def run_callbacks(self, pvname, *args, **kwargs):
        """Run callback functions."""
        super().run_callbacks(self._prefix + pvname, *args, **kwargs)

    def get_map2write(self):
        """Return map of PV name to function for write."""
        return dict()

    def _update_log(self, value):
        self.run_callbacks('Log-Mon', value)

    def _update_status(self):
        pass


class BaseTimingConfig(_Callback):
    """Base timing configuration class."""

    def __init__(self, acc, callback=None):
        """Init method."""
        super().__init__(callback)
        self._csorb = _create_csorb(acc)
        self._config_ok_vals = {}
        self._config_pvs_rb = {}
        self._config_pvs_sp = {}

    @property
    def connected(self):
        """Status connected."""
        conn = True
        for k, pv in self._config_pvs_rb.items():
            if not pv.connected:
                _log.debug('NOT CONN: ' + pv.pvname)
            conn &= pv.connected
        for k, pv in self._config_pvs_sp.items():
            if not pv.connected:
                _log.debug('NOT CONN: ' + pv.pvname)
            conn &= pv.connected
        return conn

    @property
    def is_ok(self):
        """Ok status."""
        for k, val in self._config_ok_vals.items():
            pv = self._config_pvs_rb[k]
            pvval = None
            if pv.connected:
                pvval = pv.value
            if pvval is None:
                okay = False
                pvval = 'None'
            elif isinstance(val, float):
                okay = _math.isclose(val, pvval, rel_tol=1e-2)
            else:
                okay = val == pvval
            if not okay:
                msg = 'ERR: NOT CONF: {0:s}'.format(pv.pvname)
                self.run_callbacks('Log-Mon', msg)
                msg = msg[5:] + ' okv = {0}, v = {1}'.format(val, pvval)
                _log.warning(msg)
                return False
        return True

    def configure(self):
        """Configure method."""
        if not self.connected:
            return False
        for k, pv in self._config_pvs_sp.items():
            pv.put(self._config_ok_vals[k], wait=False)
        return True


def compare_kicks(val1, val2):
    """."""
    return _math.isclose(val1, val2, abs_tol=_ConstTLines.TINY_KICK)

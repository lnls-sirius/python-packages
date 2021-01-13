"""Epics PV derived classes."""

import time as _time
import struct as _struct
import numpy as _np

import epics as _epics

from ..envars import VACA_PREFIX as _prefix
from ..namesys import \
    SiriusPVName as _SiriusPVName, \
    get_pair_sprb as _get_pair_sprb


class EpicsProperty:
    """Pair of Epics PVs."""

    def __init__(self, name, prefix=_prefix, default_value=None,
                 connection_callback=None, callback=None):
        """Init."""
        try:
            self._name = _SiriusPVName(name)
            try:
                [self._pvname_sp, self._pvname_rb] = _get_pair_sprb(self._name)
            except TypeError:
                self._pvname_sp = name
                self._pvname_rb = name
        except Exception:
            self._name = name
            self._pvname_sp = name
            self._pvname_rb = name
        self._prefix = prefix
        self._default = default_value

        # Set callbacks
        self._connection_callback = connection_callback
        self._callback = callback
        callbacks = {'connection_callback': self._pv_connection_callback,
                     'callback': self._pv_callback}

        self._pv_sp = _epics.PV(self._prefix + self._pvname_sp, **callbacks)
        self._pv_rb = _epics.PV(self._prefix + self._pvname_rb, **callbacks)

    @property
    def name(self):
        """PV name."""
        return self._name

    @property
    def prefix(self):
        """PV prefix."""
        return self._prefix

    @property
    def suffix_sp(self):
        """PV SP suffix."""
        try:
            return self._pvname_sp.propty_suffix
        except Exception:
            return self._pvname_sp

    @property
    def suffix_rb(self):
        """PV RB suffix."""
        try:
            return self._pvname_rb.propty_suffix
        except Exception:
            return self._pvname_rb

    @property
    def pvname_sp(self):
        """Return SP pvname (without prefix)."""
        return self._pvname_sp

    @property
    def pvname_rb(self):
        """Return RB pvname (without prefix)."""
        return self._pvname_rb

    @property
    def connected(self):
        """State of connection."""
        return self._pv_sp.connected and self._pv_rb.connected

    @property
    def readback(self):
        """Property readback."""
        return self._pv_rb.get(timeout=0)

    @property
    def setpoint(self):
        """Property setpoint."""
        return self._pv_sp.get(timeout=0)

    @property
    def default(self):
        """Return default value."""
        return self._default

    @setpoint.setter
    def setpoint(self, value):
        """Set setpoint value."""
        if value is not None:
            self._pv_sp.value = value

    def set_setpoint_check(self, value, timeout):
        """Set setpoint value and check readback."""
        # setpoint
        self._pv_sp.value = value
        # check
        time0 = _time.time()
        while True:
            if self._pv_rb.value == value:
                return True
            if _time.time() - time0 > timeout:
                return False
            _time.sleep(min(0.1, timeout))

    def reset_default(self):
        """Reset to default value."""
        if self._default is not None:
            self.setpoint = self._default

    def set_callback(self, callback):
        """Set callback."""
        self._callback = callback

    def set_connection_callback(self, connection_callback):
        """Set connection callback."""
        self._connection_callback = connection_callback

    def _pv_connection_callback(self, **kwargs):
        if self._connection_callback is not None:
            kwargs['property'] = self
            self._connection_callback(**kwargs)

    def _pv_callback(self, **kwargs):
        if self._callback is not None:
            kwargs['property'] = self
            self._callback(**kwargs)


class EpicsPropertiesList:
    """List of Epics properties."""

    def __init__(self, properties):
        """Init."""
        self._properties = dict()
        for ppty in properties:
            self._properties[ppty.name] = ppty
        self._default = {p.name: p.default for p in self._properties.values()}
        self._logger = None

    @property
    def logger(self):
        """Return logger."""
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    @property
    def connected(self):
        """State of connection."""
        for ppty in self._properties.values():
            if not ppty.connected:
                return False
        return True

    @property
    def disconnected_properties(self):
        """Return list of disconnected properties."""
        props = []
        for name, ppty in self._properties.items():
            if not ppty.connected:
                props.append(name)
        return sorted(props)

    @property
    def properties(self):
        """Properties."""
        return sorted(self._properties.keys())

    @property
    def default(self):
        """Return default values dict."""
        return self._default

    @property
    def readbacks(self):
        """Return dict with all readbacks."""
        readbacks = dict()
        for name, ppty in self._properties.items():
            readbacks[name] = ppty.readback
        return readbacks

    def get_readback(self, name):
        """Return readback value of a property."""
        ppty = self._properties[name]
        return ppty.readback

    def get_setpoint(self, name):
        """Return setpoint value of a property."""
        ppty = self._properties[name]
        return ppty.setpoint

    def set_setpoints_check(self, setpoints, desired_readbacks=None,
                            timeout=5, order=None):
        """Set setpoints of properties."""
        if desired_readbacks is None:
            desired_readbacks = dict()
        if order is None:
            order = list(setpoints.keys())
        # setpoints
        is_nok = list()
        for name in order:
            value = setpoints[name]
            if value is not None:
                ppty = self._properties[name]
                ppty.setpoint = value
                if 'Cmd' not in name:
                    is_nok.append(name)
            if self._logger is not None:
                self._logger.update(name)
        # check
        if not desired_readbacks:
            desired_readbacks = setpoints
        time0 = _time.time()
        while _time.time() - time0 < timeout:
            finished = True
            for pvname, value in desired_readbacks.items():
                if value is None:
                    continue
                if pvname not in is_nok:
                    continue
                rbval = self._properties[pvname].readback
                if isinstance(value, (tuple, list, _np.ndarray)):
                    if not isinstance(rbval, (tuple, list, _np.ndarray)):
                        finished = False
                        break
                    if len(value) != len(rbval):
                        finished = False
                        break
                    if isinstance(rbval[0], (float, _np.float64)):
                        rbval = _np.asarray(rbval, dtype=_np.float32)
                    if isinstance(value[0], (float, _np.float64)):
                        value = _np.asarray(value, dtype=_np.float32)
                    finished = _np.array_equal(rbval, value)
                    if not finished:
                        break
                else:
                    finished = \
                        _struct.pack('f', rbval) == _struct.pack('f', value)
                    if not finished:
                        break
                if finished:
                    is_nok.remove(pvname)
            if finished:
                break
            _time.sleep(timeout/10.0)
        return finished, is_nok

    def reset_default(self):
        """Reset properties to default values."""
        for ppty in self._properties.values():
            ppty.reset_default()

    def set_callback(self, callback):
        """Set callback."""
        for ppty in self._properties.values():
            ppty.set_callback(callback)

    def set_connection_callback(self, connection_callback):
        """Set connection callback."""
        for ppty in self._properties.values():
            ppty.set_connection_callback(connection_callback)

    def __getitem__(self, key):
        """Property item."""
        if isinstance(key, int):
            properties = self.properties
            key = properties[key]
        return self._properties[key]

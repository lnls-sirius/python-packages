"""Devices of Archive PVs."""

import threading as _threading
import dateutil as _dateutil
from copy import deepcopy as _dcopy
import numpy as _np

from .pvarch import PVData as _PVData
from .time import Time as _Time
from ..search import BPMSearch as _BPMSearch
from ..util import ClassProperty as _classproperty


class Consts:
    """."""

    _BPMS_TB = None
    _BPMS_BO = None
    _BPMS_TS = None
    _BPMS_SI = None

    @_classproperty
    def BPMS_TB(cls):
        if cls._BPMS_TB is None:
            cls._BPMS_TB = _BPMSearch.get_names({'sec': 'TB'})
        return _dcopy(cls._BPMS_TB)

    @_classproperty
    def BPMS_BO(cls):
        if cls._BPMS_BO is None:
            cls._BPMS_BO = _BPMSearch.get_names({'sec': 'BO'})
        return _dcopy(cls._BPMS_BO)

    @_classproperty
    def BPMS_TS(cls):
        if cls._BPMS_TS is None:
            cls._BPMS_TS = _BPMSearch.get_names({'sec': 'TS'})
        return _dcopy(cls._BPMS_TS)

    @_classproperty
    def BPMS_SI(cls):
        if cls._BPMS_SI is None:
            cls._BPMS_SI = _BPMSearch.get_names({'sec': 'SI'})
        return _dcopy(cls._BPMS_SI)


class OrbitBPM(Consts):
    """."""

    _CONV = 0.001  # [nm -> um]

    class DEVICES:
        """."""

        TB_X = 'TB_X'
        TB_Y = 'TB_Y'
        BO_X = 'BO_X'
        BO_Y = 'BO_Y'
        TS_X = 'TS_X'
        TS_Y = 'TS_Y'
        SI_X = 'SI_X'
        SI_Y = 'SI_Y'

    Time = _Time

    def __init__(self, devname, connector=None):
        """."""
        self._devname = devname
        self._connector = connector
        self._bpmnames, self._pvnames = self._get_pvnames()
        self._pvdetails, self._pvdata = self._init_connectors()
        self._timestamp_start = None
        self._timestamp_stop = None
        self._times = None
        self._orbit = None

    @property
    def request_url(self):
        """."""
        for pvdata in self._pvdata.values():
            print(pvdata.request_url)

    @property
    def bpmnames(self):
        """Return ordered list of device BPMs."""
        return list(self._bpmnames)

    @property
    def pvnames(self):
        """."""
        return list(self._pvnames)

    @property
    def timestamp_start(self):
        """."""
        return self._timestamp_start

    @timestamp_start.setter
    def timestamp_start(self, value):
        """."""
        if isinstance(value, _Time):
            value = value.get_iso8601()
        self._timestamp_start = value

    @property
    def timestamp_stop(self):
        """."""
        return self._timestamp_stop

    @timestamp_stop.setter
    def timestamp_stop(self, value):
        """."""
        if isinstance(value, _Time):
            value = value.get_iso8601()
        self._timestamp_stop = value

    @property
    def timestamp(self):
        """Return retrieved orbit generated timestamps."""
        return self._times

    @property
    def value(self):
        """Return retrieved orbit interpolated values."""
        return self._orbit

    def update(self,
               timestamp_start=None, timestamp_stop=None, avg_dtime=None):
        """Update state by retrieving data.

        Parameters:
        timestamp_start -- ISO9601 str or Time object with starting instant.
                           Example: '2019-05-23T13:32:27.570Z'
        timestamp_stop -- ISO9601 str or Time object with stopping instant.
        dtime_avg -- averaging time window [s]. If None, no retrieved average
                     is performed.

        """
        if timestamp_start:
            self._timestamp_start = timestamp_start
        if timestamp_stop:
            self._timestamp_stop = timestamp_stop
        if None in (self._timestamp_start, self._timestamp_stop):
            raise Exception('Undefined timestamps!')

        # use threads to retrieve data, one for each PV
        threads = dict()
        for pvname in self._pvdata:
            threads[pvname] = _threading.Thread(
                target=self._update_pv, args=(pvname, avg_dtime), daemon=True)
            threads[pvname].start()
        for pvname in self._pvdata:
            threads[pvname].join()

        # interpolate data
        self._times, self._orbit = \
            self._interpolate_data(avg_dtime)

    def __getitem__(self, index):
        """Return raw timestamp and value tuple data for a given BPM."""
        if isinstance(index, int):
            pvname = self._pvnames[index]
        elif isinstance(index, str):
            if index in self._pvnames:
                pvname = index
            elif index in self._bpmnames:
                index = self._bpmnames.index(index)
                pvname = self._pvnames[index]
            else:
                raise IndexError
        pvdata = self._pvdata[pvname]
        return pvdata.timestamp, pvdata.value * OrbitBPM._CONV

    # --- private methods ---

    def _get_pvnames(self):
        if self._devname.startswith('TB'):
            bpmnames = OrbitBPM.BPMS_TB
        elif self._devname.startswith('BO'):
            bpmnames = OrbitBPM.BPMS_BO
        elif self._devname.startswith('TS'):
            bpmnames = OrbitBPM.BPMS_TS
        elif self._devname.startswith('SI'):
            bpmnames = OrbitBPM.BPMS_SI
        else:
            raise ValueError('Device not defined!')
        if self._devname.endswith('X'):
            propty = ':PosX-Mon'
        elif self._devname.endswith('Y'):
            propty = ':PosY-Mon'
        else:
            raise ValueError('Device not defined!')
        pvnames = tuple(bpm + propty for bpm in bpmnames)
        return bpmnames, pvnames

    def _init_connectors(self):
        pvdetails, pvdata = dict(), dict()
        for pvname in self._pvnames:
            pvdata[pvname] = _PVData(pvname, self._connector)
        return pvdetails, pvdata

    def _update_pv(self, pvname, avg_dtime):
        pvdata = self._pvdata[pvname]
        pvdata.timestamp_start = self._timestamp_start
        pvdata.timestamp_stop = self._timestamp_stop
        pvdata.update(avg_dtime)

    def _interpolate_data(self, avg_dtime):
        # calc avg_dtime if not passed
        nr_bpms = len(self._pvdata)
        if avg_dtime is None:
            avg_dtime = 0
            for pvdata in self._pvdata.values():
                avg_dtime += pvdata.timestamp[-1] - pvdata.timestamp[0]
            avg_dtime /= nr_bpms

        # times vector
        t0_, t1_ = \
            _dateutil.parser.parse(self.timestamp_start), \
            _dateutil.parser.parse(self.timestamp_stop)
        t0_, t1_ = t0_.timestamp(), t1_.timestamp()

        times = _np.arange(t0_, t1_, avg_dtime)

        # builds orbit matrix using interpolation
        orbit = _np.zeros((nr_bpms, len(times)))
        for i, pvname in enumerate(self._pvnames):
            pvdata = self._pvdata[pvname]
            values = \
                _np.interp(times, pvdata.timestamp, pvdata.value)
            orbit[i, :] = OrbitBPM._CONV * values

        # return data
        return times, orbit


class OrbitSOFB(Consts):
    """."""

    class DEVICES:
        """."""

        TB_X = 'TB_X'
        TB_Y = 'TB_Y'
        BO_X = 'BO_X'
        BO_Y = 'BO_Y'
        TS_X = 'TS_X'
        TS_Y = 'TS_Y'
        SI_X = 'SI_X'
        SI_Y = 'SI_Y'

    Time = _Time

    def __init__(self, devname, connector=None):
        """."""
        self._devname = devname
        self._connector = connector
        self._bpmnames, self._pvname = self._get_pvname()
        self._pvdetails, self._pvdata = self._init_connectors()
        self._timestamp_start = None
        self._timestamp_stop = None
        self._times = None
        self._orbit = None

    @property
    def request_url(self):
        """."""
        for pvdata in self._pvdata.values():
            print(pvdata.request_url)

    @property
    def pvname(self):
        """."""
        return self._pvname

    @property
    def timestamp_start(self):
        """."""
        return self._timestamp_start

    @timestamp_start.setter
    def timestamp_start(self, value):
        """."""
        if isinstance(value, _Time):
            value = value.get_iso8601()
        self._timestamp_start = value

    @property
    def timestamp_stop(self):
        """."""
        return self._timestamp_stop

    @timestamp_stop.setter
    def timestamp_stop(self, value):
        """."""
        if isinstance(value, _Time):
            value = value.get_iso8601()
        self._timestamp_stop = value

    @property
    def timestamp(self):
        """Return retrieved orbit generated timestamps."""
        return self._pvdata.timestamp

    @property
    def value(self):
        """Return retrieved orbit interpolated values."""
        return self._orbit

    def update(self,
               timestamp_start=None, timestamp_stop=None, avg_dtime=None):
        """Update state by retrieving data.

        Parameters:
        timestamp_start -- ISO9601 str or Time object with starting instant.
                           Example: '2019-05-23T13:32:27.570Z'
        timestamp_stop -- ISO9601 str or Time object with stopping instant.
        dtime_avg -- averaging time window [s]. If None, no retrieved average
                     is performed.

        """
        # NOTE: understand and fix this!
        if avg_dtime is not None:
            raise ValueError(
                'Retrieval of waveforms with averaging is bogous.')

        if timestamp_start:
            self._timestamp_start = timestamp_start
        if timestamp_stop:
            self._timestamp_stop = timestamp_stop
        if None in (self._timestamp_start, self._timestamp_stop):
            raise Exception('Undefined timestamps!')

        self._pvdata.timestamp_start = self._timestamp_start
        self._pvdata.timestamp_stop = self._timestamp_stop
        self._pvdata.update(avg_dtime)

        nrbpms = len(self._bpmnames)
        self._orbit = _np.array(self._pvdata.value)
        self._orbit = self._orbit.T[:nrbpms, :]

    # --- private methods ---

    def _get_pvname(self):
        if self._devname.startswith('TB'):
            bpmnames, dev = self.BPMS_TB, 'TB-Glob:AP-SOFB'
        elif self._devname.startswith('BO'):
            bpmnames, dev = self.BPMS_BO, 'BO-Glob:AP-SOFB'
        elif self._devname.startswith('TS'):
            bpmnames, dev = self.BPMS_TS, 'TS-Glob:AP-SOFB'
        elif self._devname.startswith('SI'):
            bpmnames, dev = self.BPMS_SI, 'SI-Glob:AP-SOFB'
        else:
            raise ValueError('Device not defined!')
        if self._devname.endswith('X'):
            propty = ':SlowOrbX-Mon'
        elif self._devname.endswith('Y'):
            propty = ':SlowOrbY-Mon'
        else:
            raise ValueError('Device not defined!')
        pvname = dev + propty
        return bpmnames, pvname

    def _init_connectors(self):
        pvdetails = None
        pvdata = _PVData(self._pvname, self._connector)
        return pvdetails, pvdata

"""Devices of Archive PVs."""

import threading as _threading
import dateutil as _dateutil
import numpy as _np

from .pvarch import PVData as _PVData
from .time import Time as _Time


class Consts:
    """."""

    BPMS_TB = (
        'TB-01:DI-BPM-1',
        'TB-01:DI-BPM-2',
        'TB-02:DI-BPM-1',
        'TB-02:DI-BPM-2',
        'TB-03:DI-BPM',
        'TB-04:DI-BPM',
        )

    BPMS_BO = (
        'BO-02U:DI-BPM',
        'BO-03U:DI-BPM',
        'BO-04U:DI-BPM',
        'BO-05U:DI-BPM',
        'BO-06U:DI-BPM',
        'BO-07U:DI-BPM',
        'BO-08U:DI-BPM',
        'BO-09U:DI-BPM',
        'BO-10U:DI-BPM',
        'BO-11U:DI-BPM',
        'BO-12U:DI-BPM',
        'BO-13U:DI-BPM',
        'BO-14U:DI-BPM',
        'BO-15U:DI-BPM',
        'BO-16U:DI-BPM',
        'BO-17U:DI-BPM',
        'BO-18U:DI-BPM',
        'BO-19U:DI-BPM',
        'BO-20U:DI-BPM',
        'BO-21U:DI-BPM',
        'BO-22U:DI-BPM',
        'BO-23U:DI-BPM',
        'BO-24U:DI-BPM',
        'BO-25U:DI-BPM',
        'BO-26U:DI-BPM',
        'BO-27U:DI-BPM',
        'BO-28U:DI-BPM',
        'BO-29U:DI-BPM',
        'BO-30U:DI-BPM',
        'BO-31U:DI-BPM',
        'BO-32U:DI-BPM',
        'BO-33U:DI-BPM',
        'BO-34U:DI-BPM',
        'BO-35U:DI-BPM',
        'BO-36U:DI-BPM',
        'BO-37U:DI-BPM',
        'BO-38U:DI-BPM',
        'BO-39U:DI-BPM',
        'BO-40U:DI-BPM',
        'BO-41U:DI-BPM',
        'BO-42U:DI-BPM',
        'BO-43U:DI-BPM',
        'BO-44U:DI-BPM',
        'BO-45U:DI-BPM',
        'BO-46U:DI-BPM',
        'BO-47U:DI-BPM',
        'BO-48U:DI-BPM',
        'BO-49U:DI-BPM',
        'BO-50U:DI-BPM',
        'BO-01U:DI-BPM',
        )

    BPMS_TS = (
        'TS-01:DI-BPM',
        'TS-02:DI-BPM',
        'TS-03:DI-BPM',
        'TS-04:DI-BPM-1',
        'TS-04:DI-BPM-2',
        )

    BPMS_SI = (
        'SI-01M2:DI-BPM',
        'SI-01C1:DI-BPM-1',
        'SI-01C1:DI-BPM-2',
        'SI-01C2:DI-BPM',
        'SI-01C3:DI-BPM-1',
        'SI-01C3:DI-BPM-2',
        'SI-01C4:DI-BPM',
        'SI-02M1:DI-BPM',
        'SI-02M2:DI-BPM',
        'SI-02C1:DI-BPM-1',
        'SI-02C1:DI-BPM-2',
        'SI-02C2:DI-BPM',
        'SI-02C3:DI-BPM-1',
        'SI-02C3:DI-BPM-2',
        'SI-02C4:DI-BPM',
        'SI-03M1:DI-BPM',
        'SI-03M2:DI-BPM',
        'SI-03C1:DI-BPM-1',
        'SI-03C1:DI-BPM-2',
        'SI-03C2:DI-BPM',
        'SI-03C3:DI-BPM-1',
        'SI-03C3:DI-BPM-2',
        'SI-03C4:DI-BPM',
        'SI-04M1:DI-BPM',
        'SI-04M2:DI-BPM',
        'SI-04C1:DI-BPM-1',
        'SI-04C1:DI-BPM-2',
        'SI-04C2:DI-BPM',
        'SI-04C3:DI-BPM-1',
        'SI-04C3:DI-BPM-2',
        'SI-04C4:DI-BPM',
        'SI-05M1:DI-BPM',
        'SI-05M2:DI-BPM',
        'SI-05C1:DI-BPM-1',
        'SI-05C1:DI-BPM-2',
        'SI-05C2:DI-BPM',
        'SI-05C3:DI-BPM-1',
        'SI-05C3:DI-BPM-2',
        'SI-05C4:DI-BPM',
        'SI-06M1:DI-BPM',
        'SI-06M2:DI-BPM',
        'SI-06C1:DI-BPM-1',
        'SI-06C1:DI-BPM-2',
        'SI-06C2:DI-BPM',
        'SI-06C3:DI-BPM-1',
        'SI-06C3:DI-BPM-2',
        'SI-06C4:DI-BPM',
        'SI-07M1:DI-BPM',
        'SI-07M2:DI-BPM',
        'SI-07C1:DI-BPM-1',
        'SI-07C1:DI-BPM-2',
        'SI-07C2:DI-BPM',
        'SI-07C3:DI-BPM-1',
        'SI-07C3:DI-BPM-2',
        'SI-07C4:DI-BPM',
        'SI-08M1:DI-BPM',
        'SI-08M2:DI-BPM',
        'SI-08C1:DI-BPM-1',
        'SI-08C1:DI-BPM-2',
        'SI-08C2:DI-BPM',
        'SI-08C3:DI-BPM-1',
        'SI-08C3:DI-BPM-2',
        'SI-08C4:DI-BPM',
        'SI-09M1:DI-BPM',
        'SI-09M2:DI-BPM',
        'SI-09C1:DI-BPM-1',
        'SI-09C1:DI-BPM-2',
        'SI-09C2:DI-BPM',
        'SI-09C3:DI-BPM-1',
        'SI-09C3:DI-BPM-2',
        'SI-09C4:DI-BPM',
        'SI-10M1:DI-BPM',
        'SI-10M2:DI-BPM',
        'SI-10C1:DI-BPM-1',
        'SI-10C1:DI-BPM-2',
        'SI-10C2:DI-BPM',
        'SI-10C3:DI-BPM-1',
        'SI-10C3:DI-BPM-2',
        'SI-10C4:DI-BPM',
        'SI-11M1:DI-BPM',
        'SI-11M2:DI-BPM',
        'SI-11C1:DI-BPM-1',
        'SI-11C1:DI-BPM-2',
        'SI-11C2:DI-BPM',
        'SI-11C3:DI-BPM-1',
        'SI-11C3:DI-BPM-2',
        'SI-11C4:DI-BPM',
        'SI-12M1:DI-BPM',
        'SI-12M2:DI-BPM',
        'SI-12C1:DI-BPM-1',
        'SI-12C1:DI-BPM-2',
        'SI-12C2:DI-BPM',
        'SI-12C3:DI-BPM-1',
        'SI-12C3:DI-BPM-2',
        'SI-12C4:DI-BPM',
        'SI-13M1:DI-BPM',
        'SI-13M2:DI-BPM',
        'SI-13C1:DI-BPM-1',
        'SI-13C1:DI-BPM-2',
        'SI-13C2:DI-BPM',
        'SI-13C3:DI-BPM-1',
        'SI-13C3:DI-BPM-2',
        'SI-13C4:DI-BPM',
        'SI-14M1:DI-BPM',
        'SI-14M2:DI-BPM',
        'SI-14C1:DI-BPM-1',
        'SI-14C1:DI-BPM-2',
        'SI-14C2:DI-BPM',
        'SI-14C3:DI-BPM-1',
        'SI-14C3:DI-BPM-2',
        'SI-14C4:DI-BPM',
        'SI-15M1:DI-BPM',
        'SI-15M2:DI-BPM',
        'SI-15C1:DI-BPM-1',
        'SI-15C1:DI-BPM-2',
        'SI-15C2:DI-BPM',
        'SI-15C3:DI-BPM-1',
        'SI-15C3:DI-BPM-2',
        'SI-15C4:DI-BPM',
        'SI-16M1:DI-BPM',
        'SI-16M2:DI-BPM',
        'SI-16C1:DI-BPM-1',
        'SI-16C1:DI-BPM-2',
        'SI-16C2:DI-BPM',
        'SI-16C3:DI-BPM-1',
        'SI-16C3:DI-BPM-2',
        'SI-16C4:DI-BPM',
        'SI-17M1:DI-BPM',
        'SI-17M2:DI-BPM',
        'SI-17C1:DI-BPM-1',
        'SI-17C1:DI-BPM-2',
        'SI-17C2:DI-BPM',
        'SI-17C3:DI-BPM-1',
        'SI-17C3:DI-BPM-2',
        'SI-17C4:DI-BPM',
        'SI-18M1:DI-BPM',
        'SI-18M2:DI-BPM',
        'SI-18C1:DI-BPM-1',
        'SI-18C1:DI-BPM-2',
        'SI-18C2:DI-BPM',
        'SI-18C3:DI-BPM-1',
        'SI-18C3:DI-BPM-2',
        'SI-18C4:DI-BPM',
        'SI-19M1:DI-BPM',
        'SI-19M2:DI-BPM',
        'SI-19C1:DI-BPM-1',
        'SI-19C1:DI-BPM-2',
        'SI-19C2:DI-BPM',
        'SI-19C3:DI-BPM-1',
        'SI-19C3:DI-BPM-2',
        'SI-19C4:DI-BPM',
        'SI-20M1:DI-BPM',
        'SI-20M2:DI-BPM',
        'SI-20C1:DI-BPM-1',
        'SI-20C1:DI-BPM-2',
        'SI-20C2:DI-BPM',
        'SI-20C3:DI-BPM-1',
        'SI-20C3:DI-BPM-2',
        'SI-20C4:DI-BPM',
        'SI-01M1:DI-BPM',
        )


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

    # NOTE: The bpm ordering should come from another location,
    # from a primary source! SOFB?

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

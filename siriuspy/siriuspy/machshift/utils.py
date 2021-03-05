"""Machine shift utils."""

import re as _re
import copy as _copy
import time as _time
from datetime import datetime as _datetime
from concurrent.futures import ThreadPoolExecutor
import numpy as _np
from scipy.interpolate import interp1d as _interp1d
from matplotlib import pyplot as _plt

from .. import util as _util
from .. import clientweb as _web
from ..namesys import SiriusPVName as _SiriusPVName
from ..clientarch import ClientArchiver as _CltArch, Time as _Time, \
    PVData as _PVData, PVDetails as _PVDetails


class MacScheduleData:
    """Machine schedule data."""

    _TAG_FORMAT = r'(\d+)h(\d+)-(\w)'

    _mac_schedule_data_plain = dict()
    _mac_schedule_data_numeric = dict()
    _user_operation_count = dict()

    @staticmethod
    def get_mac_schedule_data(year, formating='plain'):
        """Get machine schedule data for year."""
        MacScheduleData._reload_mac_schedule_data(year)
        if formating == 'plain':
            data = MacScheduleData._mac_schedule_data_plain[year]
            mac_schedule = _copy.deepcopy(data)
        elif formating == 'numeric':
            data = MacScheduleData._mac_schedule_data_numeric[year]
            mac_schedule = list(zip(*data))
        else:
            raise NotImplementedError(
                "machine schedule for formating '{}' "
                "is not defined".format(formating))
        return mac_schedule

    @staticmethod
    def get_users_operation_count(year):
        """Get users operation count for year."""
        MacScheduleData._reload_mac_schedule_data(year)
        return MacScheduleData._user_operation_count[year]

    @staticmethod
    def is_user_operation_predefined(
            timestamp=None, datetime=None, year=None,
            month=None, day=None, hour=None, minute=None):
        """Return whether a day is a predefined user operation."""
        ret_bool = False
        if timestamp is not None:
            if not isinstance(timestamp, (list, tuple, _np.ndarray)):
                timestamp = [timestamp, ]
                ret_bool = True
            datetime = [_datetime.fromtimestamp(ts) for ts in timestamp]
        elif datetime is not None:
            if not isinstance(datetime, (list, tuple, _np.ndarray)):
                datetime = [datetime, ]
                ret_bool = True
            timestamp = [dt.timestamp() for dt in datetime]
        elif year is not None:
            ret_bool = True
            datetime = [_datetime(year, month, day, hour, minute), ]
            timestamp = [dt.timestamp() for dt in datetime]
        else:
            raise Exception('Enter timestamp, datetime or datetime items data.')

        year_init = datetime[0].year
        year_end = datetime[-1].year
        times, tags = list(), list()
        for y2l in _np.arange(year_init, year_end+1):
            MacScheduleData._reload_mac_schedule_data(y2l)
            data = MacScheduleData._mac_schedule_data_numeric[y2l]
            ytim, ytag = list(zip(*data))
            times.extend(ytim)
            tags.extend(ytag)

        fun = _interp1d(times, tags, 'previous', fill_value='extrapolate')
        if ret_bool:
            return bool(fun(timestamp)[0])
        return fun(timestamp)

    @staticmethod
    def plot_mac_schedule(year):
        """Get machine schedule data for year."""
        MacScheduleData._reload_mac_schedule_data(year)
        timestamps, tags = MacScheduleData.get_mac_schedule_data(
            year, formating='numeric')
        days_of_year = len(MacScheduleData._mac_schedule_data_plain[year])
        fun = _interp1d(timestamps, tags, 'previous', fill_value='extrapolate')
        new_timestamp = _np.linspace(timestamps[0], timestamps[-1],
                                     days_of_year*24*60)
        new_datetimes = [_datetime.fromtimestamp(ts) for ts in new_timestamp]
        new_tags = fun(new_timestamp)

        _plt.plot_date(new_datetimes, new_tags, '-', label='')
        _plt.title('Machine Schedule - ' + str(year))
        _plt.legend()
        _plt.show()

    # --- private methods ---

    @staticmethod
    def _reload_mac_schedule_data(year):
        if year in MacScheduleData._mac_schedule_data_plain:
            return
        if not _web.server_online():
            raise Exception('could not connect to web server')

        try:
            data, _ = _util.read_text_data(_web.mac_schedule_read(year))
        except Exception:
            raise Exception(
                'could not read machine schedule data for year ' +
                str(year) + ' from web server')

        numeric_data = list()
        userop_count = 0
        for datum in data:
            if len(datum) < 2:
                raise Exception(
                    'there is a date ({0}) with problem in {1} '
                    'machine schedule'.format(datum, year))

            month, day = int(datum[0]), int(datum[1])
            if len(datum) == 2:
                timestamp = _datetime(year, month, day, 0, 0).timestamp()
                numeric_data.append((timestamp, 0))
            else:
                userop_count += 1
                for tag in datum[2:]:
                    hour, minute, flag = _re.findall(
                        MacScheduleData._TAG_FORMAT, tag)[0]
                    flag_bit = 0 if flag == 'E' else 1
                    hour, minute = int(hour), int(minute)
                    timestamp = _datetime(
                        year, month, day, hour, minute).timestamp()
                    numeric_data.append((timestamp, flag_bit))

        MacScheduleData._mac_schedule_data_plain[year] = data
        MacScheduleData._mac_schedule_data_numeric[year] = numeric_data
        MacScheduleData._user_operation_count[year] = userop_count


class MacReport:
    """Class for machine reports.

    Reports available:
    -

    """

    _THRESHOLD_STOREDBEAM = 0.005  # [mA]
    _AVG_TIME = 1  # [s]
    _MQUERRY_MIN_BIN_INTVL = 10  # [h]

    def __init__(self, connector=None):
        """Initialize object."""
        # client archiver connector
        self._connector = connector or _CltArch()

        # pvs used to compose reports
        self._pvnames = [
            'SI-Glob:AP-CurrInfo:Current-Mon',
            'AS-Glob:AP-MachShift:Mode-Sts',
        ]
        self._pvnames = [_SiriusPVName(pvn) for pvn in self._pvnames]

        # create pv connectors
        self._pvdata, self._pvdetails = self._init_connectors()

        # query data
        self._timestamp_start = None
        self._timestamp_stop = None
        self._failures_interval = None
        self._failures_count = None
        self._ebeam_total_interval = None
        self._ebeam_total_mean_current = None
        self._ebeam_users_progmd_interval = None
        self._ebeam_users_impltd_interval = None
        self._ebeam_users_mean_current = None
        self._mean_time_to_recover = None
        self._mean_time_between_failures = None
        self._beam_availability = None

        # auxiliary data
        self._failures = None

    @property
    def timestamp_start(self):
        """Query interval start timestamp."""
        return self._timestamp_start

    @timestamp_start.setter
    def timestamp_start(self, new_timestamp):
        if not self._timestamp_start or \
                new_timestamp != self._timestamp_start.get_timestamp():
            self._timestamp_start = _Time(timestamp=new_timestamp)

    @property
    def timestamp_stop(self):
        """Query interval stop timestamp."""
        return self._timestamp_stop

    @timestamp_stop.setter
    def timestamp_stop(self, new_timestamp):
        if not self._timestamp_stop or \
                new_timestamp != self._timestamp_stop.get_timestamp():
            self._timestamp_stop = _Time(timestamp=new_timestamp)

    @property
    def failures_interval(self):
        """Failures interval."""
        return self._failures_interval

    @property
    def failures_count(self):
        """Failures count."""
        return self._failures_count

    @property
    def ebeam_total_interval(self):
        """Electron beam interval."""
        return self._ebeam_total_interval

    @property
    def ebeam_total_mean_current(self):
        """Electron beam mean current."""
        return self._ebeam_total_mean_current

    @property
    def ebeam_users_impltd_interval(self):
        """Electron beam interval."""
        return self._ebeam_users_impltd_interval

    @property
    def ebeam_users_progmd_interval(self):
        """Electron beam interval."""
        return self._ebeam_users_progmd_interval

    @property
    def ebeam_users_mean_current(self):
        """Electron beam mean current in user shift."""
        return self._ebeam_users_mean_current

    @property
    def mean_time_to_recover(self):
        """Mean time to recover."""
        return self._mean_time_to_recover

    @property
    def mean_time_between_failures(self):
        """Mean time between failures."""
        return self._mean_time_between_failures

    @property
    def beam_availability(self):
        """Beam availability."""
        return self._beam_availability

    def update(self, avg_intvl=None):
        """Update."""
        if avg_intvl is None:
            avg_intvl = MacReport._AVG_TIME
        for pvname in self._pvnames:
            _t0 = _time.time()
            pvdata = self._pvdata[pvname]
            pvdata.timestamp_start = self._timestamp_start.get_iso8601()
            pvdata.timestamp_stop = self._timestamp_stop.get_iso8601()
            intvl = None if 'MachShift' in pvname else avg_intvl
            pvdata.update(intvl)
            print(pvname, _time.time() - _t0)
        self._compute_metrics()

    # ----- auxiliary methods -----

    def _init_connectors(self):
        pvdata, pvdetails = dict(), dict()
        for pvname in self._pvnames:
            pvdata[pvname] = _PVData(pvname, self._connector)
            pvdetails[pvname] = _PVDetails(pvname, self._connector)
        return pvdata, pvdetails

    def _compute_metrics(self):
        # get current data
        curr_data = self._pvdata['SI-Glob:AP-CurrInfo:Current-Mon']
        curr_values = _np.array(curr_data.value)
        is_stored = curr_values > MacReport._THRESHOLD_STOREDBEAM
        curr_times = _np.array(curr_data.timestamp)

        # get implemented shift data in current timestamps
        ishift_data = self._pvdata['AS-Glob:AP-MachShift:Mode-Sts']
        self._ishift_values = _np.array([int(not v) for v in ishift_data.value])
        ishift_times = _np.array(ishift_data.timestamp)
        ishift_fun = _interp1d(
            ishift_times, self._ishift_values, 'previous', fill_value='extrapolate')
        self._ishift_values = ishift_fun(curr_times)

        # get desired shift data in current timestamps
        _t0 = _time.time()
        self._dshift_values = MacScheduleData.is_user_operation_predefined(
            timestamp=curr_times)
        print('get desired shift data', _time.time() - _t0)

        # calculate time vectors
        dtimes = _np.diff(curr_times)
        dtimes = _np.insert(dtimes, 0, 0)
        dtimes_total_stored = dtimes*is_stored
        dtimes_users_progmd = dtimes*self._dshift_values
        dtimes_users_impltd = dtimes*self._dshift_values*_np.logical_not(
            self._failures)

        # tag failures
        self._failures = _np.logical_or(
            [(self._dshift_values - self._ishift_values) > 0], # wrong shift
            _np.logical_not(is_stored*dtimes_users_progmd)     # without beam
        )
        dtimes_failures = dtimes*self._failures

        # metrics
        self._failures_interval = _np.sum(dtimes_failures)

        self._failures_count = _np.sum(_np.diff(self._failures) > 0)

        self._ebeam_total_interval = _np.sum(dtimes_total_stored)

        self._ebeam_total_mean_current = \
            _np.sum(curr_values*dtimes_total_stored) / \
            self._ebeam_total_interval

        self._ebeam_users_progmd_interval = _np.sum(dtimes_users_progmd)

        self._ebeam_users_impltd_interval = _np.sum(dtimes_users_impltd)

        self._ebeam_users_mean_current = \
            _np.sum(curr_values*dtimes_users_impltd) / \
            self._ebeam_users_impltd_interval

        self._mean_time_to_recover = \
            self._failures_interval / self._failures_count

        self._mean_time_between_failures = \
            self._ebeam_users_progmd_interval / self._failures_count

        self._beam_availability = \
            self._ebeam_users_impltd_interval / \
            self._ebeam_users_progmd_interval

    def __getitem__(self, pvname):
        return self._pvdata[pvname], self._pvdetails[pvname]

"""Machine shift utils."""

import sys as _sys
import re as _re
import copy as _copy
import time as _time
import logging as _log
from datetime import datetime as _datetime

import numpy as _np
from scipy.interpolate import interp1d as _interp1d
from matplotlib import pyplot as _plt

from .. import util as _util
from .. import clientweb as _web
from ..namesys import SiriusPVName as _SiriusPVName
from ..clientarch import ClientArchiver as _CltArch, Time as _Time, \
    PVData as _PVData, PVDetails as _PVDetails
from .csdev import Const


class MacScheduleData:
    """Machine schedule data."""

    _TAG_FORMAT = r'(\d+)h(\d+)-(\w)'

    _mac_schedule_sdata = dict()
    _mac_schedule_ndata_byshift = dict()
    _mac_schedule_ndata_byday = dict()
    _mac_schedule_ndata_inicurr = dict()

    @staticmethod
    def get_mac_schedule_data(year, formating='plain'):
        """Get machine schedule data for year."""
        MacScheduleData._reload_mac_schedule_data(year)
        if formating == 'plain':
            data = MacScheduleData._mac_schedule_sdata[year]
            mac_schedule = _copy.deepcopy(data)
        elif formating == 'numeric_byshift':
            data = MacScheduleData._mac_schedule_ndata_byshift[year]
            mac_schedule = list(zip(*data))
        elif formating == 'numeric_byday':
            data = MacScheduleData._mac_schedule_ndata_byday[year]
            mac_schedule = list(zip(*data))
        else:
            raise NotImplementedError(
                "machine schedule for formating '{}' "
                "is not defined".format(formating))
        return mac_schedule

    @staticmethod
    def get_users_shift_count(begin, end):
        """Get users shift count for a period."""
        begin, end = MacScheduleData._handle_interval_data(begin, end)
        _, tags = MacScheduleData._get_numeric_data_for_interval(
            begin, end, dtype='macsched_byshift')
        return _np.sum(tags) if begin != end else 0

    @staticmethod
    def get_users_shift_day_count(begin, end):
        """Get users shift day count for a period."""
        begin, end = MacScheduleData._handle_interval_data(begin, end)
        _, tags = MacScheduleData._get_numeric_data_for_interval(
            begin, end, dtype='macsched_byday')
        return _np.sum(tags) if begin != end else 0

    @staticmethod
    def is_user_shift_programmed(
            timestamp=None, datetime=None,
            year=None, month=None, day=None, hour=0, minute=0):
        """Return whether a day is a predefined user shift."""
        timestamp, datetime, ret_uni = MacScheduleData._handle_timestamp_data(
            timestamp, datetime, year, month, day, hour, minute)
        times, tags = MacScheduleData._get_numeric_data_for_interval(
            datetime[0], datetime[-1], dtype='macsched_byshift')
        fun = _interp1d(times, tags, 'previous', fill_value='extrapolate')
        val = fun(timestamp)
        return bool(val) if ret_uni else val

    @staticmethod
    def get_initial_current_programmed(
            timestamp=None, datetime=None,
            year=None, month=None, day=None, hour=0, minute=0):
        """Return initial current for shift."""
        timestamp, datetime, ret_uni = MacScheduleData._handle_timestamp_data(
            timestamp, datetime, year, month, day, hour, minute)
        times, currs = MacScheduleData._get_numeric_data_for_interval(
            datetime[0], datetime[-1], dtype='initial_current')
        fun = _interp1d(times, currs, 'previous', fill_value='extrapolate')
        val = fun(timestamp)
        return val[0] if ret_uni else val

    @staticmethod
    def plot_mac_schedule(year):
        """Get machine schedule data for year."""
        MacScheduleData._reload_mac_schedule_data(year)
        times, tags = MacScheduleData.get_mac_schedule_data(
            year, formating='numeric_byshift')
        days_of_year = len(MacScheduleData._mac_schedule_sdata[year])
        fun = _interp1d(times, tags, 'previous', fill_value='extrapolate')
        new_timestamp = _np.linspace(times[0], times[-1], days_of_year*24*60)
        new_datetimes = [_datetime.fromtimestamp(ts) for ts in new_timestamp]
        new_tags = fun(new_timestamp)

        fig = _plt.figure()
        _plt.plot_date(new_datetimes, new_tags, '-')
        _plt.title('Machine Schedule - ' + str(year))
        return fig

    # --- private methods ---

    @staticmethod
    def _reload_mac_schedule_data(year):
        if year in MacScheduleData._mac_schedule_sdata:
            return
        if not _web.server_online():
            raise Exception('could not connect to web server')

        try:
            data, _ = _util.read_text_data(_web.mac_schedule_read(year))
        except Exception:
            print('No data provided for year ' + str(year) + '. '
                  'Getting template data.')
            data, _ = _util.read_text_data(_web.mac_schedule_read('template'))

        databyshift = list()
        databyday = list()
        datainicurr = list()
        for datum in data:
            if len(datum) < 3:
                raise Exception(
                    'there is a date ({0}) with problem in {1} '
                    'machine schedule'.format(datum, year))

            month, day, inicurr = int(datum[0]), int(datum[1]), float(datum[2])
            if len(datum) == 3:
                timestamp = _datetime(year, month, day, 0, 0).timestamp()
                databyshift.append((timestamp, 0))
                databyday.append((timestamp, 0))
                datainicurr.append((timestamp, inicurr))
            else:
                timestamp = _datetime(year, month, day, 0, 0).timestamp()
                databyday.append((timestamp, 1))
                datainicurr.append((timestamp, inicurr))
                for tag in datum[3:]:
                    hour, minute, flag = _re.findall(
                        MacScheduleData._TAG_FORMAT, tag)[0]
                    flag_bit = 0 if flag == 'E' else 1
                    hour, minute = int(hour), int(minute)
                    timestamp = _datetime(
                        year, month, day, hour, minute).timestamp()
                    databyshift.append((timestamp, flag_bit))

        MacScheduleData._mac_schedule_sdata[year] = data
        MacScheduleData._mac_schedule_ndata_byshift[year] = databyshift
        MacScheduleData._mac_schedule_ndata_byday[year] = databyday
        MacScheduleData._mac_schedule_ndata_inicurr[year] = datainicurr

    @staticmethod
    def _handle_timestamp_data(
            timestamp=None, datetime=None, year=None,
            month=None, day=None, hour=0, minute=0):
        ret_uni = False
        if timestamp is not None:
            if not isinstance(timestamp, (list, tuple, _np.ndarray)):
                timestamp = [timestamp, ]
                ret_uni = True
            datetime = [_datetime.fromtimestamp(ts) for ts in timestamp]
        elif datetime is not None:
            if not isinstance(datetime, (list, tuple, _np.ndarray)):
                datetime = [datetime, ]
                ret_uni = True
            timestamp = [dt.timestamp() for dt in datetime]
        elif year is not None:
            ret_uni = True
            datetime = [_datetime(year, month, day, hour, minute), ]
            timestamp = [dt.timestamp() for dt in datetime]
        else:
            raise Exception(
                'Enter timestamp, datetime or datetime items data.')
        return timestamp, datetime, ret_uni

    @staticmethod
    def _handle_interval_data(begin, end):
        if isinstance(begin, float):
            begin = _datetime.fromtimestamp(begin)
            end = _datetime.fromtimestamp(end)
        elif isinstance(begin, dict):
            begin = _datetime(**begin)
            end = _datetime(**end)
        return begin, end

    @staticmethod
    def _get_numeric_data_for_interval(begin, end, dtype='macsched_byshift'):
        times, tags = list(), list()
        for y2l in _np.arange(begin.year, end.year+1):
            MacScheduleData._reload_mac_schedule_data(y2l)
            if dtype == 'macsched_byshift':
                data = MacScheduleData._mac_schedule_ndata_byshift[y2l]
            elif dtype == 'macsched_byday':
                data = MacScheduleData._mac_schedule_ndata_byday[y2l]
            elif dtype == 'initial_current':
                data = MacScheduleData._mac_schedule_ndata_inicurr[y2l]
            ytim, ytag = list(zip(*data))
            times.extend(ytim)
            tags.extend(ytag)
        times, tags = _np.array(times), _np.array(tags)
        if begin != end:
            idcs = _np.where(_np.logical_and(
                times >= begin.timestamp(), times <= end.timestamp()))[0]
            if idcs[0] != 0:
                idcs = _np.r_[idcs[0]-1, idcs]
            return times[idcs], tags[idcs]
        return times, tags


class MacReport:
    """Machine reports.

    Based on archiver data and machine schedule data.

    Reports available:
    - ebeam_total_interval
        Time interval in which there was stored beam, for any
        current value above a threshold (THOLD_STOREDBEAM)
    - ebeam_total_average_current
        Average current considering the entire interval in which
        there was any current above a threshold (THOLD_STOREDBEAM)
    - ebeam_total_stddev_current
        Current standard deviation considering the entire interval in which
        there was any current above a threshold (THOLD_STOREDBEAM)
    - ebeam_total_max_current
        Maximum current considering the entire interval in which
        there was any current above a threshold (THOLD_STOREDBEAM)
    - user_shift_progmd_interval
        Time interval programmed to be user shift.
    - user_shift_impltd_interval
        Time interval implemented as programmed user shift, considering
        right shift and current above initial current*THOLD_FACTOR_USERSSBEAM.
    - user_shift_extra_interval
        Extra user shift time interval.
    - user_shift_total_interval
        Total user shift time interval (implemented + extra).
    - user_shift_progmd_count
        Count of user shifts programmed.
    - user_shift_canceled_count
        Count of user shifts canceled.
    - user_shift_average_current
        Average current in the total user shift time interval.
    - user_shift_stddev_current
        Current standard deviation in the total user shift time interval.
    - user_shift_max_current
        Maximum current in the total user shift time interval.
    - inj_shift_interval
        Time interval in injection shift
    - inj_shift_count
        Count of injections occurred
    - inj_shift_mean_interval
        Mean interval in injection shift (inj_shift_interval/inj_shift_count)
    - failures_interval
        Total failure duration.
    - failures_count
        Count of failures occurred.
    - beam_loss_count
        Count of beam losses occurred.
    - mean_time_to_recover
        Mean time took to recover from failures.
    - mean_time_between_failures
        Mean time between failure occurrences.
    - beam_availability
        Ratio between time implemented and time programmed as user shift.
    """

    THOLD_STOREDBEAM = 0.005  # [mA]
    THOLD_FACTOR_USERSSBEAM = 0.2  # 20%
    QUERY_AVG_TIME = 60  # [s]

    def __init__(self, connector=None, logger=None):
        """Initialize object."""
        # client archiver connector
        self._connector = connector or _CltArch()

        # auxiliary logger
        self._logger = logger
        self._logger_message = ''
        if not logger:
            _log.basicConfig(format='%(asctime)s | %(message)s',
                             datefmt='%F %T', level=_log.INFO,
                             stream=_sys.stdout)

        # pvs used to compose reports
        self._pvnames = [
            'SI-Glob:AP-CurrInfo:Current-Mon',
            'AS-Glob:AP-MachShift:Mode-Sts',
            # 'LI-01:EG-TriggerPS:enablereal',
            # 'LI-01:EG-PulsePS:singleselstatus',
        ]
        self._pvnames = [_SiriusPVName(pvn) for pvn in self._pvnames]

        # create pv connectors
        self._pvdata, self._pvdetails = self._init_connectors()

        # query data
        self._timestamp_start = None
        self._timestamp_stop = None
        self._ebeam_total_interval = None
        self._ebeam_total_average_current = None
        self._ebeam_total_stddev_current = None
        self._ebeam_total_max_current = None
        self._user_shift_progmd_interval = None
        self._user_shift_impltd_interval = None
        self._user_shift_extra_interval = None
        self._user_shift_total_interval = None
        self._user_shift_progmd_count = None
        self._user_shift_canceled_count = None
        self._user_shift_average_current = None
        self._user_shift_stddev_current = None
        self._user_shift_max_current = None
        self._inj_shift_interval = None
        self._inj_shift_count = None
        self._inj_shift_mean_interval = None
        self._failures_interval = None
        self._failures_count = None
        self._beam_loss_count = None
        self._mean_time_to_recover = None
        self._mean_time_between_failures = None
        self._beam_availability = None

        # auxiliary data
        self._raw_data = None
        self._failures = None
        self._curr_times = None
        self._curr_values = None
        self._inj_shift_values = None
        self._user_shift_values = None
        self._user_shift_progmd_values = None
        self._user_shift_inicurr_values = None
        self._is_stored_total = None
        self._is_stored_users = None

    @property
    def connector(self):
        """Client archiver connector."""
        return self._connector

    @property
    def timestamp_start(self):
        """Query interval start timestamp."""
        return self._timestamp_start

    @timestamp_start.setter
    def timestamp_start(self, new_timestamp):
        self._timestamp_start = _Time(timestamp=new_timestamp)

    @property
    def timestamp_stop(self):
        """Query interval stop timestamp."""
        return self._timestamp_stop

    @timestamp_stop.setter
    def timestamp_stop(self, new_timestamp):
        self._timestamp_stop = _Time(timestamp=new_timestamp)

    @property
    def ebeam_total_interval(self):
        """Stored electron beam interval."""
        return self._ebeam_total_interval/60/60

    @property
    def ebeam_total_average_current(self):
        """Stored electron beam average current."""
        return self._ebeam_total_average_current

    @property
    def ebeam_total_stddev_current(self):
        """Stored electron beam current standard deviation."""
        return self._ebeam_total_stddev_current

    @property
    def ebeam_total_max_current(self):
        """Stored electron beam maximum current."""
        return self._ebeam_total_max_current

    @property
    def user_shift_progmd_interval(self):
        """User shift interval programmed."""
        return self._user_shift_progmd_interval/60/60

    @property
    def user_shift_impltd_interval(self):
        """User shift interval implemented."""
        return self._user_shift_impltd_interval/60/60

    @property
    def user_shift_extra_interval(self):
        """User shift interval extra."""
        return self._user_shift_extra_interval/60/60

    @property
    def user_shift_total_interval(self):
        """User shift interval total (implemented + extra)."""
        return self._user_shift_total_interval/60/60

    @property
    def user_shift_average_current(self):
        """User shift average current."""
        return self._user_shift_average_current

    @property
    def user_shift_stddev_current(self):
        """User shift current standard deviation."""
        return self._user_shift_stddev_current

    @property
    def user_shift_max_current(self):
        """User shift maximum current."""
        return self._user_shift_max_current

    @property
    def user_shift_progmd_count(self):
        """User shift programmed count."""
        return self._user_shift_progmd_count

    @property
    def user_shift_canceled_count(self):
        """User shift canceled count."""
        return self._user_shift_canceled_count

    @property
    def inj_shift_interval(self):
        """Injection shift interval."""
        return self._inj_shift_interval/60/60

    @property
    def inj_shift_count(self):
        """Injection shift count."""
        return self._inj_shift_count

    @property
    def inj_shift_mean_interval(self):
        """Injection shift mean interval."""
        return self._inj_shift_mean_interval/60/60

    @property
    def failures_interval(self):
        """Failures interval."""
        return self._failures_interval/60/60

    @property
    def failures_count(self):
        """Failures count."""
        return self._failures_count

    @property
    def beam_loss_count(self):
        """Beam loss count."""
        return self._beam_loss_count

    @property
    def mean_time_to_recover(self):
        """Mean time to recover."""
        return self._mean_time_to_recover/60/60

    @property
    def mean_time_between_failures(self):
        """Mean time between failures."""
        return self._mean_time_between_failures/60/60

    @property
    def beam_availability(self):
        """Beam availability."""
        return self._beam_availability

    def update(self, avg_intvl=None):
        """Update."""
        if avg_intvl is None:
            avg_intvl = MacReport.QUERY_AVG_TIME
        for pvname in self._pvnames:
            _t0 = _time.time()
            pvdata = self._pvdata[pvname]
            pvdata.timestamp_start = self._timestamp_start.get_timestamp()
            pvdata.timestamp_stop = self._timestamp_stop.get_timestamp()
            intvl = None if 'Current' not in pvname else avg_intvl
            pvdata.update(intvl)
            self._update_log(
                'Query for {0} in archiver took {1}s'.format(
                    pvname, _time.time()-_t0))
        self._compute_metrics()

    @property
    def raw_data(self):
        """Shift data and failures details."""
        return self._raw_data

    def plot_raw_data(self):
        """Plot raw data for period timestamp_start to timestamp_stop."""
        datetimes = [_datetime.fromtimestamp(t)
                     for t in self._raw_data['Timestamp']]

        fig, axs = _plt.subplots(7, 1, sharex=True)
        fig.set_size_inches(8, 8)
        axs[0].set_title('Raw data')

        axs[0].plot_date(
            datetimes, self._raw_data['Current'], '-',
            color='blue', label='Current')
        axs[0].legend(loc='upper left')
        axs[0].grid()

        axs[1].plot_date(
            datetimes, self._raw_data['UserShiftInitCurr'], '-',
            color='blue', label='User Shifts - Initial Current')
        axs[1].legend(loc='upper left')
        axs[1].grid()

        axs[2].plot_date(
            datetimes, self._raw_data['InjShift'], '-',
            color='lightsalmon', label='Injection Shifts')
        axs[2].legend(loc='upper left')
        axs[2].grid()

        axs[3].plot_date(
            datetimes, self._raw_data['UserShiftProgmd'], '-',
            color='gold', label='User Shifts - Programmed')
        axs[3].legend(loc='upper left')
        axs[3].grid()

        axs[4].plot_date(
            datetimes, self._raw_data['UserShiftTotal'], '-',
            color='gold', label='User Shifts - Total')
        axs[4].legend(loc='upper left')
        axs[4].grid()

        axs[5].plot_date(
            datetimes, self._raw_data['Failures']['NoEBeam'], '-',
            color='red', label='Failures - NoEBeam')
        axs[5].legend(loc='upper left')
        axs[5].grid()

        axs[6].plot_date(
            datetimes, self._raw_data['Failures']['WrongShift'], '-',
            color='red', label='Failures - WrongShift')
        axs[6].legend(loc='upper left')
        axs[6].grid()

        fig.tight_layout()
        return fig

    # ----- auxiliary methods -----

    def _init_connectors(self):
        pvdata, pvdetails = dict(), dict()
        for pvname in self._pvnames:
            pvdata[pvname] = _PVData(pvname, self._connector)
            pvdetails[pvname] = _PVDetails(pvname, self._connector)
        return pvdata, pvdetails

    def _compute_metrics(self):
        self._raw_data = dict()

        # current data
        curr_data = self._pvdata['SI-Glob:AP-CurrInfo:Current-Mon']
        self._curr_values = _np.array(curr_data.value)
        self._curr_times = _np.array(curr_data.timestamp)
        self._raw_data['Timestamp'] = self._curr_times
        self._raw_data['Current'] = self._curr_values

        # implemented shift data
        ishift_data = self._pvdata['AS-Glob:AP-MachShift:Mode-Sts']
        ishift_times = _np.array(ishift_data.timestamp)

        inj_shift_values = _np.array(
            [1*(v == Const.MachShift.Injection) for v in ishift_data.value])
        inj_shift_fun = _interp1d(
            ishift_times, inj_shift_values,
            'previous', fill_value='extrapolate')
        self._inj_shift_values = inj_shift_fun(self._curr_times)
        self._raw_data['InjShift'] = self._inj_shift_values

        user_shift_values = _np.array(
            [1*(v == Const.MachShift.Users) for v in ishift_data.value])
        user_shift_fun = _interp1d(
            ishift_times, user_shift_values,
            'previous', fill_value='extrapolate')
        self._user_shift_values = user_shift_fun(self._curr_times)
        self._raw_data['UserShiftTotal'] = self._user_shift_values

        # desired shift data
        _t0 = _time.time()
        self._user_shift_progmd_values = \
            MacScheduleData.is_user_shift_programmed(
                timestamp=self._curr_times)
        self._user_shift_inicurr_values = \
            MacScheduleData.get_initial_current_programmed(
                timestamp=self._curr_times)
        self._user_shift_progmd_count = \
            MacScheduleData.get_users_shift_count(
                self._curr_times[0], self._curr_times[-1])
        self._update_log(
            'Query for machine schedule data took {0}s'.format(
                _time.time()-_t0))
        self._raw_data['UserShiftProgmd'] = self._user_shift_progmd_values
        self._raw_data['UserShiftInitCurr'] = self._user_shift_inicurr_values

        # # single/multi bunch mode data
        # egtrig_data = self._pvdata['LI-01:EG-PulsePS:singleselstatus']
        # egtrig_values = _np.array(egtrig_data.value)
        # egtrig_times = _np.array(egtrig_data.timestamp)

        # egmode_data = self._pvdata['LI-01:EG-TriggerPS:enablereal']
        # egmode_values = _np.array(egmode_data.value)
        # egmode_times = _np.array(egmode_data.timestamp)

        # is stored data
        self._is_stored_total = self._curr_values > MacReport.THOLD_STOREDBEAM
        self._is_stored_users = self._curr_values >= \
            self._user_shift_inicurr_values*MacReport.THOLD_FACTOR_USERSSBEAM

        # canceled shifts
        self._user_shift_act_values = \
            self._user_shift_values * self._is_stored_users

        self._shift_transit = _np.diff(self._user_shift_progmd_values)
        shift_beg_idcs = _np.where(self._shift_transit == 1)[0]
        shift_end_idcs = _np.where(self._shift_transit == -1)[0]
        if shift_beg_idcs[0] > shift_end_idcs[0]:
            shift_end_idcs = shift_end_idcs[1:]
        if shift_beg_idcs.size > shift_end_idcs.size:
            shift_end_idcs = _np.r_[
                shift_end_idcs, self._user_shift_progmd_values.size-1]
        shift_sts_values = [
            _np.mean(self._user_shift_act_values[
                shift_beg_idcs[i]:shift_end_idcs[i]])
            for i in range(shift_beg_idcs.size)]
        self._user_shift_canceled_count = _np.sum(
            _np.logical_not(shift_sts_values))

        # time vectors and failures
        dtimes = _np.diff(self._curr_times)
        dtimes = _np.insert(dtimes, 0, 0)
        dtimes_total_stored = dtimes*self._is_stored_total
        dtimes_users_progmd = dtimes*self._user_shift_progmd_values
        dtimes_injection = dtimes*self._inj_shift_values

        self._raw_data['Failures'] = dict()
        self._raw_data['Failures']['NoEBeam'] = \
            _np.logical_not(self._is_stored_users)*dtimes_users_progmd
        self._raw_data['Failures']['WrongShift'] = \
            1 * ((self._user_shift_progmd_values-self._user_shift_values) > 0)

        self._failures = 1 * _np.logical_or.reduce(
            [value for value in self._raw_data['Failures'].values()])
        dtimes_failures = dtimes*self._failures
        dtimes_users_impltd = dtimes_users_progmd*_np.logical_not(
            self._failures)
        dtimes_users_total = dtimes*self._user_shift_act_values
        dtimes_users_extra = dtimes_users_total*_np.logical_not(
            self._user_shift_progmd_values)

        # calculate metrics
        # # total stored beam metrics
        self._ebeam_total_interval = _np.sum(dtimes_total_stored)

        if not self._ebeam_total_interval:
            self._ebeam_total_average_current = 0.0
            self._ebeam_total_stddev_current = 0.0
        else:
            self._ebeam_total_average_current = \
                _np.sum(self._curr_values*dtimes_total_stored) / \
                self._ebeam_total_interval

            aux = (self._curr_values - self._ebeam_total_average_current)
            self._ebeam_total_stddev_current = _np.sqrt(
                _np.sum(aux*aux*dtimes_total_stored) /
                self._ebeam_total_interval)

        self._ebeam_total_max_current = _np.max(self._curr_values)

        # # injection shift metrics
        self._inj_shift_interval = _np.sum(dtimes_injection)

        self._inj_shift_count = _np.sum(_np.diff(self._inj_shift_values) > 0)

        self._inj_shift_mean_interval = 0.0 if self._inj_shift_count == 0 else\
            self._inj_shift_interval / self._inj_shift_count

        # # users shift metrics
        self._user_shift_progmd_interval = _np.sum(dtimes_users_progmd)

        self._user_shift_impltd_interval = _np.sum(dtimes_users_impltd)

        self._user_shift_extra_interval = _np.sum(dtimes_users_extra)

        self._user_shift_total_interval = _np.sum(dtimes_users_total)

        if not self._user_shift_total_interval:
            self._user_shift_average_current = 0.0
            self._user_shift_stddev_current = 0.0
        else:
            self._user_shift_average_current = \
                _np.sum(self._curr_values*dtimes_users_total) / \
                self._user_shift_total_interval

            aux = (self._curr_values - self._user_shift_average_current)
            self._user_shift_stddev_current = _np.sqrt(
                _np.sum(aux*aux*dtimes_users_total) /
                self._user_shift_total_interval)

        self._user_shift_max_current = _np.max(
            self._curr_values*self._user_shift_act_values)

        # # failure metrics
        self._failures_interval = _np.sum(dtimes_failures)

        self._failures_count = _np.sum(_np.diff(self._failures) > 0)

        beam_loss_values = _np.logical_not(
            self._raw_data['Failures']['WrongShift']) * \
            self._raw_data['Failures']['NoEBeam']
        self._beam_loss_count = _np.sum(_np.diff(beam_loss_values) > 0)

        self._mean_time_to_recover = 0.0 if not self._failures_count else \
            self._failures_interval/self._failures_count

        self._mean_time_between_failures = _np.inf if not self._failures_count\
            else self._user_shift_progmd_interval/self._failures_count

        self._beam_availability = \
            0.0 if not self._user_shift_progmd_interval else \
            self._user_shift_impltd_interval/self._user_shift_progmd_interval

    def __getitem__(self, pvname):
        return self._pvdata[pvname], self._pvdetails[pvname]

    def _update_log(self, message='', done=False, warning=False, error=False):
        self._logger_message = message
        if self._logger:
            self._logger.update(message, done, warning, error)
        if done and not message:
            message = 'Done.'
        _log.info(message)

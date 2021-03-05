"""Machine shift utils."""

import re as _re
import copy as _copy
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
    def is_user_operation_predefined(year=None, month=None, day=None,
                                     hour=None, minute=None, datetime=None):
        """Return whether a day is a predefined user operation."""
        if year is not None:
            datetime_obj = _datetime(year, month, day, hour, minute)
        else:
            year = datetime.year
            datetime_obj = datetime
        MacScheduleData._reload_mac_schedule_data(year)
        data = MacScheduleData._mac_schedule_data_numeric[year]
        timestamps, tags = list(zip(*data))
        fun = _interp1d(timestamps, tags, 'previous', fill_value='extrapolate')
        return bool(fun(datetime_obj.timestamp()))

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

        # query interval
        self._timestamp_start = None
        self._timestamp_stop = None

        # initialize auxiliary variables
        self._timestamp = dict()
        self._value = dict()

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

    def update(self):
        """Update."""
        for pvname in self._pvnames:
            pvdata = self._pvdata[pvname]
            pvdata.timestamp_start = self._timestamp_start.get_iso8601()
            pvdata.timestamp_stop = self._timestamp_stop.get_iso8601()
            pvdata.update()

    # ----- auxiliary methods -----

    def _init_connectors(self):
        pvdata, pvdetails = dict(), dict()
        for pvname in self._pvnames:
            pvdata[pvname] = _PVData(pvname, self._connector)
            pvdetails[pvname] = _PVDetails(pvname, self._connector)
        return pvdata, pvdetails

    def __getitem__(self, pvname):
        return self._pvdata[pvname], self._pvdetails[pvname]

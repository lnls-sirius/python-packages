"""."""

from .client import ClientArchiver as _ClientArchiver


class PVDetails:
    """Archive PV Details."""

    _field2type = {
        'Number of elements': ('nelms', int),
        'Units:': ('units', str),
        'Host name': ('host_name', str),
        'Average bytes per event': ('avg_bytes_per_event', float),
        'Estimated storage rate (KB/hour)':
            ('estimated_storage_rate_kb_hour', float),
        'Estimated storage rate (MB/day)':
            ('estimated_storage_rate_mb_day', float),
        'Estimated storage rate (GB/year)':
            ('estimated_storage_rate_gb_year', float),
        }

    def __init__(self, pvname, connector=None):
        """."""
        self.pvname = pvname
        self.connector = connector
        self.is_scalar = None
        self.is_paused = None
        self.is_connected = None
        self.nelms = None
        self.units = None
        self.host_name = None
        self.avg_bytes_per_event = None
        self.estimated_storage_rate_kb_hour = None
        self.estimated_storage_rate_mb_day = None
        self.estimated_storage_rate_gb_year = None

    @property
    def connected(self):
        """."""
        if not self.connector:
            return False
        return self.connector.connected

    @property
    def request_url(self):
        """."""
        self.connect()
        url = self.connector.getPVDetails(self.pvname, get_request_url=True)
        return url

    @property
    def is_archived(self):
        """."""
        self.connect()
        data = self.connector.getPVDetails(self.pvname)
        if not data:
            return False
        return True

    def connect(self):
        """."""
        if self.connector is None:
            self.connector = _ClientArchiver()

    def update(self):
        """."""
        self.connect()
        data = self.connector.getPVDetails(self.pvname)
        if not data:
            return False
        for datum in data:
            # print(datum)
            field, value = datum['name'], datum['value']
            # value = value.replace(',', '.')
            value = value.replace(',', '')
            if field in PVDetails._field2type:
                fattr, ftype = PVDetails._field2type[field]
                if not value == 'Not enough info':
                    value = ftype(value)
                setattr(self, fattr, value)
            elif field == 'Is this a scalar:':
                self.is_scalar = (value.lower() == 'yes')
            elif field == 'Is this PV paused:':
                self.is_paused = (value.lower() == 'yes')
            elif field == 'Is this PV currently connected?':
                self.is_connected = (value.lower() == 'yes')
        return True

    def __str__(self):
        """."""
        rst = ''
        rst += '{:<30s}: {:}\n'.format('pvname', self.pvname)
        rst += '{:<30s}: {:}\n'.format('is_scalar', self.is_scalar)
        rst += '{:<30s}: {:}\n'.format('is_paused', self.is_paused)
        rst += '{:<30s}: {:}\n'.format('is_connected', self.is_connected)
        rst += '{:<30s}: {:}\n'.format('nelms', self.nelms)
        rst += '{:<30s}: {:}\n'.format('units', self.units)
        rst += '{:<30s}: {:}\n'.format('host_name', self.host_name)
        rst += '{:<30s}: {:}\n'.format(
            'avg_bytes_per_event', self.avg_bytes_per_event)
        rst += '{:<30s}: {:}\n'.format(
            'estimated_storage_rate_kb_hour',
            self.estimated_storage_rate_kb_hour)
        rst += '{:<30s}: {:}\n'.format(
            'estimated_storage_rate_mb_day',
            self.estimated_storage_rate_mb_day)
        rst += '{:<30s}: {:}\n'.format(
            'estimated_storage_rate_gb_year',
            self.estimated_storage_rate_gb_year)
        return rst


class PVData:
    """Archive PV Data."""

    _MQUERY_BIN_INTVL = 10  # [h]

    def __init__(self, pvname, connector=None):
        """."""
        self.pvname = pvname
        self.connector = connector
        self.timestamp_start = None
        self.timestamp_stop = None
        self.timestamp = None
        self.value = None
        self.status = None
        self.severity = None

    @property
    def connected(self):
        """."""
        return self.connector and self.connector.connected

    @property
    def request_url(self):
        """."""
        self.connect()
        url = self.connector.getData(
            self.pvname, self.timestamp_start,
            self.timestamp_stop, get_request_url=True)
        return url

    @property
    def is_archived(self):
        """."""
        self.connect()
        req = self.connector.getPVDetails(self.pvname)
        if not req.ok:
            return False
        return True

    def connect(self):
        """."""
        if self.connector is None:
            self.connector = _ClientArchiver()

    def update_orig(self, mean_sec=None):
        """."""
        self.connect()
        if None in (self.timestamp_start, self.timestamp_stop):
            print('Start and stop timestamps not defined!')
            return
        process_type = 'mean' if mean_sec is not None else ''
        data = self.connector.getData(
            self.pvname, self.timestamp_start, self.timestamp_stop,
            process_type=process_type, interval=mean_sec)
        if not data:
            return
        self.timestamp, self.value, self.status, self.severity = data

    def update(self, mean_sec=None):
        """."""
        self.connect()
        if None in (self.timestamp_start, self.timestamp_stop):
            print('Start and stop timestamps not defined!')
            return
        process_type = 'mean' if mean_sec is not None else ''

        timestamp, value, status, severity = list(), list(), list(), list()

        t_start, t_stop = self.timestamp_start, self.timestamp_stop
        data = self.connector.getData(
            self.pvname, t_start, t_stop, process_type=process_type,
            interval=mean_sec)
        timestamp.extend(data[0])
        value.extend(data[1])
        status.extend(data[2])
        severity.extend(data[3])

        if not timestamp:
            return
        self.timestamp, self.value = timestamp, value
        self.status, self.severity = status, severity

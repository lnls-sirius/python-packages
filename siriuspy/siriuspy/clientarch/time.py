"""Time conversion module."""

from datetime import datetime as _datetime


class Time:
    """Time conversion class."""

    def __init__(self, year=None, month=None, day=None,
                 hour=None, minute=0, second=0, microsecond=0,
                 timestamp=None, datetime=None,
                 timestamp_string=None, timestamp_format=None):
        """Init."""
        if datetime:
            if not isinstance(datetime, _datetime):
                raise TypeError("Expected an argument of type 'datetime'.")
            self.datetime = datetime
        elif timestamp:
            if not isinstance(timestamp, float):
                raise TypeError("Expected an argument of type 'float'.")
            self.datetime = _datetime.fromtimestamp(timestamp)
        elif timestamp_string:
            if not isinstance(timestamp_string, str):
                raise TypeError("Expected an argument of type 'str'.")
            self.timestamp_format = '%Y-%m-%d %H:%M:%S.%f' \
                if timestamp_format is None else timestamp_format
            self.datetime = _datetime.strptime(
                timestamp_string, self.timestamp_format)
        else:
            self.datetime = _datetime(
                year=year, month=month, day=day,
                hour=hour, minute=minute, second=second,
                microsecond=microsecond)

    @property
    def year(self):
        """Return year."""
        return self.datetime.year

    @property
    def month(self):
        """Return month."""
        return self.datetime.month

    @property
    def day(self):
        """Return day."""
        return self.datetime.day

    @property
    def hour(self):
        """Return hour."""
        return self.datetime.hour

    @property
    def minute(self):
        """Return minute."""
        return self.datetime.minute

    @property
    def second(self):
        """Return second."""
        return self.datetime.second

    @property
    def microsecond(self):
        """Return microsecond."""
        return self.datetime.microsecond

    def get_timestamp(self):
        """Get timestamp in seconds since epoch format."""
        return self.datetime.timestamp()

    def get_iso8601(self):
        """Get iso8601 format."""
        return self.datetime.astimezone().isoformat()

    def __add__(self, other):
        """Addition."""
        if isinstance(other, Time):
            return self.datetime + other.datetime
        return self.datetime + other

    def __sub__(self, other):
        """Subtraction."""
        if isinstance(other, Time):
            return self.datetime - other.datetime
        return self.datetime - other

    def __eq__(self, other):
        """Equal operator."""
        if isinstance(other, Time):
            return self.datetime == other.datetime
        return self.datetime == other

    def __lt__(self, other):
        """Less-than operator."""
        if isinstance(other, Time):
            return self.datetime < other.datetime
        return self.datetime < other

    def __gt__(self, other):
        """Greater-than operator."""
        if isinstance(other, Time):
            return other.__lt__(self)
        return other.__lt__(self.datetime)

    def __le__(self, other):
        """Less-or-equal operator."""
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        """Greater-or-equal operator."""
        return self.__gt__(other) or self.__eq__(other)

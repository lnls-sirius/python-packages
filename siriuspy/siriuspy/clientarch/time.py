"""Time conversion module."""


class Time:
    """Time conversion class."""

    def __init__(self, year=None, month=None, day=None,
                 hour=None, minute=None, second=None, subsecond=None):
        """."""
        minute = 0 if minute is None else minute
        second = 0 if second is None else second
        subsecond = 0 if subsecond is None else subsecond
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.subsecond = subsecond

    def get_iso8601(self):
        """."""
        fstr = '{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.{:03d}Z'.format(
            self.year, self.month, self.day,
            self.hour, self.minute, self.second, int(self.subsecond*1000))
        return fstr

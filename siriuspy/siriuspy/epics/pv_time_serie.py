"""SiriusPVTimeSerie Class."""

import collections as _collections
import time as _time
import threading as _threading
import numpy as _np


class SiriusPVTimeSerie:
    """Class to handle time series from pv monitoring."""

    def __init__(self, pv,
                 time_window=None,
                 nr_max_points=None,
                 time_min_interval=0.0,
                 mode=0,
                 timestamp_init_data=None,
                 value_init_data=None,
                 use_pv_timestamp=True):
        """Class constructor."""
        if (use_pv_timestamp is False) and (mode == 1):
            raise ValueError(
                "Can not create an auto-fill serie without using "
                "PV timestamp!")
        self._pvobj = pv
        self._time_window = time_window
        self._time_min_interval = time_min_interval
        self._nr_max_points = nr_max_points
        self._use_pv_timestamp = use_pv_timestamp
        if timestamp_init_data:
            if not value_init_data:
                raise ValueError("Provide 'value_init_data' input!")
            self._timestamp_deque = _collections.deque(
                timestamp_init_data, maxlen=nr_max_points)
            self._value_deque = _collections.deque(
                value_init_data, maxlen=nr_max_points)
        else:
            self._timestamp_deque = _collections.deque(maxlen=nr_max_points)
            self._value_deque = _collections.deque(maxlen=nr_max_points)
        self._mode = mode
        if self._mode == 1:
            self._th_auto_acquire = _threading.Thread(
                target=self._auto_acquire, daemon=True)
            self._stop_auto_acquire = False
            self._th_auto_acquire.start()
        else:
            self._stop_auto_acquire = True

    @property
    def time_window(self):
        """Time window of datapoints."""
        return self._time_window

    @time_window.setter
    def time_window(self, value):
        self._time_window = value
        timestamp = _time.time()
        self._update(timestamp)

    @property
    def time_min_interval(self):
        """Minimum time interval between the datapoints."""
        return self._time_min_interval

    @time_min_interval.setter
    def time_min_interval(self, value):
        self._time_min_interval = value

        if self._timestamp_deque:
            old_timestamp_deque = _collections.deque(
                self._timestamp_deque, maxlen=self._nr_max_points)
            old_value_deque = _collections.deque(
                self._value_deque, maxlen=self._nr_max_points)
            self._timestamp_deque = _collections.deque(
                maxlen=self._nr_max_points)
            self._value_deque = _collections.deque(
                maxlen=self._nr_max_points)

            aux = old_timestamp_deque.pop()
            self._timestamp_deque.appendleft(aux)
            aux = old_value_deque.pop()
            self._value_deque.appendleft(aux)

            while old_timestamp_deque:
                if self._time_min_interval < (
                        self._timestamp_deque[0] - old_timestamp_deque[-1]):
                    aux = old_timestamp_deque.pop()
                    self._timestamp_deque.appendleft(aux)
                    aux = old_value_deque.pop()
                    self._value_deque.appendleft(aux)
                else:
                    old_timestamp_deque.pop()
                    old_value_deque.pop()

    @property
    def nr_max_points(self):
        """Maximum number of datapoints."""
        return self._nr_max_points

    @nr_max_points.setter
    def nr_max_points(self, value):
        self._nr_max_points = value
        self._timestamp_deque = _collections.deque(
            self._timestamp_deque, maxlen=self._nr_max_points)
        self._value_deque = _collections.deque(
            self._value_deque, maxlen=self._nr_max_points)

    @property
    def mode(self):
        """Mode of acquisition: 0 if manual and 1 if automatic."""
        return self._mode

    @mode.setter
    def mode(self, value):
        if self._mode != value:
            self._mode = value
            if self._mode == 1:
                self._th_auto_acquire = _threading.Thread(
                    target=self._auto_acquire, daemon=True)
                self._stop_auto_acquire = False
                self._th_auto_acquire.start()
            else:
                self._stop_auto_acquire = True

    @property
    def serie(self):
        """PV time series, as two separate lists: timestamp and value."""
        return self.get_serie()

    def get_serie(self, time_absolute=False):
        """Return series, as two separate numpy arrays: timestamp and value."""
        timestamp = _time.time()
        self._update(timestamp)
        timestamp_array = _np.array(self._timestamp_deque)
        if not time_absolute:
            timestamp_array -= timestamp
        value_array = _np.array(self._value_deque)
        return timestamp_array, value_array

    def acquire(self):
        """Acquire a new time serie datapoint.

        Returns True if datapoint was acquired and False otherwise.
        """
        minintv = self._time_min_interval
        # check if pv is connected
        if self.connected():
            timestamp = _time.time()
            if self._use_pv_timestamp:
                pv_timestamp, pv_value = \
                    self._pvobj.timestamp, self._pvobj.value
            else:
                pv_timestamp, pv_value = timestamp, self._pvobj.value

            # check if it is a new datapoint
            if not self._timestamp_deque or \
                    pv_timestamp != self._timestamp_deque[-1]:
                # check if there is a limiting time_window
                if self._time_window is None:
                    # check if there is a limiting time_min_interval
                    if not self._timestamp_deque or \
                            minintv <= timestamp-self._timestamp_deque[-1]:
                        self._timestamp_deque.append(pv_timestamp)
                        self._value_deque.append(pv_value)
                        return True
                    else:
                        # print('not acquired: time interval not sufficient')
                        return False
                else:
                    # Check if the datapoints in the deques are yet valid
                    # to the limiting time_window
                    self._update(timestamp)
                    # check if the new point is within the limiting time_window
                    if pv_timestamp >= timestamp - self._time_window:
                        if not self._timestamp_deque or \
                                minintv <= timestamp-self._timestamp_deque[-1]:
                            self._timestamp_deque.append(pv_timestamp)
                            self._value_deque.append(pv_value)
                            return True
                        else:
                            # print('not acquired: not enough time interval')
                            return False
                    else:
                        # print('not acquired: not within time_window')
                        return False
            else:
                # print('not acquired: item already in deque')
                return False
        else:
            # print('not acquired: pv not connected')
            return False

    def _auto_acquire(self):
        while not self._stop_auto_acquire:
            self.acquire()
            _time.sleep(self.time_min_interval)

    def _update(self, timestamp):
        """Update time serie according to current timestamp."""
        if not self._timestamp_deque or self._time_window is None:
            return

        min_timestamp = timestamp - self._time_window
        if self._timestamp_deque[-1] <= min_timestamp:
            self.clearserie()
        elif self._timestamp_deque[0] >= min_timestamp:
            pass
        else:
            low_interval_end = 0
            high_interval_end = len(self._timestamp_deque)-1
            search_index = (high_interval_end - low_interval_end)//2

            while low_interval_end != search_index:
                if self._timestamp_deque[search_index] <= min_timestamp:
                    low_interval_end = search_index
                    search_index = (
                        (high_interval_end - low_interval_end)//2 +
                        low_interval_end)
                else:
                    high_interval_end = search_index
                    search_index = (
                        (high_interval_end - low_interval_end)//2 +
                        low_interval_end)

            for _ in range(search_index + 1):
                self._timestamp_deque.popleft()
                self._value_deque.popleft()

    def clearserie(self):
        """Clear time serie."""
        self._timestamp_deque.clear()
        self._value_deque.clear()

    def connected(self):
        """Check PV connection."""
        return self._pvobj.connected

    def __str__(self):
        """Return string representation of time series."""
        raise NotImplementedError()

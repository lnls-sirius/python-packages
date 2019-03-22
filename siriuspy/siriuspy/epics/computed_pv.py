"""Definition of ComputedPV class that simulates a PV composed of epics PVs."""
from epics import get_pv as _get_pv
from siriuspy.epics import connection_timeout as _connection_timeout


class ComputedPV:
    """Computed PV class.

    Objects of this class are used for properties or process variables that are
    computed from other primary process variables. magnet strengths which
    are derived from power supply currents are typical examples of such
    computed process variables.
    """

    def __init__(self, pvname, computer, queue, pvs, monitor=True):
        """Initialize PVs."""
        # starts computer_pvs queue, if not started yet
        self._queue = queue
        if not self._queue.running:
            self._queue.start()

        # --- properties ---

        self.pvname = pvname
        self._value = None
        self._set_limits((None,)*6)
        self.computer = computer
        self.pvs = self._create_primary_pvs_list(pvs)

        # flags if computed_pv is of the 'monitor' type.
        self._monitor_pv = \
            '-Mon' in self.pvname and 'Ref-Mon' not in self.pvname

        # add callback
        self._callbacks = {}
        self._monitor = monitor
        if self._monitor:
            if self._monitor_pv:
                # in order to optimize efficiency if computed pv is of the
                # monitor type add callback only to the first primary pv, the
                # one corresponding to the main current to the call
                self.pvs[0].add_callback(self._value_update_callback)
            else:
                for pv in self.pvs:
                    pv.add_callback(self._value_update_callback)

        # init limits
        if self.connected:
            lims = self.computer.compute_limits(self)
            self._set_limits(lims)

        for pv in self.pvs:
            pv.run_callbacks()

    # --- public methods ---

    @property
    def connected(self):
        """Return wether all pvs are connected."""
        for pv in self.pvs:
            if not pv.connected:
                return False
        return True

    @property
    def value(self):
        """Return computed PV value."""
        return self.get()
        # return self._value

    def get(self):
        """Return current value of computed PV."""
        if self._monitor:
            pass
        else:
            self._update_value()
        return self._value

    def put(self, value):
        """Put `value` to the first pv of the pv list."""
        self._value = value
        self.computer.compute_put(self, value)

    def add_callback(self, func, index=None):
        """Add callback to be issued when a PV is updated."""
        if not callable(func):
            raise ValueError("Tried to set non callable as a callback")
        if index is None:
            index = 0 if len(self._callbacks) == 0 \
                else max(self._callbacks.keys()) + 1
        self._callbacks[index] = func
        return len(self._callbacks) - 1

    def run_callbacks(self):
        """Run all callbacks."""
        self._issue_callback(**{
            'pvname': self.pvname,
            'value': self._value,
            'hihi': self.upper_alarm_limit,
            'high': self.upper_warning_limit,
            'hilim': self.upper_disp_limit,
            'lolim': self.lower_disp_limit,
            'low': self.lower_warning_limit,
            'lolo': self.lower_alarm_limit,
            })

    def wait_for_connection(self, timeout):
        """Wait util computed PV is connected or until timeout."""
        pass

    # --- private methods ---

    def _set_limits(self, lims):
        self.upper_alarm_limit = lims[0]
        self.upper_warning_limit = lims[1]
        self.upper_disp_limit = lims[2]
        self.lower_disp_limit = lims[3]
        self.lower_warning_limit = lims[4]
        self.lower_alarm_limit = lims[5]

    def _create_primary_pvs_list(self, pvs):
        # get list of primary pvs
        ppvs = list()  # List with PVs used by the computed PV
        for pv in pvs:
            if isinstance(pv, str):  # give up string option.
                tpv = _get_pv(pv, connection_timeout=_connection_timeout)
                ppvs.append(tpv)
            else:
                ppvs.append(pv)
        return ppvs

    def _update_value(self, pvname=None, value=None):
        # Get dict with pv props that changed
        # print('update_value')
        kwargs = self.computer.compute_update(self, pvname, value)

        if kwargs is not None:
            if ('high' not in kwargs and kwargs['value'] == self._value) or \
                    ('high' in kwargs and
                     kwargs['value'] == self._value and
                     kwargs['hihi'] == self.upper_alarm_limit and
                     kwargs['high'] == self.upper_warning_limit and
                     kwargs['hilim'] == self.upper_disp_limit and
                     kwargs['hilim'] == self.lower_disp_limit and
                     kwargs['low'] == self.lower_warning_limit and
                     kwargs['lolo'] == self.lower_alarm_limit):
                # nothing changed
                return None
            self._value = kwargs["value"]
            # Check if limits are in the return dict and update them
            if "high" in kwargs:
                self.upper_alarm_limit = kwargs["hihi"]
                self.upper_warning_limit = kwargs["high"]
                self.upper_disp_limit = kwargs["hilim"]
                self.lower_disp_limit = kwargs["lolim"]
                self.lower_warning_limit = kwargs["low"]
                self.lower_alarm_limit = kwargs["lolo"]

            self._issue_callback(pvname=self.pvname, **kwargs)

    def _value_update_callback(self, pvname, value, **kwargs):
        # if 'Current-Mon' not in pvname:
        #     print(pvname, value)
        if self.connected:
            self._queue.add_callback(self._update_value, pvname, value)

    def _issue_callback(self, **kwargs):
        for index, callback in self._callbacks.items():
            callback(**kwargs)

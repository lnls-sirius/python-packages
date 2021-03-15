"""Power Supply Module."""

# import random as _random
import time as _time
import math as _math
import numpy as _np


from ...bsmp import SerialError as _SerialError


def _psupply_update_connected(func):
    # This functions decorates PSDevState methods to keep track of
    # connected status.
    def new_update_func(obj, *args, **kwargs):
        try:
            response = func(obj, *args, **kwargs)
            setattr(obj, '_connected', True)
            return response
        except _SerialError:
            setattr(obj, '_connected', False)
            raise
    return new_update_func


class PSDevState:
    """Power supply device state.

        Objects of this class are used to store power supply device
    states.
    """

    DEFAULT_UPDATE_INTERVAL_WFM = 2.0  # [s]
    DEFAULT_UPDATE_INTERVAL_VARIABLES = 0.1  # [s]
    DEFAULT_UPDATE_INTERVAL_PARAMETERS = 2.0  # [s]

    def __init__(self, psbsmp):
        """Init."""
        self._psbsmp = psbsmp
        self._connected = None
        self._groups = PSDevState._init_groups()
        self._variables = PSDevState._init_variables()
        self._curves = PSDevState._init_curves()
        self._parameters = self._init_parameters()
        self._wfmref_rb = None
        self._wfmref = None
        self._scope = None
        self._timestamp_update = None
        self._timestamp_update_group = None
        self._timestamp_update_variables = None
        self._timestamp_update_wfm = None
        self._timestamp_update_parameters = None

    @property
    def psbsmp(self):
        """Return PSBSMP communication objetc."""
        return self._psbsmp

    @property
    def connected(self):
        """Return connection state."""
        return self._connected

    @property
    def wfmref_rb(self):
        """Return wfmref_rb (Wfm-RB)."""
        return self._wfmref_rb

    @wfmref_rb.setter
    def wfmref_rb(self, value):
        """Set wfmref_rb.

        This is invoked for the object to store wfmref that has been read
        from power supply right after writting a new wfmref curve.
        """
        self._wfmref_rb = _np.array(value)

    @property
    def wfmref(self):
        """Return wfmref (WfmRef-Mon)."""
        return self._wfmref

    @property
    def wfmref_index(self):
        """Return current index into DSP selected curve."""
        curve_id = \
            self._variables[self._psbsmp.CONST.V_WFMREF_SELECTED]
        if curve_id == 0:
            beg = self._variables[
                self._psbsmp.CONST.V_WFMREF0_START]
            end = self._variables[
                self._psbsmp.CONST.V_WFMREF0_END]
        else:
            beg = self._variables[
                self._psbsmp.CONST.V_WFMREF1_START]
            end = self._variables[
                self._psbsmp.CONST.V_WFMREF1_END]
        index = self._psbsmp.curve_index_calc(beg, end)
        return index

    @property
    def scope(self):
        """Return scope (Wfm-Mon)."""
        return self._scope

    @property
    def variables(self):
        """."""
        return self._variables

    @property
    def parameters(self):
        """."""
        return self._parameters

    @property
    def timestamp_update(self):
        """Return timestamp of last power supply update."""
        tstamps = (
            self._timestamp_update,
            self._timestamp_update_group,
            self._timestamp_update_variables,
            self._timestamp_update_wfm)
        maxtstamp = max(val if val is not None else 0 for val in tstamps)
        return maxtstamp

    def get_variable(self, var_id):
        """."""
        return self._variables[var_id]

    def get_parameter(self, eid):
        """."""
        return self._parameters[eid]

    def update(self, interval=0.0):
        """Update all power supply entities.

        Method does not update groups of variables.
        """
        now = _time.time()
        tstamp = self._timestamp_update
        if tstamp is None or (now - tstamp) > interval:
            connected = True
            # variables
            if not self.update_variables(interval=0.0):
                return False
            connected &= self._connected
            # wfmref
            if not self.update_wfm(interval=0.0):
                return False
            connected &= self._connected
            # parameters
            if not self.update_parameters(interval=0.0):
                return False
            connected &= self._connected
            # update connected state
            self._connected = connected
            if connected:
                self._timestamp_update = now
        return True

    @_psupply_update_connected
    def update_groups(self, interval=0.0):
        """."""
        now = _time.time()
        tstamp = self._timestamp_update_group
        if tstamp is None or (now - tstamp) >= interval:
            ack, groupsinfo = self._psbsmp.query_list_of_group_of_variables()
            if ack == self.psbsmp.CONST_BSMP.ACK_OK:
                for i in range(len(groupsinfo)):
                    ack, var_ids = \
                        self._psbsmp.query_group_of_variables(group_id=i)
                    if ack == self.psbsmp.CONST_BSMP.ACK_OK:
                        self._groups[i] = var_ids
                    else:
                        return False
            else:
                return False
            self._timestamp_update_group = now
        return True

    @_psupply_update_connected
    def update_variables(self, interval=None):
        """Update all variables."""
        if interval is None:
            interval = PSDevState.DEFAULT_UPDATE_INTERVAL_VARIABLES
        now = _time.time()
        tstamp = self._timestamp_update_variables
        if tstamp is None or (now - tstamp) >= interval:
            group_id = self._psbsmp.CONST.G_ALL
            ack, values = self._psbsmp.read_group_of_variables(
                group_id=group_id)
            if ack == self.psbsmp.CONST_BSMP.ACK_OK:
                # update _variables with data read from device
                if group_id not in self._groups:
                    return False
                var_ids = self._groups[group_id]
                for var_id, value in zip(var_ids, values):
                    self._variables[var_id] = value
                # NOTE: test line for benchmarking
                # self._variables[27] += 0.001 * (_random.random() - 0.5)
                # update timestamp
                self._timestamp_update_variables = now
            else:
                return False
        return True

    @_psupply_update_connected
    def update_wfm(self, interval=None):
        """Update wfmref."""
        if self._psbsmp.IS_DCLINK:
            return True
        if interval is None:
            interval = PSDevState.DEFAULT_UPDATE_INTERVAL_WFM
        now = _time.time()
        tstamp = self._timestamp_update_wfm
        if tstamp is None or (now - tstamp) >= interval:
            # update wfmref
            wfmref = self._psbsmp.wfmref_read()
            if wfmref is None:
                return False
            self._wfmref = wfmref
            # update scope
            scope = self._psbsmp.scope_read()
            if scope is not None:
                self._scope = scope
                # NOTE: a successful readout means scope is not
                # currently being filled by DSP. Therefore a scope-fill
                # enable command is in order!
                self._psbsmp.scope_enable()
            # update timestamp (even it could not read scope)
            self._timestamp_update_wfm = now
        return True

    @_psupply_update_connected
    def update_parameters(self, interval=None):
        """Update power supply parameters."""
        if interval is None:
            interval = PSDevState.DEFAULT_UPDATE_INTERVAL_PARAMETERS
        now = _time.time()
        tstamp = self._timestamp_update_parameters
        if tstamp is None or (now - tstamp) >= interval:
            parameters = self._psbsmp.entities.parameters
            conn_status_ok = True
            for eid in parameters.eids:
                parameter = parameters[eid]
                counter = parameter['count']
                if eid != self._psbsmp.CONST.P_PS_NAME and counter > 1:
                    value = _np.zeros(counter)
                    for idx in range(counter):
                        value[idx] = self._psbsmp.parameter_read(eid, idx)
                        if value[idx] is None:
                            conn_status_ok = False
                        if _math.isnan(value[idx]):
                            value[idx] = 0
                else:
                    value = self._psbsmp.parameter_read(eid)
                    if value is None:
                        conn_status_ok = False
                self._parameters[eid] = value
                # print(eid, value)
            if conn_status_ok:
                self._timestamp_update_parameters = now
                return True
            return False
        return True

    def reset_variables_groups(self, groups):
        """."""
        # reset groups of variables for all bsmp devices
        ack, _ = self._psbsmp.reset_groups_of_variables(groups[3:])
        if ack != self.psbsmp.CONST_BSMP.ACK_OK:
            ValueError('Could not reset groups of variables!')
        return True

    # --- private methods ---

    @staticmethod
    def _init_groups():
        # NOTE: template to be expanded, if necessary.
        return dict()

    @staticmethod
    def _init_variables():
        # NOTE: template to be expanded, if necessary.
        return dict()

    @staticmethod
    def _init_curves():
        # NOTE: template to be expanded, if necessary.
        return dict()

    def _init_parameters(self):
        """Init power supply parameters."""
        parameters = self._psbsmp.entities.parameters
        parameters_values = dict()
        for eid in parameters.eids:
            if eid == 0:
                parameters_values[eid] = ''
            else:
                parameter = parameters[eid]
                counter = parameter['count']
                value = _np.zeros(counter) * float('NaN')
                parameters_values[eid] = value
        return parameters_values

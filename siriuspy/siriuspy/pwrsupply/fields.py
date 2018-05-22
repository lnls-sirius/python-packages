"""Define fields that map episc fields to bsmp entity ids.

These classes implement a common interface that exposes the `read` method.
"""
import re as _re

from siriuspy.pwrsupply.bsmp import Const as _c
from PRUserial485 import ConstSyncMode as _SYNC_MODE
from siriuspy.pwrsupply.status import PSCStatus as _PSCStatus


class VariableFactory:
    """Create a variable object."""

    @staticmethod
    def get(ps_model, device_id, epics_field, pru_controller):
        """Factory."""
        if epics_field == 'PwrState-Sts':
            return PwrState(
                Variable(pru_controller, device_id, _c.V_PS_STATUS))
        elif epics_field == 'OpMode-Sts':
            return OpMode(Variable(pru_controller, device_id, _c.V_PS_STATUS))
        elif epics_field == 'CtrlMode-Mon':
            return CtrlMode(
                Variable(pru_controller, device_id, _c.V_PS_STATUS))
        elif epics_field == 'OpenLoop-Mon':
            return OpenLoop(
                Variable(pru_controller, device_id, _c.V_PS_STATUS))
        elif epics_field == 'Current-RB':
            return Variable(pru_controller, device_id, _c.V_PS_SETPOINT)
        elif epics_field == 'CurrentRef-Mon':
            return Variable(pru_controller, device_id, _c.V_PS_REFERENCE)
        elif epics_field == 'Current-Mon':
            return Variable(pru_controller, device_id, _c.V_I_LOAD)
        elif epics_field == 'CycleEnbl-Mon':
            return Variable(pru_controller, device_id, _c.V_SIGGEN_ENABLE)
        elif epics_field == 'CycleType-Sts':
            return Variable(pru_controller, device_id, _c.V_SIGGEN_TYPE)
        elif epics_field == 'CycleNrCycles-RB':
            return Variable(pru_controller, device_id, _c.V_SIGGEN_NUM_CYCLES)
        elif epics_field == 'CycleIndex-Mon':
            return Variable(pru_controller, device_id, _c.V_SIGGEN_N)
        elif epics_field == 'CycleFreq-RB':
            return Variable(pru_controller, device_id, _c.V_SIGGEN_FREQ)
        elif epics_field == 'CycleAmpl-RB':
            return Variable(pru_controller, device_id, _c.V_SIGGEN_AMPLITUDE)
        elif epics_field == 'CycleOffset-RB':
            return Variable(pru_controller, device_id, _c.V_SIGGEN_OFFSET)
        elif epics_field == 'CycleAuxParam-RB':
            return Variable(pru_controller, device_id, _c.V_SIGGEN_AUX_PARAM)
        elif epics_field == 'IntlkSoft-Mon':
            return Variable(pru_controller, device_id, _c.V_PS_SOFT_INTERLOCKS)
        elif epics_field == 'IntlkHard-Mon':
            return Variable(pru_controller, device_id, _c.V_PS_HARD_INTERLOCKS)
        elif epics_field == 'Version-Cte':
            return Version(
                Variable(pru_controller, device_id, _c.V_FIRMWARE_VERSION))
        elif epics_field == 'WfmData-RB':
            return PRUCurve(pru_controller, device_id)
        elif epics_field == 'WfmIndex-Mon':
                return Constant(0)
        elif epics_field == 'PRUSyncMode-Mon':
            return PRUSyncMode(pru_controller)
        elif epics_field == 'PRUBlockIndex-Mon':
            return PRUProperty(pru_controller, 'pru_curve_block')
        elif epics_field == 'PRUSyncPulseCount-Mon':
            return PRUProperty(pru_controller, 'pru_sync_pulse_count')
        elif epics_field == 'PRUCtrlQueueSize-Mon':
            return PRUProperty(pru_controller, 'queue_length')
        elif epics_field == 'Current2-Mon':
            return Constant(0)
        else:
            raise ValueError('{} not defined'.format(epics_field))


class Variable:
    """Readable variable."""

    def __init__(self, pru_controller, device_id, bsmp_id):
        """Init properties."""
        self.pru_controller = pru_controller
        self.device_id = device_id
        self.bsmp_id = bsmp_id

    def read(self):
        """Read variable from pru controller."""
        return self.pru_controller.read_variables(self.device_id, self.bsmp_id)


class PRUCurve:
    """PRU Curve read."""

    def __init__(self, pru_controller, device_id):
        """Init properties."""
        self.pru_controller = pru_controller
        self.device_id = device_id

    def read(self):
        """Read curve."""
        return self.pru_controller.pru_curve_read(self.device_id)


class PRUProperty:
    """Read a PRU property."""

    def __init__(self, pru_controller, property):
        """Get pru controller and property name."""
        self.pru_controller = pru_controller
        self.property = property

    def read(self):
        """Read pru property."""
        return getattr(self.pru_controller, self.property)


class PRUSyncMode:
    """Return sync mode."""

    _sync_mode = {
        _SYNC_MODE.BRDCST: 1,
        _SYNC_MODE.RMPEND: 2,
        _SYNC_MODE.MIGEND: 3}

    def __init__(self, pru_controller):
        """Init."""
        self.sync_status = PRUProperty(pru_controller, 'pru_sync_status')
        self.sync_mode = PRUProperty(pru_controller, 'pru_sync_mode')

    def read(self):
        """Read."""
        if not self.sync_status.read():
            return 0
        else:
            return PRUSyncMode._sync_mode[self.sync_mode.read()]


class PwrState:
    """Variable decorator."""

    def __init__(self, variable):
        """Set variable."""
        self.variable = variable
        self.psc_status = _PSCStatus()

    def read(self):
        """Decorate read."""
        value = self.variable.read()
        if value is None:
            return value
        self.psc_status.ps_status = value
        return self.psc_status.ioc_pwrstate


class OpMode:
    """Variable decorator."""

    def __init__(self, variable):
        """Set variable."""
        self.variable = variable
        self.psc_status = _PSCStatus()

    def read(self):
        """Decorate read."""
        value = self.variable.read()
        if value is None:
            return value
        self.psc_status.ps_status = value
        return self.psc_status.ioc_opmode


class CtrlMode:
    """Variable decorator."""

    def __init__(self, variable):
        """Set variable."""
        self.variable = variable
        self.psc_status = _PSCStatus()

    def read(self):
        """Decorate read."""
        value = self.variable.read()
        if value is None:
            return value
        self.psc_status.ps_status = value
        return self.psc_status.interface


class OpenLoop:
    """Variable decorator."""

    def __init__(self, variable):
        """Set variable."""
        self.variable = variable
        self.psc_status = _PSCStatus()

    def read(self):
        """Decorate read."""
        value = self.variable.read()
        if value is None:
            return value
        self.psc_status.ps_status = value
        return self.psc_status.open_loop


class Version:
    """Version variable."""

    def __init__(self, variable):
        """Set variable."""
        self.variable = variable

    def read(self):
        """Decorate read."""
        value = self.variable.read()
        version = ''.join([c.decode() for c in value])
        try:
            value, _ = version.split('\x00', 0)
        except ValueError:
            value = version
        return value


class Constant:
    """Constant."""

    _constant_regexp = _re.compile('^.*-Cte$')

    def __init__(self, value):
        """Constant value."""
        self.value = value

    def read(self):
        """Return value."""
        return self.value

    @staticmethod
    def match(field):
        """Check if field is a constant."""
        return Constant._constant_regexp.match(field)


class Setpoint:
    """Setpoint."""

    _setpoint_regexp = _re.compile('^.*-(SP|Sel|Cmd)$')

    def __init__(self, epics_field, epics_database):
        """Init."""
        self.field = epics_field
        self.value = epics_database['value']
        self.database = epics_database
        if '-Cmd' in epics_field:
            self.is_cmd = True
        else:
            self.is_cmd = False
        self.type = epics_database['type']
        if 'count' in epics_database:
            self.count = epics_database['count']
        else:
            self.count = None
        if self.type == 'enum' and 'enums' in epics_database:
            self.enums = epics_database['enums']
        else:
            self.enums = None
        self.value = epics_database['value']
        if self.type in ('int', 'float'):
            if 'hihi' in epics_database:
                self.high = epics_database['hihi']
            else:
                self.high = None
            if 'lolo' in epics_database:
                self.low = epics_database['lolo']
            else:
                self.low = None

    def apply(self, value):
        """Apply setpoint value."""
        if self.check(value):
            if self.is_cmd:
                self.value += 1
            else:
                self.value = value
            return True
        return False

    def check(self, value):
        """Check value."""
        if self.is_cmd:
            if value > 1:
                return True
        elif self.type in ('int', 'float'):
            if self.low is None and self.high is None:
                return True
            if value is not None and (value > self.low and value < self.high):
                return True
        elif self.type == 'enum':
            if value in tuple(range(len(self.enums))):
                return True
        return False

    def read(self):
        """Return setpoint value."""
        return self.value

    # def trim_value(self, setpoint):
    #     if self.count is None:
    #         if self.low is not None:
    #             setpoint = max(self.low, setpoint)
    #         if self.high is not None:
    #             setpoint = min(self.high, setpoint)
    #         else:
    #             pass
    #     return setpoint

    @staticmethod
    def match(field):
        """Check if field is a setpoint."""
        return Setpoint._setpoint_regexp.match(field)

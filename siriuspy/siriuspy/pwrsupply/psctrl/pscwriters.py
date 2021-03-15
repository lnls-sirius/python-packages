"""Define functions used to map an epics field to a BSMP entity id.

These classes implement a command interface, that is, they have
an `execute` method.
"""

import re as _re

from ..csdev import Const as _const_psdev
from ..bsmp.constants import ConstPSBSMP as _const_psbsmp


class Function:
    """Generic function class."""

    def execute(self, value):
        """Execute function."""
        raise NotImplementedError()


class BSMPFunction(Function):
    """Used PRU controller to execute a function."""

    def __init__(self, device_ids, pru_controller, func_id, setpoints=()):
        """Get controller and bsmp function id."""
        self._device_ids = device_ids
        self.pru_controller = pru_controller
        self.func_id = func_id
        self.setpoints = setpoints

    def execute(self, value=None):
        """Execute command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            if value is None:
                self.pru_controller.exec_functions(
                    self._device_ids, self.func_id)
            else:
                self.pru_controller.exec_functions(
                    self._device_ids, self.func_id, value)


class Command(BSMPFunction):
    """Execute a Cmd type PV."""

    def execute(self, value=None):
        """Execute command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            self.pru_controller.exec_functions(self._device_ids, self.func_id)


class BSMPFunctionNull(BSMPFunction):
    """Do nothing."""

    def __init__(self):
        """Do nothing."""
        super().__init__(None, None, None)

    def execute(self, value=None):
        """Do nothing."""


class WfmMonAcq(Function):
    """Enable/Disable Wfm-Mon curve acquisition."""

    def __init__(self, device_ids, pru_controller, setpoints=None):
        """Define CurveAcq."""
        self._device_ids = device_ids
        self.enable = BSMPFunction(
            device_ids, pru_controller, _const_psbsmp.F_ENABLE_SCOPE)
        self.disable = BSMPFunction(
            device_ids, pru_controller, _const_psbsmp.F_DISABLE_SCOPE)
        self.setpoints = setpoints

    def execute(self, value=None):
        """Execute Command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            if value == 1:
                self.enable.execute()
            elif value == 0:
                self.disable.execute()


class WfmSP(Function):
    """Executes a Wfm curve write command."""

    def __init__(self, device_ids, pru_controller, setpoints=()):
        """Get pru controller."""
        self._device_ids = device_ids
        self.pru_controller = pru_controller
        self.setpoints = setpoints

    def execute(self, value=None):
        """Execute command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            for dev_id in self._device_ids:
                self.pru_controller.wfmref_write(dev_id, value)


class WfmUpdate(Function):
    """Wfm Update command."""

    def __init__(self, device_ids, pru_controller, setpoints=()):
        """Get controller and bsmp function id."""
        self._device_ids = device_ids
        self.pru_controller = pru_controller
        self.setpoints = setpoints

    def execute(self, value=None):
        """Execute command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            self.pru_controller.wfm_update(self._device_ids, interval=0)


class WfmUpdateAutoSel(Function):
    """Enable/Disable curves acquisition."""

    def __init__(self, device_ids, pru_controller, setpoints=None):
        """Define CurveAcq."""
        self._device_ids = device_ids
        self.pru_controller = pru_controller
        self.setpoints = setpoints

    def execute(self, value=None):
        """Execute Command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            if value == 1:
                self.pru_controller.scope_update_auto_enable()
            elif value == 0:
                self.pru_controller.scope_update_auto_disable()


class PRUCProperty(Function):
    """Executes a PRUCProperty command."""

    def __init__(self, pru_controller, property_name, setpoints=()):
        """Get pru controller."""
        self.pru_controller = pru_controller
        self.property = property_name
        self.setpoints = setpoints

    def execute(self, value=None):
        """Execute command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            setattr(self.pru_controller, self.property, value)


class PSPwrState(Function):
    """Adapter to deal with FBP turn on/off functions."""

    def __init__(self, device_ids, pru_controller, setpoints=None):
        """Define function."""
        self._device_ids = device_ids
        self.turn_on = BSMPFunction(
            device_ids, pru_controller, _const_psbsmp.F_TURN_ON)
        self.close_loop = BSMPFunction(
            device_ids, pru_controller, _const_psbsmp.F_CLOSE_LOOP)
        self.turn_off = BSMPFunction(
            device_ids, pru_controller, _const_psbsmp.F_TURN_OFF)
        self.setpoints = setpoints

    def execute(self, value=None):
        """Execute Command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            if value == 1:
                self.turn_on.execute()
                # Not necessary anymore from firmware v1.25 onwards
                # self.close_loop.execute()
            elif value == 0:
                self.turn_off.execute()


class PSPwrStateFBP_DCLink(Function):
    """Adapter to deal with FBP_DCLink turn on/off functions."""

    def __init__(self, device_ids, pru_controller, setpoints=None):
        """Define function."""
        self.setpoints = setpoints
        self.turn_on = BSMPFunction(
            device_ids, pru_controller, _const_psbsmp.F_TURN_ON)
        self.turn_off = BSMPFunction(
            device_ids, pru_controller, _const_psbsmp.F_TURN_OFF)
        self.open_loop = BSMPFunction(
            device_ids, pru_controller, _const_psbsmp.F_OPEN_LOOP)

    def execute(self, value=None):
        """Execute Command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            if value == _const_psdev.PwrStateSel.On:
                self.turn_on.execute()
            elif value == _const_psdev.PwrStateSel.Off:
                self.turn_off.execute()


# NOTE: writers below may be implemented as a general class 
# with the BMSP Function ID as an argument.


class CtrlLoop(Function):
    """Adapter to close or open control loops."""

    def __init__(self, device_ids, pru_controller, setpoints=None):
        """Define function."""
        self.pru_controller = pru_controller
        self.setpoints = setpoints
        self.open_loop = BSMPFunction(
            device_ids, pru_controller, _const_psbsmp.F_OPEN_LOOP)
        self.close_loop = BSMPFunction(
            device_ids, pru_controller, _const_psbsmp.F_CLOSE_LOOP)

    def execute(self, value=None):
        """Execute Command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            if value == 1:
                self.open_loop.execute(None)
            elif value == 0:
                self.close_loop.execute(None)


class PSOpMode(Function):
    """Decorate a function."""

    def __init__(self, device_ids, function, setpoints=None):
        """Command."""
        self._device_ids = device_ids
        self.function = function
        self.setpoints = setpoints

    def execute(self, value=None):
        """Parse before executing."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            if value == _const_psdev.OpMode.SlowRef:
                op_mode = _const_psdev.States.SlowRef
            elif value == _const_psdev.OpMode.SlowRefSync:
                op_mode = _const_psdev.States.SlowRefSync
            elif value == _const_psdev.OpMode.Cycle:
                op_mode = _const_psdev.States.Cycle
            elif value == _const_psdev.OpMode.RmpWfm:
                op_mode = _const_psdev.States.RmpWfm
            elif value == _const_psdev.OpMode.MigWfm:
                op_mode = _const_psdev.States.MigWfm
            else:
                op_mode = value
            # execute opmode change
            self.function.execute(op_mode)


class Current(Function):
    """Writer to set power supplies current."""
    # NOTE: This was needed when PRU was used to control timing.
    # It may be discarded...
    def __init__(self, device_ids, pru_controller, setpoints=None):
        """Create command to set current."""
        self._device_ids = device_ids
        self.pru_controller = pru_controller
        self.set_current = BSMPFunction(
            device_ids, pru_controller, _const_psbsmp.F_SET_SLOWREF)
        self.setpoints = setpoints

    def execute(self, value=None):
        """Execute command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            self.set_current.execute(value)

class Voltage(Function):
    """Command to set voltage in DCLink type PS."""

    def __init__(self, device_ids, pru_controller, setpoints=None):
        """Create command to set voltage."""
        self.device_ids = device_ids
        func_id = _const_psbsmp.F_SET_SLOWREF
        self.set_voltage = BSMPFunction(device_ids, pru_controller, func_id)
        self.setpoints = setpoints

    def execute(self, value=None):
        """Execute command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            self.set_voltage.execute()


class ScopeSrcAddr(Function):
    """Writer to set scope source address."""
    def __init__(self, device_ids, pru_controller, setpoints=None):
        """."""
        self._device_ids = device_ids
        self.pru_controller = pru_controller
        self.set_address = BSMPFunction(
            device_ids, pru_controller, _const_psbsmp.F_CFG_SOURCE_SCOPE)
        self.setpoints = setpoints

    def execute(self, value=None):
        """Execute command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            self.set_address.execute(value)


class ScopeFreq(Function):
    """Writer to set scpope frequency."""
    def __init__(self, device_ids, pru_controller, setpoints=None):
        """."""
        self._device_ids = device_ids
        self.pru_controller = pru_controller
        self.set_frequency = BSMPFunction(
            device_ids, pru_controller, _const_psbsmp.F_CFG_FREQ_SCOPE)
        self.setpoints = setpoints

    def execute(self, value=None):
        """Execute command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            self.set_frequency.execute(value)


class ScopeDuration(Function):
    """Writer to set scpope frequency."""
    def __init__(self, device_ids, pru_controller, setpoints=None):
        """."""
        self._device_ids = device_ids
        self.pru_controller = pru_controller
        self.set_duration = BSMPFunction(
            device_ids, pru_controller, _const_psbsmp.F_CFG_DURATION_SCOPE)
        self.setpoints = setpoints

    def execute(self, value=None):
        """Execute command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            self.set_duration.execute(value)


class CfgSiggen(Function):
    """Command to configure siggen."""

    def __init__(self, device_ids, pru_controller, idx, setpoints=None):
        """Init."""
        self._idx = idx
        self._setpoints = setpoints
        self._cfg = BSMPFunction(
            device_ids, pru_controller, _const_psbsmp.F_CFG_SIGGEN)

    def execute(self, value=None):
        """Execute command."""
        if self._idx == 5:
            if not self._setpoints or \
                    (self._setpoints and
                     self._setpoints.apply(value[self._idx:])):
                self._cfg.execute(value)
        else:
            if not self._setpoints or \
                    (self._setpoints and
                     self._setpoints.apply(value[self._idx])):
                self._cfg.execute(value)


class SOFBCurrent(Function):
    """."""

    def __init__(self, device_ids, pru_controller, setpoints=None):
        """Create command to set SOFBCurrent."""
        self._device_ids = device_ids
        self.pru_controller = pru_controller
        self.setpoints = setpoints

    def execute(self, value=None):
        """Execute command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            self.pru_controller.sofb_current_set(value)


class SOFBMode(Function):
    """."""

    def __init__(self, pru_controller, setpoints=None):
        """Create command to set SOFBMode."""
        self.pru_controller = pru_controller
        self.setpoints = setpoints

    def execute(self, value=None):
        """Execute command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            self.pru_controller.sofb_mode_set(value)


class SOFBUpdate(Function):
    """."""

    def __init__(self, pru_controller, setpoints=None):
        """Create command to set SOFBMode."""
        self.pru_controller = pru_controller
        self.setpoints = setpoints

    def execute(self, value=None):
        """Execute command."""
        if not self.setpoints or \
                (self.setpoints and self.setpoints.apply(value)):
            self.pru_controller.sofb_update_variables_state()


class Setpoint:
    """Setpoint."""

    _regexp_setpoint = _re.compile('^.*-(SP|Sel|Cmd)$')

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
        else:
            self.low = None
            self.high = None

    def apply(self, value):
        """Apply setpoint value."""
        if self._check(value):
            if self.is_cmd:
                self.value += 1
            else:
                self.value = value
            return True
        return False

    def read(self):
        """Read setpoint value."""
        return self.value

    def _check(self, value):
        """Check value."""
        if self.is_cmd:
            if value > 0:
                return True
        elif self.type in ('int', 'float'):
            if self.low is None and self.high is None:
                return True
            if value is not None and \
               (value >= self.low and value <= self.high):
                return True
        elif self.type == 'enum':
            if value in tuple(range(len(self.enums))):
                return True
        return False

    @staticmethod
    def match(field):
        """Check if field is a setpoint."""
        return Setpoint._regexp_setpoint.match(field)


class Setpoints:
    """Setpoints."""

    def __init__(self, setpoints):
        """Constructor."""
        self._setpoints = setpoints

    def apply(self, value):
        """Apply setpoint."""
        for setpoint in self._setpoints:
            if not setpoint.apply(value):
                return False

        return True

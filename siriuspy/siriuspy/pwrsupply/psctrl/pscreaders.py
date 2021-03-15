"""Reader Classes.

Define classes whose objects are mapped from epics PVs to
power supply controllers properties or functions. These classes
implement a common interface that exposes the `read` method.
"""
import re as _re

from .pscstatus import PSCStatus as _PSCStatus


class Variable:
    """Readable BSMP variable."""

    def __init__(self, pru_controller, device_id, bsmp_id):
        """Init properties."""
        self.pru_controller = pru_controller
        self.device_id = device_id
        self.bsmp_id = bsmp_id

    def read(self):
        """Read variable from pru controller."""
        value = self.pru_controller.read_variables(
            self.device_id, self.bsmp_id)
        return value


class WfmRBCurve:
    """BSMP PS WfmRB Curve read."""

    def __init__(self, pru_controller, device_id):
        """Init properties."""
        self.pru_controller = pru_controller
        self.device_id = device_id

    def read(self):
        """Read curve."""
        data = self.pru_controller.wfmref_rb_read(self.device_id)
        return data


class WfmRefMonCurve:
    """BSMP PS WfmRef-Mon Curve read."""

    def __init__(self, pru_controller, device_id):
        """Init properties."""
        self.pru_controller = pru_controller
        self.device_id = device_id

    def read(self):
        """Read curve."""
        data = self.pru_controller.wfmref_read(self.device_id)
        return data


class WfmMonCurve:
    """BSMP PS Wfm-Mon Curve read."""

    def __init__(self, pru_controller, device_id):
        """Init properties."""
        self.pru_controller = pru_controller
        self.device_id = device_id

    def read(self):
        """Read curve."""
        data = self.pru_controller.scope_read(self.device_id)
        # print(self.device_id, data)
        return data


class WfmIndexCurve:
    """BSMP PS WfmIndex Curve read."""

    def __init__(self, pru_controller, device_id):
        """Init properties."""
        self.pru_controller = pru_controller
        self.device_id = device_id

    def read(self):
        """Read curve."""
        data = self.pru_controller.wfmref_index(self.device_id)
        return data


class WfmUpdateAutoSts:
    """Wfm Update Auto Status."""

    def __init__(self, pru_controller, device_id):
        """Init properties."""
        self.pru_controller = pru_controller
        self.device_id = device_id

    def read(self):
        """Read status."""
        data = self.pru_controller.scope_update_auto
        return data


class TimestampUpdate:
    """Timestamp update read."""

    def __init__(self, pru_controller, device_id):
        """Init properties."""
        self.pru_controller = pru_controller
        self.device_id = device_id

    def read(self):
        """Read curve."""
        timestamp = self.pru_controller.timestamp_update()
        return timestamp


class PRUCProperty:
    """Read a PRU property."""

    def __init__(self, pru_controller, pru_property):
        """Get pru controller and property name."""
        self.pru_controller = pru_controller
        self.property = pru_property

    def read(self):
        """Read pru property."""
        return getattr(self.pru_controller, self.property)


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
            return None
        self.psc_status.ps_status = value
        return self.psc_status.state


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


class CtrlLoop:
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
        if value is None:
            return None
        version = ''.join([c.decode() for c in value])
        try:
            value, _ = version.split('\x00', 0)
        except ValueError:
            value = version
        return value


class Constant:
    """Constant."""

    _regexp_constant = _re.compile('^.*-Cte$')

    def __init__(self, value):
        """Constant value."""
        self.value = value

    def read(self):
        """Return value."""
        return self.value

    @staticmethod
    def match(field):
        """Check if field is a constant."""
        return Constant._regexp_constant.match(field)


class ConstParameter:
    """Readable power supply parameter."""

    def __init__(self, pru_controller, device_id, param_id):
        """Init properties."""
        self.pru_controller = pru_controller
        self.device_id = device_id
        self.param_id = param_id
        self.value = None

    def read(self):
        """Read ps parameter from pru controller."""
        if self.value is None:
            self.update()
        return self.value

    def update(self):
        """Update value."""
        self.value = self.pru_controller.read_parameters(
            self.device_id, self.param_id)

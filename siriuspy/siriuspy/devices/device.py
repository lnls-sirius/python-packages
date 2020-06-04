"""Epics Devices and Device Application."""

import time as _time

from epics.ca import ChannelAccessGetFailure as _ChannelAccessGetFailure

from ..envars import VACA_PREFIX as _VACA_PREFIX
from ..epics import PV as _PV, CONNECTION_TIMEOUT as _CONN_TIMEOUT, \
    GET_TIMEOUT as _GET_TIMEOUT
from ..simul import SimPV as _PVSim
from ..simul import Simulation as _Simulation
from ..namesys import SiriusPVName as _SiriusPVName


class Device:
    """Epics Device."""

    CONNECTION_TIMEOUT = _CONN_TIMEOUT
    GET_TIMEOUT = _GET_TIMEOUT
    _properties = ()

    def __init__(self, devname, properties):
        """."""
        self._properties = properties[:]
        self._devname, self._pvs = self._create_pvs(devname)

    @property
    def devname(self):
        """Return device name."""
        return self._devname

    @property
    def properties(self):
        """Return device properties."""
        return self._properties

    @property
    def simulators(self):
        """Return simulator."""
        sims = set()
        for pvname in self.pvnames:
            sims.update(_Simulation.simulator_find(pvname))
        return sims

    @property
    def pvnames(self):
        """Return device PV names."""
        pvnames = {pv.pvname for pv in self._pvs.values()}
        return pvnames

    @property
    def connected(self):
        """Return PVs connection status."""
        for pvobj in self._pvs.values():
            if not pvobj.connected:
                return False
        return True

    @property
    def disconnected_pvnames(self):
        """Return list of disconnected device PVs."""
        set_ = set()
        for pvname, pvobj in self._pvs.items():
            if not pvobj.connected:
                set_.add(pvname)
        return set_

    def update(self):
        """Update device properties."""
        for pvobj in self._pvs.values():
            pvobj.get()

    def pv_object(self, propty):
        """Return PV object for a given device property."""
        return self._pvs[propty]

    def pv_attribute_values(self, attribute):
        """Return property-value dict of a given attribute for all PVs."""
        attributes = dict()
        for propty in self._properties:
            pvobj = self._pvs[propty]
            attributes[pvobj.pvname] = getattr(pvobj, attribute)
        return attributes

    @property
    def hosts(self):
        """Return dict of IOC hosts providing device properties."""
        return self.pv_attribute_values('host')

    @property
    def values(self):
        """Return dict of property values."""
        return self.pv_attribute_values('value')

    def wait_for_connection(self, timeout=None):
        """Wait for connection."""
        for pvobj in self._pvs.values():
            res = pvobj.wait_for_connection(timeout)
            if not res:
                return False
        return True

    def __getitem__(self, propty):
        """Return value of property."""
        pvobj = self._pvs[propty]
        try:
            value = pvobj.get(timeout=Device.GET_TIMEOUT)
        except _ChannelAccessGetFailure:
            # This is raised in a Virtual Circuit Disconnect (192)
            # event. If the PV IOC goes down, for example.
            print('Could not get value of {}'.format(pvobj.pvname))
            value = None
        return value

    def __setitem__(self, propty, value):
        """Set value of property."""
        pvobj = self._pvs[propty]
        pvobj.value = value

    # --- private methods ---

    def _create_pvs(self, devname):
        if devname:
            devname = _SiriusPVName(devname)

        pvs = dict()
        for propty in self._properties:
            pvname = self._get_pvname(devname, propty)
            pvname = _VACA_PREFIX + pvname
            auto_monitor = not pvname.endswith('-Mon')
            in_sim = _Simulation.pv_check(pvname)
            pvclass = _PVSim if in_sim else _PV
            pvs[propty] = pvclass(
                pvname, auto_monitor=auto_monitor,
                connection_timeout=Device.CONNECTION_TIMEOUT)
        return devname, pvs

    def _wait(self, propty, value, timeout=10):
        """."""
        interval = 0.050  # [s]
        ntrials = int(timeout/interval)
        _time.sleep(4*interval)
        for _ in range(ntrials):
            if self[propty] == value:
                break
            _time.sleep(interval)

    def _get_pvname(self, devname, propty):
        if devname:
            func = devname.substitute
            pvname = func(propty=propty)
        else:
            pvname = propty
        return pvname


# NOTE: This class is temporary. It should become deprecated once all
# devices names are in accordance with Sirius naming system
class DeviceNC(Device):
    """Non-compliant Devices.

    This device class is to be used for those devices whose
    names and PVs are not compliant to the Sirius naming system.
    """

    def _create_pvs(self, devname):
        pvs = dict()
        devname = devname or ''
        for propty in self._properties:
            pvname = devname + ':' + propty
            auto_monitor = not pvname.endswith('-Mon')
            pvs[propty] = _PV(pvname, auto_monitor=auto_monitor)
        return devname, pvs


class DeviceApp(Device):
    """Application Device.

    This kind of device groups properties of other devices.
    """

    def __init__(self, properties, devname=None):
        """."""
        self._devname_app = devname

        # call base class constructor
        super().__init__(None, properties=properties)

    @property
    def devname(self):
        """Return application device name."""
        return self._devname_app


class Devices:
    """."""

    def __init__(self, devname, devices):
        """."""
        self._devname = devname
        self._devices = devices

        self._properties = []
        for dev in self._devices:
            if dev is not None:
                self._properties += dev.properties

    @property
    def devname(self):
        """Return device name."""
        return self._devname

    @property
    def properties(self):
        """Return device properties."""
        return self._properties

    @property
    def simulators(self):
        """Return list of simulators."""
        sims = set()
        for dev in self._devices:
            sims.update(dev.simulators)
        return sims

    @property
    def pvnames(self):
        """Return device PV names."""
        set_ = set()
        for dev in self._devices:
            set_.update(dev.pvnames)
        return set_

    @property
    def connected(self):
        """Return PVs connection status."""
        for dev in self._devices:
            if not dev.connected:
                return False
        return True

    @property
    def disconnected_pvnames(self):
        """Return list of disconnected device PVs."""
        set_ = set()
        for dev in self._devices:
            set_.update(dev.disconnected_pvnames)
        return set_

    def update(self):
        """Update device properties."""
        for dev in self._devices:
            dev.update()

    def pv_attribute_values(self, attribute):
        """Return property-value dict of a given attribute for all PVs."""
        attributes = dict()
        for dev in self._devices:
            attrs = dev.pv_attribute_values(attribute)
            attributes.update(attrs)
        return attributes

    @property
    def hosts(self):
        """Return dict of IOC hosts providing device properties."""
        return self.pv_attribute_values('host')

    @property
    def values(self):
        """Return dict of property values."""
        return self.pv_attribute_values('value')

    @property
    def devices(self):
        """Return devices."""
        return self._devices

    def __getitem__(self, devidx):
        """Return device."""
        return self._devices[devidx]

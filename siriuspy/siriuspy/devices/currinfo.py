"""."""
from .device import Device as _Device
from .device import Devices as _Devices
from .ict import ICT


class CurrInfoTranspEff(_Device):
    """."""

    class DEVICES:
        """Devices names."""

        LI = 'LI-Glob:AP-CurrInfo'
        TB = 'TB-Glob:AP-CurrInfo'
        TS = 'TS-Glob:AP-CurrInfo'
        ALL = (LI, TB, TS, )

    _properties = ('TranspEff-Mon', )

    def __init__(self, devname):
        """."""
        # check if device exists
        if devname not in CurrInfoTranspEff.DEVICES.ALL:
            raise NotImplementedError(devname)

        # call base class constructor
        super().__init__(devname, properties=CurrInfoTranspEff._properties)

    @property
    def transpeff(self):
        """."""
        return self['TranspEff-Mon']


class CurrInfoLinear(_Devices):
    """."""

    class DEVICES:
        """Devices names."""

        LI = CurrInfoTranspEff.DEVICES.LI
        TB = CurrInfoTranspEff.DEVICES.TB
        TS = CurrInfoTranspEff.DEVICES.TS
        ALL = (LI, TB, TS, )

    def __init__(self, devname):
        """."""
        # check if device exists
        if devname not in CurrInfoLinear.DEVICES.ALL:
            raise NotImplementedError(devname)

        if devname == CurrInfoLinear.DEVICES.LI:
            transp = CurrInfoTranspEff(CurrInfoLinear.DEVICES.LI)
            ict1 = ICT(ICT.DEVICES.LI_1)
            ict2 = ICT(ICT.DEVICES.LI_2)
        elif devname == CurrInfoLinear.DEVICES.TB:
            transp = CurrInfoTranspEff(CurrInfoLinear.DEVICES.TB)
            ict1 = ICT(ICT.DEVICES.TB_02)
            ict2 = ICT(ICT.DEVICES.TB_04)
        elif devname == CurrInfoLinear.DEVICES.TS:
            transp = CurrInfoTranspEff(CurrInfoLinear.DEVICES.TS)
            ict1 = ICT(ICT.DEVICES.TS_01)
            ict2 = ICT(ICT.DEVICES.TS_04)

        devices = (
            transp, ict1, ict2,
        )

        # call base class constructor
        super().__init__(devname, devices)

    @property
    def transpeff(self):
        """."""
        return self.devices[0].transpeff

    @property
    def charge_ict1(self):
        """."""
        return self.devices[1].charge

    @property
    def charge_ict2(self):
        """."""
        return self.devices[2].charge

    @property
    def charge_avg_ict1(self):
        """."""
        return self.devices[1].charge_avg

    @property
    def charge_avg_ict2(self):
        """."""
        return self.devices[2].charge_avg

    @property
    def charge_max_ict1(self):
        """."""
        return self.devices[1].charge_max

    @property
    def charge_max_ict2(self):
        """."""
        return self.devices[2].charge_max

    @property
    def charge_min_ict1(self):
        """."""
        return self.devices[1].charge_min

    @property
    def charge_min_ict2(self):
        """."""
        return self.devices[2].charge_min

    @property
    def charge_std_ict1(self):
        """."""
        return self.devices[1].charge_std

    @property
    def charge_std_ict2(self):
        """."""
        return self.devices[2].charge_std

    @property
    def pulse_count_ict1(self):
        """."""
        return self.devices[1].pulse_count

    @property
    def pulse_count_ict2(self):
        """."""
        return self.devices[2].pulse_count


class CurrInfoBO(_Device):
    """."""

    DEVNAME = 'BO-Glob:AP-CurrInfo'

    _properties = (
        'Charge150MeV-Mon', 'Current150MeV-Mon',
        'Charge1GeV-Mon', 'Current1GeV-Mon',
        'Charge2GeV-Mon', 'Current2GeV-Mon',
        'Charge3GeV-Mon', 'Current3GeV-Mon',
        'IntCurrent3GeV-Mon', 'RampEff-Mon',
    )

    def __init__(self):
        """."""
        # call base class constructor
        super().__init__(CurrInfoBO.DEVNAME, properties=CurrInfoBO._properties)

    @property
    def charge150mev(self):
        """."""
        return self['Charge150MeV-Mon']

    @property
    def current150mev(self):
        """."""
        return self['Current150MeV-Mon']

    @property
    def charge1gev(self):
        """."""
        return self['Charge1GeV-Mon']

    @property
    def current1gev(self):
        """."""
        return self['Current1GeV-Mon']

    @property
    def charge2gev(self):
        """."""
        return self['Charge2GeV-Mon']

    @property
    def current2gev(self):
        """."""
        return self['Current2GeV-Mon']

    @property
    def charge3gev(self):
        """."""
        return self['Charge3GeV-Mon']

    @property
    def current3gev(self):
        """."""
        return self['Current3GeV-Mon']

    @property
    def intcurrent3gev(self):
        """."""
        return self['IntCurrent3GeV-Mon']

    @property
    def rampeff(self):
        """."""
        return self['RampEff-Mon']


class CurrInfoSI(_Device):
    """."""

    DEVNAME = 'SI-Glob:AP-CurrInfo'

    _properties = (
        'Charge-Mon', 'Current-Mon',
        'InjEff-Mon', 'Lifetime-Mon', 'LifetimeBPM-Mon',
        'StoredEBeam-Mon',
    )

    def __init__(self):
        """."""
        # call base class constructor
        super().__init__(CurrInfoSI.DEVNAME, properties=CurrInfoSI._properties)

    @property
    def charge(self):
        """."""
        return self['Charge-Mon']

    @property
    def current(self):
        """."""
        return self['Current-Mon']

    @property
    def injeff(self):
        """."""
        return self['InjEff-Mon']

    @property
    def lifetime(self):
        """."""
        return self['Lifetime-Mon']

    @property
    def lifetimebpm(self):
        """."""
        return self['LifetimeBPM-Mon']

    @property
    def storedbeam(self):
        """."""
        return self['StoredEBeam-Mon']


class CurrInfoAS(_Devices):
    """."""

    class DEVICES:
        """Devices names."""

        LI = CurrInfoLinear.DEVICES.LI
        TB = CurrInfoLinear.DEVICES.TB
        BO = CurrInfoBO.DEVNAME
        TS = CurrInfoLinear.DEVICES.TS
        SI = CurrInfoSI.DEVNAME
        ALL = (LI, TB, BO, TS, SI, )

    def __init__(self):
        """."""
        currinfo_li = CurrInfoLinear(CurrInfoLinear.DEVICES.LI)
        currinfo_tb = CurrInfoLinear(CurrInfoLinear.DEVICES.TB)
        currinfo_bo = CurrInfoBO()
        currinfo_ts = CurrInfoLinear(CurrInfoLinear.DEVICES.TS)
        currinfo_si = CurrInfoSI()

        devices = (
            currinfo_li, currinfo_tb, currinfo_bo,
            currinfo_ts, currinfo_si
        )

        # call base class constructor
        super().__init__('', devices)

    @property
    def li(self):
        """Return LI CurrInfo device."""
        return self.devices[0]

    @property
    def tb(self):
        """Return TB CurrInfo device."""
        return self.devices[1]

    @property
    def bo(self):
        """Return BO CurrInfo device."""
        return self.devices[2]

    @property
    def ts(self):
        """Return TS CurrInfo device."""
        return self.devices[3]

    @property
    def si(self):
        """Return SI CurrInfo device."""
        return self.devices[4]

"""."""

from .device import Device as _Device


class ICT(_Device):
    """ICT Device."""

    class DEVICES:
        """Devices names."""

        LI_1 = 'LI-01:DI-ICT-1'
        LI_2 = 'LI-01:DI-ICT-2'
        TB_02 = 'TB-02:DI-ICT'
        TB_04 = 'TB-04:DI-ICT'
        TS_01 = 'TS-01:DI-ICT'
        TS_04 = 'TS-04:DI-ICT'
        ALL = (LI_1, LI_2, TB_02, TB_04, TS_01, TS_04, )

    _properties = (
        'Charge-Mon', 'ChargeAvg-Mon', 'ChargeMax-Mon',
        'ChargeMin-Mon', 'ChargeStd-Mon', 'PulseCount-Mon')

    def __init__(self, devname):
        """."""
        # check if device exists
        if devname not in ICT.DEVICES.ALL:
            raise NotImplementedError(devname)

        # call base class constructor
        super().__init__(devname, properties=ICT._properties)

    @property
    def charge(self):
        """."""
        return self['Charge-Mon']

    @property
    def charge_avg(self):
        """."""
        return self['ChargeAvg-Mon']

    @property
    def charge_max(self):
        """."""
        return self['ChargeMax-Mon']

    @property
    def charge_min(self):
        """."""
        return self['ChargeMin-Mon']

    @property
    def charge_std(self):
        """."""
        return self['ChargeStd-Mon']

    @property
    def pulse_count(self):
        """."""
        return self['PulseCount-Mon']


class TranspEff(_Device):
    """Linac Transport Efficiency Device."""

    class DEVICES:
        """Devices names."""

        LI = 'LI-Glob:AP-TranspEff'
        ALL = (LI, )

    _properties_li = ('Eff-Mon', 'EffAvg-Mon', )

    _properties = {
        DEVICES.LI: _properties_li}

    def __init__(self, devname):
        """."""
        # check if device exists
        if devname not in TranspEff.DEVICES.ALL:
            raise NotImplementedError(devname)

        # call base class constructor
        super().__init__(devname, properties=TranspEff._properties[devname])

    @property
    def efficiency(self):
        """."""
        return self['Eff-Mon']

    @property
    def efficiency_avg(self):
        """."""
        return self['EffAvg-Mon']

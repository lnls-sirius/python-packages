"""."""

from .device import Device as _Device


class Screen(_Device):
    """."""

    class DEVICES:
        """Devices names."""

        TB_1 = 'TB-01:DI-Scrn-1'
        TB_2 = 'TB-01:DI-Scrn-2'
        TB_3 = 'TB-02:DI-Scrn-1'
        TB_4 = 'TB-02:DI-Scrn-2'
        TB_5 = 'TB-03:DI-Scrn'
        TB_6 = 'TB-04:DI-Scrn'
        BO_1 = 'BO-01D:DI-Scrn-1'
        BO_2 = 'BO-01D:DI-Scrn-2'
        BO_3 = 'BO-02U:DI-Scrn'
        TS_1 = 'TS-01:DI-Scrn'
        TS_2 = 'TS-02:DI-Scrn'
        TS_3 = 'TS-03:DI-Scrn'
        TS_4 = 'TS-04:DI-Scrn-1'
        TS_5 = 'TS-04:DI-Scrn-2'
        TS_6 = 'TS-04:DI-Scrn-3'
        TB = (TB_1, TB_2, TB_3, TB_4, TB_5, TB_6)
        TS = (TS_1, TS_2, TS_3, TS_4, TS_5, TS_6)
        BO = (BO_1, BO_2, BO_3)
        ALL = (
            TB_1, TB_2, TB_3, TB_4, TB_5, TB_6,
            BO_1, BO_2, BO_3,
            TS_1, TS_2, TS_3, TS_4, TS_5, TS_6)

    _properties = (
        'ImgData-Mon',
        'CenterXDimFei-Mon', 'CenterYDimFei-Mon',
        'SigmaXDimFei-Mon', 'SigmaYDimFei-Mon',
        'ThetaDimFei-Mon',
    )

    def __init__(self, devname):
        """."""
        # check if device exists
        if devname not in Screen.DEVICES.ALL:
            raise NotImplementedError(devname)

        # call base class constructor
        super().__init__(devname, properties=Screen._properties)

    @property
    def image(self):
        """."""
        return self['ImgData-Mon']

    @property
    def centerx(self):
        """."""
        return self['CenterXDimFei-Mon']

    @property
    def centery(self):
        """."""
        return self['CenterYDimFei-Mon']

    @property
    def sigmax(self):
        """."""
        return self['SigmaXDimFei-Mon']

    @property
    def sigmay(self):
        """."""
        return self['SigmaYDimFei-Mon']

    @property
    def angle(self):
        """."""
        return self['ThetaDimFei-Mon']

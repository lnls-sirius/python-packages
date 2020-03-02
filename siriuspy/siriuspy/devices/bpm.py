#!/usr/bin/env python-sirius
"""."""

from .device import Device as _Device


class BPM(_Device):
    """."""

    _properties = (
        'SP_AArrayData', 'SP_BArrayData', 'SP_CArrayData', 'SP_DArrayData',
        'SPPosX-Mon', 'SPPosY-Mon', 'SPSum-Mon')

    def __init__(self, devname):
        """."""
        # call base class constructor
        super().__init__(devname, properties=BPM._properties)

    @property
    def sp_anta(self):
        """."""
        return self.get('SP_AArrayData')

    @property
    def sp_antb(self):
        """."""
        return self.get('SP_BArrayData')

    @property
    def sp_antc(self):
        """."""
        return self.get('SP_CArrayData')

    @property
    def sp_antd(self):
        """."""
        return self.get('SP_DArrayData')

    @property
    def spposx(self):
        """."""
        return self.get('SPPosX-Mon')

    @property
    def spposy(self):
        """."""
        return self.get('SPPosY-Mon')

    @property
    def spsum(self):
        """."""
        return self.get('SPSum-Mon')
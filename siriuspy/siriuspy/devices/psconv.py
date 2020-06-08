"""Define Power Supply Property and Strength Devices."""

from ..namesys import SiriusPVName as _SiriusPVName
from ..magnet.factory import NormalizerFactory as _NormalizerFactory

from .device import Devices as _Devices
from .syncd import DevicesSync as _DevicesSync


class PSProperty(_DevicesSync):
    """Power Supply Epics Connector."""

    _ps2devs = {
        # devices which are mapped to more than one device
        'BO-Fam:PS-B-1': ('BO-Fam:PS-B-1', 'BO-Fam:PS-B-2'),
        'BO-Fam:PS-B-2': ('BO-Fam:PS-B-1', 'BO-Fam:PS-B-2'),
        'SI-Fam:PS-B1B2-1': ('SI-Fam:PS-B1B2-1', 'SI-Fam:PS-B1B2-2'),
        'SI-Fam:PS-B1B2-2': ('SI-Fam:PS-B1B2-1', 'SI-Fam:PS-B1B2-2'),
        }

    def __init__(self, devname, propty, auto_mon=False):
        """."""
        devname = _SiriusPVName(devname)

        # get devnames
        devnames = PSProperty._get_devnames(devname)

        # call base class constructor
        super().__init__(
            devnames=devnames, propty_sync=[propty], auto_mon=auto_mon)

    @property
    def property_sync(self):
        """Return sole synchonized property name of device."""
        return self.properties_sync[0]

    @property
    def value(self):
        """Return property value."""
        return self.value_get(self.property_sync)

    @value.setter
    def value(self, current):
        """Set property value."""
        self.value_set(self.property_sync, current)

    @property
    def limits(self):
        """Return Property limits."""
        # NOTE: improve code.
        try:
            pvname = self.pvnames[0]
        except TypeError:
            # is a set
            for pvn in self.pvnames:
                if pvn.endswith('-SP'):
                    pvname = pvn
        pvobj = self.pv_object(pvname)
        limits = (
            pvobj.lower_alarm_limit,
            pvobj.lower_warning_limit,
            pvobj.lower_disp_limit,
            pvobj.upper_disp_limit,
            pvobj.upper_warning_limit,
            pvobj.upper_alarm_limit)
        return limits

    @staticmethod
    def _get_devnames(devname):
        """."""
        if devname in PSProperty._ps2devs:
            return PSProperty._ps2devs[devname]
        return (devname, )


class StrengthConv(_Devices):
    """Strength Converter."""

    # TODO: Test changing default value of auto_mon to see if conversion
    # IOCs are improved.

    def __init__(self, devname, proptype, auto_mon=False):
        """."""
        devname = _SiriusPVName(devname)

        # get pwrsupply normalized
        self._norm_mag = self._create_normalizer(devname)

        # get devices that provide normalization current for strengths
        self._dev_dip, self._dev_fam = \
            self._get_devices(devname, proptype, auto_mon)
        if self._dev_fam:
            devices = (self._dev_dip, self._dev_fam)
        elif self._dev_dip:
            devices = (self._dev_dip, )
        else:
            devices = ()

        # call base class constructor
        super().__init__(devname, devices)

    @property
    def dipole_strength(self):
        """Return dipole strength."""
        if self._dev_dip:
            return self._dev_dip.value
        return None

    @property
    def family_strength(self):
        """Return family strength."""
        if self._dev_fam:
            return self._dev_fam.value
        return None

    def conv_current_2_strength(
            self, currents,
            strengths_dipole=None, strengths_family=None):
        """Convert currents to strengths."""
        norm = self._norm_mag
        kwargs = self._get_kwargs(strengths_dipole, strengths_family)
        if kwargs is None:
            return None
        strengths = \
            norm.conv_current_2_strength(currents=currents, **kwargs)
        return strengths

    def conv_strength_2_current(self, strengths,
                                strengths_dipole=None,
                                strengths_family=None):
        """Convert strengths to currents."""
        norm = self._norm_mag
        kwargs = self._get_kwargs(strengths_dipole, strengths_family)
        if kwargs is None:
            return None
        currents = \
            norm.conv_strength_2_current(strengths=strengths, **kwargs)
        return currents

    def _get_kwargs(self,
                    strengths_dipole=None,
                    strengths_family=None):
        if not self._dev_dip:
            # is a dipole
            kwargs = dict()
            return kwargs
        if not self._dev_fam:
            # is not a trim
            if strengths_dipole is None:
                strengths_dipole = self._dev_dip.value
                if strengths_dipole is None:
                    return None
            kwargs = {'strengths_dipole': strengths_dipole}
            return kwargs
        # is a trim
        if strengths_dipole is None:
            strengths_dipole = self._dev_dip.value
            if strengths_dipole is None:
                return None
        if strengths_family is None:
            strengths_family = self._dev_fam.value
            if strengths_family is None:
                return None
        kwargs = {
            'strengths_dipole': strengths_dipole,
            'strengths_family': strengths_family}
        return kwargs

    @staticmethod
    def _create_normalizer(psname):
        if psname.sec == 'TB' and psname.dev == 'B':
            norm_mag = _NormalizerFactory.create('TB-Fam:MA-B')
        elif psname.sec == 'BO' and psname.dev == 'B':
            norm_mag = _NormalizerFactory.create('BO-Fam:MA-B')
        elif psname.sec == 'TS' and psname.dev == 'B':
            norm_mag = _NormalizerFactory.create('TS-Fam:MA-B')
        elif psname.sec == 'SI' and psname.dev == 'B1B2':
            norm_mag = _NormalizerFactory.create('SI-Fam:MA-B1B2')
        else:
            maname = psname.replace(':PS', ':MA').replace(':PU', ':PM')
            norm_mag = _NormalizerFactory.create(maname)
        return norm_mag

    @staticmethod
    def _get_devices(devname, proptype, auto_mon):
        # is dipole?
        if StrengthConv._get_dev_if_dipole(devname):
            return None, None

        # is insertion device?
        if StrengthConv._get_dev_if_id(devname):
            return None, None

        # is trim?
        status, dev_dip, dev_fam = \
            StrengthConv._get_dev_if_trim(devname, proptype, auto_mon)
        if status:
            return dev_dip, dev_fam

        # is booster ps?
        status, dev_dip = StrengthConv._get_dev_if_booster(
            devname, proptype, auto_mon)
        if status:
            return dev_dip, None

        # is others
        return StrengthConv._get_dev_others(devname, proptype, auto_mon), None

    @staticmethod
    def _get_dev_if_dipole(devname):
        if devname.dev in {'B', 'B1B2'}:
            # dipoles need no connectors
            return True
        return False

    @staticmethod
    def _get_dev_if_id(devname):
        if devname.dis == 'ID':
            # insertion devices need no connectors
            return True
        return False

    @staticmethod
    def _get_dev_if_trim(devname, proptype, auto_mon):
        if StrengthConv._is_trim(devname):
            # trims need dipole and family connectors
            dev_dip = PSProperty(
                'SI-Fam:PS-B1B2-1', 'Energy' + proptype, auto_mon)
            devname = devname.substitute(sub='Fam')
            dev_fam = PSProperty(devname, 'KL' + proptype, auto_mon)
            return True, dev_dip, dev_fam
        return False, None, None

    @staticmethod
    def _get_dev_if_booster(devname, proptype, auto_mon):
        if devname.startswith('BO'):
            if devname.dev == 'InjKckr':
                # BO injection kicker uses TB dipole normalizer
                dev_dip = PSProperty(
                    'TB-Fam:PS-B', 'Energy' + proptype, auto_mon)
            elif devname.dev == 'EjeKckr':
                # BO ejection kicker uses TS dipole normalizer
                dev_dip = PSProperty(
                    'TS-Fam:PS-B', 'Energy' + proptype, auto_mon)
            else:
                # other BO ps use BO dipoles as normalizer
                dev_dip = PSProperty(
                    'BO-Fam:PS-B-1', 'Energy' + proptype, auto_mon)
            return True, dev_dip
        return False, None

    @staticmethod
    def _get_dev_others(devname, proptype, auto_mon):
        if devname.startswith('LI'):
            return PSProperty('TB-Fam:PS-B', 'Energy' + proptype, auto_mon)
        if devname.startswith('TB'):
            # all TB ps other than dipoles need dipole connectors
            return PSProperty('TB-Fam:PS-B', 'Energy' + proptype, auto_mon)
        elif devname.startswith('TS'):
            # all TS ps use TS dipole
            return PSProperty('TS-Fam:PS-B', 'Energy' + proptype, auto_mon)
        elif devname.startswith('SI'):
            if devname.dev in {'InjDpKckr', 'InjNLKckr'}:
                # SI injection ps use TS dipole
                return PSProperty('TS-Fam:PS-B', 'Energy' + proptype, auto_mon)
            else:
                # other SI ps use SI dipole
                return PSProperty(
                    'SI-Fam:PS-B1B2-1', 'Energy' + proptype, auto_mon)
        return None

    @staticmethod
    def _is_trim(psname):
        check = (psname.sec == 'SI')
        check &= (psname.sub != 'Fam')
        check &= 'QS' not in psname.dev
        check &= 'Q' in psname.dev
        return check

"""."""
import numpy as _np

from ..search import PSSearch as _PSSearch
from ..namesys import SiriusPVName as _SiriusPVName

from . import Device as _Device
from . import Devices as _Devices
from . psconv import StrengthConv as _StrengthConv


class PSNamesSOFB:
    """."""

    _sofb = dict()
    _sofb_factory = None

    @staticmethod
    def get_psnames_ch(acc):
        """Return horizontal corrector psnames of a given sector."""
        if PSNamesSOFB._sofb_factory is None:
            from ..sofb.csdev import SOFBFactory
            PSNamesSOFB._sofb_factory = SOFBFactory
        if acc not in PSNamesSOFB._sofb:
            PSNamesSOFB._sofb[acc] = PSNamesSOFB._sofb_factory.create(acc)
        return PSNamesSOFB._sofb[acc].ch_names

    @staticmethod
    def get_psnames_cv(acc):
        """Return vertical corrector psnames of a given sector."""
        if PSNamesSOFB._sofb_factory is None:
            from ..sofb.csdev import SOFBFactory
            PSNamesSOFB._sofb_factory = SOFBFactory
        if acc not in PSNamesSOFB._sofb:
            PSNamesSOFB._sofb[acc] = PSNamesSOFB._sofb_factory.create(acc)
        return PSNamesSOFB._sofb[acc].cv_names


class PSCorrSOFB(_Device):
    """SOFB corrector device.

    Group SOFB setpoints of all corrector power supplies belonging to
    the same BeagleBone.
    """

    _curr_sp = 'SOFBCurrent-SP'
    _curr_rb = 'SOFBCurrent-RB'
    _curr_refmon = 'SOFBCurrentRef-Mon'
    _curr_mon = 'SOFBCurrent-Mon'

    _properties = (
        _curr_sp,
        _curr_rb,
        _curr_refmon,
        _curr_mon)

    def __init__(self, devname, auto_mon=False):
        """."""
        self._devname_orig = _SiriusPVName(devname)
        self._sec = self._devname_orig.sec

        # check if device exists and is a SOFB corrector
        if devname not in PSNamesSOFB.get_psnames_ch(self._sec) and \
                devname not in PSNamesSOFB.get_psnames_cv(self._sec):
            raise NotImplementedError(devname)

        # get bbbname and linked bsmp devices
        self._bbbname = _PSSearch.conv_psname_2_bbbname(devname)
        self._bsmpdevs = _PSSearch.conv_bbbname_2_bsmps(self._bbbname)

        # call base class constructor
        devname = self._bsmpdevs[0][0]
        super().__init__(
            devname, properties=PSCorrSOFB._properties, auto_mon=auto_mon)

        # get sofb indices
        self._sofb_indices, self._idx_corr = self._get_sofb_indices()

    @property
    def devname(self):
        """Device name."""
        return self._devname_orig

    @property
    def devname_first_udc(self):
        """Device name of first UDC power supply."""
        return self._bsmpdevs[0][0]

    @property
    def bbbname(self):
        """BBB name."""
        return self._bbbname

    @property
    def bsmpdevs(self):
        """BSMP devices."""
        return self._bsmpdevs

    @property
    def sofb_indices(self):
        """Return indices of devices in SOFB current vector."""
        return self._sofb_indices

    @property
    def current(self):
        """Return current Ref-Mon in SOFB order."""
        # get refmon
        values = self[self._curr_refmon]

        # trim values
        values = _np.asarray(values)
        values = values[self._idx_corr]
        return values

    @current.setter
    def current(self, value):
        """Set current -SP in SOFB order."""
        # trim set value
        value = _np.asarray(value)
        idx_val = _np.where(~_np.isnan(value))[0]

        # combine refmon and  setpoint values
        values = self[self._curr_sp]
        idx_pv = self._idx_corr[idx_val]
        values[idx_pv] = value[idx_val]

        # set new values
        self[self._curr_sp] = values

    @property
    def current_sp(self):
        """Return current -SP in SOFB order."""
        # get setpoints
        values = self[self._curr_sp]

        # trim values
        values = _np.asarray(values)
        values = values[self._idx_corr]
        return values

    @property
    def current_rb(self):
        """Return current -RB in SOFB order."""
        # get rb
        values = self[self._curr_rb]

        # trim values
        values = _np.asarray(values)
        values = values[self._idx_corr]
        return values

    @property
    def current_mon(self):
        """Return current -Mon in SOFB order."""
        # get mon
        values = self[self._curr_mon]

        # trim values
        values = _np.asarray(values)
        values = values[self._idx_corr]
        return values

    # --- private methods ---

    def _get_sofb_indices(self):
        devids = sorted([dev[1] for dev in self._bsmpdevs])
        psnames = PSNamesSOFB.get_psnames_ch(self._sec) + \
            PSNamesSOFB.get_psnames_cv(self._sec)
        indices = list()
        idx_corr = list()
        for devname, dev_id in self._bsmpdevs:
            if devname in psnames:
                idx_id = devids.index(dev_id)
                idx_ps = psnames.index(devname)
                idx_corr.append(idx_id)
                indices.append(idx_ps)
        indices = _np.asarray(indices)
        idx_corr = _np.asarray(idx_corr)
        return indices, idx_corr


class PSApplySOFB(_Devices):
    """SOFB corrector devices.

    Group SOFB setpoints of all corrector power supplies.
    """

    _dipole_propty = 'Ref-Mon'

    class DEVICES:
        """."""

        BO = 'BO'
        SI = 'SI'
        ALL = (BO, SI)

    def __init__(self, devname, auto_mon=False):
        """."""
        # check if device exists
        if devname not in PSApplySOFB.DEVICES.ALL:
            raise NotImplementedError(devname)

        # get devices
        devices = PSApplySOFB._get_pscorrsofb_devices(devname, auto_mon)

        # strengthconv dictionaries
        self._pstype_2_index, self._pstype_2_sconv = \
            self._get_strenconv(devname, auto_mon)

        # add StrengthConv devices
        devices += self._pstype_2_sconv.values()

        # call base class constructor
        super().__init__(devname, devices=devices)

        # number of correctors
        self._nr_chs = len(self.psnames_ch)
        self._nr_cvs = len(self.psnames_cv)

    @property
    def psnames_ch(self):
        """."""
        return PSNamesSOFB.get_psnames_ch(self.devname)

    @property
    def psnames_cv(self):
        """."""
        return PSNamesSOFB.get_psnames_cv(self.devname)

    @property
    def nr_correctors(self):
        """Return number of correctors."""
        return len(self.psnames_ch) + len(self.psnames_cv)

    @property
    def indices_ch(self):
        """Return selection indices for horizontal correctors."""
        return _np.arange(len(self.psnames_ch))

    @property
    def indices_cv(self):
        """Return selection indices for vertical correctors."""
        return _np.arange(len(self.psnames_ch), self.nr_correctors)

    @property
    def current(self):
        """Return CurrentRef-Mon vector in SOFB order."""
        currents = self._get_current('current')
        return currents

    @current.setter
    def current(self, value):
        """Set Current-SP vector in SOFB order."""
        value = _np.asarray(value)
        for corr in self.devices:
            if isinstance(corr, PSCorrSOFB):
                inds = corr.sofb_indices
                current = value[inds]
                corr.current = current

    @property
    def current_sp(self):
        """Return Current-SP vector in SOFB order."""
        currents = self._get_current('current_sp')
        return currents

    @property
    def current_rb(self):
        """Return Current-RB vector in SOFB order."""
        currents = self._get_current('current_rb')
        return currents

    @property
    def current_mon(self):
        """Return Current-Mon vector in SOFB order."""
        currents = self._get_current('current_mon')
        return currents

    @property
    def kick(self):
        """Return correctors Ref-Mon kicks in SOFB order."""
        current = self.current
        strength = self._conv_curr2stren(current)
        return strength

    @kick.setter
    def kick(self, value):
        """Set correctors -SP kicks in SOFB order."""
        current = self._conv_stren2curr(value)
        self.current = current

    @property
    def kick_sp(self):
        """Return correctors -SP kicks in SOFB order."""
        current = self.current_sp
        strength = self._conv_curr2stren(current)
        return strength

    @property
    def kick_rb(self):
        """Return correctors -RB kicks in SOFB order."""
        current = self.current_rb
        strength = self._conv_curr2stren(current)
        return strength

    @property
    def kick_mon(self):
        """Return correctors -Mon kicks in SOFB order."""
        current = self.current_mon
        strength = self._conv_curr2stren(current)
        return strength

    # --- private methods ---

    def _get_current(self, propty):
        values = _np.zeros(self._nr_chs + self._nr_cvs)
        for corr in self.devices:
            if isinstance(corr, PSCorrSOFB):
                inds = corr.sofb_indices
                vals = getattr(corr, propty)
                values[inds] = vals
        return values

    def _conv_curr2stren(self, current):
        strength = _np.zeros(len(current))
        for pstype, index in self._pstype_2_index.items():
            sconv = self._pstype_2_sconv[pstype]
            value = current[index]
            stren = sconv.conv_current_2_strength(currents=value)
            strength[index] = stren
        return strength

    def _conv_stren2curr(self, strength):
        current = _np.full(len(strength), _np.nan, dtype=float)
        for pstype, index in self._pstype_2_index.items():
            sconv = self._pstype_2_sconv[pstype]
            value = strength[index]
            idcs = ~_np.isnan(value)
            curr = sconv.conv_strength_2_current(strengths=value[idcs])
            current[index[idcs]] = curr
        return current

    @staticmethod
    def _get_pscorrsofb_devices(devname, auto_mon):
        psnames = PSNamesSOFB.get_psnames_ch(devname) + \
            PSNamesSOFB.get_psnames_cv(devname)
        devices = dict()
        all_devices = list()
        for psname in psnames:
            if psname in all_devices:
                continue
            sofb_corr = PSCorrSOFB(psname, auto_mon)
            all_devices += [dev[0] for dev in sofb_corr.bsmpdevs]
            devname = sofb_corr.devname_first_udc
            if devname not in devices:
                devices[devname] = sofb_corr
        return list(devices.values())

    def _get_strenconv(self, devname, auto_mon):
        # 1. create pstype to StrengthConv dictionary.
        # 2. create pstype to corrector index dictionnary.
        pstype_2_index = dict()
        pstype_2_sconv = dict()
        psnames = PSNamesSOFB.get_psnames_ch(devname) + \
            PSNamesSOFB.get_psnames_cv(devname)
        for i, psname in enumerate(psnames):
            pstype = _PSSearch.conv_psname_2_pstype(psname)
            if pstype not in pstype_2_index:
                pstype_2_index[pstype] = []
            pstype_2_index[pstype].append(i)
            if pstype not in pstype_2_sconv:
                sconv = _StrengthConv(
                    psname, PSApplySOFB._dipole_propty, auto_mon)
                pstype_2_sconv[pstype] = sconv

        # convert index to numpy array
        for pstype in pstype_2_index:
            pstype_2_index[pstype] = _np.asarray(pstype_2_index[pstype])

        return pstype_2_index, pstype_2_sconv

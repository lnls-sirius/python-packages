"""."""
import numpy as _np

from ..search import PSSearch as _PSSearch
from ..namesys import SiriusPVName as _SiriusPVName

from . import Device as _Device
from . import Devices as _Devices
from . psconv import StrengthConv as _StrengthConv


class PSCorrSOFB(_Device):
    """SOFB corrector device.

    Group SOFB setpoints of all corrector power supplies in a BeagleBone.
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

    def __init__(self,
                 devname, psnames_ch=None, psnames_cv=None):
        """."""
        self._devname_orig = _SiriusPVName(devname)

        # check if device exists
        filt = {'sec': '(TB|BO|TS|SI)', 'dis': 'PS', 'dev': '(CH|CV)'}
        if devname not in _PSSearch.get_psnames(filt):
            raise NotImplementedError(devname)

        # get bbbname and linked bsmp devices
        self._bbbname = _PSSearch.conv_psname_2_bbbname(devname)
        self._bsmpdevs = _PSSearch.conv_bbbname_2_bsmps(self._bbbname)

        # call base class constructor
        devname = self._bsmpdevs[0][0]
        super().__init__(
            devname, properties=PSCorrSOFB._properties)

        # get psnames and apply indices
        if psnames_ch is None or psnames_cv is None:
            self._psnames_ch, self._psnames_cv = \
                self._init_corr_names()
        else:
            self._psnames_ch, self._psnames_cv = psnames_ch, psnames_cv

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
    def psnames_ch(self):
        """."""
        return self._psnames_ch

    @property
    def psnames_cv(self):
        """."""
        return self._psnames_cv

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
        values = _np.array(values)
        values = values[self._idx_corr]
        return values

    @current.setter
    def current(self, value):
        """Set current -SP in SOFB order."""
        # trim set value
        value = _np.array(value)
        idx_val = _np.where((value == value) & _np.not_equal(value, None))[0]

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
        values = _np.array(values)
        values = values[self._idx_corr]
        return values

    @property
    def current_rb(self):
        """Return current -RB in SOFB order."""
        # get rb
        values = self[self._curr_rb]

        # trim values
        values = _np.array(values)
        values = values[self._idx_corr]
        return values

    @property
    def current_mon(self):
        """Return current -Mon in SOFB order."""
        # get mon
        values = self[self._curr_mon]

        # trim values
        values = _np.array(values)
        values = values[self._idx_corr]
        return values

    # --- private methods ---

    def _init_corr_names(self):
        # get accelerator sector, power supply names
        sec = self._devname.sec
        corrh = {'sec': sec, 'dis': 'PS', 'dev': 'CH'}
        corrv = {'sec': sec, 'dis': 'PS', 'dev': 'CV'}
        # update class consts CH_NAMES and CV_NAMES
        psnames_ch = \
            PSCorrSOFB._filter_id_correctors(_PSSearch.get_psnames(corrh))
        psnames_cv = \
            PSCorrSOFB._filter_id_correctors(_PSSearch.get_psnames(corrv))
        return psnames_ch, psnames_cv

    def _get_sofb_indices(self):
        devids = sorted([dev[1] for dev in self._bsmpdevs])
        psnames = self._psnames_ch + self._psnames_cv
        indices = list()
        idx_corr = list()
        for devname, dev_id in self._bsmpdevs:
            if devname in psnames:
                idx_id = devids.index(dev_id)
                idx_ps = psnames.index(devname)
                idx_corr.append(idx_id)
                indices.append(idx_ps)
        indices = _np.array(indices)
        idx_corr = _np.array(idx_corr)
        return indices, idx_corr

    @staticmethod
    def _filter_id_correctors(psnames):
        psnames_ = []
        for psname in psnames:
            if 'SA:PS-' not in psname and \
               'SB:PS-' not in psname and \
               'SP:PS-' not in psname:
                psnames_.append(psname)
        return tuple(psnames_)


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

    def __init__(self, devname):
        """."""
        # check if device exists
        if devname not in PSApplySOFB.DEVICES.ALL:
            raise NotImplementedError(devname)

        # get devices
        devices, self._psnames_ch, self._psnames_cv = \
            PSApplySOFB._get_pscorrsofb_devices(devname)

        # strengthconv dictionaries
        self._pstype_2_index, self._pstype_2_sconv = \
            self._get_strenconv()

        # add StrengthConv devices
        devices += self._pstype_2_sconv.values()

        # call base class constructor
        super().__init__(devname, devices=devices)

    @property
    def psnames_ch(self):
        """."""
        return self._psnames_ch

    @property
    def psnames_cv(self):
        """."""
        return self._psnames_cv

    @property
    def nr_correctors(self):
        """Return number of correctors."""
        return len(self._psnames_ch) + len(self._psnames_cv)

    @property
    def indices_ch(self):
        """Return selection indices for horizontal correctors."""
        return _np.arange(len(self._psnames_ch))

    @property
    def indices_cv(self):
        """Return selection indices for vertical correctors."""
        return _np.arange(len(self._psnames_ch), self.nr_correctors)

    @property
    def current(self):
        """Return CurrentRef-Mon vector in SOFB order."""
        currents = self._get_current('current')
        return currents

    @current.setter
    def current(self, value):
        """Set Current-SP vector in SOFB order."""
        value = _np.array(value)
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
        strength = self._get_kick(current)
        return strength

    @kick.setter
    def kick(self, value):
        """Set correctors -SP kicks in SOFB order."""

    @property
    def kick_sp(self):
        """Return correctors -SP kicks in SOFB order."""
        current = self.current_sp
        strength = self._get_kick(current)
        return strength

    @property
    def kick_rb(self):
        """Return correctors -RB kicks in SOFB order."""
        current = self.current_rb
        strength = self._get_kick(current)
        return strength

    @property
    def kick_mon(self):
        """Return correctors -Mon kicks in SOFB order."""
        current = self.current_mon
        strength = self._get_kick(current)
        return strength

    # --- private methods ---

    def _get_current(self, propty):
        values = _np.zeros(len(self._psnames_ch) + len(self._psnames_cv))
        for corr in self.devices:
            if isinstance(corr, PSCorrSOFB):
                inds = corr.sofb_indices
                vals = getattr(corr, propty)
                values[inds] = vals
        return values

    def _get_kick(self, current):
        strength = _np.zeros(len(current))
        for pstype, index in self._pstype_2_index.items():
            sconv = self._pstype_2_sconv[pstype]
            value = current[index]
            stren = sconv.conv_current_2_strength(currents=value)
            strength[index] = stren
        return strength

    @staticmethod
    def _get_pscorrsofb_devices(devname):
        # get ps names
        if devname == PSApplySOFB.DEVICES.SI:
            sec = 'SI'
        elif devname == PSApplySOFB.DEVICES.BO:
            sec = 'BO'
        filt = {'sec': sec, 'dis': 'PS', 'dev': '(CH|CV)'}
        psnames = _PSSearch.get_psnames(filt)
        devices = dict()
        psnames_ch, psnames_cv = None, None
        all_devices = list()
        for psname in psnames:
            if psname in all_devices:
                continue
            sofb_corr = PSCorrSOFB(psname, psnames_ch, psnames_cv)
            all_devices += [dev[0] for dev in sofb_corr.bsmpdevs]
            psnames_ch, psnames_cv = sofb_corr.psnames_ch, sofb_corr.psnames_cv
            devname = sofb_corr.devname_first_udc
            if devname not in devices:
                devices[devname] = sofb_corr
        return list(devices.values()), psnames_ch, psnames_cv

    def _get_strenconv(self):
        # 1. create pstype to StrengthConv dictionary.
        # 2. create pstype to corrector index dictionnary.
        pstype_2_index = dict()
        pstype_2_sconv = dict()
        for i, psname in enumerate(self._psnames_ch + self._psnames_cv):
            pstype = _PSSearch.conv_psname_2_pstype(psname)
            if pstype not in pstype_2_index:
                pstype_2_index[pstype] = []
            pstype_2_index[pstype].append(i)
            if pstype not in pstype_2_sconv:
                sconv = _StrengthConv(
                    psname, PSApplySOFB._dipole_propty)
                pstype_2_sconv[pstype] = sconv

        # convert index to numpy array
        for pstype in pstype_2_index:
            pstype_2_index[pstype] = _np.array(pstype_2_index[pstype])

        return pstype_2_index, pstype_2_sconv

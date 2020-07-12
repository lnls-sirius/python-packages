"""."""

import time as _time

from ..sofb.csdev import SOFBFactory
from .device import Device as _Device


class SOFB(_Device):
    """SOFB Device."""

    class DEVICES:
        """Devices names."""

        TB = 'TB-Glob:AP-SOFB'
        BO = 'BO-Glob:AP-SOFB'
        TS = 'TS-Glob:AP-SOFB'
        SI = 'SI-Glob:AP-SOFB'
        ALL = (TB, BO, TS, SI)

    _propty_tmpl = (
        'SOFBMode-Sel', 'SOFBMode-Sts',
        'KickCH-Mon', 'KickCV-Mon',
        'DeltaKickCH-Mon', 'DeltaKickCV-Mon',
        'DeltaKickCH-SP', 'DeltaKickCV-SP',
        'DeltaFactorCH-SP', 'DeltaFactorCV-SP',
        'DeltaFactorCH-RB', 'DeltaFactorCV-RB',
        'RefOrbX-SP', 'RefOrbY-SP',
        'RefOrbX-RB', 'RefOrbY-RB',
        'BPMXEnblList-SP', 'BPMYEnblList-SP',
        'BPMXEnblList-RB', 'BPMYEnblList-RB',
        'CHEnblList-SP', 'CVEnblList-SP',
        'CHEnblList-RB', 'CVEnblList-RB',
        'RFEnbl-Sel', 'RFEnbl-Sts',
        'CalcDelta-Cmd', 'ApplyDelta-Cmd', 'SmoothReset-Cmd',
        'SmoothNrPts-SP', 'SmoothNrPts-RB',
        'BufferCount-Mon',
        'TrigNrSamplesPost-SP',
        'TrigNrSamplesPost-RB',
        'ClosedLoop-Sts', 'ClosedLoop-Sel',
        'SPassSum-Mon', 'SPassOrbX-Mon', 'SPassOrbY-Mon',
        # properties used only for ring-type accelerators:
        'SlowOrbX-Mon', 'SlowOrbY-Mon',
        'MTurnSum-Mon', 'MTurnOrbX-Mon', 'MTurnOrbY-Mon',
        'MTurnIdxOrbX-Mon', 'MTurnIdxOrbY-Mon', 'MTurnIdxSum-Mon',
        'MTurnTime-Mon')

    _default_timeout = 10  # [s]
    _off, _on = 0, 1

    def __init__(self, devname):
        """."""
        # check if device exists
        if devname not in SOFB.DEVICES.ALL:
            raise NotImplementedError(devname)

        # SOFB object
        self.data = SOFBFactory.create(devname[:2])

        propts = SOFB._propty_tmpl
        if not self.data.isring:
            propts = [p for p in propts if not p.startswith(('MTurn', 'Slow'))]

        # call base class constructor
        super().__init__(devname, properties=propts)

    @property
    def opmode(self):
        """."""
        return self['SOFBMode-Sts']

    @opmode.setter
    def opmode(self, value):
        if value is None:
            return
        if isinstance(value, str) and value in self.data.SOFBMode._fields:
            self['SOFBMode-Sel'] = self.data.SOFBMode._fields.index(value)
        elif int(value) in self.data.SOFBMode:
            self['SOFBMode-Sel'] = int(value)

    @property
    def opmode_str(self):
        """."""
        return self.data.SOFBMode._fields[self['SOFBMode-Sts']]

    @property
    def sp_trajx(self):
        """."""
        return self['SPassOrbX-Mon']

    @property
    def sp_trajy(self):
        """."""
        return self['SPassOrbY-Mon']

    @property
    def sp_sum(self):
        """."""
        return self['SPassSum-Mon']

    @property
    def mt_trajx(self):
        """."""
        return self['MTurnOrbX-Mon'] if self.data.isring else None

    @property
    def mt_trajy(self):
        """."""
        return self['MTurnOrbY-Mon'] if self.data.isring else None

    @property
    def mt_sum(self):
        """."""
        return self['MTurnSum-Mon'] if self.data.isring else None

    @property
    def mt_time(self):
        """."""
        return self['MTurnTime-Mon'] if self.data.isring else None

    @property
    def mt_trajx_idx(self):
        """."""
        return self['MTurnIdxOrbX-Mon'] if self.data.isring else None

    @property
    def mt_trajy_idx(self):
        """."""
        return self['MTurnIdxOrbY-Mon'] if self.data.isring else None

    @property
    def mt_sum_idx(self):
        """."""
        return self['MTurnIdxSum-Mon'] if self.data.isring else None

    @property
    def trajx(self):
        """."""
        if self.data.isring and self.opmode == self.data.SOFBMode.MultiTurn:
            return self.mt_trajx_idx
        return self.sp_trajx

    @property
    def trajy(self):
        """."""
        if self.data.isring and self.opmode == self.data.SOFBMode.MultiTurn:
            return self.mt_trajy_idx
        return self.sp_trajy

    @property
    def sum(self):
        """."""
        if self.data.isring and self.opmode == self.data.SOFBMode.MultiTurn:
            return self.mt_sum_idx
        return self.sp_sum

    @property
    def orbx(self):
        """."""
        return self['SlowOrbX-Mon'] if self.data.isring else None

    @property
    def orby(self):
        """."""
        return self['SlowOrbY-Mon'] if self.data.isring else None

    @property
    def kickch(self):
        """."""
        return self['KickCH-Mon']

    @property
    def kickcv(self):
        """."""
        return self['KickCV-Mon']

    @property
    def deltakickch(self):
        """."""
        return self['DeltaKickCH-Mon']

    @deltakickch.setter
    def deltakickch(self, value):
        """."""
        self['DeltaKickCH-SP'] = value

    @property
    def deltakickcv(self):
        """."""
        return self['DeltaKickCV-Mon']

    @deltakickcv.setter
    def deltakickcv(self, value):
        """."""
        self['DeltaKickCV-SP'] = value

    @property
    def deltafactorch(self):
        """."""
        return self['DeltaFactorCH-RB']

    @deltafactorch.setter
    def deltafactorch(self, value):
        """."""
        self['DeltaFactorCH-SP'] = value

    @property
    def deltafactorcv(self):
        """."""
        return self['DeltaFactorCV-RB']

    @deltafactorcv.setter
    def deltafactorcv(self, value):
        """."""
        self['DeltaFactorCV-SP'] = value

    @property
    def refx(self):
        """."""
        return self['RefOrbX-RB']

    @refx.setter
    def refx(self, value):
        """."""
        self['RefOrbX-SP'] = value

    @property
    def refy(self):
        """."""
        return self['RefOrbY-RB']

    @refy.setter
    def refy(self, value):
        """."""
        self['RefOrbY-SP'] = value

    @property
    def bpmxenbl(self):
        """."""
        return self['BPMXEnblList-RB']

    @bpmxenbl.setter
    def bpmxenbl(self, value):
        """."""
        self['BPMXEnblList-SP'] = value

    @property
    def bpmyenbl(self):
        """."""
        return self['BPMYEnblList-RB']

    @bpmyenbl.setter
    def bpmyenbl(self, value):
        """."""
        self['BPMYEnblList-SP'] = value

    @property
    def chenbl(self):
        """."""
        return self['CHEnblList-RB']

    @chenbl.setter
    def chenbl(self, value):
        """."""
        self['CHEnblList-SP'] = value

    @property
    def cvenbl(self):
        """."""
        return self['CVEnblList-RB']

    @cvenbl.setter
    def cvenbl(self, value):
        """."""
        self['CVEnblList-SP'] = value

    @property
    def rfenbl(self):
        """."""
        dta = self.data
        return self['RFEnbl-Sts'] if dta.acc_idx == dta.Rings.SI else None

    @rfenbl.setter
    def rfenbl(self, value):
        """."""
        if self.data.acc_idx == self.data.Rings.SI:
            self['RFEnbl-Sel'] = value

    @property
    def buffer_count(self):
        """."""
        return self['BufferCount-Mon']

    @property
    def nr_points(self):
        """."""
        return self['SmoothNrPts-RB']

    @nr_points.setter
    def nr_points(self, value):
        """."""
        self['SmoothNrPts-SP'] = int(value)

    @property
    def trigsample(self):
        """."""
        return self['TrigNrSamplesPost-RB']

    @trigsample.setter
    def trigsample(self, value):
        """."""
        self['TrigNrSamplesPost-SP'] = int(value)

    def cmd_reset(self):
        """."""
        self['SmoothReset-Cmd'] = SOFB._on

    def cmd_calccorr(self):
        """."""
        self['CalcDelta-Cmd'] = SOFB._on

    def cmd_applycorr(self):
        """."""
        self['ApplyDelta-Cmd'] = self.data.ApplyDelta.CH
        _time.sleep(0.3)
        self['ApplyDelta-Cmd'] = self.data.ApplyDelta.CV

    @property
    def autocorrsts(self):
        """."""
        return self['ClosedLoop-Sts']

    def cmd_turn_on_autocorr(self, timeout=None):
        """."""
        timeout = timeout or SOFB._default_timeout
        self['ClosedLoop-Sel'] = SOFB._on
        self._wait(
            'ClosedLoop-Sts', SOFB._on, timeout=timeout)

    def cmd_turn_off_autocorr(self, timeout=None):
        """."""
        timeout = timeout or SOFB._default_timeout
        self['ClosedLoop-Sel'] = SOFB._off
        self._wait(
            'ClosedLoop-Sts', SOFB._off, timeout=timeout)

    def wait_buffer(self, timeout=None):
        """."""
        timeout = timeout or SOFB._default_timeout
        interval = 0.050  # [s]
        ntrials = int(timeout/interval)
        _time.sleep(10*interval)
        for _ in range(ntrials):
            if self.buffer_count >= self['SmoothNrPts-SP']:
                break
            _time.sleep(interval)
        else:
            print('WARN: Timed out waiting orbit.')

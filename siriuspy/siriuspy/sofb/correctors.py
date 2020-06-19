"""Module to deal with correctors."""

import time as _time
import logging as _log
import numpy as _np

from .. import util as _util
from ..epics import PV as _PV
from ..thread import RepeaterThread as _Repeat
from ..pwrsupply.csdev import Const as _PSConst
from ..timesys.csdev import Const as _TIConst
from ..search import HLTimeSearch as _HLTimesearch
from ..envars import VACA_PREFIX as LL_PREF
from ..namesys import SiriusPVName as _PVName
from ..devices import PSApplySOFB as _PSSOFB

from .base_class import BaseClass as _BaseClass, \
    BaseTimingConfig as _BaseTimingConfig, compare_kicks as _compare_kicks

TIMEOUT = 0.05


class Corrector(_BaseTimingConfig):
    """Corrector class."""

    def __init__(self, corr_name):
        """Init method."""
        super().__init__(corr_name[:2])
        self._name = _PVName(corr_name)
        self._sp = None
        self._rb = None

    @property
    def name(self):
        """Corrector name."""
        return self._name

    @property
    def connected(self):
        """Status connected."""
        conn = super().connected
        pvs = (self._sp, self._rb)
        for pv in pvs:
            if not pv.connected:
                _log.debug('NOT CONN: ' + pv.pvname)
            conn &= pv.connected
        return conn

    @property
    def opmode_ok(self):
        """Opmode ok status."""
        return self.connected

    @property
    def opmode(self):
        """Opmode."""
        return 1

    @opmode.setter
    def opmode(self, val):
        """."""

    @property
    def state(self):
        """State."""
        pv = self._config_pvs_rb['PwrState']
        return pv.value == _PSConst.PwrStateSel.On if pv.connected else False

    @state.setter
    def state(self, boo):
        """."""
        val = _PSConst.PwrStateSel.On if boo else _PSConst.PwrStateSel.Off
        pv = self._config_pvs_sp['PwrState']
        if pv.connected:
            self._config_ok_vals['PwrState'] = val
            pv.put(val, wait=False)

    @property
    def value(self):
        """Value."""
        if self._rb.connected:
            return self._rb.value

    @value.setter
    def value(self, val):
        """."""
        self._sp.put(val, wait=False)

    @property
    def refvalue(self):
        """."""
        return self.value


class RFCtrl(Corrector):
    """RF control class."""

    def __init__(self, acc):
        """Init method."""
        super().__init__(acc)
        self._name = self._csorb.RF_GEN_NAME
        opt = {'connection_timeout': TIMEOUT}
        self._sp = _PV(LL_PREF+self._name+':GeneralFreq-SP', **opt)
        self._rb = _PV(LL_PREF+self._name+':GeneralFreq-RB', **opt)
        self._config_ok_vals = {'PwrState': 1}
        self._config_pvs_sp = dict()
        #     'PwrState': _PV(LL_PREF+self._name+':PwrState-Sel', **opt)}
        self._config_pvs_rb = dict()
        #     'PwrState': _PV(LL_PREF+self._name+':PwrState-Sts', **opt)}

    @property
    def value(self):
        """Value."""
        if self._rb.connected:
            return self._rb.value

    @value.setter
    def value(self, freq):
        """."""
        delta_max = 20  # Hz
        freq0 = self.value
        if freq0 is None or freq is None:
            return
        delta = abs(freq-freq0)
        if delta < 0.1 or delta > 10000:
            return
        npoints = int(delta//delta_max) + 2
        freq_span = _np.linspace(freq0, freq, npoints)[1:]
        for i, freq in enumerate(freq_span, 1):
            self._sp.put(freq, wait=False)
            if i != freq_span.size:
                _time.sleep(1)

    @property
    def state(self):
        """State."""
        # TODO: database of RF GEN
        return True
        # pv = self._config_pvs_rb['PwrState']
        # return pv.value == 1 if pv.connected else False

    @state.setter
    def state(self, boo):
        """."""
        # TODO: database of RF GEN
        return
        # val = 1 if boo else 0
        # pv = self._config_pvs_sp['PwrState']
        # if pv.connected:
        #     self._config_ok_vals['PwrState'] = val
        #     pv.put(val, wait=False)


class CHCV(Corrector):
    """CHCV class."""

    def __init__(self, corr_name):
        """Init method."""
        super().__init__(corr_name)
        opt = {'connection_timeout': TIMEOUT}
        pvsp = self._name.substitute(
            prefix=LL_PREF, propty_name='Kick', propty_suffix='SP')
        pvrb = pvsp.substitute(propty_suffix='RB')
        pvref = pvsp.substitute(propty_name='KickRef', propty_suffix='Mon')
        self._sp = _PV(pvsp, **opt)
        self._rb = _PV(pvrb, **opt)
        self._ref = _PV(pvref, **opt)
        self._config_ok_vals = {
            'OpMode': _PSConst.OpMode.SlowRef,
            'PwrState': _PSConst.PwrStateSel.On}
        self._config_pvs_sp = {
            'OpMode': _PV(LL_PREF+self._name+':OpMode-Sel', **opt),
            'PwrState': _PV(LL_PREF+self._name+':PwrState-Sel', **opt)}
        self._config_pvs_rb = {
            'OpMode': _PV(LL_PREF+self._name+':OpMode-Sts', **opt),
            'PwrState': _PV(LL_PREF+self._name+':PwrState-Sts', **opt)}

    @property
    def opmode_ok(self):
        """Opmode ok status."""
        return self.opmode == self._config_ok_vals['OpMode']

    @property
    def opmode(self):
        """Opmode."""
        pv = self._config_pvs_rb['OpMode']
        if not pv.connected:
            return None
        elif pv.value == _PSConst.States.SlowRefSync:
            return _PSConst.OpMode.SlowRefSync
        elif pv.value == _PSConst.States.SlowRef:
            return _PSConst.OpMode.SlowRef
        return pv.value

    @opmode.setter
    def opmode(self, val):
        """."""
        pv = self._config_pvs_sp['OpMode']
        self._config_ok_vals['OpMode'] = val
        if pv.connected and pv.value != val:
            pv.put(val, wait=False)

    @property
    def connected(self):
        """Status connected."""
        conn = super().connected
        conn &= self._ref.connected
        if not self._ref.connected:
            _log.debug('NOT CONN: ' + self._ref.pvname)
        return conn

    @property
    def refvalue(self):
        """."""
        if self._ref.connected:
            return self._ref.value


class Septum(Corrector):
    """Septum class."""

    def __init__(self, corr_name):
        """Init method."""
        super().__init__(corr_name)
        opt = {'connection_timeout': TIMEOUT}
        pvsp = self._name.substitute(
            prefix=LL_PREF, propty_name='Kick', propty_suffix='SP')
        pvrb = pvsp.substitute(propty_suffix='RB')
        self._sp = _PV(pvsp, **opt)
        self._rb = _PV(pvrb, **opt)
        self._nominalkick = 98.55  # mrad
        self._config_ok_vals = {
            'Pulse': 1,
            'PwrState': _PSConst.PwrStateSel.On}
        self._config_pvs_sp = {
            'Pulse': _PV(LL_PREF+self._name+':Pulse-Sel', **opt),
            'PwrState': _PV(LL_PREF+self._name+':PwrState-Sel', **opt)}
        self._config_pvs_rb = {
            'Pulse': _PV(LL_PREF+self._name+':Pulse-Sts', **opt),
            'PwrState': _PV(LL_PREF+self._name+':PwrState-Sts', **opt)}

    @property
    def opmode_ok(self):
        """Opmode ok status."""
        return self.opmode == self._config_ok_vals['Pulse']

    @property
    def opmode(self):
        """Opmode."""
        pv = self._config_pvs_rb['Pulse']
        if not pv.connected:
            return None
        return pv.value

    @opmode.setter
    def opmode(self, val):
        """."""
        pv = self._config_pvs_sp['Pulse']
        self._config_ok_vals['Pulse'] = val
        if pv.connected and pv.value != val:
            pv.put(val, wait=False)

    @property
    def value(self):
        """Value."""
        if self._rb.connected:
            val = self._rb.value
            if val is not None:
                return -(val + self._nominalkick) * 1e3

    @value.setter
    def value(self, val):
        """."""
        val = val/1e3 + self._nominalkick
        self._sp.put(-val, wait=False)


def get_corr(name):
    """."""
    if name.dis == 'PU':
        return Septum(name)
    else:
        return CHCV(name)


class TimingConfig(_BaseTimingConfig):
    """Timing configuration class."""

    def __init__(self, acc):
        """Init method."""
        super().__init__(acc)
        evt = self._csorb.evt_cor_name
        pref_name = LL_PREF + self._csorb.evg_name + ':' + evt
        trig = self._csorb.trigger_cor_name
        opt = {'connection_timeout': TIMEOUT}
        self._evt_sender = _PV(pref_name + 'ExtTrig-Cmd', **opt)
        src_val = self._csorb.CorrExtEvtSrc._fields.index(evt)
        src_val = self._csorb.CorrExtEvtSrc[src_val]
        self._config_ok_vals = {
            'Mode': _TIConst.EvtModes.External,
            'Src': src_val, 'Delay': 0.0,
            'NrPulses': 1, 'Duration': 150.0, 'State': 1, 'Polarity': 0,
            }
        if _HLTimesearch.has_delay_type(trig):
            self._config_ok_vals['RFDelayType'] = _TIConst.TrigDlyTyp.Manual
        pref_trig = LL_PREF + trig + ':'
        self._config_pvs_rb = {
            'Mode': _PV(pref_name + 'Mode-Sts', **opt),
            'Src': _PV(pref_trig + 'Src-Sts', **opt),
            'Delay': _PV(pref_trig + 'Delay-RB', **opt),
            'NrPulses': _PV(pref_trig + 'NrPulses-RB', **opt),
            'Duration': _PV(pref_trig + 'Duration-RB', **opt),
            'State': _PV(pref_trig + 'State-Sts', **opt),
            'Polarity': _PV(pref_trig + 'Polarity-Sts', **opt),
            }
        self._config_pvs_sp = {
            'Mode': _PV(pref_name + 'Mode-Sel', **opt),
            'Src': _PV(pref_trig + 'Src-Sel', **opt),
            'Delay': _PV(pref_trig + 'Delay-SP', **opt),
            'NrPulses': _PV(pref_trig + 'NrPulses-SP', **opt),
            'Duration': _PV(pref_trig + 'Duration-SP', **opt),
            'State': _PV(pref_trig + 'State-Sel', **opt),
            'Polarity': _PV(pref_trig + 'Polarity-Sel', **opt),
            }
        if _HLTimesearch.has_delay_type(trig):
            self._config_pvs_rb['RFDelayType'] = _PV(
                pref_trig + 'RFDelayType-Sts', **opt)
            self._config_pvs_sp['RFDelayType'] = _PV(
                pref_trig + 'RFDelayType-Sel', **opt)

    def send_evt(self):
        """Send event method."""
        self._evt_sender.value = 1

    @property
    def connected(self):
        """Status connected."""
        conn = super().connected
        conn &= self._evt_sender.connected
        if not self._evt_sender.connected:
            _log.debug('NOT CONN: ' + self._evt_sender.pvname)
        return conn


class BaseCorrectors(_BaseClass):
    """Base correctors class."""


class EpicsCorrectors(BaseCorrectors):
    """Class to deal with correctors."""

    TINY_INTERVAL = 0.005
    NUM_TIMEOUT = 1000

    def __init__(self, acc, prefix='', callback=None):
        """Initialize the instance."""
        super().__init__(acc, prefix=prefix, callback=callback)
        self._synced_kicks = False
        self._acq_rate = 2
        self._names = self._csorb.ch_names + self._csorb.cv_names
        self._corrs = [get_corr(dev) for dev in self._names]
        if self.acc == 'SI':
            self._pssofb = _PSSOFB(self.acc, auto_mon=True)
            self._corrs.append(RFCtrl(self.acc))
            self.timing = TimingConfig(acc)
        self._corrs_thread = _Repeat(
            1/self._acq_rate, self._update_corrs_strength, niter=0)
        self._corrs_thread.start()

    @property
    def corrs(self):
        """."""
        return self._corrs

    def get_map2write(self):
        """Get the write methods of the class."""
        dbase = {
            'CorrConfig-Cmd': self.configure_correctors,
            'KickAcqRate-SP': self.set_kick_acq_rate,
            }
        if self.acc == 'SI':
            dbase['CorrSync-Sel'] = self.set_corrs_mode
        return dbase

    def apply_kicks(self, values, use_pssofb=False):
        """Apply kicks."""
        strn = '    TIMEIT: {0:20s} - {1:7.3f}'
        _log.info('    TIMEIT: BEGIN')
        time1 = _time.time()

        not_nan_idcs = ~_np.isnan(values)
        # Send correctors setpoint
        if self.acc == 'SI' and use_pssofb:
            self._pssofb.kick = values[:-1]
            if not_nan_idcs[-1]:
                self.put_value_in_corr(self._corrs[-1], values[-1])
        else:
            for i, corr in enumerate(self._corrs):
                if not_nan_idcs[i]:
                    self.put_value_in_corr(corr, values[i])
        time2 = _time.time()
        _log.info(strn.format('send sp:', 1000*(time2-time1)))

        # Wait for readbacks to be updated
        if self._timed_out(values, mode='ready', use_pssofb=use_pssofb):
            return
        time3 = _time.time()
        _log.info(strn.format('check ready:', 1000*(time3-time2)))

        # Send trigger signal for implementation
        self.send_evt()
        time4 = _time.time()
        _log.info(strn.format('send evt:', 1000*(time4-time3)))

        # Wait for references to be updated
        if not (self.acc == 'SI' and use_pssofb and self._synced_kicks):
            self._timed_out(values, mode='applied', use_pssofb=use_pssofb)
        time5 = _time.time()
        _log.info(strn.format('check applied:', 1000*(time5-time4)))
        _log.info('    TIMEIT: END')

    def put_value_in_corr(self, corr, value):
        """Put value in corrector method."""
        if not corr.connected:
            msg = 'ERR: ' + corr.name + ' not connected.'
            self._update_log(msg)
            _log.error(msg[5:])
        elif not corr.state:
            msg = 'ERR: ' + corr.name + ' is off.'
            self._update_log(msg)
            _log.error(msg[5:])
        elif not corr.opmode_ok:
            msg = 'ERR: ' + corr.name + ' mode not configured.'
            self._update_log(msg)
            _log.error(msg[5:])
        else:
            corr.value = value

    def send_evt(self):
        """Send event method."""
        if self.acc != 'SI' or not self._synced_kicks:
            return
        if not self.timing.connected:
            msg = 'ERR: timing disconnected.'
            self._update_log(msg)
            _log.error(msg[5:])
            return
        elif not self.timing.is_ok:
            msg = 'ERR: timing not configured.'
            self._update_log(msg)
            _log.error(msg[5:])
            return
        self.timing.send_evt()

    def get_strength(self, use_pssofb=False):
        """Get the correctors strengths."""
        corr_values = _np.zeros(self._csorb.nr_corrs, dtype=float)
        if self.acc == 'SI' and use_pssofb:
            corr_values[:-1] = self._pssofb.kick
            corr_values[-1] = self._corrs[-1].value
        else:
            for i, corr in enumerate(self._corrs):
                if corr.connected and corr.value is not None:
                    corr_values[i] = corr.value
                else:
                    msg = 'ERR: Failed to get value from '
                    msg += corr.name
                    self._update_log(msg)
                    _log.error(msg[5:])
        return corr_values

    def set_kick_acq_rate(self, value):
        """Set kick caq rate method."""
        self._acq_rate = value
        self._corrs_thread.interval = 1/value
        self.run_callbacks('KickAcqRate-RB', value)
        return True

    def _update_corrs_strength(self):
        try:
            corr_vals = self.get_strength()
            self.run_callbacks('KickCH-Mon', corr_vals[:self._csorb.nr_ch])
            self.run_callbacks(
                'KickCV-Mon', corr_vals[self._csorb.nr_ch:self._csorb.nr_chcv])
            if self.acc == 'SI':
                self.run_callbacks('KickRF-Mon', corr_vals[-1])
        except Exception as err:
            self._update_log('ERR: ' + str(err))
            _log.error(str(err))

    def set_corrs_mode(self, value):
        """Set mode of CHs and CVs method."""
        self._synced_kicks = value
        if self._synced_kicks == self._csorb.CorrSync.On:
            val = _PSConst.OpMode.SlowRefSync
        elif self._synced_kicks == self._csorb.CorrSync.Off:
            val = _PSConst.OpMode.SlowRef

        for corr in self._corrs:
            if corr.connected:
                corr.opmode = val
            else:
                msg = 'ERR: Failed to configure '
                msg += corr.name
                self._update_log(msg)
                _log.error(msg[5:])
                return False
        msg = 'Correctors set to {0:s} Mode'.format(
            'Sync' if value else 'Async')
        self._update_log(msg)
        _log.info(msg)
        self.run_callbacks('CorrSync-Sts', value)
        return True

    def configure_correctors(self, _):
        """Configure correctors method."""
        val = _PSConst.OpMode.SlowRef
        if self.acc == 'SI' and self._synced_kicks == self._csorb.CorrSync.On:
            val = _PSConst.OpMode.SlowRefSync
        for corr in self._corrs:
            if corr.connected:
                corr.state = True
                # Do not configure opmode in BO corrs because they are ramping.
                if self.acc == 'BO':
                    continue
                corr.opmode = val
            else:
                msg = 'ERR: Failed to configure '
                msg += corr.name
                self._update_log(msg)
                _log.error(msg[5:])
        if not self.isring:
            return True

        if self.acc == 'SI' and self._synced_kicks == self._csorb.CorrSync.On:
            if not self.timing.configure():
                msg = 'ERR: Failed to configure timing'
                self._update_log(msg)
                _log.error(msg[5:])
        return True

    def _update_status(self):
        status = 0b0000111
        if self.acc == 'SI':
            status = 0b1111111
        elif self.isring:
            status = 0b0011111

        chcvs = self._corrs[:self._csorb.nr_chcv]
        status = _util.update_bit(
            status, bit_pos=0,
            bit_val=not all(corr.connected for corr in chcvs))
        # Do not check mode of BO correctors because they are ramping.
        opmode_ok = True
        if self.acc != 'BO':
            opmode_ok = all(corr.opmode_ok for corr in chcvs)
        status = _util.update_bit(status, bit_pos=1, bit_val=not opmode_ok)
        status = _util.update_bit(
            status, bit_pos=2,
            bit_val=not all(corr.state for corr in chcvs))
        if self.acc == 'SI' and self._synced_kicks == self._csorb.CorrSync.On:
            tim_conn = self.timing.connected
            tim_conf = self.timing.is_ok
        else:
            tim_conn = tim_conf = True
        status = _util.update_bit(status, bit_pos=3, bit_val=not tim_conn)
        status = _util.update_bit(status, bit_pos=4, bit_val=not tim_conf)
        if self.acc == 'SI':
            rfctrl = self._corrs[-1]
            status = _util.update_bit(
                status, bit_pos=5, bit_val=not rfctrl.connected)
            status = _util.update_bit(
                status, bit_pos=6, bit_val=not rfctrl.state)
        self._status = status
        self.run_callbacks('CorrStatus-Mon', status)

    def _timed_out(self, values, mode='ready', use_pssofb=False):
        if self.acc == 'SI' and use_pssofb:
            return self._timed_out_pssofb(values, mode=mode)

        okg = [False, ] * len(self._corrs)
        for _ in range(self.NUM_TIMEOUT):
            for i, corr in enumerate(self._corrs):
                if okg[i]:
                    continue
                if _np.isnan(values[i]):
                    okg[i] = True
                    continue
                val = corr.value if mode == 'ready' else corr.refvalue
                okg[i] = val is not None and _compare_kicks(values[i], val)
            if all(okg):
                return False
            _time.sleep(self.TINY_INTERVAL)

        self._print_guilty(okg, mode=mode)
        return True

    def _timed_out_pssofb(self, values, mode='ready'):
        pss = self._pssofb
        rfc = self._corrs[-1]

        okg = [False, ] * len(self._corrs)
        val4comp = _np.zeros(len(okg), dtype=float)
        for _ in range(self.NUM_TIMEOUT):
            val4comp[:-1] = pss.kick_rb if mode == 'ready' else pss.kick
            val4comp[-1] = rfc.value if mode == 'ready' else rfc.refvalue
            for i, val in enumerate(val4comp):
                if okg[i]:
                    continue
                if _np.isnan(values[i]):
                    okg[i] = True
                    continue
                okg[i] = ~_np.isnan(val) and _compare_kicks(values[i], val)
            if all(okg):
                return False
            _time.sleep(self.TINY_INTERVAL)

        self._print_guilty(okg, mode=mode)
        return True

    def _print_guilty(self, okg, mode='ready'):
        mde = 'RB' if mode == 'ready' else 'Ref'
        for oki, corr in zip(okg, self._corrs):
            if not oki:
                msg = 'ERR: timeout {0:3s}: {1:s}'.format(mde, corr.name)
                self._update_log(msg)
                _log.error(msg[5:])

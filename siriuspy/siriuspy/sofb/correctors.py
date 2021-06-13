"""Module to deal with correctors."""

import time as _time
import logging as _log
import traceback as _traceback

import numpy as _np
from PRUserial485 import EthBridgeClient

from .. import util as _util
from ..epics import PV as _PV
from ..thread import RepeaterThread as _Repeat
from ..pwrsupply.csdev import Const as _PSConst
from ..pwrsupply.bsmp.constants import ConstPSBSMP as _ConstPSBSMP
from ..timesys.csdev import Const as _TIConst
from ..search import HLTimeSearch as _HLTimesearch
from ..envars import VACA_PREFIX as LL_PREF
from ..namesys import SiriusPVName as _PVName
from ..devices import PSApplySOFB as _PSSOFBIOC

from ..pwrsupply.pssofb import PSSOFB as _PSSOFB


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
    def standbymode_ok(self):
        """StandByMode ok status."""
        return self.connected

    @property
    def standbymode(self):
        """StandByMode."""
        return 0

    @standbymode.setter
    def standbymode(self, val):
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
            'PwrState': _PSConst.PwrStateSel.On,
            'StandByMode': _PSConst.DsblEnbl.Dsbl}
        self._config_pvs_sp = {
            'OpMode': _PV(LL_PREF+self._name+':OpMode-Sel', **opt),
            'PwrState': _PV(LL_PREF+self._name+':PwrState-Sel', **opt),
            'StandByMode': _PV(LL_PREF+self._name+':StandByMode-Sel', **opt)}
        self._config_pvs_rb = {
            'OpMode': _PV(LL_PREF+self._name+':OpMode-Sts', **opt),
            'PwrState': _PV(LL_PREF+self._name+':PwrState-Sts', **opt),
            'StandByMode': _PV(LL_PREF+self._name+':StandByMode-Sts', **opt)}

    @property
    def opmode_ok(self):
        """Opmode ok status."""
        isok = self.opmode == self._config_ok_vals['OpMode']
        if not isok:
            msg = 'OpMode not Ok {0:s}'.format(self.name)
            _log.warning(msg)
        return isok

    @property
    def opmode(self):
        """Opmode."""
        pvobj = self._config_pvs_rb['OpMode']
        if not pvobj.connected:
            return None
        elif pvobj.value == _PSConst.States.SlowRefSync:
            return _PSConst.OpMode.SlowRefSync
        elif pvobj.value == _PSConst.States.SlowRef:
            return _PSConst.OpMode.SlowRef
        return pvobj.value

    @opmode.setter
    def opmode(self, val):
        """."""
        pvobj = self._config_pvs_sp['OpMode']
        self._config_ok_vals['OpMode'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def standbymode_ok(self):
        """Opmode ok status."""
        isok = self.standbymode == self._config_ok_vals['StandByMode']
        if not isok:
            msg = 'StandByMode not Ok {0:s}'.format(self.name)
            _log.warning(msg)
        return isok

    @property
    def standbymode(self):
        """StandByMode."""
        pvobj = self._config_pvs_rb['StandByMode']
        if not pvobj.connected:
            return None
        return pvobj.value

    @standbymode.setter
    def standbymode(self, val):
        """."""
        pvobj = self._config_pvs_sp['StandByMode']
        self._config_ok_vals['StandByMode'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

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

    def configure(self):
        """Configure method."""
        if not self.connected:
            return False
        val = self._config_ok_vals['StandByMode']
        self.standbymode = 0
        for k, pvo in self._config_pvs_sp.items():
            if k in self._config_ok_vals and k != 'StandByMode':
                pvo.put(self._config_ok_vals[k], wait=False)
        self.standbymode = val
        return True


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
        self.EVT = src_val
        src_val = self._csorb.CorrExtEvtSrc._fields.index(
            self._csorb.clk_cor_name)
        src_val = self._csorb.CorrExtEvtSrc[src_val]
        self.CLK = src_val
        self._config_ok_vals = {
            'Mode': _TIConst.EvtModes.External,
            'Src': src_val, 'NrPulses': 1, 'Duration': 150.0, 'State': 1,
            'Polarity': 0,
            }
        if _HLTimesearch.has_delay_type(trig):
            self._config_ok_vals['RFDelayType'] = _TIConst.TrigDlyTyp.Manual
        pref_trig = LL_PREF + trig + ':'
        self._config_pvs_rb = {
            'Mode': _PV(pref_name + 'Mode-Sts', **opt),
            'Src': _PV(pref_trig + 'Src-Sts', **opt),
            'DelayRaw': _PV(pref_trig + 'DelayRaw-RB', **opt),
            'NrPulses': _PV(pref_trig + 'NrPulses-RB', **opt),
            'Duration': _PV(pref_trig + 'Duration-RB', **opt),
            'State': _PV(pref_trig + 'State-Sts', **opt),
            'Polarity': _PV(pref_trig + 'Polarity-Sts', **opt),
            }
        self._config_pvs_sp = {
            'Mode': _PV(pref_name + 'Mode-Sel', **opt),
            'Src': _PV(pref_trig + 'Src-Sel', **opt),
            'DelayRaw': _PV(pref_trig + 'DelayRaw-SP', **opt),
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
    def sync_type(self):
        """."""
        return self._config_pvs_rb['Src'].value

    @sync_type.setter
    def sync_type(self, value):
        """."""
        if value not in (self.EVT, self.CLK):
            return
        self._config_ok_vals['Src'] = value
        pvobj = self._config_pvs_sp['Src']
        if pvobj.connected:
            pvobj.value = value

    @property
    def delayraw(self):
        """."""
        defv = 0
        pvobj = self._config_pvs_rb['DelayRaw']
        val = pvobj.value if pvobj.connected else defv
        return val if val else defv

    @delayraw.setter
    def delayraw(self, value):
        """."""
        pvobj = self._config_pvs_sp['DelayRaw']
        if pvobj.connected:
            pvobj.value = int(value)

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
    PSSOFB_USE_IOC = False
    MAX_PROB = 5

    def __init__(self, acc, prefix='', callback=None):
        """Initialize the instance."""
        super().__init__(acc, prefix=prefix, callback=callback)
        self._sync_kicks = False
        self._acq_rate = 2
        self._names = self._csorb.ch_names + self._csorb.cv_names
        self._corrs = [get_corr(dev) for dev in self._names]
        self._use_pssofb = False
        self._wait_pssofb = False
        if self.acc == 'SI':
            self._ref_kicks = None
            self._ret_kicks = None
            self._func_ret = None
            self._prob = None
            if not EpicsCorrectors.PSSOFB_USE_IOC:
                self._pssofb = _PSSOFB(
                    EthBridgeClient, nr_procs=8, asynchronous=True,
                    sofb_update_iocs=True)
                self._pssofb.processes_start()
            else:
                self._pssofb = _PSSOFBIOC('SI', auto_mon=True)
            self._corrs.append(RFCtrl(self.acc))
            self.timing = TimingConfig(acc)
        self._corrs_thread = _Repeat(
            1/self._acq_rate, self._update_corrs_strength, niter=0)
        self._corrs_thread.start()

    @property
    def corrs(self):
        """."""
        return self._corrs

    @property
    def use_pssofb(self):
        """."""
        return self._use_pssofb

    @use_pssofb.setter
    def use_pssofb(self, value):
        self.set_use_pssofb(value)

    def shutdown(self):
        """Shutdown Process."""
        if self.acc == 'SI':
            self._pssofb.processes_shutdown()

    def get_map2write(self):
        """Get the write methods of the class."""
        dbase = {
            'CorrConfig-Cmd': self.configure_correctors,
            'KickAcqRate-SP': self.set_kick_acq_rate,
            }
        if self.acc == 'SI':
            dbase['CorrPSSOFBEnbl-Sel'] = self.set_use_pssofb
            dbase['CorrPSSOFBWait-Sel'] = self.set_wait_pssofb
            dbase['CorrSync-Sel'] = self.set_corrs_mode
        return dbase

    def apply_kicks(self, values):
        """Apply kicks.

        Will return -2 if there is a problem with some PS.
        Will return -1 if PS did not finish applying last kick.
        Will return 0 if all previous kick were implemented.
        Will return >0 indicating how many previous kicks were not implemented.
        """
        if self.acc == 'SI' and self._use_pssofb:
            return self.apply_kicks_pssofb(values)

        strn = '    TIMEIT: {0:20s} - {1:7.3f}'
        _log.info('    TIMEIT: BEGIN')
        time1 = _time.time()

        not_nan_idcs = ~_np.isnan(values)
        # Send correctors setpoint
        for i, corr in enumerate(self._corrs):
            if not_nan_idcs[i]:
                self.put_value_in_corr(corr, values[i])
        time2 = _time.time()
        _log.info(strn.format('send sp:', 1000*(time2-time1)))

        # Wait for readbacks to be updated
        if self._timed_out(values, mode='ready'):
            return -1
        time3 = _time.time()
        _log.info(strn.format('check ready:', 1000*(time3-time2)))

        # Send trigger signal for implementation
        self.send_evt()
        time4 = _time.time()
        _log.info(strn.format('send evt:', 1000*(time4-time3)))

        # Wait for references to be updated
        self._timed_out(values, mode='applied')
        time5 = _time.time()
        _log.info(strn.format('check applied:', 1000*(time5-time4)))
        _log.info('    TIMEIT: END')
        return 0

    def apply_kicks_pssofb(self, values):
        """Apply kicks with PSSOFB.

        Will return -2 if there is a problem with some PS.
        Will return -1 if PS did not finish applying last kick.
        Will return 0 if all previous kick were implemented.
        Will return >0 indicating how many previous kicks were not implemented.
        """
        if not self._pssofb.is_ready():
            return -1

        # Send correctors setpoint
        ret_kicks = self._pssofb.sofb_kick_readback_ref
        func_ret = self._pssofb.sofb_func_return
        self._ret_kicks = ret_kicks
        self._func_ret = func_ret

        self._set_ref_kicks(values)
        self._pssofb.bsmp_sofb_kick_set(self._ref_kicks[-1][:-1])
        if not _np.isnan(values[-1]):
            self.put_value_in_corr(self._corrs[-1], values[-1])

        if self._wait_pssofb:
            self._pssofb.wait()

        # compare kicks to check if there is something wrong
        ret = self._compare_kicks_pssofb(ret_kicks, func_ret)

        # Send trigger signal for implementation
        self.send_evt()

        return ret

    def _set_ref_kicks(self, values):
        new_ref = _np.array(self._ref_kicks[-1])
        not_nan = ~_np.isnan(values)
        new_ref[not_nan] = values[not_nan]
        self._ref_kicks.append(new_ref)
        del self._ref_kicks[0]

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
        if self.acc != 'SI' or self._sync_kicks != self._csorb.CorrSync.Event:
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

    def get_strength(self):
        """Get the correctors strengths."""
        corr_values = _np.zeros(self._csorb.nr_corrs, dtype=float)
        if self.acc == 'SI' and self._use_pssofb:
            return self._ref_kicks[-1].copy()

        for i, corr in enumerate(self._corrs):
            if corr.connected and corr.value is not None:
                corr_values[i] = corr.refvalue
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
            if self.acc == 'SI' and corr_vals[-1] > 0:
                rfv = corr_vals[-1]
                circ = 1/rfv * self._csorb.harm_number * 299792458
                self.run_callbacks('KickRF-Mon', rfv)
                self.run_callbacks('OrbLength-Mon', circ)
        except Exception as err:
            self._update_log('ERR: ' + str(err))
            _log.error(_traceback.format_exc())

    def set_corrs_mode(self, value):
        """Set mode of CHs and CVs method."""
        if value not in self._csorb.CorrSync:
            return False
        self._sync_kicks = value
        val = _PSConst.OpMode.SlowRefSync
        if value == self._csorb.CorrSync.Off:
            self.set_timing_delay(0)
            val = _PSConst.OpMode.SlowRef
        elif value == self._csorb.CorrSync.Event:
            self.set_timing_delay(0)
            self.timing.sync_type = self.timing.EVT
        else:
            self.set_timing_delay(self._csorb.CORR_DEF_DELAY)
            self.timing.sync_type = self.timing.CLK

        for corr in self._corrs:
            if corr.connected:
                corr.opmode = val
            else:
                msg = 'ERR: Failed to configure '
                msg += corr.name
                self._update_log(msg)
                _log.error(msg[5:])
                return False

        strsync = self._csorb.CorrSync._fields[self._sync_kicks]
        msg = 'Synchronization set to {0:s}'.format(strsync)
        self._update_log(msg)
        _log.info(msg)
        self.run_callbacks('CorrSync-Sts', value)
        return True

    def set_timing_delay(self, value):
        """."""
        frf = 499664 / 4  # [kHz]
        raw = int(value * frf)
        self.timing.delayraw = raw
        return True

    def set_use_pssofb(self, val):
        """."""
        if self.acc != 'SI':
            return False
        if val not in self._csorb.CorrPSSOFBEnbl:
            return False
        if val != self._use_pssofb and val == self._csorb.CorrPSSOFBEnbl.Enbld:
            kicks = self.get_strength()
            self._ref_kicks = [kicks.copy(), kicks.copy(), kicks.copy()]
            self._prob = _np.zeros(kicks.size, dtype=_np.int8)
            # initialize PSSOFB State
            self._pssofb.bsmp_sofb_kick_set(kicks[:-1])
        self._use_pssofb = val

        # NOTE: We need this time to avoid problems in the Correctors IOCs.
        # We noticed that without this sleep, in ramdom manner, the IOCs from
        # some correctors do not turn off the SOFB mode when requested, which
        # required the reboot of the IOC to get back control of the corrs.
        # We noticed this problem only happens when we use PSSOFB to control
        # the correctors. This means that PSConnSOFB, which doesn't use
        # multiprocessing, is problem free somehow.
        # We don't understand the reason for this sleep to solve the problem
        # and neither why the problem even occurs...
        _time.sleep(0.2)

        for corr in self._corrs[:-1]:
            if not corr.connected:
                msg = 'ERR: Failed to configure '
                msg += corr.name
                self._update_log(msg)
                _log.error(msg[5:])
                continue
            corr.standbymode = val

        self.run_callbacks('CorrPSSOFBEnbl-Sts', val)
        return True

    def set_wait_pssofb(self, val):
        """."""
        if self.acc != 'SI':
            return False
        if val not in self._csorb.CorrPSSOFBWait:
            return False
        self._wait_pssofb = val
        self.run_callbacks('CorrPSSOFBWait-Sts', val)
        return True

    def configure_correctors(self, _):
        """Configure correctors method."""
        for corr in self._corrs:
            if not corr.connected:
                msg = 'ERR: Failed to configure '
                msg += corr.name
                self._update_log(msg)
                _log.error(msg[5:])
                continue
            # Do not configure opmode in BO corrs because they are ramping.
            if self.acc == 'BO':
                corr.state = True
                continue
            corr.configure()
        if not self.isring:
            return True

        if self.acc == 'SI' and self._sync_kicks != self._csorb.CorrSync.Off:
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
        if self.acc == 'SI':
            opmode_ok &= all(corr.standbymode_ok for corr in chcvs)
        status = _util.update_bit(status, bit_pos=1, bit_val=not opmode_ok)
        status = _util.update_bit(
            status, bit_pos=2,
            bit_val=not all(corr.state for corr in chcvs))
        if self.acc == 'SI' and self._sync_kicks != self._csorb.CorrSync.Off:
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

    def _timed_out(self, values, mode='ready'):
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

    def _compare_kicks_pssofb(self, values, fret):
        rfc = self._corrs[-1]
        ref_vals = self._ref_kicks[0]

        res_tim = _np.ones(ref_vals.size, dtype=bool)
        res_tim[:-1] = fret != _ConstPSBSMP.ACK_DSP_TIMEOUT
        res = fret != _ConstPSBSMP.ACK_OK
        res &= res_tim[:-1]
        if _np.any(res):
            self._print_guilty(
                ~res, mode='prob_code', fret=fret)
            return -2

        curr_vals = _np.zeros(self._csorb.nr_corrs, dtype=float)
        curr_vals[:-1] = values
        curr_vals[-1] = rfc.value

        # NOTE: If the return value is zero, it might mean the corrector had a
        # problem. In this case we return -2 so the main correction loop can
        # exit and give back the control to the IOC.
        iszero = _compare_kicks(curr_vals, 0)
        iszero_ref = _compare_kicks(ref_vals, 0)
        prob = iszero & ~(iszero_ref)
        # For debugging:
        # if _np.any(prob):
        #     self._print_guilty(
        #         ~prob, mode='prob_curr', currs=curr_vals, refs=ref_vals)

        # Only acuse problem if it repeats for MAX_PROB consecutive times:
        # Because in some cases of previous unsuccessful applications, the
        # current value will be different from this reference.
        self._prob[prob] += 1
        self._prob[~prob] = 0
        if _np.any(self._prob >= self.MAX_PROB):
            self._print_guilty(
                ~prob, mode='prob_curr', currs=curr_vals, refs=ref_vals)
            return -2

        equl = _compare_kicks(curr_vals, ref_vals)
        equl |= ~res_tim
        return _np.sum(~equl)

    def _print_guilty(
            self, okg, mode='ready', fret=None, currs=None, refs=None):
        msg_tmpl = 'ERR: timeout {0:3s}: {1:s}'
        data = [tuple(), ] * len(self._corrs)
        if mode == 'prob_code':
            msg_tmpl = 'ERR: {0:s} --> {1:s}: code={2:d}'
            data = zip(fret)
        elif mode == 'prob_curr':
            msg_tmpl = 'ERR: {0:s} --> {1:s}: curr={2:.4g}, ref={3:.4g}'
            data = zip(currs, refs)
        elif mode == 'diff':
            msg_tmpl = 'ERR: Corrector {1:s} diff from setpoint!'
        for oki, corr, args in zip(okg, self._corrs, data):
            if not oki:
                msg = msg_tmpl.format(mode, corr.name, *args)
                self._update_log(msg)
                _log.error(msg[5:])

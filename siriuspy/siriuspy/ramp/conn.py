"""Module with connector classes.

This module implements connector classes responsible for communications with
pwrsupply soft IOcs, ConfigDB service and orbit IOCs.
"""

# TODO: Implementations in this module make pylint very confused.
# Is there a code efficiency reason to initialize class attributes
# outside private methods?

import math as _math
import numpy as _np


from .. import envars as _envars
from .. import csdev as _csdev

from ..epics import EpicsProperty as _EpicsProperty, \
    EpicsPropertiesList as _EpicsPropsList
from ..namesys import SiriusPVName as _PVName
from ..pwrsupply.csdev import Const as _PSConst
from ..timesys.csdev import Const as _TIConst, \
    get_hl_trigger_database as _get_trig_db
from ..sofb.csdev import SOFBRings as _SOFBRings
from ..search import LLTimeSearch as _LLTimeSearch, \
    PSSearch as _PSSearch

from . import util as _rutil


_PREFIX = _envars.VACA_PREFIX
_TIMEOUT_DFLT = 8
_TIMEOUT_PWRSTATE_ON = 2
_TIMEOUT_PWRSTATE_OFF = 1
_TIMEOUT_OPMODE_CHANGE = 6


class ConnTI(_EpicsPropsList):
    """Timing connector class."""

    class Const(_csdev.Const):
        """Properties names."""

        BO_HarmNum = 828
        EVG_RFDiv = 4

        # EVG PVs
        EVG = _LLTimeSearch.get_evg_name()
        EVG_DevEnbl = EVG + ':DevEnbl-Sel'
        EVG_ContinuousEvt = EVG + ':ContinuousEvt-Sel'
        EVG_InjectionEvt = EVG + ':InjectionEvt-Sel'
        EVG_FPGAClk = EVG + ':FPGAClk-Cte'
        EVG_UpdateEvt = EVG + ':UpdateEvt-Cmd'

        # Linac Egun mode properties
        LinacEgun_SglBun_State = 'LI-01:EG-PulsePS:singleselstatus'
        LinacEgun_MultBun_State = 'LI-01:EG-PulsePS:multiselstatus'

        # Interlock PV
        Intlk = 'LA-RFH01RACK2:TI-EVR:IntlkStatus-Mon'

    # Add events properties to Const
    _events = {
        'EvtLinac': Const.EVG + ':Linac',
        'EvtInjBO': Const.EVG + ':InjBO',
        'EvtInjSI': Const.EVG + ':InjSI',
        'EvtRmpBO': Const.EVG + ':RmpBO',
        'EvtDigLI': Const.EVG + ':DigLI',
        'EvtDigTB': Const.EVG + ':DigTB',
        'EvtDigBO': Const.EVG + ':DigBO',
        'EvtDigTS': Const.EVG + ':DigTS',
        'EvtDigSI': Const.EVG + ':DigSI',
        'EvtStudy': Const.EVG + ':Study'}

    evt_propties = ('Mode-Sel', 'DelayType-Sel', 'Delay-SP')
    for attr, evt_name in _events.items():
        setattr(Const, attr, evt_name)
        for p in evt_propties:
            p = _PVName(p)
            new_attr = attr+'_'+p.propty_name
            setattr(Const, new_attr, evt_name+p)

    # Add trigger properties to Const
    _triggers = {
        'TrgMags': 'BO-Glob:TI-Mags-Fams',
        'TrgCorrs': 'BO-Glob:TI-Mags-Corrs',
        'TrgLLRFRmp': 'BO-Glob:TI-LLRF-Rmp',
        'TrgEGunSglBun': 'LI-01:TI-EGun-SglBun',
        'TrgEGunMultBun': 'LI-01:TI-EGun-MultBun',
        'TrgEjeKckr': 'BO-48D:TI-EjeKckr',
        'TrgInjKckr': 'SI-01SA:TI-InjDpKckr'}

    trg_propties = ('State-Sel', 'Polarity-Sel', 'Src-Sel', 'NrPulses-SP',
                    'Duration-SP', 'Delay-SP', 'Status-Mon')
    for attr, trg_name in _triggers.items():
        setattr(Const, attr, trg_name)
        for p in trg_propties:
            p = _PVName(p)
            new_attr = attr+'_'+p.propty_name
            setattr(Const, new_attr, trg_name+':'+p)

    def __init__(self, ramp_config=None, prefix=_PREFIX,
                 connection_callback=None, callback=None):
        """Init."""
        self._ramp_config = ramp_config
        properties = self._define_properties(prefix, connection_callback,
                                             callback)
        super().__init__(properties)

    def get_ramp_config(self, ramp_config):
        """Receive BoosterRamp configuration."""
        self._ramp_config = ramp_config

    # --- timing setup commands ---

    def cmd_setup(self, timeout=_TIMEOUT_DFLT):
        """Do setup TI subsystem to ramp."""
        sp = self.ramp_basicsetup.copy()
        ppties = list(sp.keys())
        for ppty in ppties:
            if 'Status-Mon' in ppty:
                sp.pop(ppty)
        return self._command(sp, timeout)

    def cmd_config_ramp(self, events_inj, events_eje, timeout=_TIMEOUT_DFLT):
        """Apply ramp_config values to TI subsystem."""
        if self._ramp_config is None:
            return

        sp = dict()
        c = ConnTI.Const

        # Triggers delays
        sp[c.TrgMags_Delay] = self._ramp_config.ti_params_ps_ramp_delay
        sp[c.TrgCorrs_Delay] = self._ramp_config.ti_params_ps_ramp_delay
        sp[c.TrgLLRFRmp_Delay] = self._ramp_config.ti_params_rf_ramp_delay

        # Event delays
        sp[c.EvtRmpBO_Delay] = 0
        delays = self.calc_evts_delay(events_inj, events_eje)
        sp[c.EvtLinac_Delay] = delays['Linac']
        sp[c.EvtInjBO_Delay] = delays['InjBO']
        sp[c.EvtInjSI_Delay] = delays['InjSI']
        sp[c.TrgInjKckr_Delay] = delays[c.TrgInjKckr_Delay]
        for event in events_inj:
            attr = getattr(c, 'Evt'+event+'_Delay')
            sp[attr] = delays[event]
        for event in events_eje:
            attr = getattr(c, 'Evt'+event+'_Delay')
            sp[attr] = delays[event]

        # Update ramp_configsetup
        self.update_ramp_configsetup(events_inj, events_eje, delays)

        return self._command(sp, timeout)

    def cmd_start_ramp(self, timeout=_TIMEOUT_DFLT):
        """Start EVG continuous events."""
        sp = {ConnTI.Const.EVG_ContinuousEvt: _TIConst.DsblEnbl.Enbl}
        return self._command(sp, timeout)

    def cmd_stop_ramp(self, timeout=_TIMEOUT_DFLT):
        """Stop EVG continuous events."""
        sp = {ConnTI.Const.EVG_ContinuousEvt: _TIConst.DsblEnbl.Dsbl}
        return self._command(sp, timeout)

    def cmd_start_injection(self, timeout=_TIMEOUT_DFLT):
        """Start EVG injection events."""
        sp = {ConnTI.Const.EVG_InjectionEvt: _TIConst.DsblEnbl.Enbl}
        return self._command(sp, timeout)

    def cmd_stop_injection(self, timeout=_TIMEOUT_DFLT):
        """Stop EVG injection events."""
        sp = {ConnTI.Const.EVG_InjectionEvt: _TIConst.DsblEnbl.Dsbl}
        return self._command(sp, timeout)

    def cmd_set_magnet_trigger_state(self, state, timeout=_TIMEOUT_DFLT):
        c = ConnTI.Const
        sp = {c.TrgMags_State: state,
              c.TrgCorrs_State: state}
        return self._command(sp, timeout)

    def cmd_update_evts(self, timeout=_TIMEOUT_DFLT):
        sp = {ConnTI.Const.EVG_UpdateEvt: 1}
        return self._command(sp, timeout)

    # --- timing mode check ---

    def check_intlk(self):
        """Check if interlock is reset."""
        return self._check(ConnTI.Const.Intlk, 0)

    def check_setup_ramp(self):
        """Check if ramp basic setup is implemented."""
        return self._check(self.ramp_basicsetup)

    def check_ramping(self):
        """Check if continuous events are enabled."""
        rb = {ConnTI.Const.EVG_ContinuousEvt: _TIConst.DsblEnbl.Enbl}
        return self._check(rb)

    def check_injecting(self):
        """Check if injection events are enabled."""
        rb = {ConnTI.Const.EVG_InjectionEvt: _TIConst.DsblEnbl.Enbl}
        return self._check(rb)

    # --- helper methods ---

    def calc_evts_delay(self, events_inj=list(), events_eje=list()):
        """Calculate event delays."""
        if self._ramp_config is None:
            return
        if not self.connected:
            return

        c = ConnTI.Const
        evg_base_time = 1e6 / self.get_readback(c.EVG_FPGAClk)
        bo_rev = evg_base_time * c.BO_HarmNum/c.EVG_RFDiv

        # Injection
        injection_time = self._ramp_config.ti_params_injection_time*1e3
        egun_dly = self.get_readback(c.TrgEGunSglBun_Delay) \
            if self.get_readback(c.LinacEgun_SglBun_State) \
            else self.get_readback(c.TrgEGunMultBun_Delay)
        delay_inj = injection_time - egun_dly

        # curr_linac_dly = self.get_readback(c.EvtLinac_Delay)
        curr_injbo_dly = self.get_readback(c.EvtInjBO_Delay)
        dlt_inj_dly = delay_inj - curr_injbo_dly
        dlt_inj_dly = int(dlt_inj_dly/bo_rev)*bo_rev

        # Ejection
        ejection_time = self._ramp_config.ti_params_ejection_time*1e3
        ejekckr_dly = self.get_readback(c.TrgEjeKckr_Delay)
        delay_eje = ejection_time - ejekckr_dly

        curr_injsi_dly = self.get_readback(c.EvtInjSI_Delay)
        dlt_eje_dly = delay_eje - curr_injsi_dly
        dlt_eje_dly = int(dlt_eje_dly/bo_rev)*bo_rev

        # calc delays
        delays = dict()

        events_inj = sorted(events_inj)
        if 'Linac' not in events_inj:
            events_inj.append('Linac')
        if 'InjBO' not in events_inj:
            events_inj.append('InjBO')
        for event in events_inj:
            attr = getattr(c, 'Evt'+event+'_Delay')
            curr = self.get_readback(attr)
            delays[event] = curr + dlt_inj_dly

        events_eje = sorted(events_eje)
        if 'InjSI' not in events_eje:
            events_eje.append('InjSI')
        for event in events_eje:
            attr = getattr(c, 'Evt'+event+'_Delay')
            curr = self.get_readback(attr)
            delays[event] = curr + dlt_eje_dly

        injkckr_dly = self.get_readback(c.TrgInjKckr_Delay)
        delays[c.TrgInjKckr_Delay] = injkckr_dly + dlt_eje_dly
        return delays

    def update_ramp_configsetup(self, events_inj, events_eje, delays):
        """Update ramp_configsetup dict."""
        c = ConnTI.Const
        self.ramp_configsetup.update({c.EvtRmpBO_Delay: 0})
        self.ramp_configsetup.update(
            {c.TrgMags_Delay: self._ramp_config.ti_params_ps_ramp_delay})
        self.ramp_configsetup.update(
            {c.TrgCorrs_Delay: self._ramp_config.ti_params_ps_ramp_delay})
        self.ramp_configsetup.update(
            {c.TrgLLRFRmp_Delay: self._ramp_config.ti_params_rf_ramp_delay})
        for events in [events_inj, events_eje]:
            for evt in events:
                attr = getattr(c, 'Evt'+evt+'_Delay')
                self.ramp_configsetup.update({attr: delays[evt]})

    def get_injection_time(self):
        """Return injection time."""
        c = ConnTI.Const
        # curr_linac_dly = self.get_readback(c.EvtLinac_Delay)
        curr_injbo_dly = self.get_readback(c.EvtInjBO_Delay)
        egun_dly = self.get_readback(c.TrgEGunSglBun_Delay) \
            if self.get_readback(c.LinacEgun_SglBun_State) \
            else self.get_readback(c.TrgEGunMultBun_Delay)
        return curr_injbo_dly + egun_dly

    def get_ejection_time(self):
        """Return ejection time."""
        c = ConnTI.Const
        curr_injsi_dly = self.get_readback(c.EvtInjSI_Delay)
        ejekckr_dly = self.get_readback(c.TrgEjeKckr_Delay)
        return curr_injsi_dly + ejekckr_dly

    # --- private methods ---

    def _define_properties(self, prefix, connection_callback, callback):
        c = ConnTI.Const

        mags_db = _get_trig_db(c.TrgMags)
        corrs_db = _get_trig_db(c.TrgCorrs)
        llrf_db = _get_trig_db(c.TrgLLRFRmp)

        self.ramp_basicsetup = {
            # EVG
            c.EVG_DevEnbl: _TIConst.DsblEnbl.Enbl,
            # Mags trigger
            c.TrgMags_State: _TIConst.DsblEnbl.Enbl,
            c.TrgMags_Polarity: _TIConst.TrigPol.Normal,
            c.TrgMags_Src: mags_db['Src-Sel']['enums'].index('RmpBO'),
            c.TrgMags_NrPulses: 1,
            c.TrgMags_Duration: 150.0,       # [us]
            # c.TrgMags_Status: 0,
            # Corrs trigger
            c.TrgCorrs_State: _TIConst.DsblEnbl.Enbl,
            c.TrgCorrs_Polarity: _TIConst.TrigPol.Normal,
            c.TrgCorrs_Src: corrs_db['Src-Sel']['enums'].index('RmpBO'),
            c.TrgCorrs_NrPulses: 1,
            c.TrgCorrs_Duration: 150.0,      # [us]
            # c.TrgCorrs_Status: 0,
            # LLRFRmp trigger
            c.TrgLLRFRmp_State: _TIConst.DsblEnbl.Enbl,
            c.TrgLLRFRmp_Polarity: _TIConst.TrigPol.Normal,
            c.TrgLLRFRmp_Src: llrf_db['Src-Sel']['enums'].index('RmpBO'),
            c.TrgLLRFRmp_NrPulses: 1,
            c.TrgLLRFRmp_Duration: 150.0}    # [us]
        #     c.TrgLLRFRmp_Status: 0}

        self.ramp_configsetup = {
            # Event delays
            c.EvtLinac_Delay: None,          # [us]
            c.EvtInjBO_Delay: None,          # [us]
            c.EvtRmpBO_Delay: None,          # [us]
            c.EvtInjSI_Delay: None,          # [us]
            c.EvtDigLI_Delay: None,          # [us]
            c.EvtDigTB_Delay: None,          # [us]
            c.EvtDigBO_Delay: None,          # [us]
            c.EvtDigTS_Delay: None,          # [us]
            c.EvtDigSI_Delay: None,          # [us]
            c.EvtStudy_Delay: None,          # [us]
            c.TrgInjKckr_Delay: None,        # [us]
            # Mags trigger
            c.TrgMags_Delay: 0.0,           # [us]
            # Corrs trigger
            c.TrgCorrs_Delay: 0.0,          # [us]
            # LLRFRmp trigger
            c.TrgLLRFRmp_Delay: 0.0}        # [us]

        self._evgcontrol_propties = {
            c.EVG_ContinuousEvt: _TIConst.DsblEnbl.Dsbl,
            c.EVG_InjectionEvt: _TIConst.DsblEnbl.Dsbl,
            c.EVG_UpdateEvt: None}

        self._reading_propties = {
            # EGun trigger delays
            c.EVG_FPGAClk: 0,
            c.TrgEGunSglBun_Delay: 0,     # [us]
            c.TrgEGunMultBun_Delay: 0,    # [us]
            # EjeKckr trigger delay
            c.TrgEjeKckr_Delay: 0,        # [us]
            # LinacEgun Mode
            c.LinacEgun_SglBun_State: 0,
            c.LinacEgun_MultBun_State: 0,
            # Intlk
            c.Intlk: 0}

        propty2defaultvalue = self.ramp_basicsetup.copy()
        propty2defaultvalue.update(self.ramp_configsetup)
        propty2defaultvalue.update(self._evgcontrol_propties)
        propty2defaultvalue.update(self._reading_propties)

        properties = list()
        for propty, default_value in propty2defaultvalue.items():
            properties.append(
                _EpicsProperty(propty, prefix, default_value,
                               connection_callback=connection_callback,
                               callback=callback))
        return properties

    def _command(self, setpoints, timeout):
        if self.connected:
            return self.set_setpoints_check(setpoints, timeout=timeout,
                                            rel_tol=0.05, abs_tol=0.008)
        else:
            return False

    def _check(self, readbacks):
        for name, value in readbacks.items():
            if value is None:
                continue
            elif isinstance(value, float):
                if not _math.isclose(value, self.get_readback(name),
                                     abs_tol=0.008):
                    return False
            elif not self.get_readback(name) == value:
                return False
        return True


class ConnPS(_EpicsPropsList):
    """Power supplies connector class."""

    def __init__(self, ramp_config=None, prefix=_PREFIX,
                 connection_callback=None, callback=None):
        """Init."""
        self._ramp_config = ramp_config
        self._get_psnames()
        properties = self._define_properties(prefix, connection_callback,
                                             callback)
        super().__init__(properties)

    @property
    def psnames(self):
        """Return psnames."""
        return self._psnames

    def get_ramp_config(self, ramp_config):
        """Receive BoosterRamp configuration."""
        self._ramp_config = ramp_config

    # --- power supplies commands ---

    def cmd_pwrstate_on(self, timeout=_TIMEOUT_PWRSTATE_ON):
        """Turn all power supplies on."""
        return self._command_all('PwrState-Sel',
                                 _PSConst.PwrStateSel.On,
                                 desired_readback=_PSConst.PwrStateSts.On,
                                 timeout=timeout)

    def cmd_pwrstate_off(self, timeout=_TIMEOUT_PWRSTATE_OFF):
        """Turn all power supplies off."""
        return self._command_all('PwrState-Sel',
                                 _PSConst.PwrStateSel.Off,
                                 desired_readback=_PSConst.PwrStateSts.Off,
                                 timeout=timeout)

    def cmd_opmode_slowref(self, timeout=_TIMEOUT_OPMODE_CHANGE):
        """Select SlowRef opmode for all power supplies."""
        return self._command_all('OpMode-Sel',
                                 _PSConst.OpMode.SlowRef,
                                 desired_readback=_PSConst.States.SlowRef,
                                 timeout=timeout)

    def cmd_opmode_cycle(self, timeout=_TIMEOUT_OPMODE_CHANGE):
        """Select Cycle opmode for all power supplies."""
        return self._command_all('OpMode-Sel',
                                 _PSConst.OpMode.Cycle,
                                 desired_readback=_PSConst.States.Cycle,
                                 timeout=timeout)

    def cmd_opmode_rmpwfm(self, timeout=_TIMEOUT_OPMODE_CHANGE):
        """Select RmpWfm opmode for all power supplies."""
        return self._command_all('OpMode-Sel',
                                 _PSConst.OpMode.RmpWfm,
                                 desired_readback=_PSConst.States.RmpWfm,
                                 timeout=timeout)

    def cmd_wfm(self, psnames=list(), timeout=_TIMEOUT_DFLT):
        """Set wfmdata of all powersupplies."""
        if self._ramp_config is None:
            return False
        pwrsupplys = psnames if psnames else self.psnames
        sp = dict()
        for ps in pwrsupplys:
            sp[ps+':Wfm-SP'] = self._ramp_config.ps_waveform_get_currents(ps)
        return self.set_setpoints_check(sp, timeout=timeout)

    # --- power supplies checks ---

    def check_pwrstate_on(self):
        """Check pwrstates of all power supplies are On."""
        return self._check_all('PwrState-Sel', _PSConst.PwrStateSts.On)

    def check_opmode_slowref(self):
        """Check opmodes of all power supplies ar SlowRef."""
        return self._check_all('OpMode-Sel', _PSConst.OpMode.SlowRef)

    def check_opmode_cycle(self):
        """Check opmodes of all power supplies ar Cycle."""
        return self._check_all('OpMode-Sel', _PSConst.OpMode.Cycle)

    def check_opmode_rmpwfm(self):
        """Check opmodes of all power supplies ar RmpWfm."""
        return self._check_all('OpMode-Sel', _PSConst.OpMode.RmpWfm)

    def check_intlksoft(self):
        """Check if software interlocks are reset."""
        return self._check_all('IntlkSoft-Mon', 0)

    def check_intlkhard(self):
        """Check if hardware interlocks are reset."""
        return self._check_all('IntlkHard-Mon', 0)

    # --- private methods ---

    def _get_psnames(self):
        self._psnames = _PSSearch.get_psnames({'sec': 'BO', 'dis': 'PS'})

    def _define_properties(self, prefix, connection_callback, callback):
        p = prefix
        properties = []
        for psname in self._psnames:
            properties.append(
                _EpicsProperty(psname + ':PwrState-Sel', p,
                               connection_callback=connection_callback,
                               callback=callback))
            properties.append(
                _EpicsProperty(psname + ':OpMode-Sel', p,
                               connection_callback=connection_callback,
                               callback=callback))
            properties.append(
                _EpicsProperty(psname + ':Wfm-SP', p,
                               connection_callback=connection_callback,
                               callback=callback))
            properties.append(
                _EpicsProperty(psname + ':IntlkSoft-Mon', p,
                               connection_callback=connection_callback,
                               callback=callback))
            properties.append(
                _EpicsProperty(psname + ':IntlkHard-Mon', p,
                               connection_callback=connection_callback,
                               callback=callback))
        return properties

    def _command_all(self, prop, setpoint, desired_readback=None,
                     timeout=_TIMEOUT_DFLT):
        """Exec command for all power supplies."""
        sp = dict()
        rb = dict()
        for psname in self.psnames:
            name = psname + ':' + prop
            check_val = desired_readback if desired_readback else setpoint
            if not self._check_pwrsupply(psname, prop, check_val):
                sp[name] = setpoint
                rb[name] = check_val
        return self.set_setpoints_check(setpoints=sp,
                                        desired_readbacks=rb,
                                        timeout=timeout,
                                        abs_tol=1e-5)

    def _check_pwrsupply(self, psname, prop, value):
        """Check a prop of a power supplies for a value."""
        if isinstance(value, (_np.ndarray, float)):
            ok = _np.isclose(self.get_readback(psname + ':' + prop), value,
                             atol=1e-5)
        else:
            ok = self.get_readback(psname + ':' + prop) == value
        if not ok:
            return False
        return True

    def _check_all(self, prop, value):
        """Check a prop of all power supplies for a value."""
        for psname in self.psnames:
            if not self._check_pwrsupply(psname, prop, value):
                return False
        return True


class ConnRF(_EpicsPropsList):
    """RF connector class."""

    class Const(_csdev.Const):
        """Properties names."""

        DevName = 'BR-RF-DLLRF-01'
        Rmp_Enbl = DevName + ':RmpEnbl-Sel'
        Rmp_Ts1 = DevName + ':RmpTs1-SP'
        Rmp_Ts2 = DevName + ':RmpTs2-SP'
        Rmp_Ts3 = DevName + ':RmpTs3-SP'
        Rmp_Ts4 = DevName + ':RmpTs4-SP'
        Rmp_VoltBot = DevName + ':RmpVoltBot-SP'
        Rmp_VoltTop = DevName + ':RmpVoltTop-SP'
        Rmp_PhsBot = DevName + ':RmpPhsBot-SP'
        Rmp_PhsTop = DevName + ':RmpPhsTop-SP'
        Rmp_Intlk = DevName + ':Intlk-Mon'
        Rmp_RmpReady = DevName + ':RmpReady-Mon'

    def __init__(self, ramp_config=None, prefix=_PREFIX,
                 connection_callback=None, callback=None):
        """Init."""
        self._ramp_config = ramp_config
        properties = self._define_properties(prefix, connection_callback,
                                             callback)
        super().__init__(properties)

    def get_ramp_config(self, ramp_config):
        """Receive BoosterRamp configuration."""
        self._ramp_config = ramp_config

    # --- RF commands ---

    def cmd_ramping_enable(self, timeout=_TIMEOUT_DFLT):
        """Turn RF ramping enable."""
        sp = {ConnRF.Const.Rmp_Enbl: ConnRF.Const.DsblEnbl.Enbl}
        return self.set_setpoints_check(sp, timeout=timeout)

    def cmd_ramping_disable(self, timeout=_TIMEOUT_DFLT):
        """Turn RF ramping disable."""
        sp = {ConnRF.Const.Rmp_Enbl: ConnRF.Const.STATE_DISBL}
        return self.set_setpoints_check(sp, timeout=timeout)

    def cmd_config_ramp(self, timeout=_TIMEOUT_DFLT):
        """Apply ramp_config values to RF subsystem."""
        sp = dict()
        c = ConnRF.Const
        sp[c.Rmp_Ts1] = self._ramp_config.rf_ramp_bottom_duration
        sp[c.Rmp_Ts2] = self._ramp_config.rf_ramp_rampup_duration
        sp[c.Rmp_Ts3] = self._ramp_config.rf_ramp_top_duration
        sp[c.Rmp_Ts4] = self._ramp_config.rf_ramp_rampdown_duration
        sp[c.Rmp_VoltBot] = self._ramp_config.rf_ramp_bottom_voltage
        sp[c.Rmp_VoltTop] = self._ramp_config.rf_ramp_top_voltage
        sp[c.Rmp_PhsBot] = self._ramp_config.rf_ramp_bottom_phase
        sp[c.Rmp_PhsTop] = self._ramp_config.rf_ramp_top_phase
        return self.set_setpoints_check(sp, timeout=timeout)

    # --- RF checks ---

    def check_config_ramp(self):
        """Check if configured to ramp."""
        rb = dict()
        c = ConnRF.Const
        rb[c.Rmp_Ts1] = self._ramp_config.rf_ramp_bottom_duration
        rb[c.Rmp_Ts2] = self._ramp_config.rf_ramp_rampup_duration
        rb[c.Rmp_Ts3] = self._ramp_config.rf_ramp_top_duration
        rb[c.Rmp_Ts4] = self._ramp_config.rf_ramp_rampdown_duration
        rb[c.Rmp_VoltBot] = self._ramp_config.rf_ramp_bottom_voltage
        rb[c.Rmp_VoltTop] = self._ramp_config.rf_ramp_top_voltage
        rb[c.Rmp_PhsBot] = self._ramp_config.rf_ramp_bottom_phase
        rb[c.Rmp_PhsTop] = self._ramp_config.rf_ramp_top_phase
        return self._check(rb)

    def check_intlk(self):
        """Check if hardware interlocks are reset."""
        return self._check({ConnRF.Const.Rmp_Intlk: 0})

    def check_rmpready(self):
        """Check if ramp increase was concluded."""
        return self._check({ConnRF.Const.Rmp_Enbl: 1,
                            ConnRF.Const.Rmp_RmpReady: 1})

    # --- private methods ---

    def _define_properties(self, prefix, connection_callback, callback):
        c = ConnRF.Const
        propty2defaultvalue = {
            c.Rmp_Enbl: ConnRF.Const.DsblEnbl.Enbl,
            c.Rmp_Ts1: _rutil.DEFAULT_RF_RAMP_BOTTOM_DURATION,
            c.Rmp_Ts2: _rutil.DEFAULT_RF_RAMP_RAMPUP_DURATION,
            c.Rmp_Ts3: _rutil.DEFAULT_RF_RAMP_TOP_DURATION,
            c.Rmp_Ts4: _rutil.DEFAULT_RF_RAMP_RAMPDOWN_DURATION,
            c.Rmp_VoltBot: _rutil.DEFAULT_RF_RAMP_BOTTOM_VOLTAGE,
            c.Rmp_VoltTop: _rutil.DEFAULT_RF_RAMP_TOP_VOLTAGE,
            c.Rmp_PhsBot: _rutil.DEFAULT_RF_RAMP_BOTTOM_PHASE,
            c.Rmp_PhsTop: _rutil.DEFAULT_RF_RAMP_TOP_PHASE,
            c.Rmp_Intlk: None,
            c.Rmp_RmpReady: None}

        properties = list()
        for propty, default_value in propty2defaultvalue.items():
            properties.append(
                _EpicsProperty(propty, prefix, default_value,
                               connection_callback=connection_callback,
                               callback=callback))
        return properties

    def _check(self, readbacks):
        for name, value in readbacks.items():
            if value is None:
                continue
            if not self.get_readback(name) == value:
                return False
        return True


class ConnSOFB(_EpicsPropsList):
    """SOFB connector class."""

    IOC_PREFIX = 'BO-Glob:AP-SOFB'

    def __init__(self, prefix=_PREFIX,
                 connection_callback=None, callback=None):
        """Init."""
        properties = self._define_properties(prefix, connection_callback,
                                             callback)
        super().__init__(properties)

    def get_deltakicks(self):
        """Get CH and CV delta kicks calculated by SOFB."""
        bo_sofb_db = _SOFBRings(acc='BO')
        rb = self.readbacks
        ch_dkicks = rb[ConnSOFB.IOC_PREFIX + ':DeltaKickCH-Mon']
        ch_names = bo_sofb_db.ch_names

        cv_dkicks = rb[ConnSOFB.IOC_PREFIX + ':DeltaKickCV-Mon']
        cv_names = bo_sofb_db.cv_names

        corrs2dkicks_dict = dict()
        for idx in range(len(ch_names)):
            corrs2dkicks_dict[ch_names[idx]] = ch_dkicks[idx]
        for idx in range(len(cv_names)):
            corrs2dkicks_dict[cv_names[idx]] = cv_dkicks[idx]
        return corrs2dkicks_dict

    def _define_properties(self, prefix, connection_callback, callback):
        properties = list()
        for ppty in ['DeltaKickCH-Mon', 'DeltaKickCV-Mon']:
            properties.append(
                _EpicsProperty(ConnSOFB.IOC_PREFIX + ':' + ppty, prefix,
                               connection_callback=connection_callback,
                               callback=callback))
        return properties

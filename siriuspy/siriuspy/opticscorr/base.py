"""Base module of AS-AP-OpticsCorr IOC."""

import time as _time
from copy import deepcopy as _dcopy
from threading import Thread as _Thread
import numpy as _np
from epics import PV as _PV

from .. import util as _util
from ..callbacks import Callback as _Callback
from ..envars import VACA_PREFIX as _vaca_prefix
from ..namesys import SiriusPVName as _SiriusPVName
from ..search import LLTimeSearch as _LLTimeSearch
from ..clientconfigdb import ConfigDBClient as _ConfigDBClient, \
    ConfigDBException as _ConfigDBException
from ..pwrsupply.csdev import Const as _PSConst
from ..timesys.csdev import Const as _TIConst, \
    get_hl_trigger_database as _get_trig_db

from .opticscorr import OpticsCorr as _OpticsCorr
from .csdev import Const as _Const, \
    get_chrom_database as _get_chrom_database, \
    get_tune_database as _get_tune_database
from .utils import HandleConfigNameFile as _HandleConfigNameFile

# Constants
ALLSET = 0x1f
ALLCLR_SYNCON = 0x00
ALLCLR_SYNCOFF = 0x10


class BaseApp(_Callback):
    """Main application for handling optics correction."""

    _optics_param = ''

    def __init__(self, acc):
        """Class constructor."""
        super().__init__()
        self._acc = acc.upper()

        # consts
        if self._optics_param == 'tune':
            self._pvs_database = _get_tune_database(self._acc)
            if self._acc == 'BO':
                self._psfams = _Const.BO_QFAMS_TUNECORR
                self._psfam_nelm = _Const.BO_QFAMS_NELM
            else:
                self._psfams = _Const.SI_QFAMS_TUNECORR
                self._psfam_nelm = _Const.SI_QFAMS_NELM
                self._trigger_name = 'SI-Glob:TI-Mags-Quads'
                self._event_name = 'TunSI'
        else:
            self._pvs_database = _get_chrom_database(self._acc)
            if self._acc == 'BO':
                self._psfams = _Const.BO_SFAMS_CHROMCORR
                self._psfam_nelm = _Const.BO_SFAMS_NELM
            else:
                self._psfams = _Const.SI_SFAMS_CHROMCORR
                self._psfam_nelm = _Const.SI_SFAMS_NELM
                self._trigger_name = 'SI-Glob:TI-Mags-Sexts'
                self._event_name = 'ChromSI'

        self._status = ALLSET if self._acc == 'SI' else 0x0f

        self._optprm_est = [0.0, 0.0]

        self._apply_corr_cmd_count = 0
        self._config_ps_cmd_count = 0

        self._psfam_check_connection = {fam: 0 for fam in self._psfams}
        self._psfam_check_pwrstate_sts = {fam: 0 for fam in self._psfams}
        self._psfam_check_opmode_sts = {fam: -1 for fam in self._psfams}
        self._psfam_check_ctrlmode_mon = {fam: 1 for fam in self._psfams}
        self._psfam_intstr_rb = {fam: 0 for fam in self._psfams}

        if self._acc == 'SI':
            self._corr_method = _Const.CorrMeth.Proportional
            self._corr_group = _Const.CorrGroup.TwoKnobs
            self._sync_corr = _Const.SyncCorr.Off

            self._config_ti_cmd_count = 0
            self._timing_check_config = 9*[0]

            self._measuring_config = False
            self._meas_config_status = _Const.MeasMon.Idle
            self._meas_config_lastcomm = _Const.MeasCmd.Reset
            self._meas_config_wait = 1
            self._meas_config_name = 'UNDEF'
            self._meas_config_2_save = None
            self._meas_config_save_cmd_count = 0

            self._is_storedebeam = 0
        else:
            self._corr_method = _Const.CorrMeth.Additional
            self._corr_group = _Const.CorrGroup.TwoKnobs
            self._sync_corr = _Const.SyncCorr.Off

        # Get focusing and defocusing families
        psfam_focusing = []
        psfam_defocusing = []
        ps_focus_type = 'QF' if self._optics_param == 'tune' else 'SF'
        for fam in self._psfams:
            if ps_focus_type in fam:
                psfam_focusing.append(fam)
            else:
                psfam_defocusing.append(fam)
        psfam_focusing = tuple(psfam_focusing)
        psfam_defocusing = tuple(psfam_defocusing)

        # Initialize correction parameters from local file and configdb
        self.cn_handler = _HandleConfigNameFile(self._acc, self._optics_param)
        self.cdb_client = _ConfigDBClient(
            config_type=self._acc.lower()+'_'+self._optics_param+'corr_params')
        [done, corrparams] = self._get_corrparams()
        if done:
            self._config_name = corrparams[0]
            self._nominal_matrix = corrparams[1]
            self._psfam_nom_intstr = corrparams[2]
            self._nominal_opticsparam = corrparams[3]
            self._opticscorr = _OpticsCorr(
                magnetfams_ordering=self._psfams,
                nominal_matrix=self._nominal_matrix,
                nominal_intstrengths=self._psfam_nom_intstr,
                nominal_opticsparam=self._nominal_opticsparam,
                magnetfams_focusing=psfam_focusing,
                magnetfams_defocusing=psfam_defocusing)
        else:
            raise Exception(
                "Could not read correction parameters from configdb.")

        # Connect to Quadrupoles Families
        self._psfam_intstr_sp_pvs = dict()
        self._psfam_intstr_rb_pvs = dict()
        self._psfam_pwrstate_sel_pvs = dict()
        self._psfam_pwrstate_sts_pvs = dict()
        self._psfam_opmode_sel_pvs = dict()
        self._psfam_opmode_sts_pvs = dict()
        self._psfam_ctrlmode_mon_pvs = dict()
        for fam in self._psfams:
            pss = _SiriusPVName(_vaca_prefix+self._acc+'-Fam:PS-'+fam)
            intstr = 'KL' if self._optics_param == 'tune' else 'SL'
            self._psfam_intstr_sp_pvs[fam] = _PV(
                pss.substitute(propty_name=intstr, propty_suffix='SP'),
                connection_callback=self._callback_conn_psfam,
                connection_timeout=0.05)

            self._psfam_pwrstate_sel_pvs[fam] = _PV(
                pss.substitute(propty_name='PwrState', propty_suffix='Sel'),
                connection_timeout=0.05)
            self._psfam_pwrstate_sts_pvs[fam] = _PV(
                pss.substitute(propty_name='PwrState', propty_suffix='Sts'),
                callback=self._callback_psfam_pwrstate_sts,
                connection_timeout=0.05)

            self._psfam_opmode_sel_pvs[fam] = _PV(
                pss.substitute(propty_name='OpMode', propty_suffix='Sel'),
                connection_timeout=0.05)
            self._psfam_opmode_sts_pvs[fam] = _PV(
                pss.substitute(propty_name='OpMode', propty_suffix='Sts'),
                callback=self._callback_psfam_opmode_sts,
                connection_timeout=0.05)

            self._psfam_ctrlmode_mon_pvs[fam] = _PV(
                pss.substitute(propty_name='CtrlMode', propty_suffix='Mon'),
                callback=self._callback_psfam_ctrlmode_mon,
                connection_timeout=0.05)

        if self._acc == 'SI':
            # Connect to Timing
            trig_name = self._trigger_name
            evt_name = self._event_name
            try:
                trig_db = _get_trig_db(trig_name)
                self._evt_src_idx = trig_db['Src-Sel']['enums'].index(evt_name)
            except (KeyError, ValueError):
                self._evt_src_idx = 1

            self._trigger_state_sel = _PV(
                _vaca_prefix+trig_name+':State-Sel', connection_timeout=0.05)
            self._trigger_state_sts = _PV(
                _vaca_prefix+trig_name+':State-Sts',
                callback=self._callback_timing_state, connection_timeout=0.05)

            self._trigger_polarity_sel = _PV(
                _vaca_prefix+trig_name+':Polarity-Sel',
                connection_timeout=0.05)
            self._trigger_polarity_sts = _PV(
                _vaca_prefix+trig_name+':Polarity-Sts',
                callback=self._callback_timing_state, connection_timeout=0.05)

            self._trigger_src_sel = _PV(
                _vaca_prefix+trig_name+':Src-Sel', connection_timeout=0.05)
            self._trigger_src_sts = _PV(
                _vaca_prefix+trig_name+':Src-Sts',
                callback=self._callback_timing_state, connection_timeout=0.05)

            self._trigger_nrpulses_sp = _PV(
                _vaca_prefix+trig_name+':NrPulses-SP',
                connection_timeout=0.05)
            self._trigger_nrpulses_rb = _PV(
                _vaca_prefix+trig_name+':NrPulses-RB',
                callback=self._callback_timing_state, connection_timeout=0.05)

            self._trigger_duration_sp = _PV(
                _vaca_prefix+trig_name+':Duration-SP',
                connection_timeout=0.05)
            self._trigger_duration_rb = _PV(
                _vaca_prefix+trig_name+':Duration-RB',
                callback=self._callback_timing_state, connection_timeout=0.05)

            self._trigger_delay_sp = _PV(
                _vaca_prefix+trig_name+':Delay-SP', connection_timeout=0.05)
            self._trigger_delay_rb = _PV(
                _vaca_prefix+trig_name+':Delay-RB',
                callback=self._callback_timing_state, connection_timeout=0.05)

            evg = _LLTimeSearch.get_evg_name()
            self._event_mode_sel = _PV(
                _vaca_prefix+evg+':'+evt_name+'Mode-Sel',
                connection_timeout=0.05)
            self._event_mode_sts = _PV(
                _vaca_prefix+evg+':'+evt_name+'Mode-Sts',
                callback=self._callback_timing_state, connection_timeout=0.05)

            self._event_delaytype_sel = _PV(
                _vaca_prefix+evg+':'+evt_name+'DelayType-Sel',
                connection_timeout=0.05)
            self._event_delaytype_sts = _PV(
                _vaca_prefix+evg+':'+evt_name+'DelayType-Sts',
                callback=self._callback_timing_state, connection_timeout=0.05)

            self._event_delay_sp = _PV(
                _vaca_prefix+evg+':'+evt_name+'Delay-SP',
                connection_timeout=0.05)
            self._event_delay_rb = _PV(
                _vaca_prefix+evg+':'+evt_name+'Delay-RB',
                callback=self._callback_timing_state, connection_timeout=0.05)

            self._event_exttrig_cmd = _PV(
                _vaca_prefix+evg+':'+evt_name+'ExtTrig-Cmd',
                connection_timeout=0.05)

            # Connect to CurrInfo
            self._storedebeam_pv = _PV(
                _vaca_prefix+'SI-Glob:AP-CurrInfo:StoredEBeam-Mon',
                callback=self._callback_get_storedebeam,
                connection_timeout=0.05)

            # Connect to Tunes
            self._tune_x_pv = _PV(
                _vaca_prefix+'SI-Glob:DI-Tune-H:TuneFrac-Mon',
                connection_timeout=0.05)
            self._tune_y_pv = _PV(
                _vaca_prefix+'SI-Glob:DI-Tune-V:TuneFrac-Mon',
                connection_timeout=0.05)

        # Create map of pv -> write function
        self.map_pv2write = {
            'ApplyDelta-Cmd': self.cmd_apply_corr,
            'ConfigName-SP': self.set_config_name,
            'CorrMeth-Sel': self.set_corr_meth,
            'CorrGroup-Sel': self.set_corr_group,
            'SyncCorr-Sel': self.set_sync_corr,
            'ConfigPS-Cmd': self.cmd_config_ps,
            'ConfigTiming-Cmd': self.cmd_config_ti,
            'MeasConfigWait-SP': self.set_meas_config_wait,
            'MeasConfig-Cmd': self.cmd_meas_config,
            'MeasConfigName-SP': self.set_meas_config_name,
            'MeasConfigSave-Cmd': self.cmd_meas_config_save,
        }

    def init_database(self):
        """Set initial PV values."""
        self.run_callbacks('ConfigName-SP', self._config_name)
        self.run_callbacks('ConfigName-RB', self._config_name)
        self.update_corrparams_pvs()
        self.run_callbacks('Log-Mon', 'Started.')
        self.run_callbacks('Status-Mon', self._status)
        if self._optics_param == 'tune':
            for fam in self._psfams:
                self.run_callbacks(
                    'RefKL'+fam+'-Mon', self._psfam_refkl[fam])
            self.run_callbacks('DeltaTuneX-Mon', self._optprm_est[0])
            self.run_callbacks('DeltaTuneY-Mon', self._optprm_est[1])
        else:
            self.run_callbacks('ChromX-Mon', self._optprm_est[0])
            self.run_callbacks('ChromY-Mon', self._optprm_est[1])

    def update_corrparams_pvs(self):
        """Set initial correction parameters PVs values."""
        raise NotImplementedError

    @property
    def pvs_database(self):
        """Return PVs database."""
        return self._pvs_database

    def process(self, interval):
        """Sleep."""
        _time.sleep(interval)

    def write(self, reason, value):
        """Write value to reason and let callback update PV database."""
        if reason in self.map_pv2write.keys():
            status = self.map_pv2write[reason](value)
        else:
            status = False
        return status

    # ------ handle pv write methods -------

    def cmd_apply_corr(self, value):
        """ApplyCorr command."""
        if self._apply_corr():
            self._apply_corr_cmd_count += 1
            self.run_callbacks('ApplyDelta-Cmd', self._apply_corr_cmd_count)
        return False

    def set_config_name(self, value):
        """Set configuration name."""
        [done, corrparams] = self._get_corrparams(value)
        if done:
            try:
                self._opticscorr.nominal_matrix = corrparams[1]
                self._opticscorr.nominal_intstrengths = corrparams[2]
                self._opticscorr.nominal_opticsparam = corrparams[3]
                self._calc_intstrength()
            except Exception:
                self.run_callbacks(
                    'Log-Mon', 'Could not update correction parameters.')
                return False
            else:
                self._config_name = corrparams[0]
                self.cn_handler.set_config_name(self._config_name)
                self.run_callbacks('ConfigName-RB', self._config_name)

                self._nominal_matrix = corrparams[1]
                self._psfam_nom_intstr = corrparams[2]
                self._nominal_opticsparam = corrparams[3]
                self.update_corrparams_pvs()
                self.run_callbacks('Log-Mon', 'Updated correction parameters.')
                return True
        self.run_callbacks('Log-Mon', 'ERR: Config not found in configdb.')
        return False

    def set_corr_meth(self, value):
        """Set CorrMeth."""
        if value == self._corr_method:
            return False
        self._corr_method = value
        self.run_callbacks('CorrMeth-Sts', value)
        self._calc_intstrength()
        return True

    def set_corr_group(self, value):
        """Set CorrGroup."""
        if value == self._corr_group:
            return False
        self._corr_group = value
        self.run_callbacks('CorrGroup-Sts', self._corr_group)
        self._calc_intstrength()
        return True

    def set_sync_corr(self, value):
        """Set SyncCorr."""
        if self._meas_config_status == _Const.MeasMon.Measuring:
            self.run_callbacks(
                'Log-Mon', 'ERR: Configuration measurement in progress.')
            return False
        if value == self._sync_corr:
            return False

        self._sync_corr = value

        if self._config_ps():
            self._config_ps_cmd_count += 1
            self.run_callbacks('ConfigPS-Cmd', self._config_ps_cmd_count)

        if value == 1:
            if self._config_timing():
                self._config_ti_cmd_count += 1
                self.run_callbacks(
                    'ConfigTiming-Cmd', self._config_ti_cmd_count)

        val = 1
        if (self._status & 0x1) == 0:
            for fam in self._psfams:
                self._psfam_check_opmode_sts[fam] = \
                    self._psfam_opmode_sts_pvs[fam].value

            opmode = _PSConst.OpMode.SlowRefSync if value \
                else _PSConst.OpMode.SlowRef
            val = any(op != opmode for op in
                      self._psfam_check_opmode_sts.values())

        self._status = _util.update_bit(
            v=self._status, bit_pos=2, bit_val=val)

        self.run_callbacks('Status-Mon', self._status)
        self.run_callbacks('SyncCorr-Sts', self._sync_corr)
        return True

    def cmd_config_ps(self, value):
        """ConfigPS command."""
        if self._config_ps():
            self._config_ps_cmd_count += 1
            self.run_callbacks('ConfigPS-Cmd', self._config_ps_cmd_count)
        return False

    def cmd_config_ti(self, value):
        """ConfigTiming command."""
        if self._config_timing():
            self._config_ti_cmd_count += 1
            self.run_callbacks('ConfigTiming-Cmd', self._config_ti_cmd_count)
        return False

    def set_meas_config_wait(self, value):
        """Set MeasConfigWait."""
        if value == self._meas_config_wait:
            return False
        self._meas_config_wait = value
        self.run_callbacks('MeasConfigWait-RB', value)
        return True

    def cmd_meas_config(self, value):
        """MeasConfig command."""
        if value == _Const.MeasCmd.Start:
            status = self._start_meas_config()
        elif value == _Const.MeasCmd.Stop:
            status = self._stop_meas_config()
        elif value == _Const.MeasCmd.Reset:
            status = self._reset_meas_config()
        if status:
            self._meas_config_lastcomm = value
        return status

    def set_meas_config_name(self, value):
        """Set MeasConfigName."""
        if value == self._meas_config_name:
            return False
        if not self.cdb_client.check_valid_configname(value):
            self.run_callbacks('Log-Mon', 'ERR: Config name not valid!')
            return False
        self._meas_config_name = value
        self.run_callbacks('MeasConfigName-RB', value)
        return True

    def cmd_meas_config_save(self, value):
        """MeasConfigSave command."""
        if self._meas_config_2_save is None:
            self.run_callbacks(
                'Log-Mon', 'ERR: No new data to save in configdb!')
        elif self._save_corrparams(self._meas_config_name):
            self._meas_config_save_cmd_count += 1
            self.run_callbacks(
                'MeasConfigSave-Cmd', self._meas_config_save_cmd_count)

            self._config_name = _dcopy(self._meas_config_name)
            self.cn_handler.set_config_name(self._config_name)
            self.run_callbacks('ConfigName-RB', self._config_name)

            self._meas_config_name = 'UNDEF'
            self.run_callbacks('MeasConfigName-SP', self._meas_config_name)
            self.run_callbacks('MeasConfigName-RB', self._meas_config_name)

            self.run_callbacks('Log-Mon', 'Updated config. name.')
        return False

    # ---------- auxiliar methods ----------

    def _get_corrparams(self, config_name=''):
        """Get response matrix from configurations database."""
        try:
            if not config_name:
                config_name = self.cn_handler.get_config_name()
            params = self.cdb_client.get_config_value(name=config_name)
        except _ConfigDBException:
            return [False, []]
        else:
            data = list()
            data.append(config_name)
            data.extend(self._handle_corrparams_2_read(params))
            return [True, data]

    def _handle_corrparams_2_read(self, params):
        """Edit correction params."""
        raise NotImplementedError

    def _save_corrparams(self, config_name):
        """Save correction parameters in configdb."""
        value = self._handle_corrparams_2_save()
        try:
            self.cdb_client.insert_config(name=config_name, value=value)
        except _ConfigDBException as err:
            self._meas_config_2_save = value
            if err.server_code == -2:
                log_msg = 'ERR: Could not connect to configdb!'
            else:
                log_msg = 'ERR: Could not save configuration in configdb!'
        else:
            self._meas_config_2_save = None
            log_msg = "Saved config. '{}' in configdb!".format(config_name)
        self.run_callbacks('Log-Mon', log_msg)
        return 'ERR' not in log_msg

    def _handle_corrparams_2_save(self):
        """Handle configuration value to save."""
        raise NotImplementedError

    def _is_status_ok(self):
        """Return if status is OK."""
        if self._sync_corr == _Const.SyncCorr.Off:
            is_ok = self._status in (ALLCLR_SYNCOFF, ALLCLR_SYNCON)
        else:
            is_ok = self._status == ALLCLR_SYNCON
        return is_ok

    def _calc_intstrength(self):
        """Calculate integrated strength."""
        raise NotImplementedError

    def _apply_intstrength(self, int_strengths):
        """Apply integrated strength."""
        for fam, pvobj in self._psfam_intstr_sp_pvs.items():
            pvobj.put(int_strengths[fam])

    def _apply_corr(self):
        """Apply correction."""
        raise NotImplementedError

    def _config_ps(self):
        """Configurate power supplies."""
        opmode = _PSConst.OpMode.SlowRefSync if self._sync_corr \
            else _PSConst.OpMode.SlowRef
        for fam in self._psfams:
            if self._psfam_pwrstate_sel_pvs[fam].connected:
                self._psfam_pwrstate_sel_pvs[fam].put(_PSConst.PwrStateSel.On)
                self._psfam_opmode_sel_pvs[fam].put(opmode)
            else:
                self.run_callbacks('Log-Mon', 'ERR:'+fam+' is disconnected.')
                return False
        self.run_callbacks('Log-Mon', 'Configuration sent to power supplies.')
        return True

    def _config_timing(self):
        """Configurate Timing."""
        conn = not any(pv.connected is False for pv in [
            self._trigger_state_sel,
            self._trigger_polarity_sel,
            self._trigger_src_sel,
            self._trigger_nrpulses_sp,
            self._trigger_duration_sp,
            self._trigger_delay_sp,
            self._event_mode_sel,
            self._event_delaytype_sel,
            self._event_delay_sp])
        if conn:
            self._trigger_state_sel.put(_TIConst.DsblEnbl.Enbl)
            self._trigger_polarity_sel.put(_TIConst.TrigPol.Normal)
            self._trigger_src_sel.put(self._evt_src_idx)
            self._trigger_nrpulses_sp.put(1)
            self._trigger_duration_sp.put(150)
            self._trigger_delay_sp.put(0)
            self._event_mode_sel.put(_TIConst.EvtModes.External)
            self._event_delaytype_sel.put(_TIConst.EvtDlyTyp.Incr)
            self._event_delay_sp.put(0)

            self.run_callbacks('Log-Mon', 'Configuration sent to TI.')
            return True
        else:
            self.run_callbacks('Log-Mon', 'ERR:Some TI PV is disconnected.')
            return False

    def _get_tunes(self):
        """Return tunes."""
        if self._tune_x_pv.connected:
            sts = True
            tunex = self._tune_x_pv.value
            tuney = self._tune_y_pv.value
        else:
            sts = False
            tunex, tuney = [0, 0]
        return sts, [tunex, tuney]

    def _get_optics_param(self):
        """Get nominal optics parameter."""
        raise NotImplementedError

    def _get_delta_intstrength(self, fam):
        """Get delta integrated strengths."""
        raise NotImplementedError

    def _start_meas_config(self):
        """Start configuration measurement."""
        cont = True
        if self._sync_corr == _Const.SyncCorr.On:
            log_msg = 'ERR: Turn off syncronized correction!'
            cont = False
        elif self._meas_config_name == 'UNDEF':
            log_msg = 'ERR: Define a conf.name to save the measure!'
            cont = False
        elif self._status != 0:
            log_msg = 'ERR: Verify power supplies status!'
            cont = False
        elif self._measuring_config:
            log_msg = 'ERR: Measurement already in progress!'
            cont = False
        elif not self._is_storedebeam:
            log_msg = 'ERR: Cannot measure, there is not stored beam!'
            cont = False
        elif not self._tune_x_pv.connected or not self._tune_y_pv.connected:
            log_msg = 'ERR: Cannot measure, tune PVs not connected!'
            cont = False
        if not cont:
            self.run_callbacks('Log-Mon', log_msg)
            return False

        self.run_callbacks(
            'Log-Mon', 'Starting correction config measurement!')
        self._measuring_config = True
        thread = _Thread(target=self._meas_config_thread, daemon=True)
        thread.start()
        return True

    def _stop_meas_config(self):
        """Stop configuration measurement."""
        if not self._measuring_config:
            self.run_callbacks('Log-Mon', 'ERR: No measurement occuring!')
            return False
        self.run_callbacks('Log-Mon', 'Aborting config measurement!')
        self._measuring_config = False
        return True

    def _reset_meas_config(self):
        """Reset configuration measurement."""
        if self._measuring_config:
            self.run_callbacks(
                'Log-Mon', 'WARN: Status not reset, measurement in progress!')
            return False
        self.run_callbacks('Log-Mon', 'Reseting measurement status!')
        self._meas_config_status = _Const.MeasMon.Idle
        self.run_callbacks('MeasConfigStatus-Mon', self._meas_config_status)
        return True

    def _meas_config_thread(self):
        """Configuration measurement thread."""
        self._meas_config_status = _Const.MeasMon.Measuring
        self.run_callbacks('MeasConfigStatus-Mon', self._meas_config_status)

        respm = _np.zeros((2, len(self._psfams)), dtype=float)
        fams_intstr0 = {
            fam: self._psfam_intstr_rb[fam] for fam in self._psfams}
        fams_intstr = _dcopy(fams_intstr0)

        aborted = False
        if self._optics_param == 'chrom':
            sts, data = self._get_optics_param()
            if sts:
                self._nominal_opticsparam = data
            else:
                log_msg = 'ERR: Could not measure chrom!'
                aborted = True

        for fam in self._psfams:
            if not self._measuring_config:
                log_msg = 'Stoped measurement!'
                aborted = True
            elif not self._is_storedebeam:
                log_msg = 'ERR: Stoping measurement, there is no stored beam!'
                aborted = True
            elif self._status != 0:
                log_msg = 'ERR: Stoping measurement, verify power supplies!'
                aborted = True
            elif not self._tune_x_pv.connected or \
                    not self._tune_y_pv.connected:
                log_msg = 'ERR: Stoping measurement, tune PVs not connected!'
                aborted = True

            if aborted:
                break

            fam_idx = self._psfams.index(fam)
            self.run_callbacks(
                'Log-Mon', 'Step: {0:d}/{1:d} --> {2:s}'.format(
                    fam_idx+1, len(self._psfams), fam))

            delta = self._get_delta_intstrength(fam)

            fams_intstr[fam] = fams_intstr0[fam] + delta/2
            self._apply_intstrength(fams_intstr)
            _time.sleep(self._meas_config_wait)
            sts, data = self._get_optics_param()
            if sts:
                param_pos_x, param_pos_y = data
            else:
                log_msg = 'ERR: Could not measure '+self._optics_param+'!'
                aborted = True
                break

            fams_intstr[fam] = fams_intstr0[fam] - delta/2
            self._apply_intstrength(fams_intstr)
            _time.sleep(self._meas_config_wait)
            sts, data = self._get_optics_param()
            if sts:
                param_neg_x, param_neg_y = data
            else:
                log_msg = 'ERR: Could not measure '+self._optics_param+'!'
                aborted = True
                break

            respm[0, fam_idx] = (param_pos_x-param_neg_x)/delta
            respm[1, fam_idx] = (param_pos_y-param_neg_y)/delta

            fams_intstr[fam] = fams_intstr0[fam]
            self._apply_intstrength(fams_intstr)

        self.run_callbacks(
            'Log-Mon', 'Ensure power supplies return to initial values...')
        self._apply_intstrength(fams_intstr0)

        if aborted:
            self._meas_config_status = _Const.MeasMon.Aborted
        else:
            self._meas_config_status = _Const.MeasMon.Completed
            log_msg = 'Correction configuration measurement completed!'

        self.run_callbacks('MeasConfigStatus-Mon', self._meas_config_status)
        self._measuring_config = False
        self.run_callbacks('Log-Mon', log_msg)

        # update corrparams
        self._nominal_matrix = respm.flatten().tolist()
        self._psfam_nom_intstr = [fams_intstr0[fam] for fam in self._psfams]
        self.update_corrparams_pvs()

        try:
            self._opticscorr.nominal_matrix = self._nominal_matrix
            self._opticscorr.nominal_intstrengths = self._psfam_nom_intstr
            self._opticscorr.nominal_opticsparam = self._nominal_opticsparam
            self._calc_intstrength()
            self.run_callbacks('Log-Mon', 'New correction parameters in use.')
        except Exception:
            self._meas_config_2_save = self._handle_corrparams_2_save()
            self.run_callbacks('Log-Mon', 'ERR: Could not use new parameters.')
            self.run_callbacks('Log-Mon', 'ERR: Will not save new parameters.')
        else:
            if self._save_corrparams(self._meas_config_name):
                # update configname
                self._config_name = _dcopy(self._meas_config_name)
                self.cn_handler.set_config_name(self._config_name)
                self.run_callbacks('ConfigName-RB', self._config_name)

                self._meas_config_name = 'UNDEF'
                self.run_callbacks('MeasConfigName-SP', self._meas_config_name)
                self.run_callbacks('MeasConfigName-RB', self._meas_config_name)

    # ---------- callbacks ----------

    def _callback_conn_psfam(self, pvname, conn, **kws):
        """Connection callback."""
        if not conn:
            self.run_callbacks('Log-Mon', 'WARN:'+pvname+' disconnected.')

        fam = _SiriusPVName(pvname).dev
        self._psfam_check_connection[fam] = (1 if conn else 0)

        # Change the first bit of correction status
        self._status = _util.update_bit(
            v=self._status, bit_pos=0,
            bit_val=any(v == 0 for v in self._psfam_check_connection.values()))
        self.run_callbacks('Status-Mon', self._status)

    def _callback_psfam_pwrstate_sts(self, pvname, value, **kws):
        """Callback."""
        if value != _PSConst.PwrStateSts.On:
            self.run_callbacks('Log-Mon', 'WARN:'+pvname+' is not On.')

        fam = _SiriusPVName(pvname).dev
        self._psfam_check_pwrstate_sts[fam] = value

        # Change the second bit of correction status
        self._status = _util.update_bit(
            v=self._status, bit_pos=1,
            bit_val=any(v != _PSConst.PwrStateSts.On
                        for v in self._psfam_check_pwrstate_sts.values()))
        self.run_callbacks('Status-Mon', self._status)

    def _callback_psfam_opmode_sts(self, pvname, value, **kws):
        """Callback."""
        self.run_callbacks('Log-Mon', 'WARN:'+pvname+' changed.')

        fam = _SiriusPVName(pvname).dev
        self._psfam_check_opmode_sts[fam] = value

        # Change the third bit of correction status
        opmode = _PSConst.States.SlowRefSync if self._sync_corr \
            else _PSConst.States.SlowRef
        self._status = _util.update_bit(
            v=self._status, bit_pos=2,
            bit_val=any(v != opmode for v in
                        self._psfam_check_opmode_sts.values()))
        self.run_callbacks('Status-Mon', self._status)

    def _callback_psfam_ctrlmode_mon(self, pvname, value, **kws):
        """Callback."""
        if value != _PSConst.Interface.Remote:
            self.run_callbacks('Log-Mon', 'WARN:'+pvname+' is not Remote.')

        fam = _SiriusPVName(pvname).dev
        self._psfam_check_ctrlmode_mon[fam] = value

        # Change the fourth bit of correction status
        self._status = _util.update_bit(
            v=self._status, bit_pos=3,
            bit_val=any(v != _PSConst.Interface.Remote
                        for v in self._psfam_check_ctrlmode_mon.values()))
        self.run_callbacks('Status-Mon', self._status)

    def _callback_timing_state(self, pvname, value, **kws):
        """Callback."""
        if self._trigger_name+':State' in pvname:
            self._timing_check_config[0] = (value == _TIConst.DsblEnbl.Enbl)
        elif self._trigger_name+':Polarity' in pvname:
            self._timing_check_config[1] = (value == _TIConst.TrigPol.Normal)
        elif self._trigger_name+':Src' in pvname:
            self._timing_check_config[2] = (value == self._evt_src_idx)
        elif self._trigger_name+':NrPulses' in pvname:  # 1 pulse
            self._timing_check_config[3] = (value == 1)
        elif self._trigger_name+':Duration' in pvname:  # 150us
            self._timing_check_config[4] = _np.isclose(value, 150, atol=0.1)
        elif self._trigger_name+':Delay' in pvname:  # 0us
            self._timing_check_config[5] = _np.isclose(value, 0, atol=0.1)
        elif self._event_name+'Mode' in pvname:
            self._timing_check_config[6] = value == _TIConst.EvtModes.External
        elif self._event_name+'DelayType' in pvname:
            self._timing_check_config[7] = value == _TIConst.EvtDlyTyp.Incr
        elif self._event_name+'Delay' in pvname:  # 0us
            self._timing_check_config[8] = _np.isclose(value, 0, atol=0.1)

        # Change the fifth bit of correction status
        if self._sync_corr == _Const.SyncCorr.Off:
            bit_val = 0
        else:
            bit_val = any(idx == 0 for idx in self._timing_check_config)
        self._status = _util.update_bit(
            v=self._status, bit_pos=4, bit_val=bit_val)
        self.run_callbacks('Status-Mon', self._status)

    def _callback_get_storedebeam(self, value, **kws):
        """Callback."""
        if value == 0:
            self.run_callbacks('Log-Mon', 'WARN: There is no stored beam!')
        self._is_storedebeam = value

"""Main module of AS-AP-ChromCorr IOC."""

import time as _time
from threading import Thread as _Thread
import numpy as _np
from epics import PV as _PV
from epics.ca import ChannelAccessGetFailure as _ChannelAccessGetFailure

from ..envars import VACA_PREFIX as _vaca_prefix
from ..namesys import SiriusPVName as _SiriusPVName
from ..devices import RFGen

from .csdev import Const as _Const
from .base import BaseApp as _BaseApp

_MOM_COMPACT = 1.68e-4


class ChromCorrApp(_BaseApp):
    """Main application for handling chromaticity correction."""

    _optics_param = 'chrom'

    def __init__(self, acc):
        """Class constructor."""
        super().__init__(acc)

        # consts
        self._chrom_sp = 2*[0.0]
        self._deltachrom_sp = 2*[0.0]
        self._chrom_mon = 2*[0.0]
        self._last_param_set = 'abs'

        if self._acc == 'SI':
            self._measuring_chrom = False
            self._meas_chrom_status = _Const.MeasMon.Idle
            self._meas_chrom_lastcomm = _Const.MeasCmd.Reset
            self._meas_chrom_dfreq_rf = 200.0
            self._meas_chrom_wait_tune = 5.0
            self._meas_chrom_nrsteps = 8

            self._meas_config_dsl_sf = 10.000
            self._meas_config_dsl_sd = 10.000

        # Connect to Sextupoles Families
        self._lastcalc_sl = {fam: 0 for fam in self._psfams}
        for fam in self._psfams:
            self._psfam_intstr_rb_pvs[fam] = _PV(
                _vaca_prefix+self._acc+'-Fam:PS-'+fam+':SL-RB',
                callback=self._callback_estimate_chrom,
                connection_timeout=0.05)

        if self._acc == 'SI':
            # Connect to SI RF
            self._rf_conn = RFGen()

        self.map_pv2write.update({
            'ChromX-SP': self.set_chrom_x,
            'ChromY-SP': self.set_chrom_y,
            'DeltaChromX-SP': self.set_deltachrom_x,
            'DeltaChromY-SP': self.set_deltachrom_y,
            'MeasChromDeltaFreqRF-SP': self.set_meas_chrom_dfreq_rf,
            'MeasChromWaitTune-SP': self.set_meas_chrom_wait_tune,
            'MeasChromNrSteps-SP': self.set_meas_chrom_nrsteps,
            'MeasChrom-Cmd': self.cmd_meas_chrom,
            'MeasConfigDeltaSLFamSF-SP': self.set_meas_config_dsl_sf,
            'MeasConfigDeltaSLFamSD-SP': self.set_meas_config_dsl_sd,
        })

        # auxiliar dict limit names
        self._lims_map = {
            'hilim': 'upper_disp_limit', 'lolim': 'lower_disp_limit',
            'high': 'upper_alarm_limit', 'low': 'lower_alarm_limit',
            'hihi': 'upper_warning_limit', 'lolo': 'lower_warning_limit'}

    def update_corrparams_pvs(self):
        """Set initial correction parameters PVs values."""
        self.run_callbacks('RespMat-Mon', self._nominal_matrix)
        self.run_callbacks('NominalSL-Mon', self._psfam_nom_intstr)
        self.run_callbacks('NominalChrom-Mon', self._nominal_opticsparam)

    def process(self, interval):
        """Sleep."""
        t_ini = _time.time()
        if (self._status & 0x1) == 0:  # Check connection
            for fam in self._psfams:
                rb_pv = self._psfam_intstr_rb_pvs[fam]
                try:
                    data = rb_pv.get_ctrlvars(timeout=0.1)
                    upper_disp_limit = rb_pv.upper_disp_limit
                except _ChannelAccessGetFailure:
                    break
                else:
                    if upper_disp_limit is not None and data is not None:
                        lis = {k: data[v] for k, v in self._lims_map.items()}
                        self.run_callbacks(
                            'SL'+fam+'-Mon', info=lis, field='info')
        dtime = interval - (_time.time() - t_ini)
        _time.sleep(max(dtime, 0))

    # ------ handle pv write methods -------

    def set_chrom_x(self, value):
        """Set ChromX."""
        self._last_param_set = 'absolut'
        self._chrom_sp[0] = value
        self.run_callbacks('ChromX-RB', value)
        self._deltachrom_sp[0] = self._chrom_sp[0]-self._optprm_est[0]
        self._calc_intstrength()
        return True

    def set_chrom_y(self, value):
        """Set ChromY."""
        self._last_param_set = 'absolut'
        self._chrom_sp[1] = value
        self.run_callbacks('ChromY-RB', value)
        self._deltachrom_sp[1] = self._chrom_sp[1]-self._optprm_est[1]
        self._calc_intstrength()
        return True

    def set_deltachrom_x(self, value):
        """Set DeltaChromX."""
        self._last_param_set = 'delta'
        self._deltachrom_sp[0] = value
        self.run_callbacks('DeltaChromX-RB', value)
        self._calc_intstrength()
        return True

    def set_deltachrom_y(self, value):
        """Set DeltaChromY."""
        self._last_param_set = 'delta'
        self._deltachrom_sp[1] = value
        self.run_callbacks('DeltaChromY-RB', value)
        self._calc_intstrength()
        return True

    def set_meas_chrom_dfreq_rf(self, value):
        """Set MeasChromDeltaFreqRF."""
        if value == self._meas_chrom_dfreq_rf:
            return False
        self._meas_chrom_dfreq_rf = value
        self.run_callbacks('MeasChromDeltaFreqRF-RB', value)
        return True

    def set_meas_chrom_wait_tune(self, value):
        """Set MeasChromWaitTune."""
        if value == self._meas_chrom_wait_tune:
            return False
        self._meas_chrom_wait_tune = value
        self.run_callbacks('MeasChromWaitTune-RB', value)
        return True

    def set_meas_chrom_nrsteps(self, value):
        """Set MeasChromNrSteps."""
        if value == self._meas_chrom_nrsteps:
            return False
        self._meas_chrom_nrsteps = value
        self.run_callbacks('MeasChromNrSteps-RB', value)
        return True

    def cmd_meas_chrom(self, value):
        """MeasChrom command."""
        if value == _Const.MeasCmd.Start:
            status = self._start_meas_chrom()
        elif value == _Const.MeasCmd.Stop:
            status = self._stop_meas_chrom()
        elif value == _Const.MeasCmd.Reset:
            status = self._reset_meas_chrom()
        if status:
            self._meas_chrom_lastcomm = value
        return status

    def set_meas_config_dsl_sf(self, value):
        """Set MeasConfigDeltaSLFamSF."""
        if value == self._meas_config_dsl_sf:
            return False
        self._meas_config_dsl_sf = value
        self.run_callbacks('MeasConfigDeltaSLFamSF-RB', value)
        return True

    def set_meas_config_dsl_sd(self, value):
        """Set MeasConfigDeltaSLFamSD."""
        if value == self._meas_config_dsl_sd:
            return False
        self._meas_config_dsl_sd = value
        self.run_callbacks('MeasConfigDeltaSLFamSD-RB', value)
        return True

    # ---------- auxiliar methods ----------

    def _handle_corrparams_2_read(self, params):
        """Edit correction params."""
        nom_matrix = [item for sublist in params['matrix'] for item in sublist]
        nom_sl = params['nominal SLs']
        nom_chrom = params['nominal chrom']
        return nom_matrix, nom_sl, nom_chrom

    def _handle_corrparams_2_save(self):
        matrix = _np.array(self._nominal_matrix)
        matrix = _np.reshape(matrix, [2, len(self._psfams)])

        value = {'matrix': matrix,
                 'nominal SLs': self._psfam_nom_intstr,
                 'nominal chrom': self._nominal_opticsparam}
        return value

    def _calc_intstrength(self):
        if self._last_param_set == 'absolut':
            delta_chromx = self._chrom_sp[0]-self._optprm_est[0]
            delta_chromy = self._chrom_sp[1]-self._optprm_est[1]
        else:
            delta_chromx, delta_chromy = self._deltachrom_sp

        method = 0 \
            if self._corr_method == _Const.CorrMeth.Proportional \
            else 1
        grouping = '2knobs' \
            if self._corr_group == _Const.CorrGroup.TwoKnobs \
            else 'svd'
        lastcalc_deltasl = self._opticscorr.calculate_delta_intstrengths(
            method=method, grouping=grouping,
            delta_opticsparam=[delta_chromx, delta_chromy])

        for fam_idx, fam in enumerate(self._psfams):
            sl_now = self._psfam_intstr_rb_pvs[fam].get()
            if sl_now is None:
                self.run_callbacks(
                    'Log-Mon',
                    'ERR: Received a None value from {}'.format(fam))
                return False
            self._lastcalc_sl[fam] = sl_now + lastcalc_deltasl[fam_idx]
            self.run_callbacks('SL'+fam+'-Mon', self._lastcalc_sl[fam])
        self._estimate_calc_chrom()

        self.run_callbacks('Log-Mon', 'Calculated SL values.')
        return True

    def _apply_corr(self):
        if self._is_status_ok():
            self._apply_intstrength(self._lastcalc_sl)
            self.run_callbacks('Log-Mon', 'Applied correction.')

            if self._sync_corr == _Const.SyncCorr.On:
                self._event_exttrig_cmd.put(0)
                self.run_callbacks('Log-Mon', 'Generated trigger.')
            return True

        self.run_callbacks('Log-Mon', 'ERR:ApplyDelta-Cmd failed.')
        return False

    def _get_optics_param(self):
        """Return optics parameter."""
        sts = self._meas_chrom()
        return sts, self._chrom_mon

    def _get_delta_intstrength(self, fam):
        if 'SL' in fam:
            deltasl = self._meas_config_dsl_sf
        else:
            deltasl = self._meas_config_dsl_sd
        fam_idx = self._psfams.index(fam)
        nelm = self._psfam_nelm[fam_idx]
        return deltasl/nelm

    def _get_rf_freq(self):
        """Get RF Frequnecy."""
        if not self._rf_conn.connected:
            return 0.0
        return self._rf_conn.frequency

    def _start_meas_chrom(self):
        """Start chromaticity measurement."""
        cont = True
        if self._measuring_chrom:
            log_msg = 'ERR: Chrom measurement already in progress!'
            cont = False
        elif not self._tune_x_pv.connected or not self._tune_y_pv.connected:
            log_msg = 'ERR: Cannot measure, tune PVs not connected!'
            cont = False
        elif not self._rf_conn.connected:
            log_msg = 'ERR: Cannot measure, RF PVs not connected!'
            cont = False
        elif not self._is_storedebeam:
            log_msg = 'ERR: Cannot measure, there is no stored beam!'
            cont = False
        if not cont:
            self.run_callbacks('Log-Mon', log_msg)
            return False

        thread = _Thread(target=self._meas_chrom, daemon=True)
        thread.start()
        return True

    def _stop_meas_chrom(self):
        """Stop chromaticity measurement."""
        if not self._measuring_chrom:
            self.run_callbacks(
                'Log-Mon', 'ERR: No chrom measurement occuring!')
            return False
        self.run_callbacks('Log-Mon', 'Aborting chrom measurement!')
        self._measuring_chrom = False
        return True

    def _reset_meas_chrom(self):
        """Reset chromaticity measurement."""
        if self._measuring_chrom:
            self.run_callbacks(
                'Log-Mon', 'ERR: Status not reset, measure in progress!')
            return False
        self.run_callbacks(
            'Log-Mon', 'Reseting chrom measurement status!')
        self._meas_chrom_status = _Const.MeasMon.Idle
        self.run_callbacks('MeasChromStatus-Mon', self._meas_chrom_status)
        return True

    def _meas_chrom(self):
        """Measure chromaticities."""
        self._meas_chrom_status = _Const.MeasMon.Measuring
        self.run_callbacks('MeasChromStatus-Mon', self._meas_chrom_status)

        self._measuring_chrom = True
        self.run_callbacks('Log-Mon', 'Starting chrom measurement!')

        _, data = self._get_tunes()
        tunex0, tuney0 = data

        freq0 = self._get_rf_freq()
        frequencies = _np.linspace(
            freq0-self._meas_chrom_dfreq_rf/2,
            freq0+self._meas_chrom_dfreq_rf/2,
            self._meas_chrom_nrsteps)
        freq_list = list()
        tunex_list, tuney_list = list(), list()

        aborted = False
        for value in frequencies:
            if not self._measuring_chrom:
                log_msg = 'Stoped chrom measurement!'
                aborted = True
            elif not self._is_storedebeam:
                log_msg = 'ERR: Stoping chrom measurement, '\
                          'there is no stored beam!'
                aborted = True
            elif not self._tune_x_pv.connected or \
                    not self._tune_y_pv.connected:
                log_msg = 'ERR: Stoping chrom measurement, '\
                          'tune PVs not connected!'
                aborted = True
            elif not self._rf_conn.connected:
                log_msg = 'ERR: Stoping chrom measurement, '\
                          'RF PVs not connected!'
                aborted = True
            if aborted:
                break

            self._rf_conn.frequency = value
            freq = self._get_rf_freq()
            freq_list.append(freq)
            self.run_callbacks(
                'Log-Mon', 'Delta RF: {} Hz'.format((freq-freq0)))

            _time.sleep(self._meas_chrom_wait_tune)
            sts, data = self._get_tunes()
            if sts:
                tunex, tuney = data
                tunex_list.append(tunex)
                tuney_list.append(tuney)
                self.run_callbacks(
                    'Log-Mon', 'Delta Tune X: {}'.format(
                        (tunex_list[-1]-tunex0)))
                self.run_callbacks(
                    'Log-Mon', 'Delta Tune Y: {}'.format(
                        (tuney_list[-1]-tuney0)))
            else:
                log_msg = 'ERR: Could not measure tune!'
                aborted = True
                break

        self.run_callbacks('Log-Mon', 'Restoring RF frequency...')
        self._rf_conn.frequency = freq0
        self.run_callbacks('Log-Mon', 'RF frequency restored!')

        if aborted:
            self._meas_chrom_status = _Const.MeasMon.Aborted
        else:
            den = -(_np.array(freq_list) - freq0)/freq0/_MOM_COMPACT
            tunex_array = _np.array(tunex_list)
            tuney_array = _np.array(tuney_list)

            chromx, _ = _np.polyfit(den, tunex_array, deg=1, cov=True)
            chromy, _ = _np.polyfit(den, tuney_array, deg=1, cov=True)

            self._chrom_mon[0] = chromx[0]
            self._chrom_mon[1] = chromy[0]

            self.run_callbacks('MeasChromX-Mon', self._chrom_mon[0])
            self.run_callbacks('MeasChromY-Mon', self._chrom_mon[1])

            self._meas_chrom_status = _Const.MeasMon.Completed
            log_msg = 'Chromaticity measurement completed!'

        self.run_callbacks('MeasChromStatus-Mon', self._meas_chrom_status)
        self._measuring_config = False
        self.run_callbacks('Log-Mon', log_msg)
        return not aborted

    def _estimate_calc_chrom(self):
        sfam_deltasl = len(self._psfams)*[0]
        for fam_idx, fam in enumerate(self._psfams):
            sfam_deltasl[fam_idx] = \
                self._lastcalc_sl[fam] - self._psfam_nom_intstr[fam_idx]

        calc_estim = self._opticscorr.calculate_opticsparam(sfam_deltasl)
        self.run_callbacks('CalcChromX-Mon', calc_estim[0])
        self.run_callbacks('CalcChromY-Mon', calc_estim[1])

    # ---------- callbacks ----------

    def _callback_estimate_chrom(self, pvname, value, **kws):
        if value is None:
            return
        fam = _SiriusPVName(pvname).dev
        self._psfam_intstr_rb[fam] = value

        sfam_deltasl = len(self._psfams)*[0]
        for fam_idx, fam in enumerate(self._psfams):
            sfam_deltasl[fam_idx] = \
                self._psfam_intstr_rb[fam] - self._psfam_nom_intstr[fam_idx]

        self._optprm_est = self._opticscorr.calculate_opticsparam(sfam_deltasl)
        self.run_callbacks('ChromX-Mon', self._optprm_est[0])
        self.run_callbacks('ChromY-Mon', self._optprm_est[1])

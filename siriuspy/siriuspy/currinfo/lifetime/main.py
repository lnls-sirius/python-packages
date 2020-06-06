"""Main Module of the IOC Logic."""

import warnings
import time as _time
import numpy as _np
from epics import PV as _PV

from ...callbacks import Callback as _Callback
from ...epics import SiriusPVTimeSerie as _SiriusPVTimeSerie
from ...envars import VACA_PREFIX as _vaca_prefix
from ..csdev import \
    Const as _Const, get_lifetime_database as _get_database

warnings.filterwarnings('error')

_MAX_BUFFER_SIZE = 36000


class SILifetimeApp(_Callback):
    """Main Class of the IOC Logic."""

    def __init__(self):
        """Class constructor."""
        super().__init__()

        self._init_time = _time.time()

        self._pvs_database = _get_database()
        self._mode = _Const.Fit.Linear
        self._current_offset = 0.0
        self._frst_smpl_ts = self._init_time
        self._last_smpl_ts = -1
        self._frst_smpl_ts_dcct = self._init_time
        self._last_smpl_ts_dcct = -1
        self._smpl_intvl_mon_dcct = 0.0
        self._frst_smpl_ts_bpm = self._init_time
        self._last_smpl_ts_bpm = -1
        self._smpl_intvl_mon_bpm = 0.0
        self._last_ts_set = 'last'
        self._sampling_interval = 500.0
        self._min_intvl_btw_spl = 0.0
        self._rstbuff_cmd_count = 0
        self._buffautorst_mode = _Const.BuffAutoRst.Off
        self._buffautorst_dcurr = 0.1
        self._is_stored = 0
        self._lifetime = 0
        self._lifetime_bpm = 0

        self._current_pv = _PV(
            _vaca_prefix+'SI-Glob:AP-CurrInfo:Current-Mon',
            connection_timeout=0.05)
        self._bpmsum_pv = _PV(
            _vaca_prefix+'SI-01M1:DI-BPM:Sum-Mon',
            connection_timeout=0.05)
        self._storedebeam_pv = _PV(
            _vaca_prefix+'SI-Glob:AP-CurrInfo:StoredEBeam-Mon',
            connection_timeout=0.05)

        self._current_buffer = _SiriusPVTimeSerie(
            pv=self._current_pv, mode=0, nr_max_points=_MAX_BUFFER_SIZE,
            use_pv_timestamp=False)
        self._bpmsum_buffer = _SiriusPVTimeSerie(
            pv=self._bpmsum_pv, mode=0, nr_max_points=_MAX_BUFFER_SIZE,
            use_pv_timestamp=False)

        self._current_pv.add_callback(self._callback_calclifetime)
        self._bpmsum_pv.add_callback(self._callback_calclifetime)
        self._storedebeam_pv.add_callback(self._callback_get_storedebeam)

    @property
    def pvs_database(self):
        """Return pvs database."""
        return self._pvs_database

    def init_database(self):
        """Set PVs initial values."""
        self.run_callbacks('FrstSplTime-SP', self._frst_smpl_ts)
        self.run_callbacks('LastSplTime-SP', self._last_smpl_ts)
        self.run_callbacks('FrstSplTime-RB', self._frst_smpl_ts)
        self.run_callbacks('LastSplTime-RB', self._last_smpl_ts)
        self.run_callbacks('FrstSplTimeBPM-RB', self._frst_smpl_ts_bpm)
        self.run_callbacks('LastSplTimeBPM-RB', self._last_smpl_ts_bpm)

    def process(self, interval):
        """Sleep."""
        _time.sleep(interval)

    def read(self, reason):
        """Read from IOC database."""
        value = None
        if reason in ['Lifetime-Mon', 'LifetimeBPM-Mon']:
            is_bpm = 'BPM' in reason
            lt_type = 'BPM' if is_bpm else ''
            lt_name = '_lifetime'+('_bpm' if is_bpm else '')
            buffer_dt = self._bpmsum_buffer if is_bpm else self._current_buffer

            # get first and last sample
            now = _time.time()
            self._update_times(now)
            first_name = '_frst_smpl_ts'+('_bpm' if is_bpm else '_dcct')
            first_smpl = getattr(self, first_name)
            last_name = '_last_smpl_ts'+('_bpm' if is_bpm else '_dcct')
            last_smpl = getattr(self, last_name)
            last_smpl = now if last_smpl == -1 else min(last_smpl, now)
            intvl_name = '_smpl_intvl_mon'+('_bpm' if is_bpm else '_dcct')
            intvl_smpl = getattr(self, intvl_name)

            # calculate lifetime
            ts_abs_dqorg, val_dqorg = buffer_dt.get_serie(time_absolute=True)
            ts_dqorg = ts_abs_dqorg - now
            ts_dq, val_dq, ts_abs_dq = self._filter_buffer(
                ts_dqorg, val_dqorg, ts_abs_dqorg, first_smpl, last_smpl)

            if ts_dq.size == 0:
                setattr(self, lt_name, 0)
            else:
                if first_smpl != ts_abs_dq[0]:
                    setattr(self, first_name, ts_abs_dq[0])
                    self.run_callbacks(
                        'FrstSplTime'+lt_type+'-RB', getattr(self, first_name))
                intvl_smpl = last_smpl - first_smpl
                setattr(self, intvl_name, intvl_smpl)
                self.run_callbacks(
                    'SplIntvl'+lt_type+'-Mon', getattr(self, intvl_name))

                val_dq -= self._current_offset

                # check min number of points in buffer
                if len(val_dq) > 100:
                    fit = 'lin' if self._mode == _Const.Fit.Linear else 'exp'
                    value = self._least_squares_fit(ts_dq, val_dq, fit=fit)
                else:
                    value = 0
                setattr(self, lt_name, value)

            # update pvs
            self.run_callbacks('BufferValue'+lt_type+'-Mon', val_dq)
            self.run_callbacks('BufferTimestamp'+lt_type+'-Mon', ts_dq)
            self.run_callbacks('BuffSize'+lt_type+'-Mon', len(val_dq))
            self.run_callbacks('BuffSizeTot'+lt_type+'-Mon', len(val_dqorg))
        return value

    def write(self, reason, value):
        """Write value to reason and let callback update PV database."""
        status = False
        now = _time.time()
        if reason == 'MaxSplIntvl-SP':
            if value == -1 or value >= 0:
                self._sampling_interval = value
                if value != -1:
                    self._update_times(now, force_min_first=True)
            elif value < 0:
                self._sampling_interval = 0
            self.run_callbacks('MaxSplIntvl-RB', self._sampling_interval)
            status = True
        elif reason == 'MinIntvlBtwSpl-SP':
            if value < 0:
                value = 0
            self._min_intvl_btw_spl = value
            self.run_callbacks('MinIntvlBtwSpl-RB', value)
            status = True
        elif reason == 'LtFitMode-Sel':
            self._mode = value
            self.run_callbacks('LtFitMode-Sts', value)
            status = True
        elif reason == 'CurrOffset-SP':
            self._current_offset = value
            self.run_callbacks('CurrOffset-RB', value)
            status = True
        elif reason == 'BuffRst-Cmd':
            self._rstbuff_cmd_count += 1
            self._reset_buff()
            self.run_callbacks('BuffRst-Cmd', self._rstbuff_cmd_count)
            status = True
        elif reason == 'BuffAutoRst-Sel':
            self._buffautorst_mode = value
            self.run_callbacks('BuffAutoRst-Sts', value)
            status = True
        elif reason == 'BuffAutoRstDCurr-SP':
            self._buffautorst_dcurr = value
            self.run_callbacks('BuffAutoRstDCurr-RB', value)
            status = True
        elif reason == 'FrstSplTime-SP':
            self._frst_smpl_ts = value
            self._frst_smpl_ts_dcct = value
            self._frst_smpl_ts_bpm = value
            self._last_ts_set = 'first'
            self._update_times(now)
            status = True
        elif reason == 'LastSplTime-SP':
            self._last_smpl_ts = value
            self._last_smpl_ts_dcct = value
            self._last_smpl_ts_bpm = value
            self._last_ts_set = 'last'
            self._update_times(now, force_min_first=True)
            status = True
        return status

    # ---------- callbacks ----------

    def _callback_get_storedebeam(self, value, **kws):
        self._is_stored = value

    def _callback_calclifetime(self, pvname, timestamp, **kws):
        # check DCCT StoredEBeam PV
        if not self._is_stored:
            self._buffautorst_check()
            return

        is_bpm = 'BPM' in pvname
        buffer_dt = self._bpmsum_buffer if is_bpm else self._current_buffer

        # try to add a new point to buffer
        if not buffer_dt.acquire():
            return

        # check whether the buffer must be reset
        self._buffautorst_check()

    # ---------- auxiliar methods ----------

    def _buffautorst_check(self):
        """Check situations to clear internal buffer.
        If BuffAutoRst == DCurrCheck, check abrupt variation of current by
        a factor of 20 times the DCCT fluctuation/resolution.
        """
        if self._buffautorst_mode == _Const.BuffAutoRst.Off:
            return

        reset = False
        [_, value] = self._current_buffer.serie
        if len(value) >= 2:
            deltacurr = abs(value[-1] - value[-2])
        else:
            deltacurr = 0.0
        if deltacurr > self._buffautorst_dcurr:
            reset = True
        if reset:
            self._reset_buff()

    def _reset_buff(self):
        now = _time.time()
        self._frst_smpl_ts = now
        self._last_smpl_ts = -1
        self._frst_smpl_ts_dcct = now
        self._last_smpl_ts_dcct = -1
        self._frst_smpl_ts_bpm = now
        self._last_smpl_ts_bpm = -1
        self.run_callbacks('FrstSplTime-RB', self._frst_smpl_ts_dcct)
        self.run_callbacks('LastSplTime-RB', self._last_smpl_ts_dcct)
        self.run_callbacks('FrstSplTimeBPM-RB', self._frst_smpl_ts_bpm)
        self.run_callbacks('LastSplTimeBPM-RB', self._last_smpl_ts_bpm)

        self._lifetime_bpm = 0
        self._lifetime = 0
        self.run_callbacks('Lifetime-Mon', self._lifetime)
        self.run_callbacks('LifetimeBPM-Mon', self._lifetime_bpm)

    def _filter_buffer(self, timestamp, value, abs_timestamp, first, last):
        ts_arrayorg = _np.asarray(timestamp)
        val_arrayorg = _np.asarray(value)
        ts_abs_arrayorg = _np.asarray(abs_timestamp)
        if ts_abs_arrayorg.size == 0:
            return ts_arrayorg, val_arrayorg, ts_abs_arrayorg

        ind1 = ts_abs_arrayorg >= first
        ind2 = ts_abs_arrayorg <= last
        indices = _np.logical_and(ind1, ind2).nonzero()
        if not indices[0].size:
            return _np.array([]), _np.array([]), _np.array([])
        slc = slice(indices[0][0], indices[0][-1]+1)

        ts_aux_array = ts_arrayorg[slc]
        val_aux_array = val_arrayorg[slc]
        ts_aux_abs_array = ts_abs_arrayorg[slc]

        min_intvl = self._min_intvl_btw_spl
        if min_intvl <= 0.0:
            return ts_aux_array, val_aux_array, ts_aux_abs_array

        indices = _np.zeros(len(ts_aux_array), dtype=bool)
        indices[0] = _np.True_
        last_idx = 0
        for i, _ in enumerate(ts_aux_array):
            if abs(ts_aux_array[last_idx] - ts_aux_array[i]) > min_intvl:
                indices[i] = _np.True_
                last_idx = i

        indices = indices.nonzero()
        ts_array = ts_aux_array[indices]
        val_array = val_aux_array[indices]
        ts_abs_array = ts_aux_abs_array[indices]
        return ts_array, val_array, ts_abs_array

    @staticmethod
    def _least_squares_fit(timestamp, value, fit='exp'):
        if fit == 'exp':
            try:
                value = _np.log(value)
            except Exception:
                return 0.0
        _ns = len(timestamp)
        _x1 = _np.sum(timestamp)
        _y1 = _np.sum(value)
        if timestamp.size > 10000:
            _x2 = _np.sum(timestamp*timestamp)
            _xy = _np.sum(timestamp*value)
        else:
            _x2 = _np.dot(timestamp, timestamp)
            _xy = _np.dot(timestamp, value)
        fit_a = (_x2*_y1 - _xy*_x1)/(_ns*_x2 - _x1*_x1)
        fit_b = (_ns*_xy - _x1*_y1)/(_ns*_x2 - _x1*_x1)

        if fit == 'exp':
            lifetime = - 1/fit_b
        else:
            lifetime = - fit_a/fit_b
        return lifetime

    def _update_times(self, now, force_min_first=False):
        if self._last_ts_set == 'first':
            value = self._frst_smpl_ts
            if self._sampling_interval != -1:
                last = value + self._sampling_interval
                self._last_smpl_ts_dcct = last
                self._last_smpl_ts_bpm = last
        elif self._last_ts_set == 'last':
            value = now if self._last_smpl_ts == -1 else self._last_smpl_ts
            if self._sampling_interval != -1:
                first = value - self._sampling_interval
                if self._frst_smpl_ts_dcct < first or force_min_first:
                    self._frst_smpl_ts_dcct = first
                if self._frst_smpl_ts_bpm < first or force_min_first:
                    self._frst_smpl_ts_bpm = first

        self.run_callbacks('FrstSplTime-RB', self._frst_smpl_ts_dcct)
        self.run_callbacks('FrstSplTimeBPM-RB', self._frst_smpl_ts_bpm)
        self.run_callbacks('LastSplTime-RB', self._last_smpl_ts_dcct)
        self.run_callbacks('LastSplTimeBPM-RB', self._last_smpl_ts_bpm)

"""Module to deal with orbit acquisition."""
import os as _os
import time as _time
from math import ceil as _ceil
import logging as _log
from functools import partial as _part
from copy import deepcopy as _dcopy
from threading import Lock, Thread, Event as _Event
import multiprocessing as _mp
import traceback as _traceback

import numpy as _np
import bottleneck as _bn

from .. import util as _util
from ..diagbeam.bpm.csdev import Const as _csbpm
from ..thread import RepeaterThread as _Repeat
from ..epics import PV as _PV, CAProcessSpawn as _Process

from .base_class import BaseClass as _BaseClass
from .bpms import BPM, TimingConfig, TIMEOUT


class BaseOrbit(_BaseClass):
    """."""


def run_subprocess(pvs, send_pipe, recv_pipe):
    """Run subprocesses."""
    max_spread = 25/1000  # in [s]
    timeout = 50/1000  # in [s]

    ready_evt = _Event()

    tstamps = _np.full(len(pvs), _np.nan)

    def callback(*_, **kwargs):
        pvo = kwargs['cb_info'][1]
        # pvo._args['timestamp'] = _time.time()
        tstamps[pvo.index] = pvo.timestamp
        maxi = _bn.nanmax(tstamps)
        mini = _bn.nanmin(tstamps)
        if (maxi-mini) < max_spread:
            ready_evt.set()

    def conn_callback(pvname=None, conn=None, pv=None):
        if not conn:
            tstamps[pv.index] = _np.nan

    pvsobj = []
    for i, pvn in enumerate(pvs):
        pvo = _PV(pvn, connection_timeout=TIMEOUT)
        pvo.index = i
        pvsobj.append(pvo)

    for pvo in pvsobj:
        pvo.wait_for_connection()

    for pvo in pvsobj:
        pvo.add_callback(callback)
        pvo.connection_callbacks.append(conn_callback)

    boo = True
    while boo or recv_pipe.recv():
        boo = False
        ready_evt.clear()
        nok = 0.0
        if not ready_evt.wait(timeout=timeout):
            nok = 1.0
        out = []
        for pvo in pvsobj:
            if not pvo.connected:
                out.append(_np.nan)
                continue
            # out.append(pvo.timestamp)
            out.append(pvo.value)
        out.append(nok)
        send_pipe.send(out)


class EpicsOrbit(BaseOrbit):
    """Class to deal with orbit acquisition."""

    def __init__(self, acc, prefix='', callback=None):
        """Initialize the instance."""
        super().__init__(acc, prefix=prefix, callback=callback)

        self._mode = self._csorb.SOFBMode.Offline
        self._sync_with_inj = False
        self._sloworb_timeout = 0
        self.ref_orbs = {
            'X': _np.zeros(self._csorb.nr_bpms),
            'Y': _np.zeros(self._csorb.nr_bpms)}
        self._load_ref_orbs()
        self.raw_orbs = {'X': [], 'Y': []}
        self.raw_sporbs = {'X': [], 'Y': [], 'Sum': []}
        self.raw_mtorbs = {'X': [], 'Y': [], 'Sum': []}
        self._lock_raw_orbs = Lock()
        self.smooth_orb = {'X': None, 'Y': None}
        self.smooth_sporb = {'X': None, 'Y': None, 'Sum': None}
        self.smooth_mtorb = {'X': None, 'Y': None, 'Sum': None}
        self.offline_orbit = {
            'X': _np.zeros(self._csorb.nr_bpms),
            'Y': _np.zeros(self._csorb.nr_bpms)}
        self._smooth_npts = 1
        self._smooth_meth = self._csorb.SmoothMeth.Average
        self._spass_mask = [0, 0]
        self._spass_average = 1
        self._spass_th_acqbg = None
        self._spass_bgs = [dict() for _ in range(self._csorb.nr_bpms)]
        self._spass_usebg = self._csorb.SPassUseBg.NotUsing
        self._acqrate = self._csorb.MIN_SLOWORB_RATE
        self._oldacqrate = self._acqrate
        self._acqtrignrsamplespre = 0
        self._acqtrignrsamplespost = 360
        self._acqtrignrshots = 1
        self._multiturnidx = 0
        self._mturndownsample = 1
        self._timevector = None
        self._ring_extension = 1
        self.bpms = [BPM(name, callback) for name in self._csorb.bpm_names]
        self.timing = TimingConfig(acc, callback)
        self.new_orbit = _Event()
        if self.acc == 'SI':
            self._processes = []
            self._mypipes_recv = []
            self._mypipes_send = []
            self._create_processes(nrprocs=16)
        self._orbit_thread = _Repeat(
            1/self._acqrate, self._update_orbits, niter=0)
        self._orbit_thread.start()
        self._update_time_vector()

    def _create_processes(self, nrprocs=8):
        # get the start method of the Processes that will be launched:
        spw = _mp.get_context('spawn')

        pvs = []
        for bpm in self._csorb.bpm_names:
            pvs.append(bpm+':PosX-Mon')
        for bpm in self._csorb.bpm_names:
            pvs.append(bpm+':PosY-Mon')

        # subdivide the pv list for the processes
        div = len(pvs) // nrprocs
        rem = len(pvs) % nrprocs
        sub = [div*i + min(i, rem) for i in range(nrprocs+1)]

        # create processes
        for i in range(nrprocs):
            mine, send_pipe = spw.Pipe(duplex=False)
            self._mypipes_recv.append(mine)
            recv_pipe, mine = spw.Pipe(duplex=False)
            self._mypipes_send.append(mine)
            pvsn = pvs[sub[i]:sub[i+1]]
            self._processes.append(_Process(
                target=run_subprocess,
                args=(pvsn, send_pipe, recv_pipe),
                daemon=True))
        for proc in self._processes:
            proc.start()

    def shutdown(self):
        """."""
        self._orbit_thread.resume()
        self._orbit_thread.stop()
        self._orbit_thread.join()
        if self.acc == 'SI':
            for pipe in self._mypipes_send:
                pipe.send(False)
                pipe.close()
            for proc in self._processes:
                proc.join()

    def get_map2write(self):
        """Get the write methods of the class."""
        dbase = {
            'SOFBMode-Sel': self.set_orbit_mode,
            'SyncWithInjection-Sel': self.set_sync_with_injection,
            'TrigAcqConfig-Cmd': self.acq_config_bpms,
            'TrigAcqCtrl-Sel': self.set_trig_acq_control,
            'TrigAcqChan-Sel': self.set_trig_acq_channel,
            'TrigDataChan-Sel': self.set_trig_acq_datachan,
            'TrigAcqTrigger-Sel': self.set_trig_acq_trigger,
            'TrigAcqRepeat-Sel': self.set_trig_acq_repeat,
            'TrigDataSel-Sel': self.set_trig_acq_datasel,
            'TrigDataThres-SP': self.set_trig_acq_datathres,
            'TrigDataHyst-SP': self.set_trig_acq_datahyst,
            'TrigDataPol-Sel': self.set_trig_acq_datapol,
            'TrigNrSamplesPre-SP': _part(self.set_acq_nrsamples, ispost=False),
            'TrigNrSamplesPost-SP': _part(self.set_acq_nrsamples, ispost=True),
            'RefOrbX-SP': _part(self.set_reforb, 'X'),
            'RefOrbY-SP': _part(self.set_reforb, 'Y'),
            'OfflineOrbX-SP': _part(self.set_offlineorb, 'X'),
            'OfflineOrbY-SP': _part(self.set_offlineorb, 'Y'),
            'SmoothNrPts-SP': self.set_smooth_npts,
            'SmoothMethod-Sel': self.set_smooth_method,
            'SmoothReset-Cmd': self.set_smooth_reset,
            'SPassMaskSplBeg-SP': _part(self.set_spass_mask, beg=True),
            'SPassMaskSplEnd-SP': _part(self.set_spass_mask, beg=False),
            'SPassBgCtrl-Cmd': self.set_spass_bg,
            'SPassUseBg-Sel': self.set_spass_usebg,
            'SPassAvgNrTurns-SP': self.set_spass_average,
            'OrbAcqRate-SP': self.set_orbit_acq_rate,
            'TrigNrShots-SP': self.set_trig_acq_nrshots,
            'PolyCalibration-Sel': self.set_poly_calibration,
            }
        if not self.isring:
            return dbase
        dbase.update({
            'MTurnAcquire-Cmd': self.acquire_mturn_orbit,
            'MTurnIdx-SP': self.set_orbit_multiturn_idx,
            'MTurnDownSample-SP': self.set_mturndownsample,
            'MTurnSyncTim-Sel': self.set_mturn_sync,
            'MTurnUseMask-Sel': self.set_mturn_usemask,
            'MTurnMaskSplBeg-SP': _part(self.set_mturnmask, beg=True),
            'MTurnMaskSplEnd-SP': _part(self.set_mturnmask, beg=False),
            })
        return dbase

    @property
    def mode(self):
        """."""
        return self._mode

    @property
    def acqtrignrsamples(self):
        """."""
        return self._acqtrignrsamplespre + self._acqtrignrsamplespost

    @property
    def update_raws(self):
        """."""
        return not self._sync_with_inj or self.timing.injecting

    def is_sloworb(self, mode=None):
        """Check is mode or self._mode is in SlowOrb mode."""
        if mode is None:
            mode = self._mode
        return self.acc == 'SI' and mode == self._csorb.SOFBMode.SlowOrb

    def is_multiturn(self, mode=None):
        """Check is mode or self._mode is in MultiTurn mode."""
        if mode is None:
            mode = self._mode
        return self.isring and mode == self._csorb.SOFBMode.MultiTurn

    def is_singlepass(self, mode=None):
        """Check is mode or self._mode is in SinglePass mode."""
        if mode is None:
            mode = self._mode
        return mode == self._csorb.SOFBMode.SinglePass

    def is_trigmode(self, mode=None):
        """Check is mode or self._mode is in any of the Triggered modes."""
        return self.is_singlepass(mode) or self.is_multiturn(mode)

    def set_ring_extension(self, val):
        """."""
        maval = self._csorb.MAX_RINGSZ
        val = 1 if val < 1 else int(val)
        val = maval if val > maval else val
        if val == self._ring_extension:
            return True
        with self._lock_raw_orbs:
            self._spass_average = 1
            self.run_callbacks('SPassAvgNrTurns-SP', 1)
            self.run_callbacks('SPassAvgNrTurns-RB', 1)
            self._mturndownsample = 1
            self.run_callbacks('MTurnDownSample-SP', 1)
            self.run_callbacks('MTurnDownSample-RB', 1)
            self._reset_orbs()
            self._ring_extension = val
            nrb = val * self._csorb.nr_bpms
            for pln in self.offline_orbit:
                orb = self.ref_orbs[pln]
                if orb.size < nrb:
                    nrep = _ceil(nrb/orb.size)
                    orb2 = _np.tile(orb, nrep)
                    orb = orb2[:nrb]
                self.ref_orbs[pln] = orb
                self.run_callbacks('RefOrb'+pln+'-RB', orb[:nrb])
                self.run_callbacks('RefOrb'+pln+'-SP', orb[:nrb])
                orb = self.offline_orbit[pln]
                if orb.size < nrb:
                    orb2 = self.ref_orbs[pln].copy()
                    orb2[:orb.size] = orb
                    orb = orb2
                self.offline_orbit[pln] = orb
                self.run_callbacks('OfflineOrb'+pln+'-RB', orb[:nrb])
                self.run_callbacks('OfflineOrb'+pln+'-SP', orb[:nrb])
        self._save_ref_orbits()
        Thread(target=self._prepare_mode, daemon=True).start()
        return True

    def get_orbit(self, reset=False, synced=False, timeout=1/10):
        """Return the orbit distortion."""
        nrb = self._ring_extension * self._csorb.nr_bpms
        refx = self.ref_orbs['X'][:nrb]
        refy = self.ref_orbs['Y'][:nrb]
        if self._mode == self._csorb.SOFBMode.Offline:
            orbx = self.offline_orbit['X'][:nrb]
            orby = self.offline_orbit['Y'][:nrb]
            return _np.hstack([orbx-refx, orby-refy])

        if reset:
            with self._lock_raw_orbs:
                self._reset_orbs()
            _time.sleep(self._smooth_npts/self._acqrate)

        if self.is_multiturn():
            orbs = self.smooth_mtorb
            raw_orbs = self.raw_mtorbs
            getorb = self._get_orbit_multiturn
        elif self.is_singlepass():
            orbs = self.smooth_sporb
            raw_orbs = self.raw_sporbs
            getorb = self._get_orbit_singlepass
        elif self.is_sloworb():
            if synced:
                self.new_orbit.wait(timeout=timeout)
                self.new_orbit.clear()
            orbs = self.smooth_orb
            raw_orbs = self.raw_orbs
            getorb = self._get_orbit_online

        for _ in range(3 * self._smooth_npts):
            isnone = orbs['X'] is None or orbs['Y'] is None
            if isnone or len(raw_orbs['X']) < self._smooth_meth:
                _time.sleep(1/self._acqrate)
                continue
            orbx, orby = getorb(orbs)
            break
        else:
            msg = 'ERR: timeout waiting orbit.'
            self._update_log(msg)
            _log.error(msg[5:])
            orbx, orby = refx, refy
        # # for tests:
        # orbx -= _time.time()
        # orby -= _time.time()
        return _np.hstack([orbx-refx, orby-refy])

    def _get_orbit_online(self, orbs):
        """."""
        return orbs['X'], orbs['Y']

    def _get_orbit_singlepass(self, orbs):
        """."""
        return orbs['X'], orbs['Y']

    def _get_orbit_multiturn(self, orbs):
        """."""
        idx = self._multiturnidx
        return orbs['X'][idx, :], orbs['Y'][idx, :]

    def set_offlineorb(self, plane, orb):
        """."""
        msg = 'Setting New Offline Orbit.'
        self._update_log(msg)
        _log.info(msg)
        orb = _np.array(orb, dtype=float)
        nrb = self._ring_extension * self._csorb.nr_bpms
        if orb.size % self._csorb.nr_bpms:
            msg = 'ERR: Wrong OfflineOrb Size.'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        elif orb.size < nrb:
            orb2 = _np.zeros(nrb, dtype=float)
            orb2[:orb.size] = orb
            orb = orb2
        self.offline_orbit[plane] = orb
        self.run_callbacks('OfflineOrb'+plane+'-RB', orb[:nrb])
        return True

    def set_smooth_npts(self, num):
        """."""
        self._smooth_npts = num
        self.run_callbacks('SmoothNrPts-RB', num)
        return True

    def set_smooth_method(self, meth):
        """."""
        self._smooth_meth = meth
        self.run_callbacks('SmoothMethod-Sts', meth)
        return True

    def set_spass_mask(self, val, beg=True):
        """."""
        val = int(val) if val > 0 else 0
        other_mask = self._spass_mask[1 if beg else 0]
        maxsz = self.bpms[0].tbtrate - other_mask - 2
        val = val if val < maxsz else maxsz
        self._spass_mask[0 if beg else 1] = val
        name = 'Beg' if beg else 'End'
        self.run_callbacks('SPassMaskSpl' + name + '-RB', val)
        return True

    def set_spass_bg(self, val):
        """."""
        if val == self._csorb.SPassBgCtrl.Acquire:
            trh = self._spass_th_acqbg
            if trh is None or not trh.is_alive():
                self._spass_th_acqbg = Thread(
                    target=self._do_acquire_spass_bg, daemon=True)
                self._spass_th_acqbg.start()
            else:
                msg = 'WARN: SPassBg is already being acquired.'
                self._update_log(msg)
                _log.warning(msg[6:])
        elif val == self._csorb.SPassBgCtrl.Reset:
            self.run_callbacks(
                'SPassUseBg-Sts', self._csorb.SPassUseBg.NotUsing)
            self._spass_bgs = [dict() for _ in range(len(self.bpms))]
            self.run_callbacks('SPassBgSts-Mon', self._csorb.SPassBgSts.Empty)
        else:
            msg = 'ERR: SPassBg Control not recognized.'
            self._update_log(msg)
            _log.warning(msg[5:])
            return False
        return True

    def set_mturn_sync(self, val):
        """."""
        value = _csbpm.EnbldDsbld.enabled
        if val == self._csorb.EnbldDsbld.Dsbld:
            value = _csbpm.EnbldDsbld.disabled
        for bpm in self.bpms:
            bpm.tbt_sync_enbl = value
        self.run_callbacks('MTurnSyncTim-Sts', val)
        return True

    def set_mturn_usemask(self, val):
        """."""
        value = _csbpm.EnbldDsbld.enabled
        if val == self._csorb.EnbldDsbld.Dsbld:
            value = _csbpm.EnbldDsbld.disabled
        for bpm in self.bpms:
            bpm.tbt_mask_enbl = value
        self.run_callbacks('MTurnUseMask-Sts', val)
        return True

    def set_mturnmask(self, val, beg=True):
        """."""
        val = int(val) if val > 0 else 0
        omsk = \
            self.bpms[0].tbt_mask_begin if not beg else \
            self.bpms[0].tbt_mask_end
        omsk = omsk or 0
        maxsz = self.bpms[0].tbtrate - omsk - 2
        val = val if val < maxsz else maxsz
        for bpm in self.bpms:
            if beg:
                bpm.tbt_mask_begin = val
            else:
                bpm.tbt_mask_end = val
        name = 'Beg' if beg else 'End'
        self.run_callbacks('MTurnMaskSpl' + name + '-RB', val)
        return True

    def _do_acquire_spass_bg(self):
        """."""
        self.run_callbacks('SPassBgSts-Mon', self._csorb.SPassBgSts.Acquiring)
        self._spass_bgs = [dict() for _ in range(len(self.bpms))]
        ants = {'A': [], 'B': [], 'C': [], 'D': []}
        bgs = [_dcopy(ants) for _ in range(len(self.bpms))]
        # Acquire the samples
        for _ in range(self._smooth_npts):
            for i, bpm in enumerate(self.bpms):
                bgs[i]['A'].append(bpm.arraya)
                bgs[i]['B'].append(bpm.arrayb)
                bgs[i]['C'].append(bpm.arrayc)
                bgs[i]['D'].append(bpm.arrayd)
            _time.sleep(1/self._acqrate)
        # Make the smoothing
        try:
            for i, bpm in enumerate(self.bpms):
                for k, val in bgs[i].items():
                    if self._smooth_meth == self._csorb.SmoothMeth.Average:
                        bgs[i][k] = _np.mean(val, axis=0)
                    else:
                        bgs[i][k] = _np.median(val, axis=0)
                    if not _np.all(_np.isfinite(bgs[i][k])):
                        raise ValueError('there was some nans or infs.')
            self._spass_bgs = bgs
            self.run_callbacks(
                'SPassBgSts-Mon', self._csorb.SPassBgSts.Acquired)
        except (ValueError, TypeError) as err:
            msg = 'ERR: SPassBg Acq ' + str(err)
            self._update_log(msg)
            _log.error(msg[5:])
            self.run_callbacks('SPassBgSts-Mon', self._csorb.SPassBgSts.Empty)

    def set_spass_usebg(self, val):
        """."""
        self._spass_usebg = int(val)
        return True

    def set_spass_average(self, val):
        """."""
        if self._ring_extension != 1 and val != 1:
            msg = 'ERR: Cannot set SPassAvgNrTurns > 1 when RingSize > 1.'
            self._update_log(msg)
            _log.warning(msg[5:])
            return False
        val = int(val) if val > 1 else 1
        with self._lock_raw_orbs:
            self._spass_average = val
            self._reset_orbs()
        self.run_callbacks('SPassAvgNrTurns-RB', val)
        Thread(target=self._prepare_mode, daemon=True).start()
        return True

    def set_smooth_reset(self, _):
        """."""
        with self._lock_raw_orbs:
            self._reset_orbs()
        return True

    def set_reforb(self, plane, orb):
        """."""
        msg = 'Setting New Reference Orbit.'
        self._update_log(msg)
        _log.info(msg)
        orb = _np.array(orb, dtype=float)
        nrb = self._csorb.nr_bpms * self._ring_extension
        if orb.size % self._csorb.nr_bpms:
            msg = 'ERR: Wrong RefOrb Size.'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        elif orb.size < nrb:
            msg = 'WARN: Orb Size is too small. Replicating...'
            self._update_log(msg)
            _log.error(msg[6:])
            nrep = int(nrb//orb.size) + 1
            orb2 = _np.tile(orb, nrep)
            orb = orb2[:nrb]
        self.ref_orbs[plane] = orb
        self._save_ref_orbits()
        with self._lock_raw_orbs:
            self._reset_orbs()
        self.run_callbacks('RefOrb'+plane+'-RB', orb[:nrb])
        return True

    def set_orbit_acq_rate(self, value):
        """."""
        if self.is_trigmode() and value > self._csorb.MAX_TRIGMODE_RATE:
            msg = 'ERR: In triggered mode cannot set rate > {:d}.'.format(
                self._csorb.MAX_TRIGMODE_RATE)
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        elif self.is_sloworb() and value < self._csorb.MIN_SLOWORB_RATE:
            msg = 'ERR: In SlowOrb cannot set rate < {:d}.'.format(
                self._csorb.MIN_SLOWORB_RATE)
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        self._acqrate = value
        self._orbit_thread.interval = 1/value
        self.run_callbacks('OrbAcqRate-RB', value)
        return True

    def set_orbit_mode(self, value):
        """."""
        bo1 = self.is_trigmode()
        bo2 = not self.is_trigmode(value)
        omode = self._mode
        if not bo2:
            acqrate = self._csorb.MAX_TRIGMODE_RATE
            dic = {'lolim': 0.01, 'hilim': acqrate}
        else:
            acqrate = self._oldacqrate
            dic = {'lolim': self._csorb.MIN_SLOWORB_RATE, 'hilim': 100}
        self.run_callbacks('OrbAcqRate-SP', acqrate, **dic)
        self.run_callbacks('OrbAcqRate-RB', acqrate, **dic)

        with self._lock_raw_orbs:
            self._mode = value
            if bo1 == bo2:
                self._oldacqrate = self._acqrate
                self.set_orbit_acq_rate(acqrate)
            self._reset_orbs()
        Thread(
            target=self._prepare_mode,
            kwargs={'oldmode': omode, }, daemon=True).start()
        self.run_callbacks('SOFBMode-Sts', value)
        return True

    def set_sync_with_injection(self, boo):
        """."""
        self._sync_with_inj = bool(boo)
        self.run_callbacks('SyncWithInjection-Sts', bool(boo))
        return True

    def _prepare_mode(self, oldmode=None):
        """."""
        oldmode = self._mode if oldmode is None else oldmode
        self.set_trig_acq_control(self._csorb.TrigAcqCtrl.Abort)

        if not self.is_trigmode():
            self.acq_config_bpms()
            return True

        points = self._ring_extension
        if self.is_singlepass():
            chan = self._csorb.TrigAcqChan.ADCSwp
            rep = self._csorb.TrigAcqRepeat.Repetitive
            points *= self._spass_average * self.bpms[0].tbtrate
        elif self.is_multiturn():
            chan = self._csorb.TrigAcqChan.TbT
            rep = self._csorb.TrigAcqRepeat.Repetitive
            points *= self._mturndownsample

        if self._mode != oldmode:
            self.run_callbacks('TrigAcqChan-Sel', chan)
            self.set_trig_acq_channel(chan)
            self.run_callbacks('TrigAcqRepeat-Sel', rep)
            self.set_trig_acq_repeat(rep)
            if self.acqtrignrsamples < points:
                pts = points - self._acqtrignrsamplespre
                self.run_callbacks('TrigNrSamplesPost-SP', pts)
                self.set_acq_nrsamples(pts, ispost=True)
        self._update_time_vector()
        self.acq_config_bpms()

        self.set_trig_acq_control(self._csorb.TrigAcqCtrl.Start)
        return True

    def set_orbit_multiturn_idx(self, value):
        """."""
        maxidx = self.acqtrignrsamples // self._mturndownsample
        maxidx *= self._acqtrignrshots
        if value >= maxidx:
            value = maxidx-1
            msg = 'WARN: MTurnIdx is too large. Redefining...'
            self._update_log(msg)
            _log.warning(msg[6:])
        with self._lock_raw_orbs:
            self._multiturnidx = int(value)
        self.run_callbacks('MTurnIdx-RB', self._multiturnidx)
        self.run_callbacks(
            'MTurnIdxTime-Mon', self._timevector[self._multiturnidx])
        return True

    def acq_config_bpms(self, *args):
        """."""
        _ = args
        for bpm in self.bpms:
            if self.is_multiturn():
                bpm.mode = _csbpm.OpModes.MultiBunch
                bpm.switching_mode = _csbpm.SwModes.direct
                bpm.configure()
                self.timing.configure()
            elif self.is_singlepass():
                bpm.mode = _csbpm.OpModes.MultiBunch
                bpm.switching_mode = _csbpm.SwModes.direct
                bpm.configure()
                self.timing.configure()
            elif self.is_sloworb():
                bpm.switching_mode = _csbpm.SwModes.switching
        Thread(target=self._synchronize_bpms, daemon=True).start()
        return True

    def _synchronize_bpms(self):
        for bpm in self.bpms:
            bpm.monit1_sync_enbl = _csbpm.EnbldDsbld.enabled
            bpm.monit_sync_enbl = _csbpm.EnbldDsbld.enabled
        _time.sleep(0.5)
        for bpm in self.bpms:
            bpm.monit_sync_enbl = _csbpm.EnbldDsbld.disabled
            bpm.monit1_sync_enbl = _csbpm.EnbldDsbld.disabled

    def set_trig_acq_control(self, value):
        """."""
        acqctrl = self._csorb.TrigAcqCtrl
        if value == acqctrl.Start:
            self._wait_bpms()

        for bpm in self.bpms:
            bpm.ctrl = value
        self.run_callbacks('TrigAcqCtrl-Sts', value)

        if value in {acqctrl.Stop, acqctrl.Abort}:
            self._wait_bpms()
        return True

    def set_trig_acq_channel(self, value):
        """."""
        try:
            val = self._csorb.TrigAcqChan._fields[value]
            val = _csbpm.AcqChan._fields.index(val)
        except (IndexError, ValueError):
            return False
        for bpm in self.bpms:
            bpm.acq_type = val
        self.run_callbacks('TrigAcqChan-Sts', value)
        self._update_time_vector(channel=val)
        return True

    def set_trig_acq_trigger(self, value):
        """."""
        val = _csbpm.AcqTrigTyp.Data
        if value == self._csorb.TrigAcqTrig.External:
            val = _csbpm.AcqTrigTyp.External
        for bpm in self.bpms:
            bpm.acq_trigger = val
        self.run_callbacks('TrigAcqTrigger-Sts', value)
        return True

    def set_trig_acq_repeat(self, value):
        """."""
        for bpm in self.bpms:
            bpm.acq_repeat = value
        self.run_callbacks('TrigAcqRepeat-Sts', value)
        return True

    def set_trig_acq_datachan(self, value):
        """."""
        try:
            val = self._csorb.TrigAcqDataChan._fields[value]
            val = _csbpm.AcqChan._fields.index(val)
        except (IndexError, ValueError):
            return False
        for bpm in self.bpms:
            bpm.acq_trig_datatype = val
        self.run_callbacks('TrigDataChan-Sts', value)
        return True

    def set_trig_acq_datasel(self, value):
        """."""
        for bpm in self.bpms:
            bpm.acq_trig_datasel = value
        self.run_callbacks('TrigDataSel-Sts', value)
        return True

    def set_trig_acq_datathres(self, value):
        """."""
        for bpm in self.bpms:
            bpm.acq_trig_datathres = value
        self.run_callbacks('TrigDataThres-RB', value)
        return True

    def set_trig_acq_datahyst(self, value):
        """."""
        for bpm in self.bpms:
            bpm.acq_trig_datahyst = value
        self.run_callbacks('TrigDataHyst-RB', value)
        return True

    def set_trig_acq_datapol(self, value):
        """."""
        for bpm in self.bpms:
            bpm.acq_trig_datapol = value
        self.run_callbacks('TrigDataPol-Sts', value)
        return True

    def set_acq_nrsamples(self, val, ispost=True):
        """."""
        val = int(val) if val > 0 else 0
        val = val if val < 20000 else 20000
        suf = 'post' if ispost else 'pre'
        with self._lock_raw_orbs:
            for bpm in self.bpms:
                setattr(bpm, 'nrsamples' + suf, val)
            self._reset_orbs()
            setattr(self, '_acqtrignrsamples' + suf, val)
        self.run_callbacks('TrigNrSamples'+suf.title()+'-RB', val)
        self._update_time_vector()
        return True

    def set_trig_acq_nrshots(self, val):
        """."""
        val = int(val) if val > 1 else 1
        val = val if val < 1000 else 1000
        with self._lock_raw_orbs:
            for bpm in self.bpms:
                bpm.nrshots = val
            self.timing.nrpulses = val
            self._reset_orbs()
            self._acqtrignrshots = val
        self.run_callbacks('TrigNrShots-RB', val)
        self._update_time_vector()
        return True

    def set_poly_calibration(self, val):
        """."""
        value = _csbpm.EnbldDsbld.enabled
        if val == self._csorb.EnbldDsbld.Dsbld:
            value = _csbpm.EnbldDsbld.disabled
        for bpm in self.bpms:
            bpm.polycal = value
        self.run_callbacks('PolyCalibration-Sts', val)
        return True

    def set_mturndownsample(self, val):
        """."""
        if self._ring_extension != 1 and val != 1:
            msg = 'ERR: Cannot set DownSample > 1 when RingSize > 1.'
            self._update_log(msg)
            _log.warning(msg[5:])
            return False
        val = int(val) if val > 1 else 1
        val = val if val < 1000 else 1000
        with self._lock_raw_orbs:
            self._mturndownsample = val
            self._reset_orbs()
        self.run_callbacks('MTurnDownSample-RB', val)
        Thread(target=self._prepare_mode, daemon=True).start()
        return True

    def acquire_mturn_orbit(self, _):
        """Acquire Multiturn data from BPMs."""
        Thread(target=self._update_multiturn_orbits, daemon=True).start()

    def _wait_bpms(self):
        """."""
        for _ in range(40):
            if all(map(lambda x: x.is_ok, self.bpms)):
                break
            _time.sleep(0.1)
        else:
            _log.warning('Timeout waiting BPMs.')

    def _update_time_vector(self, delay=None, duration=None, channel=None):
        """."""
        if not self.isring:
            return
        dly = (delay or self.timing.totaldelay or 0.0) * 1e-6  # from us to s
        dur = (duration or self.timing.duration or 0.0) * 1e-6  # from us to s
        channel = channel or self.bpms[0].acq_type or 0

        # revolution period in s
        if channel == _csbpm.AcqChan.Monit1:
            dtime = self.bpms[0].monit1period
        elif channel == _csbpm.AcqChan.FOFB:
            dtime = self.bpms[0].fofbperiod
        else:
            dtime = self.bpms[0].tbtperiod
        mult = self._mturndownsample * self._ring_extension
        dtime *= mult
        nrptpst = self.acqtrignrsamples // mult
        offset = self._acqtrignrsamplespre / mult
        nrst = self._acqtrignrshots
        shots = _np.arange(nrst)
        pts = _np.arange(nrptpst, dtype=float) + (0.5 - offset)
        vect = dly + dur/nrst*shots[:, None] + dtime*pts[None, :]
        self._timevector = vect.ravel()
        self.run_callbacks('MTurnTime-Mon', self._timevector)
        self.set_orbit_multiturn_idx(self._multiturnidx)

    def _load_ref_orbs(self):
        """."""
        if not _os.path.isfile(self._csorb.ref_orb_fname):
            return
        self.ref_orbs['X'], self.ref_orbs['Y'] = _np.loadtxt(
            self._csorb.ref_orb_fname, unpack=True)
        self.run_callbacks('RefOrbX-RB', self.ref_orbs['X'].copy())
        self.run_callbacks('RefOrbY-RB', self.ref_orbs['Y'].copy())

    def _save_ref_orbits(self):
        """."""
        refx = self.ref_orbs['X']
        refy = self.ref_orbs['Y']
        if refx.size < refy.size:
            ref = _np.zeros(refy.shape, dtype=float)
            ref[:refx.size] = refx
            refx = ref
        elif refy.size < refx.size:
            ref = _np.zeros(refx.shape, dtype=float)
            ref[:refy.size] = refy
            refy = ref
        orbs = _np.array([refx, refy]).T
        try:
            path = _os.path.split(self._csorb.ref_orb_fname)[0]
            if not _os.path.isdir(path):
                _os.mkdir(path)
            _np.savetxt(self._csorb.ref_orb_fname, orbs)
        except FileNotFoundError:
            msg = 'WARN: Could not save reference orbit in file.'
            self._update_log(msg)
            _log.warning(msg[6:])

    def _reset_orbs(self):
        """."""
        self.raw_orbs = {'X': [], 'Y': []}
        self.smooth_orb = {'X': None, 'Y': None}
        self.raw_sporbs = {'X': [], 'Y': [], 'Sum': []}
        self.smooth_sporb = {'X': None, 'Y': None, 'Sum': None}
        self.raw_mtorbs = {'X': [], 'Y': [], 'Sum': []}
        self.smooth_mtorb = {'X': None, 'Y': None, 'Sum': None}
        self.run_callbacks('BufferCount-Mon', 0)

    def _update_orbits(self):
        """."""
        try:
            count = 0
            if self.is_multiturn():
                self._update_multiturn_orbits()
                count = len(self.raw_mtorbs['X'])
            elif self.is_singlepass():
                self._update_singlepass_orbits()
                count = len(self.raw_sporbs['X'])
            elif self.is_sloworb():
                self._update_online_orbits()
                count = len(self.raw_orbs['X'])
            self.run_callbacks('BufferCount-Mon', count)
        except Exception as err:
            self._update_log('ERR: ' + str(err))
            _log.error(_traceback.format_exc())

    def _update_online_orbits(self):
        """."""
        posx, posy, nok = self._get_orbit_from_processes()
        posx /= 1000
        posy /= 1000
        nanx = _np.isnan(posx)
        nany = _np.isnan(posy)
        posx[nanx] = self.ref_orbs['X'][nanx]
        posy[nany] = self.ref_orbs['Y'][nany]
        if self._ring_extension > 1:
            posx = _np.tile(posx, (self._ring_extension, ))
            posy = _np.tile(posy, (self._ring_extension, ))
        orbs = {'X': posx, 'Y': posy}

        for plane in ('X', 'Y'):
            with self._lock_raw_orbs:
                raws = self.raw_orbs
                raws[plane].append(orbs[plane])
                raws[plane] = raws[plane][-self._smooth_npts:]
                if not raws[plane]:
                    return
                if self._smooth_meth == self._csorb.SmoothMeth.Average:
                    orb = _np.mean(raws[plane], axis=0)
                else:
                    orb = _np.median(raws[plane], axis=0)
            self.smooth_orb[plane] = orb
        self.new_orbit.set()

        self._sloworb_timeout += nok
        if self._sloworb_timeout >= 1000:
            self._sloworb_timeout = 0
        self.run_callbacks('SlowOrbTimeout-Mon', self._sloworb_timeout)
        for plane in ('X', 'Y'):
            orb = self.smooth_orb[plane]
            if orb is None:
                return
            dorb = orb - self.ref_orbs[plane]
            self.run_callbacks(f'SlowOrb{plane:s}-Mon', _np.array(orb))
            self.run_callbacks(f'DeltaOrb{plane:s}Avg-Mon', _bn.nanmean(dorb))
            self.run_callbacks(f'DeltaOrb{plane:s}Std-Mon', _bn.nanstd(dorb))
            self.run_callbacks(f'DeltaOrb{plane:s}Min-Mon', _bn.nanmin(dorb))
            self.run_callbacks(f'DeltaOrb{plane:s}Max-Mon', _bn.nanmax(dorb))

    def _get_orbit_from_processes(self):
        nr_bpms = self._csorb.nr_bpms
        out = []
        nok = []
        for pipe in self._mypipes_recv:
            res = pipe.recv()
            out.extend(res[:-1])
            nok.append(res[-1])
        for pipe in self._mypipes_send:
            pipe.send(True)
        orbx = _np.array(out[:nr_bpms], dtype=float)
        orby = _np.array(out[nr_bpms:], dtype=float)
        return orbx, orby, any(nok)

    def _update_multiturn_orbits(self):
        """."""
        if self._ring_extension != 1 and self._mturndownsample != 1:
            return
        orbs = {'X': [], 'Y': [], 'Sum': []}
        with self._lock_raw_orbs:  # I need the lock here to ensure consistency
            samp = self.acqtrignrsamples
            down = self._mturndownsample
            ringsz = self._ring_extension
            samp -= samp % (ringsz*down)
            if samp < 1:
                msg = 'ERR: Actual nr_samples in MTurn orb calc. is < 1.'
                self._update_log(msg)
                _log.error(msg[5:])
                return
            samp *= self._acqtrignrshots
            orbsz = self._csorb.nr_bpms * ringsz
            nr_pts = self._smooth_npts
            for i, bpm in enumerate(self.bpms):
                pos = bpm.mtposx
                if pos is None:
                    posx = _np.full(samp, self.ref_orbs['X'][i])
                elif pos.size < samp:
                    posx = _np.full(samp, self.ref_orbs['X'][i])
                    posx[:pos.size] = pos
                else:
                    posx = pos[:samp]
                pos = bpm.mtposy
                if pos is None:
                    posy = _np.full(samp, self.ref_orbs['Y'][i])
                elif pos.size < samp:
                    posy = _np.full(samp, self.ref_orbs['Y'][i])
                    posy[:pos.size] = pos
                else:
                    posy = pos[:samp]
                pos = bpm.mtsum
                if pos is None:
                    psum = _np.full(samp, 0)
                elif pos.size < samp:
                    psum = _np.full(samp, 0)
                    psum[:pos.size] = pos
                else:
                    psum = pos[:samp]
                orbs['X'].append(posx)
                orbs['Y'].append(posy)
                orbs['Sum'].append(psum)

            for pln, raw in self.raw_mtorbs.items():
                norb = _np.array(orbs[pln], dtype=float)  # bpms x turns
                norb = norb.T.reshape(-1, orbsz)  # turns/rz x rz*bpms
                if self.update_raws:
                    raw.append(norb)
                del raw[:-nr_pts]
                if not raw:
                    return
                if self._smooth_meth == self._csorb.SmoothMeth.Average:
                    orb = _np.mean(raw, axis=0)
                else:
                    orb = _np.median(raw, axis=0)
                if down > 1:
                    orb = _np.mean(orb.reshape(-1, down, orbsz), axis=1)
                self.smooth_mtorb[pln] = orb
                orbs[pln] = orb
        idx = min(self._multiturnidx, orb.shape[0])
        for pln, orb in orbs.items():
            name = ('Orb' if pln != 'Sum' else '') + pln
            self.run_callbacks('MTurn' + name + '-Mon', orb.ravel())
            self.run_callbacks(
                'MTurnIdx' + name + '-Mon', orb[idx, :].ravel())

    def _update_singlepass_orbits(self):
        """."""
        if self._ring_extension != 1 and self._spass_average != 1:
            return
        orbs = {'X': [], 'Y': [], 'Sum': []}
        ringsz = self._ring_extension
        down = self._spass_average
        use_bg = self._spass_usebg == self._csorb.SPassUseBg.Using
        use_bg &= bool(self._spass_bgs[-1])  # check if there is a BG saved
        pvv = self._csorb.SPassUseBg
        self.run_callbacks(
            'SPassUseBg-Sts', pvv.Using if use_bg else pvv.NotUsing)
        with self._lock_raw_orbs:  # I need the lock here to assure consistency
            dic = {
                'maskbeg': self._spass_mask[0],
                'maskend': self._spass_mask[1],
                'nturns': ringsz * down}
            nr_pts = self._smooth_npts
            for i, bpm in enumerate(self.bpms):
                dic.update({
                    'refx': self.ref_orbs['X'][i],
                    'refy': self.ref_orbs['Y'][i],
                    'bg': self._spass_bgs[i] if use_bg else dict()})
                orbx, orby, summ = bpm.calc_sp_multiturn_pos(**dic)
                orbs['X'].append(orbx)
                orbs['Y'].append(orby)
                orbs['Sum'].append(summ)

            for pln, raw in self.raw_sporbs.items():
                norb = _np.array(orbs[pln], dtype=float).T  # turns x bpms
                norb = norb.reshape(-1)
                if self.update_raws:
                    raw.append(norb)
                del raw[:-nr_pts]
                if not raw:
                    return
                if self._smooth_meth == self._csorb.SmoothMeth.Average:
                    orb = _np.mean(raw, axis=0)
                else:
                    orb = _np.median(raw, axis=0)
                if down > 1:
                    orb = _np.mean(orb.reshape(down, -1), axis=0)
                self.smooth_sporb[pln] = orb
                name = ('Orb' if pln != 'Sum' else '') + pln
                self.run_callbacks('SPass' + name + '-Mon', list(orb))

    def _update_status(self):
        """."""
        status = 0b11111

        if self.is_trigmode():
            tim_conn = self.timing.connected
            tim_conf = self.timing.is_ok
        else:
            tim_conn = True
            tim_conf = True
        status = _util.update_bit(status, bit_pos=0, bit_val=not tim_conn)
        status = _util.update_bit(status, bit_pos=1, bit_val=not tim_conf)

        if self._mode == self._csorb.SOFBMode.Offline:
            bpm_conn = True
            bpm_stt = True
        else:
            bpm_conn = all(bpm.connected for bpm in self.bpms)
            bpm_stt = all(bpm.state for bpm in self.bpms)
        status = _util.update_bit(v=status, bit_pos=2, bit_val=not bpm_conn)
        status = _util.update_bit(v=status, bit_pos=3, bit_val=not bpm_stt)

        isok = True
        if self.is_trigmode():
            isok = all(map(lambda x: x.is_ok, self.bpms))
        elif self.is_sloworb():
            isok = all(map(
                lambda x: x.switching_mode == _csbpm.SwModes.switching,
                self.bpms))
        status = _util.update_bit(v=status, bit_pos=4, bit_val=not isok)

        self._status = status
        self.run_callbacks('OrbStatus-Mon', status)
        self._update_bpmoffsets()

    def _update_bpmoffsets(self):
        """."""
        nrb = self._csorb.nr_bpms
        orbx = _np.zeros(nrb * self._ring_extension, dtype=float)
        orby = orbx.copy()
        for i, bpm in enumerate(self.bpms):
            orbx[i::nrb] = bpm.offsetx or 0.0
            orby[i::nrb] = bpm.offsety or 0.0
        self.run_callbacks('BPMOffsetX-Mon', orbx)
        self.run_callbacks('BPMOffsetY-Mon', orby)

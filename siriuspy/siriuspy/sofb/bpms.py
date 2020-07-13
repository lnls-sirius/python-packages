"""Module to deal with orbit acquisition."""
import logging as _log
import numpy as _np

from ..epics import PV as _PV
from ..diag.bpm.csdev import Const as _csbpm
from ..timesys import csdev as _cstime
from ..search import HLTimeSearch as _HLTimesearch
from ..envars import VACA_PREFIX as LL_PREF

from .base_class import BaseTimingConfig as _BaseTimingConfig

TIMEOUT = 0.05


class BPM(_BaseTimingConfig):
    """."""

    def __init__(self, name, callback=None):
        """."""
        super().__init__(name[:2], callback)
        self._name = name
        self._orb_conv_unit = self._csorb.ORBIT_CONVERSION_UNIT
        pvpref = LL_PREF + self._name + ':'
        opt = {'connection_timeout': TIMEOUT}
        self._poskx = _PV(pvpref + 'PosKx-RB', **opt)
        self._posky = _PV(pvpref + 'PosKy-RB', **opt)
        self._ksum = _PV(pvpref + 'PosKsum-RB', **opt)
        self._spposx = _PV(pvpref + 'SPPosX-Mon', **opt)
        self._spposy = _PV(pvpref + 'SPPosY-Mon', **opt)
        self._spsum = _PV(pvpref + 'SPSum-Mon', **opt)
        self._polyx = _PV(pvpref + 'GEN_PolyXArrayCoeff-RB', **opt)
        self._polyy = _PV(pvpref + 'GEN_PolyYArrayCoeff-RB', **opt)
        opt['auto_monitor'] = False
        self._arraya = _PV(pvpref + 'GEN_AArrayData', **opt)
        self._arrayb = _PV(pvpref + 'GEN_BArrayData', **opt)
        self._arrayc = _PV(pvpref + 'GEN_CArrayData', **opt)
        self._arrayd = _PV(pvpref + 'GEN_DArrayData', **opt)
        self._arrayx = _PV(pvpref + 'GEN_XArrayData', **opt)
        self._arrayy = _PV(pvpref + 'GEN_YArrayData', **opt)
        self._arrays = _PV(pvpref + 'GEN_SUMArrayData', **opt)
        opt.pop('auto_monitor')
        self._offsetx = _PV(pvpref + 'PosXOffset-RB', **opt)
        self._offsety = _PV(pvpref + 'PosYOffset-RB', **opt)
        self._config_ok_vals = {
            'asyn.ENBL': _csbpm.EnblTyp.Enable,
            'ACQBPMMode': _csbpm.OpModes.MultiBunch,
            'ACQChannel': _csbpm.AcqChan.ADC,
            # 'ACQNrShots': 1,
            'ACQShots': 1,
            # 'ACQTriggerHwDly': 0.0,  # NOTE: leave this property commented
            'ACQUpdateTime': 0.001,
            # 'ACQNrSamplesPre': 0,
            'ACQSamplesPre': 0,
            # 'ACQNrSamplesPost': 200,
            'ACQSamplesPost': 360,
            # 'ACQCtrl': _csbpm.AcqEvents.Stop,
            'ACQTriggerEvent': _csbpm.AcqEvents.Stop,
            # 'ACQTriggerType': _csbpm.AcqTrigTyp.External,
            'ACQTrigger': _csbpm.AcqTrigTyp.External,
            'ACQTriggerRep': _csbpm.AcqRepeat.Normal,
            # 'ACQTriggerDataChan': _csbpm.AcqChan.Monit1,
            'ACQDataTrigChan': _csbpm.AcqChan.ADC,
            'ACQTriggerDataSel': _csbpm.AcqDataTyp.A,
            'ACQTriggerDataThres': 1,
            'ACQTriggerDataPol': _csbpm.Polarity.Positive,
            'ACQTriggerDataHyst': 0,
            'TbtTagEn': _csbpm.EnbldDsbld.disabled,  # Enable TbT sync Timing
            'Monit1TagEn': _csbpm.EnbldDsbld.disabled,
            'MonitTagEn': _csbpm.EnbldDsbld.disabled,
            'TbtDataMaskEn': _csbpm.EnbldDsbld.disabled,  # Enable use of mask
            'TbtDataMaskSamplesBeg': 0,
            'TbtDataMaskSamplesEnd': 0,
            'XYPosCal': _csbpm.EnbldDsbld.enabled,
            'SUMPosCal': _csbpm.EnbldDsbld.enabled}
        pvs = {
            'asyn.ENBL': 'asyn.ENBL',
            'ACQBPMMode': 'ACQBPMMode-Sel',
            'ACQChannel': 'ACQChannel-Sel',
            # 'ACQNrShots': 'ACQNrShots-SP',
            'ACQShots': 'ACQShots-SP',
            # 'ACQTriggerHwDly': 'ACQTriggerHwDly-SP',
            'ACQUpdateTime': 'ACQUpdateTime-SP',
            # 'ACQNrSamplesPre': 'ACQNrSamplesPre-SP',
            'ACQSamplesPre': 'ACQSamplesPre-SP',
            # 'ACQNrSamplesPost': 'ACQNrSamplesPost-SP',
            'ACQSamplesPost': 'ACQSamplesPost-SP',
            # 'ACQCtrl': 'ACQCtrl-Sel',
            'ACQTriggerEvent': 'ACQTriggerEvent-Sel',
            # 'ACQTriggerType': 'ACQTriggerType-Sel',
            'ACQTrigger': 'ACQTrigger-Sel',
            'ACQTriggerRep': 'ACQTriggerRep-Sel',
            # 'ACQTriggerDataChan': 'ACQTriggerDataChan-Sel',
            'ACQDataTrigChan': 'ACQDataTrigChan-Sel',
            # 'ACQTriggerDataSel': 'ACQTriggerDataSel-Sel',
            'ACQTriggerDataSel': 'ACQTriggerDataSel-SP',
            'ACQTriggerDataThres': 'ACQTriggerDataThres-SP',
            'ACQTriggerDataPol': 'ACQTriggerDataPol-Sel',
            'ACQTriggerDataHyst': 'ACQTriggerDataHyst-SP',
            'TbtTagEn': 'TbtTagEn-Sel',  # Enable TbT sync with timing
            'Monit1TagEn': 'Monit1TagEn-Sel',  # Enable Monit1 sync with timing
            'MonitTagEn': 'MonitTagEn-Sel',  # Enable Monit sync with timing
            'TbtDataMaskEn': 'TbtDataMaskEn-Sel',  # Enable use of mask
            'TbtDataMaskSamplesBeg': 'TbtDataMaskSamplesBeg-SP',
            'TbtDataMaskSamplesEnd': 'TbtDataMaskSamplesEnd-SP',
            'XYPosCal': 'XYPosCal-Sel',
            'SUMPosCal': 'SUMPosCal-Sel'}

        self._config_pvs_sp = {
            k: _PV(pvpref + v, **opt) for k, v in pvs.items()}
        pvs = {
            'asyn.ENBL': 'asyn.ENBL',
            'asyn.CNCT': 'asyn.CNCT',
            'INFOClkFreq': 'INFOClkFreq-RB',
            'INFOHarmonicNumber': 'INFOHarmonicNumber-RB',
            'INFOTBTRate': 'INFOTBTRate-RB',
            'INFOFOFBRate': 'INFOFOFBRate-RB',
            'INFOMONITRate': 'INFOMONITRate-RB',
            'INFOMONIT1Rate': 'INFOMONIT1Rate-RB',
            'ACQBPMMode': 'ACQBPMMode-Sts',
            'ACQChannel': 'ACQChannel-Sts',
            # 'ACQNrShots': 'ACQNrShots-RB',
            'ACQShots': 'ACQShots-RB',
            # 'ACQTriggerHwDly': 'ACQTriggerHwDly-RB',
            'ACQUpdateTime': 'ACQUpdateTime-RB',
            # 'ACQNrSamplesPre': 'ACQNrSamplesPre-RB',
            'ACQSamplesPre': 'ACQSamplesPre-RB',
            # 'ACQNrSamplesPost': 'ACQNrSamplesPost-RB',
            'ACQSamplesPost': 'ACQSamplesPost-RB',
            # 'ACQCtrl': 'ACQCtrl-Sts',
            'ACQTriggerEvent': 'ACQTriggerEvent-Sts',
            # 'ACQStatus': 'ACQStatus-Mon',
            'ACQStatus': 'ACQStatus-Sts',
            # 'ACQTriggerType': 'ACQTriggerType-Sts',
            'ACQTrigger': 'ACQTrigger-Sts',
            'ACQTriggerRep': 'ACQTriggerRep-Sts',
            # 'ACQTriggerDataChan': 'ACQTriggerDataChan-Sts',
            'ACQDataTrigChan': 'ACQDataTrigChan-Sts',
            # 'ACQTriggerDataSel': 'ACQTriggerDataSel-Sts',
            'ACQTriggerDataSel': 'ACQTriggerDataSel-RB',
            'ACQTriggerDataThres': 'ACQTriggerDataThres-RB',
            'ACQTriggerDataPol': 'ACQTriggerDataPol-Sts',
            'ACQTriggerDataHyst': 'ACQTriggerDataHyst-RB',
            'TbtTagEn': 'TbtTagEn-Sts',
            'Monit1TagEn': 'Monit1TagEn-Sts',
            'MonitTagEn': 'MonitTagEn-Sts',
            'TbtDataMaskEn': 'TbtDataMaskEn-Sts',
            'TbtDataMaskSamplesBeg': 'TbtDataMaskSamplesBeg-RB',
            'TbtDataMaskSamplesEnd': 'TbtDataMaskSamplesEnd-RB',
            'XYPosCal': 'XYPosCal-Sts',
            'SUMPosCal': 'SUMPosCal-Sts'}
        self._config_pvs_rb = {
            k: _PV(pvpref + v, **opt) for k, v in pvs.items()}

    @property
    def name(self):
        """."""
        return self._name

    @property
    def connected(self):
        """."""
        conn = super().connected
        pvs = (
            self._spposx, self._spposy, self._spsum,
            self._arrayx, self._arrayy, self._arrays,
            self._offsetx, self._offsety,
            self._polyx, self._polyx,
            self._arraya, self._arrayb, self._arrayc, self._arrayd,
            self._poskx, self._posky, self._ksum)
        for pvobj in pvs:
            if not pvobj.connected:
                _log.debug('NOT CONN: ' + pvobj.pvname)
            conn &= pvobj.connected
        return conn

    @property
    def is_ok(self):
        """."""
        if not super().is_ok:
            return False

        pvobj = self._config_pvs_rb['ACQStatus']
        stts = _csbpm.AcqStates
        okay = pvobj.value not in {
            stts.Error, stts.No_Memory, stts.Too_Few_Samples,
            stts.Too_Many_Samples, stts.Acq_Overflow}

        if self._config_ok_vals['ACQTriggerEvent'] == _csbpm.AcqEvents.Start:
            okay &= pvobj.value not in {stts.Idle, stts.Aborted}
        else:
            okay &= pvobj.value not in {
                stts.Waiting, stts.External_Trig, stts.Data_Trig,
                stts.Software_Trig, stts.Acquiring}
        if not okay:
            msg = 'ERR: Error in {0:s}'.format(pvobj.pvname)
            self.run_callbacks('Log-Mon', msg)
            _log.warning(msg[5:])
        return okay

    @property
    def state(self):
        """."""
        pvobj = self._config_pvs_rb['asyn.ENBL']
        if pvobj.connected:
            return pvobj.value == _csbpm.EnblTyp.Enable
        return False

    @state.setter
    def state(self, boo):
        """."""
        val = _csbpm.EnblTyp.Enable if boo else _csbpm.EnblTyp.Disable
        pvobj = self._config_pvs_sp['asyn.ENBL']
        self._config_ok_vals['asyn.ENBL'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def adcfreq(self):
        """."""
        defv = 218446014.0 if self._csorb.acc == 'BO' else 220870069.0
        pvobj = self._config_pvs_rb['INFOClkFreq']
        val = pvobj.value if pvobj.connected else defv
        return val if val else defv

    @property
    def tbtrate(self):
        """."""
        defv = 362 if self._csorb.acc == 'BO' else 382
        pvobj = self._config_pvs_rb['INFOTBTRate']
        val = pvobj.value if pvobj.connected else defv
        return val if val else defv

    @property
    def tbtperiod(self):
        """."""
        return self.tbtrate / self.adcfreq

    @property
    def fofbrate(self):
        """."""
        defv = (362 if self._csorb.acc == 'BO' else 382) * 24
        pvobj = self._config_pvs_rb['INFOFOFBRate']
        val = pvobj.value if pvobj.connected else defv
        return val if val else defv

    @property
    def fofbperiod(self):
        """."""
        return self.fofbrate / self.adcfreq

    @property
    def monitrate(self):
        """."""
        defv = (362 if self._csorb.acc == 'BO' else 382) * 59904
        pvobj = self._config_pvs_rb['INFOMONITRate']
        val = pvobj.value if pvobj.connected else defv
        return val if val else defv

    @property
    def monitperiod(self):
        """."""
        return self.monitrate / self.adcfreq

    @property
    def monit1rate(self):
        """."""
        defv = (362 if self._csorb.acc == 'BO' else 382) * 603
        pvobj = self._config_pvs_rb['INFOMONIT1Rate']
        val = pvobj.value if pvobj.connected else defv
        return val if val else defv

    @property
    def monit1period(self):
        """."""
        return self.monit1rate / self.adcfreq

    @property
    def poskx(self):
        """."""
        defv = 1
        pvobj = self._poskx
        val = pvobj.value if pvobj.connected else defv
        return val if val else defv

    @property
    def posky(self):
        """."""
        defv = 1
        pvobj = self._posky
        val = pvobj.value if pvobj.connected else defv
        return val if val else defv

    @property
    def polyx(self):
        """."""
        pvobj = self._polyx
        if pvobj.connected:
            val = pvobj.value
            if val is not None:
                return val
        defv = _np.zeros(15, dtype=float)
        defv[0] = 1
        return defv

    @property
    def polyy(self):
        """."""
        pvobj = self._polyy
        if pvobj.connected:
            val = pvobj.value
            if val is not None:
                return val
        defv = _np.zeros(15, dtype=float)
        defv[0] = 1
        return defv

    @property
    def ksum(self):
        """."""
        defv = 1
        pvobj = self._ksum
        val = pvobj.value if pvobj.connected else defv
        return val if val else defv

    @property
    def mode(self):
        """."""
        pvobj = self._config_pvs_rb['ACQBPMMode']
        return pvobj.value if pvobj.connected else _csbpm.OpModes.MultiBunch

    @mode.setter
    def mode(self, mode):
        """."""
        pvobj = self._config_pvs_sp['ACQBPMMode']
        self._config_ok_vals['ACQBPMMode'] = mode
        if pvobj.connected:
            pvobj.value = mode

    @property
    def spposx(self):
        """."""
        pvobj = self._spposx
        val = pvobj.value if pvobj.connected else None
        if val is not None:
            return self._orb_conv_unit*val

    @property
    def spposy(self):
        """."""
        pvobj = self._spposy
        val = pvobj.value if pvobj.connected else None
        if val is not None:
            return self._orb_conv_unit*val

    @property
    def spsum(self):
        """."""
        pvobj = self._spsum
        val = pvobj.value if pvobj.connected else None
        if val is not None:
            return val

    @property
    def arraya(self):
        """."""
        pvobj = self._arraya
        return pvobj.get() if pvobj.connected else None

    @property
    def arrayb(self):
        """."""
        pvobj = self._arrayb
        return pvobj.get() if pvobj.connected else None

    @property
    def arrayc(self):
        """."""
        pvobj = self._arrayc
        return pvobj.get() if pvobj.connected else None

    @property
    def arrayd(self):
        """."""
        pvobj = self._arrayd
        return pvobj.get() if pvobj.connected else None

    @property
    def mtposx(self):
        """."""
        pvobj = self._arrayx
        val = pvobj.get() if pvobj.connected else None
        if val is not None:
            return self._orb_conv_unit*val

    @property
    def mtposy(self):
        """."""
        pvobj = self._arrayy
        val = pvobj.get() if pvobj.connected else None
        if val is not None:
            return self._orb_conv_unit*val

    @property
    def mtsum(self):
        """."""
        pvobj = self._arrays
        val = pvobj.get() if pvobj.connected else None
        if val is not None:
            return val

    @property
    def offsetx(self):
        """."""
        pvobj = self._offsetx
        val = pvobj.value if pvobj.connected else None
        if val is not None:
            return self._orb_conv_unit*val

    @property
    def offsety(self):
        """."""
        pvobj = self._offsety
        val = pvobj.value if pvobj.connected else None
        if val is not None:
            return self._orb_conv_unit*val

    @property
    def ctrl(self):
        """."""
        # pvobj = self._config_pvs_rb['ACQCtrl']
        pvobj = self._config_pvs_rb['ACQTriggerEvent']
        return pvobj.value if pvobj.connected else None

    @ctrl.setter
    def ctrl(self, val):
        """."""
        # pvobj = self._config_pvs_sp['ACQCtrl']
        pvobj = self._config_pvs_sp['ACQTriggerEvent']
        # self._config_ok_vals['ACQCtrl'] = val
        self._config_ok_vals['ACQTriggerEvent'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def acq_type(self):
        """."""
        pvobj = self._config_pvs_rb['ACQChannel']
        return pvobj.value if pvobj.connected else None

    @acq_type.setter
    def acq_type(self, val):
        """."""
        pvobj = self._config_pvs_sp['ACQChannel']
        self._config_ok_vals['ACQChannel'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def acq_trigger(self):
        """."""
        # pvobj = self._config_pvs_rb['ACQTriggerType']
        pvobj = self._config_pvs_rb['ACQTrigger']
        return pvobj.value if pvobj.connected else None

    @acq_trigger.setter
    def acq_trigger(self, val):
        """."""
        # pvobj = self._config_pvs_sp['ACQTriggerType']
        pvobj = self._config_pvs_sp['ACQTrigger']
        # self._config_ok_vals['ACQTriggerType'] = val
        self._config_ok_vals['ACQTrigger'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def acq_repeat(self):
        """."""
        pvobj = self._config_pvs_rb['ACQTriggerRep']
        return pvobj.value if pvobj.connected else None

    @acq_repeat.setter
    def acq_repeat(self, val):
        """."""
        pvobj = self._config_pvs_sp['ACQTriggerRep']
        self._config_ok_vals['ACQTriggerRep'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def acq_trig_datatype(self):
        """."""
        # pvobj = self._config_pvs_rb['ACQTriggerDataChan']
        pvobj = self._config_pvs_rb['ACQDataTrigChan']
        return pvobj.value if pvobj.connected else None

    @acq_trig_datatype.setter
    def acq_trig_datatype(self, val):
        """."""
        # pvobj = self._config_pvs_sp['ACQTriggerDataChan']
        pvobj = self._config_pvs_sp['ACQDataTrigChan']
        # self._config_ok_vals['ACQTriggerDataChan'] = val
        self._config_ok_vals['ACQDataTrigChan'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def acq_trig_datasel(self):
        """."""
        pvobj = self._config_pvs_rb['ACQTriggerDataSel']
        return pvobj.value if pvobj.connected else None

    @acq_trig_datasel.setter
    def acq_trig_datasel(self, val):
        """."""
        pvobj = self._config_pvs_sp['ACQTriggerDataSel']
        self._config_ok_vals['ACQTriggerDataSel'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def acq_trig_datathres(self):
        """."""
        pvobj = self._config_pvs_rb['ACQTriggerDataThres']
        return pvobj.value if pvobj.connected else None

    @acq_trig_datathres.setter
    def acq_trig_datathres(self, val):
        """."""
        pvobj = self._config_pvs_sp['ACQTriggerDataThres']
        self._config_ok_vals['ACQTriggerDataThres'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def acq_trig_datahyst(self):
        """."""
        pvobj = self._config_pvs_rb['ACQTriggerDataHyst']
        return pvobj.value if pvobj.connected else None

    @acq_trig_datahyst.setter
    def acq_trig_datahyst(self, val):
        """."""
        pvobj = self._config_pvs_sp['ACQTriggerDataHyst']
        self._config_ok_vals['ACQTriggerDataHyst'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def acq_trig_datapol(self):
        """."""
        pvobj = self._config_pvs_rb['ACQTriggerDataPol']
        return pvobj.value if pvobj.connected else None

    @acq_trig_datapol.setter
    def acq_trig_datapol(self, val):
        """."""
        pvobj = self._config_pvs_sp['ACQTriggerDataPol']
        self._config_ok_vals['ACQTriggerDataPol'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def tbt_sync_enbl(self):
        """."""
        pvobj = self._config_pvs_rb['TbtTagEn']
        return pvobj.value if pvobj.connected else None

    @tbt_sync_enbl.setter
    def tbt_sync_enbl(self, val):
        """."""
        pvobj = self._config_pvs_sp['TbtTagEn']
        self._config_ok_vals['TbtTagEn'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def monit1_sync_enbl(self):
        """."""
        pvobj = self._config_pvs_rb['Monit1TagEn']
        return pvobj.value if pvobj.connected else None

    @monit1_sync_enbl.setter
    def monit1_sync_enbl(self, val):
        """."""
        pvobj = self._config_pvs_sp['Monit1TagEn']
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def monit_sync_enbl(self):
        """."""
        pvobj = self._config_pvs_rb['MonitTagEn']
        return pvobj.value if pvobj.connected else None

    @monit_sync_enbl.setter
    def monit_sync_enbl(self, val):
        """."""
        pvobj = self._config_pvs_sp['MonitTagEn']
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def tbt_mask_enbl(self):
        """."""
        pvobj = self._config_pvs_rb['TbtDataMaskEn']
        return pvobj.value if pvobj.connected else None

    @tbt_mask_enbl.setter
    def tbt_mask_enbl(self, val):
        """."""
        pvobj = self._config_pvs_sp['TbtDataMaskEn']
        self._config_ok_vals['TbtDataMaskEn'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def tbt_mask_begin(self):
        """."""
        pvobj = self._config_pvs_rb['TbtDataMaskSamplesBeg']
        return pvobj.value if pvobj.connected else None

    @tbt_mask_begin.setter
    def tbt_mask_begin(self, val):
        """."""
        pvobj = self._config_pvs_sp['TbtDataMaskSamplesBeg']
        self._config_ok_vals['TbtDataMaskSamplesBeg'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def tbt_mask_end(self):
        """."""
        pvobj = self._config_pvs_rb['TbtDataMaskSamplesEnd']
        return pvobj.value if pvobj.connected else None

    @tbt_mask_end.setter
    def tbt_mask_end(self, val):
        """."""
        pvobj = self._config_pvs_sp['TbtDataMaskSamplesEnd']
        self._config_ok_vals['TbtDataMaskSamplesEnd'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def polycal(self):
        """."""
        pvobj = self._config_pvs_rb['XYPosCal']
        return pvobj.value if pvobj.connected else None

    @polycal.setter
    def polycal(self, val):
        """."""
        val = _csbpm.EnbldDsbld.enabled if val else _csbpm.EnbldDsbld.disabled
        pv1 = self._config_pvs_sp['XYPosCal']
        pv2 = self._config_pvs_sp['SUMPosCal']
        self._config_ok_vals['XYPosCal'] = val
        self._config_ok_vals['SUMPosCal'] = val
        if pv1.connected:
            pv1.put(val, wait=False)
        if pv2.connected:
            pv2.put(val, wait=False)

    @property
    def nrsamplespost(self):
        """."""
        # pvobj = self._config_pvs_rb['ACQNrSamplesPost']
        pvobj = self._config_pvs_rb['ACQSamplesPost']
        return pvobj.value if pvobj.connected else None

    @nrsamplespost.setter
    def nrsamplespost(self, val):
        """."""
        # pvobj = self._config_pvs_sp['ACQNrSamplesPost']
        pvobj = self._config_pvs_sp['ACQSamplesPost']
        # self._config_ok_vals['ACQNrSamplesPost'] = val
        self._config_ok_vals['ACQSamplesPost'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def nrsamplespre(self):
        """."""
        # pvobj = self._config_pvs_rb['ACQNrSamplesPre']
        pvobj = self._config_pvs_rb['ACQSamplesPre']
        return pvobj.value if pvobj.connected else None

    @nrsamplespre.setter
    def nrsamplespre(self, val):
        """."""
        # pvobj = self._config_pvs_sp['ACQNrSamplesPre']
        pvobj = self._config_pvs_sp['ACQSamplesPre']
        # self._config_ok_vals['ACQNrSamplesPre'] = val
        self._config_ok_vals['ACQSamplesPre'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    @property
    def nrshots(self):
        """."""
        # pvobj = self._config_pvs_rb['ACQNrShots']
        pvobj = self._config_pvs_rb['ACQShots']
        return pvobj.value if pvobj.connected else None

    @nrshots.setter
    def nrshots(self, val):
        """."""
        # pvobj = self._config_pvs_sp['ACQNrShots']
        pvobj = self._config_pvs_sp['ACQShots']
        # self._config_ok_vals['ACQNrShots'] = val
        self._config_ok_vals['ACQShots'] = val
        if pvobj.connected:
            pvobj.put(val, wait=False)

    def calc_sp_multiturn_pos(self, **kwargs):
        """."""
        nturns = kwargs.get('nturns', 1)
        refx = kwargs.get('refx', 0.0)
        refy = kwargs.get('refy', 0.0)
        refsum = kwargs.get('refsum', 0.0)
        maskbeg = kwargs.get('maskbeg', 0)
        maskend = kwargs.get('maskend', 0)
        bgd = kwargs.get('bg', dict())

        wsize = self.tbtrate
        maskbeg = min(maskbeg, wsize - 2)
        maskend = min(maskend, wsize - maskbeg - 2)
        mask = slice(maskbeg, wsize - maskend)

        # NOTE: I have to invert array B with C here because of the way
        # the ADCSWAP rate works. Fixed in 2020/07/01 after talking to
        # Daniel Tavares.
        vals = {
            'A': self.arraya, 'C': self.arrayb,
            'B': self.arrayc, 'D': self.arrayd}
        siz = None
        for key, val in vals.items():
            if val is None or val.size == 0:
                siz = 0
                break
            nzrs = val.size
            siz = nzrs if siz is None else min(siz, nzrs)
            if bgd and bgd[key].size >= val.size:
                vals[key] -= bgd[key][:val.size]

        x_cal = _np.full(nturns, refx)
        y_cal = _np.full(nturns, refy)
        s_cal = _np.full(nturns, refsum)

        # handle cases where length read is smaller than required.
        rnts = min(siz//wsize, nturns)
        if not (siz and rnts):
            return x_cal, y_cal, s_cal

        for key, val in vals.items():
            val = val[:(rnts*wsize)]
            val = val.reshape(-1, wsize)[:, mask]
            vals[key] = _np.std(val, axis=1)

        sum1, sum2 = vals['A'] + vals['C'], vals['D'] + vals['B']
        zero1 = _np.logical_not(_np.isclose(sum1, 0.0))
        zero2 = _np.logical_not(_np.isclose(sum2, 0.0))
        diff1 = (vals['A'][zero1] - vals['C'][zero1]) / sum1[zero1]
        diff2 = (vals['D'][zero2] - vals['B'][zero2]) / sum2[zero2]
        x_uncal = (diff1 + diff2) / 2
        y_uncal = (diff1 - diff2) / 2
        if self._config_ok_vals['XYPosCal'] == _csbpm.EnbldDsbld.disabled:
            x_cal[:rnts][zero1] = x_uncal * self.poskx
            y_cal[:rnts][zero2] = y_uncal * self.posky
        else:
            x_cal[:rnts][zero1], y_cal[:rnts][zero2] = self._apply_polyxy(
                x_uncal, y_uncal)
        x_cal[:rnts][zero1] *= self._orb_conv_unit
        y_cal[:rnts][zero2] *= self._orb_conv_unit
        x_cal[:rnts][zero1] -= self.offsetx or 0.0
        y_cal[:rnts][zero2] -= self.offsety or 0.0
        s_cal[:rnts] = (sum1 + sum2) * self.ksum
        return x_cal, y_cal, s_cal

    def _apply_polyxy(self, x_uncal, y_uncal):
        """."""
        x_cal = self._calc_poly(x_uncal, y_uncal, plane='x')
        y_cal = self._calc_poly(y_uncal, x_uncal, plane='y')
        return x_cal, y_cal

    def _calc_poly(self, th1, ot1, plane='x'):
        """."""
        ot2 = ot1*ot1
        ot4 = ot2*ot2
        ot6 = ot4*ot2
        ot8 = ot4*ot4
        th2 = th1*th1
        th3 = th2*th1
        th5 = th3*th2
        th7 = th5*th2
        th9 = th7*th2
        pol = self.polyx if plane == 'x' else self.polyy

        return (
            th1*(pol[0] + ot2*pol[1] + ot4*pol[2] + ot6*pol[3] + ot8*pol[4]) +
            th3*(pol[5] + ot2*pol[6] + ot4*pol[7] + ot6*pol[8]) +
            th5*(pol[9] + ot2*pol[10] + ot4*pol[11]) +
            th7*(pol[12] + ot2*pol[13]) +
            th9*pol[14])


class TimingConfig(_BaseTimingConfig):
    """."""

    def __init__(self, acc, callback=None):
        """."""
        super().__init__(acc, callback=callback)
        trig = self._csorb.trigger_acq_name
        evg = self._csorb.evg_name
        opt = {'connection_timeout': TIMEOUT}
        self._config_ok_vals = {
            'NrPulses': 1,
            'State': _cstime.Const.TrigStates.Enbl}
        if _HLTimesearch.has_delay_type(trig):
            self._config_ok_vals['RFDelayType'] = \
                                    _cstime.Const.TrigDlyTyp.Manual
        pref_name = LL_PREF + trig + ':'
        self._config_pvs_rb = {
            'Delay': _PV(pref_name + 'Delay-RB', **opt),
            'NrPulses': _PV(pref_name + 'NrPulses-RB', **opt),
            'Duration': _PV(pref_name + 'Duration-RB', **opt),
            'State': _PV(pref_name + 'State-Sts', **opt),
            'Injecting': _PV(LL_PREF + evg + ':InjectionEvt-Sts', **opt),
            'EGTrig': _PV('LI-01:EG-TriggerPS:status', **opt),
            }
        self._config_pvs_sp = {
            'NrPulses': _PV(pref_name + 'NrPulses-SP', **opt),
            'State': _PV(pref_name + 'State-Sel', **opt)}
        if _HLTimesearch.has_delay_type(trig):
            self._config_pvs_rb['RFDelayType'] = _PV(
                pref_name + 'RFDelayType-Sts', **opt)
            self._config_pvs_sp['RFDelayType'] = _PV(
                pref_name + 'RFDelayType-Sel', **opt)

    @property
    def injecting(self):
        """."""
        inj = bool(self._config_pvs_rb['Injecting'].value)
        eg_trig = bool(self._config_pvs_rb['EGTrig'].value)
        return inj and eg_trig

    @property
    def nrpulses(self):
        """."""
        pvobj = self._config_pvs_rb['NrPulses']
        return pvobj.value if pvobj.connected else None

    @nrpulses.setter
    def nrpulses(self, val):
        """."""
        pvobj = self._config_pvs_sp['NrPulses']
        if pvobj.connected:
            self._config_ok_vals['NrPulses'] = val
            pvobj.put(val, wait=False)

    @property
    def duration(self):
        """."""
        pvobj = self._config_pvs_rb['Duration']
        return pvobj.value if pvobj.connected else None

    @property
    def delay(self):
        """."""
        pvobj = self._config_pvs_rb['Delay']
        return pvobj.value if pvobj.connected else None

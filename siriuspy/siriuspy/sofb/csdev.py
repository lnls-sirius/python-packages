"""Define PVs, constants and properties of OrbitCorr SoftIOCs."""
import os as _os
from copy import deepcopy as _dcopy

from .. import csdev as _csdev
from ..namesys import SiriusPVName as _PVName
from ..search import MASearch as _MASearch, BPMSearch as _BPMSearch, \
    LLTimeSearch as _TISearch, HLTimeSearch as _HLTISearch, \
    PSSearch as _PSSearch
from ..diag.bpm.csdev import Const as _csbpm
from ..timesys import csdev as _cstiming


# --- Enumeration Types ---

class ETypes(_csdev.ETypes):
    """Local enumerate types."""

    ENBL_RF = _csdev.ETypes.OFF_ON
    ORB_MODE_RINGS = ('Offline', 'SlowOrb', 'MultiTurn', 'SinglePass')
    ORB_MODE_TLINES = ('Offline', 'SinglePass')
    SMOOTH_METH = ('Average', 'Median')
    SPASS_METHOD = ('FromBPMs', 'Calculated')
    SPASS_BG_CTRL = ('Acquire', 'Reset')
    SPASS_BG_STS = ('Empty', 'Acquiring', 'Acquired')
    SPASS_USE_BG = ('NotUsing', 'Using')
    APPLY_CORR_TLINES = ('CH', 'CV', 'All')
    APPLY_CORR_SI = ('CH', 'CV', 'RF', 'All')
    ORB_ACQ_CHAN = ('Monit1', 'FOFB', 'TbT', 'ADC', 'ADCSwp')
    MEAS_RMAT_CMD = ('Start', 'Stop', 'Reset')
    MEAS_RMAT_MON = ('Idle', 'Measuring', 'Completed', 'Aborted')
    TLINES = ('TB', 'TS')
    RINGS = ('BO', 'SI')
    ACCELERATORS = TLINES + RINGS

    STS_LBLS_CORR_TLINES = (
        'CHCVConnected', 'CHCVModeConfigured', 'CHCVPwrStateOn')
    STS_LBLS_CORR_RINGS = STS_LBLS_CORR_TLINES + (
        'TimingConnected', 'TimingConfigured')
    STS_LBLS_CORR_SI = STS_LBLS_CORR_RINGS + ('RFConnected', 'RFPwrStateOn')
    STS_LBLS_ORB = (
        'TimingConnected', 'TimingConfigured', 'BPMsConnected',
        'BPMsEnabled', 'BPMsConfigured')
    STS_LBLS_GLOB = ('Ok', 'NotOk')


_et = ETypes  # syntactic sugar


# --- Const class ---

class ConstTLines(_csdev.Const):
    """Const class defining transport lines orbitcorr constants."""

    ORBIT_CONVERSION_UNIT = 1/1000  # from nm to um
    MAX_MT_ORBS = 4000
    MAX_RINGSZ = 5
    TINY_KICK = 1e-3  # urad

    EnbldDsbld = _csdev.Const.register('EnbldDsbld', _et.DSBLD_ENBLD)
    TrigAcqCtrl = _csbpm.AcqEvents
    TrigAcqChan = _csdev.Const.register('TrigAcqChan', _et.ORB_ACQ_CHAN)
    TrigAcqDataChan = _csbpm.AcqChan
    TrigAcqDataSel = _csbpm.AcqDataTyp
    TrigAcqDataPol = _csbpm.Polarity
    TrigAcqRepeat = _csbpm.AcqRepeat
    TrigAcqTrig = _csdev.Const.register('TrigAcqTrig', ('External', 'Data'))
    SmoothMeth = _csdev.Const.register('SmoothMeth', _et.SMOOTH_METH)
    SPassBgCtrl = _csdev.Const.register('SPassBgCtrl', _et.SPASS_BG_CTRL)
    SPassBgSts = _csdev.Const.register('SPassBgSts', _et.SPASS_BG_STS)
    SPassUseBg = _csdev.Const.register('SPassUseBg', _et.SPASS_USE_BG)
    MeasRespMatCmd = _csdev.Const.register('MeasRespMatCmd', _et.MEAS_RMAT_CMD)
    MeasRespMatMon = _csdev.Const.register('MeasRespMatMon', _et.MEAS_RMAT_MON)
    TransportLines = _csdev.Const.register(
        'TransportLines', _et.TLINES, (0, 1))
    Rings = _csdev.Const.register('Rings', _et.RINGS, (2, 3))
    Accelerators = _csdev.Const.register('Accelerators', _et.ACCELERATORS)

    SOFBMode = _csdev.Const.register('SOFBMode', _et.ORB_MODE_TLINES)
    SyncWithInj = _csdev.Const.register('SyncWithInj', _et.OFF_ON)
    ApplyDelta = _csdev.Const.register('ApplyDelta', _et.APPLY_CORR_TLINES)
    StsLblsCorr = _csdev.Const.register(
        'StsLblsCorr', _et.STS_LBLS_CORR_TLINES)
    StsLblsOrb = _csdev.Const.register('StsLblsOrb', _et.STS_LBLS_ORB)
    StsLblsGlob = _csdev.Const.register('StsLblsGlob', _et.STS_LBLS_GLOB)

    ClosedLoop = _csdev.Const.register('ClosedLoop', _et.OFF_ON)


class ConstRings(ConstTLines):
    """Const class defining rings orbitcorr constants."""

    SOFBMode = _csdev.Const.register('SOFBMode', _et.ORB_MODE_RINGS)
    StsLblsCorr = _csdev.Const.register('StsLblsCorr', _et.STS_LBLS_CORR_RINGS)


class ConstSI(ConstRings):
    """Const class defining rings orbitcorr constants."""

    ApplyDelta = _csdev.Const.register('ApplyDelta', _et.APPLY_CORR_SI)
    StsLblsCorr = _csdev.Const.register('StsLblsCorr', _et.STS_LBLS_CORR_SI)
    CorrSync = _csdev.Const.register('CorrSync', _et.OFF_ON)

    RF_GEN_NAME = 'RF-Gen'
    EnblRF = _csdev.Const.register('EnblRF', _et.ENBL_RF)


# --- Database classes ---

class SOFBTLines(ConstTLines):
    """SOFB class for TLines."""

    def __init__(self, acc):
        """Init1 method."""
        self.acc = acc.upper()
        self.evg_name = _TISearch.get_evg_name()
        self.acc_idx = self.Accelerators._fields.index(self.acc)
        # Define the BPMs and correctors:
        self.bpm_names = _BPMSearch.get_names({'sec': acc})
        self.ch_names = _PSSearch.get_psnames(
            {'sec': acc, 'dis': 'PS', 'dev': 'CH'})
        self.cv_names = _PSSearch.get_psnames(
            {'sec': acc, 'dis': 'PS', 'dev': 'CV'})
        if self.acc == 'TS':
            self.ch_names = [_PVName('TS-01:PU-EjeSeptG'), ] + self.ch_names
        elif self.acc == 'SI':
            id_cors = ('SA', 'SB', 'SP')
            self.ch_names = list(filter(
                lambda x: not x.sub.endswith(id_cors), self.ch_names))
            self.cv_names = list(filter(
                lambda x: not x.sub.endswith(id_cors), self.cv_names))
        # Give them a nickname:
        self.bpm_nicknames = _BPMSearch.get_nicknames(self.bpm_names)
        self.ch_nicknames = _PSSearch.get_psnicknames(self.ch_names)
        self.cv_nicknames = _PSSearch.get_psnicknames(self.cv_names)
        if self.acc == 'TS':
            self.ch_nicknames[0] = 'EjeseptG'
        # Find their position along the ring:
        self.bpm_pos = _BPMSearch.get_positions(self.bpm_names)
        self.ch_pos = _MASearch.get_mapositions(map(
            lambda x: x.substitute(dis='MA' if x.dis == 'PS' else 'PM'),
            self.ch_names))
        self.cv_pos = _MASearch.get_mapositions(map(
            lambda x: x.substitute(dis='MA' if x.dis == 'PS' else 'PM'),
            self.cv_names))
        # Find the total number of BPMs and correctors:
        self.nr_bpms = len(self.bpm_names)
        self.nr_ch = len(self.ch_names)
        self.nr_cv = len(self.cv_names)
        self.nr_chcv = self.nr_ch + self.nr_cv
        self.nr_corrs = self.nr_chcv + 1 if acc == 'SI' else self.nr_chcv

        ext = acc.lower() + 'orb'
        ioc_fol = acc.lower() + '-ap-sofb'
        ioc_fol = _os.path.join('/home', 'sirius', 'iocs-log', ioc_fol, 'data')
        self.ref_orb_fname = _os.path.join(ioc_fol, 'ref_orbit.'+ext)
        ext = acc.lower() + 'respmat'
        self.respmat_fname = _os.path.join(ioc_fol, 'respmat.'+ext)

        self.trigger_acq_name = self.acc + '-Fam:TI-BPM'
        if self.acc == 'SI':
            self.trigger_cor_name = self.acc + '-Glob:TI-Mags-Corrs'
            self.evt_cor_name = 'Orb' + self.acc

        self.evt_acq_name = 'Dig' + self.acc
        self.matrix_size = self.nr_corrs * (2 * self.nr_bpms)
        self.nr_svals = min(self.nr_corrs, 2 * self.nr_bpms)
        self.circum = 21.2477 if self.acc == 'TB' else 26.8933  # in meters
        self.rev_per = self.circum / 299792458  # in seconds

    @property
    def isring(self):
        """."""
        return self.acc in self.Rings._fields

    def get_ioc_database(self, prefix=''):
        """Return IOC database."""
        dbase = self.get_sofb_database(prefix)
        dbase.update(self.get_corrs_database(prefix))
        dbase.update(self.get_respmat_database(prefix))
        dbase.update(self.get_orbit_database(prefix))
        dbase = _csdev.add_pvslist_cte(dbase)
        return dbase

    def get_sofb_database(self, prefix=''):
        """Return OpticsCorr-Chrom Soft IOC database."""
        dbase = {
            'Log-Mon': {'type': 'char', 'value': '', 'count': 200},
            'ClosedLoop-Sel': {
                'type': 'enum', 'enums': self.ClosedLoop._fields, 'value': 0},
            'ClosedLoop-Sts': {
                'type': 'enum', 'enums': self.ClosedLoop._fields, 'value': 0},
            'ClosedLoopFreq-SP': {
                'type': 'float', 'value': 1, 'unit': 'Hz', 'prec': 3,
                'lolim': 1e-3, 'hilim': 20},
            'ClosedLoopFreq-RB': {
                'type': 'float', 'value': 1, 'prec': 2, 'unit': 'Hz'},
            'MeasRespMat-Cmd': {
                'type': 'enum', 'value': 0,
                'enums': self.MeasRespMatCmd._fields},
            'MeasRespMat-Mon': {
                'type': 'enum', 'value': 0,
                'enums': self.MeasRespMatMon._fields},
            'MeasRespMatKickCH-SP': {
                'type': 'float', 'value': 80, 'unit': 'urad', 'prec': 3,
                'lolim': 0.002, 'hilim': 500},
            'MeasRespMatKickCH-RB': {
                'type': 'float', 'value': 80, 'unit': 'urad', 'prec': 3,
                'lolim': 0.002, 'hilim': 500},
            'MeasRespMatKickCV-SP': {
                'type': 'float', 'value': 80, 'unit': 'urad', 'prec': 3,
                'lolim': 0.002, 'hilim': 500},
            'MeasRespMatKickCV-RB': {
                'type': 'float', 'value': 80, 'unit': 'urad', 'prec': 3,
                'lolim': 0.002, 'hilim': 500},
            'MeasRespMatWait-SP': {
                'type': 'float', 'value': 1, 'unit': 's', 'prec': 3,
                'lolim': 0.005, 'hilim': 100},
            'MeasRespMatWait-RB': {
                'type': 'float', 'value': 1, 'unit': 's', 'prec': 3,
                'lolim': 0.005, 'hilim': 100},
            'CalcDelta-Cmd': {
                'type': 'int', 'value': 0, 'unit': 'Calculate kicks'},
            'DeltaFactorCH-SP': {
                'type': 'float', 'value': 100, 'unit': '%', 'prec': 2,
                'lolim': -10000, 'hilim': 10000},
            'DeltaFactorCH-RB': {
                'type': 'float', 'value': 100, 'prec': 2, 'unit': '%'},
            'DeltaFactorCV-SP': {
                'type': 'float', 'value': 100, 'unit': '%', 'prec': 2,
                'lolim': -10000, 'hilim': 10000},
            'DeltaFactorCV-RB': {
                'type': 'float', 'value': 100, 'prec': 2, 'unit': '%'},
            'MaxKickCH-SP': {
                'type': 'float', 'value': 300, 'unit': 'urad', 'prec': 3,
                'lolim': 0, 'hilim': 500000},
            'MaxKickCH-RB': {
                'type': 'float', 'value': 300, 'prec': 3, 'unit': 'urad',
                'lolim': 0, 'hilim': 500000},
            'MaxKickCV-SP': {
                'type': 'float', 'value': 300, 'unit': 'urad', 'prec': 3,
                'lolim': 0, 'hilim': 10000},
            'MaxKickCV-RB': {
                'type': 'float', 'value': 300, 'prec': 3, 'unit': 'urad',
                'lolim': 0, 'hilim': 10000},
            'MaxDeltaKickCH-SP': {
                'type': 'float', 'value': 300, 'unit': 'urad', 'prec': 3,
                'lolim': 0, 'hilim': 10000},
            'MaxDeltaKickCH-RB': {
                'type': 'float', 'value': 300, 'prec': 3, 'unit': 'urad',
                'lolim': 0, 'hilim': 10000},
            'MaxDeltaKickCV-SP': {
                'type': 'float', 'value': 300, 'unit': 'urad', 'prec': 3,
                'lolim': 0, 'hilim': 10000},
            'MaxDeltaKickCV-RB': {
                'type': 'float', 'value': 300, 'prec': 3, 'unit': 'urad',
                'lolim': 0, 'hilim': 10000},
            'DeltaKickCH-SP': {
                'type': 'float', 'count': self.nr_ch, 'value': self.nr_ch*[0],
                'unit': 'urad'},
            'DeltaKickCH-RB': {
                'type': 'float', 'count': self.nr_ch, 'value': self.nr_ch*[0],
                'unit': 'urad'},
            'DeltaKickCV-SP': {
                'type': 'float', 'count': self.nr_cv, 'value': self.nr_cv*[0],
                'unit': 'urad'},
            'DeltaKickCV-RB': {
                'type': 'float', 'count': self.nr_cv, 'value': self.nr_cv*[0],
                'unit': 'urad'},
            'ApplyDelta-Cmd': {
                'type': 'enum', 'enums': self.ApplyDelta._fields, 'value': 0,
                'unit': 'Apply last calculated kicks.'},
            'Status-Mon': {
                'type': 'enum', 'value': 1,
                'enums': self.StsLblsGlob._fields}
            }
        return self._add_prefix(dbase, prefix)

    def get_corrs_database(self, prefix=''):
        """Return OpticsCorr-Chrom Soft IOC database."""
        dbase = {
            'KickAcqRate-SP': {
                'type': 'float', 'unit': 'Hz', 'value': 2,
                'hilim': 20, 'lolim': 0.01, 'prec': 2},
            'KickAcqRate-RB': {
                'type': 'float', 'unit': 'Hz', 'value': 2,
                'hilim': 20, 'lolim': 0.01, 'prec': 2},
            'KickCH-Mon': {
                'type': 'float', 'count': self.nr_ch, 'value': self.nr_ch*[0],
                'unit': 'urad'},
            'KickCV-Mon': {
                'type': 'float', 'count': self.nr_cv, 'value': self.nr_cv*[0],
                'unit': 'urad'},
            'CorrConfig-Cmd': {'type': 'int', 'value': 0},
            'CHPosS-Cte': {
                'type': 'float', 'unit': 'm', 'count': self.nr_ch,
                'value': self.ch_pos},
            'CVPosS-Cte': {
                'type': 'float', 'unit': 'm', 'count': self.nr_cv,
                'value': self.cv_pos},
            'CHNickName-Cte': {
                'type': 'string', 'unit': 'shortname for the chs.',
                'count': self.nr_ch, 'value': self.ch_nicknames},
            'CVNickName-Cte': {
                'type': 'string', 'unit': 'shortname for the cvs.',
                'count': self.nr_cv, 'value': self.cv_nicknames},
            'CorrStatus-Mon': {'type': 'int', 'value': 0b1111111},
            'CorrStatusLabels-Cte': {
                'type': 'string', 'count': len(self.StsLblsCorr._fields),
                'value': self.StsLblsCorr._fields}
            }
        return self._add_prefix(dbase, prefix)

    def get_orbit_database(self, prefix=''):
        """Return Orbit database."""
        nbpm = self.nr_bpms
        pvs = [
            'RefOrbX-SP', 'RefOrbX-RB',
            'RefOrbY-SP', 'RefOrbY-RB',
            'SPassOrbX-Mon', 'SPassOrbY-Mon',
            'SPassSum-Mon',
            'OfflineOrbX-SP', 'OfflineOrbX-RB',
            'OfflineOrbY-SP', 'OfflineOrbY-RB',
            'BPMOffsetX-Mon', 'BPMOffsetY-Mon',
            ]
        dbase = dict()
        prop = {
            'type': 'float', 'unit': 'um', 'count': self.MAX_RINGSZ*nbpm,
            'value': nbpm*[0]}
        for k in pvs:
            dbase[k] = _dcopy(prop)
        dbase.update({
            'SOFBMode-Sel': {
                'type': 'enum', 'unit': 'Change orbit acquisition mode.',
                'value': self.SOFBMode.Offline,
                'enums': self.SOFBMode._fields},
            'SOFBMode-Sts': {
                'type': 'enum', 'unit': 'Change orbit acquisition mode.',
                'value': self.SOFBMode.Offline,
                'enums': self.SOFBMode._fields},
            'SyncWithInjection-Sel': {
                'type': 'enum', 'unit': 'Sync orbit acq. with injection',
                'value': self.SyncWithInj.Off,
                'enums': self.SyncWithInj._fields},
            'SyncWithInjection-Sts': {
                'type': 'enum', 'unit': 'Sync orbit acq. with injection',
                'value': self.SyncWithInj.Off,
                'enums': self.SyncWithInj._fields},
            'TrigAcqConfig-Cmd': {'type': 'int', 'value': 0},
            'TrigAcqCtrl-Sel': {
                'type': 'enum', 'unit': 'Start/Stop/Abort acquistion.',
                'value': self.TrigAcqCtrl.Stop,
                'enums': self.TrigAcqCtrl._fields},
            'TrigAcqCtrl-Sts': {
                'type': 'enum', 'unit': 'Start/Stop/Reset acquistion.',
                'value': self.TrigAcqCtrl.Stop,
                'enums': self.TrigAcqCtrl._fields},
            'TrigAcqChan-Sel': {
                'type': 'enum', 'unit': 'Change orbit acquisition Channel.',
                'value': self.TrigAcqChan.ADC,
                'enums': self.TrigAcqChan._fields},
            'TrigAcqChan-Sts': {
                'type': 'enum', 'unit': 'Change orbit acquisition Channel.',
                'value': self.TrigAcqChan.ADC,
                'enums': self.TrigAcqChan._fields},
            'TrigDataChan-Sel': {
                'type': 'enum', 'unit': 'Set Data-driven trigger Channel.',
                'value': self.TrigAcqDataChan.ADC,
                'enums': self.TrigAcqDataChan._fields},
            'TrigDataChan-Sts': {
                'type': 'enum', 'unit': 'Set Data-driven trigger Channel.',
                'value': self.TrigAcqDataChan.ADC,
                'enums': self.TrigAcqDataChan._fields},
            'TrigAcqTrigger-Sel': {
                'type': 'enum', 'unit': 'If trigger is external or by data.',
                'value': self.TrigAcqTrig.External,
                'enums': self.TrigAcqTrig._fields},
            'TrigAcqTrigger-Sts': {
                'type': 'enum', 'unit': 'If trigger is external or by data.',
                'value': self.TrigAcqTrig.External,
                'enums': self.TrigAcqTrig._fields},
            'TrigAcqRepeat-Sel': {
                'type': 'enum', 'unit': 'Auto arm to repeat acquisition.',
                'value': self.TrigAcqRepeat.Normal,
                'enums': self.TrigAcqRepeat._fields},
            'TrigAcqRepeat-Sts': {
                'type': 'enum', 'unit': 'Auto arm to repeat acquisition.',
                'value': self.TrigAcqRepeat.Normal,
                'enums': self.TrigAcqRepeat._fields},
            'TrigNrShots-SP': {
                'type': 'int', 'unit': '', 'value': 1,
                'hilim': 1000, 'lolim': 1},
            'TrigNrShots-RB': {
                'type': 'int', 'unit': '', 'value': 1,
                'hilim': 1000, 'lolim': 1},
            'TrigNrSamplesPre-SP': {
                'type': 'int', 'unit': '', 'value': 0,
                'hilim': 20000, 'lolim': -1},
            'TrigNrSamplesPre-RB': {
                'type': 'int', 'unit': '', 'value': 0,
                'hilim': 20000, 'lolim': -1},
            'TrigNrSamplesPost-SP': {
                'type': 'int', 'unit': '', 'value': 360,
                'hilim': 20000, 'lolim': 0},
            'TrigNrSamplesPost-RB': {
                'type': 'int', 'unit': '', 'value': 360,
                'hilim': 20000, 'lolim': 0},
            'TrigDataSel-Sel': {
                'type': 'enum', 'unit': 'Set Data trigger Selection.',
                'value': self.TrigAcqDataSel.A,
                'enums': self.TrigAcqDataSel._fields},
            'TrigDataSel-Sts': {
                'type': 'enum', 'unit': 'Set Data trigger Selection.',
                'value': self.TrigAcqDataSel.A,
                'enums': self.TrigAcqDataSel._fields},
            'TrigDataThres-SP': {
                'type': 'int', 'value': 1,
                'unit': 'set data trigger threshold',
                'lolim': -1000, 'hilim': 2**31-1},
            'TrigDataThres-RB': {
                'type': 'int', 'value': 1,
                'unit': 'set data trigger threshold',
                'lolim': -1000, 'hilim': 2**31-1},
            'TrigDataHyst-SP': {
                'type': 'int', 'value': 0,
                'unit': 'set data trigger hysteresis',
                'lolim': 0, 'hilim': 2**31-1},
            'TrigDataHyst-RB': {
                'type': 'int', 'value': 0,
                'unit': 'set data trigger hysteresis',
                'lolim': 0, 'hilim': 2**31-1},
            'TrigDataPol-Sel': {
                'type': 'enum', 'unit': 'Set Data trigger Polarity.',
                'value': self.TrigAcqDataPol.Positive,
                'enums': self.TrigAcqDataPol._fields},
            'TrigDataPol-Sts': {
                'type': 'enum', 'unit': 'Set Data trigger Polarity.',
                'value': self.TrigAcqDataPol.Positive,
                'enums': self.TrigAcqDataPol._fields},
            'PolyCalibration-Sel': {
                'type': 'enum', 'value': self.EnbldDsbld.Dsbld,
                'enums': self.EnbldDsbld._fields},
            'PolyCalibration-Sts': {
                'type': 'enum', 'value': self.EnbldDsbld.Dsbld,
                'enums': self.EnbldDsbld._fields},
            'OrbAcqRate-SP': {
                'type': 'float', 'unit': 'Hz', 'value': 10,
                'hilim': 20, 'lolim': 0.01, 'prec': 2},
            'OrbAcqRate-RB': {
                'type': 'float', 'unit': 'Hz', 'value': 10,
                'hilim': 20, 'lolim': 0.01, 'prec': 2},
            'SmoothNrPts-SP': {
                'type': 'int', 'value': 1,
                'unit': 'number of points for smoothing',
                'lolim': 1, 'hilim': 500},
            'SmoothNrPts-RB': {
                'type': 'int', 'value': 1,
                'unit': 'number of points for smoothing',
                'lolim': 1, 'hilim': 500},
            'SmoothMethod-Sel': {
                'type': 'enum', 'value': self.SmoothMeth.Average,
                'enums': _et.SMOOTH_METH},
            'SmoothMethod-Sts': {
                'type': 'enum', 'value': self.SmoothMeth.Average,
                'enums': _et.SMOOTH_METH},
            'SmoothReset-Cmd': {
                'type': 'int', 'value': 0, 'unit': 'Reset orbit buffer'},
            'BufferCount-Mon': {
                'type': 'int', 'value': 0, 'unit': 'Current buffer size'},
            'SPassMaskSplBeg-SP': {
                'type': 'int', 'value': 0, 'lolim': -1, 'hilim': 1000},
            'SPassMaskSplBeg-RB': {
                'type': 'int', 'value': 0, 'lolim': -1, 'hilim': 1000},
            'SPassMaskSplEnd-SP': {
                'type': 'int', 'value': 0, 'lolim': -1, 'hilim': 1000},
            'SPassMaskSplEnd-RB': {
                'type': 'int', 'value': 0, 'lolim': -1, 'hilim': 1000},
            'SPassAvgNrTurns-SP': {
                'type': 'int', 'value': 1, 'lolim': 1, 'hilim': 1000},
            'SPassAvgNrTurns-RB': {
                'type': 'int', 'value': 1, 'lolim': 1, 'hilim': 1000},
            'SPassBgCtrl-Cmd': {
                'type': 'enum', 'value': self.SPassBgCtrl.Acquire,
                'enums': self.SPassBgCtrl._fields},
            'SPassBgSts-Mon': {
                'type': 'enum', 'value': self.SPassBgSts.Empty,
                'enums': self.SPassBgSts._fields},
            'SPassUseBg-Sel': {
                'type': 'enum', 'value': self.SPassUseBg.NotUsing,
                'enums': self.SPassUseBg._fields},
            'SPassUseBg-Sts': {
                'type': 'enum', 'value': self.SPassUseBg.NotUsing,
                'enums': self.SPassUseBg._fields},
            'BPMPosS-Mon': {
                'type': 'float', 'unit': 'm', 'count': self.MAX_RINGSZ*nbpm,
                'value': self.bpm_pos, 'prec': 2},
            'BPMNickName-Cte': {
                'type': 'string', 'unit': 'shortname for the bpms.',
                'count': self.MAX_RINGSZ*nbpm, 'value': self.bpm_nicknames},
            'OrbStatus-Mon': {'type': 'int', 'value': 0b00000},
            'OrbStatusLabels-Cte': {
                'type': 'string', 'count': len(self.StsLblsOrb._fields),
                'value': self.StsLblsOrb._fields},
            })
        return self._add_prefix(dbase, prefix)

    def get_respmat_database(self, prefix=''):
        """Return OpticsCorr-Chrom Soft IOC database."""
        dbase = {
            'RespMat-SP': {
                'type': 'float', 'count': self.MAX_RINGSZ*self.matrix_size,
                'value': self.matrix_size*[0],
                'unit': '(BH, BV)(um) x (CH, CV, RF)(urad, Hz)'},
            'RespMat-RB': {
                'type': 'float', 'count': self.MAX_RINGSZ*self.matrix_size,
                'value': self.matrix_size*[0],
                'unit': '(BH, BV)(um) x (CH, CV, RF)(urad, Hz)'},
            'SingValues-Mon': {
                'type': 'float', 'count': self.nr_svals,
                'value': self.nr_svals*[0],
                'unit': 'Singular values of the matrix in use'},
            'InvRespMat-Mon': {
                'type': 'float', 'count': self.MAX_RINGSZ*self.matrix_size,
                'value': self.matrix_size*[0],
                'unit': '(CH, CV, RF)(urad, Hz) x (BH, BV)(um)'},
            'CHEnblList-SP': {
                'type': 'int', 'count': self.nr_ch, 'value': self.nr_ch*[1],
                'unit': 'CHs used in correction'},
            'CHEnblList-RB': {
                'type': 'int', 'count': self.nr_ch, 'value': self.nr_ch*[1],
                'unit': 'CHs used in correction'},
            'CVEnblList-SP': {
                'type': 'int', 'count': self.nr_cv, 'value': self.nr_cv*[1],
                'unit': 'CVs used in correction'},
            'CVEnblList-RB': {
                'type': 'int', 'count': self.nr_cv, 'value': self.nr_cv*[1],
                'unit': 'CVs used in correction'},
            'BPMXEnblList-SP': {
                'type': 'int', 'count': self.MAX_RINGSZ*self.nr_bpms,
                'value': self.nr_bpms*[1],
                'unit': 'BPMX used in correction'},
            'BPMXEnblList-RB': {
                'type': 'int', 'count': self.MAX_RINGSZ*self.nr_bpms,
                'value': self.nr_bpms*[1],
                'unit': 'BPMX used in correction'},
            'BPMYEnblList-SP': {
                'type': 'int', 'count': self.MAX_RINGSZ*self.nr_bpms,
                'value': self.nr_bpms*[1],
                'unit': 'BPMY used in correction'},
            'BPMYEnblList-RB': {
                'type': 'int', 'count': self.MAX_RINGSZ*self.nr_bpms,
                'value': self.nr_bpms*[1],
                'unit': 'BPMY used in correction'},
            'NrSingValues-SP': {
                'type': 'int', 'value': self.nr_svals,
                'lolim': 1, 'hilim': self.nr_svals,
                'unit': 'Maximum number of SV to use'},
            'NrSingValues-RB': {
                'type': 'int', 'value': self.nr_svals,
                'lolim': 1, 'hilim': self.nr_svals,
                'unit': 'Maximum number of SV to use'},
            'DeltaKickCH-Mon': {
                'type': 'float', 'count': self.nr_ch, 'value': self.nr_ch*[0],
                'unit': 'urad'},
            'DeltaKickCV-Mon': {
                'type': 'float', 'count': self.nr_cv, 'value': self.nr_cv*[0],
                'unit': 'urad'},
            }
        return self._add_prefix(dbase, prefix)

    def _add_prefix(self, dbase, prefix):
        if prefix:
            return {prefix + k: v for k, v in dbase.items()}
        return dbase


class SOFBRings(SOFBTLines, ConstRings):
    """SOFB class."""

    def __init__(self, acc):
        """Init method."""
        SOFBTLines.__init__(self, acc)
        self.circum = 496.8  # in meter
        self.rev_per = self.circum / 299792458  # in seconds

    def get_sofb_database(self, prefix=''):
        """Return OpticsCorr-Chrom Soft IOC database."""
        db_ring = {
            'RingSize-SP': {
                'type': 'int', 'value': 1, 'lolim': 0,
                'hilim': self.MAX_RINGSZ+1,
                'unit': 'Nr Times to extend the ring'},
            'RingSize-RB': {
                'type': 'int', 'value': 1, 'lolim': 0,
                'hilim': self.MAX_RINGSZ+1,
                'unit': 'Nr Times to extend the ring'},
            }
        dbase = super().get_sofb_database(prefix=prefix)
        dbase.update(self._add_prefix(db_ring, prefix))
        return dbase

    def get_orbit_database(self, prefix=''):
        """Return Orbit database."""
        nbpm = self.nr_bpms
        pvs_ring = [
            'SlowOrbX-Mon', 'SlowOrbY-Mon',
            'MTurnIdxOrbX-Mon', 'MTurnIdxOrbY-Mon',
            'MTurnIdxSum-Mon',
            ]
        db_ring = dict()
        prop = {
            'type': 'float', 'unit': 'um', 'count': self.MAX_RINGSZ*nbpm,
            'value': nbpm*[0]}
        for k in pvs_ring:
            db_ring[k] = _dcopy(prop)
        db_ring.update({
            'MTurnSyncTim-Sel': {
                'type': 'enum', 'value': self.EnbldDsbld.Enbld,
                'enums': self.EnbldDsbld._fields},
            'MTurnSyncTim-Sts': {
                'type': 'enum', 'value': self.EnbldDsbld.Enbld,
                'enums': self.EnbldDsbld._fields},
            'MTurnUseMask-Sel': {
                'type': 'enum', 'value': self.EnbldDsbld.Dsbld,
                'enums': self.EnbldDsbld._fields},
            'MTurnUseMask-Sts': {
                'type': 'enum', 'value': self.EnbldDsbld.Dsbld,
                'enums': self.EnbldDsbld._fields},
            'MTurnMaskSplBeg-SP': {
                'type': 'int', 'value': 0, 'lolim': -1, 'hilim': 1000},
            'MTurnMaskSplBeg-RB': {
                'type': 'int', 'value': 0, 'lolim': -1, 'hilim': 1000},
            'MTurnMaskSplEnd-SP': {
                'type': 'int', 'value': 0, 'lolim': -1, 'hilim': 1000},
            'MTurnMaskSplEnd-RB': {
                'type': 'int', 'value': 0, 'lolim': -1, 'hilim': 1000},
            'MTurnDownSample-SP': {
                'type': 'int', 'unit': '', 'value': 1,
                'hilim': 20000, 'lolim': 1},
            'MTurnDownSample-RB': {
                'type': 'int', 'unit': '', 'value': 1,
                'hilim': 20000, 'lolim': 1},
            'MTurnOrbX-Mon': {
                'type': 'float', 'unit': 'um', 'count': self.MAX_MT_ORBS*nbpm,
                'value': 50*nbpm*[0]},
            'MTurnOrbY-Mon': {
                'type': 'float', 'unit': 'um', 'count': self.MAX_MT_ORBS*nbpm,
                'value': 50*nbpm*[0]},
            'MTurnSum-Mon': {
                'type': 'float', 'unit': 'count',
                'count': self.MAX_MT_ORBS*nbpm,
                'value': 50*nbpm*[0]},
            'MTurnTime-Mon': {
                'type': 'float', 'unit': 's', 'count': self.MAX_MT_ORBS,
                'value': 50*[0]},
            'MTurnIdx-SP': {
                'type': 'int', 'unit': '', 'value': 0,
                'hilim': self.MAX_MT_ORBS, 'lolim': 0},
            'MTurnIdx-RB': {
                'type': 'int', 'unit': '', 'value': 0,
                'hilim': self.MAX_MT_ORBS, 'lolim': 0},
            'MTurnIdxTime-Mon': {
                'type': 'float', 'unit': 's', 'value': 0.0, 'prec': 5,
                'hilim': 500, 'lolim': 0},
            })
        dbase = super().get_orbit_database(prefix=prefix)
        dbase.update(self._add_prefix(db_ring, prefix))
        return dbase


class SOFBSI(SOFBRings, ConstSI):
    """SOFB class."""

    def __init__(self, acc):
        """Init method."""
        SOFBRings.__init__(self, acc)
        evts = _HLTISearch.get_hl_trigger_allowed_evts(self.trigger_cor_name)
        vals = _cstiming.get_hl_trigger_database(self.trigger_cor_name)
        vals = tuple([vals['Src-Sel']['enums'].index(evt) for evt in evts])
        self.CorrExtEvtSrc = self.register('CorrExtEvtSrc', evts, vals)
        self.circum = 518.396  # in meter
        self.rev_per = self.circum / 299792458  # in seconds

    def get_sofb_database(self, prefix=''):
        """Return OpticsCorr-Chrom Soft IOC database."""
        db_ring = {
            'MeasRespMatKickRF-SP': {
                'type': 'float', 'value': 50, 'unit': 'Hz', 'prec': 2,
                'lolim': 1, 'hilim': 1000},
            'MeasRespMatKickRF-RB': {
                'type': 'float', 'value': 50, 'unit': 'Hz', 'prec': 2,
                'lolim': 1, 'hilim': 1000},
            'DeltaFactorRF-SP': {
                'type': 'float', 'value': 100, 'unit': '%', 'prec': 2,
                'lolim': -1000, 'hilim': 1000},
            'DeltaFactorRF-RB': {
                'type': 'float', 'value': 100, 'prec': 2, 'unit': '%'},
            'MaxKickRF-SP': {
                'type': 'float', 'value': 499663000, 'unit': 'Hz', 'prec': 2,
                'lolim': 499660000, 'hilim': 499665000},
            'MaxKickRF-RB': {
                'type': 'float', 'value': 499663000, 'unit': 'Hz', 'prec': 2,
                'lolim': 499660000, 'hilim': 499665000},
            'MaxDeltaKickRF-SP': {
                'type': 'float', 'value': 500, 'unit': 'Hz', 'prec': 2,
                'lolim': 0, 'hilim': 10000},
            'MaxDeltaKickRF-RB': {
                'type': 'float', 'value': 500, 'prec': 2, 'unit': 'Hz',
                'lolim': 0, 'hilim': 10000},
            'DeltaKickRF-SP': {
                'type': 'float', 'value': 0, 'prec': 2, 'unit': 'Hz'},
            'DeltaKickRF-RB': {
                'type': 'float', 'value': 0, 'prec': 2, 'unit': 'Hz'},
            }
        dbase = super().get_sofb_database(prefix=prefix)
        dbase.update(self._add_prefix(db_ring, prefix))
        return dbase

    def get_corrs_database(self, prefix=''):
        """Return OpticsCorr-Chrom Soft IOC database."""
        db_ring = {
            'CorrSync-Sel': {
                'type': 'enum', 'enums': self.CorrSync._fields,
                'value': self.CorrSync.Off},
            'CorrSync-Sts': {
                'type': 'enum', 'enums': self.CorrSync._fields,
                'value': self.CorrSync.Off},
            'KickRF-Mon': {
                'type': 'float', 'value': 1, 'unit': 'Hz', 'prec': 2},
            }
        dbase = super().get_corrs_database(prefix=prefix)
        dbase.update(self._add_prefix(db_ring, prefix))
        return dbase

    def get_respmat_database(self, prefix=''):
        """Return OpticsCorr-Chrom Soft IOC database."""
        db_ring = {
            'RFEnbl-Sel': {
                'type': 'enum', 'enums': self.EnblRF._fields, 'value': 0,
                'unit': 'If RF is used in correction'},
            'RFEnbl-Sts': {
                'type': 'enum', 'enums': self.EnblRF._fields, 'value': 0,
                'unit': 'If RF is used in correction'},
            'DeltaKickRF-Mon': {
                'type': 'float', 'value': 0, 'prec': 2, 'unit': 'Hz'},
            }
        dbase = super().get_respmat_database(prefix=prefix)
        dbase.update(self._add_prefix(db_ring, prefix))
        return dbase


class SOFBFactory:
    """Factory class for SOFB objects."""

    @staticmethod
    def create(acc):
        """Return appropriate SOFB object."""
        acc = acc.upper()
        if acc == 'SI':
            return SOFBSI(acc)
        elif acc in _et.RINGS:
            return SOFBRings(acc)
        elif acc in _et.TLINES:
            return SOFBTLines(acc)
        else:
            raise ValueError('Invalid accelerator name "{}"'.format(acc))

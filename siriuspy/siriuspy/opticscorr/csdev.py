"""Define PVs, constants and properties of OpticsCorr SoftIOCs."""
from .. import csdev as _csdev


# --- Enumeration Types ---

class ETypes(_csdev.ETypes):
    """Local enumerate types."""

    PROP_ADD = ('Proportional', 'Additional')
    INDIV_2KNOBS = ('Individual', 'TwoKnobs')
    MEAS_CMD = ('Reset', 'Start', 'Stop')
    MEAS_MON = ('Idle', 'Measuring', 'Completed', 'Aborted')


_et = ETypes  # syntactic sugar


# --- Const class ---

class Const(_csdev.Const):
    """Const class defining OpticsCorr constants and Enum types."""

    CorrMeth = _csdev.Const.register('CorrMeth', _et.PROP_ADD)
    CorrGroup = _csdev.Const.register('CorrGroup', _et.INDIV_2KNOBS)
    SyncCorr = _csdev.Const.register('SyncCorr', _et.OFF_ON)
    MeasCmd = _csdev.Const.register('MeasCmd', _et.MEAS_CMD)
    MeasMon = _csdev.Const.register('MeasMon', _et.MEAS_MON)

    BO_SFAMS_CHROMCORR = ('SF', 'SD')
    BO_SFAMS_NELM = (25, 10)

    SI_SFAMS_CHROMCORR = ('SFA1', 'SFA2', 'SDA1', 'SDA2', 'SDA3',
                          'SFB1', 'SFB2', 'SDB1', 'SDB2', 'SDB3',
                          'SFP1', 'SFP2', 'SDP1', 'SDP2', 'SDP3')
    SI_SFAMS_NELM = (10, 10, 10, 10, 10,
                     20, 20, 20, 20, 20,
                     10, 10, 10, 10, 10)

    BO_QFAMS_TUNECORR = ('QF', 'QD')
    BO_QFAMS_NELM = (50, 25)

    SI_QFAMS_TUNECORR = ('QFA', 'QFB', 'QFP',
                         'QDA', 'QDB1', 'QDB2', 'QDP1', 'QDP2')
    SI_QFAMS_NELM = (10, 20, 10,
                     10, 20, 20, 10, 10)

    STATUS_LABELS = ('PS Connection', 'PS PwrState', 'PS OpMode',
                     'PS CtrlMode', 'Timing Config')


_ct = Const  # syntactic sugar


# --- Databases ---


def get_chrom_database(acc):
    """Return OpticsCorr-Chrom Soft IOC database."""
    if acc == 'BO':
        sfams = _ct.BO_SFAMS_CHROMCORR
    elif acc == 'SI':
        sfams = _ct.SI_SFAMS_CHROMCORR

    corrmat_size = len(sfams)*2

    pvs_database = {
        'Version-Cte': {'type': 'string', 'value': 'UNDEF'},

        'Log-Mon': {'type': 'string', 'value': 'Starting...'},

        'ChromX-SP': {'type': 'float', 'value': 0, 'prec': 6,
                      'hilim': 10, 'lolim': -10, 'high': 10,
                      'low': -10, 'hihi': 10, 'lolo': -10},
        'ChromX-RB': {'type': 'float', 'value': 0, 'prec': 6},
        'ChromY-SP': {'type': 'float', 'value': 0, 'prec': 6,
                      'hilim': 10, 'lolim': -10, 'high': 10,
                      'low': -10, 'hihi': 10, 'lolo': -10},
        'ChromY-RB': {'type': 'float', 'value': 0, 'prec': 6},

        'DeltaChromX-SP': {'type': 'float', 'value': 0, 'prec': 6,
                           'hilim': 10, 'lolim': -10, 'high': 10,
                           'low': -10, 'hihi': 10, 'lolo': -10},
        'DeltaChromX-RB': {'type': 'float', 'value': 0, 'prec': 6},
        'DeltaChromY-SP': {'type': 'float', 'value': 0, 'prec': 6,
                           'hilim': 10, 'lolim': -10, 'high': 10,
                           'low': -10, 'hihi': 10, 'lolo': -10},
        'DeltaChromY-RB': {'type': 'float', 'value': 0, 'prec': 6},

        'ChromX-Mon': {'type': 'float', 'value': 0, 'prec': 6},
        'ChromY-Mon': {'type': 'float', 'value': 0, 'prec': 6},
        'CalcChromX-Mon': {'type': 'float', 'value': 0, 'prec': 6},
        'CalcChromY-Mon': {'type': 'float', 'value': 0, 'prec': 6},

        'ApplyDelta-Cmd': {'type': 'int', 'value': 0},

        'ConfigName-SP': {'type': 'string', 'value': ''},
        'ConfigName-RB': {'type': 'string', 'value': ''},
        'RespMat-Mon': {'type': 'float', 'count': corrmat_size,
                        'value': corrmat_size*[0], 'prec': 6, 'unit':
                        'Chrom x SFams (Matrix of add method)'},
        'NominalChrom-Mon': {'type': 'float', 'count': 2, 'value': 2*[0],
                             'prec': 6},
        'NominalSL-Mon': {'type': 'float', 'count': len(sfams),
                          'value': len(sfams)*[0], 'prec': 6},

        'ConfigPS-Cmd': {'type': 'int', 'value': 0},

        'Status-Mon': {'type': 'int', 'value': 0b11111},
        'StatusLabels-Cte': {'type': 'char', 'count': 1000,
                             'value': '\n'.join(_ct.STATUS_LABELS)},
    }

    for fam in sfams:
        pvs_database['SL' + fam + '-Mon'] = {
            'type': 'float', 'value': 0, 'prec': 4, 'unit': '1/m^2',
            'lolim': 0, 'hilim': 0, 'low': 0, 'high': 0, 'lolo': 0, 'hihi': 0}

    if acc == 'SI':
        pvs_database['CorrMeth-Sel'] = {
            'type': 'enum', 'enums': _et.PROP_ADD,
            'value': _ct.CorrMeth.Proportional}
        pvs_database['CorrMeth-Sts'] = {
            'type': 'enum', 'enums': _et.PROP_ADD,
            'value': _ct.CorrMeth.Proportional}
        pvs_database['CorrGroup-Sel'] = {
            'type': 'enum', 'enums': _et.INDIV_2KNOBS,
            'value': _ct.CorrGroup.TwoKnobs}
        pvs_database['CorrGroup-Sts'] = {
            'type': 'enum', 'enums': _et.INDIV_2KNOBS,
            'value': _ct.CorrGroup.TwoKnobs}

        # pvs_database['SyncCorr-Sel'] = {
        #     'type': 'enum', 'enums': _et.OFF_ON, 'value': _ct.SyncCorr.Off}
        # pvs_database['SyncCorr-Sts'] = {
        #     'type': 'enum', 'enums': _et.OFF_ON, 'value': _ct.SyncCorr.Off}
        # pvs_database['ConfigTiming-Cmd'] = {'type': 'int', 'value': 0}

        pvs_database['MeasChromDeltaFreqRF-SP'] = {
            'type': 'float', 'value': 200.0, 'unit': 'Hz',
            'prec': 4, 'lolim': 0.1, 'hilim': 1000.0}
        pvs_database['MeasChromDeltaFreqRF-RB'] = {
            'type': 'float', 'value': 200.0, 'unit': 'Hz',
            'prec': 4, 'lolim': 0.1, 'hilim': 1000.0}
        pvs_database['MeasChromWaitTune-SP'] = {
            'type': 'float', 'value': 5, 'unit': 's',
            'prec': 3, 'lolim': 0.005, 'hilim': 100}
        pvs_database['MeasChromWaitTune-RB'] = {
            'type': 'float', 'value': 5, 'unit': 's',
            'prec': 3, 'lolim': 0.005, 'hilim': 100}
        pvs_database['MeasChromNrSteps-SP'] = {
            'type': 'int', 'value': 8, 'unit': 'nr pts',
            'prec': 3, 'lolim': 2, 'hilim': 10}
        pvs_database['MeasChromNrSteps-RB'] = {
            'type': 'int', 'value': 8, 'unit': 'nr pts',
            'prec': 3, 'lolim': 2, 'hilim': 10}
        pvs_database['MeasChrom-Cmd'] = {
            'type': 'enum', 'enums': _et.MEAS_CMD, 'value': _ct.MeasCmd.Reset}
        pvs_database['MeasChromStatus-Mon'] = {
            'type': 'enum', 'enums': _et.MEAS_MON, 'value': _ct.MeasMon.Idle}
        pvs_database['MeasChromX-Mon'] = {
            'type': 'float', 'value': 0, 'prec': 6}
        pvs_database['MeasChromY-Mon'] = {
            'type': 'float', 'value': 0, 'prec': 6}

        pvs_database['MeasConfigDeltaSLFamSF-SP'] = {
            'type': 'float', 'value': 10.000, 'unit': '1/m2',
            'prec': 3, 'lolim': 0.100, 'hilim': 50.000}
        pvs_database['MeasConfigDeltaSLFamSF-RB'] = {
            'type': 'float', 'value': 10.000, 'unit': '1/m2',
            'prec': 3, 'lolim': 0.100, 'hilim': 50.000}
        pvs_database['MeasConfigDeltaSLFamSD-SP'] = {
            'type': 'float', 'value': 10.000, 'unit': '1/m2',
            'prec': 3, 'lolim': 0.100, 'hilim': 50.000}
        pvs_database['MeasConfigDeltaSLFamSD-RB'] = {
            'type': 'float', 'value': 10.000, 'unit': '1/m2',
            'prec': 3, 'lolim': 0.100, 'hilim': 50.000}
        pvs_database['MeasConfigWait-SP'] = {
            'type': 'float', 'value': 1, 'unit': 's',
            'prec': 3, 'lolim': 0.005, 'hilim': 100}
        pvs_database['MeasConfigWait-RB'] = {
            'type': 'float', 'value': 1, 'unit': 's',
            'prec': 3, 'lolim': 0.005, 'hilim': 100}
        pvs_database['MeasConfigName-SP'] = {
            'type': 'string', 'value': 'UNDEF'}
        pvs_database['MeasConfigName-RB'] = {
            'type': 'string', 'value': 'UNDEF'}
        pvs_database['MeasConfigSave-Cmd'] = {
            'type': 'int', 'value': 0}
        pvs_database['MeasConfig-Cmd'] = {
            'type': 'enum', 'enums': _et.MEAS_CMD, 'value': _ct.MeasCmd.Reset}
        pvs_database['MeasConfigStatus-Mon'] = {
            'type': 'enum', 'enums': _et.MEAS_MON, 'value': _ct.MeasMon.Idle}

    pvs_database = _csdev.add_pvslist_cte(pvs_database)
    return pvs_database


def get_tune_database(acc):
    """Return OpticsCorr-Tune Soft IOC database."""
    if acc == 'BO':
        qfams = _ct.BO_QFAMS_TUNECORR
    elif acc == 'SI':
        qfams = _ct.SI_QFAMS_TUNECORR

    corrmat_size = len(qfams)*2

    pvs_database = {
        'Version-Cte': {'type': 'string', 'value': 'UNDEF'},

        'Log-Mon': {'type': 'string', 'value': 'Starting...'},

        'DeltaTuneX-SP': {'type': 'float', 'value': 0, 'prec': 6,
                          'hilim': 5, 'lolim': -5, 'high': 5, 'low': -5,
                          'hihi': 5, 'lolo': -5},
        'DeltaTuneX-RB': {'type': 'float', 'value': 0, 'prec': 6,
                          'hilim': 5, 'lolim': -5, 'high': 5, 'low': -5,
                          'hihi': 5, 'lolo': -5},
        'DeltaTuneX-Mon': {'type': 'float', 'value': 0, 'prec': 6,
                           'hilim': 5, 'lolim': -5, 'high': 5, 'low': -5,
                           'hihi': 5, 'lolo': -5},
        'DeltaTuneY-SP': {'type': 'float', 'value': 0, 'prec': 6,
                          'hilim': 5, 'lolim': -5, 'high': 5, 'low': -5,
                          'hihi': 5, 'lolo': -5},
        'DeltaTuneY-RB': {'type': 'float', 'value': 0, 'prec': 6,
                          'hilim': 5, 'lolim': -5, 'high': 5, 'low': -5,
                          'hihi': 5, 'lolo': -5},
        'DeltaTuneY-Mon': {'type': 'float', 'value': 0, 'prec': 6,
                           'hilim': 5, 'lolim': -5, 'high': 5, 'low': -5,
                           'hihi': 5, 'lolo': -5},

        'ApplyDelta-Cmd': {'type': 'int', 'value': 0},

        'ConfigName-SP': {'type': 'string', 'value': ''},
        'ConfigName-RB': {'type': 'string', 'value': ''},
        'RespMat-Mon': {'type': 'float', 'count': corrmat_size,
                        'value': corrmat_size*[0], 'prec': 6, 'unit':
                        'Tune x QFams (Nominal Response Matrix)'},
        'NominalKL-Mon': {'type': 'float', 'count': len(qfams),
                          'value': len(qfams)*[0], 'prec': 6},

        'ConfigPS-Cmd': {'type': 'int', 'value': 0},

        'SetNewRefKL-Cmd': {'type': 'int', 'value': 0},

        'Status-Mon': {'type': 'int', 'value': 0b11111},
        'StatusLabels-Cte': {'type': 'char', 'count': 1000,
                             'value': '\n'.join(_ct.STATUS_LABELS)},
    }

    for fam in qfams:
        pvs_database['RefKL' + fam + '-Mon'] = {
            'type': 'float', 'value': 0, 'prec': 6, 'unit': '1/m'}

        pvs_database['DeltaKL' + fam + '-Mon'] = {
            'type': 'float', 'value': 0, 'prec': 6, 'unit': '1/m',
            'lolim': 0, 'hilim': 0, 'low': 0, 'high': 0, 'lolo': 0, 'hihi': 0}

    if acc == 'SI':
        pvs_database['CorrMeth-Sel'] = {
            'type': 'enum', 'enums': _et.PROP_ADD,
            'value': _ct.CorrMeth.Proportional}
        pvs_database['CorrMeth-Sts'] = {
            'type': 'enum', 'enums': _et.PROP_ADD,
            'value': _ct.CorrMeth.Proportional}
        pvs_database['CorrGroup-Sel'] = {
            'type': 'enum', 'enums': _et.INDIV_2KNOBS,
            'value': _ct.CorrGroup.TwoKnobs}
        pvs_database['CorrGroup-Sts'] = {
            'type': 'enum', 'enums': _et.INDIV_2KNOBS,
            'value': _ct.CorrGroup.TwoKnobs}

        pvs_database['SyncCorr-Sel'] = {
            'type': 'enum', 'enums': _et.OFF_ON, 'value': _ct.SyncCorr.Off}
        pvs_database['SyncCorr-Sts'] = {
            'type': 'enum', 'enums': _et.OFF_ON, 'value': _ct.SyncCorr.Off}
        pvs_database['ConfigTiming-Cmd'] = {'type': 'int', 'value': 0}

        pvs_database['MeasConfigDeltaKLFamQF-SP'] = {
            'type': 'float', 'value': 0.020, 'unit': '1/m',
            'prec': 3, 'lolim': 0.001, 'hilim': 0.100}
        pvs_database['MeasConfigDeltaKLFamQF-RB'] = {
            'type': 'float', 'value': 0.020, 'unit': '1/m',
            'prec': 3, 'lolim': 0.001, 'hilim': 0.100}
        pvs_database['MeasConfigDeltaKLFamQD-SP'] = {
            'type': 'float', 'value': 0.020, 'unit': '1/m',
            'prec': 3, 'lolim': 0.001, 'hilim': 0.100}
        pvs_database['MeasConfigDeltaKLFamQD-RB'] = {
            'type': 'float', 'value': 0.020, 'unit': '1/m',
            'prec': 3, 'lolim': 0.001, 'hilim': 0.100}
        pvs_database['MeasConfigWait-SP'] = {
            'type': 'float', 'value': 1, 'unit': 's',
            'prec': 3, 'lolim': 0.005, 'hilim': 100}
        pvs_database['MeasConfigWait-RB'] = {
            'type': 'float', 'value': 1, 'unit': 's',
            'prec': 3, 'lolim': 0.005, 'hilim': 100}
        pvs_database['MeasConfigName-SP'] = {
            'type': 'string', 'value': 'UNDEF'}
        pvs_database['MeasConfigName-RB'] = {
            'type': 'string', 'value': 'UNDEF'}
        pvs_database['MeasConfigSave-Cmd'] = {
            'type': 'int', 'value': 0}
        pvs_database['MeasConfig-Cmd'] = {
            'type': 'enum', 'enums': _et.MEAS_CMD, 'value': _ct.MeasCmd.Reset}
        pvs_database['MeasConfigStatus-Mon'] = {
            'type': 'enum', 'enums': _et.MEAS_MON, 'value': _ct.MeasMon.Idle}

    pvs_database = _csdev.add_pvslist_cte(pvs_database)
    return pvs_database

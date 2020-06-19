"""Define PVs, contants and properties of PosAng SoftIOCs."""

from .. import csdev as _csdev


class Const:
    """Const class defining PosAng constants."""

    TB_CORRH_POSANG = ('TB-04:PS-CH-1', 'TB-04:PU-InjSept')
    TB_CORRV_POSANG = ('TB-04:PS-CV-1', 'TB-04:PS-CV-2')

    TS_CORRH_POSANG_CHSEPT = ('TS-04:PS-CH', 'TS-04:PU-InjSeptF')
    TS_CORRH_POSANG_SEPTSEPT = \
        ('TS-04:PU-InjSeptG-1', 'TS-04:PU-InjSeptG-2', 'TS-04:PU-InjSeptF')
    TS_CORRV_POSANG = \
        ('TS-04:PS-CV-0', 'TS-04:PS-CV-1', 'TS-04:PS-CV-1E2', 'TS-04:PS-CV-2')

    STATUSLABELS = ('PS Connection', 'PS PwrState', 'PS OpMode', 'PS CtrlMode')


def get_posang_database(tl, corrs_type='ch-sept'):
    """Return Soft IOC database."""
    if tl.upper() == 'TS':
        if corrs_type == 'ch-sept':
            corrh = Const.TS_CORRH_POSANG_CHSEPT
        else:
            corrh = Const.TS_CORRH_POSANG_SEPTSEPT
        corrv = Const.TS_CORRV_POSANG
        ch1_kick_unit = 'mrad'
    elif tl.upper() == 'TB':
        corrh = Const.TB_CORRH_POSANG
        corrv = Const.TB_CORRV_POSANG
        ch1_kick_unit = 'urad'

    pvs_database = {
        'Version-Cte':       {'type': 'string', 'value': 'UNDEF'},

        'Log-Mon':           {'type': 'string', 'value': 'Starting...'},

        'DeltaPosX-SP':      {'type': 'float', 'value': 0, 'prec': 6,
                              'unit': 'mm', 'hilim': 10, 'lolim': -10},
        'DeltaPosX-RB':      {'type': 'float', 'value': 0, 'prec': 6,
                              'unit': 'mm'},
        'DeltaAngX-SP':      {'type': 'float', 'value': 0, 'prec': 6,
                              'unit': 'mrad', 'hilim': 10, 'lolim': -10},
        'DeltaAngX-RB':      {'type': 'float', 'value': 0, 'prec': 6,
                              'unit': 'mrad'},

        'DeltaPosY-SP':      {'type': 'float', 'value': 0, 'prec': 6,
                              'unit': 'mm', 'hilim': 10, 'lolim': -10},
        'DeltaPosY-RB':      {'type': 'float', 'value': 0, 'prec': 6,
                              'unit': 'mm'},
        'DeltaAngY-SP':      {'type': 'float', 'value': 0, 'prec': 6,
                              'unit': 'mrad', 'hilim': 10, 'lolim': -10},
        'DeltaAngY-RB':      {'type': 'float', 'value': 0, 'prec': 6,
                              'unit': 'mrad'},

        'ConfigName-SP':     {'type': 'string', 'value': ''},
        'ConfigName-RB':     {'type': 'string', 'value': ''},
        'RespMatX-Mon':      {'type': 'float', 'value': 4*[0], 'prec': 6,
                              'count': 4},
        'RespMatY-Mon':      {'type': 'float', 'value': 4*[0], 'prec': 6,
                              'count': 4},

        'CH1-Cte':           {'type': 'string', 'value': corrh[0]},
        'RefKickCH1-Mon':    {'type': 'float', 'value': 0, 'prec': 4,
                              'unit': ch1_kick_unit},
        'CH2-Cte':           {'type': 'string', 'value': corrh[1]},
        'RefKickCH2-Mon':    {'type': 'float', 'value': 0, 'prec': 4,
                              'unit': 'mrad'},
        'CV1-Cte':           {'type': 'string', 'value':  corrv[0]},
        'RefKickCV1-Mon':    {'type': 'float', 'value': 0, 'prec': 4,
                              'unit': 'urad'},
        'CV2-Cte':           {'type': 'string', 'value':  corrv[1]},
        'RefKickCV2-Mon':    {'type': 'float', 'value': 0, 'prec': 4,
                              'unit': 'urad'},
        'SetNewRefKick-Cmd': {'type': 'int', 'value': 0},

        'ConfigPS-Cmd':      {'type': 'int', 'value': 0},

        'Status-Mon':        {'type': 'int', 'value': 0b1111},
        'StatusLabels-Cte':  {'type': 'char', 'count': 1000,
                              'value': '\n'.join(Const.STATUSLABELS)},
    }
    if len(corrh) == 3:
        pvs_database['CH3-Cte'] = {'type': 'string', 'value': corrh[2]}
        pvs_database['RefKickCH3-Mon'] = {'type': 'float', 'value': 0,
                                          'prec': 4, 'unit': 'mrad'}
    if len(corrv) == 4:
        pvs_database['CV3-Cte'] = {'type': 'string', 'value': corrv[2]}
        pvs_database['RefKickCV3-Mon'] = {'type': 'float', 'value': 0,
                                          'prec': 4, 'unit': 'urad'}
        pvs_database['CV4-Cte'] = {'type': 'string', 'value': corrv[3]}
        pvs_database['RefKickCV4-Mon'] = {'type': 'float', 'value': 0,
                                          'prec': 4, 'unit': 'urad'}
    pvs_database = _csdev.add_pvslist_cte(pvs_database)
    return pvs_database

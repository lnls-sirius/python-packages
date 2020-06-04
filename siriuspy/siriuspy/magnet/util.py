"""Magnet utils."""

import math as _math
import re as _re

import numpy as _numpy


from ..namesys import SiriusPVName as _SiriusPVName


def get_nominal_dipole_angles():
    """Return individual nominal angles [rad] of all Sirius dipole types."""
    ref_angles = {
        'SI_BC': _math.radians(4.296600),
        'SI_B1': _math.radians(2.755300),
        'SI_B2': _math.radians(4.096400),
        'TS': _math.radians(5.011542),  # TS.V03.03
        'BO': _math.radians(7.200000),
        'TB': _math.radians(15.00000),
        'LI': _math.radians(-45.00000),
    }
    return ref_angles


def get_magfunc_2_multipole_dict():
    """Return multipole dict given the magnetic function.

    Conventions:
        1. harmonics: 0 (dipole), 1 (quadrupole), 2 (sectupole), etc
        2. 'normal' for  normal field and 'skew' for skew field.
    """
    _magfuncs = {
        'dipole': {'type': 'normal', 'harmonic': 0},
        'corrector-horizontal': {'type': 'normal', 'harmonic': 0},
        'corrector-vertical': {'type': 'skew', 'harmonic': 0},
        'quadrupole': {'type': 'normal', 'harmonic': 1},
        'quadrupole-skew': {'type': 'skew', 'harmonic': 1},
        'sextupole': {'type': 'normal', 'harmonic': 2},
        'id-apu': {'type': 'normal', 'harmonic': 0},
    }
    return _magfuncs


def get_multipole_name(harmonic, suffix=None):
    """Return names of multipoles, given harmonic number."""
    names = {0: 'dipole',
             1: 'quadrupole',
             2: 'sextupole',
             3: 'octupole',
             4: 'decapole',
             5: 'dodecapole', }
    suffix = 'pole' if suffix is None else suffix
    try:
        return names[harmonic].replace('pole', suffix)
    except KeyError:
        return '{0:d}-pole'.format((harmonic+1)*2).replace('pole', suffix)


def get_multipole_si_units(harmonic, power=None, product=None):
    """Return multipole units, given harmonic number."""
    product = '.' if product is None else product
    if harmonic == 0:
        return 'T{0:s}m'.format(product)
    elif harmonic == 1:
        return 'T'
    elif harmonic == 2:
        return 'T/m'
    else:
        power = '^' if power is None else power
        return 'T/m{0:s}{1:d}'.format(power, harmonic-1)


def linear_extrapolation(x, x1, x2, y1, y2):
    """Return linear extrapolation function value."""
    if x2 == x1:
        return min(y1, y2, key=abs)
    else:
        return y1 + (y2-y1)*(x-x1)/(x2-x1)


def sum_magnetic_multipoles(*multipoles_list):
    """Sum an iterable composed of multipoles dictionaries."""
    res = {}
    for multipoles in multipoles_list:
        nmpoles = multipoles.get('normal', {})
        res_tmp = res.get('normal', {})
        for harm, mpole in nmpoles.items():
            res_tmp[harm] = res_tmp.get(harm, 0.0) + mpole
        if res_tmp:
            res['normal'] = res_tmp
        smpoles = multipoles.get('skew', {})
        res_tmp = res.get('skew', {})
        for harm, mpole in smpoles.items():
            res_tmp[harm] = res_tmp.get(harm, 0.0) + mpole
        if res_tmp:
            res['skew'] = res_tmp
    return res


# TODO: merge this function with corresponding functions|class in
# ramp. also, default nrpts should be taken from csdevices!!!
def get_default_ramp_waveform(interval=500, nrpts=4000,
                              ti=None, fi=None, forms=None):
    """Generate normalized ramp."""
    time = interval * _numpy.linspace(0, 1.0, nrpts)
    if ti is None:
        ti = interval * _numpy.array([0, 13, 310,
                                      322, 330, 342, 480, 500])/500.0
    if fi is None:
        fi = _numpy.array([0.01, 0.02625, 1.0339285714,
                           1.05, 1.05, 1, 0.07, 0.01])
    if forms is None:
        forms = ['cube', 'injection', 'cube', 'line', 'cube', 'line', 'cube']

    # brho_3gev = 10.00692271077752  # [T.m]
    # brho_150mev = 0.5003432394479871  # [T.m]

    ramp = _numpy.zeros(len(time))
    va1 = _numpy.zeros(len(ti))
    dti = _numpy.zeros(len(forms))

    # findout the initial derivatives and delta time from the straigth lines
    for i, wfm in enumerate(forms):
        dti[i] = (ti[i+1]-ti[i])
        if wfm.startswith(('l', 'i')) or wfm == 0:
            equal_previous = False
            va1[i] = (fi[i+1]-fi[i])/dti[i]
            va1[i+1] = va1[i]
        else:
            equal_previous = True
        if equal_previous:
            va1[i] = va1[i-1]

    # calculate the ramp:
    for i, wfm in enumerate(forms):
        ind = _numpy.bitwise_and(ti[i] <= time, time <= ti[i+1])
        dtime = time[ind] - ti[i]
        va2, va3 = 0, 0
        if wfm.startswith(('c', 'i')):
            va2 = (-3*(fi[i]-fi[i+1]) - dti[i] * (2*va1[i]+va1[i+1]))/dti[i]**2
            va3 = (2*(fi[i]-fi[i+1]) + dti[i] * (va1[i]+va1[i+1]))/dti[i]**3
        ramp[ind] = fi[i] + va1[i]*dtime + va2*dtime**2 + va3*dtime**3

    return ramp


def get_section_dipole_name(maname):
    """Return name of dipole in the same section of given magnet name."""
    maname = _SiriusPVName(maname)
    if _re.match('B.*', maname.dev):
        return None
    elif maname.sec == 'SI':
        if maname.dev in {"InjDpKckr", "InjNLKckr"}:
            return 'TS-Fam:MA-B'
        return "SI-Fam:MA-B1B2"
    elif maname.sec == 'BO':
        if maname.dev in {'InjKckr', 'EjeKckr'}:
            return 'TB-Fam:MA-B'
        return 'BO-Fam:MA-B'
    elif maname.sec in {'TB', 'LI'}:
        return 'TB-Fam:MA-B'
    elif maname.sec == 'TS':
        return 'TS-Fam:MA-B'
    else:
        raise NotImplementedError(
            'No section named {}'.format(maname.sec))


def get_magnet_family_name(maname):
    """Return family name associated with a given magnet name."""
    maname = _SiriusPVName(maname)
    if maname.sec == "SI" and \
            maname.sub != "Fam" and \
            _re.match("(?:QD|QF|Q[0-9]).*", maname.dev):
        return _re.sub("SI-\d{2}\w{2}:", "SI-Fam:", maname)
    else:
        return None


def magnet_class(maname):
    """Return class of a magnet: Dipole, Normal, Trim, Pulsed."""
    maname = _SiriusPVName(maname)
    if maname.dis == 'ID':
        if maname.dev in ('APU22', ):
            return 'id-apu'
    if maname.dis != 'MA' and maname.dis != 'PM':
        raise ValueError("Cannot classify {}".format(maname))
    if maname.dis == 'PM':
        return 'pulsed'
    if maname.dev.startswith('B'):
        return 'dipole'
    if 'QS' not in maname.dev and \
            maname.sec == 'SI' and \
            maname.dev.startswith('Q') and \
            maname.sub != 'Fam':
        return 'trim'

    return 'normal'

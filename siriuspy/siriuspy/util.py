"""Module with general utilities."""

import os as _os
import sys as _sys
import time as _time
from collections import Counter as _Counter
from collections import namedtuple as _namedtuple
import logging as _log
import inspect as _inspect
import subprocess as _sp
import datetime as _datetime

import epics as _epics

from mathphys import beam_optics as _beam
from siriuspy import envars as _envars


def conv_splims_labels(label):
    """Convert setpoint limit labels from pcaspy to epics and vice-versa."""
    # Limits description:
    # -------------------
    # DRVH     driver high level limit
    # HIHI     high-high level limit (ALARM)
    # HIGH     IOC high level limit (ALARM)
    # DRVL     driver low level limit
    # LOLO     IOC low-low level limit (ALARM)
    # LOW      IOC low level limit (ALARM)
    # LOPR     Low operating range
    # HOPR     High operating range
    #
    # Rules
    # -----
    # LOLO <= LO <= HI <= HIHI
    # DRVL <= LOPR <= HOPR <= DRVH.
    #
    labels_dict = {
        # Epics-DB  pcaspy    PyEpics
        # ===========================
        'DRVH':     'DRVH',   # upper_ctrl_limit
        'HIHI':     'hihi',   # upper_alarm_limit
        'HIGH':     'high',   # upper_warning_limit
        'HOPR':     'hilim',  # upper_disp_limit
        'LOPR':     'lolim',  # lower_disp_limit
        'LOW':      'low',    # lower_warning_limit
        'LOLO':     'lolo',   # lower_alarm_limit
        'DRVL':     'DRVL',   # lower_ctrl_limit
        'TSTV':     'TSTV',   # SIRIUS specific (Test value)
        'TSTR':     'TSTR',   # SIRIUS specific (Test acceptable range)
    }
    if label in labels_dict:
        # epics -> pcaspy
        return labels_dict[label]
    else:
        for k, value in labels_dict.items():
            if value == label:
                # pcaspy -> epics
                return k
        raise KeyError('Invalid splims label "' + label + '"!')


def get_last_commit_hash():
    """Get commit Hash of the repository of the calling file."""
    fname = _os.path.realpath(_inspect.stack()[1][1])
    path = fname.rpartition(_os.path.sep)[0]
    pwd = _os.path.abspath('.')
    return _sp.getoutput('cd ' + path +
                         '; git log --format=%h -1; cd ' + pwd)


def get_timestamp(now=None):
    """Get formatted timestamp ."""
    if now is None:
        now = _time.time()
    st = _datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d-%H:%M:%S')
    st = st + '.{0:03d}'.format(int(1000*(now-int(now))))
    return st


def read_text_data(text):
    """Parse text data from sirius-consts web server."""
    lines = text.splitlines()
    parameters = {}
    data = []
    for line in lines:
        line = line.strip()
        if not line:
            continue  # empty line
        if line[0] == '#':
            if len(line[1:].strip()) > 0:
                token, *words = line[1:].split()
                if token[0] == '[':
                    # it is a parameter.
                    parm = token[1:-1].strip()
                    parameters[parm] = words
        else:
            # it is a data line
            data.append(line.split())
    return data, parameters


def print_ioc_banner(ioc_name, db, description, version, prefix):
    """IOC banner."""
    strl = '==================================='
    nchars = (len(strl)-len(ioc_name))//2
    line = ' '*nchars + ioc_name + ' '*nchars
    _log.info(strl)
    _log.info(line)
    _log.info(strl)
    _log.info(description)
    _log.info('LNLS, Sirius Project.')
    _log.info('Version   : %s', version)
    _log.info('Timestamp : %s', get_timestamp())
    _log.info('Prefix    : %s', prefix)
    _log.info('')
    pvs = sorted(tuple(db.keys()))
    for i, pvname in enumerate(pvs, 1):
        _log.info('{0:04d} {1:<}'.format(i, pvname))


def configure_log_file(stream=None, filename=None, debug=False):
    """Configure logging messages for the IOCs."""
    if stream is not None:
        dic_ = {'stream': stream}
    elif filename is not None:
        dic_ = {'filename': filename, 'filemode': 'w'}
    else:
        dic_ = {'stream': _sys.stdout}

    level = _log.DEBUG if debug else _log.INFO
    fmt = ('%(levelname)7s | %(asctime)s | ' +
           '%(module)15s.%(funcName)-20s[%(lineno)4d] ::: %(message)s')
    _log.basicConfig(format=fmt, datefmt='%F %T', level=level, **dic_)


def beam_rigidity(energy):
    """Return beam rigidity, beta amd game, given its energy [GeV]."""
    brho, _, beta, gamma, _ = _beam.beam_rigidity(energy=energy)
    return brho, beta, gamma


def check_pv_online(pvname, timeout=1.0, use_prefix=True):
    """Return whether a PV is online."""
    if use_prefix:
        pvname = _envars.VACA_PREFIX + pvname
    pvobj = _epics.PV(pvname=pvname, connection_timeout=timeout)
    status = pvobj.wait_for_connection(timeout=timeout)
    return status


def get_strength_label(magfunc):
    """Return magnetic function strength label."""
    if magfunc == 'dipole':
        return 'Energy'
    elif magfunc in ('quadrupole', 'quadrupole-skew'):
        return 'KL'
    elif magfunc in ('sextupole',):
        return 'SL'
    elif magfunc in ('corrector-horizontal', 'corrector-vertical'):
        return 'Kick'
    else:
        raise ValueError('magfunc "{}" not defined!'.format(magfunc))


def get_strength_units(magfunc, pstype=None, pulsed=False):
    """Return strength units."""
    if magfunc == 'dipole':
        return 'GeV'
    elif magfunc in ('quadrupole', 'quadrupole-skew'):
        return '1/m'
    elif magfunc in ('sextupole',):
        return '1/m^2'
    elif magfunc in ('corrector-horizontal', 'corrector-vertical'):
        if pulsed:
            return 'mrad'
        if pstype and pstype.startswith('li-spect'):
            return 'deg'
        return 'urad'
    else:
        raise ValueError('magfunc "{}" not defined!'.format(magfunc))


def update_bit(v, bit_pos, bit_val):
    """Update a specific integer bit.

    Parameters
    ----------
    v: non-negative int
        Integer whose bit will be updated.
    bit_pos: non-negative int
        The position of the bit to update.
    bit_val: Any python object that evaluates to True or False
        Value to put on the bit.

    """
    if not isinstance(v, int) or not isinstance(bit_pos, int):
        raise TypeError("v and bit_pos must be integers.")

    if v < 0 or bit_pos < 0:
        raise ValueError("v and bit_pos must be non-negative.")

    return v | (1 << bit_pos) if bit_val else v & ~(1 << bit_pos)


def get_bit(v, bit_pos):
    """Update a specific integer bit.

    Parameters
    ----------
    v: non-negative int
        Integer whose bit will be get.
    bit_pos: int
        The position of the bit to get.

    """
    if not isinstance(v, int) or not isinstance(bit_pos, int):
        raise TypeError("v and bit_pos must be integers")

    if v < 0 or bit_pos < 0:
        raise ValueError("v and bit_pos must be non-negative.")

    return (v >> bit_pos) & 1


def mode(lst):
    """Find statistical mode of iterable of hashable objects."""
    counter = _Counter(lst)
    return counter.most_common(1)[0]


def check_public_interface_namespace(namespace, valid_interface,
                                     checkdoc_flag=True,
                                     print_flag=True):
    """Check function used in unittests to test module's public interface.

    This function checks only static public interface symbols. It does not
    check those symbols that are created within class methods.
    """
    for name in namespace.__dict__:
        if checkdoc_flag:
            doc = getattr(name, '__doc__')
            if doc is None or len(doc) < 5:
                if print_flag:
                    print('"' + name + '" has an invalid docstring!')
                return False
        if not name.startswith('_') and name not in valid_interface:
            if print_flag:
                print('Invalid symbol: ', name)
            return False
    for name in valid_interface:
        if name not in namespace.__dict__:
            if print_flag:
                print('Missing symbol: ', name)
            return False
    return True


# This solution was copied from:
# https://stackoverflow.com/questions/5189699/how-to-make-a-class-property
class ClassProperty:
    """This is a way of defining a readable class property.

    It is useful to delay the process of reading static tables during
    modules initialization (import time)
    """

    def __init__(self, func):
        """."""
        self.func = func

    def __get__(self, obj, owner):
        """."""
        return self.func(owner)

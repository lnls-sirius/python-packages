
"""Utilities for cycle."""

import time as _time
import numpy as _np

from ..namesys import Filter as _Filter
from ..search import PSSearch as _PSSearch, HLTimeSearch as _HLTimeSearch


TRIGGER_NAMES = {
    'TB-Glob:TI-Mags', 'TS-Glob:TI-Mags',
    'BO-Glob:TI-Mags-Fams', 'BO-Glob:TI-Mags-Corrs',
    'SI-Glob:TI-Mags-Bends', 'SI-Glob:TI-Mags-Quads',
    'SI-Glob:TI-Mags-Sexts', 'SI-Glob:TI-Mags-Skews',
    'SI-Glob:TI-Mags-Corrs', 'SI-Glob:TI-Mags-QTrims'}


def get_psnames():
    """Return psnames."""
    names = _PSSearch.get_psnames({'sec': '(LI|TB|TS)', 'dis': 'PS'})
    names.extend(_PSSearch.get_psnames(
        {'sec': 'SI', 'sub': 'Fam', 'dis': 'PS', 'dev': '(B|Q.*|S.*)'}))
    names.extend(_PSSearch.get_psnames(
        {'sec': 'SI', 'sub': '[0-2][0-9]C2', 'dis': 'PS',
         'dev': 'CV', 'idx': '2'}))
    to_remove = _PSSearch.get_psnames({'sec': 'TS', 'idx': '(0|1E2)'})
    for name in to_remove:
        names.remove(name)
    return names


def get_sections(psnames):
    """Return sections."""
    sections = list()
    for sec in ('LI', 'TB', 'BO', 'TS', 'SI'):
        if _Filter.process_filters(psnames, filters={'sec': sec}):
            sections.append(sec)
    return sections


def get_trigger_by_psname(psnames):
    """Return triggers corresponding to psnames."""
    psnames = set(psnames)
    triggers = set()
    for trig in TRIGGER_NAMES:
        dev_names = set(_HLTimeSearch.get_hl_trigger_channels(trig))
        dev_names = {dev.device_name for dev in dev_names}
        if psnames & dev_names:
            triggers.add(trig)
    return triggers


def pv_timed_get(pvobj, value, wait=5, abs_tol=0.0, rel_tol=1e-06):
    """Do timed get."""
    if not pvobj.connected:
        return False
    time0 = _time.time()
    while _time.time() - time0 < wait:
        pvvalue = pvobj.get()
        status = False
        if isinstance(value, (tuple, list, _np.ndarray)):
            if not isinstance(pvvalue, (tuple, list, _np.ndarray)):
                status = False
            elif len(value) != len(pvvalue):
                status = False
            else:
                if all(_np.isclose(pvvalue, value,
                                   atol=abs_tol, rtol=rel_tol)):
                    status = True
                    break
        else:
            if _np.isclose(pvvalue, value, atol=abs_tol, rtol=rel_tol):
                status = True
                break
        _time.sleep(wait/10.0)
    return status


def pv_conn_put(pvobj, value):
    """Put if connected."""
    if not pvobj.connected:
        return False
    if pvobj.put(value):
        return True
    return False

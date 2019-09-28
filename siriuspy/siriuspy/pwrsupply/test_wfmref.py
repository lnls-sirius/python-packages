#!/usr/bin/env python-sirius

"""Module for WfmRef tests."""

import time
import matplotlib.pyplot as plt
import numpy as np

from siriuspy.search import PSSearch
from siriuspy.pwrsupply.udc import UDC
from siriuspy.pwrsupply.pru import PRU
# from siriuspy.pwrsupply.bsmp import FBP
from siriuspy.pwrsupply.status import PSCStatus


BBBNAME = 'IA-08RaCtrl:CO-PSCtrl-SI5'


def create_udc(bbbname):
    """Create UDC."""
    pru = PRU(bbbname=bbbname)
    bsmps = PSSearch.conv_bbbname_2_bsmps(bbbname)
    psnames, device_ids = zip(*bsmps)
    psmodel = PSSearch.conv_psname_2_psmodel(psnames[0])
    _udc = UDC(pru=pru, psmodel=psmodel, device_ids=device_ids)
    return _udc


def print_status(ps_list):
    """Print status."""

    st1, st2, st3, st4, st5, st6 = ['{:<15}:'] * 6
    va1, va2, va3, va4, va5, va6 = \
        [['status'], ['open_loop'], ['interface'],
         ['interface'], ['model'], ['unlock']]
    for ps in ps_list:
        _, ps_status = ps.read_variable(
            ps.CONST_PSBSMP.V_PS_STATUS, timeout=100)
        status = PSCStatus(ps_status=ps_status)
        st1 += ' {:6d}'
        va1.append(status.state)
        st2 += ' {:6d}'
        va2.append(status.open_loop)
        st3 += ' {:6d}'
        va3.append(status.interface)
        st4 += ' {:6d}'
        va4.append(status.active)
        st5 += ' {:6d}'
        va5.append(status.active)
        st6 += ' {:6d}'
        va6.append(status.unlocked)
    sts = [st1, st2, st3, st4, st5, st6]
    vas = [va1, va2, va3, va4, va5, va6]
    for st, va in zip(sts, vas):
        print(st.format(*va))


def print_wfmref(ps_list):
    """Print wfmref data."""
    st1, st2, st3, st4, st5, st6, st7 = ['{:<15}:'] * 7
    va1, va2, va3, va4, va5, va6, va7 = \
        [['wfmref_maxsize'],
         ['wfmref_select'],
         ['wfmref_size'],
         ['wfmref_idx'],
         ['wfmref_ptr_beg'],
         ['wfmref_ptr_end'],
         ['wfmref_ptr_idx']]
    for ps in ps_list:
        wfmref_ptr_values = ps.wfmref_pointer_values
        st1 += ' {:6d}'
        va1.append(ps.wfmref_maxsize)
        st2 += ' {:6d}'
        va2.append(ps.wfmref_select)
        st3 += ' {:6d}'
        va3.append(ps.wfmref_size)
        st4 += ' {:6d}'
        va4.append(ps.wfmref_idx)
        st5 += ' {:6d}'
        va5.append(wfmref_ptr_values[0])
        st6 += ' {:6d}'
        va6.append(wfmref_ptr_values[1])
        st7 += ' {:6d}'
        va7.append(wfmref_ptr_values[2])
    sts = [st1, st2, st3, st4, st5, st6, st7]
    vas = [va1, va2, va3, va4, va5, va6, va7]
    for st, va in zip(sts, vas):
        print(st.format(*va))


def plot_wfmref(ps_list):
    """Plot wfmref."""
    for i, ps in enumerate(ps_list):
        curve = ps.wfmref_read()
        plt.plot(curve, label='WfmRef {} ({} points)'.format(i, len(curve)))
    plt.xlabel('Index')
    plt.ylabel('Current [A]')
    plt.legend()
    plt.show()


def print_basic_info(ps_list):
    """Print all info."""
    print('--- power supply status ---')
    print_status(ps_list)
    # print('--- wfmref ---')
    print_wfmref(ps_list)
    # print()
    # plot_wfmref(ps)


def reset_powersupplies(ps_list=None):
    """."""
    # reset UDC
    udc.reset()

    if ps_list is None:
        ps_list = (ps1, ps2, ps3, ps4)

    for ps in ps_list:
        # turn power supply on
        ps.execute_function(
            func_id=ps.CONST_PSBSMP.F_TURN_ON,
            input_val=None,
            timeout=100)
        # change mode to RmpWfm
        ps.execute_function(
            func_id=ps.CONST_PSBSMP.F_SELECT_OP_MODE,
            input_val=ps.CONST_PSBSMP.E_STATE_RMPWFM,
            timeout=100)
        time.sleep(0.010)  # needed?


def test_write_wfmref(ps):
    """."""
    reset_powersupplies([ps, ])

    # read original wfmref curve
    curve1 = np.array(ps.wfmref_read())
    # change it
    # new_curve = [2.0*i/len(curve1) for i in range(len(curve1))]
    new_curve = curve1[::-1]
    # write new wfmref curve and get it back
    ps.wfmref_write(new_curve)
    curve2 = np.array(ps.wfmref_read())
    # compare previous and next wfmref curves
    plt.plot(curve1, label='Prev WfmRef ({} points)'.format(len(curve1)))
    # plt.plot(new_curve, label='New curve ({} points)'.format(len(new_curve)))
    plt.plot(curve2, label='Next WfmRef ({} points)'.format(len(curve2)))
    plt.xlabel('Index')
    plt.ylabel('Current [A]')
    plt.legend()
    plt.show()

# --- create global objects ---

udc = create_udc(bbbname=BBBNAME)
ps1 = udc[1]
ps2 = udc[2]
ps3 = udc[3]
ps4 = udc[4]
all_ps = [ps1, ps2, ps3, ps4]

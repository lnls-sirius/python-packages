#!/usr/bin/env python-sirius

"""Module for WfmRef tests."""

import time
import matplotlib.pyplot as plt
import numpy as np

from siriuspy.search import PSSearch
from siriuspy.pwrsupply.pructrl.udc import UDC
from siriuspy.pwrsupply.pructrl.pru import PRU
from siriuspy.pwrsupply.pructrl.psdevstate import PSDevState
from siriuspy.pwrsupply.psctrl.pscstatus import PSCStatus


# BBBNAME = 'IA-08RaCtrl:CO-PSCtrl-SI5'
BBBNAME = 'IA-08RaCtrl:CO-PSCtrl-SI3'


def create_udc(bbbname=BBBNAME, udc_index=None):
    """Create UDC."""
    pru = PRU(bbbname=bbbname)
    if udc_index is not None:
        udc_list = PSSearch.conv_bbbname_2_udc(bbbname)
        udcname = udc_list[udc_index]
        bsmps = PSSearch.conv_udc_2_bsmps(udcname)
    else:
        bsmps = PSSearch.conv_bbbname_2_bsmps(bbbname)
    psnames, device_ids = zip(*bsmps)
    for psname, dev_id in bsmps:
        print('psname: {:<15}   dev_id: {}'.format(psname, dev_id))
    psmodel = PSSearch.conv_psname_2_psmodel(psnames[0])
    udc = UDC(pru=pru, psmodel=psmodel, device_ids=device_ids)
    return udc


def r485_message_duration(nrbytes=None, nrfloats=None):
    """Return nominal serial duration."""
    serial_clock = 6e6  # [MHz]
    serial_period = 1.0/serial_clock  # [s]
    byte_bitlen = 10
    byte_duration = byte_bitlen * serial_period  # [s]

    if nrfloats is not None:
        nrbytes = nrfloats*4
    duration = nrbytes * byte_duration
    return duration


def measure_duration_read_group_of_variables(psupply, group_id):
    """."""
    print('--- duration read_group_of_variables ---')
    psupply.channel.size_counter_reset()
    psupply.channel.pru.wr_duration_reset()
    time0 = time.time()
    psupply.read_group_of_variables(group_id, timeout=100)
    time1 = time.time()
    nrbytes = psupply.channel.size_counter
    duration_serial = r485_message_duration(nrbytes=nrbytes)
    duration_python = time1 - time0
    duration_prulib = psupply.channel.pru.wr_duration
    print('python duration: {:.2f} ms'.format(1000*duration_python))
    print('prulib duration: {:.2f} ms'.format(1000*duration_prulib))
    print('serial duration: {:.2f} ms'.format(1000*duration_serial))


def measure_duration_request_curve_block(psupply, curve_id, block):
    """."""
    print('--- duration request_curve_block ---')
    psupply.channel.size_counter_reset()
    psupply.channel.pru.wr_duration_reset()
    time0 = time.time()
    psupply.request_curve_block(curve_id, block, timeout=100)
    time1 = time.time()
    nrbytes = psupply.channel.size_counter
    duration_serial = r485_message_duration(nrbytes=nrbytes)
    duration_python = time1 - time0
    duration_prulib = psupply.channel.pru.wr_duration
    print('python duration: {:.2f} ms'.format(1000*duration_python))
    print('prulib duration: {:.2f} ms'.format(1000*duration_prulib))
    print('serial duration: {:.2f} ms'.format(1000*duration_serial))


def measure_duration_wfmref_read(psupply):
    """."""
    print('--- duration wfmref_read ---')
    psupply.channel.size_counter_reset()
    psupply.channel.pru.wr_duration_reset()
    time0 = time.time()
    psupply.wfmref_read()
    time1 = time.time()
    nrbytes = psupply.channel.size_counter
    duration_serial = r485_message_duration(nrbytes=nrbytes)
    duration_python = time1 - time0
    duration_prulib = psupply.channel.pru.wr_duration
    print('python duration: {:.2f} ms'.format(1000*duration_python))
    print('prulib duration: {:.2f} ms'.format(1000*duration_prulib))
    print('serial duration: {:.2f} ms'.format(1000*duration_serial))


# --- info print ---


def process_response(response, msg=''):
    """."""
    if not response:
        return None
    ack, data = response
    if ack != 0xE0:
        print()
        if msg:
            print(msg)
        print('!!! Error: {:02X}'.format(ack))
        print('    Data : {}'.format(data))
        print()
        return None
    return ack, data


def print_status(ps_list):
    """Print status."""
    if not isinstance(ps_list, (list, tuple)):
        ps_list = [ps_list, ]
    st1, st2, st3, st4, st5, st6, = ['{:<15}:'] * 6
    va1, va2, va3, va4, va5, va6, = \
        [['state'], ['open_loop'], ['interface'],
         ['active'], ['model'], ['unlock']]
    for ps in ps_list:
        address = ps.channel.address
        _, ps_status = process_response(
            ps.read_variable(
                ps.CONST.V_PS_STATUS, timeout=100),
            'ps_status {}'.format(address))

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
        va5.append(status.model)

        st6 += ' {:6d}'
        va6.append(status.unlocked)

    sts = [st1, st2, st3, st4, st5, st6]
    vas = [va1, va2, va3, va4, va5, va6]
    for st, va in zip(sts, vas):
        print(st.format(*va))


def print_wfmref(ps_list):
    """Print wfmref data."""
    if not isinstance(ps_list, (list, tuple)):
        ps_list = [ps_list, ]
    st1, st2, st3, st4, st5, st6, st7 = ['{:<15}:'] * 7
    va1, va2, va3, va4, va5, va6, va7 = \
        [['wfmref_select'],
         ['wfmref_maxsize'],
         ['wfmref_size'],
         ['wfmref_idx'],
         ['wfmref_ptr_beg'],
         ['wfmref_ptr_end'],
         ['wfmref_ptr_idx']]
    for ps in ps_list:
        wfmref_mon_ptr_values = ps.wfmref_pointer_values
        st1 += ' {:6d}'
        va1.append(ps.wfmref_select)
        st2 += ' {:6d}'
        va2.append(ps.wfmref_maxsize)
        st3 += ' {:6d}'
        va3.append(ps.wfmref_size())
        st4 += ' {:6d}'
        va4.append(ps.wfmref_index)
        st5 += ' {:6d}'
        va5.append(wfmref_mon_ptr_values[0])
        st6 += ' {:6d}'
        va6.append(wfmref_mon_ptr_values[1])
        st7 += ' {:6d}'
        va7.append(wfmref_mon_ptr_values[2])
    sts = [st1, st2, st3, st4, st5, st6, st7]
    vas = [va1, va2, va3, va4, va5, va6, va7]
    for st, va in zip(sts, vas):
        print(st.format(*va))


def print_info(ps_list):
    """Print all info."""
    if not isinstance(ps_list, (list, tuple)):
        ps_list = [ps_list, ]
    print('--- power supply status ---')
    print_status(ps_list)
    print_wfmref(ps_list)


def turn_on_opmode_slowref(ps_list):
    """."""
    if not isinstance(ps_list, (list, tuple)):
        ps_list = [ps_list, ]
    # turn ps on
    for psupply in ps_list:
        psupply.execute_function(0, timeout=100)

    # slowref
    for psupply in ps_list:
        psupply.execute_function(4, 3, timeout=100)


def turn_on_opmode_rmpwfm(ps_list):
    """."""
    if not isinstance(ps_list, (list, tuple)):
        ps_list = [ps_list, ]
    # turn ps on
    for psupply in ps_list:
        psupply.execute_function(0, timeout=100)

    # slowref
    for psupply in ps_list:
        psupply.execute_function(4, 6, timeout=100)


# --- set wfmref ---


def set_wfmref(ps_list, amplitude=0):
    """."""
    if not isinstance(ps_list, (list, tuple)):
        ps_list = [ps_list, ]
    curve = amplitude * np.sin([2*3.14159 * i/1023.0 for i in range(1024)])
    for i, psupply in enumerate(ps_list):
        psupply.wfmref_write((i+1) * curve)


def plot_wfmref(ps_list):
    """Plot wfmref."""
    if not isinstance(ps_list, (list, tuple)):
        ps_list = [ps_list, ]
    for i, psupply in enumerate(ps_list):
        curve = psupply.wfmref_read()
        plt.plot(curve, label='ps{} ({} points)'.format(i+1, len(curve)))
    plt.xlabel('Index')
    plt.ylabel('Current [A]')
    plt.legend()
    plt.show()


def reset_powersupplies(udc, ps_list, opmode='SlowRef'):
    """."""
    if not isinstance(ps_list, (list, tuple)):
        ps_list = [ps_list, ]
    # select opmode
    ps = ps_list[0]
    if opmode == 'SlowRef':
        opmode = ps.CONST_PSBSMP.E_STATE_SLOWREF
    elif opmode == 'RmpWfm':
        opmode = ps.CONST_PSBSMP.E_STATE_RMPWFM
    print('resetps - selected opmode: {}'.format(opmode))

    # reset UDC
    print('resetps - turn all ps off and reset udc')
    process_response(udc.reset())

    for ps in ps_list:
        # turn power supply on
        print('resetps - turn ps id:{} on'.format(ps.channel.address))
        ps.execute_function(
            func_id=ps.CONST_PSBSMP.F_TURN_ON,
            input_val=None,
            timeout=100)
        # change mode to RmpWfm
        ps.execute_function(
            func_id=ps.CONST_PSBSMP.F_SELECT_OP_MODE,
            input_val=opmode,
            timeout=100)
        time.sleep(0.010)  # needed?
    print()


def test_reset(udc, ps_list):
    """."""
    curve = [0.0 for i in range(500)]
    ps_list[0].wfmref_write(curve)
    print_basic_info(ps_list)
    udc.reset()
    print_basic_info(ps_list)


def test_reset_2019_10_02():
    udc = create_udc(BBBNAME, 1)
    ps_list = [udc[5], udc[6], udc[7]]
    test_reset(udc, ps_list)


def wfmref_flip(ps):
    id1 = ps.wfmref_select
    c1 = ps.wfmref_read()
    c_new = c1[::-1]
    # c_new = [i/1023 for i in range(1024)] # c_new[:500]
    # c_new = c1[:500]
    ps.wfmref_write(c_new)
    id2 = ps.wfmref_select
    c2 = ps.wfmref_read()
    plt.plot(c1, label='prev (id:{})'.format(id1))
    plt.plot(c2, label='next (id:{})'.format(id2))
    plt.legend()
    plt.show()


def test_wfmref_write_slowref():
    udc = create_udc('IA-08RaCtrl:CO-PSCtrl-SI5')
    all_ps = [udc[5], udc[6], udc[7]]
    ps5 = all_ps[0]
    reset_powersupplies(udc, all_ps, 'SlowRef')
    print_basic_info(all_ps)
    wfmref_flip(ps5)
    print_basic_info(all_ps)
    wfmref_flip(ps5)
    return udc, all_ps


def test_wfmref_write_rmpwfm():
    udc = create_udc('IA-08RaCtrl:CO-PSCtrl-SI5')
    all_ps = [udc[5], udc[6], udc[7]]
    ps5 = all_ps[0]
    reset_powersupplies(udc, all_ps, 'RmpWfm')
    print_basic_info(all_ps)
    wfmref_flip(ps5)
    print_basic_info(all_ps)
    wfmref_flip(ps5)
    return udc, all_ps

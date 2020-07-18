#!/usr/bin/env python-sirius
"""."""

import sys as _sys
import time as _time
from multiprocessing import Pipe
from copy import deepcopy as _dcopy

from epics import CAProcess

import numpy as _np
import matplotlib.pyplot as _plt
import matplotlib.gridspec as _mgs
from matplotlib import rcParams

import epics as _epics
from PRUserial485 import EthBrigdeClient

from siriuspy.pwrsupply.pssofb import PSSOFB


rcParams.update({
    'font.size': 14, 'lines.linewidth': 2, 'axes.grid': True})
NRPTS = 5000


def benchmark_bsmp_sofb_current_update():
    """."""
    pssofb = PSSOFB(EthBrigdeClient)
    exectimes = [0] * NRPTS
    for i, _ in enumerate(exectimes):
        time0 = _time.time()
        pssofb.bsmp_sofb_current_update()
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)
    for exectime in exectimes:
        print(exectime)

    exectimes = [0] * NRPTS
    for i, _ in enumerate(exectimes):

        # start clock
        time0 = _time.time()

        # read from power supplies
        pssofb.bsmp_sofb_current_update()

        # comparison
        issame = True

        # stop clock
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)

        if not issame:
            print('SP<>RB in event {}'.format(i))

    for exectime in exectimes:
        print(exectime)

    pssofb.stop_threads()


def _run_subprocess_pssofb(pipe, bbbnames):
    """."""
    PSSOFB.BBBNAMES = bbbnames
    pssofb = PSSOFB(EthBrigdeClient)
    pssofb.bsmp_slowref()

    pssofb.bsmp_sofb_update()
    curr_refmon = pssofb.sofb_current_refmon
    idcs = _np.sort(_np.hstack(list(pssofb.indcs_sofb.values())))
    pipe.send((idcs, curr_refmon[idcs]))

    while True:
        curr_sp = pipe.recv()
        if curr_sp is None:
            break

        # set kick values
        pssofb.bsmp_sofb_current_set(curr_sp)
        ref_curr = pssofb.sofb_current_readback_ref
        pipe.send(ref_curr[idcs])

    # restore state
    pssofb.bsmp_sofb_current_set(curr_refmon)

    # pssofb.stop_threads()


def benchmark_bsmp_sofb_current_setpoint_mp(fname='test'):
    """."""
    bbbnames = _dcopy(PSSOFB.BBBNAMES)
    pipes = list()
    procs = list()
    nprocs = 2
    slc_sz = int(len(bbbnames)/nprocs)
    for i in range(nprocs):
        slc = slice(slc_sz*i, slc_sz*(i+1))
        mine, theirs = Pipe()
        pipes.append(mine)
        proc = CAProcess(
            target=_run_subprocess_pssofb, args=(theirs, bbbnames[slc]),
            daemon=True)
        procs.append(proc)
        proc.start()

    indcs = list()
    curr_refmon = _np.zeros(280, dtype=float)
    for pipe in pipes:
        idcs, refmon = pipe.recv()
        indcs.append(idcs)
        curr_refmon[idcs] = refmon

    exectimes = [0] * NRPTS

    curr_sp_prev = None
    for i, _ in enumerate(exectimes):

        # start clock
        time0 = _time.time()

        # set current values
        curr_sp = curr_refmon + 1 * 0.01 * _np.random.randn(curr_refmon.size)
        for pipe in pipes:
            pipe.send(curr_sp)

        curr_read = _np.zeros(280, dtype=float)
        for pipe, idcs in zip(pipes, indcs):
            curr_read[idcs] = pipe.recv()

        # stop clock
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)

        # compare readback_ref read with previous value set
        if curr_sp_prev is not None:
            issame = PSSOFB.sofb_vector_issame(curr_read, curr_sp_prev)
        else:
            issame = True

        # update curr_sp_prev for comparison in the next iteration
        curr_sp_prev = curr_sp

        if not issame:
            print('SP<>RB in event {}'.format(i))

    for pipe in pipes:
        pipe.send(None)

    for proc in procs:
        proc.join()

    _np.savetxt(fname, exectimes)


def benchmark_bsmp_sofb_current_setpoint(fname='test'):
    """."""
    pssofb = PSSOFB(EthBrigdeClient)
    pssofb.bsmp_slowref()
    exectimes = [0] * NRPTS

    pssofb.bsmp_sofb_update()
    curr_refmon = pssofb.sofb_current_refmon

    curr_sp_prev = None
    for i, _ in enumerate(exectimes):

        # start clock
        time0 = _time.time()

        # set current values
        curr_sp = curr_refmon + 1 * 0.01 * _np.random.randn(curr_refmon.size)
        pssofb.bsmp_sofb_current_set(curr_sp)

        # stop clock
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)

        # compare readback_ref read with previous value set
        if curr_sp_prev is not None:
            curr_read = pssofb.sofb_current_readback_ref.copy()
            issame = pssofb.sofb_vector_issame(curr_read, curr_sp_prev)
        else:
            issame = True

        # update curr_sp_prev for comparison in the next iteration
        curr_sp_prev = curr_sp

        if not issame:
            print('SP<>RB in event {}'.format(i))

    # restore state
    pssofb.bsmp_sofb_current_set(curr_refmon)

    _np.savetxt(fname, exectimes)
    pssofb.stop_threads()


def benchmark_bsmp_sofb_current_setpoint_update():
    """."""
    pssofb = PSSOFB(EthBrigdeClient)
    exectimes = [0] * NRPTS
    curr_sp = 0.1 * _np.random.randn(280)
    for i, _ in enumerate(exectimes):

        # start clock
        time0 = _time.time()

        # set current values
        pssofb.bsmp_sofb_current_set_update(curr_sp)

        # read from power supplies
        curr_rb = pssofb.sofb_current_rb

        # comparison
        issame = pssofb.sofb_vector_issame(curr_sp, curr_rb)

        # stop clock
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)

        if not issame:
            print('SP<>RB in event {}'.format(i))

    for exectime in exectimes:
        print(exectime)

    pssofb.stop_threads()


def benchmark_bsmp_sofb_current_setpoint_then_update():
    """."""
    pssofb = PSSOFB(EthBrigdeClient)
    exectimes = [0] * NRPTS

    pssofb.bsmp_sofb_update()
    curr_refmon = pssofb.sofb_current_refmon

    for i, _ in enumerate(exectimes):

        # start clock
        time0 = _time.time()

        # set current values
        curr_sp = curr_refmon + 1 * 0.005 * _np.random.randn(len(curr_refmon))
        pssofb.bsmp_sofb_current_set(curr_sp)

        # read from power supplies
        pssofb.bsmp_sofb_update()
        curr_rb = pssofb.sofb_current_rb

        # comparison
        issame = pssofb.sofb_vector_issame(curr_sp, curr_rb)

        # stop clock
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)

        if not issame:
            print('SP<>RB in event {}'.format(i))

    # restore state
    pssofb.bsmp_sofb_current_set(curr_refmon)

    for exectime in exectimes:
        print(exectime)

    pssofb.stop_threads()


def benchmark_bsmp_sofb_kick_setpoint(fname='test'):
    """."""
    pssofb = PSSOFB(EthBrigdeClient)
    pssofb.bsmp_slowref()
    exectimes = [0] * NRPTS

    pssofb.bsmp_sofb_update()
    kick_refmon = pssofb.sofb_kick_refmon

    curr_sp_prev = None
    for i, _ in enumerate(exectimes):

        # print(i)
        # start clock
        time0 = _time.time()

        # set kick values
        kick_sp = kick_refmon + 0 * 0.01 * _np.random.randn(len(kick_refmon))
        curr_sp_this = pssofb.bsmp_sofb_kick_set(kick_sp)

        # stop clock
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)

        # NOTE:
        # curr_sp_this is kick_sp converted to current units. It should be
        # used for comparisons instead of kick_sp, since the mapping
        # (kick -> current -> kick) is not exactly bijective.

        # compare readback_ref read with previous value set
        if curr_sp_prev is not None:
            curr_read = pssofb.sofb_current_readback_ref.copy()
            issame = pssofb.sofb_vector_issame(curr_read, curr_sp_prev)
        else:
            issame = True

        # update curr_sp_prev for comparison in the next iteration
        curr_sp_prev = curr_sp_this

        if not issame:
            print('SP<>RB in event {}'.format(i))

    # restore state
    pssofb.bsmp_sofb_kick_set(kick_refmon)

    _np.savetxt(fname, exectimes)
    pssofb.stop_threads()


def benchmark_bsmp_sofb_kick_setpoint_then_update():
    """."""
    pssofb = PSSOFB(EthBrigdeClient)
    pssofb.bsmp_slowref()
    exectimes = [0] * NRPTS

    pssofb.bsmp_sofb_update()
    kick_refmon = pssofb.sofb_kick_refmon.copy()

    for i, _ in enumerate(exectimes):

        # start clock
        time0 = _time.time()

        # set kick values
        kick_sp = kick_refmon + 0 * 0.01 * _np.random.randn(len(kick_refmon))
        curr_sp = pssofb.bsmp_sofb_kick_set(kick_sp)

        # read from power supplies
        pssofb.bsmp_sofb_update()
        curr_rb = pssofb.sofb_current_rb

        # comparison
        issame = pssofb.sofb_vector_issame(curr_sp, curr_rb)

        # stop clock
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)

        if not issame:
            print('SP<>RB in event {}'.format(i))

    # restore state
    pssofb.bsmp_sofb_kick_set(kick_refmon)

    for exectime in exectimes:
        print(exectime)

    pssofb.stop_threads()


def benchmark_bsmp_sofb_kick_setpoint_delay(delay_before, delay_after):
    """."""
    trigger = _epics.PV('AS-RaMO:TI-EVG:OrbSIExtTrig-Cmd')
    trigger.wait_for_connection()

    pssofb = PSSOFB(EthBrigdeClient)
    pssofb.bsmp_slowrefsync()

    exectimes = [0] * 150

    pssofb.bsmp_sofb_update()
    kick_refmon = pssofb.sofb_kick_refmon

    for i, _ in enumerate(exectimes):

        # calc new kick
        kick_sp = kick_refmon + 1 * 0.01 * _np.random.randn(len(kick_refmon))

        # start clock
        time0 = _time.time()

        # set kick values
        curr_sp = pssofb.bsmp_sofb_kick_set(kick_sp)

        # sleep for a while
        _time.sleep(delay_before)

        # send trigger
        trigger.value = 1

        # stop clock
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)

        # make sure trigger signal gets to power supplies.
        _time.sleep(delay_after)

        # read from power supplies
        pssofb.bsmp_sofb_update()
        curr_rb = pssofb.sofb_current_refmon

        # comparison
        issame = pssofb.sofb_vector_issame(curr_sp, curr_rb)

        if not issame:
            print('SP<>RB in event {}'.format(i))

    # restore state
    pssofb.bsmp_sofb_kick_set(kick_refmon)

    for exectime in exectimes:
        print(exectime)

    pssofb.stop_threads()


def bsmp_communication_test():
    """."""
    pssofb = PSSOFB(EthBrigdeClient)
    time0 = _time.time()
    pssofb.bsmp_state_update()
    time1 = _time.time()
    print(1e3*(time1 - time0))

    print('--- hard interlock ---')
    print(pssofb.sofb_interlock_hard)

    print('--- soft interlock ---')
    print(pssofb.sofb_interlock_soft)

    print('--- current_mon ---')
    print(pssofb.sofb_state_variable_get(var_id=26))

    return pssofb


def plot_results(fname, title):
    """."""
    data = _np.loadtxt(fname)
    avg = data.mean()
    std = data.std()
    minv = data.min()
    maxv = data.max()

    fig = _plt.figure(figsize=(7, 8))
    gs = _mgs.GridSpec(3, 1)
    gs.update(
        left=0.12, right=0.97, top=0.95, bottom=0.08,
        hspace=0.3, wspace=0.25)
    adt = _plt.subplot(gs[0, 0])
    asp = _plt.subplot(gs[1, 0])
    apc = _plt.subplot(gs[2, 0], sharex=asp)

    fig.suptitle(title)

    adt.plot(data, '.')
    adt.set_xlabel('apply index')
    adt.set_ylabel('Time [ms]')
    adt.grid(True)

    dist, bins, _ = asp.hist(data, bins=max(int(maxv/1), 50))
    asp.set_xlabel('Execution time [ms]')
    asp.set_ylabel('# total apply')
    asp.grid(True)

    bins += (bins[1]-bins[0])/2
    perc = _np.cumsum(dist, )
    perc *= 100/perc[-1]
    apc.plot(bins[:-1], perc)
    apc.set_xlabel('Execution time [ms]')
    apc.set_ylabel('Int. distribution [%]')
    apc.grid(True)

    stg = f'avg = {avg:05.1f} ms\n'
    stg += f'std = {std:05.1f} ms\n'
    stg += f'min = {minv:05.1f} ms\n'
    stg += f'max = {maxv:05.1f} ms'
    apc.text(
        0.98, 0.05, stg, horizontalalignment='right',
        fontsize='x-small',
        verticalalignment='bottom', transform=apc.transAxes,
        bbox=dict(edgecolor='k', facecolor='w', alpha=1.0))

    fig.savefig(title + '.png')

    _plt.show()


def run():
    """."""
    fname = 'test.txt'

    # benchmark_bsmp_sofb_current_update()
    # benchmark_bsmp_sofb_current_setpoint(fname)
    benchmark_bsmp_sofb_current_setpoint_mp(fname)
    # benchmark_bsmp_sofb_current_setpoint_update()
    # benchmark_bsmp_sofb_current_setpoint_then_update()

    # benchmark_bsmp_sofb_kick_setpoint()
    # benchmark_bsmp_sofb_kick_setpoint_then_update()
    # sleep_trigger_before = float(_sys.argv[1])
    # sleep_trigger_after = float(_sys.argv[2])
    # benchmark_bsmp_sofb_kick_setpoint_delay(
    #     sleep_trigger_before, sleep_trigger_after)
    # test_methods()
    plot_results(fname, fname.split('.')[0])


if __name__ == '__main__':
    run()

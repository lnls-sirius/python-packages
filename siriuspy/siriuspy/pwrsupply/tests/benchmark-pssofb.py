#!/usr/bin/env python-sirius
"""."""

import time
import numpy as np


TINY_CURRENT = (1e-3/400)*10


def benchmark(pssofb, print_flag=False):
    """."""
    value = pssofb.current
    setpoint = np.random.randint(0, 100, len(value))/1000
    pssofb.current = setpoint
    t0_ = time.time()
    while not np.allclose(pssofb.current, setpoint, TINY_CURRENT):
        pass
    t1_ = time.time()
    dt_ = 1e3*(t1_ - t0_)
    if print_flag:
        print('elapsed time: {:.3f} ms'.format(dt_))
    return dt_


def benchmark_kick(pssofb, print_flag=False):
    """."""
    value = pssofb.kick
    setpoint = np.random.randint(0, 10, len(value))
    t0_ = time.time()
    pssofb.kick = setpoint
    while not np.allclose(pssofb.kick, setpoint, TINY_CURRENT):
        pass
    t1_ = time.time()
    dt_ = 1e3*(t1_ - t0_)
    if print_flag:
        print('elapsed time: {:.3f} ms'.format(dt_))
    return dt_


def benchmark_kick_init(pssofb, kick0, print_flag=False):
    """."""
    setpoint = kick0 + 0 * 0.01 * np.random.randn(len(kick0))
    t0_ = time.time()
    pssofb.kick = setpoint
    while not np.allclose(pssofb.kick, setpoint, TINY_CURRENT):
        pass
    t1_ = time.time()
    dt_ = 1e3*(t1_ - t0_)
    if print_flag:
        print('elapsed time: {:.3f} ms'.format(dt_))
    return dt_


def turn_on_pwrsupplies(psnames):
    """."""
    from siriuspy.devices import PowerSupply

    psupplies = [PowerSupply(psname) for psname in psnames]

    # set slowref
    print('--- psupplies slowref')
    for psupply in psupplies:
        print('psupply slowref: ', psupply.devname)
        psupply.cmd_slowref()
    time.sleep(1.0)
    for psupply in psupplies:
        while not psupply.connected:
            time.sleep(0.1)
        print('{} : {}'.format(psupply.devname, psupply.opmode))

    # turn power supplies on
    print('--- psupplies on')
    for psupply in psupplies:
        print('psupply on: ', psupply.devname)
        psupply.cmd_turn_on()
    time.sleep(1.0)
    for psupply in psupplies:
        print('{} : {}'.format(psupply.devname, psupply.pwrstate))


def turn_on_pwrsupplies_all(acc):
    """."""
    from siriuspy.devices import PSApplySOFB

    pssofb = PSApplySOFB(acc, auto_mon=True)
    pssofb.wait_for_connection()

    # configure power supplies
    psnames = pssofb.psnames_ch + pssofb.psnames_cv
    turn_on_pwrsupplies(psnames)


def turn_off_pwrsupplies(psnames):
    """."""

    from siriuspy.devices import PowerSupply

    psupplies = [PowerSupply(psname) for psname in psnames]

    # turn power supplies off
    print('--- psupplies off')
    for psupply in psupplies:
        psupply.cmd_turn_off()


def test_pscorrsofb(acc, psnames=None, save_flag=False):
    """."""
    from siriuspy.devices import PSCorrSOFB
    import matplotlib.pyplot as plt

    if psnames is None:
        if acc == 'SI':
            psnames = (
                'SI-01M1:PS-CH',
                'SI-01M1:PS-CV',
                'SI-01M2:PS-CH',
                'SI-01M2:PS-CV',
                'SI-01C2:PS-CH',
                'SI-01C2:PS-CV-1',
                'SI-01C2:PS-CV-2',
                )
        if acc == 'BO':
            psnames = (
                'BO-03U:PS-CH',
                'BO-03U:PS-CV',
                'BO-05U:PS-CH',
                'BO-05U:PS-CV',
                )

    # prepare power supplies
    turn_on_pwrsupplies(psnames)

    # wait for connection
    print('--- create device and wait for connection')
    pssofb = PSCorrSOFB(psnames[0])
    while not pssofb.connected:
        time.sleep(0.1)

    # check why PVs are connected but values are being returned None
    time.sleep(1.0)

    # neglect first setppoint in stats
    for _ in range(10):
        benchmark(pssofb, print_flag=False)

    # do benchmark
    stats = list()
    for _ in range(5000):
        stats.append(benchmark(pssofb, print_flag=True))
    stats = np.array(stats)

    # turn power supplies off
    # turn_off_pwrsupplies(psnames)

    print('--- benchmarks ---')
    print('avg: {:08.3f} ms'.format(np.mean(stats)))
    print('std: {:08.3f} ms'.format(np.std(stats)))
    print('min: {:08.3f} ms'.format(np.min(stats)))
    print('max: {:08.3f} ms'.format(np.max(stats)))

    plt.hist(stats, 100, log=True)
    plt.title(
        psnames[0] + ' - SOFB setpoint ({} operations)'.format(len(stats)))
    plt.xlabel('Execution time [ms]')
    plt.ylabel('Number of realizations')
    if save_flag:
        fname = psnames[0].replace(':', '--') + '.png'
        plt.savefig(fname)
    else:
        plt.show()

    plt.plot(stats)
    plt.title(
        psnames[0] + ' - SOFB setpoint ({} operations)'.format(len(stats)))
    plt.xlabel('Measuremunt Index')
    plt.ylabel('Execution time [ms]')
    if save_flag:
        fname = 'time_' + psnames[0].replace(':', '--') + '.png'
        plt.savefig(fname)
    else:
        plt.show()


def test_pscorrsofb_all(acc):
    """."""
    from siriuspy.devices import PSCorrSOFB
    from siriuspy.devices import PSApplySOFB

    pssofb = PSApplySOFB(PSApplySOFB.DEVICES.SI, auto_mon=True)

    psnames = dict()
    for dev in pssofb.devices:
        if isinstance(dev, PSCorrSOFB):
            psn = [v[0] for v in dev.bsmpdevs]
            psnames[dev.devname] = psn
    del pssofb

    for psn in psnames.values():
        print(psn)
        test_pscorrsofb(acc, psn, True)
        print()


def test_si_psapplysofb(fname=None):
    """."""
    from siriuspy.devices import PSApplySOFB
    import matplotlib.pyplot as plt

    pssofb = PSApplySOFB(PSApplySOFB.DEVICES.SI, auto_mon=True)
    pssofb.wait_for_connection()

    # check why PVs are connected but values are being returned None
    time.sleep(1.0)

    # neglect first setppoint in stats
    for _ in range(10):
        benchmark_kick(pssofb, print_flag=False)

    # do benchmark
    stats = list()
    for _ in range(5000):
        # stats.append(benchmark(pssofb, print_flag=True))
        stats.append(benchmark_kick(pssofb, print_flag=True))
    stats = np.array(stats)

    # # turn power supplies off
    # turn_off_pwrsupplies(psnames)

    print('--- benchmarks ---')
    print('avg: {:08.3f} ms'.format(np.mean(stats)))
    print('std: {:08.3f} ms'.format(np.std(stats)))
    print('min: {:08.3f} ms'.format(np.min(stats)))
    print('max: {:08.3f} ms'.format(np.max(stats)))

    plt.hist(stats, 100, log=True)
    plt.title('SOFB setpoint ({} operations)'.format(len(stats)))
    plt.xlabel('Excetution time [ms]')
    plt.ylabel('Number of realizations')
    if fname:
        plt.savefig(fname)
    plt.show()

    plt.plot(stats)
    plt.title('SOFB setpoint ({} operations)'.format(len(stats)))
    plt.ylabel('Measurement Index')
    plt.ylabel('Excetution time [ms]')
    if fname:
        plt.savefig('time_' + fname)
    plt.show()


def test_si_psapplysofb_init(fname=None):
    """."""
    from siriuspy.devices import PSApplySOFB
    import matplotlib.pyplot as plt

    pssofb = PSApplySOFB(PSApplySOFB.DEVICES.SI, auto_mon=True)
    pssofb.wait_for_connection()

    # check why PVs are connected but values are being returned None
    time.sleep(1.0)

    # get original kick
    kick0 = pssofb.kick

    print(kick0)
    return

    # neglect first setppoint in stats
    for _ in range(10):
        benchmark_kick_init(pssofb, kick0, print_flag=False)

    # do benchmark
    stats = list()
    for _ in range(5000):
        # stats.append(benchmark(pssofb, print_flag=True))
        timeexec = benchmark_kick_init(pssofb, kick0, print_flag=True)
        stats.append(timeexec)
    stats = np.array(stats)

    # restore original kick
    pssofb.kick = kick0

    # # turn power supplies off
    # turn_off_pwrsupplies(psnames)

    print('--- benchmarks ---')
    print('avg: {:08.3f} ms'.format(np.mean(stats)))
    print('std: {:08.3f} ms'.format(np.std(stats)))
    print('min: {:08.3f} ms'.format(np.min(stats)))
    print('max: {:08.3f} ms'.format(np.max(stats)))

    plt.hist(stats, 100, log=True)
    plt.title('SOFB setpoint ({} operations)'.format(len(stats)))
    plt.xlabel('Excetution time [ms]')
    plt.ylabel('Number of realizations')
    if fname:
        plt.savefig(fname)
    plt.show()

    plt.plot(stats)
    plt.title('SOFB setpoint ({} operations)'.format(len(stats)))
    plt.ylabel('Measurement Index')
    plt.ylabel('Excetution time [ms]')
    if fname:
        plt.savefig('time_' + fname)
    plt.show()


def test_si_psapplysofb_order():
    """."""
    import numpy as np
    from siriuspy.devices import PSApplySOFB

    pssofb = PSApplySOFB('SI')
    pssofb.wait_for_connection()

    indices = []
    psnames = []
    for i in range(40):
        """."""
        corrs = pssofb[i]
        indcs = corrs.sofb_indices
        for i, dev in enumerate(corrs.bsmpdevs):
            psname, bsmpid = dev
            indices.append(indcs[i])
            psnames.append(psname)
    indices = np.array(indices)
    psnames = np.array(psnames)

    sindcs = np.argsort(indices)
    indices = indices[sindcs]
    psnames = psnames[sindcs]

    for i in range(len(indices)):
        print('{1:<20s} {0:03d}'.format(indices[i], psnames[i]))


# test_pscorrsofb('BO')
# test_pscorrsofb('SI', save_flag=False)
# test_pscorrsofb_all('SI')
# turn_on_pwrsupplies_all('SI')
test_si_psapplysofb_init('sofb-include-setpoint.png')
# test_si_psapplysofb_order()

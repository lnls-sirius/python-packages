#!/usr/bin/env python-sirius

import os
os.environ['OMP_NUM_THREADS'] = '2'

import time
import numpy as np
from threading import Event
import signal

from siriuspy.sofb.orbit import EpicsOrbit


def calc_values(value):
    return dict(
        ave=value.mean(),
        maxi=value.max(),
        mini=value.min(),
        std=value.std())


def shutdown(signum, frame):
    global evt
    evt.set()


evt = Event()
signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

print('creating orbit object...')
orbit = EpicsOrbit('SI')
orbit.set_orbit_acq_rate(30)
time.sleep(15)
print('setting SlowOrb mode...')
orbit.set_orbit_mode(orbit._csorb.SOFBMode.SlowOrb)
time.sleep(5)

print('starting acquisition')
tmpl = '{ave:18.9f} {std:18.9f} {maxi:18.9f} {mini:18.9f}\n'
cnt = 0
orbs = []
while not evt.is_set():
    t0 = time.time()
    orbs.append(orbit.get_orbit(synced=True))
    cnt += 1
    print(f'dt = {(time.time()-t0)*1000:.2f} ms')
    if cnt > 40 * 25:
        break

np.savetxt('orb.txt', orbs)

orbit.shutdown()

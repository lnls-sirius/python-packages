#!/usr/bin/env python-sirius

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

tmpl = '{:^18s} '*4 + '\n'
with open('orbx.txt', 'w') as fil:
    fil.write(tmpl.format('# avg', 'std', 'max', 'min'))

with open('orby.txt', 'w') as fil:
    fil.write(tmpl.format('# avg', 'std', 'max', 'min'))

print('creating orbit object...')
orbit = EpicsOrbit('SI')
time.sleep(10)
print('setting SlowOrb mode...')
orbit.set_orbit_mode(orbit._csorb.SOFBMode.SlowOrb)
time.sleep(5)

print('starting acquisition')
tmpl = '{ave:18.9f} {std:18.9f} {maxi:18.9f} {mini:18.9f}\n'
while not evt.wait(timeout=10e-3):
    orb = orbit.get_orbit(synced=True)
    datax = calc_values(orb[:160])
    datay = calc_values(orb[160:])
    with open('orbx.txt', 'w') as fil:
        fil.write(tmpl.format(**datax))
    with open('orby.txt', 'w') as fil:
        fil.write(tmpl.format(**datay))

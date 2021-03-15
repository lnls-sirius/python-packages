"""BeagleBone class."""

# NOTE on current behaviour of BeagleBone:
#
# 01. While in RmpWfm, MigWfm or SlowRefSync, the PS_I_LOAD variable read from
#     power supplies after setting the last curve point may not be the
#     final value given by PS_REFERENCE. This is due to the fact that the
#     power supply control loop takes some time to converge and the PRU may
#     block serial comm. before it. This is evident in SlowRefSync mode, where
#     reference values may change considerably between two setpoints.
#     (see identical note in PRUController)
#
# 02. Now that SOFB controls correctors power supplies directly, the
#     'priority_pvs' mechanism for updating SOFBCurrent-* PVs may be dropped.

import time as _time

from ..devices import StrengthConv as _StrengthConv


class BeagleBone:
    """BeagleBone class.

    Through objects of this class power supply controllers can be accessed
    in order to redirect read, write connected requests to the
    aproppriate device.
    """

    def __init__(self, controllers, databases):
        """Init object.

        Parameters:
        controllers : list of PSController objectsused to communicate with
                      BSMP devices.
        databases   : corresponding controllers databases.

        """
        # ps controllers.
        self._controllers = controllers

        # ps cpntrollers databases
        self._databases = databases

        # psnames
        self._psnames = tuple(self._controllers.keys())

        # strength property names
        self._strenames = self._get_strength_names()

        # create devname to scan interval dict
        self._create_dev2interval_dict()

        # init mirror variables and last update timestamp dicts
        self._create_dev2mirr_dev2timestamp_dict()

        # create strength conv epics objects
        self._streconv, self._streconnected, self._strelims = \
            self._create_streconvs()

        # initialized state
        self._initialized = False

    @property
    def controllers(self):
        """Return beaglebone power supply controllers."""
        return self._controllers

    @property
    def psnames(self):
        """PS names."""
        return self._psnames

    def update_interval(self, devname=None):
        """Update interval, as defined in PRUcontrollers."""
        if devname is not None:
            return self._dev2interval[devname]
        intervals = tuple(self._dev2interval.values())
        return min(intervals)

    def read(self, devname, field=None, force_update=False):
        """Read from device."""
        # if not initialized, return None
        if not self._initialized:
            return None, False

        now = _time.time()
        last = self._dev2timestamp[devname]

        # NOTE: update frequency with which class updates state mirror of
        # power supply.
        interval = self._dev2interval[devname]

        # reads, if updating is needed
        if force_update or last is None or now - last > interval:
            updated = True
            self._dev2mirror[devname] = \
                self._controllers[devname].read_all_fields(devname)
            self._update_strengths(devname)
            self._dev2timestamp[devname] = now
        else:
            updated = False

        if field is None:
            return self._dev2mirror[devname], updated
        else:
            pvname = devname + ':' + field
            return self._dev2mirror[devname][pvname], updated

    def write(self, devname, field, value):
        """Write value to a device field.

        Return pvname-value dictionary of priority PVs.
        """
        # if not initialized, return None
        if not self._initialized:
            return None

        if field in {'Energy-SP', 'Kick-SP', 'KL-SP', 'SL-SP'}:
            streconv = self._streconv[devname]
            curr = streconv.conv_strength_2_current(value)
            priority_pvs = self._controllers[devname].write(
                devname, 'Current-SP', curr)
        else:
            priority_pvs = self._controllers[devname].write(
                devname, field, value)
        return priority_pvs

    def get_strength_limits(self, devname):
        """Return strength lower and upper limits."""
        return self._strelims[devname]

    def check_connected(self, devname):
        """Check wether device is connected."""
        return self._controllers[devname].check_connected(devname)

    def check_connected_strength(self, devname):
        """Check connection with PVs for strength calc."""
        return self._streconnected[devname]

    def strength_name(self, devname):
        """Return strength name."""
        return self._strenames[devname]

    def strength_limits(self, devname):
        """Return strength limits."""
        return self._strelims[devname]

    def database(self, devname):
        """Return device database."""
        return self._databases[devname]

    def init(self):
        """Initialize controllers."""
        # return  # allow for IOC initialization without HW comm.

        # initialize controller communication and setpoint fields
        pruc_initialized = set()
        psc_initialized = set()
        for controller in self._controllers.values():
            pruc = controller.pru_controller
            if pruc not in pruc_initialized:
                pruc.bsmp_init_communication()
                pruc.processing = True
                pruc.scanning = True
                pruc_initialized.add(pruc)
            if controller not in psc_initialized:
                controller.init_setpoints()
                psc_initialized.add(controller)
        self._initialized = True

    # --- private methods ---

    def _get_strength_names(self):
        strenames = dict()
        for psname, dbase in self._databases.items():
            if 'Energy-SP' in dbase:
                strenames[psname] = 'Energy'
            elif 'Kick-SP' in dbase:
                strenames[psname] = 'Kick'
            elif 'KL-SP' in dbase:
                strenames[psname] = 'KL'
            elif 'SL-SP' in dbase:
                strenames[psname] = 'SL'
            else:
                strenames[psname] = None
        return strenames

    def _create_dev2mirr_dev2timestamp_dict(self):
        self._dev2timestamp = dict()
        self._dev2mirror = dict()
        for devname in self._controllers:
            self._dev2timestamp[devname] = None
            self._dev2mirror[devname] = dict()

    def _create_dev2interval_dict(self):
        self._dev2interval = dict()
        for devname, controller in self._controllers.items():
            pruc = controller.pru_controller
            self._dev2interval[devname] = 1.0/pruc.params.FREQ_SCAN

    def _create_streconvs(self):
        streconvs = dict()
        strec = dict()
        strelims = dict()
        for psname in self.psnames:
            if 'DCLink' in psname:
                strec[psname] = True
            else:
                # NOTE: use 'Ref-Mon' proptype for all
                strec[psname] = False
                streconvs[psname] = _StrengthConv(psname, 'Ref-Mon')
                strelims[psname] = [None, None]
        return streconvs, strec, strelims

    def _update_strengths(self, psname):
        # t0_ = _time.time()
        if 'DCLink' in psname:
            return
        streconv = self._streconv[psname]
        strelims = self._strelims[psname]
        mirror = self._dev2mirror[psname]
        dbase = self._databases[psname]
        curr0 = mirror[psname + ':Current-SP']
        curr1 = mirror[psname + ':Current-RB']
        curr2 = mirror[psname + ':CurrentRef-Mon']
        curr3 = mirror[psname + ':Current-Mon']
        curr4 = dbase['Current-SP']['lolo']
        curr5 = dbase['Current-SP']['hihi']
        currs = (curr0, curr1, curr2, curr3, curr4, curr5)
        strengths = streconv.conv_current_2_strength(currents=currs)
        if strengths is None or None in strengths:
            self._streconnected[psname] = False
        else:
            self._streconnected[psname] = True
            propname = psname + ':' + self._strenames[psname]
            mirror[propname + '-SP'] = strengths[0]
            mirror[propname + '-RB'] = strengths[1]
            mirror[propname + 'Ref-Mon'] = strengths[2]
            mirror[propname + '-Mon'] = strengths[3]
            # update strength limits
            if strengths[4] <= strengths[5]:
                strelims[0], strelims[1] = strengths[4], strengths[5]
            else:
                strelims[0], strelims[1] = strengths[5], strengths[4]
        # t1_ = _time.time()
        # print('update_strengths: {:.3f}'.format(1000*(t1_-t0_)))

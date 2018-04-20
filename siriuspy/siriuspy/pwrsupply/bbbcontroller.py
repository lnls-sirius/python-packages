"""BeagleBone Controller.

This module implements classes that are used to do low level BeagleBone
communications, be it with PRU or BSMP requests to power supply controllers
at the other end of the serial line.
"""

import time as _time
import math as _math
from collections import deque as _deque
from collections import namedtuple as _namedtuple
from threading import Thread as _Thread
from threading import Lock as _Lock
from copy import deepcopy as _dcopy


from siriuspy.bsmp import BSMP
from siriuspy.bsmp import Response
from siriuspy.pwrsupply.pru import PRUInterface as _PRUInterface
from siriuspy.pwrsupply.pru import PRU
from siriuspy.pwrsupply.bsmp import Const as _c
from siriuspy.pwrsupply.bsmp import MAP_MIRROR_2_ORIG as _mirror_map


class BSMPOpQueue(_deque):
    """BSMPOpQueue.

    This class takes manages operations which invoque BSMP communications using
    an append-right, pop-left queue. It also processes the next operation in a
    way as to circumvent the blocking character of UART writes when PRU sync
    mode is on.
    """

    _lock = _Lock()

    def __init__(self):
        """Init."""
        self._thread = None
        self._ignore = False

    @property
    def last_operation(self):
        """Return last operation."""
        return self._last_operation

    def ignore_set(self):
        """Turn ignore state on."""
        self._ignore = True

    def ignore_clear(self):
        """Turn ignore state on."""
        self._ignore = False

    def append(self, operation, unique=False):
        """Append operation to queue."""
        BSMPOpQueue._lock.acquire(blocking=True)
        if not self._ignore:
            if not unique:
                super().append(operation)
                self._last_operation = operation
            else:
                # super().append(operation)
                # self._last_operation = operation
                n = self.count(operation)
                if n == 0:
                    super().append(operation)
                    self._last_operation = operation
        BSMPOpQueue._lock.release()

    def clear(self):
        """Clear deque."""
        self._lock.acquire()
        super().clear()
        self._lock.release()

    def popleft(self):
        """Pop left operation from queue."""
        BSMPOpQueue._lock.acquire(blocking=True)
        if super().__len__() > 0:
            value = super().popleft()
        else:
            value = None
        BSMPOpQueue._lock.release()
        return value

    def process(self):
        """Process operation from queue."""
        # first check if a thread is already running
        if self._thread is None or not self._thread.is_alive():
            # no thread is running, we can process queue
            operation = self.popleft()
            if operation is None:
                # nothing in queue
                return False
            else:
                # process operation take from queue
                func, args = operation
                self._thread = _Thread(target=func, args=args, daemon=True)
                self._thread.start()
                return True
        else:
            return False


class BBBController:
    """BeagleBone controller.

    This class implements all basic PRU configuration and BSMP communications
    of the BeagleBone computer connected through a serial line to power supply
    controllers.
    """

    # TODO: make class robust to BSMP errors!!!
    # TODO: test class in sync on mode and trigger from timing
    # TODO: implement BSMP function executions

    # TODO: Improve update frequency in WfmRamp/MigRamp
    #
    # Gabriel from ELP proposed the idea of a privilegded slave that
    # could define BSMP variables that corresponded to other slaves variables
    # By defining a BSMP variable group with selected variables from all
    # devices we could update all device states with a single BSMP request
    # thus providing higher refresh rates.

    # TODO: check if these measured times are not artifact of python!

    # frequency constants
    FREQ = _namedtuple('FREQ', '')
    FREQ.RAMP = 2.0  # [Hz]
    FREQ.SCAN = 10.0  # [Hz]

    # PRU constants
    SYNC = _namedtuple('SYNC', '')
    SYNC.OFF = _PRUInterface._SYNC_OFF
    SYNC.ON = _PRUInterface._SYNC_ON
    SYNC.MIGINT = _PRUInterface.SYNC_MIGINT
    SYNC.MIGEND = _PRUInterface.SYNC_MIGEND
    SYNC.RMPINT = _PRUInterface.SYNC_RMPINT
    SYNC.RMPEND = _PRUInterface.SYNC_RMPEND
    SYNC.CYCLE = _PRUInterface.SYNC_CYCLE

    _groups = dict()

    # predefined variable groups

    # reserved group with ids of all device variable
    _groups[0] = (
        # --- common variables
        _c.V_PS_STATUS,
        _c.V_PS_SETPOINT,
        _c.V_PS_REFERENCE,
        _c.V_FIRMWARE_VERSION,
        _c.V_COUNTER_SET_SLOWREF,
        _c.V_COUNTER_SYNC_PULSE,
        _c.V_SIGGEN_ENABLE,
        _c.V_SIGGEN_TYPE,
        _c.V_SIGGEN_NUM_CYCLES,
        _c.V_SIGGEN_N,
        _c.V_SIGGEN_FREQ,
        _c.V_SIGGEN_AMPLITUDE,
        _c.V_SIGGEN_OFFSET,
        _c.V_SIGGEN_AUX_PARAM,
        # --- undefined variables
        _c.V_UNDEF14,
        _c.V_UNDEF15,
        _c.V_UNDEF16,
        _c.V_UNDEF17,
        _c.V_UNDEF18,
        _c.V_UNDEF19,
        _c.V_UNDEF20,
        _c.V_UNDEF21,
        _c.V_UNDEF22,
        _c.V_UNDEF23,
        _c.V_UNDEF24,
        # --- FSB variables ---
        _c.V_PS_SOFT_INTERLOCKS,
        _c.V_PS_HARD_INTERLOCKS,
        _c.V_I_LOAD,
        _c.V_V_LOAD,
        _c.V_V_DCLINK,
        _c.V_TEMP_SWITCHES,
        _c.V_DUTY_CYCLE,
        # --- undefined variables
        _c.V_UNDEF32,
        _c.V_UNDEF33,
        _c.V_UNDEF34,
        _c.V_UNDEF35,
        _c.V_UNDEF36,
        _c.V_UNDEF37,
        _c.V_UNDEF38,
        _c.V_UNDEF39,
        # --- mirror variables ---
        _c.V_PS_STATUS_1,
        _c.V_PS_STATUS_2,
        _c.V_PS_STATUS_3,
        _c.V_PS_STATUS_4,
        _c.V_PS_SETPOINT_1,
        _c.V_PS_SETPOINT_2,
        _c.V_PS_SETPOINT_3,
        _c.V_PS_SETPOINT_4,
        _c.V_PS_REFERENCE_1,
        _c.V_PS_REFERENCE_2,
        _c.V_PS_REFERENCE_3,
        _c.V_PS_REFERENCE_4,
        _c.V_PS_SOFT_INTERLOCKS_1,
        _c.V_PS_SOFT_INTERLOCKS_2,
        _c.V_PS_SOFT_INTERLOCKS_3,
        _c.V_PS_SOFT_INTERLOCKS_4,
        _c.V_PS_HARD_INTERLOCKS_1,
        _c.V_PS_HARD_INTERLOCKS_2,
        _c.V_PS_HARD_INTERLOCKS_3,
        _c.V_PS_HARD_INTERLOCKS_4,
        _c.V_I_LOAD_1,
        _c.V_I_LOAD_2,
        _c.V_I_LOAD_3,
        _c.V_I_LOAD_4,)
    # reserved group with ids of all read-only device variables
    _groups[1] = _groups[0]
    # reserved group with ids of all writebale device variables
    _groups[2] = tuple()
    # new group with all relevante device variables
    _groups[3] = (
        # --- common variables
        _c.V_PS_STATUS,
        _c.V_PS_SETPOINT,
        _c.V_PS_REFERENCE,
        _c.V_FIRMWARE_VERSION,
        _c.V_COUNTER_SET_SLOWREF,
        _c.V_COUNTER_SYNC_PULSE,
        _c.V_SIGGEN_ENABLE,
        _c.V_SIGGEN_TYPE,
        _c.V_SIGGEN_NUM_CYCLES,
        _c.V_SIGGEN_N,
        _c.V_SIGGEN_FREQ,
        _c.V_SIGGEN_AMPLITUDE,
        _c.V_SIGGEN_OFFSET,
        _c.V_SIGGEN_AUX_PARAM,
        # --- FSB variables ---
        _c.V_PS_SOFT_INTERLOCKS,
        _c.V_PS_HARD_INTERLOCKS,
        _c.V_I_LOAD,
        _c.V_V_LOAD,
        _c.V_V_DCLINK,
        _c.V_TEMP_SWITCHES,
        _c.V_DUTY_CYCLE,)
    _groups[4] = (
        # =======================================================
        # cmd exec_funcion read_group:
        #   17.2 ± 0.3 ms @ BBB1, 4 ps as measured from Python
        #   180us @ BBB1, 1 ps as measured in the oscilloscope
        # =======================================================
        # --- common variables
        _c.V_PS_STATUS,
        _c.V_PS_SETPOINT,
        _c.V_PS_REFERENCE,
        _c.V_COUNTER_SET_SLOWREF,
        _c.V_COUNTER_SYNC_PULSE,
        _c.V_SIGGEN_ENABLE,
        _c.V_SIGGEN_TYPE,
        _c.V_SIGGEN_NUM_CYCLES,
        _c.V_SIGGEN_N,
        _c.V_SIGGEN_FREQ,
        _c.V_SIGGEN_AMPLITUDE,
        _c.V_SIGGEN_OFFSET,
        _c.V_SIGGEN_AUX_PARAM,
        # --- FSB variables ---
        _c.V_PS_SOFT_INTERLOCKS,
        _c.V_PS_HARD_INTERLOCKS,
        _c.V_I_LOAD,
        _c.V_V_LOAD,
        _c.V_V_DCLINK,
        _c.V_TEMP_SWITCHES,)
    _groups[5] = (
        # --- mirror variables ---
        _c.V_PS_STATUS_1,
        _c.V_PS_STATUS_2,
        _c.V_PS_STATUS_3,
        _c.V_PS_STATUS_4,
        _c.V_PS_SETPOINT_1,
        _c.V_PS_SETPOINT_2,
        _c.V_PS_SETPOINT_3,
        _c.V_PS_SETPOINT_4,
        _c.V_PS_REFERENCE_1,
        _c.V_PS_REFERENCE_2,
        _c.V_PS_REFERENCE_3,
        _c.V_PS_REFERENCE_4,
        _c.V_PS_SOFT_INTERLOCKS_1,
        _c.V_PS_SOFT_INTERLOCKS_2,
        _c.V_PS_SOFT_INTERLOCKS_3,
        _c.V_PS_SOFT_INTERLOCKS_4,
        _c.V_PS_HARD_INTERLOCKS_1,
        _c.V_PS_HARD_INTERLOCKS_2,
        _c.V_PS_HARD_INTERLOCKS_3,
        _c.V_PS_HARD_INTERLOCKS_4,
        _c.V_I_LOAD_1,
        _c.V_I_LOAD_2,
        _c.V_I_LOAD_3,
        _c.V_I_LOAD_4,)

    _group_allrelevant = 3
    _group_mirror = 5
    _group_slowref = 4
    _group_cycle = 4
    _group_rmpwfm = 5
    _group_migwfm = 4

    _sleep_delay = 0.010  # [s]

    # --- public interface ---

    def __init__(self, bsmp_entities, device_ids):
        """Init."""
        self._device_ids = sorted(device_ids)
        # self._device_ids = sorted(device_ids + device_ids)  # test with 4 PS

        # create PRU with sync mode off.
        self._pru = PRU()
        self._time_interval = self._get_time_interval()

        # initialize BSMP
        self._initialize_bsmp(bsmp_entities)

        # operation queue
        self._queue = BSMPOpQueue()

        # scan thread
        self._last_device_scanned = len(self._device_ids)  # next is the first
        self._update_exec_time = None  # registers last update exec time
        self._thread_scan = _Thread(target=self._loop_scan, daemon=True)
        self._scanning = True
        self._thread_scan.start()

        # process thread
        self._thread_process = _Thread(target=self._loop_process, daemon=True)
        self._processing = True
        self._thread_process.start()

    @property
    def device_ids(self):
        """Device ids."""
        return self._device_ids[:]

    @property
    def scan(self):
        """Return scanning state."""
        return self._scanning

    @scan.setter
    def scan(self, value):
        """Set scanning state."""
        self._scanning = value

    @property
    def process(self):
        """Return processing state."""
        return self._processing

    @process.setter
    def process(self, value):
        """Set scan state."""
        self._processing = value

    @property
    def queue_length(self):
        """Number of operations currently in the queue."""
        return len(self._queue)

    # ---- main methods ----

    def read_variable(self, device_id, variable_id=None):
        """Return current mirror of variable values of the BSMP device."""
        dev_values = self._variables_values[device_id]
        if variable_id is None:
            values = dev_values
        else:
            values = dev_values[variable_id]
        return _dcopy(values)  # return a deep copy

    def exec_function(self, device_id, function_id, args=None):
        """Append a BSMP function execution to operations queue."""
        if self._pru.sync_status == self.SYNC.OFF:
            # in PRU sync off mode, append BSM function exec operation to queue
            if not args:
                args = (device_id, function_id)
            else:
                args = (device_id, function_id, args)
            operation = (self._bsmp_exec_function, args)
            self._queue.append(operation)
        else:
            # does nothing if PRU sync is on, regardless of sync mode.
            return False

    # ---- PRU and BSMP methods ----

    def pru_get_sync_status(self):
        """Return PRU sync status."""
        return self._pru.sync_status

    def pru_sync_stop(self):
        """Stop PRU sync mode."""
        # TODO: should we do more than what is implemented?
        self._pru.sync_stop()
        self._time_interval = self._get_time_interval()

    def pru_sync_start(self, sync_mode):
        """Start PRU sync mode."""
        # try to abandon previous sync mode gracefully
        if self._pru.sync_status != self.SYNC.OFF:
            # --- already with sync mode on.
            if sync_mode != self._pru.sync_mode:
                # --- different sync mode
                # PRU sync is on but it needs sync_mode change
                # first turn off PRY sync mode
                self.pru_sync_stop()
            else:
                # --- already in selected sync mode
                # TODO: to do nothing is what we want? what about WfmIndex?
                return
        else:
            # --- current sync mode is off
            pass

        # wait for all queued operations to be processed
        self._queue.ignore_set()  # ignore eventual new operation requests
        while len(self._queue) > 0:
            _time.sleep(5*self._sleep_delay)  # sleep a little

        # update time interval according to new sync mode selected
        self._time_interval = self._get_time_interval()

        # set selected sync mode
        self._pru.sync_start(
            sync_mode=sync_mode,
            sync_address=self._device_ids[0], delay=100)

        # accept back new operation requests
        self._queue.ignore_clear()

    def bsmp_scan(self):
        """Run scan one."""
        # select devices and variable group, defining the read group
        # opertation to be performed
        device_ids, group_id = self._select_device_group_ids()
        operation = (self._bsmp_update_variables,
                     (device_ids, group_id, ))
        if len(self._queue) == 0 or \
           operation != self._queue.last_operation:
            if self._pru.sync_status == self.SYNC.OFF:
                # with sync off, function executions are allowed and
                # therefore operations must be queued in order
                self._queue.append(operation)
            else:
                # for sync on, no function execution is accepted and
                # we can therefore append only unique operations since
                # processing order is not relevant.
                self._queue.append(operation, unique=True)
        else:
            # does not append if last operation is the same as last one
            # operation appended to queue
            pass

    def bsmp_process(self):
        """Run process once."""
        # process first operation in queue, if any
        self._queue.process()
        # print info
        n = len(self._queue)
        if n > 50:
            print('BBB queue size: {} !!!'.format(len(self._queue)))

    # ---- methods to access and measure communication times ----

    def meas_exec_time(self):
        """Return last update execution time [s]."""
        return self._update_exec_time

    def meas_sample_exec_time(self, device_ids, group_id, nrpoints=20):
        """Measure execution times and return stats and sample."""
        sample = []
        self.pru_sync_stop()

        # turn scanning off
        self._scanning = False

        # wait until queue empties
        while len(self._queue) > 0:
            _time.sleep(5*self._sleep_delay)  # sleep a little
        _time.sleep(self._time_interval)

        # loop and collect sample
        while len(sample) < nrpoints:
            self._bsmp_update_variables(device_ids, group_id)
            value = self.meas_exec_time()
            sample.append(value)
            print('{:03d}: {:.4f} ms'.format(len(sample), 1000*value))
            _time.sleep(self._time_interval)

        # turn scanning back on
        self._scanning = True

        # calc stats and return
        n = len(sample)
        avg = sum(sample)/n
        dev = _math.sqrt(sum([(v - avg)**2 for v in sample])/(n-1.0))
        return avg, dev, sample

    # --- private methods ---

    def _initialize_bsmp(self, bsmp_entities):

        # TODO: deal with BSMP comm errors at init!!

        # create BSMP devices
        self._bsmp = self._create_bsmp(bsmp_entities)

        # initialize variable groups
        self._initialize_groups()

        # initialize variables_values, a mirror state of BSMP devices
        self._initialize_variable_values(bsmp_entities)

    def _create_bsmp(self, bsmp_entities):
        bsmp = dict()
        for id in self._device_ids:
            # TODO: catch BSMP comm errors
            bsmp[id] = BSMP(self._pru, id, bsmp_entities)
        return bsmp

    def _initialize_variable_values(self, bsmp_entities):

        # create _variables_values
        max_id = max([max(ids) for ids in BBBController._groups[3:]])
        dev_variables = [None, ] * (1 + max_id)
        self._variables_values = \
            {id: dev_variables[:] for id in self._device_ids}
        # TODO: should we initialize this reading the ps controllers?

        # read all variable from BSMP devices
        self._bsmp_update_variables(device_ids=self._device_ids,
                                    group_id=BBBController._group_allrelevant)

    def _initialize_groups(self):

        # TODO: catch BSMP comm errors

        # check if groups have consecutive ids
        groups_ids = sorted(self._groups.keys())
        if len(groups_ids) < 3:
            raise ValueError('Invalid variable group definition!')
        for i in range(len(groups_ids)):
            if i not in groups_ids:
                raise ValueError('Invalid variable group definition!')

        # loop over bsmp devices
        for id in self._device_ids:
            # remove previous variables groups and fresh ones
            self._bsmp[id].remove_all_groups()
            for group_id in groups_ids[3:]:
                var_ids = self._groups[group_id]
                self._bsmp[id].create_group(var_ids)

    def _loop_scan(self):
        while True:
            if self._scanning:
                self.bsmp_scan()
            # wait for time_interval
            _time.sleep(self._time_interval)

    def _loop_process(self):
        while True:
            if self._processing:
                self.bsmp_process()
            # sleep a little
            _time.sleep(self._sleep_delay)

    def _select_device_group_ids(self):
        """Return variable group id and device ids for the loop scan."""
        if self._pru.sync_status == self.SYNC.OFF:
            return self._device_ids, BBBController._group_slowref
        elif self._pru.sync_mode == self.SYNC.MIGEND:
            return self._device_ids, BBBController._group_migwfm
        elif self._pru.sync_mode == self.SYNC.RMPEND:
            dev_ids = self._select_next_device_id()
            return dev_ids, BBBController._group_rmpwfm
        elif self._pru.sync_mode == self.SYNC.CYCLE:
            return self._device_ids, BBBController._group_cycle
        else:
            raise NotImplementedError('Sync mode not implemented!')

    def _select_next_device_id(self):
        # TODO: with the mirror var solution this selection is not necessary!
        #       attribute self._last_device_scanned can be deleted.
        #
        # # calc index of next single device to be scanned
        # nr_devs = len(self._device_ids)
        # dev_idx = (self._last_device_scanned + 1) % nr_devs
        # dev_id = self._device_ids[dev_idx]
        # self._last_device_scanned = dev_idx

        # now always return first device to read the selected variables of
        # all power supplies through mirror variables.
        return (self._devices_ids[0], )

    def _get_time_interval(self):
        if self._pru.sync_status == self.SYNC.OFF or \
           self._pru.sync_mode == self.SYNC.CYCLE:
            return 1.0/self.FREQ.SCAN  # [s]
        else:
            return 1.0/self.FREQ.RAMP  # [s]

    # --- methods that generate BSMP UART communications ---

    def _bsmp_update_variables(self, device_ids, group_id):

        ack, data = dict(), dict()

        # --- send requests to serial line
        t0 = _time.time()
        for id in device_ids:
            ack[id], data[id] = \
                self._bsmp[id].read_group_variables(group_id=group_id)
        self._update_exec_time = _time.time() - t0

        # --- update variables, if ack is ok
        var_ids = self._groups[group_id]
        for id in device_ids:
            if ack[id] == Response.ok:
                values = data[id]
                # print('values: ', values)
                for i in range(len(values)):
                    var_id = var_ids[i]
                    # process mirror variables, if the case
                    if group_id == BBBController._group_mirror:
                        mir_dev_id, mir_var_id = _mirror_map[var_id]
                        self._variables_values[mir_dev_id][mir_var_id] = \
                            values[i]
                    # process original variable
                    self._variables_values[id][var_id] = values[i]
            else:
                # TODO: update 'connect' state for that device
                pass

    def _bsmp_exec_function(self, device_id, function_id, args=None):
        ack, values = self._bsmp[device_id].execute_function(function_id, args)
        if ack == Response.ok:
            return values
        else:
            # TODO: update 'connect' state for that device
            return None

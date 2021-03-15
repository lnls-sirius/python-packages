"""PRUController.

This module implements classes that are used to do low level BeagleBone
communications, be it with PRU or BSMP requests to power supply controllers
at the other end of the serial line.
"""

import time as _time
from copy import deepcopy as _dcopy
from threading import Thread as _Thread
from threading import Lock as _Lock

from ...bsmp import SerialError as _SerialError

from ..bsmp.constants import _const_bsmp
from ..bsmp.constants import __version__ as _firmware_version_siriuspy

from .udc import UDC as _UDC
from .psdevstate import PSDevState as _PSDevState


class PRUController:
    """Beaglebone controller.

    This class implements all basic PRU configuration and BSMP communications
    of the Beaglebone computer connected through a serial line to power supply
    controllers.
    """

    # NOTE: All private methods starting with '_bsmp' string invole serial
    #       bsmp communications.

    _sleep_process_loop = 0.020  # [s]

    # --- public interface ---

    def __init__(self,
                 pru,
                 prucqueue,
                 psmodel,
                 devices,
                 processing=False,
                 scanning=False,
                 freq=None,
                 init=True):
        """Init."""
        # --- Init structures ---

        print()
        print('PRUController: struct initialization')
        print('devices: {}'.format(devices))

        # init timetsamp
        self._timestamp_update = _time.time()

        # init time interval
        t0_ = _time.time()

        # init sofb mode to false
        self._sofb_mode = False

        # index of device in self._device_ids for next update in SOFB mode
        self._sofb_update_dev_idx = 0  # cyclical updates!

        # create lock
        self._lock = _Lock()

        # PRU communication object
        self._pru = pru

        # store power supply model
        self._psmodel = psmodel

        # devices
        self._devices = _dcopy(devices)

        # sorted list of device ids
        self._device_ids = sorted([dev[1] for dev in devices])

        # initialize UDC
        self._udc, self._parms, self._psupplies = PRUController._init_udc(
            pru, self._psmodel.name, self._device_ids, freq)

        # index of device in self._device_ids for wfmref/scope update
        self._scope_update = False
        self._scope_update_dev_idx = 0  # cyclical updates!

        # update time interval attribute
        self._scan_interval = self._get_scan_interval()

        # time interval
        t1_ = _time.time()
        print('TIMING struct init [{:.3f} ms]'.format(1000*(t1_ - t0_)))

        # attributes that control processing flow
        self._queue = prucqueue
        self._processing = processing
        self._scanning = scanning

        # starts communications
        self._dev_idx_last_scanned = None
        self._thread_process = None
        self._thread_scan = None
        if init:
            self.bsmp_init_communication()

    # --- properties to read and set controller state and access functions ---

    @property
    def scan_interval(self):
        """Scan interval."""
        return self._scan_interval

    @property
    def scanning(self):
        """Return scanning state."""
        return self._scanning

    @scanning.setter
    def scanning(self, value):
        """Set scanning state."""
        self._scanning = value

    @property
    def processing(self):
        """Return processing state."""
        return self._processing

    @processing.setter
    def processing(self, value):
        """Set processing state."""
        self._processing = value

    @property
    def queue_length(self):
        """Store number of operations currently in the queue."""
        return len(self._queue)

    @property
    def params(self):
        """Return PRUController parameters."""
        return self._parms

    @property
    def connected(self):
        """Store connection state."""
        return all((self.check_connected(id) for id in self._device_ids))

    def check_connected(self, device_id):
        """Return connection state of a device."""
        # TODO: may not be the true current connection state
        psupply = self._psupplies[device_id]
        return psupply.connected

    def timestamp_update(self):
        """Return tmestamp of last device update."""
        return self._timestamp_update
        # psupply = self._psupplies[device_id]
        # with self._lock:
        #     tstamp = psupply.timestamp_update
        # return tstamp

    # === queueing writes and local state copy reads ===

    # --- bsmp variables ---

    def read_variables(self, device_ids, variable_id=None):
        """
        Return device variables.

        Parameters
        ----------
        device_ids : int, tuple or list
            The BSMP device ids.
        variable_id : int or None, optional.
            The BSMP variable id selected. If not passed all device variables
            will be returned.

        Returns
        -------
        Selected BSMP device variable values.

        """
        # process device_ids
        if isinstance(device_ids, int):
            dev_ids = (device_ids, )
        else:
            dev_ids = device_ids

        # builds dict of requested values
        values = dict()
        for dev_id in dev_ids:
            if variable_id is None:
                values[dev_id] = self._psupplies[dev_id].variables
            else:
                values[dev_id] = \
                    self._psupplies[dev_id].get_variable(variable_id)

        # make copy
        with self._lock:
            if isinstance(device_ids, int):
                return _dcopy(values[device_ids])
            return _dcopy(values)

    def read_parameters(self, device_ids, parameter_id=None):
        """Return power supply parameters."""
        # process device_ids
        if isinstance(device_ids, int):
            dev_ids = (device_ids, )
        else:
            dev_ids = device_ids

        # builds dict of requested values
        values = dict()
        for dev_id in dev_ids:
            if parameter_id is None:
                values[dev_id] = self._psupplies[dev_id].parameters
            else:
                values[dev_id] = \
                    self._psupplies[dev_id].get_parameter(parameter_id)

        # make copy
        with self._lock:
            if isinstance(device_ids, int):
                return _dcopy(values[device_ids])
            return _dcopy(values)

    def exec_functions(self, device_ids, function_id, args=None):
        """
        Append BSMP function executions to opertations queue.

        Parameters
        ----------
        device_ids : int, tuple or list
            The BSMP device ids. It can be a list of ids or a singe id.
        function_id : int
            The BSMP function id to be executed for the devices.
        args : tuple, optional
            The list of BSMP function argument values

        Returns
        -------
        status : bool
            True is operation was queued or False, if operation was rejected
            because of the SOFBMode state.

        """
        # if in SOFBMode on, do not accept exec functions
        if self._sofb_mode:
            return False

        # prepare arguments
        if isinstance(device_ids, int):
            device_ids = (device_ids, )
        if args is None:
            args = (device_ids, function_id)
        else:
            args = (device_ids, function_id, args)

        # append bsmp function exec operation to queue
        operation = (self._bsmp_exec_function, args)
        self._queue.append(operation)
        return True

    # --- wfmref and scope curves ---

    def scope_update_auto_enable(self):
        """Enable wfmref and scope curves updates."""
        self._scope_update = True

    def scope_update_auto_disable(self):
        """Disable wfmref and scope curves updates."""
        self._scope_update = False

    @property
    def scope_update_auto(self):
        """Return state of scope_update_auto."""
        return self._scope_update

    def wfm_update(self, device_ids, interval=None):
        """Queue update wfm and scope curves."""
        if isinstance(device_ids, int):
            device_ids = (device_ids, )
        operation = (self._bsmp_update_wfm, (device_ids, interval, ))
        self._queue.append(operation)
        return True

    def wfmref_write(self, device_ids, data):
        """Write wfm curves."""
        # if in SOFBMode on, do not accept exec functions
        if self._sofb_mode:
            return False

        # prepare arguments
        if isinstance(device_ids, int):
            device_ids = (device_ids, )

        # append bsmp function exec operation to queue
        operation = (self._bsmp_wfmref_write, (device_ids, data))
        self._queue.append(operation)
        return True

    def wfmref_rb_read(self, device_id):
        """Return wfmref_rb curve."""
        psupply = self._psupplies[device_id]
        # NOTE: investigate whether lock and copy are really necessary!
        with self._lock:
            return _dcopy(psupply.wfmref_rb)

    def wfmref_read(self, device_id):
        """Return wfmref curve."""
        psupply = self._psupplies[device_id]
        with self._lock:
            curve = psupply.wfmref
            return _dcopy(curve)

    def wfmref_index(self, device_id):
        """Return current index into DSP selected curve."""
        psupply = self._psupplies[device_id]
        with self._lock:
            index = psupply.wfmref_index
        return index

    def scope_read(self, device_id):
        """Return Wfm-Mon curve."""
        psupply = self._psupplies[device_id]
        with self._lock:
            return _dcopy(psupply.scope)

    # --- SOFBCurrent parameters ---

    def sofb_mode_set(self, state):
        """Change SOFB mode: True or False."""
        self._sofb_mode = state
        if state:
            while self._queue:  # wait until queue is empty
                pass

    @property
    def sofb_mode(self):
        """Return SOFB mode."""
        return self._sofb_mode

    def sofb_current_set(self, value):
        """."""
        # wait until queue is empty
        while self._queue:
            pass

        # execute SOFB setpoint
        self._bsmp_update_sofb_setpoint(value)

        return True

    @property
    def sofb_current_rb(self):
        """."""
        return self._udc.sofb_current_rb_get()

    @property
    def sofb_current_refmon(self):
        """."""
        return self._udc.sofb_current_refmon_get()

    @property
    def sofb_current_mon(self):
        """."""
        return self._udc.sofb_current_mon_get()

    def sofb_update_variables_state(self):
        """Update variables state mirror."""
        # do sofb update only if in SOFBMode On
        if not self._sofb_mode:
            return

        # wait until queue is empty
        while self._queue:
            pass

        # select power supply dev_id for updating
        self._sofb_update_dev_idx = \
            (self._sofb_update_dev_idx + 1) % len(self._device_ids)
        dev_id = self._device_ids[self._sofb_update_dev_idx]

        # update variables state mirror for selected power supply
        self._bsmp_update_variables(dev_id)

    # --- scan and process loop methods ---

    def bsmp_scan(self):
        """Run scan one."""
        # select devices and variable group, defining the read group
        # operation to be performed
        operation = (self._bsmp_update, ())
        if not self._queue or operation != self._queue.last_operation:
            self._queue.append(operation)
        else:
            # do not append if last operation is the same as last one
            # operation appended to queue
            pass

    def bsmp_process(self):
        """Run process once."""
        # process first operation in queue, if any.
        self._queue.process()

    def bsmp_init_communication(self):
        """."""
        # --- BSMP communication ---

        print()
        print('PRUController: bsmp initialization')
        # init time interval
        t0_ = _time.time()

        # reset power supply controllers (contains first BSMP comm)
        self._bsmp_reset_udc()

        # update state of PRUController from ps controller
        self._bsmp_init_update()

        # init thread structures
        self._init_threads()

        # time interval
        t1_ = _time.time()
        print('TIMING bsmp init [{:.3f} ms]\n'.format(
            1000*(t1_ - t0_)))

        # after all initializations, threads are started
        self._running = True
        self._thread_process.start()
        self._thread_scan.start()

    # --- private methods: initializations ---

    def _init_threads(self):

        fmt = '  - {:<20s} ({:^20s}) [{:09.3f}] ms'
        t0_ = _time.time()

        # define process thread
        self._thread_process = _Thread(target=self._loop_process, daemon=True)

        # define scan thread
        self._dev_idx_last_scanned = \
            len(self._device_ids)-1  # the next will be the first bsmp dev
        self._thread_scan = _Thread(target=self._loop_scan, daemon=True)

        dt_ = _time.time() - t0_
        print(fmt.format('init_threads', 'create structures', 1e3*dt_))

    @staticmethod
    def _init_udc(pru, psmodel_name, device_ids, freq):

        # create UDC
        udc = _UDC(pru, psmodel_name, device_ids)
        parms = udc.prucparms

        # create PSDevState objects
        psupplies = dict()
        for dev_id in device_ids:
            psupplies[dev_id] = _PSDevState(psbsmp=udc[dev_id])

        # bypass psmodel default frequencies
        if freq is not None:
            parms.FREQ_SCAN = freq

        # print info on scan frequency
        fstr = ('device_id:{:2d}, scan_freq: {:4.1f} Hz')
        for dev in device_ids:
            freq = 10.0 if freq is None else freq
            print(fstr.format(dev, parms.FREQ_SCAN))
        print()

        return udc, parms, psupplies

    def _init_check_version(self):
        if not self.connected:
            return
        for dev_id in self._device_ids:
            # V_FIRMWARE_VERSION should be defined for all BSMP devices
            psupply = self._psupplies[dev_id]
            _firmware_version_udc = psupply.get_variable(
                self._parms.CONST_PSBSMP.V_FIRMWARE_VERSION)
            _firmware_version_udc = \
                self._udc.parse_firmware_version(_firmware_version_udc)
            if 'Simulation' not in _firmware_version_udc and \
               _firmware_version_udc != _firmware_version_siriuspy:
                errmsg = ('PRUController: Incompatible bsmp implementation version '
                          'for device id:{}')
                print(errmsg.format(dev_id))
                errmsg = 'lib version: {}'
                print(errmsg.format(_firmware_version_siriuspy))
                errmsg = 'udc version: {}'
                print(errmsg.format(_firmware_version_udc))
                print()
                # raise ValueError(errmsg)

    # --- private methods: scan and process ---

    def _loop_scan(self):
        while self._running:

            t0_ = _time.time()

            # run scan method once
            if self.scanning and \
               self._scan_interval != 0 and \
               not self._sofb_mode:
                self.bsmp_scan()

            # update scan interval
            self._scan_interval = self._get_scan_interval()

            # wait for time_interval
            dt_ = _time.time() - t0_
            if dt_ < self._scan_interval:
                _time.sleep(self._scan_interval - dt_)

            # update timestamp
            self._timestamp_update = _time.time()

    def _loop_process(self):
        while self._running:
            if self.processing:
                self.bsmp_process()
            # if queue is empty, sleep a little
            # _time.sleep(self._sleep_process_loop)
            # NOTE: this optimization is being tested...
            if not self._queue:
                _time.sleep(self._sleep_process_loop)

    def _get_scan_interval(self):
        if self._parms.FREQ_SCAN == 0:
            return 0
        else:
            return 1.0/self._parms.FREQ_SCAN  # [s]

    def _serial_error(self, device_ids):
        # signal disconnected for device ids.
        for dev_id in device_ids:
            psupply = self._psupplies[dev_id]
            psupply._connected = False

    def _check_groups(self):
        group_ids = sorted(self._parms.groups.keys())

        # needs to have all default groups
        if len(group_ids) < 3:
            raise ValueError(('Invalid variable group definition: '
                              'default group missing!'))
        # needs to have all consecutive groups
        for i in range(len(group_ids)):
            if i not in group_ids:
                raise ValueError(('Invalid variable group definition: '
                                  'non-consecutive group ids!'))

    # --- private methods: BSMP UART communications ---

    def _bsmp_reset_udc(self):

        # set scan interval
        self._scan_interval = self._get_scan_interval()

        # initialize variable groups (first BSMP comm.)
        self._bsmp_init_devices()

    def _bsmp_init_devices(self):

        fmt = '  - {:<20s} ({:^20s}) [{:09.3f}] ms'

        # create vars groups list from dict
        groups = PRUController._dict2list_vargroups(self._parms.groups)

        # reset group of bsmp variables for all devices
        t0_ = _time.time()
        for psupply in self._psupplies.values():
            psupply.reset_variables_groups(groups)
        dt_ = _time.time() - t0_
        print(fmt.format('bsmp_init_devices', 'reset groups', 1e3*dt_))

        # update psupply groups
        t0_ = _time.time()
        for psupply in self._psupplies.values():
            psupply.update_groups(interval=0.0)
        dt_ = _time.time() - t0_
        print(fmt.format('bsmp_init_devices', 'update groups', 1e3*dt_))

        # disable DSP from writting to bufsample (uses first device)
        t0_ = _time.time()
        self._udc.bufsample_disable()
        dt_ = _time.time() - t0_
        print(fmt.format('bsmp_init_devices', 'bufsample_disable', 1e3*dt_))

    def _bsmp_update(self):

        # print('{:<30s} : {:>9.3f} ms'.format(
        #     'PRUC._bsmp_update (beg)', 1e3*(_time.time() % 1)))

        # update variables
        self._bsmp_update_variables()

        # update device wfm curves cyclically
        if self._scope_update:
            self._scope_update_dev_idx = \
                (self._scope_update_dev_idx + 1) % len(self._device_ids)
            dev_id = self._device_ids[self._scope_update_dev_idx]
            self._bsmp_update_wfm(dev_id)

        # print('{:<30s} : {:>9.3f} ms'.format(
        #     'PRUC._bsmp_update (end)', 1e3*(_time.time() % 1)))

    def _bsmp_update_variables(self, dev_id=None):
        if dev_id is None:
            psupplies = self._psupplies.values()
        else:
            psupplies = (self._psupplies[dev_id], )

        for psupply in psupplies:
            try:
                psupply.update_variables(interval=0.0)
            except _SerialError:
                # no serial connection !
                pass

    def _bsmp_update_wfm(self, device_id):
        """Read curve from devices."""
        psupplies = self._psupplies

        try:
            psupply = psupplies[device_id]
            psupply.update_wfm()
        except _SerialError:
            # no serial connection !
            pass

        # stores updated psupplies dict
        self._psupplies = psupplies  # atomic operation

    def _bsmp_update_sofb_setpoint(self, value):

        # execute sofb current setpoint
        self._udc.sofb_current_set(value)

        # update sofb state
        self._udc.sofb_update()

        # # update all other device parameters
        # self._bsmp_update()

        # print('{:<30s} : {:>9.3f} ms'.format(
        #     'PRUC._bsmp_update_sofb_setpoint (end)', 1e3*(_time.time() % 1)))

    def _bsmp_wfmref_write(self, device_ids, curve):
        """Write wfmref curve to devices."""
        try:
            # write curves
            for dev_id in device_ids:
                psupply = self._psupplies[dev_id]
                # sends new wfmref curve to power supply then reads back
                # curve in UDC memory
                curve = psupply.psbsmp.wfmref_write(curve)
                with self._lock:
                    psupply.wfmref_rb = curve
                    psupply.update_wfm(interval=0.0)
        except (_SerialError, IndexError):
            print('PRUController: bsmp_wfmref_write error!')
            self._serial_error(device_ids)

    def _bsmp_exec_function(self, device_ids, function_id, args=None):
        # --- send func exec request to serial line

        # BSMP device's 'execute_function' needs to lock code execution
        # so as to avoid more than one thread reading each other's responses.
        # class BSMP method 'request' should always do that

        ack, data = dict(), dict()

        # --- send requests to serial line
        try:
            for dev_id in device_ids:
                resp = self._udc[dev_id].execute_function(function_id, args)
                ack[dev_id], data[dev_id] = resp
                # check anomalous response
                if ack[dev_id] != _const_bsmp.ACK_OK:
                    print('PRUController: anomalous response !')
                    datum = data[dev_id]
                    if isinstance(datum, str):
                        datum = ord(datum)
                    self._udc[dev_id].anomalous_response(
                        _const_bsmp.CMD_EXECUTE_FUNCTION, ack[dev_id],
                        device_id=dev_id, function_id=function_id,
                        data_type=type(datum), data=datum)
        except _SerialError:
            return None
        except TypeError:
            print('--- PRUController debug ---')
            print('device_ids  : ', device_ids)
            print('dev_id      : ', dev_id)
            print('function_id : ', function_id)
            print('resp        : ', resp)
            print('data        : ', data[dev_id])
            raise

        # --- check if all function executions succeeded.
        success = True
        for dev_id in device_ids:
            connected = (ack[dev_id] == _const_bsmp.ACK_OK)
            success &= connected

        if success:
            return data
        else:
            return None

    def _bsmp_init_update(self):

        fmt = '  - {:<20s} ({:^20s}) [{:09.3f}] ms'

        # initialize variables_values, a mirror state of BSMP devices
        t0_ = _time.time()
        self._bsmp_init_variable_values()
        dt_ = _time.time() - t0_
        print(fmt.format('bsmp_init_update', 'variable_values', 1e3*dt_))

        # initialize ps curves
        t0_ = _time.time()
        self._bsmp_init_wfm()
        dt_ = _time.time() - t0_
        print(fmt.format('bsmp_init_update', 'waveform_values', 1e3*dt_))

        # initialize sofb
        t0_ = _time.time()
        self._bsmp_init_sofb_values()
        dt_ = _time.time() - t0_
        print(fmt.format('bsmp_init_update', 'sofb_values', 1e3*dt_))

        # initialize parameters
        t0_ = _time.time()
        self._bsmp_init_parameter_values()
        dt_ = _time.time() - t0_
        print(fmt.format('bsmp_init_update', 'parameter_values', 1e3*dt_))

    def _bsmp_init_wfm(self):

        for psupply in self._psupplies.values():

            # update
            psupply.update_wfm(interval=0.0)

            # raise ValueError('!!! Debug stop !!!')

            # registers RB using psupply object
            psupply.wfmref_rb = psupply.wfmref

            # raise ValueError('!!! Debug stop !!!')

        # raise ValueError('!!! Debug stop !!!')

        # enable bufsample
        # self._udc.bufsample_enable()

        # raise ValueError('!!! Debug stop !!!')

    def _bsmp_init_variable_values(self):

        # init psupplies variables
        for psupply in self._psupplies.values():
            psupply.update_variables(interval=0.0)

    def _bsmp_init_parameter_values(self):

        # init psupplies variables
        for psupply in self._psupplies.values():
            psupply.update_parameters(interval=0.0)

    def _bsmp_init_sofb_values(self):

        self._udc.sofb_update()

    @staticmethod
    def _dict2list_vargroups(groups_dict):
        group_ids = sorted(groups_dict.keys())
        if len(group_ids) < 3:  # needs to have all default groups
            print('PRUController: Incorrect variables group definition: '
                  'it does not have all three standard groups!')
            raise ValueError
        for i in range(len(group_ids)):  # consecutive?
            if i not in group_ids:
                print('PRUController: Incorrect variables group definition: '
                      'it does not have consecutive group ids!')
                raise ValueError
        # create list of variable ids
        groups_list = [groups_dict[gid] for gid in group_ids]
        return groups_list

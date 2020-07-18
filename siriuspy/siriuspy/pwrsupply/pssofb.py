"""PSSOFB class."""

from threading import Thread as _Thread, Event as _Event

import numpy as _np

from ..search import PSSearch as _PSSearch
from ..bsmp import SerialError as _SerialError
from ..bsmp import constants as _const_bsmp
from ..bsmp.serial import Channel as _Channel
from ..devices import StrengthConv as _StrengthConv
from ..thread import AsynchronousWorker as _AsynWorker

from .bsmp.constants import ConstFBP as _const_fbp
from .csdev import PSSOFB_MAX_NR_UDC as _PSSOFB_MAX_NR_UDC
from .csdev import UDC_MAX_NR_DEV as _UDC_MAX_NR_DEV
from .pructrl.pru import PRU as _PRU
from .pructrl.udc import UDC as _UDC
from .psctrl.pscstatus import PSCStatus as _PSCStatus


class _BBBThread(_AsynWorker):
    """Class to run methods from a given BBB."""

    def configure_new_run(self, target, args=None):
        """Configure a new run of the thread."""
        args_ = (self.name, )
        if isinstance(args, tuple):
            args_ = args_ + args
        return super().configure_new_run(target, args_)


class PSNamesSOFB:
    """."""

    _sofb = dict()
    _sofb_factory = None

    @staticmethod
    def get_psnames_ch(acc):
        """Return horizontal corrector psnames of a given sector."""
        if PSNamesSOFB._sofb_factory is None:
            from ..sofb.csdev import SOFBFactory
            PSNamesSOFB._sofb_factory = SOFBFactory
        if acc not in PSNamesSOFB._sofb:
            PSNamesSOFB._sofb[acc] = PSNamesSOFB._sofb_factory.create(acc)
        return PSNamesSOFB._sofb[acc].ch_names

    @staticmethod
    def get_psnames_cv(acc):
        """Return vertical corrector psnames of a given sector."""
        if PSNamesSOFB._sofb_factory is None:
            from ..sofb.csdev import SOFBFactory
            PSNamesSOFB._sofb_factory = SOFBFactory
        if acc not in PSNamesSOFB._sofb:
            PSNamesSOFB._sofb[acc] = PSNamesSOFB._sofb_factory.create(acc)
        return PSNamesSOFB._sofb[acc].cv_names


class PSSOFB:
    """."""

    BBBNAMES = (
        'IA-01RaCtrl:CO-PSCtrl-SI2',
        'IA-02RaCtrl:CO-PSCtrl-SI2',
        'IA-03RaCtrl:CO-PSCtrl-SI2',
        'IA-04RaCtrl:CO-PSCtrl-SI2',
        'IA-05RaCtrl:CO-PSCtrl-SI2',
        'IA-06RaCtrl:CO-PSCtrl-SI2',
        'IA-07RaCtrl:CO-PSCtrl-SI2',
        'IA-08RaCtrl:CO-PSCtrl-SI2',
        'IA-09RaCtrl:CO-PSCtrl-SI2',
        'IA-10RaCtrl:CO-PSCtrl-SI2',
        'IA-11RaCtrl:CO-PSCtrl-SI2',
        'IA-12RaCtrl:CO-PSCtrl-SI2',
        'IA-13RaCtrl:CO-PSCtrl-SI2',
        'IA-14RaCtrl:CO-PSCtrl-SI2',
        'IA-15RaCtrl:CO-PSCtrl-SI2',
        'IA-16RaCtrl:CO-PSCtrl-SI2',
        'IA-17RaCtrl:CO-PSCtrl-SI2',
        'IA-18RaCtrl:CO-PSCtrl-SI2',
        'IA-19RaCtrl:CO-PSCtrl-SI2',
        'IA-20RaCtrl:CO-PSCtrl-SI2',
        'IA-01RaCtrl:CO-PSCtrl-SI4',
        'IA-02RaCtrl:CO-PSCtrl-SI4',
        'IA-03RaCtrl:CO-PSCtrl-SI4',
        'IA-04RaCtrl:CO-PSCtrl-SI4',
        'IA-05RaCtrl:CO-PSCtrl-SI4',
        'IA-06RaCtrl:CO-PSCtrl-SI4',
        'IA-07RaCtrl:CO-PSCtrl-SI4',
        'IA-08RaCtrl:CO-PSCtrl-SI4',
        'IA-09RaCtrl:CO-PSCtrl-SI4',
        'IA-10RaCtrl:CO-PSCtrl-SI4',
        'IA-11RaCtrl:CO-PSCtrl-SI4',
        'IA-12RaCtrl:CO-PSCtrl-SI4',
        'IA-13RaCtrl:CO-PSCtrl-SI4',
        'IA-14RaCtrl:CO-PSCtrl-SI4',
        'IA-15RaCtrl:CO-PSCtrl-SI4',
        'IA-16RaCtrl:CO-PSCtrl-SI4',
        'IA-17RaCtrl:CO-PSCtrl-SI4',
        'IA-18RaCtrl:CO-PSCtrl-SI4',
        'IA-19RaCtrl:CO-PSCtrl-SI4',
        'IA-20RaCtrl:CO-PSCtrl-SI4',
    )
    BBB2DEVS = dict()

    _MAX_NR_DEVS = _PSSOFB_MAX_NR_UDC * _UDC_MAX_NR_DEV
    _dipole_propty = 'Ref-Mon'

    PS_PWRSTATE = _PSCStatus.PWRSTATE
    PS_OPMODE = _PSCStatus.OPMODE

    def __init__(self, ethbridgeclnt_class):
        """."""
        self._acc = 'SI'
        self.pru = None
        self.udc = None

        self._sofb_psnames = \
            PSNamesSOFB.get_psnames_ch(self._acc) + \
            PSNamesSOFB.get_psnames_cv(self._acc)

        # snapshot of sofb current values
        self._sofb_current_rb = _np.zeros(len(self._sofb_psnames))
        self._sofb_current_refmon = _np.zeros(len(self._sofb_psnames))
        self._sofb_current_mon = _np.zeros(len(self._sofb_psnames))
        self._sofb_current_readback_ref = _np.zeros(len(self._sofb_psnames))

        # create sofb and bsmp indices
        self.indcs_bsmp, self.indcs_sofb = self._create_indices()

        # initialize connector objects for bsmp communications.
        self._init_connectors(ethbridgeclnt_class)

        # dictionaries with comm. ack and state snapshot of all correctors
        self._dev_state_initialized = False
        self._dev_ack = dict()  # last ack state of bsmp comm.
        self._dev_state = dict()  # snapshot of device variable values
        self._threads = list()  # threads to run BBB methods
        for bbbname, bsmpdevs in PSSOFB.BBB2DEVS.items():
            self._dev_ack[bbbname] = {bsmp[1]: True for bsmp in bsmpdevs}
            self._dev_state[bbbname] = {bsmp[1]: dict() for bsmp in bsmpdevs}
            thread = _BBBThread(name=bbbname)
            thread.start()
            self._threads.append(thread)

        # power supply status objects
        self._pscstatus = [_PSCStatus() for _ in self._sofb_psnames]

        # strength to current converters
        self._strengths_dipole = 3.0  # [GeV]
        self._pstype_2_index, self._pstype_2_sconv = self._get_strenconv()

    # --- bsmp methods: invoke communications with correctors ---

    def bsmp_sofb_current_set(self, current):
        """Send current sofb setpoint to power supplies."""
        self._parallel_execution(self._bsmp_current_setpoint, (current, ))

    def bsmp_sofb_kick_set(self, kick):
        """Send kick sofb setpoint to power supplies."""
        current = self._conv_stren2curr(kick)
        self.bsmp_sofb_current_set(current)
        return current

    def bsmp_sofb_current_set_update(self, current):
        """Send current sofb setpoint to power supplies and update."""
        self._parallel_execution(self._bsmp_current_setpoint_update, current)

    def bsmp_sofb_kick_set_update(self, kick):
        """Send kick sofb setpoint to power supplies and update."""
        current = self._conv_stren2curr(kick)
        self.bsmp_sofb_current_set_update(current)
        return current

    def bsmp_sofb_update(self):
        """Receive from correctors currents and update object attributes."""
        self._parallel_execution(self._bsmp_current_update)

    def bsmp_state_update(self):
        """Receive from correctors variables and update object attributes."""
        self._parallel_execution(self._bsmp_state_update)
        self._dev_state_initialized = True

    def bsmp_pwrstate_on(self):
        """Turn all correctors on and update state."""
        args = (_const_fbp.F_TURN_ON, )
        self._parallel_execution(self._bsmp_execute_function, args)
        self._parallel_execution(self._bsmp_state_update)

    def bsmp_pwrstate_off(self):
        """Turn all correctors off and update state."""
        args = (_const_fbp.F_TURN_OFF, )
        self._parallel_execution(self._bsmp_execute_function, args)
        self._parallel_execution(self._bsmp_state_update)

    def bsmp_slowref(self):
        """Set all correctors to SlowRef opmode and update state."""
        args = (_const_fbp.F_SELECT_OP_MODE, _PSCStatus.STATES.SlowRef)
        self._parallel_execution(self._bsmp_execute_function, args)
        self._parallel_execution(self._bsmp_state_update)

    def bsmp_slowrefsync(self):
        """Turn all correctors ro SlowRefSync opmode and update state."""
        args = (_const_fbp.F_SELECT_OP_MODE, _PSCStatus.STATES.SlowRefSync)
        self._parallel_execution(self._bsmp_execute_function, args)
        self._parallel_execution(self._bsmp_state_update)

    # --- sofb-vector object attribute methods ---

    @property
    def sofb_psnames(self):
        """Return corrector names in SOFB order."""
        return self._sofb_psnames

    @property
    def sofb_kick_refmon(self):
        """Return SOFB kick Ref-Mon vector, as last updated."""
        current = self.sofb_current_refmon
        strength = self._conv_curr2stren(current)
        return strength

    @property
    def sofb_kick_readback_ref(self):
        """Return SOFB kick calculated from current readback after last setpoint."""
        current = self.sofb_current_readback_ref
        strength = self._conv_curr2stren(current)
        return strength

    @property
    def sofb_current_rb(self):
        """Return SOFB current RB vector, as last updated."""
        return self._sofb_current_rb

    @property
    def sofb_current_refmon(self):
        """Return SOFB current Ref-Mon vector, as last updated."""
        return self._sofb_current_refmon

    @property
    def sofb_current_mon(self):
        """Return SOFB current -Mon vector, as last updated."""
        return self._sofb_current_mon

    @property
    def sofb_current_readback_ref(self):
        """Return SOFB current readback after last setpoint."""
        return self._sofb_current_readback_ref

    def sofb_state_variable_get(self, var_id, dtype=float):
        """Return SOFB vector with bsmp variable values, as last updated."""
        if not self._dev_state_initialized:
            self.bsmp_state_update()
        return self._sofb_state_variable(var_id=var_id, dtype=dtype)

    @property
    def sofb_opmode(self):
        """Return SOFB vector with OpMode-Sts values, as last updated."""
        if not self._dev_state_initialized:
            self.bsmp_state_update()
        return self._sofb_pscstatus_get('ioc_opmode')

    @property
    def sofb_pwrstate(self):
        """Return SOFB vector with PwrState-Sts values, as last updated."""
        if not self._dev_state_initialized:
            self.bsmp_state_update()
        return self._sofb_pscstatus_get('ioc_pwrstate')

    @property
    def sofb_interlock_hard(self):
        """Return SOFB vector with IntlkHard-Sts values, as last updated."""
        if not self._dev_state_initialized:
            self.bsmp_state_update()
        return self._sofb_state_variable(
            _const_fbp.V_PS_HARD_INTERLOCKS, dtype=int)

    @property
    def sofb_interlock_soft(self):
        """Return SOFB vector with IntlkSoft-Sts values, as last updated."""
        if not self._dev_state_initialized:
            self.bsmp_state_update()
        return self._sofb_state_variable(
            _const_fbp.V_PS_SOFT_INTERLOCKS, dtype=int)

    @staticmethod
    def sofb_vector_issame(vector1, vector2):
        """Check if two sofb vectors are identical within float32 precision."""
        if len(vector1) != len(vector2):
            return False
        # comparison
        vec1 = _np.asarray(vector1, dtype=_np.float32)
        vec2 = _np.asarray(vector2, dtype=_np.float32)
        return _np.all(vec1 == vec2)

    def conv_psname_2_sofb_index(self, psname):
        """."""
        return self._sofb_psnames.index(psname)

    def stop_threads(self):
        """Stop BBB threads."""
        for thr in self._threads:
            thr.stop()
        for thr in self._threads:
            thr.join()

    # --- private methods ---

    def _parallel_execution(self, target, args=None):
        """Execute 'method' in parallel."""
        # run threads
        for thr in self._threads:
            if not thr.configure_new_run(target, args=args):
                raise RuntimeError('Thread is not ready for job!')
        # wait for run to finish
        for thr in self._threads:
            thr.wait_ready()

    def _bsmp_current_update(self, bbbname):
        """Update SOFB parameters of a single beaglebone."""
        udc = self.udc[bbbname]

        # --- bsmp communication ---
        udc.sofb_update()

        # update currents
        self._update_currents(bbbname)

    def _bsmp_current_setpoint(self, bbbname, curr_sp):
        """.

        benchmarks:
            - lnls560-linux, no comm.  :   4.56 us +/- 98.4 ns
        """
        udc = self.udc[bbbname]

        # get indices
        indcs_sofb = self.indcs_sofb[bbbname]
        indcs_bsmp = self.indcs_bsmp[bbbname]

        # get valid current setpoints from sofb array
        current = curr_sp[indcs_sofb]
        notnan = ~_np.isnan(current)
        current = current[notnan]

        # initialize setpoint
        readback = udc.sofb_current_rb_get()  # stores last setpoint
        if readback is None:
            setpoint = _np.zeros(PSSOFB._MAX_NR_DEVS)
        else:
            setpoint = _np.asarray(readback)

        # update setpoint
        setpoint[indcs_bsmp[notnan]] = current

        # --- bsmp communication ---
        udc.sofb_current_set(tuple(setpoint))

        # update sofb_current_readback_ref
        current = udc.sofb_current_readback_ref_get()
        if current is None:
            return
        self._sofb_current_readback_ref[indcs_sofb] = current[indcs_bsmp]

    def _bsmp_current_setpoint_update(self, bbbname, curr_sp):
        """."""
        self._bsmp_current_setpoint(bbbname, curr_sp)
        self._bsmp_current_update(bbbname)

    def _bsmp_state_update(self, bbbname):
        udc = self.udc[bbbname]
        devices = PSSOFB.BBB2DEVS[bbbname]
        group_id = _const_fbp.G_ALL
        self._dev_state[bbbname] = dict()

        # set dev_ack to False to all devices
        dev_ack = self._dev_ack[bbbname]
        for _, dev_id in devices:
            dev_ack[dev_id] = False

        # execute function for devices
        try:
            for _, dev_id in devices:
                resp = udc[dev_id].read_group_of_variables(group_id=group_id)
                ack, data = resp
                # check anomalous response
                if ack != _const_bsmp.ACK_OK:
                    print(('PSSOFB: could not read '
                           'group of variables id:{}').format(group_id))
                else:
                    self._dev_state[bbbname][dev_id] = data
                    dev_ack[dev_id] = True
        except _SerialError:
            # no communication
            print('PSSOFB: SerialError in bsmp_state_update!')

    def _bsmp_execute_function(self, bbbname, *args):
        """."""
        udc = self.udc[bbbname]
        devices = PSSOFB.BBB2DEVS[bbbname]
        function_id, *args = args

        # transform empty tuple in None
        args = args if args else None

        # set dev_ack to False to all devices
        dev_ack = self._dev_ack[bbbname]
        for _, dev_id in devices:
            dev_ack[dev_id] = False

        # execute function for devices
        try:
            for _, dev_id in devices:
                resp = udc[dev_id].execute_function(function_id, args)
                ack, data = resp
                # check anomalous response
                if ack != _const_bsmp.ACK_OK:
                    print('PSSOFB: anomalous response !')
                    udc[dev_id].anomalous_response(
                        _const_bsmp.CMD_EXECUTE_FUNCTION, ack,
                        device_id=dev_id,
                        function_id=function_id,
                        data_len=len(data),
                        data_type=type(data),
                        data=data)
                else:
                    dev_ack[dev_id] = True
        except _SerialError:
            # no communication
            return None
        except TypeError:
            # anomalous response triggered unexpected code error
            print('--- debug ----')
            print('devices     : ', devices)
            print('dev_id      : ', dev_id)
            print('function_id : ', function_id)
            print('resp        : ', resp)
            print('data        : ', data)
            raise

    @staticmethod
    def _create_pru(ethbridgeclnt_class):
        """."""
        pru = dict()
        for bbbname in PSSOFB.BBBNAMES:
            pru[bbbname] = _PRU(ethbridgeclnt_class, bbbname)
        return pru

    def _create_udc(self):
        """."""
        udc = dict()
        for bbbname, bsmpdevs in PSSOFB.BBB2DEVS.items():
            pru = self.pru[bbbname]
            devids = [bsmp[1] for bsmp in bsmpdevs]
            udc[bbbname] = _UDC(pru=pru, psmodel='FBP', device_ids=devids)
        return udc

    def _init_connectors(self, ethbridgeclnt_class):
        """."""
        # NOTE: Setting Channel.LOCK is necessary for the threads to interact with
        # corresponding beaglebones in parallel. It should be dropped once
        # write_then_read in eth-bridge is adopted!
        _Channel.LOCK = None

        self.pru = PSSOFB._create_pru(ethbridgeclnt_class)
        self.udc = self._create_udc()
        self._add_groups_of_variables()

    @staticmethod
    def _update_bbb2devs():
        """."""
        for bbbname in PSSOFB.BBBNAMES:
            devs = _PSSearch.conv_bbbname_2_bsmps(bbbname)
            PSSOFB.BBB2DEVS[bbbname] = devs

    def _add_groups_of_variables(self):
        # add groups of variaable with id>2 to entities class, as
        # required for message-processing verification class objects
        # to work.
        for udc in self.udc.values():
            udc.add_groups_of_variables()

    def _create_indices(self):
        """."""
        PSSOFB._update_bbb2devs()
        indcs_bsmp = dict()
        indcs_sofb = dict()
        for bbbname in PSSOFB.BBBNAMES:
            devs = PSSOFB.BBB2DEVS[bbbname]
            # add indcs_udc to dictionary
            indcs_bsmp_ = list()
            indcs_sofb_ = list()
            for psname, bsmpid in devs:
                if psname in self._sofb_psnames:
                    indcs_bsmp_.append(bsmpid-1)
                    indcs_sofb_.append(self._sofb_psnames.index(psname))
            indcs_bsmp[bbbname] = _np.array(indcs_bsmp_)
            indcs_sofb[bbbname] = _np.array(indcs_sofb_)

        return indcs_bsmp, indcs_sofb

    def _update_currents(self, bbbname):
        """."""
        udc = self.udc[bbbname]

        # get indices
        indcs_sofb = self.indcs_sofb[bbbname]
        indcs_bsmp = self.indcs_bsmp[bbbname]

        # update -RB
        current = udc.sofb_current_rb_get()
        if current is None:
            return
        self._sofb_current_rb[indcs_sofb] = current[indcs_bsmp]

        # update Ref-Mon
        current = udc.sofb_current_refmon_get()
        self._sofb_current_refmon[indcs_sofb] = current[indcs_bsmp]

        # update -Mon
        current = udc.sofb_current_mon_get()
        self._sofb_current_mon[indcs_sofb] = current[indcs_bsmp]

    def _sofb_state_variable(self, var_id, dtype=int):
        values = _np.zeros(len(self._sofb_psnames), dtype=dtype)
        for bbbname in PSSOFB.BBBNAMES:
            # beaglebone dev state
            bbbstate = self._dev_state[bbbname]
            # get state values
            bbbvalues = _np.zeros(PSSOFB._MAX_NR_DEVS, dtype=dtype)
            for _, dev_id in self.BBB2DEVS[bbbname]:
                devstate = bbbstate[dev_id]
                bbbvalues[dev_id-1] = devstate[var_id]
            # get indices
            indcs_sofb = self.indcs_sofb[bbbname]
            indcs_bsmp = self.indcs_bsmp[bbbname]
            values[indcs_sofb] = bbbvalues[indcs_bsmp]
        return values

    def _sofb_pscstatus_get(self, attr):
        status = self._sofb_state_variable(
            var_id=_const_fbp.V_PS_STATUS, dtype=int)
        values = _np.zeros(len(self._sofb_psnames), dtype=int)
        for i in range(len(self._sofb_psnames)):
            self._pscstatus[i].ps_status = status[i]
            values[i] = getattr(self._pscstatus[i], attr)
        return values

    def _get_strenconv(self):
        # 1. create pstype to StrengthConv dictionary.
        # 2. create pstype to corrector index dictionnary.
        pstype_2_index = dict()
        pstype_2_sconv = dict()
        psnames = self._sofb_psnames
        for i, psname in enumerate(psnames):
            pstype = _PSSearch.conv_psname_2_pstype(psname)
            if pstype not in pstype_2_index:
                pstype_2_index[pstype] = []
            pstype_2_index[pstype].append(i)
            if pstype not in pstype_2_sconv:
                # sconv = _NormFact.create(psname.replace(':PS', ':MA'))
                sconv = _StrengthConv(
                    psname, PSSOFB._dipole_propty, auto_mon=True)
                pstype_2_sconv[pstype] = sconv

        # convert index to numpy array
        for pstype in pstype_2_index:
            pstype_2_index[pstype] = _np.asarray(pstype_2_index[pstype])

        # wait for connection
        for sconv in pstype_2_sconv.values():
            sconv.wait_for_connection()

        return pstype_2_index, pstype_2_sconv

    def _conv_curr2stren(self, current):
        # benchmarks:
        # 0.163 ms (normalizer)
        # 0.277 ms (sconv)
        strength = _np.zeros(len(current))
        for pstype, index in self._pstype_2_index.items():
            sconv = self._pstype_2_sconv[pstype]
            value = current[index]
            # stren = sconv.conv_current_2_strength(
            #     currents=value, strengths_dipole=self._strengths_dipole)
            stren = sconv.conv_current_2_strength(currents=value)
            strength[index] = stren
        return strength

    def _conv_stren2curr(self, strength):
        # benchmarks:
        # 0.112 ms (normalizer)
        # 0.189 ms (sconv)
        current = _np.full(len(strength), _np.nan, dtype=float)
        for pstype, index in self._pstype_2_index.items():
            sconv = self._pstype_2_sconv[pstype]
            value = strength[index]
            # idcs = ~_np.isnan(value)
            # curr = sconv.conv_strength_2_current(
            #     strengths=value[idcs],
            #     strengths_dipole=self._strengths_dipole)
            # curr = sconv.conv_strength_2_current(strengths=value[idcs])
            # current[index[idcs]] = curr
            curr = sconv.conv_strength_2_current(strengths=value)
            current[index] = curr
        return current

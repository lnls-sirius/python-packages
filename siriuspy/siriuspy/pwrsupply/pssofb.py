"""PSSOFB class."""
from copy import deepcopy as _dcopy
from collections.abc import Iterable
import multiprocessing as _mp
from multiprocessing import sharedctypes as _shm

import numpy as _np
from epics import get_pv as _get_pv

from ..thread import AsyncWorker as _AsyncWorker
from ..search import PSSearch as _PSSearch
from ..bsmp import SerialError as _SerialError
from ..bsmp import constants as _const_bsmp
from ..devices import StrengthConv as _StrengthConv
from ..epics import CAProcessSpawn as _Process

from .bsmp.constants import ConstFBP as _const_fbp
from .bsmp.commands import FBP as _FBP
from .csdev import PSSOFB_MAX_NR_UDC as _PSSOFB_MAX_NR_UDC
from .csdev import UDC_MAX_NR_DEV as _UDC_MAX_NR_DEV
from .pructrl.pru import PRU as _PRU
from .pructrl.udc import UDC as _UDC
from .psctrl.pscstatus import PSCStatus as _PSCStatus


class _BBBThread(_AsyncWorker):
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


class UnitConverter:
    """."""

    DIPOLE_PROPTY = 'Ref-Mon'

    def __init__(self, psnames):
        """."""
        self.psnames = psnames
        self._pstype_2_index, self._pstype_2_sconv = self._init_strenconv()

    def _init_strenconv(self):
        # 1. create pstype to StrengthConv dictionary.
        # 2. create pstype to corrector index dictionnary.
        pstype_2_index = dict()
        pstype_2_sconv = dict()
        psnames = self.psnames
        for i, psname in enumerate(psnames):
            pstype = _PSSearch.conv_psname_2_pstype(psname)
            if pstype not in pstype_2_index:
                pstype_2_index[pstype] = []
            pstype_2_index[pstype].append(i)
            if pstype not in pstype_2_sconv:
                # sconv = _NormFact.create(psname.replace(':PS', ':MA'))
                sconv = _StrengthConv(
                    psname, UnitConverter.DIPOLE_PROPTY, auto_mon=True)
                pstype_2_sconv[pstype] = sconv

        # convert index to numpy array
        for pstype in pstype_2_index:
            pstype_2_index[pstype] = _np.asarray(pstype_2_index[pstype])

        # wait for connection
        for sconv in pstype_2_sconv.values():
            sconv.wait_for_connection()

        return pstype_2_index, pstype_2_sconv

    def conv_curr2stren(self, current):
        """."""
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

    def conv_stren2curr(self, strength):
        """."""
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


class PSConnSOFB:
    """."""

    MAX_NR_DEVS = _PSSOFB_MAX_NR_UDC * _UDC_MAX_NR_DEV

    PS_PWRSTATE = _PSCStatus.PWRSTATE
    PS_OPMODE = _PSCStatus.OPMODE

    def __init__(self, ethbridgeclnt_class, bbbnames=None, mproc=None,
                 sofb_update_iocs=False):
        """."""
        # check arguments
        if mproc is not None and \
                (not isinstance(mproc, dict) or
                 set(mproc.keys()) != {'rbref', 'ref', 'fret'}):
            raise ValueError('Invalid mproc dictionary!')

        self._acc = 'SI'
        self._pru = None
        self._udc = None
        self.bbbnames = bbbnames or _dcopy(PSSOFB.BBBNAMES)
        self.bbb2devs = dict()

        # flag that controls sending sofbupdate signal to IOCs
        self._sofb_update_iocs = sofb_update_iocs

        self._sofb_psnames = \
            PSNamesSOFB.get_psnames_ch(self._acc) + \
            PSNamesSOFB.get_psnames_cv(self._acc)

        # snapshot of sofb current values
        ncorrs = len(self._sofb_psnames)
        arr = _np.zeros(ncorrs, dtype=float)
        self._sofb_current_rb = arr.copy()
        self._sofb_current_mon = arr.copy()

        if mproc:
            self._sofb_current_readback_ref = mproc['rbref']
            self._sofb_current_refmon = mproc['ref']
            self._sofb_func_return = mproc['fret']
        else:
            self._sofb_current_readback_ref = arr.copy()
            self._sofb_current_refmon = arr.copy()
            self._sofb_func_return = _np.zeros(ncorrs, dtype=int)

        # create sofb and bsmp indices
        self.indcs_bsmp, self.indcs_sofb = self._create_indices()

        # initialize connector objects for bsmp communications.
        self._pru, self._udc = self._init_connectors(ethbridgeclnt_class)

        # dictionaries with comm. ack, state snapshot of all correctors
        # states and threads
        self._dev_ack, self._dev_state, self._threads, self._pvobjs = \
            self._init_threads_dev_state()

        # power supply status objects
        self._pscstatus = [_PSCStatus() for _ in self._sofb_psnames]

        # strength to current converters
        self._strengths_dipole = 3.0  # [GeV]
        if mproc is None:
            self.converter = UnitConverter(self._sofb_psnames)

    def pru(self):
        """Return Beagle-name to PRU-object dictionary."""
        return self._pru

    def udc(self):
        """Return Beagle-name to UDC-object dictionary."""
        return self._udc

    # --- threads manipulation methods ---

    def threads_shutdown(self):
        """Stop BBB threads."""
        for thr in self._threads:
            thr.stop()
        for thr in self._threads:
            thr.join()

    # --- bsmp methods: invoke communications with correctors ---

    def bsmp_sofb_current_set(self, current):
        """Send current sofb setpoint to power supplies."""
        self._parallel_execution(self._bsmp_current_setpoint, (current, ))

    def bsmp_sofb_kick_set(self, kick):
        """Send kick sofb setpoint to power supplies."""
        current = self.converter.conv_stren2curr(kick)
        self.bsmp_sofb_current_set(current)
        return current

    def bsmp_sofb_current_set_update(self, current):
        """Send current sofb setpoint to power supplies and update."""
        self._parallel_execution(self._bsmp_current_setpoint_update, current)

    def bsmp_sofb_kick_set_update(self, kick):
        """Send kick sofb setpoint to power supplies and update."""
        current = self.converter.conv_stren2curr(kick)
        self.bsmp_sofb_current_set_update(current)
        return current

    def bsmp_update_sofb(self):
        """Update SOFB currents by sending correctors bsmp requests."""
        self._parallel_execution(self._bsmp_update_current)

    def bsmp_update_state(self):
        """Receive from correctors variables and update object attributes."""
        self._parallel_execution(self._bsmp_update_state)

    def bsmp_pwrstate_on(self):
        """Turn all correctors on and then update state."""
        args = (_const_fbp.F_TURN_ON, )
        self._parallel_execution(self._bsmp_execute_function, args)
        self._parallel_execution(self._bsmp_update_state)

    def bsmp_pwrstate_off(self):
        """Turn all correctors off and then update state."""
        args = (_const_fbp.F_TURN_OFF, )
        self._parallel_execution(self._bsmp_execute_function, args)
        self._parallel_execution(self._bsmp_update_state)

    def bsmp_slowref(self):
        """Set all correctors to SlowRef opmode and then update state."""
        args = (_const_fbp.F_SELECT_OP_MODE, _PSCStatus.STATES.SlowRef)
        self._parallel_execution(self._bsmp_execute_function, args)
        self._parallel_execution(self._bsmp_update_state)

    def bsmp_slowrefsync(self):
        """Turn all correctors ro SlowRefSync opmode and then update state."""
        args = (_const_fbp.F_SELECT_OP_MODE, _PSCStatus.STATES.SlowRefSync)
        self._parallel_execution(self._bsmp_execute_function, args)
        self._parallel_execution(self._bsmp_update_state)

    # --- sofb-vector object attribute methods (no comm.) ---

    @property
    def sofb_psnames(self):
        """Return corrector names in SOFB order."""
        return self._sofb_psnames

    @property
    def sofb_kick_refmon(self):
        """Return SOFB kick Ref-Mon vector, as last updated."""
        current = self.sofb_current_refmon
        strength = self.converter.conv_curr2stren(current)
        return strength

    @property
    def sofb_kick_readback_ref(self):
        """Return SOFB kick from current_readback_ref from last setpoint."""
        current = self.sofb_current_readback_ref
        strength = self.converter.conv_curr2stren(current)
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
        return self._sofb_current_readback_ref.copy()

    @property
    def sofb_func_return(self):
        """Return function return from last SOFB communication."""
        return self._sofb_func_return.copy()

    def sofb_state_variable_get(self, var_id, dtype=float):
        """Return SOFB vector with bsmp variable values, as last updated."""
        return self._sofb_state_variable(var_id=var_id, dtype=dtype)

    @property
    def sofb_opmode(self):
        """Return SOFB vector with OpMode-Sts values, as last updated."""
        return self._sofb_pscstatus_get('ioc_opmode')

    @property
    def sofb_pwrstate(self):
        """Return SOFB vector with PwrState-Sts values, as last updated."""
        return self._sofb_pscstatus_get('ioc_pwrstate')

    @property
    def sofb_interlock_hard(self):
        """Return SOFB vector with IntlkHard-Sts values, as last updated."""
        return self._sofb_state_variable(
            _const_fbp.V_PS_HARD_INTERLOCKS, dtype=int)

    @property
    def sofb_interlock_soft(self):
        """Return SOFB vector with IntlkSoft-Sts values, as last updated."""
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

    def sofb_conv_psname_2_index(self, psname):
        """."""
        return self._sofb_psnames.index(psname)

    # --- private methods: bsmp comm in parallel ---

    def _parallel_execution(self, target, args=None):
        """Execute 'method' in parallel."""
        # run threads
        for thr in self._threads:
            if not thr.configure_new_run(target, args=args):
                raise RuntimeError('Thread is not ready for job!')
        # wait for run to finish
        for thr in self._threads:
            thr.wait_ready()

    def _bsmp_update_current(self, bbbname):
        """Update SOFB parameters of a single beaglebone."""
        udc = self._udc[bbbname]

        # --- bsmp communication ---
        udc.sofb_update()

        # update currents
        self._update_currents(bbbname)

    def _bsmp_current_setpoint(self, bbbname, curr_sp):
        """Set currents for a single beaglebone."""
        udc = self._udc[bbbname]

        # get indices
        indcs_sofb = self.indcs_sofb[bbbname]
        indcs_bsmp = self.indcs_bsmp[bbbname]

        # get valid current setpoints from sofb array
        current = curr_sp[indcs_sofb]

        # initialize setpoint
        readback = udc.sofb_current_rb_get()  # stores last setpoint
        if readback is None:
            setpoint = _np.zeros(PSConnSOFB.MAX_NR_DEVS)
        else:
            setpoint = _np.asarray(readback)

        # update setpoint
        setpoint[indcs_bsmp] = current

        # --- bsmp communication ---
        udc.sofb_current_set(setpoint)

        # update sofb_func_return
        func_return = udc.sofb_func_return_get()
        self._sofb_func_return[indcs_sofb] = func_return[indcs_bsmp]

        # update sofb_current_readback_ref
        current = udc.sofb_current_readback_ref_get()
        if current is None:
            return
        self._sofb_current_readback_ref[indcs_sofb] = current[indcs_bsmp]

        # send signal to IOC to update one power supply state
        if self._sofb_update_iocs:
            pvobj = self._pvobjs[bbbname]
            pvobj.put(1, wait=False)  # send signal to IOC

    def _bsmp_current_setpoint_update(self, bbbname, curr_sp):
        """."""
        self._bsmp_current_setpoint(bbbname, curr_sp)
        self._bsmp_update_current(bbbname)

    def _bsmp_update_state(self, bbbname):
        udc = self._udc[bbbname]
        devices = self.bbb2devs[bbbname]
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
        udc = self._udc[bbbname]
        devices = self.bbb2devs[bbbname]
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
                    if isinstance(data, str):
                        data = ord(data)
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

    # --- private methods: class initializations. ---

    def _create_indices(self):
        """."""
        self._update_bbb2devs()
        indcs_bsmp = dict()
        indcs_sofb = dict()
        for bbbname in self.bbbnames:
            devs = self.bbb2devs[bbbname]
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

    def _init_connectors(self, ethbridgeclnt_class):
        """."""
        pru, udc = self._create_pru_udc(ethbridgeclnt_class)
        self._add_groups_of_variables(udc)

        return pru, udc

    def _add_groups_of_variables(self, udc):
        # add groups of variaable with id>2 to entities class, as
        # required for message-processing verification class objects
        # to work.
        for udc_ in udc.values():
            udc_.add_groups_of_variables()

    def _update_currents(self, bbbname):
        """."""
        udc = self._udc[bbbname]

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
        for bbbname in self.bbbnames:
            # beaglebone dev state
            bbbstate = self._dev_state[bbbname]
            if not bbbstate:
                raise KeyError('PSSOFB.bsmp_state_update not invoked first!')
            # get state values
            bbbvalues = _np.zeros(PSConnSOFB.MAX_NR_DEVS, dtype=dtype)
            for _, dev_id in self.bbb2devs[bbbname]:
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

    def _init_threads_dev_state(self):
        dev_ack = dict()  # last ack state of bsmp comm.
        dev_state = dict()  # snapshot of device variable values
        threads = list()  # threads to run BBB methods
        pvobjs = dict()  # SOFBUpdate PVs
        for bbbname, bsmpdevs in self.bbb2devs.items():
            dev_ack[bbbname] = {bsmp[1]: True for bsmp in bsmpdevs}
            dev_state[bbbname] = {bsmp[1]: dict() for bsmp in bsmpdevs}
            if self._sofb_update_iocs:
                pvname = bsmpdevs[0][0] + ':SOFBUpdate-Cmd'
                pvobjs[bbbname] = _get_pv(pvname)
            thread = _BBBThread(name=bbbname)
            thread.start()
            threads.append(thread)
        return dev_ack, dev_state, threads, pvobjs

    def _update_bbb2devs(self):
        """."""
        for bbbname in self.bbbnames:
            devs = _PSSearch.conv_bbbname_2_bsmps(bbbname)
            self.bbb2devs[bbbname] = devs

    def _create_pru_udc(self, ethbridgeclnt_class):
        """."""
        pru, udc = dict(), dict()

        # signal FBP comm class not to print comm. error statements
        _FBP.SOFB_PRINT_COMM_ERRORS = False

        for bbbname, bsmpdevs in self.bbb2devs.items():

            # create PRU object for bsmp communication
            pru_ = _PRU(ethbridgeclnt_class, bbbname)

            # for a given beagle, gather devices ids
            device_ids = [bsmp[1] for bsmp in bsmpdevs]

            # create UDC object to access power supply bsmp comm. methods
            udc_ = _UDC(pru=pru_, psmodel='FBP', device_ids=device_ids)

            # add PRU and UDC objects to disctionaries.
            pru[bbbname] = pru_
            udc[bbbname] = udc_

        return pru, udc


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

    def __init__(self, ethbridgeclnt_class, nr_procs=8, asynchronous=False,
                 sofb_update_iocs=False):
        """."""
        self._acc = 'SI'
        self._async = asynchronous
        self._sofb_update_iocs = sofb_update_iocs

        self._sofb_psnames = \
            PSNamesSOFB.get_psnames_ch(self._acc) + \
            PSNamesSOFB.get_psnames_cv(self._acc)

        # snapshot of sofb current values
        ncorrs = len(self._sofb_psnames)
        arr = _np.zeros(ncorrs, dtype=float)
        self._sofb_current_readback_ref = arr.copy()
        self._sofb_current_refmon = arr.copy()
        self._sofb_func_return = _np.zeros(ncorrs, dtype=int)

        # Unit converter.
        self.converter = UnitConverter(self._sofb_psnames)

        # Worker Processes control and synchronization
        self._ethbridge_cls = ethbridgeclnt_class
        self._nr_procs = nr_procs
        self._doneevts = []
        self._procs = []
        self._pipes = []

    # --- General class properties ---

    @property
    def asynchronous(self):
        """."""
        return self._async

    @asynchronous.setter
    def asynchronous(self, val):
        self._async = bool(val)

    def wait(self, timeout=None):
        """."""
        for doneevt in self._doneevts:
            if not doneevt.wait(timeout=timeout):
                return False
        return True

    def is_ready(self):
        """."""
        for doneevt in self._doneevts:
            if not doneevt.is_set():
                return False
        return True

    # --- processes manipulation methods ---

    def processes_start(self):
        """."""
        # get the start method of the Processes that will be launched:
        spw = _mp.get_context('spawn')

        # Create shared memory objects to be shared with worker processes.
        arr = self._sofb_current_readback_ref

        rbref = _shm.Array(_shm.ctypes.c_double, arr.size, lock=False)
        self._sofb_current_readback_ref = _np.ndarray(
            arr.shape, dtype=arr.dtype, buffer=memoryview(rbref))

        ref = _shm.Array(_shm.ctypes.c_double, arr.size, lock=False)
        self._sofb_current_refmon = _np.ndarray(
            arr.shape, dtype=arr.dtype, buffer=memoryview(ref))

        fret = _shm.Array(_shm.ctypes.c_int, arr.size, lock=False)
        self._sofb_func_return = _np.ndarray(
            arr.shape, dtype=_np.int32, buffer=memoryview(fret))

        # Unit converter.
        self.converter = UnitConverter(self._sofb_psnames)

        # subdivide the pv list for the processes
        nr_bbbs = len(PSSOFB.BBBNAMES)
        div = nr_bbbs // self._nr_procs
        rem = nr_bbbs % self._nr_procs
        sub = [div*i + min(i, rem) for i in range(self._nr_procs+1)]
        for i in range(self._nr_procs):
            bbbnames = PSSOFB.BBBNAMES[sub[i]:sub[i+1]]
            # NOTE: It is crucial to use the Event class from the appropriate
            # context, otherwise it will fail for 'spawn' start method.
            evt = spw.Event()
            evt.set()
            theirs, mine = spw.Pipe(duplex=False)
            proc = _Process(
                target=PSSOFB._run_process,
                args=(self._ethbridge_cls, bbbnames, theirs, evt,
                      arr.shape, rbref, ref, fret, self._sofb_update_iocs),
                daemon=True)
            proc.start()
            self._procs.append(proc)
            self._doneevts.append(evt)
            self._pipes.append(mine)

    def processes_shutdown(self):
        """."""
        for pipe in self._pipes:
            pipe.send(None)
            pipe.close()
        for proc in self._procs:
            proc.join()

    # --- bspm communication methods ---

    def bsmp_sofb_current_set(self, current):
        """Send current sofb setpoint to power supplies."""
        self._parallel_execution('bsmp_sofb_current_set', (current, ))

    def bsmp_sofb_kick_set(self, kick):
        """Send kick sofb setpoint to power supplies."""
        current = self.converter.conv_stren2curr(kick)
        self.bsmp_sofb_current_set(current)

    def bsmp_sofb_current_set_update(self, current):
        """Send current sofb setpoint to power supplies and update."""
        self._parallel_execution('bsmp_sofb_current_set_update', (current, ))

    def bsmp_sofb_kick_set_update(self, kick):
        """Send kick sofb setpoint to power supplies and update."""
        current = self.converter.conv_stren2curr(kick)
        self.bsmp_sofb_current_set_update(current)

    def bsmp_update_sofb(self):
        """Update SOFB currents by sending correctors bsmp requests."""
        self._parallel_execution('bsmp_update_sofb')

    def bsmp_update_state(self):
        """Receive from correctors variables and update object attributes."""
        self._parallel_execution('bsmp_update_state')

    def bsmp_pwrstate_on(self):
        """Turn all correctors on and then update state."""
        self._parallel_execution('bsmp_pwrstate_on')

    def bsmp_pwrstate_off(self):
        """Turn all correctors off and then update state."""
        self._parallel_execution('bsmp_pwrstate_off')

    def bsmp_slowref(self):
        """Set all correctors to SlowRef opmode and then update state."""
        self._parallel_execution('bsmp_slowref')

    def bsmp_slowrefsync(self):
        """Turn all correctors ro SlowRefSync opmode and then update state."""
        self._parallel_execution('bsmp_slowrefsync')

    # --- sofb-vector object attribute methods (no comm.) ---

    @property
    def sofb_psnames(self):
        """Return corrector names in SOFB order."""
        return self._sofb_psnames

    @property
    def sofb_current_refmon(self):
        """Return SOFB current readback after last setpoint."""
        return self._sofb_current_refmon.copy()

    @property
    def sofb_current_readback_ref(self):
        """Return SOFB current readback after last setpoint."""
        return self._sofb_current_readback_ref.copy()

    @property
    def sofb_kick_refmon(self):
        """Return SOFB kick from current_readback_ref from last setpoint."""
        return self.converter.conv_curr2stren(self.sofb_current_refmon)

    @property
    def sofb_kick_readback_ref(self):
        """Return SOFB kick from current_readback_ref from last setpoint."""
        return self.converter.conv_curr2stren(self.sofb_current_readback_ref)

    @property
    def sofb_func_return(self):
        """Return SOFB function return from last communication."""
        return self._sofb_func_return.copy()

    @staticmethod
    def sofb_vector_issame(vector1, vector2):
        """Check if two sofb vectors are identical within float32 precision."""
        if len(vector1) != len(vector2):
            return False
        # comparison
        vec1 = _np.asarray(vector1, dtype=_np.float32)
        vec2 = _np.asarray(vector2, dtype=_np.float32)
        return _np.all(vec1 == vec2)

    def sofb_conv_psname_2_index(self, psname):
        """."""
        return self._sofb_psnames.index(psname)

    @staticmethod
    def _run_process(
            ethbridgeclnt_class, bbbnames, pipe, doneevt,
            shape, rbref, ref, fret, sofb_update_iocs):
        """."""
        mproc = {
            'rbref': _np.ndarray(shape, dtype=float, buffer=memoryview(rbref)),
            'ref': _np.ndarray(shape, dtype=float, buffer=memoryview(ref)),
            'fret': _np.ndarray(shape, dtype=_np.int32,
                                buffer=memoryview(fret)),
            }
        psconnsofb = PSConnSOFB(
            ethbridgeclnt_class, bbbnames, mproc=mproc,
            sofb_update_iocs=sofb_update_iocs)

        while True:
            rec = pipe.recv()
            if not rec:
                break
            meth, args = rec
            if isinstance(meth, str):
                if isinstance(args, Iterable):
                    getattr(psconnsofb, meth)(*args)
                else:
                    getattr(psconnsofb, meth)()
                doneevt.set()
        psconnsofb.threads_shutdown()
        pipe.close()

    # --- private methods: get properties ---

    def _parallel_execution(self, target_name, args=None):
        """Execute 'method' in parallel."""
        for pipe, doneevt in zip(self._pipes, self._doneevts):
            doneevt.clear()
            pipe.send((target_name, args))

        if not self._async:
            self.wait()

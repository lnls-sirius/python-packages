"""Power supply controller classes."""

import time as _time
from threading import Thread as _Thread
import random as _random
import numpy as _np

from siriuspy import util as _util
from siriuspy.csdevice.pwrsupply import Const as _PSConst

from siriuspy.bsmp import Const as _BSMPConst
from siriuspy.bsmp import BSMPSim as _BSMPSim

from . import bsmp as _psbsmp
from .status import PSCStatus as _PSCStatus
from .siggen import SignalFactory as _SignalFactory

__version__ = _util.get_last_commit_hash()


# --- classes that implement specialized methods ---


class _Spec:

    I_LOAD_FLUCTUATION_RMS = 0.01  # [A]

    def _get_constants(self):
        raise NotImplementedError()

    def _get_monvar_ids(self):
        return ()

    def _get_init_value(self):
        return 0.0

    def _get_monvar_fluctuation_rms(self, var_id):
        raise NotImplementedError()


class _Spec_FBP(_Spec):
    """Spec FBP."""

    def _get_constants(self):
        return _psbsmp.ConstFBP

    def _get_monvar_ids(self):
        return (_psbsmp.ConstFBP.V_I_LOAD, )

    def _get_monvar_fluctuation_rms(self, var_id):
        return _Spec.I_LOAD_FLUCTUATION_RMS


class _Spec_FBP_DCLink(_Spec):
    """Spec FBP_DCLink."""

    _monvar_rms = {
        _psbsmp.ConstFBP_DCLink.V_V_OUT: 0.001,
        _psbsmp.ConstFBP_DCLink.V_V_OUT_1: 0.001,
        _psbsmp.ConstFBP_DCLink.V_V_OUT_2: 0.001,
        _psbsmp.ConstFBP_DCLink.V_V_OUT_3: 0.001,
        _psbsmp.ConstFBP_DCLink.V_DIG_POT_TAP: 0,
    }

    def _get_constants(self):
        return _psbsmp.ConstFBP_DCLink

    def _get_monvar_ids(self):
        return tuple(_Spec_FBP_DCLink._monvar_rms.keys())

    def _get_monvar_fluctuation_rms(self, var_id):
        return _Spec_FBP_DCLink._monvar_rms[var_id]


class _Spec_FAC_DCDC(_Spec):
    """Spec FAC_DCDC."""

    def _get_constants(self):
        return _psbsmp.ConstFAC_DCDC

    def _get_monvar_ids(self):
        return (_psbsmp.ConstFAC_DCDC.V_I_LOAD_MEAN,
                _psbsmp.ConstFAC_DCDC.V_I_LOAD1,
                _psbsmp.ConstFAC_DCDC.V_I_LOAD2)

    def _get_monvar_fluctuation_rms(self, var_id):
        return _Spec.I_LOAD_FLUCTUATION_RMS


class _Spec_FAC_2P4S_DCDC(_Spec):
    """Spec FAC_2P4S_DCDC."""

    def _get_constants(self):
        return _psbsmp.ConstFAC_2P4S_DCDC

    def _get_monvar_ids(self):
        return (_psbsmp.ConstFAC_2P4S_DCDC.V_I_LOAD_MEAN,
                _psbsmp.ConstFAC_2P4S_DCDC.V_I_LOAD1,
                _psbsmp.ConstFAC_2P4S_DCDC.V_I_LOAD2)

    def _get_monvar_fluctuation_rms(self, var_id):
        return _Spec.I_LOAD_FLUCTUATION_RMS


class _Spec_FAC_2S_DCDC(_Spec):
    """Spec FAC_2S_DCDC."""

    def _get_constants(self):
        return _psbsmp.ConstFAC_2S_DCDC

    def _get_monvar_ids(self):
        return (_psbsmp.ConstFAC_2S_DCDC.V_I_LOAD_MEAN,
                _psbsmp.ConstFAC_2S_DCDC.V_I_LOAD1,
                _psbsmp.ConstFAC_2S_DCDC.V_I_LOAD2)

    def _get_monvar_fluctuation_rms(self, var_id):
        return _Spec.I_LOAD_FLUCTUATION_RMS


class _Spec_FAC_2P4S_ACDC(_Spec):
    """Spec FAC_2P4S_ACDC."""

    def _get_constants(self):
        return _psbsmp.ConstFAC_2P4S_ACDC


class _Spec_FAC_2S_ACDC(_Spec):
    """Spec FAC_2S_ACDC."""

    def _get_constants(self):
        return _psbsmp.ConstFAC_2S_ACDC


class _Spec_FAP(_Spec):
    """Spec FAP."""

    def _get_constants(self):
        return _psbsmp.ConstFAP

    def _get_monvar_ids(self):
        return (_psbsmp.ConstFAP.V_I_LOAD_MEAN,
                _psbsmp.ConstFAP.V_I_LOAD1,
                _psbsmp.ConstFAP.V_I_LOAD2)

    def _get_monvar_fluctuation_rms(self, var_id):
        return _Spec.I_LOAD_FLUCTUATION_RMS


class _Spec_FAP_4P(_Spec):
    """Spec FAP_4P."""

    def _get_constants(self):
        return _psbsmp.ConstFAP_4P

    def _get_monvar_ids(self):
        return (_psbsmp.ConstFAP_4P.V_I_LOAD_MEAN,
                _psbsmp.ConstFAP_4P.V_I_LOAD1,
                _psbsmp.ConstFAP_4P.V_I_LOAD2)

    def _get_monvar_fluctuation_rms(self, var_id):
        return _Spec.I_LOAD_FLUCTUATION_RMS


class _Spec_FAP_2P2S(_Spec):
    """Spec FAP_2P2S."""

    def _get_constants(self):
        return _psbsmp.ConstFAP_2P2S

    def _get_monvar_ids(self):
        return (_psbsmp.ConstFAP_2P2S.V_I_LOAD_MEAN,
                _psbsmp.ConstFAP_2P2S.V_I_LOAD1,
                _psbsmp.ConstFAP_2P2S.V_I_LOAD2)

    def _get_monvar_fluctuation_rms(self, var_id):
        return _Spec.I_LOAD_FLUCTUATION_RMS


# --- simulated OpMode state classes ---


class _OpModeSimState:
    """Represent operation modes."""

    def __init__(self):
        self._c = self._get_constants()
        self._monvars = self._get_monvar_ids()

    def read_variable(self, variables, var_id):
        """Read variable."""
        for monvar_id in self._monvars:
            if var_id == monvar_id:
                return variables[var_id] + \
                    _random.gauss(
                        0.0, self._get_monvar_fluctuation_rms(monvar_id))
        value = variables[var_id]
        return value

    def turn_on(self, variables):
        """Turn ps on."""
        ps_status = variables[self._c.V_PS_STATUS]
        psc_status = _PSCStatus(ps_status=ps_status)
        if psc_status.ioc_pwrstate == _PSConst.PwrStateSel.Off:
            # Set PSController status
            value_init = self._get_init_value()
            psc_status.ioc_pwrstate = _PSConst.PwrStateSel.On
            psc_status.ioc_opmode = _PSConst.OpMode.SlowRef
            variables[self._c.V_PS_STATUS] = psc_status.ps_status
            # Set currents to 0
            variables[self._c.V_PS_SETPOINT] = value_init
            variables[self._c.V_PS_REFERENCE] = value_init
            for monvar_id in self._monvars:
                variables[monvar_id] = value_init

    def turn_off(self, variables):
        """Turn ps off."""
        ps_status = variables[self._c.V_PS_STATUS]
        psc_status = _PSCStatus(ps_status=ps_status)
        if psc_status.ioc_pwrstate == _PSConst.PwrStateSel.On:
            value_init = self._get_init_value()
            # Set PSController status
            psc_status.ioc_pwrstate = _PSConst.PwrStateSel.Off
            variables[self._c.V_PS_STATUS] = psc_status.ps_status
            # Set currents to 0
            variables[self._c.V_PS_SETPOINT] = value_init
            variables[self._c.V_PS_REFERENCE] = value_init
            for monvar_id in self._monvars:
                variables[monvar_id] = value_init

    def open_loop(self, variables):
        """Open control loop."""
        ps_status = variables[self._c.V_PS_STATUS]
        psc_status = _PSCStatus(ps_status=ps_status)
        psc_status.open_loop = 1
        variables[self._c.V_PS_STATUS] = psc_status.ps_status

    def close_loop(self, variables):
        """Close control loop."""
        ps_status = variables[self._c.V_PS_STATUS]
        psc_status = _PSCStatus(ps_status=ps_status)
        psc_status.open_loop = 0
        variables[self._c.V_PS_STATUS] = psc_status.ps_status
        for monvar_id in self._monvars:
            variables[monvar_id] = variables[self._c.V_PS_REFERENCE]

    def select_op_mode(self, variables):
        """Set operation mode."""
        raise NotImplementedError()

    def reset_interlocks(self, variables):
        """Reset ps."""
        ps_status = variables[self._c.V_PS_STATUS]
        psc_status = _PSCStatus(ps_status=ps_status)
        # Set PSController status
        psc_status.ioc_opmode = _PSConst.OpMode.SlowRef
        value_init = self._get_init_value()
        variables[self._c.V_PS_STATUS] = psc_status.ps_status
        # Set Current to 0
        variables[self._c.V_PS_SETPOINT] = value_init
        variables[self._c.V_PS_REFERENCE] = value_init
        for monvar_id in self._monvars:
            variables[monvar_id] = value_init
        # Reset interlocks
        variables[self._c.V_PS_SOFT_INTERLOCKS] = 0
        variables[self._c.V_PS_HARD_INTERLOCKS] = 0

    def set_slowref(self, variables, input_val):
        """Set current."""
        raise NotImplementedError()

    def cfg_siggen(self, variables, input_val):
        """Config siggen."""
        raise NotImplementedError()

    def set_siggen(self, variables, input_val):
        """Set siggen parameters in continuos mode."""
        raise NotImplementedError()

    def enable_siggen(self, variables):
        """Enable siggen."""
        variables[self._c.V_SIGGEN_ENABLE] = 1

    def disable_siggen(self, variables):
        """Disable siggen."""
        variables[self._c.V_SIGGEN_ENABLE] = 0

    def _is_on(self, variables):
        ps_status = variables[self._c.V_PS_STATUS]
        psc_status = _PSCStatus(ps_status=ps_status)
        return psc_status.ioc_pwrstate

    def _is_open_loop(self, variables):
        ps_status = variables[self._c.V_PS_STATUS]
        psc_status = _PSCStatus(ps_status=ps_status)
        return psc_status.open_loop


class _OpModeSimSlowRefState(_OpModeSimState):
    """SlowRef state."""

    def select_op_mode(self, variables):
        """Set operation mode."""
        ps_status = variables[self._c.V_PS_STATUS]
        psc_status = _PSCStatus(ps_status=ps_status)
        psc_status.ioc_opmode = _PSConst.States.SlowRef
        variables[self._c.V_PS_STATUS] = psc_status.ps_status
        self.set_slowref(variables, variables[self._c.V_PS_SETPOINT])

    def set_slowref(self, variables, input_val):
        """Set current."""
        variables[self._c.V_PS_SETPOINT] = input_val
        if self._is_on(variables):
            variables[self._c.V_PS_REFERENCE] = input_val
            if self._is_open_loop(variables) == 0:
                # control loop closed
                for monvar_id in self._monvars:
                    variables[monvar_id] = input_val

    def cfg_siggen(self, variables, input_val):
        """Set siggen configuration parameters."""
        variables[self._c.V_SIGGEN_TYPE] = input_val[0]
        variables[self._c.V_SIGGEN_NUM_CYCLES] = input_val[1]
        variables[self._c.V_SIGGEN_FREQ] = input_val[2]
        variables[self._c.V_SIGGEN_AMPLITUDE] = input_val[3]
        variables[self._c.V_SIGGEN_OFFSET] = input_val[4]
        variables[self._c.V_SIGGEN_AUX_PARAM] = input_val[5:]

    def set_siggen(self, variables, input_val):
        """Set siggen configuration parameters while in continuos mode."""
        variables[self._c.V_SIGGEN_FREQ] = input_val[0]
        variables[self._c.V_SIGGEN_AMPLITUDE] = input_val[1]
        variables[self._c.V_SIGGEN_OFFSET] = input_val[2]

    def trigger(self, variables):
        """Slow Ref does nothing when trigger is received."""
        pass


class _OpModeSimSlowRefSyncState(_OpModeSimState):

    def __init__(self):
        """Init."""
        _OpModeSimState.__init__(self)
        self._last_setpoint = None

    def select_op_mode(self, variables):
        """Set operation mode."""
        ps_status = variables[self._c.V_PS_STATUS]
        psc_status = _PSCStatus(ps_status=ps_status)
        psc_status.ioc_opmode = _PSConst.OpMode.SlowRefSync
        variables[self._c.V_PS_STATUS] = psc_status.ps_status

    def set_slowref(self, variables, input_val):
        """Set current."""
        self._last_setpoint = input_val

    def trigger(self, variables):
        """Apply last setpoint received."""
        if self._last_setpoint is None:
            self._last_setpoint = variables[self._c.V_PS_SETPOINT]
        variables[self._c.V_PS_SETPOINT] = self._last_setpoint
        if self._is_on(variables):
            variables[self._c.V_PS_REFERENCE] = self._last_setpoint
            if self._is_open_loop(variables) == 0:
                # control loop closed
                for monvar_id in self._monvars:
                    variables[monvar_id] = self._last_setpoint


class _OpModeSimCycleState(_OpModeSimState):
    """FBP Cycle state."""

    def __init__(self, pru):
        """Set cycle parameters."""
        _OpModeSimState.__init__(self)
        self._siggen_canceled = False
        self._pru = pru

    def read_variable(self, variables, var_id):
        """Return variable."""
        enbl = variables[self._c.V_SIGGEN_ENABLE]
        if enbl and \
           (var_id in self._monvars or var_id == self._c.V_PS_REFERENCE):
            value = self._signal.value
            variables[self._c.V_PS_REFERENCE] = value
            for monvar_id in self._monvars:
                variables[monvar_id] = value
            variables[self._c.V_SIGGEN_N] += 1
        return super().read_variable(variables, var_id)

    def select_op_mode(self, variables):
        """Set operation mode."""
        ps_status = variables[self._c.V_PS_STATUS]
        psc_status = _PSCStatus(ps_status=ps_status)
        psc_status.ioc_opmode = _PSConst.OpMode.Cycle
        variables[self._c.V_PS_STATUS] = psc_status.ps_status
        variables[self._c.V_SIGGEN_ENABLE] = 0
        variables[self._c.V_PS_REFERENCE] = 0.0
        for monvar_id in self._monvars:
            variables[monvar_id] = 0.0
        # self._set_signal(variables)
        # self.enable_siggen(variables)

    def reset_interlocks(self, variables):
        """Reset interlocks."""
        super().reset_interlocks(variables)
        self.disable_siggen(variables)

    def set_slowref(self, variables, input_val):
        """Set current."""
        variables[self._c.V_PS_SETPOINT] = input_val

    def cfg_siggen(self, variables, input_val):
        """Set siggen configuration parameters."""
        if not variables[self._c.V_SIGGEN_ENABLE]:
            variables[self._c.V_SIGGEN_TYPE] = input_val[0]
            variables[self._c.V_SIGGEN_NUM_CYCLES] = input_val[1]
            variables[self._c.V_SIGGEN_FREQ] = input_val[2]
            variables[self._c.V_SIGGEN_AMPLITUDE] = input_val[3]
            variables[self._c.V_SIGGEN_OFFSET] = input_val[4]
            variables[self._c.V_SIGGEN_AUX_PARAM] = input_val[5:]

    def set_siggen(self, variables, input_val):
        """Set siggen configuration parameters while in continuos mode."""
        if not variables[self._c.V_SIGGEN_ENABLE] or \
                (variables[self._c.V_SIGGEN_ENABLE] and
                 variables[self._c.V_SIGGEN_NUM_CYCLES] == 0):
            variables[self._c.V_SIGGEN_FREQ] = input_val[0]
            variables[self._c.V_SIGGEN_AMPLITUDE] = input_val[1]
            variables[self._c.V_SIGGEN_OFFSET] = input_val[2]

    def enable_siggen(self, variables):
        """Enable siggen."""
        # variables[self._c.V_SIGGEN_ENABLE] = 1
        self._siggen_canceled = False
        thread = _Thread(
            target=self._finish_siggen,
            args=(variables, ),
            daemon=True)
        thread.start()

    def disable_siggen(self, variables):
        """Disable siggen."""
        if variables[self._c.V_SIGGEN_ENABLE] == 1:
            variables[self._c.V_SIGGEN_ENABLE] = 0
            self._siggen_canceled = True
            self._signal.enable = False

    def _set_signal(self, variables):
        t = variables[self._c.V_SIGGEN_TYPE]
        n = variables[self._c.V_SIGGEN_NUM_CYCLES]
        f = variables[self._c.V_SIGGEN_FREQ]
        a = variables[self._c.V_SIGGEN_AMPLITUDE]
        o = variables[self._c.V_SIGGEN_OFFSET]
        p = variables[self._c.V_SIGGEN_AUX_PARAM]
        self._signal = _SignalFactory.create(type=t,
                                             num_cycles=n,
                                             freq=f,
                                             amplitude=a,
                                             offset=o,
                                             aux_param=p)

    def _finish_siggen(self, variables):
        self._set_signal(variables)
        if self._signal.duration <= 0:
            return
        time = self._signal.duration
        variables[self._c.V_SIGGEN_ENABLE] = 1
        time_up = False
        elapsed = 0
        while not time_up:
            _time.sleep(0.5)
            elapsed += 0.5
            if elapsed >= time:
                time_up = True
            if self._siggen_canceled:
                return
        val = self._signal.value
        variables[self._c.V_PS_REFERENCE] = val
        for monvar_id in self._monvars:
            variables[monvar_id] = val
        variables[self._c.V_SIGGEN_ENABLE] = 0
        variables[self._c.V_SIGGEN_N] = 0

    def trigger(self, variables):
        """Trigger received."""
        self.enable_siggen(variables)


# --- Specialized PS states ---


class _OpModeSimSlowRefState_FBP(_OpModeSimSlowRefState, _Spec_FBP):
    """SlowRef FBP state."""

    pass


class _OpModeSimSlowRefSyncState_FBP(_OpModeSimSlowRefSyncState, _Spec_FBP):
    """SlowRefSync FBP state."""

    pass


class _OpModeSimCycleState_FBP(_OpModeSimCycleState, _Spec_FBP):
    """Cycle FBP state."""

    pass


class _OpModeSimState_FBP_DCLink(_OpModeSimSlowRefState, _Spec_FBP_DCLink):
    """SlowRef FBP_DCLink state."""

    def _get_init_value(self):
        return 15.0  # [%]

    def reset_interlocks(self, variables):
        """Reset ps."""
        _OpModeSimSlowRefState.reset_interlocks(self, variables)
        # if variables[self._c.V_PS_REFERENCE] < 50.0:
        #     # sub-tension sources 1,2,3.
        #     variables[self._c.V_PS_HARD_INTERLOCKS] += \
        #         (1 << 8) + (1 << 9) + (1 << 10)


class _OpModeSimSlowRefState_FAC_DCDC(_OpModeSimSlowRefState, _Spec_FAC_DCDC):
    """SlowRef FAC_DCDC state."""

    pass


class _OpModeSimSlowRefSyncState_FAC_DCDC(_OpModeSimSlowRefSyncState,
                                          _Spec_FAC_DCDC):
    """SlowRefSync FAC_DCDC state."""

    pass


class _OpModeSimCycleState_FAC_DCDC(_OpModeSimCycleState, _Spec_FAC_DCDC):
    """Cycle FAC_DCDC state."""

    pass


class _OpModeSimState_FAC_2S_ACDC(_OpModeSimSlowRefState, _Spec_FAC_2S_ACDC):
    """SlowRef FAC_2S_ACDC state."""

    pass


class _OpModeSimState_FAC_2P4S_ACDC(_OpModeSimSlowRefState, _Spec_FAC_2P4S_ACDC):
    """SlowRef FAC_2P4S_ACDC state."""

    pass


class _OpModeSimState_FAP(_OpModeSimSlowRefState, _Spec_FAP):
    """SlowRef FAP state."""

    pass


# --- Classes for simulated BPMs ---


class _BaseBSMPSim(_BSMPSim):
    """Simulated general UDC."""

    SlowRefState = 0
    SlowRefSyncState = 1
    CycleState = 2

    def __init__(self, pru):
        """Init."""
        entities = self._get_entities()
        super().__init__(entities)
        self._pru = pru
        self._pru.add_callback(self._trigger)

        # set constants
        self._c = self._get_constants()

        # Set variables initial value
        self._variables = self._get_init_variables()

        # Set curves initial values
        self._curves = self._get_init_curves()

        # Operation mode states
        self._states = self._get_states()

        # Current state
        self._state = self._states[self.SlowRefState]

    def read_variable(self, var_id, timeout):
        """Read variable."""
        while self._pru.sync_block:
            _time.sleep(1e-1)
        return _BSMPConst.ACK_OK, self._state.read_variable(self._variables, var_id)

    def execute_function(self, func_id, input_val=None, read_flag=True):
        """Execute a function."""
        # Switch FBP func ids
        if func_id == self._c.F_TURN_ON:
            self._state.turn_on(self._variables)
        elif func_id == self._c.F_TURN_OFF:
            self._state.turn_off(self._variables)
        elif func_id == self._c.F_OPEN_LOOP:
            self._state.open_loop(self._variables)
        elif func_id == self._c.F_CLOSE_LOOP:
            self._state.close_loop(self._variables)
        elif func_id == self._c.F_SELECT_OP_MODE:  # Change state
            # Verify if ps is on
            if self._is_on():
                psc_status = _PSCStatus(input_val)
                input_val = psc_status.ioc_opmode
                self._state = self._states[input_val]
                self._state.select_op_mode(self._variables)
        elif func_id == self._c.F_RESET_INTERLOCKS:  # Change state
            self._state.reset_interlocks(self._variables)
            self._state = self._states[self.SlowRefState]
        elif func_id == self._c.F_SET_SLOWREF:
            if self._is_on():
                self._state.set_slowref(self._variables, input_val)
        elif func_id == self._c.F_CFG_SIGGEN:
            self._state.cfg_siggen(self._variables, input_val)
        elif func_id == self._c.F_SET_SIGGEN:
            self._state.set_siggen(self._variables, input_val)
        elif func_id == self._c.F_ENABLE_SIGGEN:
            self._state.enable_siggen(self._variables)
        elif func_id == self._c.F_DISABLE_SIGGEN:
            self._state.disable_siggen(self._variables)

        return _BSMPConst.ACK_OK, None

    def request_curve_block(self, curve_id, block, timeout):
        """Read curve block."""
        self._curves = self._get_init_curves()
        curveblock = self._curves[curve_id]
        return _BSMPConst.ACK_OK, curveblock

    def _is_on(self):
        ps_status = self._variables[self._c.V_PS_STATUS]
        psc_status = _PSCStatus(ps_status=ps_status)
        return psc_status.ioc_pwrstate

    def _trigger(self, value=None):
        if self._is_on():
            self._state.trigger(self._variables)

    def _get_init_curves(self):
        cvs = self.entities.curves
        if len(cvs):
            bsmp_c = cvs[0]
            sblock = bsmp_c.size // bsmp_c.type.size
            curves = _np.random.normal(
                scale=_Spec.I_LOAD_FLUCTUATION_RMS,
                size=(len(cvs), sblock))
        else:
            # cases where there is no defined bsmp curve, such as in DCLinks.
            curves = []
        return curves


class BSMPSim_FBP(_BaseBSMPSim, _Spec_FBP):
    """Simulated FBP UDC."""

    def _get_entities(self):
        return _psbsmp.EntitiesFBP()

    def _get_states(self):
        return [_OpModeSimSlowRefState_FBP(), _OpModeSimSlowRefSyncState_FBP(),
                _OpModeSimCycleState_FBP(self._pru)]

    def _get_init_variables(self):

        firmware = [b'S', b'i', b'm', b'u', b'l', b'a', b't', b'i', b'o', b'n']
        while len(firmware) < 128:
            firmware.append('\x00'.encode())
        variables = [
            0b10000,  # V_PS_STATUS
            0.0, 0.0,  # ps_setpoint, ps_reference
            firmware,
            0, 0,  # counters
            0, 0, 0, 0.0, 0.0, 0.0, 0.0, [0.0, 0.0, 0.0, 0.0],  # siggen [6-13]
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # undef [14-24]
            0, 0,  # interlocks [25-26]
            0.0, 0.0, 0.0, 0.0, 0.0,  # i_load, v_load, etc [27-31]
            0, 0, 0, 0, 0, 0, 0, 0,  # reserved [32-39]
            0, 0, 0, 0,  # mirror ps_status [40-43]
            0.0, 0.0, 0.0, 0.0,  # mirror ps_setpoints [44-47]
            0.0, 0.0, 0.0, 0.0,  # mirror ps_reference [48-51]
            0, 0, 0, 0,  # mirror soft_interlock [52-55]
            0, 0, 0, 0,  # mirror hard_interlock [56-59]
            0.0, 0.0, 0.0, 0.0]  # mirror i_load [60-63]
        default_siggen_parms = \
            _SignalFactory.DEFAULT_CONFIGS['Sine']
        variables[_psbsmp.ConstFBP.V_SIGGEN_TYPE] = default_siggen_parms[0]
        variables[_psbsmp.ConstFBP.V_SIGGEN_NUM_CYCLES] = default_siggen_parms[1]
        variables[_psbsmp.ConstFBP.V_SIGGEN_FREQ] = default_siggen_parms[2]
        variables[_psbsmp.ConstFBP.V_SIGGEN_AMPLITUDE] = default_siggen_parms[3]
        variables[_psbsmp.ConstFBP.V_SIGGEN_OFFSET] = default_siggen_parms[4]
        variables[_psbsmp.ConstFBP.V_SIGGEN_AUX_PARAM] = default_siggen_parms[5:9]
        return variables


class BSMPSim_FBP_DCLink(_BaseBSMPSim, _Spec_FBP_DCLink):
    """Simulated FBP_DCLink UDC."""

    def _get_entities(self):
        return _psbsmp.EntitiesFBP_DCLink()

    def _get_states(self):
        return [_OpModeSimState_FBP_DCLink()]

    def _get_init_variables(self):
        variables = []
        firmware = [b'S', b'i', b'm', b'u', b'l', b'a', b't', b'i', b'o', b'n']
        while len(firmware) < 128:
            firmware.append('\x00'.encode())
        variables = [
            0b10000,  # V_PS_STATUS
            0.0, 0.0,  # ps_setpoint, ps_reference
            firmware,
            0, 0,  # counters
            0, 0, 0, 0.0, 0.0, 0.0, 0.0, [0.0, 0.0, 0.0, 0.0],  # siggen [6-13]
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # undef [14-24]
            0, 0,  # interlocks [25-26]
            0,  # modules_status [27]
            0.0, 0.0, 0.0, 0.0,  # v_out [28-31],
            0]  # dig_pot_tap [32]
        return variables


class BSMPSim_FAC_DCDC(_BaseBSMPSim, _Spec_FAC_DCDC):
    """Simulated FAC_DCDC UDC."""

    def _get_entities(self):
        return _psbsmp.EntitiesFAC_DCDC()

    def _get_states(self):
        return [_OpModeSimSlowRefState_FAC_DCDC(),
                _OpModeSimSlowRefSyncState_FAC_DCDC(),
                _OpModeSimCycleState_FAC_DCDC(self._pru)]

    def _get_init_variables(self):
        firmware = [b'S', b'i', b'm', b'u', b'l', b'a', b't', b'i', b'o', b'n']
        while len(firmware) < 128:
            firmware.append('\x00'.encode())
        variables = [
            0b10000,  # V_PS_STATUS
            0.0, 0.0,  # ps_setpoint, ps_reference
            firmware,
            0, 0,  # counters
            0, 0, 0, 0.0, 0.0, 0.0, 0.0, [0.0, 0.0, 0.0, 0.0],  # siggen [6-13]
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # undef [14-24]
            0, 0,  # interlocks [25-26]
            0.0, 0.0, 0.0,  # iload_mean, iload1, iload2 [27-29]
            0.0,  # vload
            0.0,  # capacitor_bank
            25.0,  # temp_inductors
            25.0,  # temp_heatsink
            30.0,  # duty_cycle
            0.0,  # i_input_iib
            0.0,  # i_output_iib
            0.0,  # v_input_iib
            0.0,  # temp_igbts_1_iib
            0.0,  # temp_igbts_2_iib
            0.0,  # temp_inductor_iib
            0.0,  # temp_heatsink_iib
            0.0,  # driver_error_1_iib
            0.0,  # driver_error_2_iib
            0]  # iib_interlocks [44]
        default_siggen_parms = \
            _SignalFactory.DEFAULT_CONFIGS['Sine']
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_TYPE] = default_siggen_parms[0]
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_NUM_CYCLES] = default_siggen_parms[1]
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_FREQ] = default_siggen_parms[2]
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_AMPLITUDE] = default_siggen_parms[3]
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_OFFSET] = default_siggen_parms[4]
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_AUX_PARAM] = default_siggen_parms[5:9]
        return variables


class BSMPSim_FAC_2P4S_DCDC(_BaseBSMPSim, _Spec_FAC_2P4S_DCDC):
    """Simulated FAC_2P4S_DCDC UDC."""

    def _get_entities(self):
        return _psbsmp.EntitiesFAC_2P4S_DCDC()

    def _get_states(self):
        return [_OpModeSimSlowRefState_FAC_DCDC(),
                _OpModeSimSlowRefSyncState_FAC_DCDC(),
                _OpModeSimCycleState_FAC_DCDC(self._pru)]

    def _get_init_variables(self):
        firmware = [b'S', b'i', b'm', b'u', b'l', b'a', b't', b'i', b'o', b'n']
        while len(firmware) < 128:
            firmware.append('\x00'.encode())
        variables = [
            0b10000,  # V_PS_STATUS
            0.0, 0.0,  # ps_setpoint, ps_reference
            firmware,
            0, 0,  # counters
            0, 0, 0, 0.0, 0.0, 0.0, 0.0, [0.0, 0.0, 0.0, 0.0],  # siggen [6-13]
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # undef [14-24]
            0, 0,  # interlocks [25-26]
            0.0, 0.0, 0.0,  # iload_mean, iload1, iload2, v_load [27-29]
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # [30-38]
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # [39-47]
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # [48-56]
        default_siggen_parms = \
            _SignalFactory.DEFAULT_CONFIGS['Sine']
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_TYPE] = default_siggen_parms[0]
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_NUM_CYCLES] = default_siggen_parms[1]
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_FREQ] = default_siggen_parms[2]
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_AMPLITUDE] = default_siggen_parms[3]
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_OFFSET] = default_siggen_parms[4]
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_AUX_PARAM] = default_siggen_parms[5:9]
        return variables


class BSMPSim_FAC_2S_DCDC(_BaseBSMPSim, _Spec_FAC_2P4S_DCDC):
    """Simulated FAC_2S_DCDC UDC."""

    def _get_entities(self):
        return _psbsmp.EntitiesFAC_2S_DCDC()

    def _get_states(self):
        return [_OpModeSimSlowRefState_FAC_DCDC(),
                _OpModeSimSlowRefSyncState_FAC_DCDC(),
                _OpModeSimCycleState_FAC_DCDC(self._pru)]

    def _get_init_variables(self):
        firmware = [b'S', b'i', b'm', b'u', b'l', b'a', b't', b'i', b'o', b'n']
        while len(firmware) < 128:
            firmware.append('\x00'.encode())
        variables = [
            0b10000,  # V_PS_STATUS
            0.0, 0.0,  # ps_setpoint, ps_reference
            firmware,
            0, 0,  # counters
            0, 0, 0, 0.0, 0.0, 0.0, 0.0, [0.0, 0.0, 0.0, 0.0],  # siggen [6-13]
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # undef [14-24]
            0, 0,  # interlocks [25-26]
            0.0, 0.0, 0.0, 0.0,  # iload_mean, iload1, iload2, v_load [27-30]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [31-35]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [36-40]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [41-45]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [45-50]
            0.0,  # [51]
            0, 0]  # iib_interlocks [52-53]
        default_siggen_parms = \
            _SignalFactory.DEFAULT_CONFIGS['Sine']
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_TYPE] = default_siggen_parms[0]
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_NUM_CYCLES] = default_siggen_parms[1]
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_FREQ] = default_siggen_parms[2]
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_AMPLITUDE] = default_siggen_parms[3]
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_OFFSET] = default_siggen_parms[4]
        variables[_psbsmp.ConstFAC_DCDC.V_SIGGEN_AUX_PARAM] = default_siggen_parms[5:9]
        return variables


class BSMPSim_FAC_2P4S_ACDC(_BaseBSMPSim, _Spec_FAC_2P4S_ACDC):
    """Simulated FAC_2P4S_ACDC UDC."""

    def _get_entities(self):
        return _psbsmp.EntitiesFAC_2P4S_ACDC()

    def _get_states(self):
        return [_OpModeSimState_FAC_2P4S_ACDC()]

    def _get_init_variables(self):
        firmware = [b'S', b'i', b'm', b'u', b'l', b'a', b't', b'i', b'o', b'n']
        while len(firmware) < 128:
            firmware.append('\x00'.encode())
        variables = [
            0b10000,  # V_PS_STATUS
            0.0, 0.0,  # ps_setpoint, ps_reference
            firmware,
            0, 0,  # counters
            0, 0, 0, 0.0, 0.0, 0.0, 0.0, [0.0, 0.0, 0.0, 0.0],  # siggen [6-13]
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # undef [14-24]
            0, 0,  # interlocks [25-26]
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # [27-32]
        return variables


class BSMPSim_FAC_2S_ACDC(_BaseBSMPSim, _Spec_FAC_2S_ACDC):
    """Simulated FAC_2S_ACDC UDC."""

    def _get_entities(self):
        return _psbsmp.EntitiesFAC_2S_ACDC()

    def _get_states(self):
        return [_OpModeSimState_FAC_2S_ACDC()]

    def _get_init_variables(self):
        firmware = [b'S', b'i', b'm', b'u', b'l', b'a', b't', b'i', b'o', b'n']
        while len(firmware) < 128:
            firmware.append('\x00'.encode())
        variables = [
            0b10000,  # V_PS_STATUS
            0.0, 0.0,  # ps_setpoint, ps_reference
            firmware,
            0, 0,  # counters
            0, 0, 0, 0.0, 0.0, 0.0, 0.0, [0.0, 0.0, 0.0, 0.0],  # siggen [6-13]
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # undef [14-24]
            0, 0,  # interlocks [25-26]
            0.0, 0.0, 0.0,  # [27-29]
            0.0, 0.0,  # temps [30-31]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [32-36]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [37-41]
            0, 0]  # iib_interlocks [42-43]
        return variables



class BSMPSim_FAP(_BaseBSMPSim, _Spec_FAP):
    """Simulated FAP UDC."""

    def _get_entities(self):
        return _psbsmp.EntitiesFAP()

    def _get_states(self):
        return [_OpModeSimSlowRefState_FBP(), _OpModeSimSlowRefSyncState_FBP(),
                _OpModeSimCycleState_FBP(self._pru)]

    def _get_init_variables(self):
        firmware = [b'S', b'i', b'm', b'u', b'l', b'a', b't', b'i', b'o', b'n']
        while len(firmware) < 128:
            firmware.append('\x00'.encode())
        variables = [
            0b10000,  # V_PS_STATUS
            0.0, 0.0,  # ps_setpoint, ps_reference
            firmware,
            0, 0,  # counters
            0, 0, 0, 0.0, 0.0, 0.0, 0.0, [0.0, 0.0, 0.0, 0.0],  # siggen [6-13]
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # undef [14-24]
            0, 0,  # interlocks [25-26]
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # [27-35]
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # [36-46]
            0,  # [47 - iib_interlocks]
            ]
        return variables


class BSMPSim_FAP_4P(_BaseBSMPSim, _Spec_FAP_4P):
    """Simulated FAP UDC."""

    def _get_entities(self):
        return _psbsmp.EntitiesFAP_4P()

    def _get_states(self):
        return [_OpModeSimSlowRefState_FBP(), _OpModeSimSlowRefSyncState_FBP(),
                _OpModeSimCycleState_FBP(self._pru)]

    def _get_init_variables(self):
        firmware = [b'S', b'i', b'm', b'u', b'l', b'a', b't', b'i', b'o', b'n']
        while len(firmware) < 128:
            firmware.append('\x00'.encode())
        variables = [
            0b10000,  # V_PS_STATUS
            0.0, 0.0,  # ps_setpoint, ps_reference
            firmware,
            0, 0,  # counters
            0, 0, 0, 0.0, 0.0, 0.0, 0.0, [0.0, 0.0, 0.0, 0.0],  # siggen [6-13]
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # undef [14-24]
            0, 0,  # interlocks [25-26]
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # [27-35]
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # [36-46]
            0,  # [47 - iib_interlocks]
        ]
        return variables


class BSMPSim_FAP_2P2S(_BaseBSMPSim, _Spec_FAP_2P2S):
    """Simulated FAP_2P2S UDC."""

    def _get_entities(self):
        return _psbsmp.EntitiesFAP_2P2S()

    def _get_states(self):
        return [_OpModeSimSlowRefState_FBP(), _OpModeSimSlowRefSyncState_FBP(),
                _OpModeSimCycleState_FBP(self._pru)]

    def _get_init_variables(self):
        firmware = [b'S', b'i', b'm', b'u', b'l', b'a', b't', b'i', b'o', b'n']
        while len(firmware) < 128:
            firmware.append('\x00'.encode())
        variables = [
            0b10000,  # V_PS_STATUS
            0.0, 0.0,  # ps_setpoint, ps_reference
            firmware,
            0, 0,  # counters
            0, 0, 0, 0.0, 0.0, 0.0, 0.0, [0.0, 0.0, 0.0, 0.0],  # siggen [6-13]
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # undef [14-24]
            0, 0,  # interlocks [25-26]
            0.0, 0.0, 0.0,  # [27-29]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [30-34]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [35-39]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [40-44]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [45-49]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [50-54]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [55-59]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [60-64]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [65-69]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [70-74]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [75-79]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [80-84]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [85-89]
            0.0, 0.0, 0.0, 0.0, 0.0,  # [90-94]
            0.0, 0.0, 0.0,  # [95-97]
            0, 0, 0, 0,  # [98-101]
            0.0, 0.0, 0.0, 0.0]  # [102-105]
        return variables
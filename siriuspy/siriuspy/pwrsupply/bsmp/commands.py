"""Power Supply BSMP Commands.

Documentation:

https://wiki-sirius.lnls.br/mediawiki/index.php/Machine:Power_Supplies
"""

import time as _time
import numpy as _np

from ...bsmp import constants as _const_bsmp
from ...bsmp import BSMP as _BSMP

from . import constants as _const_psbsmp
from . import entities as _etity_psbsmp

# version of the BSMP implementation of power supplies that is compatible
# with the current implemenation of this module.


class PSBSMP(_BSMP):
    """Power supply BSMP.

    This class derives from basic BSMP class.
    It overrides methods with power supply specific parameters.
    """

    CONST_BSMP = _const_bsmp
    CONST = _const_psbsmp.ConstPSBSMP

    _timeout_read_variable = 100  # [ms]
    _timeout_execute_function = 100  # [ms]
    _timeout_remove_vars_groups = 100  # [ms]
    _timeout_create_vars_groups = 100  # [ms]
    _timeout_read_group_of_variables = 100  # [ms]
    _timeout_request_curve_block = 100  # [ms]
    _timeout_curve_block = 100  # [ms]
    _timeout_query_list_of_group_of_variables = 100  # [ms]
    _timeout_query_group_of_variables = 100  # [ms]

    _sleep_turn_onoff = 0.050  # [s]
    _sleep_reset_udc = 1.000  # [s]
    _sleep_disable_scope = 0.5  # [s]
    _sleep_select_op_mode = 0.030  # [s]

    # --- BSMP PS curves ---
    CURVE_ID_WFMREF_DATA0 = 0
    CURVE_ID_WFMREF_DATA1 = 1
    CURVE_ID_SCOPE = 2

    _WFMREF_POINTERS_VAR_IDS = {
        CURVE_ID_WFMREF_DATA0: (
            CONST.V_WFMREF0_START,
            CONST.V_WFMREF0_END,
            CONST.V_WFMREF0_IDX),
        CURVE_ID_WFMREF_DATA1: (
            CONST.V_WFMREF1_START,
            CONST.V_WFMREF1_END,
            CONST.V_WFMREF1_IDX),
    }

    def __init__(self, slave_address, entities, pru=None):
        """Init BSMP."""
        self.pru = pru
        super().__init__(self.pru, slave_address, entities)
        self._wfmref_check_entities_consistency()

    @staticmethod
    def parse_firmware_version(version):
        """Process firmware version from BSMP device."""
        version = version[:version.index(b'\x00')]
        version = ''.join([chr(ord(v)) for v in version])
        return version

    def reset_groups_of_variables(self, varids_groups):
        """Reset groups of variables."""

        # remove previous variables groups
        ack, data = self.remove_all_groups_of_variables(
            timeout=self._timeout_remove_vars_groups)
        if ack != PSBSMP.CONST_BSMP.ACK_OK:
            return ack, data

        # create variables groups
        for var_ids in varids_groups:
            ack, data = self.create_group_of_variables(
                var_ids, timeout=self._timeout_create_vars_groups)
            if ack != PSBSMP.CONST_BSMP.ACK_OK:
                return ack, data

        return ack, data

    # --- bsmp overriden methods ---

    def execute_function(
            self, func_id, input_val=None,
            timeout=_timeout_execute_function,
            read_flag=True, print_error=True):
        """."""
        # execute function
        # print('--- execute_function ---')
        # print('func_id: ', func_id)
        # print('input_val: ', input_val)
        # print('timeout: ', timeout)
        # print('read_flag: ', read_flag)

        if func_id in (PSBSMP.CONST.F_SYNC_PULSE,
                       PSBSMP.CONST.F_RESET_UDC):
            # NOTE: this is necessary while PS BSMP spec is
            # not updated!
            read_flag = False

        response = super().execute_function(
            func_id=func_id, input_val=input_val,
            timeout=timeout, read_flag=read_flag)

        # introduces necessary sleeps
        # TODO: check with ELP if these numbers can be optimized further!
        if func_id == PSBSMP.CONST.F_RESET_UDC:
            _time.sleep(self._sleep_reset_udc)
        elif func_id == PSBSMP.CONST.F_DISABLE_SCOPE:
            # NOTE: sleep is implemented in UDC class,
            # for optimization purpose!
            # _time.sleep(self._sleep_disable_scope)
            pass
        elif func_id == PSBSMP.CONST.F_SELECT_OP_MODE:
            # _time.sleep(self._sleep_select_op_mode)
            pass
        elif func_id in (PSBSMP.CONST.F_TURN_ON,
                         PSBSMP.CONST.F_TURN_OFF,
                         PSBSMP.CONST.F_OPEN_LOOP,
                         PSBSMP.CONST.F_CLOSE_LOOP):
            _time.sleep(self._sleep_turn_onoff)

        if read_flag:
            return response
        else:
            # TODO: This should be temporary. It is used for F_RESET_UDC.
            # Firmware should change so that F_RESET_UDC returns ack.
            return self.CONST_BSMP.ACK_OK, None

    def read_group_of_variables(
            self, group_id, timeout=_timeout_read_group_of_variables):
        """."""
        response = super().read_group_of_variables(
            group_id=group_id, timeout=timeout)

        return response

    def query_list_of_group_of_variables(
            self, timeout=_timeout_query_list_of_group_of_variables):
        """."""
        response = super().query_list_of_group_of_variables(
            timeout=timeout)

        return response

    def query_group_of_variables(
            self, group_id, timeout=_timeout_query_group_of_variables):
        """."""
        response = super().query_group_of_variables(
            group_id=group_id, timeout=timeout)

        return response

    # --- pwrsupply functions ---

    def ps_function_set_slowref_fbp(self, setpoints):
        """Write FBP 4-valued setpoints."""
        self.execute_function(
            PSBSMP.CONST.F_SET_SLOWREF_FBP, setpoints)

    def ps_function_set_slowref_fbp_readback_ref(self, setpoints):
        """Write FBP 4-valued setpoints and get reference values."""
        ack, data = self.execute_function(
            PSBSMP.CONST.F_SET_SLOWREF_FBP_READBACK_REF, setpoints)
        return ack, data

    # --- pwrsupply parameters ---

    def parameter_read(self, eid, index=None):
        """Return power supply parameter."""

        parameter = self.entities.parameters[eid]
        count = parameter['count']
        if eid == PSBSMP.CONST.P_PS_NAME:
            # PS_NAME parameter
            value = _np.zeros(count)
            for index in range(count):
                value[index] = self._read_parm(eid, index)
                if value[index] == 0.0:
                    # TODO: this end-of-string convention is
                    # yet to be implemented!
                    value = value[:index]
                    break
            value = ''.join([chr(int(v)) for v in value]).strip()
        else:
            # other parameters
            if index is None:
                value = _np.zeros(count)
                for idx in range(count):
                    val = self._read_parm(eid, idx)
                    if val is None:
                        return None
                    value[idx] = val
                if count == 1:
                    value = value[0]
            else:
                value = self._read_parm(eid, index)
                if value is None:
                    return None
        return value

    def parameter_write(self, eid, value, index=0):
        """Set power supply parameter."""
        parameter = self.entities.parameters[eid]
        count = parameter['count']
        val = value[:count]
        if eid == PSBSMP.CONST.P_PS_NAME:
            # PS_NAME parameter
            value = _np.zeros(count)
            value[:len(val)] = [float(ord(c)) for c in val]
            for index, value_datum in enumerate(value):
                self.execute_function(
                    func_id=PSBSMP.CONST.F_SET_PARAM,
                    input_val=(eid, index, value_datum))
        else:
            self.execute_function(
                func_id=PSBSMP.CONST.F_SET_PARAM,
                input_val=(eid, index, value))

    # --- wfmref and scope methods ---

    @property
    def wfmref_select(self):
        """Return wfmref curve ID currently in use by DSP."""
        _, curve_id = self.read_variable(
            var_id=PSBSMP.CONST.V_WFMREF_SELECTED,
            timeout=self._timeout_read_variable)
        return curve_id

    @wfmref_select.setter
    def wfmref_select(self, curve_id):
        """Select wfmref curve ID to be used by DSP."""
        ack, data = self.execute_function(
            func_id=PSBSMP.CONST.F_SELECT_WFMREF,
            input_val=curve_id,
            timeout=self._timeout_execute_function)
        return ack, data

    def wfmref_size(self, curve_id=None):
        """Return wfmref curve size in t_float units.

            This is the waveform size as last registered by the
        ARM controller.
        """
        # calculate wfmref size from buffer pointer values used by
        # ARM controller
        i_beg, i_end, _ = self._wfmref_get_pointers_ids_of_selected(curve_id)
        values = self._bsmp_get_variable_values(i_beg, i_end)
        return PSBSMP.curve_index_calc(values[0], values[1])

    @property
    def wfmref_index(self):
        """Return wfmref curve index.

            This index refers to the current waveform in use by the
        DSP controller.
        """
        # calculate wfmref index from buffer pointer values used by
        # ARM controller
        i_beg, _, i_idx = self._wfmref_get_pointers_ids_of_selected()
        values = self._bsmp_get_variable_values(i_beg, i_idx)
        return PSBSMP.curve_index_calc(values[0], values[1])

    @property
    def wfmref_maxsize(self):
        """Return max size of bsmp curves 0 and 1."""
        # curve with ids 0 and 1 should have same sizes.
        maxsize = self.curve_maxsize(curve_id=0)
        return maxsize

    @ property
    def wfmref_pointer_values(self):
        """Return pointer values of currently selected wfmref curve."""
        pointer_ids = self._wfmref_get_pointers_ids_of_selected()
        pointer_values = self._bsmp_get_variable_values(*pointer_ids)
        return pointer_values

    def wfmref_read(self):
        """Return data of wfmref curve currently in use by DSP."""
        # get curve ID
        curve_id = self.wfmref_select

        # get curve data
        curve = self._curve_bsmp_read(curve_id=curve_id)
        return curve

    def wfmref_write(self, curve):
        """Write a new wfmref curve to the available buffer not in use."""
        # get id of writable wfmref curve
        curve_id = self._wfmref_bsmp_select_writable_curve_id()

        # write curve
        curve = self.curve_write(curve_id, curve, read_curve=True)

        # execute selection of WfmRef to be used
        self.wfmref_select = curve_id

        return curve

    def scope_read(self):
        """Read scope."""
        curve_id = PSBSMP.CURVE_ID_SCOPE
        curve = self._curve_bsmp_read(curve_id=curve_id)
        return curve

    def scope_enable(self):
        """Enable scope update."""
        ack, data = self.execute_function(
            func_id=PSBSMP.CONST.F_ENABLE_SCOPE,
            timeout=self._timeout_execute_function)
        return ack, data

    def scope_disable(self):
        """Disable scope update."""
        ack, data = self.execute_function(
            func_id=PSBSMP.CONST.F_DISABLE_SCOPE,
            timeout=self._timeout_execute_function)
        return ack, data

    # --- curve methods ---

    def curve_read(self, curve_id):
        """Return curve."""
        curve = self._curve_bsmp_read(curve_id=curve_id)
        return curve

    def curve_write(self, curve_id, curve, read_curve=False):
        """Write curve."""
        # check curve size
        self._curve_check_size(curve_id=curve_id, curve_size=len(curve))

        # send curve blocks
        self._curve_bsmp_write(curve_id, curve)

        if read_curve:
            # get curve just written
            curve = self.curve_read(curve_id)
            return _np.array(curve)
        else:
            return curve

    def curve_maxsize(self, curve_id):
        """Return max size if t_float units according to BSMP spec."""
        curve_entity = self.entities.curves[curve_id]
        maxsize = curve_entity.max_size_t_float
        return maxsize

    @staticmethod
    def curve_index_calc(beg, end):
        """Calculate curve index."""
        return 1 + (end - beg) // 2

    # --- private methods ---

    def _wfmref_get_pointers_ids_of_selected(self, curve_id=None):
        if curve_id is None:
            curve_id = self.wfmref_select
        return PSBSMP._WFMREF_POINTERS_VAR_IDS[curve_id]

    def _wfmref_check_entities_consistency(self):
        # check consistency of curves with ids 0 and 1
        curves = self.entities.curves
        if 0 in curves and 1 in curves:
            curve0, curve1 = curves[0], curves[1]
            if False in (curve0.waccess, curve1.waccess) or \
               curve0.size != curve1.size or \
               curve0.nblocks != curve1.nblocks:
                raise ValueError('Inconsistent curves!')

    def _wfmref_bsmp_select_writable_curve_id(self):

        # get current curve id
        _, curve_id = self.read_variable(
            var_id=PSBSMP.CONST.V_WFMREF_SELECTED,
            timeout=self._timeout_read_variable)

        # select the other buffer and send curve blocks
        if curve_id == PSBSMP.CURVE_ID_WFMREF_DATA1:
            curve_id = PSBSMP.CURVE_ID_WFMREF_DATA0
        else:
            curve_id = PSBSMP.CURVE_ID_WFMREF_DATA1

        return curve_id

    def _curve_bsmp_read(self, curve_id):
        # select minimum curve size between spec and firmware.
        if curve_id == PSBSMP.CURVE_ID_SCOPE:
            # for scope, we have to assume the size as the same as selected
            # buffer since there are no bsmp variables indicating its size.
            wfmref_size = self.wfmref_size()
        else:
            wfmref_size = self.wfmref_size(curve_id)
        wfmref_size_min = self._curve_get_implementable_size(
            curve_id, wfmref_size)

        # create initial output data
        curve = _np.zeros(wfmref_size_min)

        # read curve blocks
        curve_entity = self.entities.curves[curve_id]
        indices = curve_entity.get_indices(wfmref_size_min)
        # print('reading - curve id: ', curve_id)
        # print('reading - indices: ', indices)
        for block, idx in enumerate(indices):
            # print('psbsmp.curve_read-0 ', curve_id, block)
            ack, data = self.request_curve_block(
                curve_id=curve_id,
                block=block,
                timeout=self._timeout_request_curve_block,
                print_error=False)
            # print(sum(data))
            # print((hex(ack), sum(data)))
            # print('psbsmp.curve_read-1')
            if ack != self.CONST_BSMP.ACK_OK:
                # print('psbsmp.curve_read-2')
                if curve_id == PSBSMP.CURVE_ID_SCOPE and \
                   ack == self.CONST_BSMP.ACK_RESOURCE_BUSY:
                    # print('sit1, add:{}, curve_id:{}, block:{}'.format(
                    #     add, curve_id, block))
                    # This is the expected behaviour when DSP is writting to
                    # buffer sample
                    return None
                # anomalous response!
                PSBSMP.anomalous_response(
                    self.CONST_BSMP.CMD_REQUEST_CURVE_BLOCK, ack,
                    curve_len=len(curve),
                    curve_id=curve_id,
                    block=block,
                    index=idx)
                # print('sit2, add:{}, curve_id:{}, block:{}'.format(
                #     add, curve_id, block))
                return None
            else:
                # print('sit3, add:{}, curve_id:{}, block:{}'.format(
                #     add, curve_id, block))
                idx_w = slice(idx[0], idx[1])
                idx_r = slice(0, idx[1] - idx[0])
                curve[idx_w] = data[idx_r]
        return curve

    def _curve_bsmp_write(self, curve_id, curve):
        # select minimum curve size between spec and firmware.
        wfmref_size_min = self._curve_get_implementable_size(
            curve_id, len(curve))

        # send curve blocks
        curve_entity = self.entities.curves[curve_id]
        indices = curve_entity.get_indices(wfmref_size_min)
        # print('writing - curve id: ', curve_id)
        # print('writing - indices: ', indices)

        # time0 = _time.time()
        for block, idx in enumerate(indices):
            data = curve[idx[0]:idx[1]]
            # print(sum(data))
            ack, data = self.curve_block(
                curve_id=curve_id,
                block=block,
                value=data,
                timeout=self._timeout_curve_block)
            # print((hex(ack), data))
            if ack != self.CONST_BSMP.ACK_OK:
                print(('BSMP response not OK in '
                       '_curve_bsmp_write: ack = 0x{:02X}!').format(ack))
                PSBSMP.anomalous_response(
                    self.CONST_BSMP.CMD_CURVE_BLOCK, ack,
                    curve_len=len(curve),
                    curve_id=curve_id,
                    block=block,
                    index=idx)
        # time1 = _time.time()
        # print('blocks write: {:.4f} ms'.format(1000*(time1 - time0)))

    def _bsmp_get_variable_values(self, *var_ids):
        values = [None] * len(var_ids)
        for i, var_id in enumerate(var_ids):
            _, values[i] = self.read_variable(
                var_id=var_id, timeout=self._timeout_read_variable)
        return values

    def _curve_get_implementable_size(self, curve_id, curve_size):
        curve_entity = self.entities.curves[curve_id]
        curve_size_entity = curve_entity.max_size_t_float
        curve_size_min = min(curve_size_entity, curve_size)
        return curve_size_min

    def _curve_check_size(self, curve_id, curve_size):
        if curve_size > self.curve_maxsize(curve_id=curve_id):
            raise IndexError('Curve exceeds maximum size according to spec!')

    def _read_parm(self, eid, idx):
        ack, val = self.execute_function(
            func_id=PSBSMP.CONST.F_GET_PARAM,
            input_val=(eid, idx))
        if ack == PSBSMP.CONST_BSMP.CMD_FUNCTION_ERROR:
            # TODO: when a uninitialized parameter is requested
            # the UDC responds with a function error.
            # this is a temporary bug bypass while firmware is not
            # updated!
            val = float('NaN')
        elif ack != PSBSMP.CONST_BSMP.ACK_OK:
            return None
        return val


# --- DCDC ---


class FBP(PSBSMP):
    """BSMP with EntitiesFBP."""

    SOFB_PRINT_COMM_ERRORS = True

    IS_DCLINK = False
    CONST = _const_psbsmp.ConstFBP
    _ACK_OK = _np.zeros(_const_psbsmp.UDC_MAX_NR_DEV, dtype=int)

    def __init__(self, slave_address, pru=None):
        """Init BSMP."""
        PSBSMP.__init__(
            self, slave_address, _etity_psbsmp.EntitiesFBP(), pru=pru)

        # SOFB attributes
        self._sofb_ps_setpoint = None
        self._sofb_ps_reference = None
        self._sofb_ps_iload = None
        self._sofb_ps_readback_ref = None
        self._sofb_ps_func_return = None

    # --- SOFB methods ---

    @property
    def sofb_ps_setpoint(self):
        """."""
        return self._sofb_ps_setpoint

    @property
    def sofb_ps_reference(self):
        """."""
        return self._sofb_ps_reference

    @property
    def sofb_ps_iload(self):
        """."""
        return self._sofb_ps_iload

    @property
    def sofb_ps_readback_ref(self):
        """Return mirror powersupply currents read after last setpoint."""
        return self._sofb_ps_readback_ref

    @property
    def sofb_ps_func_return(self):
        """Return ack code of last function execution."""
        return self._sofb_ps_func_return

    def sofb_ps_setpoint_set(self, value):
        """."""
        self._sofb_ps_setpoint = value
        ack, func_resp = self.ps_function_set_slowref_fbp_readback_ref(value)
        if ack == self.CONST_BSMP.ACK_OK:
            self._sofb_ps_readback_ref = func_resp
            self._sofb_ps_func_return = FBP._ACK_OK
        else:
            self._sofb_func_error(ack, func_resp, 'sofb_ps_setpoint_set')

    def sofb_update(self):
        """."""
        data = self._sofb_read_group_of_variables()
        (self._sofb_ps_setpoint,
         self._sofb_ps_reference,
         self._sofb_ps_iload) = data

    def _sofb_read_group_of_variables(self):
        group_id = self.CONST.G_SOFB
        ack, func_resp = self.read_group_of_variables(
            group_id=group_id)
        if ack == self.CONST_BSMP.ACK_OK:
            self._sofb_ps_func_return = FBP._ACK_OK
            setpoints, references, iload = \
                _np.array(func_resp).reshape((3, -1))
        else:
            setpoints, references, iload = None, None, None
            self._sofb_func_error(
                ack, func_resp, '_sofb_read_group_of_variables')

        return setpoints, references, iload

    def _sofb_func_error(self, ack, func_resp, methodname):
        func_resp = ord(func_resp)
        self._sofb_ps_func_return = FBP._ACK_OK + func_resp
        if self.SOFB_PRINT_COMM_ERRORS:
            sfmt = 'FBP: Anomalous response ' + methodname + \
                ': ack:0x{:02X}, func_resp:0x{:02X}'
            print(sfmt.format(ack, func_resp))


class FAC_DCDC(PSBSMP):
    """BSMP with EntitiesFAC_DCDC."""

    IS_DCLINK = False
    CONST = _const_psbsmp.ConstFAC_DCDC

    def __init__(self, slave_address, pru=None):
        """Init BSMP."""
        PSBSMP.__init__(
            self, slave_address, _etity_psbsmp.EntitiesFAC_DCDC(), pru=pru)


class FAC_2P4S_DCDC(PSBSMP):
    """BSMP with EntitiesFAC_2P4S_DCDC."""

    IS_DCLINK = False
    CONST = _const_psbsmp.ConstFAC_2P4S_DCDC

    def __init__(self, slave_address, pru=None):
        """Init BSMP."""
        PSBSMP.__init__(
            self, slave_address, _etity_psbsmp.EntitiesFAC_2P4S_DCDC(),
            pru=pru)


class FAC_2S_DCDC(PSBSMP):
    """BSMP with EntitiesFAC_2S_DCDC."""

    IS_DCLINK = False
    CONST = _const_psbsmp.ConstFAC_2S_DCDC

    def __init__(self, slave_address, pru=None):
        """Init BSMP."""
        PSBSMP.__init__(
            self, slave_address, _etity_psbsmp.EntitiesFAC_2S_DCDC(), pru=pru)


class FAP(PSBSMP):
    """BSMP with EntitiesFAP."""

    IS_DCLINK = False
    CONST = _const_psbsmp.ConstFAP

    def __init__(self, slave_address, pru=None):
        """Init BSMP."""
        PSBSMP.__init__(
            self, slave_address, _etity_psbsmp.EntitiesFAP(), pru=pru)


class FAP_4P(PSBSMP):
    """BSMP with EntitiesFAP_4P."""

    IS_DCLINK = False
    CONST = _const_psbsmp.ConstFAP_4P

    def __init__(self, slave_address, pru=None):
        """Init BSMP."""
        PSBSMP.__init__(
            self, slave_address, _etity_psbsmp.EntitiesFAP_4P(), pru=pru)


class FAP_2P2S(PSBSMP):
    """BSMP with EntitiesFAP_2P2S."""

    IS_DCLINK = False
    CONST = _const_psbsmp.ConstFAP_2P2S

    def __init__(self, slave_address, pru=None):
        """Init BSMP."""
        PSBSMP.__init__(
            self, slave_address, _etity_psbsmp.EntitiesFAP_2P2S(), pru=pru)


# --- ACDC ---


class FBP_DCLink(PSBSMP):
    """BSMP with EntitiesFBP_DCLink."""

    IS_DCLINK = True
    CONST = _const_psbsmp.ConstFBP_DCLink

    def __init__(self, slave_address, pru=None):
        """Init BSMP."""
        PSBSMP.__init__(
            self, slave_address, _etity_psbsmp.EntitiesFBP_DCLink(), pru=pru)


class FAC_2P4S_ACDC(PSBSMP):
    """BSMP with EntitiesFAC_2P4S_ACDC."""

    IS_DCLINK = True
    CONST = _const_psbsmp.ConstFAC_2P4S_ACDC

    def __init__(self, slave_address, pru=None):
        """Init BSMP."""
        PSBSMP.__init__(
            self, slave_address, _etity_psbsmp.EntitiesFAC_2P4S_ACDC(),
            pru=pru)


class FAC_2S_ACDC(PSBSMP):
    """BSMP with EntitiesFAC_2S_ACDC."""

    IS_DCLINK = True
    CONST = _const_psbsmp.ConstFAC_2S_ACDC

    def __init__(self, slave_address, pru=None):
        """Init BSMP."""
        PSBSMP.__init__(
            self, slave_address, _etity_psbsmp.EntitiesFAC_2S_ACDC(), pru=pru)

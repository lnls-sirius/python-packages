"""Power Supply Model classes."""

from . import pscreaders as _readers
from . import pscwriters as _writers
from . import pscontroller as _controller

from ..bsmp import constants as _const_psbsmp
from ..bsmp import entities as _etity_psbsmp


class _PSModel:
    """Abstract power supply model."""

    # class constant attributes to be overrriden in subclasses.
    _n = None  # PSModel name.
    _c = _const_psbsmp.ConstPSBSMP  # PSModel constantes.
    _e = _etity_psbsmp.EntitiesPS  # PSModel entities.

    # psmodel-specific conversions
    _bsmp_variables = dict()  # this will be filled in subclasses
    _pruc_properties = dict()  # this will be filled in subclasses

    # dictionary of epics PVs to common psmodel fields or variables.
    _e2v = {
        # Epics to direct BSMP variable
        'CycleEnbl-Mon': _c.V_SIGGEN_ENABLE,
        'CycleType-Sts': _c.V_SIGGEN_TYPE,
        'CycleNrCycles-RB': _c.V_SIGGEN_NUM_CYCLES,
        'CycleIndex-Mon': _c.V_SIGGEN_N,
        'CycleFreq-RB': _c.V_SIGGEN_FREQ,
        'CycleAmpl-RB': _c.V_SIGGEN_AMPLITUDE,
        'CycleOffset-RB': _c.V_SIGGEN_OFFSET,
        'CycleAuxParam-RB': _c.V_SIGGEN_AUX_PARAM,
        }
    _e2f = {
        # Epics to BSMP variable with pre-processing
        'PwrState-Sts': (_readers.PwrState, _c.V_PS_STATUS),
        'OpMode-Sts': (_readers.OpMode, _c.V_PS_STATUS),
        'CtrlMode-Mon': (_readers.CtrlMode, _c.V_PS_STATUS),
        'CtrlLoop-Sts': (_readers.CtrlLoop, _c.V_PS_STATUS),
        'Version-Cte': (_readers.Version, _c.V_FIRMWARE_VERSION),
        }
    _e2c = {
        # Epics to PRUCrontroller property
        'PRUCtrlQueueSize-Mon': 'queue_length',
        }
    _e2o = {
        # Epics to field object;
        'TimestampUpdate-Mon': _readers.TimestampUpdate,
        'Wfm-RB': _readers.WfmRBCurve,
        'WfmRef-Mon': _readers.WfmRefMonCurve,
        'Wfm-Mon': _readers.WfmMonCurve,
        'WfmIndex-Mon': _readers.WfmIndexCurve,
        'WfmUpdateAuto-Sts': _readers.WfmUpdateAutoSts,
        }
    _e2p = {
        # Epics to Power Supply parameter
        # --- PS ---
        'ParamPSName-Cte': _c.P_PS_NAME,  # 00
        'ParamPSModel-Cte': _c.P_PS_MODEL,  # 01
        'ParamNrModules-Cte': _c.P_PS_NR_PSMODELS,  # 02
        # --- Communication ---
        'ParamCommCmdInferface-Cte': _c.P_COMM_CMD_INTERFACE,  # 03
        'ParamCommRS485BaudRate-Cte': _c.P_COMM_RS485_BAUDRATE,  # 04
        'ParamCommRS485Addr-Cte': _c.P_COMM_RS485_ADDRESS,  # 05
        'ParamCommRS485TermRes-Cte': _c.P_COMM_RS485_TERMINATOR_RESISTOR,  # 06
        'ParamCommUDCNetAddr-Cte': _c.P_COMM_UDC_NETWORK_ADDRESS,  # 07
        'ParamCommEthIP-Cte': _c.P_COMM_ETHERNET_IP,  # 08
        'ParamCommEthSubnetMask-Cte': _c.P_COMM_ETHERNET_SUBNET_MASK,  # 09
        'ParamCommBuzVol-Cte': _c. P_COMM_BUZZER_VOLUME,  # 10
        # --- Control ---
        'ParamCtrlFreqCtrlISR-Cte': _c.P_CTRL_FREQ_CONTROL_ISR,  # 11
        'ParamCtrlFreqTimeSlicer-Cte': _c.P_CTRL_FREQ_TIME_SLICER,  # 12
        'ParamCtrlLoopState-Cte': _c.P_CTRL_CONTROL_LOOP_STATE,  # 13
        'ParamCtrlMaxRef-Cte': _c.P_CTRL_MAX_REF,  # 14
        'ParamCtrlMinRef-Cte': _c.P_CTRL_MIN_REF,  # 15
        'ParamCtrlMaxRefOpenLoop-Cte': _c.P_CTRL_MAX_REF_OPEN_LOOP,  # 16
        'ParamCtrlMinRefOpenLoop-Cte': _c.P_CTRL_MIN_REF_OPEN_LOOP,  # 17
        # --- PWM ---
        'ParamPWMFreq-Cte': _c.P_PWM_FREQ,  # 18
        'ParamPWMDeadTime-Cte': _c.P_PWM_DEAD_TIME,  # 19
        'ParamPWMMaxDuty-Cte': _c.P_PWM_MAX_DUTY,  # 20
        'ParamPWMMinDuty-Cte': _c.P_PWM_MIN_DUTY,  # 21
        'ParamPWMMaxDutyOpenLoop-Cte': _c.P_PWM_MAX_DUTY_OPEN_LOOP,  # 22
        'ParamPWMMinDutyOpenLoop-Cte': _c.P_PWM_MIN_DUTY_OPEN_LOOP,  # 23
        'ParamPWMLimDutyShare-Cte': _c.P_PWM_LIM_DUTY_SHARE,  # 24
        # ----- class HRADC -----
        # P_HRADC_NR_BOARDS = 25
        # P_HRADC_SPI_CLK = 26
        # P_HRADC_FREQ_SAMPLING = 27
        # P_HRADC_ENABLE_HEATER = 28
        # P_HRADC_ENABLE_RAILS_MON = 29
        # P_HRADC_TRANSDUCER_OUTPUT = 30
        # P_HRADC_TRANSDUCER_GAIN = 31
        # P_HRADC_TRANSDUCER_OFFSET = 32
        # # ----- class SigGen -----
        # P_SIGGEN_TYPE = 33
        # P_SIGGEN_NUM_CYCLES = 34
        # P_SIGGEN_FREQ = 35
        # P_SIGGEN_AMPLITUDE = 36
        # P_SIGGEN_OFFSET = 37
        # P_SIGGEN_AUX_PARAM = 38
        # # ----- class WfmRef -----
        # P_WFMREF_ID = 39
        # P_WFMREF_SYNC_MODE = 40
        # P_WFMREF_FREQ = 41
        # P_WFMREF_GAIN = 42
        # P_WFMREF_OFFSET = 43
        # --- Analog Variables ---
        'ParamAnalogMax-Cte': _c.P_ANALOG_MAX,  # 44
        'ParamAnalogMin-Cte': _c.P_ANALOG_MIN,  # 45
        # --- Debounce Manager ---
        'ParamHardIntlkDebounceTime-Cte': _c.P_HARD_INTLK_DEBOUNCE_TIME,  # 46
        'ParamHardIntlkResetTime-Cte': _c.P_HARD_INTLK_RESET_TIME,  # 47
        'ParamSoftIntlkDebounceTime-Cte': _c.P_SOFT_INTLK_DEBOUNCE_TIME,  # 48
        'ParamSoftIntlkResetTime-Cte': _c.P_SOFT_INTLK_RESET_TIME,  # 49
        # ---- Scope -----
        # P_SCOPE_SAMPLING_FREQUENCY = 50
        # P_SCOPE_DATA_SOURCE = 51
        }

    @property
    def name(self):
        """Model name."""
        return self._n

    @property
    def bsmp_constants(self):
        """PRU Controller parameters."""
        return self._c

    @property
    def entities(self):
        """PRU Controller parameters."""
        return self._e()

    def field(self, device_id, epics_field, pru_controller):
        """Return field."""
        # common field
        e2f = self._fields_common
        field = e2f(device_id, epics_field, pru_controller)
        if field:
            return field
        # especific field (bsmp variable)
        e2f = self._fields_psmodel_specific_bsmp_variables
        field = e2f(device_id, epics_field, pru_controller)
        if field:
            return field
        # specific field (PRUController property)
        e2f = self._fields_psmodel_specific_pruc_properties
        field = e2f(device_id, epics_field, pru_controller)
        return field

    @staticmethod
    def function(device_ids, epics_field, pru_controller, setpoints):
        """Return function."""
        function = _PSModel._function_common_sp(
            device_ids, epics_field, pru_controller, setpoints)
        if function:
            return function

        function = _PSModel._function_common_cmd(
            device_ids, epics_field, pru_controller, setpoints)
        if function:
            return function

        function = _PSModel._function_cfgsiggen(
            device_ids, epics_field, pru_controller, setpoints)
        if function:
            return function

        function = _PSModel._function_wfm(
            device_ids, epics_field, pru_controller, setpoints)
        if function:
            return function

        return _writers.BSMPFunctionNull()

    def controller(self, readers, writers, pru_controller, devices):
        """Return controller."""
        return _controller.StandardPSController(
            readers, writers, pru_controller, devices)

    # --- private methods ---

    def _fields_common(self, device_id, epics_field, pru_controller):
        if epics_field in self._e2v:
            var_id = self._e2v[epics_field]
            return _readers.Variable(pru_controller, device_id, var_id)
        if epics_field in self._e2p:
            param_id = self._e2p[epics_field]
            return _readers.ConstParameter(pru_controller, device_id, param_id)
        if epics_field in self._e2f:
            field, var_id = self._e2f[epics_field]
            return field(_readers.Variable(pru_controller, device_id, var_id))
        if epics_field in self._e2c:
            attr = self._e2c[epics_field]
            return _readers.PRUCProperty(pru_controller, attr)
        if epics_field in self._e2o:
            field = self._e2o[epics_field]
            return field(pru_controller, device_id)
        return None

    def _fields_psmodel_specific_bsmp_variables(
            self, device_id, epics_field, pru_controller):
        # Specific fields
        if epics_field in self._bsmp_variables:
            var_id = self._bsmp_variables[epics_field]
            return _readers.Variable(pru_controller, device_id, var_id)
        return None

    def _fields_psmodel_specific_pruc_properties(
            self, _, epics_field, pru_controller):
        if epics_field in self._pruc_properties:
            attr = self._pruc_properties[epics_field]
            return _readers.PRUCProperty(pru_controller, attr)

    @staticmethod
    def _function_common_sp(
            device_ids, epics_field, pru_controller, setpoints):
        _c = _const_psbsmp.ConstPSBSMP
        if epics_field == 'PwrState-Sel':
            return _writers.PSPwrState(device_ids, pru_controller, setpoints)
        if epics_field == 'OpMode-Sel':
            bsmpfunc = _writers.BSMPFunction(
                device_ids, pru_controller, _c.F_SELECT_OP_MODE)
            return _writers.PSOpMode(
                device_ids, bsmpfunc, setpoints)
        if epics_field == 'CtrlLoop-Sel':
            return _writers.CtrlLoop(device_ids, pru_controller, setpoints)
        if epics_field == 'Current-SP':
            return _writers.Current(device_ids, pru_controller, setpoints)
        return None

    @staticmethod
    def _function_common_cmd(
            device_ids, epics_field, pru_controller, setpoints):
        _c = _const_psbsmp.ConstPSBSMP
        if epics_field == 'Reset-Cmd':
            return _writers.Command(
                device_ids, pru_controller, _c.F_RESET_INTERLOCKS, setpoints)
        if epics_field == 'SyncPulse-Cmd':
            return _writers.Command(
                device_ids, pru_controller, _c.F_SYNC_PULSE, setpoints)
        if epics_field == 'Abort-Cmd':
            return _writers.BSMPFunctionNull()
        return None

    @staticmethod
    def _function_cfgsiggen(
            device_ids, epics_field, pru_controller, setpoints):
        p2i = {
            'CycleType-Sel': 0,
            'CycleNrCycles-SP': 1,
            'CycleFreq-SP': 2,
            'CycleAmpl-SP': 3,
            'CycleOffset-SP': 4,
            'CycleAuxParam-SP': 5,
            }
        _c = _const_psbsmp.ConstPSBSMP
        if epics_field in p2i:
            idx = p2i[epics_field]
            return _writers.CfgSiggen(
                device_ids, pru_controller, idx, setpoints)
        if epics_field == 'CycleDsbl-Cmd':
            return _writers.Command(
                device_ids, pru_controller, _c.F_DISABLE_SIGGEN, setpoints)
        return None

    @staticmethod
    def _function_wfm(
            device_ids, epics_field, pru_controller, setpoints):
        if epics_field == 'Wfm-SP':
            return _writers.WfmSP(
                device_ids, pru_controller, setpoints)
        if epics_field == 'WfmUpdate-Cmd':
            return _writers.WfmUpdate(
                device_ids, pru_controller, setpoints)
        if epics_field == 'WfmUpdateAuto-Sel':
            return _writers.WfmUpdateAutoSel(
                device_ids, pru_controller, setpoints)
        if epics_field == 'WfmMonAcq-Sel':
            return _writers.WfmMonAcq(
                device_ids, pru_controller, setpoints)
        return None


# Standard PS that supply magnets
class PSModelFBP(_PSModel):
    """FBP model."""

    _n = 'FBP'
    _c = _const_psbsmp.ConstFBP
    _e = _etity_psbsmp.EntitiesFBP

    _bsmp_variables = {
        'IntlkSoft-Mon':  _const_psbsmp.ConstFBP.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon':  _const_psbsmp.ConstFBP.V_PS_HARD_INTERLOCKS,
        'WfmSyncPulseCount-Mon': _const_psbsmp.ConstFBP.V_COUNTER_SYNC_PULSE,
        'Current-RB':  _const_psbsmp.ConstFBP.V_PS_SETPOINT,
        'CurrentRef-Mon':  _const_psbsmp.ConstFBP.V_PS_REFERENCE,
        'Current-Mon':  _const_psbsmp.ConstFBP.V_I_LOAD,
        'LoadVoltage-Mon': _const_psbsmp.ConstFBP.V_V_LOAD,
        'DCLinkVoltage-Mon': _const_psbsmp.ConstFBP.V_V_DCLINK,
        'SwitchesTemperature-Mon': _const_psbsmp.ConstFBP.V_TEMP_SWITCHES,
        'PWMDutyCycle-Mon': _const_psbsmp.ConstFBP.V_DUTY_CYCLE,
    }

    _pruc_properties = {
        'SOFBMode-Sts': 'sofb_mode',
        'SOFBCurrent-RB': 'sofb_current_rb',
        'SOFBCurrentRef-Mon': 'sofb_current_refmon',
        'SOFBCurrent-Mon': 'sofb_current_mon',
    }

    def function(self, device_ids, epics_field, pru_controller, setpoints):
        """Return function."""
        if epics_field == 'SOFBCurrent-SP':
            return _writers.SOFBCurrent(
                device_ids, pru_controller, setpoints)
        if epics_field == 'SOFBMode-Sel':
            return _writers.SOFBMode(
                device_ids, pru_controller, setpoints)
        return super().function(
            device_ids, epics_field, pru_controller, setpoints)


class PSModelFBP_FOFB(_PSModel):
    """FBP_FOFB power supply model."""

    _n = 'FBP_FOFB'
    _c = _const_psbsmp.ConstFBP
    _e = _etity_psbsmp.EntitiesFBP


class PSModelFAC_DCDC(_PSModel):
    """FAC power supply model."""

    _n = 'FAC_DCDC'
    _c = _const_psbsmp.ConstFAC_DCDC
    _e = _etity_psbsmp.EntitiesFAC_DCDC

    _bsmp_variables = {
        'WfmSyncPulseCount-Mon': _c.V_COUNTER_SYNC_PULSE,
        'IntlkSoft-Mon': _c.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon': _c.V_PS_HARD_INTERLOCKS,
        'Current-RB': _c.V_PS_SETPOINT,
        'CurrentRef-Mon': _c.V_PS_REFERENCE,
        'Current-Mon': _c.V_I_LOAD_MEAN,
        'Current1-Mon': _c.V_I_LOAD1,
        'Current2-Mon': _c.V_I_LOAD2,
        'LoadVoltage-Mon': _c.V_V_LOAD,
        'InductorsTemperature-Mon': _c.V_TEMP_INDUCTORS,
        'IGBTSTemperature-Mon': _c.V_TEMP_IGBTS,
        'PWMDutyCycle-Mon': _c.V_DUTY_CYCLE,
        }


class PSModelFAC_2S_DCDC(_PSModel):
    """FAC_2S_DCDC power supply model."""

    _n = 'FAC_2S_DCDC'
    _c = _const_psbsmp.ConstFAC_2S_DCDC
    _e = _etity_psbsmp.EntitiesFAC_2S_DCDC

    _bsmp_variables = {
        'Current-RB': _c.V_PS_SETPOINT,
        'CurrentRef-Mon': _c.V_PS_REFERENCE,
        'WfmSyncPulseCount-Mon': _c.V_COUNTER_SYNC_PULSE,
        'IntlkSoft-Mon': _c.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon': _c.V_PS_HARD_INTERLOCKS,
        'Current-Mon': _c.V_I_LOAD_MEAN,
        'Current1-Mon': _c.V_I_LOAD1,
        'Current2-Mon': _c.V_I_LOAD2,
        'LoadVoltage-Mon': _c.V_V_LOAD,
        'Module1Voltage-Mon': _c.V_V_OUT_1,
        'Module2Voltage-Mon': _c.V_V_OUT_2,
        'CapacitorBank1Voltage-Mon': _c.V_V_CAPBANK_1,
        'CapacitorBank2Voltage-Mon': _c.V_V_CAPBANK_2,
        'PWMDutyCycle1-Mon': _c.V_DUTY_CYCLE_1,
        'PWMDutyCycle2-Mon': _c.V_DUTY_CYCLE_2,
        'PWMDutyDiff-Mon': _c.V_DUTY_DIFF,
        'IIB1InductorsTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_1,
        'IIB1HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_1,
        'IIB2InductorsTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_2,
        'IIB2HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_2,
        'IntlkIIB1-Mon': _c.V_IIB_INTERLOCKS_1,
        'IntlkIIB2-Mon': _c.V_IIB_INTERLOCKS_2,
        }


class PSModelFAC_2P4S_DCDC(PSModelFAC_DCDC):
    """FAC_2P4S_DCDC power supply model (BO Dipoles)."""

    _n = 'FAC_2P4S_DCDC'
    _c = _const_psbsmp.ConstFAC_2P4S_DCDC
    _e = _etity_psbsmp.EntitiesFAC_2P4S_DCDC

    _bsmp_variables = {
        'Current-RB': _c.V_PS_SETPOINT,
        'CurrentRef-Mon': _c.V_PS_REFERENCE,
        'WfmSyncPulseCount-Mon': _c.V_COUNTER_SYNC_PULSE,
        'IntlkSoft-Mon': _c.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon': _c.V_PS_HARD_INTERLOCKS,
        'Current-Mon': _c.V_I_LOAD_MEAN,
        'Current1-Mon': _c.V_I_LOAD1,
        'Current2-Mon': _c.V_I_LOAD2,
        'LoadVoltage-Mon': _c.V_V_LOAD,
        'CapacitorBank1Voltage-Mon': _c.V_V_CAPBANK_1,
        'CapacitorBank2Voltage-Mon': _c.V_V_CAPBANK_2,
        'CapacitorBank3Voltage-Mon': _c.V_V_CAPBANK_3,
        'CapacitorBank4Voltage-Mon': _c.V_V_CAPBANK_4,
        'CapacitorBank5Voltage-Mon': _c.V_V_CAPBANK_5,
        'CapacitorBank6Voltage-Mon': _c.V_V_CAPBANK_6,
        'CapacitorBank7Voltage-Mon': _c.V_V_CAPBANK_7,
        'CapacitorBank8Voltage-Mon': _c.V_V_CAPBANK_8,
        'Module1Voltage-Mon': _c.V_V_OUT_1,
        'Module2Voltage-Mon': _c.V_V_OUT_2,
        'Module3Voltage-Mon': _c.V_V_OUT_3,
        'Module4Voltage-Mon': _c.V_V_OUT_4,
        'Module5Voltage-Mon': _c.V_V_OUT_5,
        'Module6Voltage-Mon': _c.V_V_OUT_6,
        'Module7Voltage-Mon': _c.V_V_OUT_7,
        'Module8Voltage-Mon': _c.V_V_OUT_8,
        'PWMDutyCycle1-Mon': _c.V_DUTY_CYCLE_1,
        'PWMDutyCycle2-Mon': _c.V_DUTY_CYCLE_2,
        'PWMDutyCycle3-Mon': _c.V_DUTY_CYCLE_3,
        'PWMDutyCycle4-Mon': _c.V_DUTY_CYCLE_4,
        'PWMDutyCycle5-Mon': _c.V_DUTY_CYCLE_5,
        'PWMDutyCycle6-Mon': _c.V_DUTY_CYCLE_6,
        'PWMDutyCycle7-Mon': _c.V_DUTY_CYCLE_7,
        'PWMDutyCycle8-Mon': _c.V_DUTY_CYCLE_8,
        'Arm1Current-Mon': _c.V_I_ARM_1,
        'Arm2Current-Mon': _c.V_I_ARM_2,
        'IIB1InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_1,
        'IIB1HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_1,
        'IIB2InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_2,
        'IIB2HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_2,
        'IIB3InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_3,
        'IIB3HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_3,
        'IIB4InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_4,
        'IIB4HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_4,
        'IIB5InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_5,
        'IIB5HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_5,
        'IIB6InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_6,
        'IIB6HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_6,
        'IIB7InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_7,
        'IIB7HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_7,
        'IIB8InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_8,
        'IIB8HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_8,
        'IntlkIIB1-Mon': _c.V_IIB_INTERLOCKS_1,
        'IntlkIIB2-Mon': _c.V_IIB_INTERLOCKS_2,
        'IntlkIIB3-Mon': _c.V_IIB_INTERLOCKS_3,
        'IntlkIIB4-Mon': _c.V_IIB_INTERLOCKS_4,
        'IntlkIIB5-Mon': _c.V_IIB_INTERLOCKS_5,
        'IntlkIIB6-Mon': _c.V_IIB_INTERLOCKS_6,
        'IntlkIIB7-Mon': _c.V_IIB_INTERLOCKS_7,
        'IntlkIIB8-Mon': _c.V_IIB_INTERLOCKS_8,
        }


class PSModelFAP(_PSModel):
    """FAP power supply model."""

    _n = 'FAP'
    _c = _const_psbsmp.ConstFAP
    _e = _etity_psbsmp.EntitiesFAP

    _bsmp_variables = {
        'WfmSyncPulseCount-Mon': _c.V_COUNTER_SYNC_PULSE,
        'IntlkSoft-Mon': _c.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon': _c.V_PS_HARD_INTERLOCKS,
        'IntlkIIB-Mon': _c.V_IIB_INTERLOCKS,
        'Current-RB': _c.V_PS_SETPOINT,
        'CurrentRef-Mon': _c.V_PS_REFERENCE,
        'Current-Mon': _c.V_I_LOAD_MEAN,
        'Current1-Mon': _c.V_I_LOAD1,
        'Current2-Mon': _c.V_I_LOAD2,
        'IIBInductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB,
        'IIBHeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB,
        'IIBLeakCurrent-Mon': _c.V_I_LEAKAGE_IIB,
        }


class PSModelFAP_4P(_PSModel):
    """FAP_4P power supply model."""

    _n = 'FAP_4P'
    _c = _const_psbsmp.ConstFAP_4P
    _e = _etity_psbsmp.EntitiesFAP_4P

    _bsmp_variables = {
        'WfmSyncPulseCount-Mon': _c.V_COUNTER_SYNC_PULSE,
        'IntlkSoft-Mon': _c.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon': _c.V_PS_HARD_INTERLOCKS,
        'Intlk1IIB-Mon': _c.V_IIB_INTERLOCKS_1,
        'Intlk2IIB-Mon': _c.V_IIB_INTERLOCKS_2,
        'Intlk3IIB-Mon': _c.V_IIB_INTERLOCKS_3,
        'Intlk4IIB-Mon': _c.V_IIB_INTERLOCKS_4,
        'Current-RB': _c.V_PS_SETPOINT,
        'CurrentRef-Mon': _c.V_PS_REFERENCE,
        'Current-Mon': _c.V_I_LOAD_MEAN,
        'Current1-Mon': _c.V_I_LOAD1,
        'Current2-Mon': _c.V_I_LOAD2,
        'DCLink1Voltage-Mon': _c.V_V_DCLINK_1,
        'DCLink2Voltage-Mon': _c.V_V_DCLINK_2,
        'DCLink3Voltage-Mon': _c.V_V_DCLINK_3,
        'DCLink4Voltage-Mon': _c.V_V_DCLINK_4,
        'Mod1Current-Mon': _c.V_I_MOD_1,
        'Mod2Current-Mon': _c.V_I_MOD_2,
        'Mod3Current-Mon': _c.V_I_MOD_3,
        'Mod4Current-Mon': _c.V_I_MOD_4,
        'IIB1InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_1,
        'IIB1HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_1,
        'IIB2InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_2,
        'IIB2HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_2,
        'IIB3InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_3,
        'IIB3HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_3,
        'IIB4InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_4,
        'IIB4HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_4,
        }


class PSModelFAP_2P2S(_PSModel):
    """FAP_2P2S power supply model."""

    _n = 'FAP_2P2S'
    _c = _const_psbsmp.ConstFAP_2P2S
    _e = _etity_psbsmp.EntitiesFAP_2P2S

    _bsmp_variables = {
        'WfmSyncPulseCount-Mon': _c.V_COUNTER_SYNC_PULSE,
        'IntlkSoft-Mon':  _c.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon':  _c.V_PS_HARD_INTERLOCKS,
        'Current-RB':  _c.V_PS_SETPOINT,
        'CurrentRef-Mon':  _c.V_PS_REFERENCE,
        'Current-Mon':  _c.V_I_LOAD_MEAN,
        'Current1-Mon': _c.V_I_LOAD1,
        'Current2-Mon': _c.V_I_LOAD2,
        'Arm1Current-Mon': _c.V_I_ARM_1,
        'Arm2Current-Mon': _c.V_I_ARM_2,
        'Mod1IGBT1Current-Mon': _c.V_I_IGBT_1_1,
        'Mod1IGBT2Current-Mon': _c.V_I_IGBT_2_1,
        'Mod2IGBT1Current-Mon': _c.V_I_IGBT_1_2,
        'Mod2IGBT2Current-Mon': _c.V_I_IGBT_2_2,
        'Mod3IGBT1Current-Mon': _c.V_I_IGBT_1_3,
        'Mod3IGBT2Current-Mon': _c.V_I_IGBT_2_3,
        'Mod4IGBT1Current-Mon': _c.V_I_IGBT_1_4,
        'Mod4IGBT2Current-Mon': _c.V_I_IGBT_2_4,
        'DCLink1Voltage-Mon': _c.V_V_DCLINK_1,
        'DCLink2Voltage-Mon': _c.V_V_DCLINK_2,
        'DCLink3Voltage-Mon': _c.V_V_DCLINK_3,
        'DCLink4Voltage-Mon': _c.V_V_DCLINK_4,
        'PWMDutyCycle-Mon': _c.V_DUTY_MEAN,
        'Mod1IGBT1PWMDutyCycle-Mon': _c.V_DUTY_CYCLE_1_1,
        'Mod1IGBT2PWMDutyCycle-Mon': _c.V_DUTY_CYCLE_2_1,
        'Mod2IGBT1PWMDutyCycle-Mon': _c.V_DUTY_CYCLE_1_2,
        'Mod2IGBT2PWMDutyCycle-Mon': _c.V_DUTY_CYCLE_2_2,
        'Mod3IGBT1PWMDutyCycle-Mon': _c.V_DUTY_CYCLE_1_3,
        'Mod3IGBT2PWMDutyCycle-Mon': _c.V_DUTY_CYCLE_2_3,
        'Mod4IGBT1PWMDutyCycle-Mon': _c.V_DUTY_CYCLE_1_4,
        'Mod4IGBT2PWMDutyCycle-Mon': _c.V_DUTY_CYCLE_2_4,
        'Mod1VoltageInput-Mon': _c.V_V_INPUT_IIB_1,
        'Mod1VoltageOutput-Mon': _c.V_V_OUTPUT_IIB_1,
        'Mod1IGBT1IIBCurrent-Mon': _c.V_I_IGBT_1_IIB_1,
        'Mod1IGBT2IIBCurrent-Mon': _c.V_I_IGBT_2_IIB_1,
        'IIB1InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_1,
        'IIB1HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_1,
        'Mod2VoltageInput-Mon': _c.V_V_INPUT_IIB_2,
        'Mod2VoltageOutput-Mon': _c.V_V_OUTPUT_IIB_2,
        'Mod2IGBT1IIBCurrent-Mon': _c.V_I_IGBT_1_IIB_2,
        'Mod2IGBT2IIBCurrent-Mon': _c.V_I_IGBT_2_IIB_2,
        'IIB2InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_2,
        'IIB2HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_2,
        'Mod3VoltageInput-Mon': _c.V_V_INPUT_IIB_3,
        'Mod3VoltageOutput-Mon': _c.V_V_OUTPUT_IIB_3,
        'Mod3IGBT1IIBCurrent-Mon': _c.V_I_IGBT_1_IIB_3,
        'Mod3IGBT2IIBCurrent-Mon': _c.V_I_IGBT_2_IIB_3,
        'IIB3InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_3,
        'IIB3HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_3,
        'Mod4VoltageInput-Mon': _c.V_V_INPUT_IIB_4,
        'Mod4VoltageOutput-Mon': _c.V_V_OUTPUT_IIB_4,
        'Mod4IGBT1IIBCurrent-Mon': _c.V_I_IGBT_1_IIB_4,
        'Mod4IGBT2IIBCurrent-Mon': _c.V_I_IGBT_2_IIB_4,
        'IIB4InductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IIB_4,
        'IIB4HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IIB_4,
        'Intlk1IIB-Mon': _c.V_IIB_INTERLOCKS_1,
        'Intlk2IIB-Mon': _c.V_IIB_INTERLOCKS_2,
        'Intlk3IIB-Mon': _c.V_IIB_INTERLOCKS_3,
        'Intlk4IIB-Mon': _c.V_IIB_INTERLOCKS_4,
        'Mod1Current-Mon': _c.V_I_MOD_1,
        'Mod2Current-Mon': _c.V_I_MOD_2,
        'Mod3Current-Mon': _c.V_I_MOD_3,
        'Mod4Current-Mon': _c.V_I_MOD_4,
        }


class PSModelCommercial(PSModelFAC_DCDC):
    """Commercial power supply model."""


# --- ACDC ---


class PSModelFBP_DCLink(_PSModel):
    """FBP_DCLink model."""

    _n = 'FBP_DCLink'
    _c = _const_psbsmp.ConstFBP_DCLink
    _e = _etity_psbsmp.EntitiesFBP_DCLink

    _bsmp_variables = {
        'IntlkSoft-Mon': _c.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon': _c.V_PS_HARD_INTERLOCKS,
        'ModulesStatus-Mon': _c.V_MODULES_STATUS,
        'Voltage-RB': _c.V_PS_SETPOINT,
        'VoltageRef-Mon': _c.V_PS_REFERENCE,
        'Voltage-Mon': _c.V_V_OUT,
        'Voltage1-Mon': _c.V_V_OUT_1,
        'Voltage2-Mon': _c.V_V_OUT_2,
        'Voltage3-Mon': _c.V_V_OUT_3,
        'VoltageDig-Mon': _c.V_DIG_POT_TAP,
        }

    def function(self, device_ids, epics_field, pru_controller, setpoints):
        """Return function."""
        _c = PSModelFBP_DCLink._c
        if epics_field == 'PwrState-Sel':
            return _writers.PSPwrStateFBP_DCLink(
                device_ids, pru_controller, setpoints)
        elif epics_field == 'CtrlLoop-Sel':
            return _writers.CtrlLoop(device_ids, pru_controller, setpoints)
        elif epics_field == 'OpMode-Sel':
            return _writers.PSOpMode(
                device_ids,
                _writers.BSMPFunction(
                    device_ids, pru_controller, _c.F_SELECT_OP_MODE),
                setpoints)
        elif epics_field == 'Voltage-SP':
            return _writers.BSMPFunction(
                device_ids, pru_controller, _c.F_SET_SLOWREF, setpoints)
        elif epics_field == 'Reset-Cmd':
            return _writers.Command(
                device_ids, pru_controller, _c.F_RESET_INTERLOCKS, setpoints)
        elif epics_field == 'Abort-Cmd':
            return _writers.BSMPFunctionNull()
        else:
            return _writers.BSMPFunctionNull()

    def controller(self, readers, writers, pru_controller, devices):
        """Return controller."""
        return _controller.PSController(
            readers, writers, pru_controller, devices)


class PSModelFAC_2S_ACDC(_PSModel):
    """FAC_2S_ACDC model."""

    _n = 'FAC_2S_ACDC'
    _c = _const_psbsmp.ConstFAC_2S_ACDC
    _e = _etity_psbsmp.EntitiesFAC_2S_ACDC

    _bsmp_variables = {
        'IntlkSoft-Mon': _c.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon': _c.V_PS_HARD_INTERLOCKS,
        'CapacitorBankVoltage-RB': _c.V_PS_SETPOINT,
        'CapacitorBankVoltageRef-Mon': _c.V_PS_REFERENCE,
        'CapacitorBankVoltage-Mon': _c.V_V_CAPBANK,
        'RectifierVoltage-Mon': _c.V_V_OUT_RECTIFIER,
        'RectifierCurrent-Mon': _c.V_I_OUT_RECTIFIER,
        'HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK,
        'InductorsTemperature-Mon': _c.V_TEMP_INDUCTORS,
        'PWMDutyCycle-Mon': _c.V_DUTY_CYCLE,
        }

    def function(self, device_ids, epics_field, pru_controller, setpoints):
        """Return function."""
        _c = PSModelFAC_2S_ACDC._c
        if epics_field == 'PwrState-Sel':
            return _writers.PSPwrState(device_ids, pru_controller, setpoints)
        elif epics_field == 'OpMode-Sel':
            return _writers.PSOpMode(
                device_ids,
                _writers.BSMPFunction(
                    device_ids, pru_controller, _c.F_SELECT_OP_MODE),
                setpoints)
        elif epics_field == 'CtrlLoop-Sel':
            return _writers.CtrlLoop(device_ids, pru_controller, setpoints)
        elif epics_field == 'CapacitorBankVoltage-SP':
            return _writers.BSMPFunction(
                device_ids, pru_controller, _c.F_SET_SLOWREF, setpoints)
        elif epics_field == 'Reset-Cmd':
            return _writers.Command(
                device_ids, pru_controller, _c.F_RESET_INTERLOCKS, setpoints)
        elif epics_field == 'Abort-Cmd':
            return _writers.BSMPFunctionNull()
        else:
            return _writers.BSMPFunctionNull()

    def controller(self, readers, writers, pru_controller, devices):
        """Return controller."""
        return _controller.PSController(
            readers, writers, pru_controller, devices)


class PSModelFAC_2P4S_ACDC(PSModelFAC_2S_ACDC):
    """FAC_2P4S_ACDC model."""

    _n = 'FAC_2P4S_ACDC'
    _c = _const_psbsmp.ConstFAC_2P4S_ACDC
    _e = _etity_psbsmp.EntitiesFAC_2P4S_ACDC

    _bsmp_variables = {
        'IntlkSoft-Mon': _c.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon': _c.V_PS_HARD_INTERLOCKS,
        'CapacitorBankVoltage-RB': _c.V_PS_SETPOINT,
        'CapacitorBankVoltageRef-Mon': _c.V_PS_REFERENCE,
        'CapacitorBankVoltage-Mon': _c.V_V_CAPACITOR_BANK,
        'RectifierVoltage-Mon': _c.V_V_OUT_RECTIFIER,
        'RectifierCurrent-Mon': _c.V_I_OUT_RECTIFIER,
        'HeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK,
        'InductorsTemperature-Mon': _c.V_TEMP_INDUCTORS,
        'PWMDutyCycle-Mon': _c.V_DUTY_CYCLE,
        'IIBISInductorTemperature-Mon': _c.V_TEMP_INDUCTOR_IS_IIB,
        'IIBISHeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_IS_IIB,
        'IIBCmdInductorTemperature-Mon': _c.V_TEMP_INDUCTOR_CMD_IIB,
        'IIBCmdHeatSinkTemperature-Mon': _c.V_TEMP_HEATSINK_CMD_IIB,
        'IntlkIIBIS-Mon': _c.V_IIB_INTERLOCKS_IS,
        'IntlkIIBCmd-Mon': _c.V_IIB_INTERLOCKS_CMD,
        }


# --- Factory ---


class PSModelFactory:
    """PSModel Factory."""

    _psname_2_factory = {
        'FBP': PSModelFBP,
        'FBP_DCLink': PSModelFBP_DCLink,
        'FBP_FOFB': PSModelFBP,
        'FAC_DCDC': PSModelFAC_DCDC,
        'FAC_2S_DCDC': PSModelFAC_2S_DCDC,
        'FAC_2S_ACDC': PSModelFAC_2S_ACDC,
        'FAC_2P4S_DCDC': PSModelFAC_2P4S_DCDC,
        'FAC_2P4S_ACDC': PSModelFAC_2P4S_ACDC,
        'FAP': PSModelFAP,
        'FAP_2P2S': PSModelFAP_2P2S,
        'FAP_4P': PSModelFAP_4P,
        'Commercial': PSModelCommercial,
        }

    @staticmethod
    def create(psmodel):
        """Return PSModel object."""
        if psmodel in PSModelFactory._psname_2_factory:
            factory = PSModelFactory._psname_2_factory[psmodel]
            return factory()
        raise ValueError('PS Model "{}" not defined'.format(psmodel))

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
        # Scope
        'ScopeSrcAddr-RB': _c.V_SCOPE_SRC_DATA,
        'ScopeFreq-RB': _c.V_SCOPE_FREQUENCY,
        'ScopeDuration-RB': _c.V_SCOPE_DURATION,
        }
    _e2r = {
        # Epics to BSMP variable but with pre/post-processing
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
        # Epics to reader object;
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
        'ParamHRADCNrBoards-Cte': _c.P_HRADC_NR_BOARDS,  # 25
        'ParamHRADCSpiClk-Cte': _c.P_HRADC_SPI_CLK,  # 26
        'ParamHRADCFreqSampling-Cte': _c.P_HRADC_FREQ_SAMPLING,  # 27
        'ParamHRADCEnableHeater-Cte': _c.P_HRADC_ENABLE_HEATER,  # 28
        'ParamHRADCEnableRails-Cte': _c.P_HRADC_ENABLE_RAILS_MON,  # 29
        'ParamHRADCTransducerOutput-Cte': _c.P_HRADC_TRANSDUCER_OUTPUT,  # 30
        'ParamHRADCTransducerGain-Cte': _c.P_HRADC_TRANSDUCER_GAIN,  # 31
        'ParamHRADCTransducerOffset-Cte': _c.P_HRADC_TRANSDUCER_OFFSET,  # 32
        # ----- class SigGen -----
        'ParamSigGenType-Cte': _c.P_SIGGEN_TYPE,  # 33
        'ParamSigGenNumCycles-Cte': _c.P_SIGGEN_NUM_CYCLES,  # 34
        'ParamSigGenFreq-Cte': _c.P_SIGGEN_FREQ,  # 35
        'ParamSigGenAmplitude-Cte': _c.P_SIGGEN_AMPLITUDE,  # 36
        'ParamSigGenOffset-Cte': _c.P_SIGGEN_OFFSET,  # 37
        'ParamSigGenAuxParam-Cte': _c.P_SIGGEN_AUX_PARAM,  # 38
        # ----- class WfmRef -----
        'ParamWfmRefId-Cte': _c.P_WFMREF_ID,  # 39
        'ParamWfmRefSyncMode-Cte': _c.P_WFMREF_SYNC_MODE,  # 40
        'ParamWfmRefFreq-Cte': _c.P_WFMREF_FREQ,  # 41
        'ParamWfmRefGain-Cte': _c.P_WFMREF_GAIN,  # 42
        'ParamWfmRefOffset-Cte': _c.P_WFMREF_OFFSET,  # 43
        # --- Analog Variables ---
        'ParamAnalogMax-Cte': _c.P_ANALOG_MAX,  # 44
        'ParamAnalogMin-Cte': _c.P_ANALOG_MIN,  # 45
        # --- Debounce Manager ---
        'ParamHardIntlkDebounceTime-Cte': _c.P_HARD_INTLK_DEBOUNCE_TIME,  # 46
        'ParamHardIntlkResetTime-Cte': _c.P_HARD_INTLK_RESET_TIME,  # 47
        'ParamSoftIntlkDebounceTime-Cte': _c.P_SOFT_INTLK_DEBOUNCE_TIME,  # 48
        'ParamSoftIntlkResetTime-Cte': _c.P_SOFT_INTLK_RESET_TIME,  # 49
        # ---- Scope -----
        'ParamScopeSamplingFreq-Cte': _c.P_SCOPE_SAMPLING_FREQUENCY,  # 50
        'ParamScopeDataSource-Cte': _c.P_SCOPE_DATA_SOURCE,  # 51
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

    def reader(self, device_id, epics_field, pru_controller):
        """Return reader."""
        # common reader
        e2f = self._readers_common
        reader = e2f(device_id, epics_field, pru_controller)
        if reader:
            return reader
        # especific reader (bsmp variable)
        e2f = self._readers_psmodel_specific_bsmp_variables
        reader = e2f(device_id, epics_field, pru_controller)
        if reader:
            return reader
        # specific reader (PRUController property)
        e2f = self._readers_psmodel_specific_pruc_properties
        reader = e2f(device_id, epics_field, pru_controller)
        return reader

    @staticmethod
    def writer(device_ids, epics_field, pru_controller, setpoints):
        """Return writer."""
        writer = _PSModel._writer_common_sp(
            device_ids, epics_field, pru_controller, setpoints)
        if writer:
            return writer

        writer = _PSModel._writer_common_cmd(
            device_ids, epics_field, pru_controller, setpoints)
        if writer:
            return writer

        writer = _PSModel._writer_cfgsiggen(
            device_ids, epics_field, pru_controller, setpoints)
        if writer:
            return writer

        writer = _PSModel._writer_wfm(
            device_ids, epics_field, pru_controller, setpoints)
        if writer:
            return writer

        return _writers.BSMPFunctionNull()

    def controller(self, readers, writers, pru_controller, devices):
        """Return controller."""
        return _controller.StandardPSController(
            readers, writers, pru_controller, devices)

    # --- private methods ---

    def _readers_common(self, device_id, epics_field, pru_controller):
        if epics_field in self._e2v:
            var_id = self._e2v[epics_field]
            return _readers.Variable(pru_controller, device_id, var_id)
        if epics_field in self._e2p:
            param_id = self._e2p[epics_field]
            return _readers.ConstParameter(pru_controller, device_id, param_id)
        if epics_field in self._e2r:
            reader, var_id = self._e2r[epics_field]
            return reader(_readers.Variable(pru_controller, device_id, var_id))
        if epics_field in self._e2c:
            attr = self._e2c[epics_field]
            return _readers.PRUCProperty(pru_controller, attr)
        if epics_field in self._e2o:
            reader = self._e2o[epics_field]
            return reader(pru_controller, device_id)
        return None

    def _readers_psmodel_specific_bsmp_variables(
            self, device_id, epics_field, pru_controller):
        # Specific fields
        if epics_field in self._bsmp_variables:
            var_id = self._bsmp_variables[epics_field]
            return _readers.Variable(pru_controller, device_id, var_id)
        return None

    def _readers_psmodel_specific_pruc_properties(
            self, _, epics_field, pru_controller):
        if epics_field in self._pruc_properties:
            attr = self._pruc_properties[epics_field]
            return _readers.PRUCProperty(pru_controller, attr)

    @staticmethod
    def _writer_common_sp(
            device_ids, epics_field, pru_controller, setpoints):
        _c = _const_psbsmp.ConstPSBSMP
        if epics_field == 'PwrState-Sel':
            return _writers.PSPwrState(device_ids, pru_controller, setpoints)
        elif epics_field == 'OpMode-Sel':
            bsmpfunc = _writers.BSMPFunction(
                device_ids, pru_controller, _c.F_SELECT_OP_MODE)
            return _writers.PSOpMode(
                device_ids, bsmpfunc, setpoints)
        elif epics_field == 'CtrlLoop-Sel':
            return _writers.CtrlLoop(device_ids, pru_controller, setpoints)
        elif epics_field == 'Current-SP':
            return _writers.Current(device_ids, pru_controller, setpoints)
        elif epics_field == 'ScopeFreq-SP':
            return _writers.ScopeFreq(device_ids, pru_controller, setpoints)
        elif epics_field == 'ScopeDuration-SP':
            return _writers.ScopeDuration(device_ids, pru_controller, setpoints)
        elif epics_field == 'ScopeSrcAddr-SP':
            return _writers.ScopeSrcAddr(device_ids, pru_controller, setpoints)
        return None

    @staticmethod
    def _writer_common_cmd(
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
    def _writer_cfgsiggen(
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
    def _writer_wfm(
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

    def writer(self, device_ids, epics_field, pru_controller, setpoints):
        """Return writer."""
        if epics_field == 'SOFBCurrent-SP':
            return _writers.SOFBCurrent(
                device_ids, pru_controller, setpoints)
        if epics_field == 'SOFBMode-Sel':
            return _writers.SOFBMode(pru_controller, setpoints)
        if epics_field == 'SOFBUpdate-Cmd':
            return _writers.SOFBUpdate(pru_controller, setpoints)
        return super().writer(
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
        'Current-RB': _c.V_PS_SETPOINT,
        'CurrentRef-Mon': _c.V_PS_REFERENCE,
        'WfmSyncPulseCount-Mon': _c.V_COUNTER_SYNC_PULSE,
        'IntlkSoft-Mon': _c.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon': _c.V_PS_HARD_INTERLOCKS,
        'Current-Mon': _c.V_I_LOAD_MEAN,
        'Current1-Mon': _c.V_I_LOAD1,
        'Current2-Mon': _c.V_I_LOAD2,
        'CapacitorBankVoltage-Mon': _c.V_V_CAPBANK,
        'PWMDutyCycle-Mon': _c.V_DUTY_CYCLE,
        'VoltageInputIIB-Mon': _c.V_V_INPUT_IIB,
        'CurrentInputIIB-Mon': _c.V_I_INPUT_IIB,
        'CurrentOutputIIB-Mon': _c.V_I_OUTPUT_IIB,
        'IGBT1TemperatureIIB-Mon': _c.V_TEMP_IGBT_1_IIB,
        'IGBT2TemperatureIIB-Mon': _c.V_TEMP_IGBT_2_IIB,
        'InductorsTemperatureIIB-Mon': _c.V_TEMP_INDUCTOR_IIB,
        'HeatSinkTemperatureIIB-Mon': _c.V_TEMP_HEATSINK_IIB,
        'IGBTDriverVoltageIIB-Mon': _c.V_V_DRIVER_IIB,
        'IGBT1DriverCurrentIIB-Mon': _c.V_I_DRIVER_1_IIB,
        'IGBT2DriverCurrentIIB-Mon': _c.V_I_DRIVER_2_IIB,
        'LeakCurrentIIB-Mon': _c.V_I_LEAKAGE_IIB,
        'BoardTemperatureIIB-Mon': _c.V_TEMP_BOARD_IIB,
        'RelativeHumidityIIB-Mon': _c.V_RH_IIB,
        'IntlkIIB-Mon': _c.V_IIB_INTERLOCKS,
        'AlarmsIIB-Mon': _c.V_IIB_ALARMS,
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
        'CapacitorBankVoltageMod1-Mon': _c.V_V_CAPBANK_1,
        'CapacitorBankVoltageMod2-Mon': _c.V_V_CAPBANK_2,
        'PWMDutyCycleMod1-Mon': _c.V_DUTY_CYCLE_1,
        'PWMDutyCycleMod2-Mon': _c.V_DUTY_CYCLE_2,
        'VoltageInputIIBMod1-Mon': _c.V_V_INPUT_IIB_1,
        'CurrentInputIIBMod1-Mon': _c.V_I_INPUT_IIB_1,
        'CurrentOutputIIBMod1-Mon': _c.V_I_OUTPUT_IIB_1,
        'IGBT1TemperatureIIBMod1-Mon': _c.V_TEMP_IGBTS_1_IIB_1,
        'IGBT2TemperatureIIBMod1-Mon': _c.V_TEMP_IGBTS_2_IIB_1,
        'InductorsTemperatureIIBMod1-Mon': _c.V_TEMP_INDUCTOR_IIB_1,
        'HeatSinkTemperatureIIBMod1-Mon': _c.V_TEMP_HEATSINK_IIB_1,
        'IGBTDriverVoltageIIBMod1-Mon': _c.V_V_DRIVER_IIB_1,
        'IGBT1DriverCurrentIIBMod1-Mon': _c.V_I_DRIVER_1_IIB_1,
        'IGBT2DriverCurrentIIBMod1-Mon': _c.V_I_DRIVER_2_IIB_1,
        'BoardTemperatureIIBMod1-Mon': _c.V_TEMP_BOARD_IIB_1,
        'RelativeHumidityIIBMod1-Mon': _c.V_RH_IIB_1,
        'IntlkIIBMod1-Mon': _c.V_IIB_INTERLOCKS_1,
        'AlarmsIIBMod1-Mon': _c.V_IIB_ALARMS_1,
        'VoltageInputIIBMod2-Mon': _c.V_V_INPUT_IIB_2,
        'CurrentInputIIBMod2-Mon': _c.V_I_INPUT_IIB_2,
        'CurrentOutputIIBMod2-Mon': _c.V_I_OUTPUT_IIB_2,
        'IGBT1TemperatureIIBMod2-Mon': _c.V_TEMP_IGBTS_1_IIB_2,
        'IGBT2TemperatureIIBMod2-Mon': _c.V_TEMP_IGBTS_2_IIB_2,
        'InductorsTemperatureIIBMod2-Mon': _c.V_TEMP_INDUCTOR_IIB_2,
        'HeatSinkTemperatureIIBMod2-Mon': _c.V_TEMP_HEATSINK_IIB_2,
        'IGBTDriverVoltageIIBMod2-Mon': _c.V_V_DRIVER_IIB_2,
        'IGBT1DriverCurrentIIBMod2-Mon': _c.V_I_DRIVER_1_IIB_2,
        'IGBT2DriverCurrentIIBMod2-Mon': _c.V_I_DRIVER_2_IIB_2,
        'BoardTemperatureIIBMod2-Mon': _c.V_TEMP_BOARD_IIB_2,
        'RelativeHumidityIIBMod2-Mon': _c.V_RH_IIB_2,
        'IntlkIIBMod2-Mon': _c.V_IIB_INTERLOCKS_2,
        'AlarmsIIBMod2-Mon': _c.V_IIB_ALARMS_2,
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
        'Arm1Current-Mon': _c.V_I_ARM_1,
        'Arm2Current-Mon': _c.V_I_ARM_2,
        'CapacitorBankVoltageMod1-Mon': _c.V_V_CAPBANK_1,
        'CapacitorBankVoltageMod2-Mon': _c.V_V_CAPBANK_2,
        'CapacitorBankVoltageMod3-Mon': _c.V_V_CAPBANK_3,
        'CapacitorBankVoltageMod4-Mon': _c.V_V_CAPBANK_4,
        'CapacitorBankVoltageMod5-Mon': _c.V_V_CAPBANK_5,
        'CapacitorBankVoltageMod6-Mon': _c.V_V_CAPBANK_6,
        'CapacitorBankVoltageMod7-Mon': _c.V_V_CAPBANK_7,
        'CapacitorBankVoltageMod8-Mon': _c.V_V_CAPBANK_8,
        'PWMDutyCycleMod1-Mon': _c.V_DUTY_CYCLE_1,
        'PWMDutyCycleMod2-Mon': _c.V_DUTY_CYCLE_2,
        'PWMDutyCycleMod3-Mon': _c.V_DUTY_CYCLE_3,
        'PWMDutyCycleMod4-Mon': _c.V_DUTY_CYCLE_4,
        'PWMDutyCycleMod5-Mon': _c.V_DUTY_CYCLE_5,
        'PWMDutyCycleMod6-Mon': _c.V_DUTY_CYCLE_6,
        'PWMDutyCycleMod7-Mon': _c.V_DUTY_CYCLE_7,
        'PWMDutyCycleMod8-Mon': _c.V_DUTY_CYCLE_8,
        'VoltageInputIIBModA-Mon': _c.V_V_INPUT_IIB_A,
        'CurrentInputIIBModA-Mon': _c.V_I_INPUT_IIB_A,
        'CurrentOutputIIBModA-Mon': _c.V_I_OUTPUT_IIB_A,
        'IGBT1TemperatureIIBModA-Mon': _c.V_TEMP_IGBTS_1_IIB_A,
        'IGBT2TemperatureIIBModA-Mon': _c.V_TEMP_IGBTS_2_IIB_A,
        'InductorTemperatureIIBModA-Mon': _c.V_TEMP_INDUCTOR_IIB_A,
        'HeatSinkTemperatureIIBModA-Mon': _c.V_TEMP_HEATSINK_IIB_A,
        'IGBTDriverVoltageIIBModA-Mon': _c.V_V_DRIVER_IIB_A,
        'IGBT1DriverCurrentIIBModA-Mon': _c.V_I_DRIVER_1_IIB_A,
        'IGBT2DriverCurrentIIBModA-Mon': _c.V_I_DRIVER_2_IIB_A,
        'BoardTemperatureIIBModA-Mon': _c.V_TEMP_BOARD_IIB_A,
        'RelativeHumidityIIBModA-Mon': _c.V_RH_IIB_A,
        'IntlkIIBModA-Mon': _c.V_IIB_INTERLOCKS_A,
        'AlarmsIIBModA-Mon': _c.V_IIB_ALARMS_A,
        'VoltageInputIIBModB-Mon': _c.V_V_INPUT_IIB_B,
        'CurrentInputIIBModB-Mon': _c.V_I_INPUT_IIB_B,
        'CurrentOutputIIBModB-Mon': _c.V_I_OUTPUT_IIB_B,
        'IGBT1TemperatureIIBModB-Mon': _c.V_TEMP_IGBTS_1_IIB_B,
        'IGBT2TemperatureIIBModB-Mon': _c.V_TEMP_IGBTS_2_IIB_B,
        'InductorTemperatureIIBModB-Mon': _c.V_TEMP_INDUCTOR_IIB_B,
        'HeatSinkTemperatureIIBModB-Mon': _c.V_TEMP_HEATSINK_IIB_B,
        'IGBTDriverVoltageIIBModB-Mon': _c.V_V_DRIVER_IIB_B,
        'IGBT1DriverCurrentIIBModB-Mon': _c.V_I_DRIVER_1_IIB_B,
        'IGBT2DriverCurrentIIBModB-Mon': _c.V_I_DRIVER_2_IIB_B,
        'BoardTemperatureIIBModB-Mon': _c.V_TEMP_BOARD_IIB_B,
        'RelativeHumidityIIBModB-Mon': _c.V_RH_IIB_B,
        'IntlkIIBModB-Mon': _c.V_IIB_INTERLOCKS_B,
        'AlarmsIIBModB-Mon': _c.V_IIB_ALARMS_B,
        }


class PSModelFAP(_PSModel):
    """FAP power supply model."""

    _n = 'FAP'
    _c = _const_psbsmp.ConstFAP
    _e = _etity_psbsmp.EntitiesFAP

    _bsmp_variables = {
        'Current-RB': _c.V_PS_SETPOINT,
        'CurrentRef-Mon': _c.V_PS_REFERENCE,
        'WfmSyncPulseCount-Mon': _c.V_COUNTER_SYNC_PULSE,
        'IntlkSoft-Mon': _c.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon': _c.V_PS_HARD_INTERLOCKS,
        'Current-Mon': _c.V_I_LOAD_MEAN,
        'Current1-Mon': _c.V_I_LOAD1,
        'Current2-Mon': _c.V_I_LOAD2,
        'DCLinkVoltage-Mon': _c.V_V_DCLINK,
        'IGBT1Current-Mon': _c.V_I_IGBT_1,
        'IGBT2Current-Mon': _c.V_I_IGBT_2,
        'IGBT1PWMDutyCycle-Mon': _c.V_DUTY_CYCLE_1,
        'IGBT2PWMDutyCycle-Mon': _c.V_DUTY_CYCLE_2,
        'PWMDutyDiff-Mon': _c.V_DUTY_DIFF,
        'VoltageInputIIB-Mon': _c.V_V_INPUT_IIB,
        'VoltageOutputIIB-Mon': _c.V_V_OUTPUT_IIB,
        'IGBT1CurrentIIB-Mon': _c.V_I_IGBT_1_IIB,
        'IGBT2CurrentIIB-Mon': _c.V_I_IGBT_2_IIB,
        'IGBT1TemperatureIIB-Mon': _c.V_TEMP_IGBT_1_IIB,
        'IGBT2TemperatureIIB-Mon': _c.V_TEMP_IGBT_2_IIB,
        'IGBTDriverVoltageIIB-Mon': _c.V_V_DRIVER_IIB,
        'IGBT1DriverCurrentIIB-Mon': _c.V_I_DRIVER_1_IIB,
        'IGBT2DriverCurrentIIB-Mon': _c.V_I_DRIVER_2_IIB,
        'InductorTemperatureIIB-Mon': _c.V_TEMP_INDUCTOR_IIB,
        'HeatSinkTemperatureIIB-Mon': _c.V_TEMP_HEATSINK_IIB,
        'LeakCurrentIIB-Mon': _c.V_I_LEAKAGE_IIB,
        'BoardTemperatureIIB-Mon': _c.V_TEMP_BOARD_IIB,
        'RelativeHumidityIIB-Mon': _c.V_RH_IIB,
        'IntlkIIB-Mon': _c.V_IIB_INTERLOCKS,
        'AlarmsIIB-Mon': _c.V_IIB_ALARMS,
        }


class PSModelFAP_4P(_PSModel):
    """FAP_4P power supply model."""

    _n = 'FAP_4P'
    _c = _const_psbsmp.ConstFAP_4P
    _e = _etity_psbsmp.EntitiesFAP_4P

    _bsmp_variables = {
        'Current-RB': _c.V_PS_SETPOINT,
        'CurrentRef-Mon': _c.V_PS_REFERENCE,
        'WfmSyncPulseCount-Mon': _c.V_COUNTER_SYNC_PULSE,
        'IntlkSoft-Mon': _c.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon': _c.V_PS_HARD_INTERLOCKS,
        'Current1-Mon': _c.V_I_LOAD1,
        'Current2-Mon': _c.V_I_LOAD2,
        'Current-Mon': _c.V_I_LOAD_MEAN,
        'LoadVoltage-Mon': _c.V_V_LOAD,
        'IGBT1CurrentMod1-Mon': _c.V_I_IGBT_1_1,
        'IGBT2CurrentMod1-Mon': _c.V_I_IGBT_2_1,
        'IGBT1CurrentMod2-Mon': _c.V_I_IGBT_1_2,
        'IGBT2CurrentMod2-Mon': _c.V_I_IGBT_2_2,
        'IGBT1CurrentMod3-Mon': _c.V_I_IGBT_1_3,
        'IGBT2CurrentMod3-Mon': _c.V_I_IGBT_2_3,
        'IGBT1CurrentMod4-Mon': _c.V_I_IGBT_1_4,
        'IGBT2CurrentMod4-Mon': _c.V_I_IGBT_2_4,
        'DCLinkVoltageMod1-Mon': _c.V_V_DCLINK_1,
        'DCLinkVoltageMod2-Mon': _c.V_V_DCLINK_2,
        'DCLinkVoltageMod3-Mon': _c.V_V_DCLINK_3,
        'DCLinkVoltageMod4-Mon': _c.V_V_DCLINK_4,
        'PWMDutyCycle-Mon': _c.V_DUTY_MEAN,
        'IGBT1PWMDutyCycleMod1-Mon': _c.V_DUTY_CYCLE_1_1,
        'IGBT2PWMDutyCycleMod1-Mon': _c.V_DUTY_CYCLE_2_1,
        'IGBT1PWMDutyCycleMod2-Mon': _c.V_DUTY_CYCLE_1_2,
        'IGBT2PWMDutyCycleMod2-Mon': _c.V_DUTY_CYCLE_2_2,
        'IGBT1PWMDutyCycleMod3-Mon': _c.V_DUTY_CYCLE_1_3,
        'IGBT2PWMDutyCycleMod3-Mon': _c.V_DUTY_CYCLE_2_3,
        'IGBT1PWMDutyCycleMod4-Mon': _c.V_DUTY_CYCLE_1_4,
        'IGBT2PWMDutyCycleMod4-Mon': _c.V_DUTY_CYCLE_2_4,
        'VoltageInputMod1-Mon': _c.V_V_INPUT_IIB_1,
        'VoltageOutputMod1-Mon': _c.V_V_OUTPUT_IIB_1,
        'IGBT1CurrentIIBMod1-Mon': _c.V_I_IGBT_1_IIB_1,
        'IGBT2CurrentIIBMod1-Mon': _c.V_I_IGBT_2_IIB_1,
        'IGBT1TemperatureIIBMod1-Mon': _c.V_TEMP_IGBT_1_IIB_1,
        'IGBT2TemperatureIIBMod1-Mon': _c.V_TEMP_IGBT_2_IIB_1,
        'IGBTDriverTemperatureIIBMod1-Mon': _c.V_V_DRIVER_IIB_1,
        'IGBT1DriverCurrentIIBMod1-Mon': _c.V_I_DRIVER_1_IIB_1,
        'IGBT2DriverCurrentIIBMod1-Mon': _c.V_I_DRIVER_2_IIB_1,
        'InductorTemperatureIIBMod1-Mon': _c.V_TEMP_INDUCTOR_IIB_1,
        'HeatSinkTemperatureIIBMod1-Mon': _c.V_TEMP_HEATSINK_IIB_1,
        'LeakageCurrentIIBMod1-Mon': _c.V_I_LEAKAGE_IIB_1,
        'TemperatureIIBMod1-Mon': _c.V_TEMP_BOARD_IIB_1,
        'RelativeHumidityIIBMod1-Mon': _c.V_RH_IIB_1,
        'IntlkIIBMod1-Mon': _c.V_IIB_INTERLOCKS_1,
        'AlarmsIIBMod1-Mon': _c.V_IIB_ALARMS_1,
        'VoltageInputMod2-Mon': _c.V_V_INPUT_IIB_2,
        'VoltageOutputMod2-Mon': _c.V_V_OUTPUT_IIB_2,
        'IGBT1CurrentIIBMod2-Mon': _c.V_I_IGBT_1_IIB_2,
        'IGBT2CurrentIIBMod2-Mon': _c.V_I_IGBT_2_IIB_2,
        'IGBT1TemperatureIIBMod2-Mon': _c.V_TEMP_IGBT_1_IIB_2,
        'IGBT2TemperatureIIBMod2-Mon': _c.V_TEMP_IGBT_2_IIB_2,
        'IGBTDriverTemperatureIIBMod2-Mon': _c.V_V_DRIVER_IIB_2,
        'IGBT1DriverCurrentIIBMod2-Mon': _c.V_I_DRIVER_1_IIB_2,
        'IGBT2DriverCurrentIIBMod2-Mon': _c.V_I_DRIVER_2_IIB_2,
        'InductorTemperatureIIBMod2-Mon': _c.V_TEMP_INDUCTOR_IIB_2,
        'HeatSinkTemperatureIIBMod2-Mon': _c.V_TEMP_HEATSINK_IIB_2,
        'LeakageCurrentIIBMod2-Mon': _c.V_I_LEAKAGE_IIB_2,
        'TemperatureIIBMod2-Mon': _c.V_TEMP_BOARD_IIB_2,
        'RelativeHumidityIIBMod2-Mon': _c.V_RH_IIB_2,
        'IntlkIIBMod2-Mon': _c.V_IIB_INTERLOCKS_2,
        'AlarmsIIBMod2-Mon': _c.V_IIB_ALARMS_2,
        'VoltageInputMod3-Mon': _c.V_V_INPUT_IIB_3,
        'VoltageOutputMod3-Mon': _c.V_V_OUTPUT_IIB_3,
        'IGBT1CurrentIIBMod3-Mon': _c.V_I_IGBT_1_IIB_3,
        'IGBT2CurrentIIBMod3-Mon': _c.V_I_IGBT_2_IIB_3,
        'IGBT1TemperatureIIBMod3-Mon': _c.V_TEMP_IGBT_1_IIB_3,
        'IGBT2TemperatureIIBMod3-Mon': _c.V_TEMP_IGBT_2_IIB_3,
        'IGBTDriverTemperatureIIBMod3-Mon': _c.V_V_DRIVER_IIB_3,
        'IGBT1DriverCurrentIIBMod3-Mon': _c.V_I_DRIVER_1_IIB_3,
        'IGBT2DriverCurrentIIBMod3-Mon': _c.V_I_DRIVER_2_IIB_3,
        'InductorTemperatureIIBMod3-Mon': _c.V_TEMP_INDUCTOR_IIB_3,
        'HeatSinkTemperatureIIBMod3-Mon': _c.V_TEMP_HEATSINK_IIB_3,
        'LeakageCurrentIIBMod3-Mon': _c.V_I_LEAKAGE_IIB_3,
        'TemperatureIIBMod3-Mon': _c.V_TEMP_BOARD_IIB_3,
        'RelativeHumidityIIBMod3-Mon': _c.V_RH_IIB_3,
        'IntlkIIBMod3-Mon': _c.V_IIB_INTERLOCKS_3,
        'AlarmsIIBMod3-Mon': _c.V_IIB_ALARMS_3,
        'VoltageInputMod4-Mon': _c.V_V_INPUT_IIB_4,
        'VoltageOutputMod4-Mon': _c.V_V_OUTPUT_IIB_4,
        'IGBT1CurrentIIBMod4-Mon': _c.V_I_IGBT_1_IIB_4,
        'IGBT2CurrentIIBMod4-Mon': _c.V_I_IGBT_2_IIB_4,
        'IGBT1TemperatureIIBMod4-Mon': _c.V_TEMP_IGBT_1_IIB_4,
        'IGBT2TemperatureIIBMod4-Mon': _c.V_TEMP_IGBT_2_IIB_4,
        'IGBTDriverTemperatureIIBMod4-Mon': _c.V_V_DRIVER_IIB_4,
        'IGBT1DriverCurrentIIBMod4-Mon': _c.V_I_DRIVER_1_IIB_4,
        'IGBT2DriverCurrentIIBMod4-Mon': _c.V_I_DRIVER_2_IIB_4,
        'InductorTemperatureIIBMod4-Mon': _c.V_TEMP_INDUCTOR_IIB_4,
        'HeatSinkTemperatureIIBMod4-Mon': _c.V_TEMP_HEATSINK_IIB_4,
        'LeakageCurrentIIBMod4-Mon': _c.V_I_LEAKAGE_IIB_4,
        'TemperatureIIBMod4-Mon': _c.V_TEMP_BOARD_IIB_4,
        'RelativeHumidityIIBMod4-Mon': _c.V_RH_IIB_4,
        'IntlkIIBMod4-Mon': _c.V_IIB_INTERLOCKS_4,
        'AlarmsIIBMod4-Mon': _c.V_IIB_ALARMS_4,
        }


class PSModelFAP_2P2S(_PSModel):
    """FAP_2P2S power supply model."""

    _n = 'FAP_2P2S'
    _c = _const_psbsmp.ConstFAP_2P2S
    _e = _etity_psbsmp.EntitiesFAP_2P2S

    _bsmp_variables = {
        'Current-RB':  _c.V_PS_SETPOINT,
        'CurrentRef-Mon':  _c.V_PS_REFERENCE,
        'WfmSyncPulseCount-Mon': _c.V_COUNTER_SYNC_PULSE,
        'IntlkSoft-Mon':  _c.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon':  _c.V_PS_HARD_INTERLOCKS,
        'Current-Mon':  _c.V_I_LOAD_MEAN,
        'Current1-Mon': _c.V_I_LOAD1,
        'Current2-Mon': _c.V_I_LOAD2,
        'Arm1Current-Mon': _c.V_I_ARM_1,
        'Arm2Current-Mon': _c.V_I_ARM_2,
        'IGBT1CurrentMod1-Mon': _c.V_I_IGBT_1_1,
        'IGBT2CurrentMod1-Mon': _c.V_I_IGBT_2_1,
        'IGBT1CurrentMod2-Mon': _c.V_I_IGBT_1_2,
        'IGBT2CurrentMod2-Mon': _c.V_I_IGBT_2_2,
        'IGBT1CurrentMod3-Mon': _c.V_I_IGBT_1_3,
        'IGBT2CurrentMod3-Mon': _c.V_I_IGBT_2_3,
        'IGBT1CurrentMod4-Mon': _c.V_I_IGBT_1_4,
        'IGBT2CurrentMod4-Mon': _c.V_I_IGBT_2_4,
        'CurrentMod1-Mon': _c.V_I_MOD_1,
        'CurrentMod2-Mon': _c.V_I_MOD_2,
        'CurrentMod3-Mon': _c.V_I_MOD_3,
        'CurrentMod4-Mon': _c.V_I_MOD_4,
        'DCLinkVoltageMod1-Mon': _c.V_V_DCLINK_1,
        'DCLinkVoltageMod2-Mon': _c.V_V_DCLINK_2,
        'DCLinkVoltageMod3-Mon': _c.V_V_DCLINK_3,
        'DCLinkVoltageMod4-Mon': _c.V_V_DCLINK_4,
        'PWMDutyCycle-Mon': _c.V_DUTY_MEAN,
        'PWMDutyCycleArmsDiff-Mon': _c.V_DUTY_ARMS_DIFF,
        'IGBT1PWMDutyCycleMod1-Mon': _c.V_DUTY_CYCLE_1_1,
        'IGBT2PWMDutyCycleMod1-Mon': _c.V_DUTY_CYCLE_2_1,
        'IGBT1PWMDutyCycleMod2-Mon': _c.V_DUTY_CYCLE_1_2,
        'IGBT2PWMDutyCycleMod2-Mon': _c.V_DUTY_CYCLE_2_2,
        'IGBT1PWMDutyCycleMod3-Mon': _c.V_DUTY_CYCLE_1_3,
        'IGBT2PWMDutyCycleMod3-Mon': _c.V_DUTY_CYCLE_2_3,
        'IGBT1PWMDutyCycleMod4-Mon': _c.V_DUTY_CYCLE_1_4,
        'IGBT2PWMDutyCycleMod4-Mon': _c.V_DUTY_CYCLE_2_4,
        'VoltageInputMod1-Mon': _c.V_V_INPUT_IIB_1,
        'VoltageOutputMod1-Mon': _c.V_V_OUTPUT_IIB_1,
        'IGBT1CurrentIIBMod1-Mon': _c.V_I_IGBT_1_IIB_1,
        'IGBT2CurrentIIBMod1-Mon': _c.V_I_IGBT_2_IIB_1,
        'IGBT1TemperatureIIBMod1-Mon': _c.V_TEMP_IGBT_1_IIB_1,
        'IGBT2TemperatureIIBMod1-Mon': _c.V_TEMP_IGBT_2_IIB_1,
        'IGBTDriverTemperatureIIBMod1-Mon': _c.V_V_DRIVER_IIB_1,
        'IGBT1DriverCurrentIIBMod1-Mon': _c.V_I_DRIVER_1_IIB_1,
        'IGBT2DriverCurrentIIBMod1-Mon': _c.V_I_DRIVER_2_IIB_1,
        'InductorTemperatureIIBMod1-Mon': _c.V_TEMP_INDUCTOR_IIB_1,
        'HeatSinkTemperatureIIBMod1-Mon': _c.V_TEMP_HEATSINK_IIB_1,
        'LeakageCurrentIIBMod1-Mon': _c.V_I_LEAKAGE_IIB_1,
        'TemperatureIIBMod1-Mon': _c.V_TEMP_BOARD_IIB_1,
        'RelativeHumidityIIBMod1-Mon': _c.V_RH_IIB_1,
        'IntlkIIBMod1-Mon': _c.V_IIB_INTERLOCKS_1,
        'AlarmsIIBMod1-Mon': _c.V_IIB_ALARMS_1,
        'VoltageInputMod2-Mon': _c.V_V_INPUT_IIB_2,
        'VoltageOutputMod2-Mon': _c.V_V_OUTPUT_IIB_2,
        'IGBT1CurrentIIBMod2-Mon': _c.V_I_IGBT_1_IIB_2,
        'IGBT2CurrentIIBMod2-Mon': _c.V_I_IGBT_2_IIB_2,
        'IGBT1TemperatureIIBMod2-Mon': _c.V_TEMP_IGBT_1_IIB_2,
        'IGBT2TemperatureIIBMod2-Mon': _c.V_TEMP_IGBT_2_IIB_2,
        'IGBTDriverTemperatureIIBMod2-Mon': _c.V_V_DRIVER_IIB_2,
        'IGBT1DriverCurrentIIBMod2-Mon': _c.V_I_DRIVER_1_IIB_2,
        'IGBT2DriverCurrentIIBMod2-Mon': _c.V_I_DRIVER_2_IIB_2,
        'InductorTemperatureIIBMod2-Mon': _c.V_TEMP_INDUCTOR_IIB_2,
        'HeatSinkTemperatureIIBMod2-Mon': _c.V_TEMP_HEATSINK_IIB_2,
        'LeakageCurrentIIBMod2-Mon': _c.V_I_LEAKAGE_IIB_2,
        'TemperatureIIBMod2-Mon': _c.V_TEMP_BOARD_IIB_2,
        'RelativeHumidityIIBMod2-Mon': _c.V_RH_IIB_2,
        'IntlkIIBMod2-Mon': _c.V_IIB_INTERLOCKS_2,
        'AlarmsIIBMod2-Mon': _c.V_IIB_ALARMS_2,
        'VoltageInputMod3-Mon': _c.V_V_INPUT_IIB_3,
        'VoltageOutputMod3-Mon': _c.V_V_OUTPUT_IIB_3,
        'IGBT1CurrentIIBMod3-Mon': _c.V_I_IGBT_1_IIB_3,
        'IGBT2CurrentIIBMod3-Mon': _c.V_I_IGBT_2_IIB_3,
        'IGBT1TemperatureIIBMod3-Mon': _c.V_TEMP_IGBT_1_IIB_3,
        'IGBT2TemperatureIIBMod3-Mon': _c.V_TEMP_IGBT_2_IIB_3,
        'IGBTDriverTemperatureIIBMod3-Mon': _c.V_V_DRIVER_IIB_3,
        'IGBT1DriverCurrentIIBMod3-Mon': _c.V_I_DRIVER_1_IIB_3,
        'IGBT2DriverCurrentIIBMod3-Mon': _c.V_I_DRIVER_2_IIB_3,
        'InductorTemperatureIIBMod3-Mon': _c.V_TEMP_INDUCTOR_IIB_3,
        'HeatSinkTemperatureIIBMod3-Mon': _c.V_TEMP_HEATSINK_IIB_3,
        'LeakageCurrentIIBMod3-Mon': _c.V_I_LEAKAGE_IIB_3,
        'TemperatureIIBMod3-Mon': _c.V_TEMP_BOARD_IIB_3,
        'RelativeHumidityIIBMod3-Mon': _c.V_RH_IIB_3,
        'IntlkIIBMod3-Mon': _c.V_IIB_INTERLOCKS_3,
        'AlarmsIIBMod3-Mon': _c.V_IIB_ALARMS_3,
        'VoltageInputMod4-Mon': _c.V_V_INPUT_IIB_4,
        'VoltageOutputMod4-Mon': _c.V_V_OUTPUT_IIB_4,
        'IGBT1CurrentIIBMod4-Mon': _c.V_I_IGBT_1_IIB_4,
        'IGBT2CurrentIIBMod4-Mon': _c.V_I_IGBT_2_IIB_4,
        'IGBT1TemperatureIIBMod4-Mon': _c.V_TEMP_IGBT_1_IIB_4,
        'IGBT2TemperatureIIBMod4-Mon': _c.V_TEMP_IGBT_2_IIB_4,
        'IGBTDriverTemperatureIIBMod4-Mon': _c.V_V_DRIVER_IIB_4,
        'IGBT1DriverCurrentIIBMod4-Mon': _c.V_I_DRIVER_1_IIB_4,
        'IGBT2DriverCurrentIIBMod4-Mon': _c.V_I_DRIVER_2_IIB_4,
        'InductorTemperatureIIBMod4-Mon': _c.V_TEMP_INDUCTOR_IIB_4,
        'HeatSinkTemperatureIIBMod4-Mon': _c.V_TEMP_HEATSINK_IIB_4,
        'LeakageCurrentIIBMod4-Mon': _c.V_I_LEAKAGE_IIB_4,
        'TemperatureIIBMod4-Mon': _c.V_TEMP_BOARD_IIB_4,
        'RelativeHumidityIIBMod4-Mon': _c.V_RH_IIB_4,
        'IntlkIIBMod4-Mon': _c.V_IIB_INTERLOCKS_4,
        'AlarmsIIBMod4-Mon': _c.V_IIB_ALARMS_4,
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

    def writer(self, device_ids, epics_field, pru_controller, setpoints):
        """Return writer."""
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
        'CapacitorBankVoltage-RB': _c.V_PS_SETPOINT,
        'CapacitorBankVoltageRef-Mon': _c.V_PS_REFERENCE,
        'IntlkSoft-Mon': _c.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon': _c.V_PS_HARD_INTERLOCKS,
        'CapacitorBankVoltage-Mon': _c.V_V_CAPBANK,
        'RectifierCurrent-Mon': _c.V_I_OUT_RECTIFIER,
        'PWMDutyCycle-Mon': _c.V_DUTY_CYCLE,
        'CurrentInputIIBModIS-Mon': _c.V_I_INPUT_IS_IIB,
        'VoltageInputIIBModIS-Mon': _c.V_V_INPUT_IS_IIB,
        'IGBTTemperatureIIBModIS-Mon': _c.V_TEMP_IGBT_IS_IIB,
        'IGBTDriverVoltageIIBModIS-Mon': _c.V_V_DRIVER_IS_IIB,
        'IGBTDriverCurrentIIBModIS-Mon': _c.V_I_DRIVER_IS_IIB,
        'InductorTemperatureIIBModIS-Mon': _c.V_TEMP_INDUCTOR_IS_IIB,
        'HeatSinkTemperatureIIBModIS-Mon': _c.V_TEMP_HEATSINK_IS_IIB,
        'BoardTemperatureIIBModIS-Mon': _c.V_TEMP_BOARD_IS_IIB,
        'RelativeHumidityIIBModIS-Mon': _c.V_RH_IS_IIB,
        'IntlkIIBModIS-Mon': _c.V_IIB_INTERLOCKS_IS,
        'AlarmsIIBModIS-Mon': _c.V_IIB_ALARMS_IS,
        'VoltageOutputIIBModCmd-Mon': _c.V_V_OUTPUT_CMD_IIB,
        'CapacitorBankVoltageIIBModCmd-Mon': _c.V_V_CAPBANK_CMD_IIB,
        'RectInductorTempIIBModCmd-Mon': _c.V_TEMP_RECT_INDUCTOR_CMD_IIB,
        'RectHeatSinkTempIIBModCmd-Mon': _c.V_TEMP_RECT_HEATSINK_CMD_IIB,
        'ExtBoardsVoltageIIBModCmd-Mon': _c.V_V_EXT_BOARDS_CMD_IIB,
        'AuxBoardCurrentIIBModCmd-Mon': _c.V_I_AUX_BOARD_CMD_IIB,
        'IDBBoardCurrentIIBModCmd-Mon': _c.V_I_IDB_BOARD_CMD_IIB,
        'LeakCurrentIIBModCmd-Mon': _c.V_I_LEAKAGE_CMD_IIB,
        'BoardTemperatureIIBModCmd-Mon': _c.V_TEMP_BOARD_CMD_IIB,
        'RelativeHumidityIIBModCmd-Mon': _c.V_RH_CMD_IIB,
        'IntlkIIBModCmd-Mon': _c.V_IIB_INTERLOCKS_CMD,
        'AlarmsIIBModCmd-Mon': _c.V_IIB_ALARMS_CMD,
        }

    def writer(self, device_ids, epics_field, pru_controller, setpoints):
        """Return writer."""
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
        'CapacitorBankVoltage-RB': _c.V_PS_SETPOINT,
        'CapacitorBankVoltageRef-Mon': _c.V_PS_REFERENCE,
        'IntlkSoft-Mon': _c.V_PS_SOFT_INTERLOCKS,
        'IntlkHard-Mon': _c.V_PS_HARD_INTERLOCKS,
        'CapacitorBankVoltage-Mon': _c.V_V_CAPACITOR_BANK,
        'RectifierCurrent-Mon': _c.V_I_OUT_RECTIFIER,
        'PWMDutyCycle-Mon': _c.V_DUTY_CYCLE,
        'CurrentInputIIBModIS-Mon': _c.V_I_INPUT_IS_IIB,
        'VoltageInputIIBModIS-Mon': _c.V_V_INPUT_IS_IIB,
        'IGBTTemperatureIIBModIS-Mon': _c.V_TEMP_IGBT_IS_IIB,
        'IGBTDriverVoltageIIBModIS-Mon': _c.V_V_DRIVER_IS_IIB,
        'IGBTDriverCurrentIIBModIS-Mon': _c.V_I_DRIVER_IS_IIB,
        'InductorTemperatureIIBModIS-Mon': _c.V_TEMP_INDUCTOR_IS_IIB,
        'HeatSinkTemperatureIIBModIS-Mon': _c.V_TEMP_HEATSINK_IS_IIB,
        'BoardTemperatureIIBModIS-Mon': _c.V_TEMP_BOARD_IS_IIB,
        'RelativeHumidityIIBModIS-Mon': _c.V_RH_IS_IIB,
        'IntlkIIBModIS-Mon': _c.V_IIB_INTERLOCKS_IS,
        'AlarmsIIBModIS-Mon': _c.V_IIB_ALARMS_IS,
        'VoltageOutputIIBModCmd-Mon': _c.V_V_OUTPUT_CMD_IIB,
        'CapacitorBankVoltageIIBModCmd-Mon': _c.V_V_CAPBANK_CMD_IIB,
        'InductorTemperatureIIBModCmd-Mon': _c.V_TEMP_RECT_INDUCTOR_CMD_IIB,
        'HeatSinkTemperatureIIBModCmd-Mon': _c.V_TEMP_RECT_HEATSINK_CMD_IIB,
        'ExtBoardsVoltageIIBModCmd-Mon': _c.V_V_EXT_BOARDS_CMD_IIB,
        'AuxBoardCurrentIIBModCmd-Mon': _c.V_I_AUX_BOARD_CMD_IIB,
        'IDBBoardCurrentIIBModCmd-Mon': _c.V_I_IDB_BOARD_CMD_IIB,
        'LeakCurrentIIBModCmd-Mon': _c.V_I_LEAKAGE_CMD_IIB,
        'BoardTemperatureIIBModCmd-Mon': _c.V_TEMP_BOARD_CMD_IIB,
        'RelativeHumidityIIBModCmd-Mon': _c.V_RH_CMD_IIB,
        'IntlkIIBModCmd-Mon': _c.V_IIB_INTERLOCKS_CMD,
        'AlarmsIIBModCmd-Mon': _c.V_IIB_ALARMS_CMD,
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

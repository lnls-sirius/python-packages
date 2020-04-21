"""Power Supply BSMP Constants.

Module for definitions of BSMP entities of power supply devices.

Documentation:

https://wiki-sirius.lnls.br/mediawiki/index.php/Machine:Power_Supplies
"""

from ...bsmp import constants as _const_bsmp

# version of the BSMP implementation of power supplies that is compatible
# with the current implemenation of this module.

__version__ = 'V0.36w2019-10-07V0.36w2019-10-07'


# --- Const DCDC ---


class ConstPSBSMP:
    """Namespace for organizing power supply BSMP constants."""

    # --- implemented protocol version ---
    # version = __bsmp_version__

    # --- group of BSMP variables
    G_ALL = _const_bsmp.ID_STD_GROUP_ALL
    G_READONLY = _const_bsmp.ID_STD_GROUP_READONLY
    G_WRITE = _const_bsmp.ID_STD_GROUP_WRITE
    G_ALLRELEVANT = 3
    G_SCAN = 4
    G_SOFB = 5

    # --- types ---
    T_STATUS = 0
    T_STATE = 1
    T_REMOTE = 2
    T_MODEL = 3
    T_FLOAT = 4
    T_UINT8 = 5
    T_UINT16 = 6
    T_UINT32 = 7
    T_CHAR128 = 8
    T_FLOAT4 = 9
    T_PARAM = 10
    T_FLOAT12 = 11
    T_DSPCLASS = 12
    T_NONE = 13
    T_ENUM = 14

    # --- enums ---
    E_STATE_OFF = 0
    E_STATE_INTERLOCK = 1
    E_STATE_INITIALIZING = 2
    E_STATE_SLOWREF = 3
    E_STATE_SLOWREFSYNC = 4
    E_STATE_CYCLE = 5
    E_STATE_RMPWFM = 6
    E_STATE_MIGWFM = 7
    E_STATE_FASTREF = 8

    E_REMOTE_REMOTE = 0
    E_REMOTE_LOCAL = 1
    E_REMOTE_PCHOST = 2

    E_SIGGENTYPE_SINE = 0
    E_SIGGENTYPE_DAMPEDSINE = 1
    E_SIGGENTYPE_TRAPEZOIDAL = 2

    # --- functions ---
    F_TURN_ON = 0
    F_TURN_OFF = 1
    F_OPEN_LOOP = 2
    F_CLOSE_LOOP = 3
    F_SELECT_OP_MODE = 4
    F_SELECT_PS_MODEL = 5
    F_RESET_INTERLOCKS = 6
    F_REMOTE_INTERFACE = 7
    F_SET_SERIAL_ADDRESS = 8
    F_SET_SERIAL_TERMINATION = 9
    F_UNLOCK_UDC = 10
    F_LOCK_UDC = 11
    F_CFG_BUF_SAMPLES = 12
    F_ENABLE_BUF_SAMPLES = 13
    F_DISABLE_BUF_SAMPLES = 14
    F_SYNC_PULSE = 15
    F_SET_SLOWREF = 16
    F_SET_SLOWREF_FBP = 17
    F_RESET_COUNTERS = 18
    F_SCALE_WFMREF = 19
    F_SELECT_WFMREF = 20
    F_GET_WFMREF_SIZE = 21
    F_RESET_WFMREF = 22
    F_CFG_SIGGEN = 23
    F_SET_SIGGEN = 24
    F_ENABLE_SIGGEN = 25
    F_DISABLE_SIGGEN = 26
    F_SET_SLOWREF_READBACK = 27
    F_SET_SLOWREF_FBP_READBACK = 28
    F_SET_PARAM = 29
    F_GET_PARAM = 30
    F_SAVE_PARAM_EEPROM = 31
    F_LOAD_PARAM_EEPROM = 32
    F_SAVE_PARAM_BANK = 33
    F_LOAD_PARAM_BANK = 34
    F_SET_DSP_COEFFS = 35
    F_GET_DSP_COEFF = 36
    F_SAVE_DSP_COEFFS_EEPROM = 37
    F_LOAD_DSP_COEFFS_EEPROM = 38
    F_SAVE_DSP_MODULES_EEPROM = 39
    F_LOAD_DSP_MODULES_EEPROM = 40
    F_RESET_UDC = 41

    # --- common variables ---
    V_PS_STATUS = 0
    V_PS_SETPOINT = 1  # corresponds to IOC Current-RB
    V_PS_REFERENCE = 2  # corresponds to IOC CurrentRef-Mon
    V_FIRMWARE_VERSION = 3
    V_COUNTER_SET_SLOWREF = 4
    V_COUNTER_SYNC_PULSE = 5
    V_SIGGEN_ENABLE = 6
    V_SIGGEN_TYPE = 7
    V_SIGGEN_NUM_CYCLES = 8
    V_SIGGEN_N = 9
    V_SIGGEN_FREQ = 10
    V_SIGGEN_AMPLITUDE = 11
    V_SIGGEN_OFFSET = 12
    V_SIGGEN_AUX_PARAM = 13
    V_WFMREF_SELECTED = 14
    V_WFMREF_SYNC_MODE = 15
    V_WFMREF_GAIN = 16
    V_WFMREF_OFFSET = 17
    V_WFMREF0_START = 18
    V_WFMREF0_END = 19
    V_WFMREF0_IDX = 20
    V_WFMREF1_START = 21
    V_WFMREF1_END = 22
    V_WFMREF1_IDX = 23

    # --- undefined variables
    V_UNDEF24 = 24

    # --- power supply parameters ---
    # ----- class PS -----
    P_PS_NAME = 0
    P_PS_MODEL = 1
    P_PS_NR_PSMODELS = 2
    # ----- class Communication -----
    P_COMM_CMD_INTERFACE = 3
    P_COMM_RS485_BAUDRATE = 4
    P_COMM_RS485_ADDRESS = 5
    P_COMM_RS485_TERMINATOR_RESISTOR = 6
    P_COMM_UDC_NETWORK_ADDRESS = 7
    P_COMM_ETHERNET_IP = 8
    P_COMM_ETHERNET_SUBNET_MASK = 9
    P_COMM_BUZZER_VOLUME = 10
    # ----- class Control -----
    P_CTRL_FREQ_CONTROL_ISR = 11
    P_CTRL_FREQ_TIME_SLICER = 12
    P_CTRL_MAX_REF = 13
    P_CTRL_MIN_REF = 14
    P_CTRL_MAX_REF_OPEN_LOOP = 15
    P_CTRL_MIN_REF_OPEN_LOOP = 16
    P_CTRL_SLEW_RATE_SLOWREF = 17
    P_CTRL_SLEW_RATE_SIGGEN_AMP = 18
    P_CTRL_SLEW_RATE_SIGGEN_OFFSET = 19
    P_CTRL_SLEW_RATE_WFMREF = 20
    # ----- class PWM -----
    P_PWM_FREQ = 21
    P_PWM_DEAD_TIME = 22
    P_PWM_MAX_DUTY = 23
    P_PWM_MIN_DUTY = 24
    P_PWM_MAX_DUTY_OPEN_LOOP = 25
    P_PWM_MIN_DUTY_OPEN_LOOP = 26
    P_PWM_LIM_DUTY_SHARE = 27
    # ----- class HRADC -----
    P_HRADC_NR_BOARDS = 28
    P_HRADC_SPI_CLK = 29
    P_HRADC_FREQ_SAMPLING = 30
    P_HRADC_ENABLE_HEATER = 31
    P_HRADC_ENABLE_RAILS_MON = 32
    P_HRADC_TRANSDUCER_OUTPUT = 33
    P_HRADC_TRANSDUCER_GAIN = 34
    P_HRADC_TRANSDUCER_OFFSET = 35
    # ----- class SigGen -----
    P_SIGGEN_TYPE = 36
    P_SIGGEN_NUM_CYCLES = 37
    P_SIGGEN_FREQ = 38
    P_SIGGEN_AMPLITUDE = 39
    P_SIGGEN_OFFSET = 40
    P_SIGGEN_AUX_PARAM = 41
    # ----- class WfmRef -----
    P_WFMREF_ID = 42
    P_WFMREF_SYNC_MODE = 43
    P_WFMREF_GAIN = 44
    P_WFMREF_OFFSET = 45
    # ----- class Analog Variables -----
    P_ANALOG_MAX = 46
    P_ANALOG_MIN = 47
    # ----- class Debounding manager -----
    P_HARD_INTLK_DEBOUNCE_TIME = 48
    P_HARD_INTLK_RESET_TIME = 49
    P_SOFT_INTLK_DEBOUNCE_TIME = 50
    P_SOFT_INTLK_RESET_TIME = 51


class ConstFBP(ConstPSBSMP):
    """Namespace for organizing power supply FBP BSMP constants."""

    # --- FSB variables ---
    V_PS_SOFT_INTERLOCKS = 25  # BSMP doc says ID numb. should be continous!
    V_PS_HARD_INTERLOCKS = 26
    V_I_LOAD = 27  # corresponds to IOC Current-Mon
    V_V_LOAD = 28
    V_V_DCLINK = 29
    V_TEMP_SWITCHES = 30
    V_DUTY_CYCLE = 31  # (float)
    # --- FBP mirror variables ----
    V_PS_STATUS1 = 40
    V_PS_STATUS2 = 41
    V_PS_STATUS3 = 42
    V_PS_STATUS4 = 43
    V_PS_SETPOINT1 = 44
    V_PS_SETPOINT2 = 45
    V_PS_SETPOINT3 = 46
    V_PS_SETPOINT4 = 47
    V_PS_REFERENCE1 = 48
    V_PS_REFERENCE2 = 49
    V_PS_REFERENCE3 = 50
    V_PS_REFERENCE4 = 51
    V_PS_SOFT_INTERLOCK1 = 52
    V_PS_SOFT_INTERLOCK2 = 53
    V_PS_SOFT_INTERLOCK3 = 54
    V_PS_SOFT_INTERLOCK4 = 55
    V_PS_HARD_INTERLOCK1 = 56
    V_PS_HARD_INTERLOCK2 = 57
    V_PS_HARD_INTERLOCK3 = 58
    V_PS_HARD_INTERLOCK4 = 59
    V_I_LOAD1 = 60
    V_I_LOAD2 = 61
    V_I_LOAD3 = 62
    V_I_LOAD4 = 63


class ConstFAC_DCDC(ConstPSBSMP):
    """Namespace for organizing power supply FAC_DCDC BSMP constants."""

    # --- FAC_DCDC variables ---
    V_PS_SOFT_INTERLOCKS = 25
    V_PS_HARD_INTERLOCKS = 26
    V_I_LOAD_MEAN = 27
    V_I_LOAD1 = 28
    V_I_LOAD2 = 29
    V_V_LOAD = 30
    V_V_CAPBANK = 31
    V_TEMP_INDUCTORS = 32
    V_TEMP_IGBTS = 33
    V_DUTY_CYCLE = 34
    V_I_INPUT_IIB = 35
    V_I_OUTPUT_IIB = 36
    V_V_INPUT_IIB = 37
    V_TEMP_IGBTS_1_IIB = 38
    V_TEMP_IGBTS_2_IIB = 39
    V_TEMP_INDUCTOR_IIB = 40
    V_TEMP_HEATSINK_IIB = 41
    V_DRIVER_ERROR_1_IIB = 42
    V_DRIVER_ERROR_2_IIB = 43
    V_IIB_INTERLOCKS = 44


class ConstFAC_2P4S_DCDC(ConstPSBSMP):
    """Namespace for organizing power supply FAC_2P4S_DCDC BSMP constants."""

    # --- FAC_2P4S_DCDC variables ---
    V_PS_SOFT_INTERLOCKS = 25
    V_PS_HARD_INTERLOCKS = 26
    V_I_LOAD_MEAN = 27
    V_I_LOAD1 = 28
    V_I_LOAD2 = 29
    V_I_ARM_1 = 30
    V_I_ARM_2 = 31
    V_V_LOAD = 32
    V_V_CAPBANK_1 = 33
    V_V_CAPBANK_2 = 34
    V_V_CAPBANK_3 = 35
    V_V_CAPBANK_4 = 36
    V_V_CAPBANK_5 = 37
    V_V_CAPBANK_6 = 38
    V_V_CAPBANK_7 = 39
    V_V_CAPBANK_8 = 40
    V_V_OUT_1 = 41
    V_V_OUT_2 = 42
    V_V_OUT_3 = 43
    V_V_OUT_4 = 44
    V_V_OUT_5 = 45
    V_V_OUT_6 = 46
    V_V_OUT_7 = 47
    V_V_OUT_8 = 48
    V_DUTY_CYCLE_1 = 49
    V_DUTY_CYCLE_2 = 50
    V_DUTY_CYCLE_3 = 51
    V_DUTY_CYCLE_4 = 52
    V_DUTY_CYCLE_5 = 53
    V_DUTY_CYCLE_6 = 54
    V_DUTY_CYCLE_7 = 55
    V_DUTY_CYCLE_8 = 56
    V_I_INPUT_IIB_1 = 57
    V_I_OUTPUT_IIB_1 = 58
    V_V_INPUT_IIB_1 = 59
    V_TEMP_INDUCTOR_IIB_1 = 60
    V_TEMP_HEATSINK_IIB_1 = 61
    V_DRIVER_ERROR_1_IIB_1 = 62
    V_DRIVER_ERROR_2_IIB_1 = 63
    V_I_INPUT_IIB_2 = 64
    V_I_OUTPUT_IIB_2 = 65
    V_V_INPUT_IIB_2 = 66
    V_TEMP_INDUCTOR_IIB_2 = 67
    V_TEMP_HEATSINK_IIB_2 = 68
    V_DRIVER_ERROR_1_IIB_2 = 69
    V_DRIVER_ERROR_2_IIB_2 = 70
    V_I_INPUT_IIB_3 = 71
    V_I_OUTPUT_IIB_3 = 72
    V_V_INPUT_IIB_3 = 73
    V_TEMP_INDUCTOR_IIB_3 = 74
    V_TEMP_HEATSINK_IIB_3 = 75
    V_DRIVER_ERROR_1_IIB_3 = 76
    V_DRIVER_ERROR_2_IIB_3 = 77
    V_I_INPUT_IIB_4 = 78
    V_I_OUTPUT_IIB_4 = 79
    V_V_INPUT_IIB_4 = 80
    V_TEMP_INDUCTOR_IIB_4 = 81
    V_TEMP_HEATSINK_IIB_4 = 82
    V_DRIVER_ERROR_1_IIB_4 = 83
    V_DRIVER_ERROR_2_IIB_4 = 84
    V_I_INPUT_IIB_5 = 85
    V_I_OUTPUT_IIB_5 = 86
    V_V_INPUT_IIB_5 = 87
    V_TEMP_INDUCTOR_IIB_5 = 88
    V_TEMP_HEATSINK_IIB_5 = 89
    V_DRIVER_ERROR_1_IIB_5 = 90
    V_DRIVER_ERROR_2_IIB_5 = 91
    V_I_INPUT_IIB_6 = 92
    V_I_OUTPUT_IIB_6 = 93
    V_V_INPUT_IIB_6 = 94
    V_TEMP_INDUCTOR_IIB_6 = 95
    V_TEMP_HEATSINK_IIB_6 = 96
    V_DRIVER_ERROR_1_IIB_6 = 97
    V_DRIVER_ERROR_2_IIB_6 = 98
    V_I_INPUT_IIB_7 = 99
    V_I_OUTPUT_IIB_7 = 100
    V_V_INPUT_IIB_7 = 101
    V_TEMP_INDUCTOR_IIB_7 = 102
    V_TEMP_HEATSINK_IIB_7 = 103
    V_DRIVER_ERROR_1_IIB_7 = 104
    V_DRIVER_ERROR_2_IIB_7 = 105
    V_I_INPUT_IIB_8 = 106
    V_I_OUTPUT_IIB_8 = 107
    V_V_INPUT_IIB_8 = 108
    V_TEMP_INDUCTOR_IIB_8 = 109
    V_TEMP_HEATSINK_IIB_8 = 110
    V_DRIVER_ERROR_1_IIB_8 = 111
    V_DRIVER_ERROR_2_IIB_8 = 112
    V_IIB_INTERLOCKS_1 = 113
    V_IIB_INTERLOCKS_2 = 114
    V_IIB_INTERLOCKS_3 = 115
    V_IIB_INTERLOCKS_4 = 116
    V_IIB_INTERLOCKS_5 = 117
    V_IIB_INTERLOCKS_6 = 118
    V_IIB_INTERLOCKS_7 = 119
    V_IIB_INTERLOCKS_8 = 120


class ConstFAC_2S_DCDC(ConstPSBSMP):
    """Namespace for organizing power supply FAC_2S_DCDC BSMP constants."""

    # --- FAC_2S_DCDC variables ---
    V_PS_SOFT_INTERLOCKS = 25
    V_PS_HARD_INTERLOCKS = 26
    V_I_LOAD_MEAN = 27
    V_I_LOAD1 = 28
    V_I_LOAD2 = 29
    V_V_LOAD = 30
    V_V_OUT_1 = 31
    V_V_OUT_2 = 32
    V_V_CAPBANK_1 = 33
    V_V_CAPBANK_2 = 34
    V_DUTY_CYCLE_1 = 35
    V_DUTY_CYCLE_2 = 36
    V_DUTY_DIFF = 37
    V_I_INPUT_IIB_1 = 38
    V_I_OUTPUT_IIB_1 = 39
    V_V_INPUT_IIB_1 = 40
    V_TEMP_INDUCTOR_IIB_1 = 41
    V_TEMP_HEATSINK_IIB_1 = 42
    V_DRIVER_ERROR_1_IIB_1 = 43
    V_DRIVER_ERROR_2_IIB_1 = 44
    V_I_INPUT_IIB_2 = 45
    V_I_OUTPUT_IIB_2 = 46
    V_V_INPUT_IIB_2 = 47
    V_TEMP_INDUCTOR_IIB_2 = 48
    V_TEMP_HEATSINK_IIB_2 = 49
    V_DRIVER_ERROR_1_IIB_2 = 50
    V_DRIVER_ERROR_2_IIB_2 = 51
    V_IIB_INTERLOCKS_1 = 52
    V_IIB_INTERLOCKS_2 = 53


class ConstFAP(ConstPSBSMP):
    """Namespace for organizing power supply FAP BSMP constants."""

    # --- FAP variables ---
    V_PS_SOFT_INTERLOCKS = 25
    V_PS_HARD_INTERLOCKS = 26
    V_I_LOAD_MEAN = 27  # corresponds to IOC Current-Mon
    V_I_LOAD1 = 28  # corresponds to IOC Current1-Mon
    V_I_LOAD2 = 29  # corresponds to IOC Current2-Mon
    V_V_DCLINK = 30
    V_I_IGBT_1 = 31
    V_I_IGBT_2 = 32
    V_DUTY_CYCLE_1 = 33
    V_DUTY_CYCLE_2 = 34
    V_DUTY_DIFF = 35
    V_V_INPUT_IIB = 36
    V_V_OUTPUT_IIB = 37
    V_I_IGBT_1_IIB = 38
    V_I_IGBT_2_IIB = 39
    V_TEMP_IGBT_1_IIB = 40
    V_TEMP_IGBT_2_IIB = 41
    V_V_DRIVER_IIB = 42
    V_I_DRIVER_1_IIB = 43
    V_I_DRIVER_2_IIB = 44
    V_TEMP_INDUCTOR_IIB = 45
    V_TEMP_HEATSINK_IIB = 46
    V_I_LEAKAGE_IIB = 47
    V_IIB_INTERLOCKS = 48


class ConstFAP_4P(ConstFAP):
    """Namespace for organizing power supply FAP_4P BSMP constants."""
    # --- FAP variables ---
    V_PS_SOFT_INTERLOCKS = 25
    V_PS_HARD_INTERLOCKS = 26
    V_I_LOAD1 = 27  # corresponds to IOC Current1-Mon
    V_I_LOAD2 = 28  # corresponds to IOC Current2-Mon
    V_I_LOAD_MEAN = 29  # corresponds to IOC Current-Mon
    V_V_LOAD = 30
    V_I_IGBT_1_1 = 31
    V_I_IGBT_2_1 = 32
    V_I_IGBT_1_2 = 33
    V_I_IGBT_2_2 = 34
    V_I_IGBT_1_3 = 35
    V_I_IGBT_2_3 = 36
    V_I_IGBT_1_4 = 37
    V_I_IGBT_2_4 = 38
    V_V_DCLINK_1 = 39
    V_V_DCLINK_2 = 40
    V_V_DCLINK_3 = 41
    V_V_DCLINK_4 = 42
    V_DUTY_MEAN = 43
    V_DUTY_CYCLE_1_1 = 44
    V_DUTY_CYCLE_2_1 = 45
    V_DUTY_CYCLE_1_2 = 46
    V_DUTY_CYCLE_2_2 = 47
    V_DUTY_CYCLE_1_3 = 48
    V_DUTY_CYCLE_2_3 = 49
    V_DUTY_CYCLE_1_4 = 50
    V_DUTY_CYCLE_2_4 = 51
    V_V_INPUT_IIB_1 = 52
    V_V_OUTPUT_IIB_1 = 53
    V_I_IGBT_1_IIB_1 = 54
    V_I_IGBT_2_IIB_1 = 55
    V_TEMP_IGBT_1_IIB_1 = 56
    V_TEMP_IGBT_2_IIB_1 = 57
    V_V_DRIVER_IIB_1 = 58
    V_I_DRIVER_1_IIB_1 = 59
    V_I_DRIVER_2_IIB_1 = 60
    V_TEMP_INDUCTOR_IIB_1 = 61
    V_TEMP_HEATSINK_IIB_1 = 62
    V_I_LEAKAGE_IIB_1 = 63
    V_V_INPUT_IIB_2 = 64
    V_V_OUTPUT_IIB_2 = 65
    V_I_IGBT_1_IIB_2 = 66
    V_I_IGBT_2_IIB_2 = 67
    V_TEMP_IGBT_1_IIB_2 = 68
    V_TEMP_IGBT_2_IIB_2 = 69
    V_V_DRIVER_IIB_2 = 70
    V_I_DRIVER_1_IIB_2 = 71
    V_I_DRIVER_2_IIB_2 = 72
    V_TEMP_INDUCTOR_IIB_2 = 73
    V_TEMP_HEATSINK_IIB_2 = 74
    V_I_LEAKAGE_IIB_2 = 75
    V_V_INPUT_IIB_3 = 76
    V_V_OUTPUT_IIB_3 = 77
    V_I_IGBT_1_IIB_3 = 78
    V_I_IGBT_2_IIB_3 = 79
    V_TEMP_IGBT_1_IIB_3 = 80
    V_TEMP_IGBT_2_IIB_3 = 81
    V_V_DRIVER_IIB_3 = 82
    V_I_DRIVER_1_IIB_3 = 83
    V_I_DRIVER_2_IIB_3 = 84
    V_TEMP_INDUCTOR_IIB_3 = 85
    V_TEMP_HEATSINK_IIB_3 = 86
    V_I_LEAKAGE_IIB_3 = 87
    V_V_INPUT_IIB_4 = 88
    V_V_OUTPUT_IIB_4 = 89
    V_I_IGBT_1_IIB_4 = 90
    V_I_IGBT_2_IIB_4 = 91
    V_TEMP_IGBT_1_IIB_4 = 92
    V_TEMP_IGBT_2_IIB_4 = 93
    V_V_DRIVER_IIB_4 = 94
    V_I_DRIVER_1_IIB_4 = 95
    V_I_DRIVER_2_IIB_4 = 96
    V_TEMP_INDUCTOR_IIB_4 = 97
    V_TEMP_HEATSINK_IIB_4 = 98
    V_I_LEAKAGE_IIB_4 = 99
    V_IIB_INTERLOCKS_1 = 100
    V_IIB_INTERLOCKS_2 = 101
    V_IIB_INTERLOCKS_3 = 102
    V_IIB_INTERLOCKS_4 = 103
    V_I_MOD_1 = 104
    V_I_MOD_2 = 105
    V_I_MOD_3 = 106
    V_I_MOD_4 = 107


class ConstFAP_2P2S(ConstPSBSMP):
    """Namespace for organizing power supply FAP_2P2S BSMP constants."""

    # --- FAP_2P2S variables ---
    V_PS_SOFT_INTERLOCKS = 25
    V_PS_HARD_INTERLOCKS = 26
    V_I_LOAD_MEAN = 27
    V_I_LOAD1 = 28
    V_I_LOAD2 = 29
    V_I_ARM_1 = 30
    V_I_ARM_2 = 31
    V_I_IGBT_1_1 = 32
    V_I_IGBT_2_1 = 33
    V_I_IGBT_1_2 = 34
    V_I_IGBT_2_2 = 35
    V_I_IGBT_1_3 = 36
    V_I_IGBT_2_3 = 37
    V_I_IGBT_1_4 = 38
    V_I_IGBT_2_4 = 39
    V_V_DCLINK_1 = 40
    V_V_DCLINK_2 = 41
    V_V_DCLINK_3 = 42
    V_V_DCLINK_4 = 43
    V_DUTY_MEAN = 44
    V_DUTY_ARMS_DIFF = 45
    V_DUTY_CYCLE_1_1 = 46
    V_DUTY_CYCLE_2_1 = 47
    V_DUTY_CYCLE_1_2 = 48
    V_DUTY_CYCLE_2_2 = 49
    V_DUTY_CYCLE_1_3 = 50
    V_DUTY_CYCLE_2_3 = 51
    V_DUTY_CYCLE_1_4 = 52
    V_DUTY_CYCLE_2_4 = 53
    V_V_INPUT_IIB_1 = 54
    V_V_OUTPUT_IIB_1 = 55
    V_I_IGBT_1_IIB_1 = 56
    V_I_IGBT_2_IIB_1 = 57
    V_TEMP_IGBT_1_IIB_1 = 58
    V_TEMP_IGBT_2_IIB_1 = 59
    V_V_DRIVER_IIB_1 = 60
    V_I_DRIVER_1_IIB_1 = 61
    V_I_DRIVER_2_IIB_1 = 62
    V_TEMP_INDUCTOR_IIB_1 = 63
    V_TEMP_HEATSINK_IIB_1 = 64
    V_V_INPUT_IIB_2 = 65
    V_V_OUTPUT_IIB_2 = 66
    V_I_IGBT_1_IIB_2 = 67
    V_I_IGBT_2_IIB_2 = 68
    V_TEMP_IGBT_1_IIB_2 = 69
    V_TEMP_IGBT_2_IIB_2 = 70
    V_V_DRIVER_IIB_2 = 71
    V_I_DRIVER_1_IIB_2 = 72
    V_I_DRIVER_2_IIB_2 = 73
    V_TEMP_INDUCTOR_IIB_2 = 74
    V_TEMP_HEATSINK_IIB_2 = 75
    V_V_INPUT_IIB_3 = 76
    V_V_OUTPUT_IIB_3 = 77
    V_I_IGBT_1_IIB_3 = 78
    V_I_IGBT_2_IIB_3 = 79
    V_TEMP_IGBT_1_IIB_3 = 80
    V_TEMP_IGBT_2_IIB_3 = 81
    V_V_DRIVER_IIB_3 = 82
    V_I_DRIVER_1_IIB_3 = 83
    V_I_DRIVER_2_IIB_3 = 84
    V_TEMP_INDUCTOR_IIB_3 = 85
    V_TEMP_HEATSINK_IIB_3 = 86
    V_V_INPUT_IIB_4 = 87
    V_V_OUTPUT_IIB_4 = 88
    V_I_IGBT_1_IIB_4 = 89
    V_I_IGBT_2_IIB_4 = 90
    V_TEMP_IGBT_1_IIB_4 = 91
    V_TEMP_IGBT_2_IIB_4 = 92
    V_V_DRIVER_IIB_4 = 93
    V_I_DRIVER_1_IIB_4 = 94
    V_I_DRIVER_2_IIB_4 = 95
    V_TEMP_INDUCTOR_IIB_4 = 96
    V_TEMP_HEATSINK_IIB_4 = 97
    V_IIB_INTERLOCKS_1 = 98
    V_IIB_INTERLOCKS_2 = 99
    V_IIB_INTERLOCKS_3 = 100
    V_IIB_INTERLOCKS_4 = 101
    V_I_MOD_1 = 102
    V_I_MOD_2 = 103
    V_I_MOD_3 = 104
    V_I_MOD_4 = 105


# --- Const ACDC ---

class ConstFBP_DCLink(ConstPSBSMP):
    """Namespace for organizing power supply FBP_DCLink BSMP constants."""

    # --- FBP_DCLink variables ---
    V_PS_SOFT_INTERLOCKS = 25
    V_PS_HARD_INTERLOCKS = 26
    V_MODULES_STATUS = 27
    V_V_OUT = 28
    V_V_OUT_1 = 29
    V_V_OUT_2 = 30
    V_V_OUT_3 = 31
    V_DIG_POT_TAP = 32


class ConstFAC_2S_ACDC(ConstPSBSMP):
    """Namespace for organizing power supply FAC_2S_ACDC BSMP constants."""

    # --- FAC_2S_ACDC variables ---
    V_PS_SOFT_INTERLOCKS = 25
    V_PS_HARD_INTERLOCKS = 26
    V_V_CAPBANK = 27
    V_V_OUT_RECTIFIER = 28
    V_I_OUT_RECTIFIER = 29
    V_TEMP_HEATSINK = 30
    V_TEMP_INDUCTORS = 31
    V_DUTY_CYCLE = 32
    V_I_INPUT_IS_IIB = 33
    V_V_INPUT_IS_IIB = 34
    V_TEMP_INDUCTOR_IS_IIB = 35
    V_TEMP_HEATSINK_IS_IIB = 36
    V_OUTPUT_CMD_IIB = 37
    V_CAPBANK_CMD_IIB = 38
    V_TEMP_INDUCTOR_CMD_IIB = 39
    V_TEMP_HEATSINK_CMD_IIB = 40
    V_I_LEAKAGE_CMD_IIB = 41
    V_IIB_INTERLOCKS_IS = 42
    V_IIB_INTERLOCKS_CMD = 43


class ConstFAC_2P4S_ACDC(ConstPSBSMP):
    """Namespace for organizing power supply FAC_2P4S_ACDC BSMP constants."""

    # --- FAC_2P4S_ACDC variables ---
    V_PS_SOFT_INTERLOCKS = 25
    V_PS_HARD_INTERLOCKS = 26
    V_V_CAPACITOR_BANK = 27
    V_V_OUT_RECTIFIER = 28
    V_I_OUT_RECTIFIER = 29
    V_TEMP_HEATSINK = 30
    V_TEMP_INDUCTORS = 31
    V_DUTY_CYCLE = 32
    V_I_INPUT_IS_IIB = 33
    V_V_INPUT_IS_IIB = 34
    V_TEMP_INDUCTOR_IS_IIB = 35
    V_TEMP_HEATSINK_IS_IIB = 36
    V_V_OUTPUT_CMD_IIB = 37
    V_V_CAPBANK_CMD_IIB = 38
    V_TEMP_INDUCTOR_CMD_IIB = 39
    V_TEMP_HEATSINK_CMD_IIB = 40
    V_I_LEAKAGE_CMD_IIB = 41
    V_IIB_INTERLOCKS_IS = 42
    V_IIB_INTERLOCKS_CMD = 43

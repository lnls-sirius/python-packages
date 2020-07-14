"""Power Supply BSMP Entities.

Module for definitions of BSMP entities of power supply devices.

Documentation:

https://wiki-sirius.lnls.br/mediawiki/index.php/Machine:Power_Supplies
"""

from ...bsmp import Entity as _Entity
from ...bsmp import Entities as _Entities
from ...bsmp import Types as _Types

from .constants import ConstPSBSMP as _ConstPSBSMP


class Parameters(_Entity):
    """Power supply parameters."""

    _parameters = {
        # ----- class PS -----
        0: {'count': 64, 'var_type': _Types.T_FLOAT, 'unit': '',
            'init': False, 'Op': True},
        1: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': '',
            'init': True, 'Op': False},
        2: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': '',
            'init': True, 'Op': False},
        # ----- class Communication -----
        3: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': '',
            'init': False, 'Op': True},
        4: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': 'bps',
            'init': True, 'Op': False},
        5: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': '',
            'init': False, 'Op': True},
        6: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': '',
            'init': True, 'Op': False},
        7: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': '',
            'init': True, 'Op': False},
        8: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': '',
            'init': True, 'Op': False},
        9: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': '',
            'init': True, 'Op': False},
        10: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': '%',
             'init': True, 'Op': False},
        # ----- class Control -----
        11: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': 'Hz',
             'init': True, 'Op': False},
        12: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': 'Hz',
             'init': True, 'Op': False},
        13: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': '',
             'init': True, 'Op': False},
        14: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': 'A/V',
             'init': False, 'Op': True},
        15: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': 'A/V',
             'init': False, 'Op': True},
        16: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': '%',
             'init': False, 'Op': True},
        17: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': '%',
             'init': False, 'Op': True},
        # ----- class PWM -----
        18: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': 'Hz',
             'init': True, 'Op': False},
        19: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': 'ns',
             'init': True, 'Op': False},
        20: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': 'pu',
             'init': False, 'Op': True},
        21: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': 'pu',
             'init': False, 'Op': True},
        22: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': 'pu',
             'init': False, 'Op': True},
        23: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': 'pu',
             'init': False, 'Op': True},
        24: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': 'pu',
             'init': False, 'Op': True},
        # ----- class HRADC -----
        25: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': '',
             'init': True, 'Op': False},
        26: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': 'MHz',
             'init': True, 'Op': False},
        27: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': 'Hz',
             'init': True, 'Op': False},
        28: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': '',
             'init': True, 'Op': False},
        29: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': '',
             'init': True, 'Op': False},
        30: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': '',
             'init': True, 'Op': False},
        31: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': '',
             'init': True, 'Op': False},
        32: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': '',
             'init': True, 'Op': False},
        # ----- class SigGen -----
        33: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': '',
             'init': True, 'Op': False},
        34: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': '',
             'init': True, 'Op': False},
        35: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': 'Hz',
             'init': False, 'Op': True},
        36: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': 'A/V/%',
             'init': False, 'Op': True},
        37: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': 'A/V/%',
             'init': False, 'Op': True},
        38: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': '',
             'init': True, 'Op': False},
        # ----- class WfmRef -----
        39: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': '',
             'init': True, 'Op': False},
        40: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': '',
             'init': True, 'Op': False},
        41: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': 'Hz',
             'init': True, 'Op': False},
        42: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': 'A/V/%',
             'init': False, 'Op': True},
        43: {'count': 4, 'var_type': _Types.T_FLOAT, 'unit': 'A/V/%',
             'init': False, 'Op': True},
        # ----- class Analog Variables -----
        44: {'count': 64, 'var_type': _Types.T_FLOAT, 'unit': '',
             'init': False, 'Op': True},
        45: {'count': 64, 'var_type': _Types.T_FLOAT, 'unit': '',
             'init': False, 'Op': True},
        # ----- class Debounding manager -----
        46: {'count': 32, 'var_type': _Types.T_FLOAT, 'unit': 'us',
             'init': True, 'Op': False},
        47: {'count': 32, 'var_type': _Types.T_FLOAT, 'unit': 'us',
             'init': True, 'Op': False},
        48: {'count': 32, 'var_type': _Types.T_FLOAT, 'unit': 'us',
             'init': True, 'Op': False},
        49: {'count': 32, 'var_type': _Types.T_FLOAT, 'unit': 'us',
             'init': True, 'Op': False},
        # ---- Scope -----
        50: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': 'Hz',
             'init': True, 'Op': False},
        51: {'count': 1, 'var_type': _Types.T_FLOAT, 'unit': '',
             'init': True, 'Op': False},
          }

    def value_to_load(self, eid, value):
        """."""
        size = Parameters._parameters[eid]['count']
        var_types = [Parameters._parameters[eid]['var_type']] * size
        if eid == 0:
            # power supply name
            value = [float(ord(c)) for c in value]
        load = self._conv_value_to_load(var_types, size, value)
        return load

    def load_to_value(self, eid, load):
        """."""
        size = Parameters._parameters[eid]['count']
        var_types = [Parameters._parameters[eid]['var_type']] * size
        value = self._conv_load_to_value(var_types, size, load)
        if eid == 0:
            # power supply name
            value = [chr(int(v)) for v in value]
        return value

    @property
    def eids(self):
        """Return entities identifications."""
        return tuple(Parameters._parameters.keys())

    def __getitem__(self, key):
        """."""
        return Parameters._parameters[key]


class EntitiesPS(_Entities):
    """PS Entities."""

    _ps_variables = (
        # --- common variables
        {'eid': 0, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT16},
        {'eid': 1, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 2, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 3, 'waccess': False, 'count': 128, 'var_type': _Types.T_CHAR},
        {'eid': 4, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 5, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 6, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT16},
        {'eid': 7, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT16},
        {'eid': 8, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT16},
        {'eid': 9, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 10, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 11, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 12, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 13, 'waccess': False, 'count': 4, 'var_type': _Types.T_FLOAT},
        {'eid': 14, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT16},
        {'eid': 15, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT16},
        {'eid': 16, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 17, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 18, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 19, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 20, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 21, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 22, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 23, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 24, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 25, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 26, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 27, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        # --- undefined variables
        {'eid': 28, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT8},
        {'eid': 29, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT8},
        {'eid': 30, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT8},
        )

    _ps_functions = (
        {'eid': _ConstPSBSMP.F_TURN_ON,
         'i_type': (), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_TURN_OFF,
         'i_type': (), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_OPEN_LOOP,
         'i_type': (), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_CLOSE_LOOP,
         'i_type': (), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_SELECT_OP_MODE,
         'i_type': (_Types.T_ENUM,), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_RESET_INTERLOCKS,
         'i_type': (), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_SET_COMMAND_INTERFACE,
         'i_type': (_Types.T_ENUM,), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_SET_SERIAL_TERMINATION,
         'i_type': (_Types.T_UINT16,), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_UNLOCK_UDC,
         'i_type': (_Types.T_UINT16,), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_LOCK_UDC,
         'i_type': (_Types.T_UINT16,), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_CFG_SOURCE_SCOPE,
         'i_type': (_Types.T_UINT32,), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_CFG_FREQ_SCOPE,
         'i_type': (_Types.T_FLOAT,), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_CFG_DURATION_SCOPE,
         'i_type': (_Types.T_FLOAT,), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_ENABLE_SCOPE,
         'i_type': (), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_DISABLE_SCOPE,
         'i_type': (), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_SYNC_PULSE,
         'i_type': (), 'o_type': ()},
        {'eid': _ConstPSBSMP.F_SET_SLOWREF,
         'i_type': (_Types.T_FLOAT,), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_SET_SLOWREF_FBP,
         'i_type': (_Types.T_FLOAT, _Types.T_FLOAT, _Types.T_FLOAT,
                    _Types.T_FLOAT),
         'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_SET_SLOWREF_READBACK_MON,
         'i_type': (_Types.T_FLOAT, _Types.T_FLOAT,
                    _Types.T_FLOAT, _Types.T_FLOAT,),
         'o_type': (_Types.T_FLOAT, _Types.T_FLOAT,
                    _Types.T_FLOAT, _Types.T_FLOAT,)},
        {'eid': _ConstPSBSMP.F_SET_SLOWREF_FBP_READBACK_MON,
         'i_type': (_Types.T_FLOAT, _Types.T_FLOAT,
                    _Types.T_FLOAT, _Types.T_FLOAT,),
         'o_type': (_Types.T_FLOAT, _Types.T_FLOAT,
                    _Types.T_FLOAT, _Types.T_FLOAT,)},
        {'eid': _ConstPSBSMP.F_SET_SLOWREF_READBACK_REF,
         'i_type': (_Types.T_FLOAT, _Types.T_FLOAT,
                    _Types.T_FLOAT, _Types.T_FLOAT,),
         'o_type': (_Types.T_FLOAT, _Types.T_FLOAT,
                    _Types.T_FLOAT, _Types.T_FLOAT,)},
        {'eid': _ConstPSBSMP.F_SET_SLOWREF_FBP_READBACK_REF,
         'i_type': (_Types.T_FLOAT, _Types.T_FLOAT,
                    _Types.T_FLOAT, _Types.T_FLOAT,),
         'o_type': (_Types.T_FLOAT, _Types.T_FLOAT,
                    _Types.T_FLOAT, _Types.T_FLOAT,)},
        {'eid': _ConstPSBSMP.F_RESET_COUNTERS,
         'i_type': (), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_CFG_WFMREF,
         'i_type': (_Types.T_UINT16, _Types.T_UINT16,
                    _Types.T_FLOAT, _Types.T_FLOAT, _Types.T_FLOAT),
         'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_SELECT_WFMREF,
         'i_type': (_Types.T_UINT16,), 'o_type': (_Types.T_UINT8,)},
        # return changed T_UINT8 -> T_UINT16
        {'eid': _ConstPSBSMP.F_GET_WFMREF_SIZE,
         'i_type': (_Types.T_UINT16,), 'o_type': (_Types.T_UINT16, )},
        {'eid': _ConstPSBSMP.F_RESET_WFMREF,
         'i_type': (), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_CFG_SIGGEN,
         'i_type': (_Types.T_ENUM, _Types.T_UINT16,
                    _Types.T_FLOAT, _Types.T_FLOAT, _Types.T_FLOAT,
                    _Types.T_FLOAT, _Types.T_FLOAT,
                    _Types.T_FLOAT, _Types.T_FLOAT),
         'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_SET_SIGGEN,
         'i_type': (_Types.T_FLOAT, _Types.T_FLOAT, _Types.T_FLOAT),
         'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_ENABLE_SIGGEN,
         'i_type': (), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_DISABLE_SIGGEN,
         'i_type': (), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_SET_PARAM,
         'i_type': (_Types.T_PARAM, _Types.T_UINT16, _Types.T_FLOAT,),
         'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_GET_PARAM,
         'i_type': (_Types.T_PARAM, _Types.T_UINT16,),
         'o_type': (_Types.T_FLOAT,)},
        {'eid': _ConstPSBSMP.F_SAVE_PARAM_EEPROM,
         'i_type': (_Types.T_PARAM, _Types.T_UINT16,),
         'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_LOAD_PARAM_EEPROM,
         'i_type': (_Types.T_PARAM, _Types.T_UINT16,),
         'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_SAVE_PARAM_BANK,
         'i_type': (), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_LOAD_PARAM_BANK,
         'i_type': (), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_SET_DSP_COEFFS,
         'i_type': (_Types.T_DSP_CLASS, _Types.T_UINT16,
                    _Types.T_FLOAT, _Types.T_FLOAT, _Types.T_FLOAT,
                    _Types.T_FLOAT, _Types.T_FLOAT, _Types.T_FLOAT,
                    _Types.T_FLOAT, _Types.T_FLOAT, _Types.T_FLOAT,
                    _Types.T_FLOAT, _Types.T_FLOAT, _Types.T_FLOAT),
         'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_GET_DSP_COEFF,
         'i_type': (_Types.T_DSP_CLASS, _Types.T_UINT16, _Types.T_UINT16,),
         'o_type': (_Types.T_FLOAT,)},
        {'eid': _ConstPSBSMP.F_SAVE_DSP_COEFFS_EEPROM,
         'i_type': (_Types.T_DSP_CLASS, _Types.T_UINT16,),
         'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_LOAD_DSP_COEFFS_EEPROM,
         'i_type': (_Types.T_DSP_CLASS, _Types.T_UINT16,),
         'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_SAVE_DSP_MODULES_EEPROM,
         'i_type': (), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_LOAD_DSP_MODULES_EEPROM,
         'i_type': (), 'o_type': (_Types.T_UINT8,)},
        {'eid': _ConstPSBSMP.F_RESET_UDC,
         'i_type': (), 'o_type': ()},)

    _ps_curves = (
        {'eid': 0, 'waccess': True, 'count': 256,
         'nblocks': 16, 'var_type': _Types.T_FLOAT},
        {'eid': 1, 'waccess': True, 'count': 256,
         'nblocks': 16, 'var_type': _Types.T_FLOAT},
        {'eid': 2, 'waccess': False, 'count': 256,
         'nblocks': 16, 'var_type': _Types.T_FLOAT},)

    _ps_parameters = Parameters()

    def __init__(self):
        """Call super."""
        super().__init__(
            self._ps_variables, self._ps_curves, self._ps_functions)

    @property
    def parameters(self):
        """Return pwrsuppli parameters."""
        return EntitiesPS._ps_parameters


# --- Entities DCDC ---


class EntitiesFBP(EntitiesPS):
    """FBP-type power supply entities."""

    _ps_variables = EntitiesPS._ps_variables + (
        # --- FBP-specific variables
        {'eid': 31, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 32, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 33, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 34, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 35, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 36, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 37, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        # --- undefined Variables
        {'eid': 38, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT8},
        {'eid': 39, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT8},
        {'eid': 40, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT8},
        {'eid': 41, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT8},
        {'eid': 42, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT8},
        {'eid': 43, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT8},
        {'eid': 44, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT8},
        {'eid': 45, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT8},
        # --- mirror variables
        # ------ PS_STATUS
        {'eid': 46, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT16},
        {'eid': 47, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT16},
        {'eid': 48, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT16},
        {'eid': 49, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT16},
        # ------ PS_SETPOINT
        {'eid': 50, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 51, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 52, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 53, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        # ------ PS_REFERENCE
        {'eid': 54, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 55, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 56, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 57, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        # ------ PS_SOFT_INTERLOCK
        {'eid': 58, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 59, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 60, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 61, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        # ------ PS_HARD_INTERLOCK
        {'eid': 62, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 63, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 64, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 65, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        # ------ PS_I_LOAD
        {'eid': 66, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 67, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 68, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 69, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
    )

    _ps_curves = (
        {'eid': 0, 'waccess': True, 'count': 256,
         'nblocks': 4, 'var_type': _Types.T_FLOAT},
        {'eid': 1, 'waccess': True, 'count': 256,
         'nblocks': 4, 'var_type': _Types.T_FLOAT},
        {'eid': 2, 'waccess': False, 'count': 256,
         'nblocks': 4, 'var_type': _Types.T_FLOAT},)


class EntitiesFAC_DCDC(EntitiesPS):
    """FAC-type power supply entities."""

    _ps_variables = EntitiesPS._ps_variables + (
        # --- FAC_DCDC-specific variables
        {'eid': 25, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 26, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 27, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 28, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 29, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 30, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 31, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 32, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 33, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 34, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 35, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 36, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 37, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 38, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 39, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 40, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 41, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 42, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 43, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 44, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32})


class EntitiesFAC_2P4S_DCDC(EntitiesPS):
    """FAC_2P4S-type power supply entities (BO Dipoles)."""

    _ps_variables = EntitiesPS._ps_variables + (
        # --- FAC_2P4S-specific variables
        {'eid': 25, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 26, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 27, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 28, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 29, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 30, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 31, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 32, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 33, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 34, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 35, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 36, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 37, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 38, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 39, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 40, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 41, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 42, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 43, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 44, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 45, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 46, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 47, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 48, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 49, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 50, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 51, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 52, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 53, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 54, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 55, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 56, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 57, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 58, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 59, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 60, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 61, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 62, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 63, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 64, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 65, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 66, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 67, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 68, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 69, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 70, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 71, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 72, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 73, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 74, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 75, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 76, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 77, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 78, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 79, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 80, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 81, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 82, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 83, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 84, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 85, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 86, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 87, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 88, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 89, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 90, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 91, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 92, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 93, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 94, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 95, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 96, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 97, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 98, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 99, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 100, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 101, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 102, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 103, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 104, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 105, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 106, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 107, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 108, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 109, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 110, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 111, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 112, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 113, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 114, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 115, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 116, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 117, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 118, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 119, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 120, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},)


class EntitiesFAC_2S_DCDC(EntitiesPS):
    """FAC_2S-type power supply entities."""

    _ps_variables = EntitiesPS._ps_variables + (
        # --- FAC_2S_DCDC-specific variables
        {'eid': 25, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 26, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 27, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 28, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 29, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 30, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 31, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 32, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 33, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 34, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 35, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 36, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 37, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 38, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 39, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 40, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 41, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 42, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 43, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 44, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 45, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 46, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 47, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 48, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 49, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 50, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 51, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 52, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 53, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},)


class EntitiesFAP(EntitiesPS):
    """FAP-type power supply entities."""

    _ps_variables = EntitiesPS._ps_variables + (
        # --- FAP-specific variables
        {'eid': 25, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 26, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 27, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 28, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 29, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 30, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 31, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 32, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 33, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 34, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 35, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 36, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 37, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 38, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 39, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 40, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 41, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 42, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 43, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 44, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 45, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 46, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 47, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 48, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32})


class EntitiesFAP_4P(EntitiesPS):
    """FAP_4P-type power supply entities."""

    _ps_variables = EntitiesPS._ps_variables + (
        # --- FAP_4P-specific variables
        {'eid': 25, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 26, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 27, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 28, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 29, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 30, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 31, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 32, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 33, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 34, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 35, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 36, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 37, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 38, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 39, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 40, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 41, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 42, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 43, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 44, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 45, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 46, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 47, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 48, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 49, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 50, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 51, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 52, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 53, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 54, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 55, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 56, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 57, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 58, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 59, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 60, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 61, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 62, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 63, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 64, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 65, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 66, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 67, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 68, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 69, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 70, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 71, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 72, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 73, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 74, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 75, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 76, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 77, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 78, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 79, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 80, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 81, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 82, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 83, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 84, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 85, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 86, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 87, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 88, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 89, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 90, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 91, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 92, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 93, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 94, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 95, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 96, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 97, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 98, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 99, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 100, 'waccess': False, 'count': 1,
         'var_type': _Types.T_UINT32},
        {'eid': 101, 'waccess': False, 'count': 1,
         'var_type': _Types.T_UINT32},
        {'eid': 102, 'waccess': False, 'count': 1,
         'var_type': _Types.T_UINT32},
        {'eid': 103, 'waccess': False, 'count': 1,
         'var_type': _Types.T_UINT32},
        {'eid': 104, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 105, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 106, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 107, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT})


class EntitiesFAP_2P2S(EntitiesPS):
    """FAP_2P2S-type power supply entities."""

    _ps_variables = EntitiesPS._ps_variables + (
        # --- FAP_2P2S-specific variables
        {'eid': 25, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 26, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 27, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 28, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 29, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 30, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 31, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 32, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 33, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 34, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 35, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 36, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 37, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 38, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 39, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 40, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 41, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 42, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 43, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 44, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 45, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 46, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 47, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 48, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 49, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 50, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 51, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 52, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 53, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 54, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 55, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 56, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 57, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 58, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 59, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 60, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 61, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 62, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 63, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 64, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 65, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 66, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 67, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 68, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 69, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 70, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 71, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 72, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 73, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 74, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 75, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 76, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 77, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 78, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 79, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 80, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 81, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 82, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 83, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 84, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 85, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 86, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 87, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 88, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 89, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 90, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 91, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 92, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 93, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 94, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 95, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 96, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 97, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 98, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 99, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 100, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 101, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 102, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 103, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 104, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 105, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},)


# --- Entities ACDC ---


class EntitiesFBP_DCLink(EntitiesPS):
    """FBP_DCLink-type power supplies entities."""

    _ps_variables = EntitiesPS._ps_variables + (
        # --- FBP_DCLINK-specific variables
        {'eid': 25, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 26, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 27, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 28, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 29, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 30, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 31, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 32, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT8},
    )

    _ps_curves = ()


class EntitiesFAC_2S_ACDC(EntitiesPS):
    """FAC_2S_ACDC-type power supply entities."""

    _ps_variables = EntitiesPS._ps_variables + (
        # --- FAC_2S_ACDC-specific variables
        {'eid': 25, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 26, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 27, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 28, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 29, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 30, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 31, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 32, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 33, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 34, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 35, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 36, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 37, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 38, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 39, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 40, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 41, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 42, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 43, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},)

    _ps_curves = ()


class EntitiesFAC_2P4S_ACDC(EntitiesPS):
    """FAC_2P4S_ACDC-type power supply entities."""

    _ps_variables = EntitiesPS._ps_variables + (
        # --- FAC_2P4S_ACDC-specific variables
        {'eid': 25, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 26, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 27, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 28, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 29, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 30, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 31, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 32, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 33, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 34, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 35, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 36, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 37, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 38, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 39, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 40, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 41, 'waccess': False, 'count': 1, 'var_type': _Types.T_FLOAT},
        {'eid': 42, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32},
        {'eid': 43, 'waccess': False, 'count': 1, 'var_type': _Types.T_UINT32})

    _ps_curves = ()

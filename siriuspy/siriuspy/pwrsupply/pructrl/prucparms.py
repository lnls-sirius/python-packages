"""PRU Controller Parameters.

These parameters are used in PRUController class to
interact with BSMP devices.
"""

from ..bsmp.constants import ConstPSBSMP as _const
from ..psctrl.psmodel import PSModelFactory as _PSModelFactory


class PRUCParmsFBP:
    """FBP-specific PRUC parameters."""

    FREQ_SCAN = 5.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FBP')
    CONST_PSBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_const.G_ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_const.G_READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_const.G_WRITE] = tuple(sorted(Entities.list_variables(2)))
    groups[CONST_PSBSMP.G_SOFB] = (
        CONST_PSBSMP.V_PS_SETPOINT1,
        CONST_PSBSMP.V_PS_SETPOINT2,
        CONST_PSBSMP.V_PS_SETPOINT3,
        CONST_PSBSMP.V_PS_SETPOINT4,
        CONST_PSBSMP.V_PS_REFERENCE1,
        CONST_PSBSMP.V_PS_REFERENCE2,
        CONST_PSBSMP.V_PS_REFERENCE3,
        CONST_PSBSMP.V_PS_REFERENCE4,
        CONST_PSBSMP.V_I_LOAD1,
        CONST_PSBSMP.V_I_LOAD2,
        CONST_PSBSMP.V_I_LOAD3,
        CONST_PSBSMP.V_I_LOAD4,)


class PRUCParmsFBP_DCLink:
    """FBP_DCLink-specific PRUC parameters."""

    FREQ_SCAN = 2.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FBP_DCLink')
    CONST_PSBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_const.G_ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_const.G_READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_const.G_WRITE] = tuple(sorted(Entities.list_variables(2)))


class PRUCParmsFAC_2S_DCDC:
    """FAC_2S specific PRUC parameters.

    Represent FAC_2S_DCDC psmodels.
    """

    FREQ_SCAN = 5.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FAC_2S_DCDC')
    CONST_PSBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_const.G_ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_const.G_READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_const.G_WRITE] = tuple(sorted(Entities.list_variables(2)))


class PRUCParmsFAC_2P4S_DCDC:
    """FAC-specific PRUC parameters.

    Represent FAC_2P4S psmodels.
    """

    FREQ_SCAN = 5.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FAC_2P4S_DCDC')
    CONST_PSBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_const.G_ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_const.G_READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_const.G_WRITE] = tuple(sorted(Entities.list_variables(2)))


class PRUCParmsFAC_DCDC:
    """FAC-specific PRUC parameters.

    Represent FAC, FAC_2S, FAC_2P4S psmodels.
    """

    FREQ_SCAN = 5.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FAC_DCDC')
    CONST_PSBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_const.G_ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_const.G_READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_const.G_WRITE] = tuple(sorted(Entities.list_variables(2)))


class PRUCParmsFAC_2S_ACDC:
    """FAC_2S_ACDC-specific PRUC parameters."""

    FREQ_SCAN = 2.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FAC_2S_ACDC')
    CONST_PSBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_const.G_ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_const.G_READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_const.G_WRITE] = tuple(sorted(Entities.list_variables(2)))


class PRUCParmsFAC_2P4S_ACDC:
    """FAC_2P4S_ACDC-specific PRUC parameters."""

    FREQ_SCAN = 2.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FAC_2P4S_ACDC')
    CONST_PSBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_const.G_ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_const.G_READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_const.G_WRITE] = tuple(sorted(Entities.list_variables(2)))


class PRUCParmsFAP:
    """FAC-specific PRUC parameters.

    Represent FAP
    """

    FREQ_SCAN = 5.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FAP')
    CONST_PSBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_const.G_ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_const.G_READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_const.G_WRITE] = tuple(sorted(Entities.list_variables(2)))


class PRUCParmsFAP_4P:
    """FAC-specific PRUC parameters.

    Represent FAP_4P
    """

    FREQ_SCAN = 5.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FAP_4P')
    CONST_PSBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_const.G_ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_const.G_READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_const.G_WRITE] = tuple(sorted(Entities.list_variables(2)))


class PRUCParmsFAP_2P2S:
    """FAC_2P2S-specific PRUC parameters.

    Represent FAP_2P2S
    """

    FREQ_SCAN = 5.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FAP_2P2S')
    CONST_PSBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_const.G_ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_const.G_READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_const.G_WRITE] = tuple(sorted(Entities.list_variables(2)))

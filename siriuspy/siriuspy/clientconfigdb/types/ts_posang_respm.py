"""TS posang correction configurations.

Values in _template_dict are arbitrary. They are used just to compare with
corresponding values when a new configuration is tried to be inserted in the
servconf database.
"""
from copy import deepcopy as _dcopy


def get_dict():
    """Return a dict with ramp settings."""
    module_name = __name__.split('.')[-1]
    _dict = {
        'config_type_name': module_name,
        'value': _dcopy(_template_dict),
        'check': False,
    }

    return _dict


# Position-Angle Correction Response Matrices for the Storage Ring Injection
# (TS correctors)
#
# Horizontal Matrix:
#
# | DeltaPosX @TS-04:DI-Scrn-3 |   | h11 h12 |   | Kick TS-04:PU-InjSeptG(1&2)|
# |                            | = |         | * |       or TS-04:PS-CH       |
# | DeltaAngX @TS-04:DI-Scrn-3 |   | h21 h22 |   |   Kick TS-04:PU-InjSeptF   |
#
# Data structure:
#         h11   h12
#         h21   h22
#
# Vertical Matrix:
#
# | DeltaPosY @TS-04:DI-Scrn-3 |   | v11 v12 v13 v14 |   | Kick TS-04:PS-CV-0 |
# |                            | = |                 | * |                    |
# | DeltaAngY @TS-04:DI-Scrn-3 |   | v21 v22 v23 v24 |   | Kick TS-04:PS-CV-1 |
#                                                        |                    |
#                                                        |Kick TS-04:PS-CV-1E2|
#                                                        |                    |
#                                                        | Kick TS-04:PS-CV-2 |
#
# Data structure:
#         v11   v12
#         v21   v22

_template_dict = {
    'respm-x': [[0.0, 0.0],
                [0.0, 0.0]],
    'respm-y': [[0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0]],
}

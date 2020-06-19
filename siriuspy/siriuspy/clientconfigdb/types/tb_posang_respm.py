"""TB posang correction configurations.

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


# Position-Angle Correction Response Matrices for the Booster Injection
# (TB correctors)
#
#
# Horizontal Matrix (ch-sept):
#
#  | DeltaPosX @ TB-04:PM-InjSept |    | h11  h12 |   |  Kick TB-04:PS-CH-1   |
#  |                              | =  |          | * |                       |
#  | DeltaAngX @ TB-04:PM-InjSept |    | h21  h22 |   | Kick TB-04:PM-InjSept |
#
# Horizontal Matrix (ch-ch):
#
#  | DeltaPosX @ TB-04:PM-InjSept |    | h11  h12 |   |  Kick TB-04:PS-CH-1  |
#  |                              | =  |          | * |                      |
#  | DeltaAngX @ TB-04:PM-InjSept |    | h21  h22 |   |  Kick TB-04:PS-CH-2  |
#
# Data structure:
#         h11   h12
#         h21   h22
#
#
# Vertical Matrix:
#
#  | DeltaPosY @ TB-04:PM-InjSept |    | v11  v12 |   | Kick TB-04:PS-CV-1 |
#  |                              | =  |          | * |                    |
#  | DeltaAngY @ TB-04:PM-InjSept |    | v21  v22 |   | Kick TB-04:PS-CV-2 |
#
# Data structure:
#         v11   v12
#         v21   v22

_template_dict = {
    'respm-x': [[0.0, 0.0],
                [0.0, 0.0]],
    'respm-y': [[0.0, 0.0],
                [0.0, 0.0]],
}

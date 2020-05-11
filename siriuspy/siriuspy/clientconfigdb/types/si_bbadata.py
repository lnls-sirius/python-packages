"""Sirius storage ring BBA data configuration.

Values in _template_dict are arbitrary. They are used just to compare with
corresponding values when a new configuration is tried to be inserted in the
servconf database.
"""
from copy import deepcopy as _dcopy


def get_dict():
    """Return configuration type dictionary."""
    module_name = __name__.split('.')[-1]
    _dict = {
        'config_type_name': module_name,
        'value': _dcopy(_template_dict),
        'check': False,
    }
    return _dict


# Sirius storage ring BBA data:
#
_template_dict = {
    'bpmnames': list(),
    'quadnames': list(),
    'scancenterx': [0.0, ] * 160,  # unit: um
    'scancentery': [0.0, ] * 160,  # unit: um
    'measure': dict(),
    }

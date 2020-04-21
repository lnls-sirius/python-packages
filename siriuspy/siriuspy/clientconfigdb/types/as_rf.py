"""AS RF configuration."""
from copy import deepcopy as _dcopy

# NOTE: absolute imports are necessary here due to how
# CONFIG_TYPES in __init__.py is built.
from siriuspy.clientconfigdb.types.global_config import _pvs_as_rf
from siriuspy.clientconfigdb.types.global_config import _pvs_bo_rf
from siriuspy.clientconfigdb.types.global_config import _pvs_si_rf


def get_dict():
    """Return configuration type dictionary."""
    module_name = __name__.split('.')[-1]
    _dict = {
        'config_type_name': module_name,
        'value': _dcopy(_template_dict),
        'check': False,
    }
    return _dict


# When using this type of configuration to set the machine,
# the list of PVs should be processed in the same order they are stored
# in the configuration. The second numeric parameter in the pair is the
# delay [s] the client should wait before setting the next PV.


_template_dict = {
    'pvs':
    _pvs_as_rf + _pvs_bo_rf + _pvs_si_rf
    }

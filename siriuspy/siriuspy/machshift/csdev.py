"""Machine Shift Control System App."""

from .. import csdev as _csdev


# --- Enumeration Types ---

class ETypes(_csdev.ETypes):
    """Local enumerate types."""

    MACHSHIFT = (
        'Users', 'Commissioning', 'Conditioning',
        'Injection', 'MachineStudy', 'Maintenance')


_et = ETypes


# --- Const class ---

class Const(_csdev.Const):
    """Const class."""

    MachShift = _csdev.Const.register('MachShift', _et.MACHSHIFT)


_c = Const


# --- Databases ---


def get_machshift_propty_database():
    """Return property database of machine shift IOC."""
    dbase = {
        'Version-Cte': {'type': 'str', 'value': 'UNDEF'},
        'Mode-Sel': {
            'type': 'enum', 'value': _c.MachShift.Commissioning,
            'enums': _et.MACHSHIFT},
        'Mode-Sts': {
            'type': 'enum', 'value': _c.MachShift.Commissioning,
            'enums': _et.MACHSHIFT},
    }
    dbase = _csdev.add_pvslist_cte(dbase)
    return dbase

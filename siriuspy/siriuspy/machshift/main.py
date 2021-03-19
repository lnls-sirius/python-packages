"""Main module of Machine Shift Application."""
import time as _time
from datetime import datetime as _datetime

from ..callbacks import Callback as _Callback

from .csdev import Const as _Const, ETypes as _ETypes, \
    get_machshift_propty_database as _get_database
from .utils import MacScheduleData as _MacSched


class App(_Callback):
    """Main application for handling machine shift."""

    def __init__(self):
        """Class constructor."""
        super().__init__()
        self._pvs_database = _get_database()

        self._progmd_users = _MacSched.is_user_shift_programmed(
            datetime=_datetime.now())
        self._mode = _Const.MachShift.Commissioning

    def init_database(self):
        """Set initial PV values."""
        self.run_callbacks('Mode-Sel', self._mode)
        self.run_callbacks('Mode-Sts', self._mode)
        self.run_callbacks('ProgmdUsersShift-Mon', self._progmd_users)

    @property
    def pvs_database(self):
        """Return pvs_database."""
        return self._pvs_database

    def process(self, interval):
        """Sleep."""
        _time.sleep(interval)

    def read(self, reason):
        """Read from IOC database."""
        value = None
        if 'ProgmdUsersShift' in reason:
            new_progmd_users = _MacSched.is_user_shift_programmed(
                datetime=_datetime.now())
            if new_progmd_users != self._progmd_users:
                self._progmd_users = new_progmd_users
                value = new_progmd_users
                self.run_callbacks('ProgmdUsersShift-Mon', self._progmd_users)
        return value

    def write(self, reason, value):
        """Write value to reason and let callback update PV database."""
        status = False
        if reason == 'Mode-Sel':
            if 0 <= value < len(_ETypes.MACHSHIFT):
                self._mode = value
                self.run_callbacks('Mode-Sts', value)
                status = True
        return status

"""UDC class."""

from .psbsmp import PSBSMPFactory as _PSBSMPFactory
from .psmodel import PSModelFactory as _PSModelFactory
from . import prucparms as _prucparms


class UDC:
    """UDC."""

    _timeout_default = 100  # [ms]

    _prucparms = {
        'FBP': _prucparms.PRUCParmsFBP,
        'FBP_DCLink': _prucparms.PRUCParmsFBP_DCLink,
        'FAC_2S_DCDC': _prucparms.PRUCParmsFAC_2S_DCDC,
        'FAC_2P4S_DCDC': _prucparms.PRUCParmsFAC_2P4S_DCDC,
        'FAC_DCDC': _prucparms.PRUCParmsFAC_DCDC,
        'FAC_2S_ACDC': _prucparms.PRUCParmsFAC_2S_ACDC,
        'FAC_2P4S_ACDC': _prucparms.PRUCParmsFAC_2P4S_ACDC,
        'FAP': _prucparms.PRUCParmsFAP,
        'FAP_4P': _prucparms.PRUCParmsFAP_4P,
        'FAP_2P2S': _prucparms.PRUCParmsFAP_2P2S,
    }

    def __init__(self, pru, psmodel, device_ids):
        """Init."""
        self._pru = pru
        self._device_ids = device_ids
        self._psmodel = psmodel
        self._bsmp_devs = self._create_bsmp_connectors()

    @property
    def pru(self):
        """Return PRU used for communication with UDC."""
        return self._pru

    @property
    def psmodel(self):
        """Return power supply model associated with UDC."""
        return self._psmodel

    @property
    def device_ids(self):
        """."""
        return self._device_ids

    @property
    def prucparms(self):
        """PRU Controller parameters."""
        return UDC._prucparms[self._psmodel]

    @property
    def CONST_PSBSMP(self):
        """Return PSBSMP constants."""
        return self.prucparms.CONST_PSBSMP

    def reset(self, timeout=_timeout_default):
        """Reset UDC."""
        # turn off all power supplies (NOTE: or F_RESET_UDC does not work)
        for bsmp in self._bsmp_devs.values():
            bsmp.execute_function(
                func_id=self.CONST_PSBSMP.F_TURN_OFF, timeout=timeout)

        # reset UDC proper.
        bsmp_dev = self._bsmp_devs[next(iter(self._bsmp_devs))]  # fisrt bsmp
        bsmp_dev.execute_function(
            func_id=self.CONST_PSBSMP.F_RESET_UDC, timeout=timeout,
            read_flag=False)

    def parse_firmware_version(self, version):
        """Process firmware version from BSMP device."""
        # uses first BSMP device
        bsmp_dev = self._bsmp_devs[next(iter(self._bsmp_devs))]  # first bsmp
        return bsmp_dev.parse_firmware_version(version)

    def reset_groups_of_variables(self, groups):
        """Reset groups of variables."""
        for bsmp_dev in self._bsmp_devs.values():
            bsmp_dev.reset_groups_of_variables(groups=groups)

    def _create_bsmp_connectors(self):
        bsmp = dict()
        model = _PSModelFactory.create(self._psmodel)
        bsmpsim_class = model.simulation_class
        for dev_id in self._device_ids:
            if self._pru.simulated:
                bsmp[dev_id] = bsmpsim_class(self._pru)
            else:
                bsmp[dev_id] = _PSBSMPFactory.create(
                    self._psmodel, dev_id, self._pru)
        return bsmp

    def __getitem__(self, index):
        """Return BSMP."""
        return self._bsmp_devs[index]

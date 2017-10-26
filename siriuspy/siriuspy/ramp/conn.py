"""Module with connector classes.

This module implements waveform communications with magnet soft IOcs and
ConfigDB service.
"""


from siriuspy.factory import MagnetFactory as _MagnetFactory
from siriuspy import envars as _envars
from siriuspy.servconf.conf_service import ConfigService


class ConnMagnet:
    """Magnet Connector Class."""

    def __init__(self,
                 use_vaca=False,
                 vaca_prefix=None):
        """Init method."""
        self._use_vaca = use_vaca
        self._vaca_prefix = vaca_prefix
        self._magnets = {}

    def wfm_send(self, maname, wfm_current):
        """Send current waveform to magnet power supply."""
        if maname not in self._magnets:
            self._create_magnet_conn(maname)
        magnet = self._magnets[maname]
        if not magnet.connected:
            raise Exception(
                    'Not connected to power supply of {}!'.format(maname))
        else:
            magnet.wfmdata_sp = wfm_current

    def wfm_recv(self, maname):
        """Receive current waveform to magnet power supply."""
        if maname not in self._magnets:
            self._create_magnet_conn(maname)
        magnet = self._magnets[maname]
        if not magnet.connected:
            raise Exception(
                'Not connected to power supply of {}!'.format(maname))
        else:
            wfm_current = magnet.wfmdata_rb
            return wfm_current

    def _create_magnet_conn(self, maname):
        self._pses[maname] = _MagnetFactory(maname=maname,
                                            use_vaca=self._use_vaca,
                                            vaca_prefix=self._vaca_prefix,
                                            lock=False,
                                            )


class ConnOrbit:
    """Connector class to interact with SOFT IOCs."""

    pass


class ConnTune:
    """Connector class to interact with TuneCorr IOCs."""

    pass


class ConnChrom:
    """Connector class to interact with ChromCorr IOCs."""

    pass


class ConnConfigDB:
    """Config DB connector class."""

    def __init__(self, url=_envars.server_url_configdb):
        """Init method."""
        self._conn = ConfigService(url)

    def insert_config(self, wfmset, name):
        """Insert ramp configuration ConfigDB."""
        # Build config settings
        config_type = wfmset.section.lower() + "_ramp_ps"
        value = self._get_config_value(wfmset)
        # Insert in DB
        response = self._conn.insert_config(
            config_type=config_type, name=name, value=value)

        if "result" in response:
            return 1
        else:
            return 0

    def get_config(self, wfmset, name):
        """Get ramp configuration from configDB and set appropriate objects."""
        config_type = wfmset.section.lower() + "_ramp_ps"
        response = self._conn.get_config(config_type=config_type, name=name)

        if "result" in response:
            config = response["result"]
            if type(config["value"]) is not dict:
                raise TypeError("Value is not a dict")
        else:
            return 0

        for pv, wvfrm in config["value"].items():
            ma = ":".join(pv.split(":")[:-1])
            if type(wvfrm) is not list:
                raise TypeError("Waveform is not a list")
            wfmset.set_wfm_current(ma, wvfrm)

        return 1

    def _get_config_value(self, wfmset):
        value = {}
        for magnet in wfmset.magnets:
            value[magnet + ":WfmData-SP"] = wfmset.get_wfm_current(magnet)
        return value

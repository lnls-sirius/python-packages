"""."""

import time as _time
import numpy as _np

from .device import DeviceNC as _DeviceNC
from .device import Devices as _Devices


class RFGen(_DeviceNC):
    """."""

    RF_DELTA_MIN = 0.1  # [Hz]
    RF_DELTA_MAX = 15000.0  # [Hz]
    RF_DELTA_RMP = 20  # [Hz]

    class DEVICES:
        """Devices names."""

        AS = 'RF-Gen'
        ALL = (AS, )

    _properties = ('GeneralFreq-SP', 'GeneralFreq-RB')

    def __init__(self, devname=None):
        """."""
        if devname is None:
            devname = RFGen.DEVICES.AS

        # check if device exists
        if devname not in RFGen.DEVICES.ALL:
            raise NotImplementedError(devname)

        # call base class constructor
        super().__init__(devname, properties=RFGen._properties)

    @property
    def frequency(self):
        """."""
        return self['GeneralFreq-RB']

    @frequency.setter
    def frequency(self, value):
        delta_max = RFGen.RF_DELTA_RMP  # [Hz]
        freq0 = self['GeneralFreq-SP']
        if freq0 is None or value is None:
            return
        delta = abs(value-freq0)
        if delta < RFGen.RF_DELTA_MIN or delta > RFGen.RF_DELTA_MAX:
            return
        npoints = int(round(delta/delta_max)) + 2
        freq_span = _np.linspace(freq0, value, npoints)[1:]
        for freq in freq_span:
            self._pvs['GeneralFreq-SP'].put(freq, wait=False)
            _time.sleep(1.0)
        self['GeneralFreq-SP'] = value


class RFLL(_DeviceNC):
    """."""

    class DEVICES:
        """Devices names."""

        BO = 'BR-RF-DLLRF-01'
        SI = 'SR-RF-DLLRF-01'
        ALL = (BO, SI)

    _properties = (
        'PL:REF:S', 'SL:INP:PHS',
        'mV:AL:REF:S', 'SL:REF:AMP',
        'RmpPhsBot-SP', 'RmpPhsBot-RB',
        'RmpPhsTop-SP', 'RmpPhsTop-RB')

    def __init__(self, devname, is_cw=None):
        """."""
        # check if device exists
        if devname not in RFLL.DEVICES.ALL:
            raise NotImplementedError(devname)

        # set is_cw
        self._is_cw = RFLL._set_is_cw(devname, is_cw)

        # call base class constructor
        super().__init__(devname, properties=RFLL._properties)

    @property
    def is_cw(self):
        """."""
        return self._is_cw

    @property
    def phase(self):
        """."""
        if self._is_cw:
            return self['SL:INP:PHS']
        return self['RmpPhsBot-RB']

    @phase.setter
    def phase(self, value):
        """."""
        if self._is_cw:
            self['PL:REF:S'] = value
        else:
            self['RmpPhsBot-SP'] = value
            self['RmpPhsTop-SP'] = value

    @property
    def voltage(self):
        """."""
        return self['SL:REF:AMP']

    @voltage.setter
    def voltage(self, value):
        self['mV:AL:REF:S'] = value

    # --- private methods ---

    @staticmethod
    def _set_is_cw(devname, is_cw):
        defcw = (devname == RFLL.DEVICES.BO)
        value = defcw if is_cw is None else is_cw
        return value


class RFPowMon(_DeviceNC):
    """."""

    class DEVICES:
        """Devices names."""

        BO = 'BO-05D:RF-P5Cav'
        SI = 'RA-RaSIA01:RF-LLRFCalSys'
        ALL = (BO, SI)

    _properties = {
        DEVICES.SI: ('PwrW1-Mon', ),
        DEVICES.BO: ('Cell3PwrTop-Mon', 'Cell3Pwr-Mon')}

    def __init__(self, devname, is_cw=None):
        """."""
        # check if device exists
        if devname not in RFPowMon.DEVICES.ALL:
            raise NotImplementedError(devname)

        # set is_cw
        self._is_cw = self._set_is_cw(devname, is_cw)

        # call base class constructor
        super().__init__(devname, properties=RFPowMon._properties[devname])

    @property
    def is_cw(self):
        """."""
        return self._is_cw

    @property
    def power(self):
        """."""
        if self._devname == RFPowMon.DEVICES.BO:
            if self.is_cw:
                return self['Cell3PwrTop-Mon']
            return self['Cell3Pwr-Mon']
        return self['PwrW1-Mon']

    # --- private methods ---

    @staticmethod
    def _set_is_cw(devname, is_cw):
        defcw = (devname == RFPowMon.DEVICES.BO)
        value = defcw if is_cw is None else is_cw
        return value


class RFCav(_Devices):
    """."""

    class DEVICES:
        """Devices names."""

        BO = 'BO-05D:RF-P5Cav'
        SI = 'RA-RaSIA01:RF-LLRFCalSys'
        ALL = (BO, SI)

    def __init__(self, devname, is_cw=None):
        """."""
        # check if device exists
        if devname not in RFCav.DEVICES.ALL:
            raise NotImplementedError(devname)

        rfgen = RFGen()
        if devname == RFCav.DEVICES.SI:
            rfll = RFLL(RFLL.DEVICES.SI, is_cw)
            rfpowmon = RFPowMon(RFPowMon.DEVICES.SI, is_cw)
        elif devname == RFCav.DEVICES.BO:
            rfll = RFLL(RFLL.DEVICES.BO, is_cw)
            rfpowmon = RFPowMon(RFPowMon.DEVICES.SI, is_cw)
        devices = (rfgen, rfll, rfpowmon)

        # call base class constructor
        super().__init__(devname, devices)

    @property
    def is_cw(self):
        """."""
        return self.devices[0].is_cw

    @property
    def dev_rfgen(self):
        """Return RFGen device."""
        return self.devices[0]

    @property
    def dev_rfll(self):
        """Return RFLL device."""
        return self.devices[1]

    @property
    def dev_rfpowmon(self):
        """Return RFPoweMon device."""
        return self.devices[2]

    def cmd_set_voltage(self, value, timeout=10):
        """."""
        self.dev_rfll.voltage = value
        self._wait('voltage', timeout=timeout)

    def cmd_set_phase(self, value, timeout=10):
        """."""
        self.dev_rfll.phase = value
        self._wait('phase', timeout=timeout)

    def cmd_set_frequency(self, value, timeout=10):
        """."""
        self.dev_rfgen.frequency = value
        self._wait('frequency', timeout=timeout)

    # --- private methods ---

    def _wait(self, propty, timeout=10):
        """."""
        nrp = int(timeout / 0.1)
        for _ in range(nrp):
            _time.sleep(0.1)
            if propty == 'phase':
                if self.is_cw:
                    phase_sp = self.dev_rfll['PL:REF:S']
                else:
                    phase_sp = self.dev_rfll['RmpPhsBot-SP']
                if abs(self.dev_rfll.phase - phase_sp) < 0.1:
                    break
            elif propty == 'voltage':
                voltage_sp = self.dev_rfll['mV:AL:REF:S']
                if abs(self.dev_rfll.voltage - voltage_sp) < 0.1:
                    break
            elif propty == 'frequency':
                freq_sp = self.dev_rfgen['GeneralFreq-SP']
                if abs(self.dev_rfgen.frequency - freq_sp) < 0.1:
                    break
            else:
                raise Exception(
                    'Set RF property (phase, voltage or frequency)')

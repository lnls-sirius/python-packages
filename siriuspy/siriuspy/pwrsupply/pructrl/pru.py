"""Module implementing PRU elements."""
import time as _time


from ... import csdev as _csdev


class PRUInterface:
    """Interface class for programmable real-time units."""

    OK = 0

    def __init__(self):
        """Init method."""
        self._timestamp_write = _time.time()
        self._timestamp_read = self._timestamp_write
        self._wr_duration = 0.0

    # --- public interface ---

    @property
    def wr_duration(self):
        """Return write-read accumulated duration."""
        return self._wr_duration

    def wr_duration_reset(self):
        """Reset write/read accumulated duration."""
        self._wr_duration = 0.0

    def UART_write(self, stream, timeout):
        """Write stream to serial port."""
        self._timestamp_write = _time.time()
        ret = self._UART_write(stream, timeout=timeout)
        return ret

    def UART_read(self):
        """Return read from UART."""
        value = self._UART_read()
        self._timestamp_read = _time.time()
        self._wr_duration += self._timestamp_read - self._timestamp_write
        return value

    def close(self):
        """Close PRU session."""
        self._close()
        return None

    # --- pure virtual methods ---

    def _UART_write(self, stream, timeout):
        raise NotImplementedError

    def _UART_read(self):
        raise NotImplementedError

    def _close(self):
        raise NotImplementedError


class PRU(PRUInterface):
    """Functions for the programmable real-time unit."""

    def __init__(self, ethbridgeclnt_class, bbbname=None, ip_address=None):
        """Init method."""
        # if ip address was not given, get it from bbbname
        if ip_address is None:
            dev2ips = _csdev.get_device_2_ioc_ip()
            ip_address = dev2ips[bbbname]
        print('BEAGLEBONE: ', bbbname)
        print('IP_ADDRESS: ', ip_address)

        # start communication threads
        self._ethbrigde = ethbridgeclnt_class(
            ip_address=ip_address, use_general=False)
        self._ethbrigde.threads_start()

        # print prulib version
        # fmtstr = 'PRUserial485 lib version_{}: {}'
        # print(fmtstr.format('client', self.version))
        # print(fmtstr.format('server', self.version_server))
        # print()

        # init PRUserial485 interface
        PRUInterface.__init__(self)

        # NOTE: open is done automatically by eth-brigde server
        # and cannot be used when use_general = False
        #
        # start PRU library and set PRU to sync off
        # baud_rate = 6
        # mode = b"M"  # "S": slave | "M": master
        # ret = self._ethbrigde.open(baud_rate, mode)
        # if ret != PRUInterface.OK:
        #     raise ValueError(('Error {} returned in '
        #                       'PRUserial485_open').format(ret))

    def _UART_write(self, stream, timeout):
        # this method send streams through UART to the RS-485 line.
        ret = self._ethbrigde.write(stream, timeout)
        return ret

    def _UART_read(self):
        # this method send streams through UART to the RS-485 line.
        value = self._ethbrigde.read()
        return value

    def _close(self):
        # self._ethbrigde.close()
        return None

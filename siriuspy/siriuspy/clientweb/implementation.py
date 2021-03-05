"""Implementation of web server data retrieval functions."""
import re as _re
import urllib.request as _urllib_request

from .. import envars as _envars


_TIMEOUT = 5.0  # [seconds]
_EXCDAT_FOLDER = '/magnet/excitation-data/'
_MAGNET_FOLDER = '/magnet/'
_PS_FOLDER = '/pwrsupply/'
_BBB_FOLDER = '/beaglebone/'
_PSTYPES_DATA_FOLDER = '/pwrsupply/pstypes-data/'
_DIAG_FOLDER = '/diagnostics/'
_TIMESYS_FOLDER = '/timesys/'
_MAC_SCHEDULE_FOLDER = '/macschedule/'


def read_url(url, timeout=_TIMEOUT):
    """Read URL from server."""

    # build list with servers
    urls = [_envars.SRVURL_CSCONSTS + url, _envars.SRVURL_CSCONSTS_2 + url]
    connected = False
    for url_ in urls:
        try:
            # try a new server
            response = _urllib_request.urlopen(url_, timeout=timeout)
            data = response.read()
            text = data.decode('utf-8')
            connected = True
            break
        except Exception:
            # could not connect with current server
            print('Error reading url "' + url_ + '"!')
    if not connected:
        raise Exception('Error reading web servers!')
    return text


def server_online():
    """Verify if the server is online."""
    try:
        read_url('', timeout=_TIMEOUT)
        return True
    except Exception:
        return False


def magnets_model_data(timeout=_TIMEOUT):
    """Return the text of the retrieved magnet model data."""
    url = _MAGNET_FOLDER + 'magnets-model-data.txt'
    return read_url(url, timeout=timeout)


def magnets_excitation_data_read(filename, timeout=_TIMEOUT):
    """Return the text of the retrieved magnet excitation data."""
    return read_url(_EXCDAT_FOLDER + filename, timeout=timeout)


def magnets_excitation_ps_read(timeout=_TIMEOUT):
    """Return the power supply excitation data."""
    url = _MAGNET_FOLDER + 'magnet-excitation-ps.txt'
    return read_url(url, timeout=timeout)


def ps_pstypes_names_read(timeout=_TIMEOUT):
    """Return the text of the power supplies type."""
    url = _PS_FOLDER + 'pstypes-names.txt'
    return read_url(url, timeout=timeout)


def ps_pstype_data_read(filename, timeout=_TIMEOUT):
    """Return the power supply data."""
    url = _PSTYPES_DATA_FOLDER + filename
    return read_url(url, timeout=timeout)


def ps_pstype_setpoint_limits(timeout=_TIMEOUT):
    """Return the power supply setpoint limits data."""
    url = _PS_FOLDER + 'pstypes-setpoint-limits.txt'
    return read_url(url, timeout=timeout)


def pu_pstype_setpoint_limits(timeout=_TIMEOUT):
    """Return the power supply setpoint limits data."""
    url = _PS_FOLDER + 'putypes-setpoint-limits.txt'
    return read_url(url, timeout=timeout)


def ps_psmodels_read(timeout=_TIMEOUT):
    """Return the psmodels file."""
    url = _PS_FOLDER + 'psmodels.txt'
    return read_url(url, timeout=timeout)


def ps_siggen_configuration_read(timeout=_TIMEOUT):
    """Return power supplies signal default generation configuration."""
    url = _PS_FOLDER + 'siggen-configuration.txt'
    return read_url(url, timeout=timeout)


def pu_psmodels_read(timeout=_TIMEOUT):
    """Return the pumodels file."""
    url = _PS_FOLDER + 'pumodels.txt'
    return read_url(url, timeout=timeout)


def beaglebone_freq_mapping(timeout=_TIMEOUT):
    """Return the beaglebone Black BSMP PRU sync off and on freqs."""
    url = _BBB_FOLDER + 'beaglebone-freq.txt'
    return read_url(url, timeout=timeout)


def beaglebone_ip_list(timeout=_TIMEOUT):
    """Return the beaglebone Black IP list."""
    url = _BBB_FOLDER + 'ip-list.txt'
    return read_url(url, timeout=timeout)


def bbb_udc_mapping(timeout=_TIMEOUT):
    """Read beaglebone-udc mapping."""
    url = _BBB_FOLDER + 'beaglebone-udc.txt'
    return read_url(url, timeout=timeout)


def udc_ps_mapping(timeout=_TIMEOUT):
    """Read beaglebone-udc mapping."""
    url = _BBB_FOLDER + 'udc-bsmp.txt'
    return read_url(url, timeout=timeout)


def crates_mapping(timeout=_TIMEOUT):
    """Return the crates mapping."""
    url = _DIAG_FOLDER + 'microTCA-vs-BPMs-mapping/'
    text = read_url(url, timeout=timeout)
    pat = _re.compile('>(names.crate[a-zA-Z_0-9]*.cfg)<')
    files = pat.findall(text)
    txt = ''
    for fi in files:
        for time in read_url(url + fi, timeout=timeout).splitlines():
            txt += '{0:20s}'.format(fi[6:13]) + time + '\n'
        txt += '\n\n'
    return txt


def bpms_data(timeout=_TIMEOUT):
    """Return the BPMs data."""
    url = _DIAG_FOLDER + 'bpms-data.txt'
    return read_url(url, timeout=timeout)


def timing_devices_mapping(timeout=_TIMEOUT):
    """Return the timing devices connections mapping."""
    url = _TIMESYS_FOLDER + 'timing-devices-connection.txt'
    return read_url(url, timeout=timeout)


def high_level_triggers(timeout=_TIMEOUT):
    """Return the data defining the high level triggers."""
    url = _TIMESYS_FOLDER + 'high-level-triggers.py'
    return read_url(url, timeout=timeout)


def high_level_events(timeout=_TIMEOUT):
    """Return the data defining the high level events."""
    url = _TIMESYS_FOLDER + 'high-level-events.py'
    return read_url(url, timeout=timeout)


def bsmp_dclink_mapping(timeout=_TIMEOUT):
    """Read bsmp dclink mapping."""
    url = _PS_FOLDER + 'bsmp-dclink.txt'
    return read_url(url, timeout=timeout)


def mac_schedule_read(year, timeout=_TIMEOUT):
    """Read machine schedule data."""
    url = _MAC_SCHEDULE_FOLDER + str(year) + '.txt'
    return read_url(url, timeout=timeout)

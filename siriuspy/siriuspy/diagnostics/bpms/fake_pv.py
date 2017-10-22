#!/usr/bin/env python
#  M Newville <newville@cars.uchicago.edu>
#  The University of Chicago, 2010
#  Epics Open License

"""
  Epics Process Variable
"""
import sys
import time
import ctypes
from random import randint as _randint
import copy
from math import log10
import numpy as _np

from epics import dbr
from epics.ca import DEFAULT_CONNECTION_TIMEOUT
from epics.ca import AUTOMONITOR_MAXLENGTH
from epics.ca import HAS_NUMPY

_PVcache_ = {}

_PYTYPES = {'float': float, 'int': int, 'bool': int,
            'string': str, 'enum': int, 'char': str}
_CATYPES = {'float': dbr.DOUBLE, 'int': dbr.LONG, 'bool': dbr.INT,
            'string': dbr.STRING, 'enum': dbr.ENUM, 'char': dbr.STRING}

_database = dict()


def add_to_database(db):
    _database.update(copy.deepcopy(db))


def clear_database():
    _database.clear()


def fmt_time(tstamp=None):
    "simple formatter for time values"
    if tstamp is None:
        tstamp = time.time()
    tstamp, frac = divmod(tstamp, 1)
    return "%s.%5.5i" % (time.strftime("%Y-%m-%d %H:%M:%S",
                                       time.localtime(tstamp)),
                         round(1.e5*frac))


def promote_type(tp, use_time=False, use_ctrl=False):
    """promotes the native field type of a ``chid`` to its TIME or CTRL variant.
    Returns the integer corresponding to the promoted field value."""
    ftype = _CATYPES[tp]
    print(ftype, tp)
    if use_ctrl:
        ftype += dbr.CTRL_STRING
    elif use_time:
        ftype += dbr.TIME_STRING
    if ftype == dbr.CTRL_STRING:
        ftype = dbr.TIME_STRING
    return ftype


def write(msg, newline=True, flush=True):
    """write message to stdout"""
    sys.stdout.write(msg)
    if newline:
        sys.stdout.write("\n")
    if flush:
        sys.stdout.flush()


class PVFake(object):
    """Fake Epics Process Variable

    A PV encapsulates an Epics Process Variable.

    The primary interface methods for a pv are to get() and put() is value::

      >>> p = PV(pv_name)  # create a pv object given a pv name
      >>> p.get()          # get pv value
      >>> p.put(val)       # set pv to specified value.

    Additional important attributes include::

      >>> p.pvname         # name of pv
      >>> p.value          # pv value (can be set or get)
      >>> p.char_value     # string representation of pv value
      >>> p.count          # number of elements in array pvs
      >>> p.type           # EPICS data type: 'string','double','enum','long',..
"""

    _fmtsca = "<PV '%(pvname)s', count=%(count)i, type=%(typefull)s, access=%(access)s>"
    _fmtarr = "<PV '%(pvname)s', count=%(count)i/%(nelm)i, type=%(typefull)s, access=%(access)s>"
    _fields = ('pvname',  'value',  'char_value',  'status',  'ftype',  'chid',
               'host', 'count', 'access', 'write_access', 'read_access',
               'severity', 'timestamp', 'posixseconds', 'nanoseconds',
               'precision', 'units', 'enum_strs',
               'upper_disp_limit', 'lower_disp_limit', 'upper_alarm_limit',
               'lower_alarm_limit', 'lower_warning_limit',
               'upper_warning_limit', 'upper_ctrl_limit', 'lower_ctrl_limit')

    def __init__(self, pvname, callback=None, form='time',
                 verbose=False, auto_monitor=None, count=None,
                 connection_callback=None,
                 connection_timeout=None,
                 access_callback=None):
        db = _database.get(pvname)
        if db is None:
            raise Exception(
                'PV not existent in local database. Configure database ' +
                'first with add_to_database module function.')
        self.pvname = pvname.strip()
        self.form = form.lower()
        self.verbose = verbose
        self.auto_monitor = auto_monitor
        self.ftype = None
        self.connected = False
        self.connection_timeout = connection_timeout
        if self.connection_timeout is None:
            self.connection_timeout = DEFAULT_CONNECTION_TIMEOUT
        self._args = {}.fromkeys(self._fields)
        self._args['pvname'] = self.pvname
        self._args['value'] = db.get('value', '' if db['type'] == 'str' else 0)
        self._args['count'] = count
        self._args['nelm'] = db.get('count', 1)
        self._args['type'] = 'unknown'
        self._args['typefull'] = 'unknown'
        self._args['access'] = 'unknown'
        self._args['severity'] = 0  # not simulated correctly
        self._args['status'] = 1  # not simulated correctly
        self._args['precision'] = db.get('prec')
        self._args['units'] = db.get('unit')
        self._args['upper_disp_limit'] = db.get('hilim')
        self._args['upper_disp_limit'] = db.get('lolim')
        self._args['upper_alarm_limit'] = db.get('high')
        self._args['upper_alarm_limit'] = db.get('low')
        self._args['upper_warning_limit'] = db.get('hihi')
        self._args['upper_warning_limit'] = db.get('lolo')
        self._args['upper_ctrl_limit'] = db.get('hilim')
        self._args['upper_ctrl_limit'] = db.get('lolim')

        self.context = dbr.ECA_NORMAL

        self._pytype = _PYTYPES[db['type']]
        self.ftype = promote_type(db['type'],
                                  use_ctrl=self.form == 'ctrl',
                                  use_time=self.form == 'time')
        self._args['type'] = dbr.Name(self.ftype).lower()

        self._args['chid'] = dbr.chid_t(_randint(1, 10000000))
        self.__on_connect(pvname=pvname, chid=self._args['chid'])
        self.chid = self._args['chid']

        self.__on_access_rights_event(read_access=True, write_access=True)

        self.connection_callbacks = []
        if connection_callback is not None:
            self.connection_callbacks = [connection_callback]

        self.access_callbacks = []
        if access_callback is not None:
            self.access_callbacks = [access_callback]

        self.callbacks = {}
        self._conn_started = False
        if isinstance(callback, (tuple, list)):
            for i, thiscb in enumerate(callback):
                if hasattr(thiscb, '__call__'):
                    self.callbacks[i] = (thiscb, {})
        elif hasattr(callback, '__call__'):
            self.callbacks[0] = (callback, {})

        pvid = (self.pvname, self.form, self.context)
        if pvid not in _PVcache_:
            _PVcache_[pvid] = self

    def force_connect(self, pvname=None, chid=None, conn=True, **kws):
        if chid is None:
            chid = self.chid
        if isinstance(chid, ctypes.c_long):
            chid = chid.value
        self._args['chid'] = self.chid = chid
        self.__on_connect(pvname=pvname, chid=chid, conn=conn, **kws)

    def force_read_access_rights(self):
        """force a read of access rights, not relying
        on last event callback.
        Note: event callback seems to fail sometimes,
        at least on initial connection on Windows 64-bit.
        """
        pass

    def __on_access_rights_event(self, read_access, write_access):
        self._args['read_access'] = read_access
        self._args['write_access'] = write_access

        acc = read_access + 2 * write_access
        access_strs = ('no access', 'read-only', 'write-only', 'read/write')
        self._args['access'] = access_strs[acc]

        for cb in self.access_callbacks:
            if callable(cb):
                cb(read_access, write_access, pv=self)

    def __on_connect(self, pvname=None, chid=None, conn=True):
        "callback for connection events"
        # occassionally chid is still None (ie if a second PV is created
        # while __on_connect is still pending for the first one.)
        # Just return here, and connection will happen later
        t0 = time.time()
        if conn:
            self.chid = self._args['chid'] = dbr.chid_t(chid.value)

            # allow reduction of elements, via count argument
            count = self._args['nelm']
            if self._args['count'] is not None:
                count = min(count, self._args['count'])
                self._args['count'] = count

            self._args['host'] = 'localhost:00000'

            _ftype_ = dbr.Name(self.ftype).lower()
            print(_ftype_, self.ftype)
            self._args['type'] = _ftype_
            self._args['typefull'] = _ftype_
            self._args['ftype'] = dbr.Name(_ftype_, reverse=True)

            if self.auto_monitor is None:
                self.auto_monitor = count < AUTOMONITOR_MAXLENGTH

        for conn_cb in self.connection_callbacks:
            if hasattr(conn_cb, '__call__'):
                conn_cb(pvname=self.pvname, conn=conn, pv=self)
            elif not conn and self.verbose:
                write("PV '%s' disconnected." % pvname)

        # pv end of connect, force a read of access rights
        self.force_read_access_rights()

        # waiting until the very end until to set self.connected prevents
        # threads from thinking a connection is complete when it is actually
        # still in progress.
        self.connected = conn
        return

    def wait_for_connection(self, timeout=None):
        """wait for a connection that started with connect() to finish"""

        if not self.connected:
            start_time = time.time()
            if not self._conn_started:
                self.connect()

            if not self.connected:
                if timeout is None:
                    timeout = self.connection_timeout
                while not self.connected and time.time()-start_time < timeout:
                    time.sleep(0.1)
        return self.connected

    def connect(self, timeout=None):
        "check that a PV is connected, forcing a connection if needed"
        if not self.connected:
            if timeout is None:
                timeout = self.connection_timeout
        self._conn_started = True
        return self.connected and self.ftype is not None

    def clear_auto_monitor(self):
        """turn off auto-monitoring: must reconnect to re-enable monitoring"""
        self.auto_monitor = False

    def reconnect(self):
        "try to reconnect PV"
        self.auto_monitor = None
        self.connected = False
        self._conn_started = False
        self.force_connect()
        return self.wait_for_connection()

    def poll(self, evt=1.e-4, iot=1.0):
        "poll for changes"
        pass

    def get(self, count=None, as_string=False, as_numpy=True,
            timeout=None, with_ctrlvars=False, use_monitor=True):
        """returns current value of PV.  Use the options:
        count       explicitly limit count for array data
        as_string   flag(True/False) to get a string representation
                    of the value.
        as_numpy    flag(True/False) to use numpy array as the
                    return type for array data.
        timeout     maximum time to wait for value to be received.
                    (default = 0.5 + log10(count) seconds)
        use_monitor flag(True/False) to use value from latest
                    monitor callback (True, default) or to make an
                    explicit CA call for the value.

        >>> p.get('13BMD:m1.DIR')
        0
        >>> p.get('13BMD:m1.DIR', as_string=True)
        'Pos'
        """
        if not self.wait_for_connection(timeout=timeout):
            return None
        if with_ctrlvars and getattr(self, 'units', None) is None:
            self.get_ctrlvars()

        val = self._args['value']
        if as_string:
            return self._set_charval(val)
        if self.count <= 1 or val is None:
            return val

        # After this point:
        #   * self.count is > 1
        #   * val should be set and a sequence
        try:
            len(val)
        except TypeError:
            # Edge case where a scalar value leaks through ca.unpack()
            val = [val]

        if count is None:
            count = len(val)

        if (as_numpy and HAS_NUMPY and
                not isinstance(val, _np.ndarray)):
            val = _np.asarray(val)
        elif (not as_numpy and HAS_NUMPY and
                isinstance(val, _np.ndarray)):
            val = val.tolist()
        # allow asking for less data than actually exists in the cached value
        if count < len(val):
            val = val[:count]
        return val

    def put(self, value, wait=False, timeout=30.0,
            use_complete=False, callback=None, callback_data=None):
        """set value for PV, optionally waiting until the processing is
        complete, and optionally specifying a callback function to be run
        when the processing is complete.
        """
        if not self.wait_for_connection():
            return None

        if value is None:
            return None
        elif (self.ftype in (dbr.ENUM, dbr.TIME_ENUM, dbr.CTRL_ENUM) and
              isinstance(value, str)):
            if self._args['enum_strs'] is None:
                self.get_ctrlvars()
            if value in self._args['enum_strs']:
                # tuple.index() not supported in python2.5
                # value = self._args['enum_strs'].index(value)
                for ival, val in enumerate(self._args['enum_strs']):
                    if val == value:
                        value = ival
                        break
        elif not isinstance(value, self._pytype):
            try:
                value = self._pytype(value)
            except Exception:
                return None
        if use_complete and callback is None:
            callback = self.__putCallbackStub
        self.__on_changes(value=value)
        callback(**callback_data) if callback_data else callback()

    def __putCallbackStub(self, pvname=None, **kws):
        "null put-calback, so that the put_complete attribute is valid"
        pass

    def _set_charval(self, val, call_ca=True):
        """ sets the character representation of the value.
        intended only for internal use"""
        if val is None:
            self._args['char_value'] = 'None'
            return 'None'
        ftype = self._args['ftype']
        ntype = dbr.native_type(ftype)
        if ntype == dbr.STRING:
            self._args['char_value'] = val
            return val
        # char waveform as string
        if ntype == dbr.CHAR and self.count < AUTOMONITOR_MAXLENGTH:
            if HAS_NUMPY and isinstance(val, _np.ndarray):
                # a numpy array
                val = val.tolist()

                if not isinstance(val, list):
                    # a scalar value from numpy, tolist() turns it into a
                    # native python integer
                    val = [val.tolist()]
            else:
                try:
                    # otherwise, try forcing it into a list. this will fail for
                    # scalar types
                    val = list(val)
                except TypeError:
                    # and when it fails, make it a list of one scalar value
                    val = [val]

            if 0 in val:
                firstnull = val.index(0)
            else:
                firstnull = len(val)
            try:
                cval = ''.join([chr(i) for i in val[:firstnull]]).rstrip()
            except ValueError:
                cval = ''
            self._args['char_value'] = cval
            return cval

        cval = repr(val)
        if self.count > 1:
            try:
                length = len(val)
            except TypeError:
                length = 1
            cval = '<array size=%d, type=%s>' % (length,
                                                 dbr.Name(ftype).lower())
        elif ntype in (dbr.FLOAT, dbr.DOUBLE):
            if call_ca and self._args['precision'] is None:
                self.get_ctrlvars()
            try:
                prec = self._args['precision']
                fmt = "%%.%if"
                if 4 < abs(int(log10(abs(val + 1.e-9)))):
                    fmt = "%%.%ig"
                cval = (fmt % prec) % val
            except (ValueError, TypeError, ArithmeticError):
                cval = str(val)
        elif ntype == dbr.ENUM:
            if call_ca and self._args['enum_strs'] in ([], None):
                self.get_ctrlvars()
            try:
                cval = self._args['enum_strs'][val]
            except (TypeError, KeyError,  IndexError):
                cval = str(val)

        self._args['char_value'] = cval
        return cval

    def get_ctrlvars(self, timeout=5, warn=True):
        "get control values for variable"
        if not self.wait_for_connection():
            return None
        kwds = dict()
        for key in ('precision', 'units', 'severity', 'status',
                    'upper_disp_limit', 'lower_disp_limit',
                    'upper_alarm_limit', 'upper_warning_limit',
                    'lower_warning_limit', 'lower_alarm_limit',
                    'upper_ctrl_limit', 'lower_ctrl_limit'):
            if self._args[key] is not None:
                kwds[key] = self._args[key]

        self.force_read_access_rights()
        return kwds

    def get_timevars(self, timeout=5, warn=True):
        "get time values for variable"
        if not self.wait_for_connection():
            return None
        kwds = dict()
        for key in ('status', 'severity', 'timestamp'):
            if self._args[key] is not None:
                kwds[key] = self._args[key]
        return kwds

    def __on_changes(self, value=None, **kwd):
        """internal callback function: do not overwrite!!
        To have user-defined code run when the PV value changes,
        use add_callback()
        """
        self._args.update(kwd)
        self._args['value'] = value
        self._args['timestamp'] = time.time()
        self._args['posixseconds'] = 0
        self._args['nanoseconds'] = 0
        self._set_charval(self._args['value'], call_ca=False)
        if self.verbose:
            now = fmt_time(self._args['timestamp'])
            write('%s: %s (%s)' % (self.pvname,
                                   self._args['char_value'], now))
        self.run_callbacks()

    def run_callbacks(self):
        """run all user-defined callbacks with the current data

        Normally, this is to be run automatically on event, but
        it is provided here as a separate function for testing
        purposes.
        """
        for index in sorted(list(self.callbacks.keys())):
            self.run_callback(index)

    def run_callback(self, index):
        """run a specific user-defined callback, specified by index,
        with the current data
        Note that callback functions are called with keyword/val
        arguments including:
             self._args  (all PV data available, keys = __fields)
             keyword args included in add_callback()
             keyword 'cb_info' = (index, self)
        where the 'cb_info' is provided as a hook so that a callback
        function  that fails may de-register itself (for example, if
        a GUI resource is no longer available).
        """
        try:
            fcn, kwargs = self.callbacks[index]
        except KeyError:
            return
        kwd = copy.copy(self._args)
        kwd.update(kwargs)
        kwd['cb_info'] = (index, self)
        if hasattr(fcn, '__call__'):
            fcn(**kwd)

    def add_callback(self, callback=None, index=None, run_now=False,
                     with_ctrlvars=True, **kw):
        """add a callback to a PV.  Optional keyword arguments
        set here will be preserved and passed on to the callback
        at runtime.

        Note that a PV may have multiple callbacks, so that each
        has a unique index (small integer) that is returned by
        add_callback.  This index is needed to remove a callback."""
        if hasattr(callback, '__call__'):
            if index is None:
                index = 1
                if len(self.callbacks) > 0:
                    index = 1 + max(self.callbacks.keys())
            self.callbacks[index] = (callback, kw)

        if with_ctrlvars and self.connected:
            self.get_ctrlvars()
        if run_now:
            self.get(as_string=True)
            if self.connected:
                self.run_callback(index)
        return index

    def remove_callback(self, index=None):
        """remove a callback by index"""
        if index in self.callbacks:
            self.callbacks.pop(index)

    def clear_callbacks(self):
        "clear all callbacks"
        self.callbacks = {}

    def _getinfo(self):
        "get information paragraph"
        if not self.wait_for_connection():
            return None
        self.get_ctrlvars()
        out = []
        mod = 'native'
        xtype = self._args['typefull']
        if '_' in xtype:
            mod, xtype = xtype.split('_')

        fmt = '%i'
        if   xtype in ('float','double'):
            fmt = '%g'
        elif xtype in ('string','char'):
            fmt = '%s'

        self._set_charval(self._args['value'], call_ca=False)
        out.append("== %s  (%s_%s) ==" % (self.pvname, mod, xtype))
        if self.count == 1:
            val = self._args['value']
            out.append('   value      = %s' % fmt % val)
        else:
            ext = {True: '...', False: ''}[self.count > 10]
            elems = range(min(5, self.count))
            try:
                aval = [fmt % self._args['value'][i] for i in elems]
            except TypeError:
                aval = ('unknown',)
            out.append("   value      = array  [%s%s]" % (",".join(aval), ext))
        for nam in ('char_value', 'count', 'nelm', 'type', 'units',
                    'precision', 'host', 'access',
                    'status', 'severity', 'timestamp',
                    'posixseconds', 'nanoseconds',
                    'upper_ctrl_limit', 'lower_ctrl_limit',
                    'upper_disp_limit', 'lower_disp_limit',
                    'upper_alarm_limit', 'lower_alarm_limit',
                    'upper_warning_limit', 'lower_warning_limit'):
            if hasattr(self, nam):
                att = getattr(self, nam)
                if att is not None:
                    if nam == 'timestamp':
                        att = "%.3f (%s)" % (att, fmt_time(att))
                    elif nam == 'char_value':
                        att = "'%s'" % att
                    if len(nam) < 12:
                        out.append('   %.11s= %s' % (nam+' '*12, str(att)))
                    else:
                        out.append('   %.20s= %s' % (nam+' '*20, str(att)))
        if xtype == 'enum':  # list enum strings
            out.append('   enum strings: ')
            for index, nam in enumerate(self.enum_strs):
                out.append("       %i = %s " % (index, nam))

        if self.auto_monitor is not None:
            msg = 'PV is internally monitored'
            out.append('   %s, with %i user-defined callbacks:' % (
                                                         msg,
                                                         len(self.callbacks)))
            if len(self.callbacks) > 0:
                for nam in sorted(self.callbacks.keys()):
                    cback = self.callbacks[nam][0]
                    out.append('      %s in file %s' % (
                                        cback.func_name,
                                        cback.func_code.co_filename))
        else:
            out.append('   PV is NOT internally monitored')
        out.append('=============================')
        return '\n'.join(out)

    def _getarg(self, arg):
        "wrapper for property retrieval"
        if self._args['value'] is None:
            self.get()
        if self._args[arg] is None:
            if arg in ('status', 'severity', 'timestamp',
                       'posixseconds', 'nanoseconds'):
                self.get_timevars(timeout=1, warn=False)
            else:
                self.get_ctrlvars(timeout=1, warn=False)
        return self._args.get(arg, None)

    def __getval__(self):
        "get value"
        return self._getarg('value')

    def __setval__(self, val):
        "put-value"
        return self.put(val)

    value = property(__getval__, __setval__, None, "value property")

    @property
    def char_value(self):
        "character string representation of value"
        return self._getarg('char_value')

    @property
    def status(self):
        "pv status"
        return self._getarg('status')

    @property
    def type(self):
        "pv type"
        return self._args['type']

    @property
    def typefull(self):
        "pv type"
        return self._args['typefull']

    @property
    def host(self):
        "pv host"
        return self._getarg('host')

    @property
    def count(self):
        """count (number of elements). For array data and later EPICS versions,
        this is equivalent to the .NORD field.  See also 'nelm' property"""
        if self._args['count'] is not None:
            return self._args['count']
        else:
            return self._getarg('count')

    @property
    def nelm(self):
        """native count (number of elements).
        For array data this will return the full array size (ie, the
        .NELM field).  See also 'count' property"""
        if self._getarg('count') == 1:
            return 1
        return self._getarg('nelm')

    @property
    def read_access(self):
        "read access"
        return self._getarg('read_access')

    @property
    def write_access(self):
        "write access"
        return self._getarg('write_access')

    @property
    def access(self):
        "read/write access as string"
        return self._getarg('access')

    @property
    def severity(self):
        "pv severity"
        return self._getarg('severity')

    @property
    def timestamp(self):
        "timestamp of last pv action"
        return self._getarg('timestamp')

    @property
    def posixseconds(self):
        """integer seconds for timestamp of last pv action
        using POSIX time convention"""
        return self._getarg('posixseconds')

    @property
    def nanoseconds(self):
        "integer nanoseconds for timestamp of last pv action"
        return self._getarg('nanoseconds')

    @property
    def precision(self):
        "number of digits after decimal point"
        return self._getarg('precision')

    @property
    def units(self):
        "engineering units for pv"
        return self._getarg('units')

    @property
    def enum_strs(self):
        "list of enumeration strings"
        return self._getarg('enum_strs')

    @property
    def upper_disp_limit(self):
        "limit"
        return self._getarg('upper_disp_limit')

    @property
    def lower_disp_limit(self):
        "limit"
        return self._getarg('lower_disp_limit')

    @property
    def upper_alarm_limit(self):
        "limit"
        return self._getarg('upper_alarm_limit')

    @property
    def lower_alarm_limit(self):
        "limit"
        return self._getarg('lower_alarm_limit')

    @property
    def lower_warning_limit(self):
        "limit"
        return self._getarg('lower_warning_limit')

    @property
    def upper_warning_limit(self):
        "limit"
        return self._getarg('upper_warning_limit')

    @property
    def upper_ctrl_limit(self):
        "limit"
        return self._getarg('upper_ctrl_limit')

    @property
    def lower_ctrl_limit(self):
        "limit"
        return self._getarg('lower_ctrl_limit')

    @property
    def info(self):
        "info string"
        return self._getinfo()

    @property
    def put_complete(self):
        "returns True if a put-with-wait has completed"
        return True

    def __repr__(self):
        "string representation"

        if self.connected:
            if self.count == 1:
                return self._fmtsca % self._args
            else:
                return self._fmtarr % self._args
        else:
            return "<PV '%s': not connected>" % self.pvname

    def __eq__(self, other):
        "test for equality"
        try:
            return (self.chid == other.chid)
        except AttributeError:
            return False

    def disconnect(self):
        "disconnect PV"
        self.connected = False
        pvid = (self.pvname, self.form, self.context)
        if pvid in _PVcache_:
            _PVcache_.pop(pvid)

        if self.auto_monitor:
            self._args = {}.fromkeys(self._fields)

        self.callbacks = {}

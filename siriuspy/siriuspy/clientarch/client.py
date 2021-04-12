#!/usr/bin/env python-sirius
"""Fetcher module.

See https://slacmshankar.github.io/epicsarchiver_docs/userguide.html
"""

from urllib import parse as _parse
import asyncio
from aiohttp import ClientSession
import urllib3 as _urllib3
import numpy as _np

from .. import envars as _envars


_TIMEOUT = 5.0  # [seconds]


class AuthenticationError(Exception):
    """."""


class ClientArchiver:
    """Archiver Data Fetcher class."""

    SERVER_URL = _envars.SRVURL_ARCHIVER
    ENDPOINT = '/mgmt/bpl'

    def __init__(self, server_url=None):
        """."""
        self.session = None
        self.timeout = _TIMEOUT
        self._url = server_url or self.SERVER_URL
        # print('urllib3 InsecureRequestWarning disabled!')
        _urllib3.disable_warnings(_urllib3.exceptions.InsecureRequestWarning)

    @property
    def connected(self):
        """."""
        # TODO: choose minimal request command in order to check connection.
        raise NotImplementedError

    def login(self, username, password):
        """Open login session."""
        headers = {"User-Agent": "Mozilla/5.0"}
        payload = {"username": username, "password": password}
        url = self._create_url(method='login')
        loop = asyncio.get_event_loop()
        self.session, authenticated = loop.run_until_complete(
            self.handle_login(
                url, headers=headers, payload=payload, ssl=False))
        if authenticated:
            print('Reminder: close connection after using this '
                  'session by calling close method!')
        else:
            self.close()
        return authenticated

    def close(self):
        """Close login session."""
        if self.session:
            loop = asyncio.get_event_loop()
            resp = loop.run_until_complete(self.close_session())
            self.session = None
            return resp
        return None

    def getPVsInfo(self, pvnames):
        """."""
        if isinstance(pvnames, (list, tuple)):
            pvnames = ','.join(pvnames)
        url = self._create_url(method='getPVStatus', pv=pvnames)
        resp = self._make_request(url, return_json=True)
        return None if not resp else resp

    def getAllPVs(self, pvnames):
        """."""
        if isinstance(pvnames, (list, tuple)):
            pvnames = ','.join(pvnames)
        url = self._create_url(method='getAllPVs', pv=pvnames, limit='-1')
        resp = self._make_request(url, return_json=True)
        return None if not resp else resp

    def deletePVs(self, pvnames):
        """."""
        if not isinstance(pvnames, (list, tuple)):
            pvnames = (pvnames, )
        for pvname in pvnames:
            url = self._create_url(
                method='deletePV', pv=pvname, deleteData='true')
            self._make_request(url, need_login=True)

    def getPausedPVsReport(self):
        """."""
        url = self._create_url(method='getPausedPVsReport')
        resp = self._make_request(url, return_json=True)
        return None if not resp else resp

    def pausePVs(self, pvnames):
        """."""
        if not isinstance(pvnames, (list, tuple)):
            pvnames = (pvnames, )
        for pvname in pvnames:
            url = self._create_url(method='pauseArchivingPV', pv=pvname)
            self._make_request(url, need_login=True)

    def renamePV(self, oldname, newname):
        """."""
        url = self._create_url(method='renamePV', pv=oldname, newname=newname)
        return self._make_request(url, need_login=True)

    def resumePVs(self, pvnames):
        """."""
        if not isinstance(pvnames, (list, tuple)):
            pvnames = (pvnames, )
        for pvname in pvnames:
            url = self._create_url(method='resumeArchivingPV', pv=pvname)
            self._make_request(url, need_login=True)

    def getData(self, pvname, timestamp_start, timestamp_stop,
                process_type='', interval=None, stddev=None,
                get_request_url=False):
        """Get archiver data.

        pvname -- name of pv.
        timestamp_start -- timestamp of interval start
                           Example: '2019-05-23T13:32:27.570Z'
        timestamp_stop -- timestamp of interval stop
                           Example: '2019-05-23T13:32:27.570Z'
        process_type -- data processing type to use. Can be:
                     '', 'mean', 'median', 'std', 'variance',
                     'popvariance', 'kurtosis', 'skewness'
                     'mini', 'maxi', 'jitter', 'count', 'ncount',
                     'firstSample', 'lastSample', 'firstFill', 'lastFill',
                     'nth', 'ignoreflyers' or 'flyers'
        interval -- interval of the bin of data, in seconds
        stddev -- number of standard deviations.
                  argument used in processing 'ignoreflyers' and 'flyers'.
        """
        if process_type:
            process_str = process_type
            if interval is not None:
                process_str += '_' + str(int(interval))
                if 'flyers' in process_type and stddev is not None:
                    process_str += '_' + str(int(stddev))
            pvname = process_str + '(' + pvname + ')'

        if isinstance(timestamp_start, str):
            timestamp_start = [timestamp_start, ]
        if isinstance(timestamp_stop, str):
            timestamp_stop = [timestamp_stop, ]

        if isinstance(timestamp_start, (list, tuple)) and \
                isinstance(timestamp_stop, (list, tuple)):
            if get_request_url:
                tstart = _parse.quote(timestamp_start[0])
                tstop = _parse.quote(timestamp_stop[-1])
                url = self._create_url(
                    method='getData.json', pv=pvname,
                    **{'from': tstart[0], 'to': tstop[-1]})
                return url

            urls = []
            for tstart, tstop in zip(timestamp_start, timestamp_stop):
                urls.append(self._create_url(
                    method='getData.json', pv=pvname,
                    **{'from': _parse.quote(tstart),
                       'to': _parse.quote(tstop)}))

            resps = self._make_request(urls, return_json=True)
            if any([not resp for resp in resps]):
                return None

            _ts, _vs, _st, _sv = [], [], [], []
            for resp in resps:
                data = resp[0]['data']
                _ts = _np.r_[_ts, [v['secs'] + v['nanos']/1.0e9 for v in data]]
                _vs = _np.r_[_vs, [v['val'] for v in data]]
                _st = _np.r_[_st, [v['status'] for v in data]]
                _sv = _np.r_[_sv, [v['severity'] for v in data]]
            if not _ts.size:
                return None
            _, _tsidx = _np.unique(_ts, return_index=True)
            timestamp, value, status, severity = \
                _ts[_tsidx], _vs[_tsidx], _st[_tsidx], _sv[_tsidx]
        else:
            raise TypeError(
                "'timestampstart' and 'timestamp_stop' arguments must be "
                "timestamp strings or iterable.")

        return timestamp, value, status, severity

    def getPVDetails(self, pvname, get_request_url=False):
        """."""
        url = self._create_url(
            method='getPVDetails', pv=pvname)
        if get_request_url:
            return url
        resp = self._make_request(url)
        return None if not resp else resp

    def _make_request(self, url, need_login=False, return_json=False):
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.handle_request(
            url, return_json=return_json, need_login=need_login))
        return response

    def _create_url(self, method, **kwargs):
        """."""
        url = self._url
        if method.startswith('getData.json'):
            url += '/retrieval/data'
        else:
            url += self.ENDPOINT
        url += '/' + method
        if kwargs:
            url += '?'
            url += '&'.join(['{}={}'.format(k, v) for k, v in kwargs.items()])
        return url

    # async methods

    async def handle_request(
            self, url, return_json=False, need_login=False):
        """Return request response."""
        if self.session is not None:
            try:
                resp = await self.session.get(url)
                if return_json:
                    resp = await resp.json()
            except asyncio.TimeoutError as err_msg:
                raise ConnectionError(err_msg)
        elif need_login:
            raise AuthenticationError('You need to login first.')
        else:
            async with ClientSession() as sess:
                try:
                    if isinstance(url, list):
                        resp = await asyncio.gather(
                            *[sess.get(u, ssl=False, timeout=self.timeout)
                              for u in url])
                        if return_json:
                            resp = await asyncio.gather(
                                *[r.json() for r in resp])
                    else:
                        resp = await sess.get(
                            url, ssl=False, timeout=self.timeout)
                        if return_json:
                            resp = await resp.json()
                except asyncio.TimeoutError as err_msg:
                    raise ConnectionError(err_msg)
        return resp

    async def handle_login(self, url, headers, payload, ssl):
        """Handle login."""
        session = ClientSession()
        async with session.post(
                url, headers=headers, data=payload, ssl=ssl,
                timeout=self.timeout) as response:
            authenticated = b"authenticated" in response.content
        return session, authenticated

    async def close_session(self):
        """Close session."""
        return await self.session.close()

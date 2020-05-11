#!/usr/bin/env python-sirius
"""Fetcher module.

See https://slacmshankar.github.io/epicsarchiver_docs/userguide.html
"""

from urllib import parse as _parse
import requests
import urllib3 as _urllib3

from .. import envars as _envars


class AuthenticationError(Exception):
    """."""


class ClientArchiver:
    """Archiver Data Fetcher class."""

    SERVER_URL = _envars.SRVURL_ARCHIVER
    ENDPOINT = '/mgmt/bpl'

    def __init__(self, server_url=None):
        """."""
        self.session = None
        self._url = server_url or self.SERVER_URL
        # print('urllib3 InsecureRequestWarning disabled!')
        _urllib3.disable_warnings(_urllib3.exceptions.InsecureRequestWarning)

    @property
    def connected(self):
        """."""
        # TODO: choose minimal request command in order to check connection.
        raise NotImplementedError

    def login(self, username, password):
        """."""
        headers = {"User-Agent": "Mozilla/5.0"}
        payload = {"username": username, "password": password}
        url = self._create_url(method='login')
        self.session = requests.Session()
        response = self.session.post(
            url, headers=headers, data=payload, verify=False)
        return b"authenticated" in response.content

    def getPVsInfo(self, pvnames):
        """."""
        if isinstance(pvnames, (list, tuple)):
            pvnames = ','.join(pvnames)
        url = self._create_url(method='getPVStatus', pv=pvnames)
        req = self._make_request(url)
        if not req.ok:
            return None
        return req.json()

    def getAllPVs(self, pvnames):
        """."""
        if isinstance(pvnames, (list, tuple)):
            pvnames = ','.join(pvnames)
        url = self._create_url(method='getAllPVs', pv=pvnames, limit='-1')
        return self._make_request(url).json()

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
        return self._make_request(url).json()

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
        self._make_request(url, need_login=True)

    def resumePVs(self, pvnames):
        """."""
        if not isinstance(pvnames, (list, tuple)):
            pvnames = (pvnames, )
        for pvname in pvnames:
            url = self._create_url(method='resumeArchivingPV', pv=pvname)
            self._make_request(url, need_login=True)

    def getData(self, pvname, timestamp_start, timestamp_stop, mean_sec=None,
                get_request_url=False):
        """Get archiver data.

        pvname -- name of pv.
        timestamp_start -- timestamp of interval start
                           Example: '2019-05-23T13:32:27.570Z'
        timestamp_stop -- timestamp of interval stop
                           Example: '2019-05-23T13:32:27.570Z'
        """
        tstart = _parse.quote(timestamp_start)
        tstop = _parse.quote(timestamp_stop)
        if mean_sec is not None:
            pvname = 'mean_' + str(int(mean_sec)) + '(' + pvname + ')'
        url = self._create_url(
            method='getData.json', pv=pvname, **{'from': tstart, 'to': tstop})
        if get_request_url:
            return url
        req = self._make_request(url)
        if not req.ok:
            return None
        ans = req.json()
        data = ans[0]['data']
        value = [v['val'] for v in data]
        timestamp = [v['secs'] + v['nanos']/1.0e9 for v in data]
        status = [v['status'] for v in data]
        severity = [v['severity'] for v in data]
        return timestamp, value, status, severity

    def getPVDetails(self, pvname, get_request_url=False):
        """."""
        url = self._create_url(
            method='getPVDetails', pv=pvname)
        if get_request_url:
            return url
        req = self._make_request(url)
        if not req.ok:
            return None
        data = req.json()
        return data

    def _make_request(self, url, need_login=False):
        if self.session is not None:
            req = self.session.get(url)
        elif need_login:
            raise AuthenticationError('You need to login first.')
        else:
            req = requests.get(url, verify=False)
        return req

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

"""ID Search module."""

from threading import Lock as _Lock

from .. import clientweb as _web
from ..magnet.excdata import ExcitationData as _ExcitationData

from .ps_search import PSSearch as _PSSearch


class IDSearch:
    """ID Search Class."""

    # NOTE: Maybe we should move these mappings to
    # static tables in our cs-constants server.

    _beamline2idname = {
        'CARNAUBA': 'SI-06SB:ID-Delta21',
        'CATERETE': 'SI-07SP:ID-Delta21',
        'EMA':      'SI-08SB:ID-APU19',
        'MANACA':   'SI-09SA:ID-APU22',
        'SABIA':    'SI-10SB:ID-Delta52',
        'IPE':      'SI-11SP:ID-Delta52',
        'COLIBRI':  'SI-12SB:ID-Delta52',
        'HARPIA':   'SI-14SB:ID-Delta21',
        'SAGUI':    'SI-15SP:ID-Delta21',
        'INGA':     'SI-16SB:ID-Delta21',
        'SAPUCAIA': 'SI-17SA:ID-APU19',
        'PAINEIRA': 'SI-18SB:ID-Delta21',
    }
    _idname2beamline = {v: k for k, v in _beamline2idname.items()}

    _idname_2_orbitcorr = {
        'SI-09SA:ID-APU22': (
            'SI-09SA:PS-CH-1', 'SI-09SA:PS-CH-2',
            'SI-09SA:PS-CH-3', 'SI-09SA:PS-CH-4',
            'SI-09SA:PS-CV-1', 'SI-09SA:PS-CV-2',
            'SI-09SA:PS-CV-3', 'SI-09SA:PS-CV-4',
        )
    }

    _idname_2_orbitffwd_fname = {
        'SI-09SA:ID-APU22': 'si-id-apu22-ffwd-09sa',
    }

    _idname_2_orbitffwd_dict = dict()

    _lock = _Lock()

    @staticmethod
    def conv_idname_2_beamline(idname):
        """Return the beam line name corresponding to sector."""
        if idname in IDSearch._idname2beamline.keys():
            return IDSearch._idname2beamline[idname]
        return None

    @staticmethod
    def conv_beamline_2_idname(beamline):
        """Return the beam line name corresponding to idname."""
        if beamline in IDSearch._beamline2idname.keys():
            return IDSearch._beamline2idname[beamline]
        return None

    @staticmethod
    def get_idname_2_beamline_dict():
        """Return idname to beamline dictionary."""
        return IDSearch._idname2beamline.copy()

    @staticmethod
    def get_beamline_2_idname_dict():
        """Return beamline to idname dictionary."""
        return IDSearch._beamline2idname.copy()

    @staticmethod
    def get_idnames(filters=None):
        """Return a sorted and filtered list of all ID names."""
        filters_ = dict()
        if filters:
            filters_.update(filters)
        filters_['dis'] = 'ID'
        return _PSSearch.get_psnames(filters_)

    @staticmethod
    def conv_idname_2_orbitcorr(idname):
        """Return list of orbit correctors of a given ID."""
        return IDSearch._idname_2_orbitcorr[idname]

    @staticmethod
    def conv_idname_2_orbitffwd(idname):
        """Convert idname to orbit feedforward excdata."""
        IDSearch._reload_idname_2_orbitffwd_dict(idname)
        return IDSearch._idname_2_orbitffwd_dict[idname]

    # --- private methods ---

    @staticmethod
    def _reload_idname_2_orbitffwd_dict(idname):
        """Load ID ffwd data."""
        with IDSearch._lock:
            if idname in IDSearch._idname_2_orbitffwd_dict:
                return
            if not _web.server_online():
                raise Exception(
                    'could not read "' + str(idname) + '" from web server!')
            ffwd_fname = IDSearch._idname_2_orbitffwd_fname[idname]
            IDSearch._idname_2_orbitffwd_dict[idname] = \
                _ExcitationData(filename_web=ffwd_fname + '.txt')

"""MA Search module."""

from threading import Lock as _Lock

from .. import util as _util
from .. import clientweb as _web
from ..namesys import Filter as _Filter
from ..namesys import SiriusPVName as _SiriusPVName
from ..magnet import util as _mutil
from .ps_search import PSSearch as _PSSearch


class MASearch:
    """MA and PM Magnet Search class."""

    _psnames_list = list()
    _manames_list = list()
    _maname_2_psnames_dict = dict()  # magnet-excitation-ps file
    _maname_2_trim_dict = dict()
    _maname_2_modeldata_dict = dict()

    _lock = _Lock()

    @staticmethod
    def get_manames(filters=None, sorting=None):
        """Return a sorted and filtered list of all magnet names.

        This list also includes pulsed magnets (PM).
        """
        MASearch._reload_maname_2_psnames_dict()
        return _Filter.process_filters(MASearch._manames_list,
                                       filters=filters,
                                       sorting=sorting)

    @staticmethod
    def get_pwrsupply_manames(filters=None, sorting=None):
        """Return a sorted and filtered list of all pwrsupply magnet names."""
        MASearch._reload_maname_2_psnames_dict()
        ps_manames_list = list(MASearch._maname_2_psnames_dict.keys())
        return _Filter.process_filters(ps_manames_list,
                                       filters=filters,
                                       sorting=sorting)

    @staticmethod
    def get_mapositions(names=None, filters=None, sorting=None):
        """Return a sorted and filtered list of all magnet positions.

        This list also includes pulsed magnets (PM).
        """
        MASearch._reload_maname_2_model_data()
        if not names:
            names = MASearch.get_manames(filters=filters, sorting=sorting)
        return [MASearch._maname_2_modeldata_dict[mag]['pos'] for mag in names]

    @staticmethod
    def get_manicknames(names=None, filters=None, sorting=None):
        """Return a list with Magnet nicknames."""
        if not names:
            names = MASearch.get_manames(filters=filters, sorting=sorting)
        nicknames = len(names)*['']
        for i, mag in enumerate(names):
            nicknames[i] = mag.sub + ('-' + mag.idx if mag.idx else '')
        return nicknames

    @staticmethod
    def conv_maname_2_trims(maname):
        """Convert maname powersupply to its trims."""
        MASearch._reload_maname_2_psnames_dict()
        return MASearch._maname_2_trim_dict.get(maname, None)

    @staticmethod
    def conv_maname_2_magfunc(maname):
        """Return a dict mapping ps to magnet functions for given magnet ps."""
        MASearch._reload_maname_2_psnames_dict()
        ps = MASearch._maname_2_psnames_dict[maname]
        ps_types = tuple(map(_PSSearch.conv_psname_2_pstype, ps))
        ma_func = tuple(map(_PSSearch.conv_pstype_2_magfunc, ps_types))

        ret = dict()
        for i, psname in enumerate(ps):
            ret[psname] = ma_func[i]

        return ret

    @staticmethod
    def conv_maname_2_psnames(maname):
        """Return list of power supplies associated with a given magnet."""
        MASearch._reload_maname_2_psnames_dict()
        return MASearch._maname_2_psnames_dict[maname]

    @staticmethod
    def conv_psmaname_2_psnames(maname):
        """Return list of power supplies associated with a given magnet ps."""
        maname = _SiriusPVName(maname)
        ma_class = _mutil.magnet_class(maname)
        if 'dipole' == ma_class:
            if 'SI' == maname.sec:
                return ['SI-Fam:PS-B1B2-1', 'SI-Fam:PS-B1B2-2']
            elif 'BO' == maname.sec:
                return ['BO-Fam:PS-B-1', 'BO-Fam:PS-B-2']
        elif 'pulsed' == ma_class:
            return [maname.replace(':PM', ':PU')]
        return [maname.replace(':MA', ':PS')]

    @staticmethod
    def conv_psname_2_psmaname(psname):
        """Return power supply maname for a given psname."""
        MASearch._reload_maname_2_psnames_dict()
        if psname not in MASearch._psnames_list or 'DCLink' in psname:
            return None
        if 'PS-B1B2' in psname:
            return 'SI-Fam:MA-B1B2'
        elif 'BO-Fam:PS-B' in psname:
            return 'BO-Fam:MA-B'
        else:
            return psname.replace('PS', 'MA').replace('PU', 'PM')

    @staticmethod
    def conv_bbbname_2_psmanames(bbbname):
        """Return psmanames for a given bbbname."""
        manames = set()
        psnames = _PSSearch.conv_bbbname_2_psnames(bbbname)
        for psname in psnames:
            maname = MASearch.conv_psname_2_psmaname(psname[0])
            if maname is None:
                continue
            manames.add(maname)
        return list(manames)

    # --- private methods ---

    @staticmethod
    def _reload_maname_2_psnames_dict():
        """Build a dict of tuples with power supplies of each magnet."""
        with MASearch._lock:
            if MASearch._maname_2_psnames_dict:
                return
            if not _web.server_online():
                raise Exception(
                    'could not read magnet-excitation-ps from web server!')
            text = _web.magnets_excitation_ps_read()
            data, param_dict = _util.read_text_data(text)
            maname_2_psnames_dict = dict()
            maname_2_trim_dict = dict()
            manames_list = list()
            for datum in data:
                magnet, *psnames = datum
                magnet = _SiriusPVName(magnet)
                manames_list.append(magnet)
                maname_2_psnames_dict[magnet] = tuple(psnames)
                if 'Fam' != magnet.sub:
                    famname = magnet
                    famname = famname.replace(
                        famname.sub, 'Fam').replace('MA-', 'PS-')
                    if '-Fam:PS-Q' in famname and famname in psnames:
                        psnames.remove(famname)
                        maname = famname.replace('PS-', 'MA-')
                        if maname not in maname_2_trim_dict:
                            maname_2_trim_dict[maname] = tuple(psnames)
                        else:
                            maname_2_trim_dict[maname] += tuple(psnames)
            MASearch._maname_2_psnames_dict = maname_2_psnames_dict
            MASearch._maname_2_trim_dict = maname_2_trim_dict
            MASearch._manames_list = sorted(manames_list)
            MASearch._psnames_list = _PSSearch.get_psnames()

    @staticmethod
    def _reload_maname_2_model_data():
        """Build a dictionary of model information for each magnet."""
        with MASearch._lock:
            if MASearch._maname_2_modeldata_dict:
                return
            if not _web.server_online():
                raise Exception(
                    'could not read magnet model data from web server!')
            text = _web.magnets_model_data()
            data, param_dict = _util.read_text_data(text)
            maname_2_modeldata_dict = dict()
            for datum in data:
                mag, *data = datum
                mag = _SiriusPVName(mag)
                maname_2_modeldata_dict[mag] = {'pos': float(data[0])}
            MASearch._maname_2_modeldata_dict = maname_2_modeldata_dict

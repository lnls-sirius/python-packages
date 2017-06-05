
import copy as _copy
import siriuspy.util as _util
import siriuspy.servweb as _web

class PSSearch:

    _connection_timeout   = None
    _pstype_dict          = None
    _pstype_2_names_dict  = None
    _pstype_2_splims_dict = None
    _splims_labels        = None
    _splims_unit          = None
    _psnames_list         = None

    @staticmethod
    def reload_pstype_dict():
        """Reload power supply type dictionary from web server."""
        if _web.server_online():
            text = _web.power_supplies_pstypes_names_read(timeout=PSSearch._connection_timeout)
            data, params_dict = _util.read_text_data(text)
            PSSearch._pstype_dict = {}
            for datum in data:
                name, polarity, magfunc = datum[0], datum[1], datum[2]
                PSSearch._pstype_dict[name] = (polarity, magfunc)
        else:
            raise Exception('could not read pstypes from web server!')

    @staticmethod
    def reload_pstype_2_names_dict():
        """Reload power supply type to power supply names dictionary from web server."""
        if PSSearch._pstype_dict is None: PSSearch.reload_pstype_dict()
        pstypes = sorted(set(PSSearch._pstype_dict.keys()))
        PSSearch._pstype_2_names_dict = {}
        PSSearch._psnames_list = []
        for pstype in pstypes:
            text = _web.power_supplies_pstype_data_read(pstype + '.txt', timeout=PSSearch._connection_timeout)
            data, param_dict = _util.read_text_data(text)
            psnames = [datum[0] for datum in data]
            PSSearch._pstype_2_names_dict[pstype] = psnames
            PSSearch._psnames_list += psnames
        PSSearch._psnames_list = sorted(set(PSSearch._psnames_list))

    @staticmethod
    def reload_pstype_2_splims_dict():
        text = _web.power_supplies_pstype_setpoint_limits(timeout=PSSearch._connection_timeout)
        data, param_dict = _util.read_text_data(text)
        PSSearch._splims_unit = tuple(param_dict['unit'])
        PSSearch._splims_labels = tuple(param_dict['power_supply_type'])
        PSSearch._pstype_2_splims_dict = {}
        for datum in data:
            pstype, *lims = datum
            PSSearch._pstype_2_splims_dict[pstype] = {PSSearch._splims_labels[i]:float(lims[i]) for i in range(len(lims))}

    @staticmethod
    def get_pstype_dict():
        """Return dictionary with key,value pairs of power supply types and corresponding (polarities,mag_function)."""
        if PSSearch._pstype_dict is None: PSSearch.reload_pstype_dict()
        return _copy.deepcopy(PSSearch._pstype_dict)

    @staticmethod
    def get_pstype_names():
        """Return sorted list of power supply types."""
        if PSSearch._pstype_dict is None: PSSearch.reload_pstype_dict()
        return sorted(set(PSSearch._pstype_dict.keys()))

    @staticmethod
    def get_polarities():
        """Return sorted list of power supply polarities."""
        if PSSearch._pstype_dict is None: PSSearch.reload_pstype_dict()
        p = [datum[0] for datum in PSSearch._pstype_dict.values()]
        return sorted(set(p))

    @staticmethod
    def get_pstype_2_names_dict():
        """Return dictionary of power supply type and corresponding power supply names."""
        if PSSearch._pstype_2_names_dict is None: PSSearch.reload_pstype_2_names_dict()
        return _copy.deepcopy(PSSearch._pstype_2_names_dict)

    @staticmethod
    def conv_psname_2_pstype(name):
        """Return the power supply type of a given power supply name."""
        if PSSearch._pstype_2_names_dict is None: PSSearch.reload_pstype_2_names_dict()
        for pstype,names in PSSearch._pstype_2_names_dict.items():
            if name in names: return pstype
        return None

    @staticmethod
    def conv_pstype_2_polarity(pstype):
        """Return polarity of a given power supply type."""
        if PSSearch._pstype_dict is None: PSSearch.reload_pstype_dict()
        for key,value in PSSearch._pstype_dict.items():
            if key == pstype: return value[0]
        return None

    @staticmethod
    def conv_pstype_2_magfunc(pstype):
        """Return magnetic function of a given power supply type."""
        if PSSearch._pstype_dict is None: PSSearch.reload_pstype_dict()
        for key,value in PSSearch._pstype_dict.items():
            if key == pstype: return value[1]
        return None

    @staticmethod
    def conv_pstype_2_splims(pstype):
        if pstype is None: return None
        if PSSearch._pstype_2_splims_dict is None: PSSearch.reload_pstype_2_splims_dict()
        return _copy.deepcopy(PSSearch._pstype_2_splims_dict[pstype])

    @staticmethod
    def get_splim(pstype, label):
        """Return setpoint limit corresponding to given label (either epics' or pcaspy's)."""
        if PSSearch._pstype_2_splims_dict is None: PSSearch.reload_pstype_2_splims_dict()
        if label in PSSearch._splims_labels:
            return PSSearch._pstype_2_splims_dict[pstype][label]
        else:
            label = _util.conv_splims_labels(label)
            if label is None:
                return None
            else:
                return PSSearch._pstype_2_splims_dict[pstype][label]

    @staticmethod
    def get_psnames(filters=None):
        """Return a sorted and filtered list of all power supply names."""
        if PSSearch._pstype_2_names_dict is None: PSSearch.reload_pstype_2_names_dict()
        return _util.filter_pvnames(PSSearch._psnames_list, filters=filters)

    @staticmethod
    def get_pstype_2_splims_dict():
        """Return a dictionary of power supply type and corresponding setpoint limits."""
        if PSSearch._pstype_2_splims_dict is None: PSSearch.reload_pstype_2_splims_dict()
        return _copy.deepcopy(PSSearch._pstype_2_splims_dict)

    @staticmethod
    def get_splims_unit():
        if PSSearch._pstype_2_splims_dict is None: PSSearch.reload_pstype_2_splims_dict()
        return PSSearch._splims_unit

    @staticmethod
    def get_splims_labels():
        if PSSearch._pstype_2_splims_dict is None: PSSearch.reload_pstype_2_splims_dict()
        return PSSearch._splims_labels

class MASearch:

    _maname_2_splims_dict = None
    _pslims_labels        = None
    _splims_unit          = None

    @staticmethod
    def reload_pstype_2_splims_dict():
        text = _web.power_supplies_pstype_setpoint_limits(timeout=PSSearch._connection_timeout)
        data, param_dict = _util.read_text_data(text)
        PSSearch._splims_unit = tuple(param_dict['unit'])
        PSSearch._splims_labels = tuple(param_dict['power_supply_type'])
        PSSearch._pstype_2_splims_dict = {}
        for datum in data:
            pstype, *lims = datum
            PSSearch._pstype_2_splims_dict[pstype] = {PSSearch._splims_labels[i]:float(lims[i]) for i in range(len(lims))}

    @staticmethod
    def get_splims_unit():
        pass

    @staticmethod
    def get_splim(maname, label):
        """Return setpoint limit corresponding to given label (either epics' or pcaspy's)."""
        if MASearch._maname_2_splims_dict is None: PSSearch.reload_maname_2_splims_dict()
        if label in MASearch._splims_labels:
            return MASearch._maname_2_splims_dict[maname][label]
        else:
            label = _util.conv_splims_labels(label)
            if label is None:
                return None
            else:
                return MASearch._maname_2_splims_dict[maname][label]

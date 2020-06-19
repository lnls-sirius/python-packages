"""Implementation of namesys functions nad classes."""

import types as _types
import re as _re


_ATTRS = (
    'channel_type',
    'prefix',
    'sec',
    'sub',
    'dis',
    'dev',
    'idx',
    'propty',
    'field',
    'device_name',
    'area_name',
    'propty_name',
    'propty_suffix',
    'device_propty',
)


def get_siriuspvname_attrs():
    """Return SiriusPVName attributes."""
    return [attr for attr in _ATTRS]


def join_name(**kwargs):
    """Return SiriusPVName object.

    Parameters
        channel_type [str] : PyDM channel type, ex: 'ca'
        prefix [str] : Prefix, ex: 'fac-454lnls'
        sec [str] : Section, ex: 'SI'
        sub [str] : Subsection, ex: 'Glob'
        dis [str] : Discipline, ex: 'PS'
        dev [str] : Device, ex: 'B'
        idx [str] : Device index, ex: '1'
        propty_name [str] : Property name, ex: 'Properties'
        propty_suffix [str] : Property suffix, ex: 'Cte'
        propty [str] : Full property, ex: 'Properties-Cte'
        field [str] : Field, ex: 'STATUS'

    """
    dic = {k: v for k, v in kwargs.items() if v}  # get valid args
    name = ''
    if len(dic.keys()) == 1:
        if 'propty' in dic.keys():
            name = dic['propty']
        elif 'propty_name' in dic.keys():
            name = dic['propty_name']
    elif len(dic.keys()) == 2:
        if 'sec' in dic.keys() and 'sub' in dic.keys():
            name = dic['sec'].upper() + '-' + dic['sub']
        elif 'dis' in dic.keys() and 'dev' in dic.keys():
            name = dic['dis'].upper() + '-' + dic['dev']
        elif 'propty_name' in dic.keys() and 'propty_suffix' in dic.keys():
            name = dic['propty_name'].upper() + '-' + dic['propty_suffix']
    elif len(dic.keys()) == 3:
        if 'dis' in dic.keys() and 'dev' in dic.keys() and 'idx' in dic.keys():
            name = dic['dis'].upper() + '-' + dic['dev'] + '-' + dic['idx']
    elif len(dic.keys()) > 3:
        name = dic['channel_type'] + '://' if 'channel_type' in dic.keys() else ''
        name = dic['prefix'] + '-' if 'prefix' in dic.keys() else ''
        name += (dic['sec'].upper() + '-' + dic['sub'] + ':' +
                 dic['dis'].upper() + '-' + dic['dev'])
        name += ('-' + dic['idx']) if 'idx' in dic.keys() else ''
        if 'propty_name' in dic.keys() and 'propty_suffix' in dic.keys():
            name += ':' + dic['propty_name'] + '-' + dic['propty_suffix']
            name += ('.' + dic['field']) if 'field' in dic.keys() else ''
        elif 'propty' in dic.keys():
            name += ':' + dic['propty']
            name += ('.' + dic['field']) if 'field' in dic.keys() else ''
        elif 'propty_name' in dic.keys():
            name += ':' + dic['propty_name']

    if not name:
        raise TypeError('Not a valid SiriusPVName elements set!')
    return SiriusPVName(name)


def split_name(pvname, elements=None):
    """Return dict with PV name split into fields.

    Parameters
        pvname [str] : a complete pvname or a valid part of it.
        elements [None, 'propty', 'sec-sub', 'dis-dev'] : if pvname is not a
            complete name, 'elements' says which part of pvname
            it corresponds to.

    """
    if not elements:
        elements = 'propty'

    # empty dictionary
    dic_ = {attr: '' for attr in _ATTRS}

    # strip PV name
    pvname = pvname.strip()
    if not pvname:
        return dic_

    # deals with channel
    dic_['channel_type'] = ''
    names = pvname.split('://')
    if len(names) == 2:
        dic_['channel_type'] = names[0]
        pvname = names[1]

    list_ = pvname.split(':')

    if len(list_) == 1:
        slist_ = list_[0].split('-')
        if len(slist_) == 1:
            dic_['propty'] = slist_[0]
            dic_['propty_name'] = slist_[0]
        elif len(slist_) == 2:
            if elements == 'propty':
                dic_['propty'] = slist_[0] + '-' + slist_[1]
                dic_['propty_name'] = slist_[0]
                dic_['propty_suffix'] = slist_[1]
            elif elements == 'sec-sub':
                dic_['sec'] = slist_[0]
                dic_['sub'] = slist_[1]
                dic_['area_name'] = slist_[0] + '-' + slist_[1]
            elif elements == 'dis-dev':
                dic_['dis'] = slist_[0]
                dic_['dev'] = slist_[1]
        elif len(slist_) == 3:
            dic_['dis'] = slist_[0]
            dic_['dev'] = slist_[1]
            dic_['idx'] = slist_[2]
    else:
        slist_ = list_[0].split('-')
        dic_['prefix'] = '-'.join([s for s in slist_[:-2]])
        dic_['area_name'] = '-'.join([s for s in slist_[-2:]])
        dic_['device_name'] = dic_['area_name'] + ':' + list_[1]

        dic_['sec'] = slist_[-2]
        dic_['sub'] = slist_[-1]

        slist_ = list_[1].split('-')
        dic_['dis'] = slist_[0]
        dic_['dev'] = slist_[1]
        dic_['idx'] = slist_[2] if len(slist_) >= 3 else ''

        if len(list_) > 2:
            slist_ = list_[2].split('.')
            sslist_ = slist_[0].split('-')
            dic_['propty'] = slist_[0]
            dic_['propty_name'] = sslist_[0]
            dic_['propty_suffix'] = sslist_[1] if len(sslist_) > 1 else ''
            dic_['field'] = slist_[1] if len(slist_) >= 2 else ''

        dic_['device_propty'] = (
            dic_['dev'] +
            ('-' + dic_['idx'] if dic_['idx'] else '') +
            (':' + dic_['propty'] if dic_['propty'] else '') +
            ('.' + dic_['field'] if dic_['field'] else ''))
    return dic_


def get_pair_sprb(pv_propty):
    """Return the equivalent [setpoint, readback] SiriusPVName property pair.

    Input: a SiriusPVName property, with a setpoint or a readback suffix.
    Output: the equivalent Sirius [setpoint, readback] pair.
    """
    _sp_rb = {'SP': 'RB', 'Sel': 'Sts'}
    _rb_sp = {v: k for k, v in _sp_rb.items()}

    suffix = pv_propty.propty_suffix

    if suffix in _sp_rb.keys():
        return [pv_propty, pv_propty.substitute(propty_suffix=_sp_rb[suffix])]
    elif suffix in _rb_sp.keys():
        return [pv_propty.substitute(propty_suffix=_rb_sp[suffix]), pv_propty]
    else:
        raise TypeError('Input is not a setpoint/readback property!')


class SiriusPVName(str):
    """Sirius PV Name Class."""

    def __new__(cls, pv_name, elements=None):
        """Implement new method."""
        name = split_name(pv_name, elements)
        obj = super().__new__(cls, pv_name)
        obj.channel_type = name['channel_type']
        obj.prefix = name['prefix']
        obj.sec = name['sec']
        obj.sub = name['sub']
        obj.area_name = name['area_name']
        obj.dis = name['dis']
        obj.dev = name['dev']
        obj.idx = name['idx']
        obj._device_name = name['device_name']
        obj.propty_name = name['propty_name']
        obj.propty_suffix = name['propty_suffix']
        obj.propty = name['propty']
        obj.device_propty = name['device_propty']
        obj.field = name['field']
        return obj

    @property
    def device_name(self):
        """."""
        return SiriusPVName(self._device_name)

    def substitute(self, **kwargs):
        """Return new SiriusPVName object with the atttributes changed."""
        dic_ = {}
        dic_['sec'] = self.sec
        dic_['sub'] = self.sub
        dic_['dis'] = self.dis
        dic_['dev'] = self.dev
        dic_['idx'] = self.idx
        dic_['propty'] = self.propty
        dic_['propty_name'] = self.propty_name
        dic_['propty_suffix'] = self.propty_suffix
        dic_['field'] = self.field
        dic_['prefix'] = self.prefix
        dic_['channel_type'] = self.channel_type
        dic_.update({k: v for k, v in kwargs.items() if isinstance(v, str)})
        if 'propty' in kwargs:
            dic_.pop('propty_name', None)
            dic_.pop('propty_suffix', None)
        return join_name(**dic_)

    def get_nickname(self, sec=False, dev=False):
        """."""
        nickname = ''
        if sec:
            nickname += self.sec + '-'
        nickname += self.sub
        if dev:
            nickname += ':' + self.dev
        nickname += '-' + self.idx if self.idx else ''
        return nickname

    def __lt__(self, other):
        """Less-than operator."""
        cond = ((type(other) == type(self)) and
                (self.sec == other.sec) and
                (self.sub != other.sub))
        return self._subsec_comp(other) if cond else super().__lt__(other)

    def __gt__(self, other):
        """Greater-than operator."""
        return other.__lt__(self)

    def __le__(self, other):
        """Less-or-equal operator."""
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        """Greater-or-equal operator."""
        return self.__gt__(other) or self.__eq__(other)

    def strip(self, *args, **kwargs):
        """."""
        return SiriusPVName(super().strip(*args, **kwargs))

    def replace(self, *args, **kwargs):
        """."""
        return SiriusPVName(super().replace(*args, **kwargs))

    def _subsec_comp(self, other):
        """Subsection comparison."""
        my_ssec = self.sub
        th_ssec = other.sub
        my_dev = self.dev
        th_dev = other.dev
        if my_ssec == 'Glob':
            return False
        elif th_ssec == 'Glob':
            return True
        elif my_ssec == 'Fam':
            return False
        elif th_ssec == 'Fam':
            return True
        elif my_ssec == '01M1':
            if th_ssec == '01SA' and th_dev == 'ScrapH':
                return True
            else:
                return False
        elif th_ssec == '01M1':
            if my_ssec == '01SA' and my_dev == 'ScrapH':
                return False
            else:
                return True
        elif my_ssec == '01U' and my_dev in {'CV', 'BPM'}:
            return False
        elif th_ssec == '01U' and th_dev in {'CV', 'BPM'}:
            return True
        elif my_ssec[:2] != th_ssec[:2]:
            return my_ssec[:2] < th_ssec[:2]
        elif len(my_ssec) == 2:
            return False
        elif len(th_ssec) == 2:
            return True
        if my_ssec[2] == th_ssec[2]:
            return my_ssec[3] < th_ssec[3]
        elif my_ssec[2] == 'C':
            return False
        elif th_ssec[2] == 'C':
            return True
        elif my_ssec[2] == 'S':
            if th_ssec[2:4] == 'M1':
                return False
            elif th_ssec[2:4] == 'M2':
                return True
        elif th_ssec[2] == 'S':
            if my_ssec[2:4] == 'M1':
                return True
            elif my_ssec[2:4] == 'M2':
                return False

    @staticmethod
    def is_write_pv(pvname):
        """."""
        return SiriusPVName.is_sp_pv(pvname) or SiriusPVName.is_cmd_pv(pvname)

    @staticmethod
    def is_sp_pv(pvname):
        """."""
        return pvname.endswith(('-Sel', '-SP'))

    @staticmethod
    def is_cmd_pv(pvname):
        """."""
        return pvname.endswith('-Cmd')

    @staticmethod
    def is_cte_pv(pvname):
        """."""
        return pvname.endswith('-Cte')

    @staticmethod
    def is_rb_pv(pvname):
        """."""
        return pvname.endswith(('-Sts', '-RB'))

    @staticmethod
    def from_sp2rb(pvname):
        """."""
        return pvname.replace('-SP', '-RB').replace('-Sel', '-Sts')

    @staticmethod
    def from_rb2sp(pvname):
        """."""
        return pvname.replace('-RB', '-SP').replace('-Sts', '-Sel')


class Filter:
    """Filter class."""

    # NOTE: Are these class constants really useful?

    # PVName regex filters
    patterns = _types.SimpleNamespace()
    patterns.FAM = 'Fam'
    patterns.TRIM = '\d{2}\w{0,2}'
    patterns.DIPOLE = 'B.*'
    patterns.QUADRUPOLE = '(?:QD|QF|Q[0-9]).*'
    patterns.QUADRUPOLE_SKEW = 'QS'
    patterns.QD = 'QD.*'
    patterns.QF = 'QF.*'
    patterns.SEXTUPOLE = 'S(?:D|F)*'
    patterns.SD = 'SD.*'
    patterns.SF = 'SF.*'
    patterns.CORRECTOR = '(?:C|FC).*'
    patterns.SLOW_CHV = 'C(?:H|V).*'
    patterns.SLOW_CH = 'CH.*'
    patterns.SLOW_CV = 'CV.*'
    patterns.FAST_CHV = 'FC.*'
    patterns.FAST_CH = 'FCH.*'
    patterns.FAST_CV = 'FCV.*'

    filters = _types.SimpleNamespace()
    filters.FAM = {'sub': patterns.FAM}
    filters.TRIM = {'sub': patterns.TRIM}
    filters.DIPOLE = {'dev': patterns.DIPOLE}
    filters.QUADRUPOLE = {'dev': patterns.QUADRUPOLE}
    filters.QUADRUPOLE_SKEW = {'dev': patterns.QUADRUPOLE_SKEW}
    filters.QD = {'dev': patterns.QD}
    filters.QF = {'dev': patterns.QF}
    filters.SEXTUPOLE = {'dev': patterns.SEXTUPOLE}
    filters.SD = {'dev': patterns.SD}
    filters.SF = {'dev': patterns.SF}
    filters.CORRECTOR = {'dev': patterns.CORRECTOR}
    filters.SLOW_CHV = {'dev': patterns.SLOW_CHV}
    filters.SLOW_CH = {'dev': patterns.SLOW_CH}
    filters.SLOW_CV = {'dev': patterns.SLOW_CV}
    filters.FAST_CHV = {'dev': patterns.FAST_CHV}
    filters.FAST_CH = {'dev': patterns.FAST_CH}
    filters.FAST_CV = {'dev': patterns.FAST_CV}

    @staticmethod
    def add_filter(filters=None, sec=None, sub=None,
                   dis=None, dev=None):
        """."""
        if filters is None:
            filters = []
        fil = {}
        if sec is not None:
            fil['sec'] = sec
        if sub is not None:
            fil['sub'] = sub
        if dis is not None:
            fil['dis'] = dis
        if dev is not None:
            fil['dev'] = dev
        if fil:
            filters.append(fil)
        return filters

    @staticmethod
    def process_filters(pvnames, filters=None, sorting=None):
        """Return a sorted and filtered list of given pv name lists.

        'filters' is either a dictionary of a list of dictionaries whose keys
        are pv sub parts and the values are the desired patterns
        """
        if filters is None:
            return pvnames
        if isinstance(filters, dict):
            filters = [filters]
        elif isinstance(pvnames, str):
            pvnames = [pvnames]

        # build filter regexp
        fs = []
        for fil in filters:
            if 'sec' not in fil or fil['sec'] is None:
                fil['sec'] = '[A-Z]{2,4}'
            if 'sub' not in fil or fil['sub'] is None:
                fil['sub'] = '\w{2,16}'
            if 'dis' not in fil or fil['dis'] is None:
                fil['dis'] = '[A-Z]{2,6}'
            if 'dev' not in fil or fil['dev'] is None:
                fil['dev'] = '.+'
            pattern = (fil['sec'] + '-' + fil['sub'] + ':' +
                       fil['dis'] + '-' + fil['dev'])
            if 'idx' in fil:
                pattern += '-' + fil['idx']
            regexp = _re.compile(pattern)
            fs.append(regexp)

        # filter list
        filtered_list = list()
        for pvname in pvnames:
            for pattern in fs:
                if pattern.match(pvname):
                    filtered_list.append(pvname)
                    break

        if sorting is None:
            sorted_filtered_list = filtered_list
        elif sorting == 'length':
            raise NotImplementedError
        return sorted_filtered_list

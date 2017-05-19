import types as _types
import copy as _copy

class _ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class EnumTypes:

    # This should be constructed from CCDB server.

    _types = {
        'OffOnTyp'        : ('Off', 'On'),
        'OffOnWaitTyp'    : ('Off', 'On', 'Wait'),
        'DsblEnblTyp'     : ('Dsbl', 'Enbl'),
        'PSOpModeTyp'     : ('SlowRef', 'SyncRef', 'FastRef',
                             'RmpMultWfm', 'RmpSglWfm',
                             'MigMultWfm', 'MigSglWfm',
                             'SigGen', 'CycGen'),
        'PSWfmLabelsTyp'  : ('Waveform1', 'Waveform2', 'Waveform3',
                             'Waveform4', 'Waveform5', 'Waveform6'),

        'PSIntlkLabelsTyp': ('Timeout', 'Bit1', 'Bit2',
                                'Bit3', 'Bit4', 'Bit5',
                                'Bit6', 'Bit7'),

        'RmtLocTyp'       : ('Remote', 'Local'),
        'SOFBOpModeTyp'   : ('Off', 'AutoCorr', 'MeasRespMat'),
    }

    @staticmethod
    def enums(typ):
        if typ not in EnumTypes._types: return None
        return EnumTypes._types[typ]

    @staticmethod
    def get_idx(typ,value):
        values = EnumTypes.enums(typ)
        if value not in values: return None
        return values.index(value)

    @staticmethod
    def key(typ,idx):
        if idx is None: return 'None'
        values = EnumTypes.enums(typ)
        return values[idx]

    @staticmethod
    def values(typ):
        return tuple(range(len(EnumTypes._types[typ])))

    @staticmethod
    def types():
        return _copy.deepcopy(EnumTypes._types)

    @_ClassProperty
    @classmethod
    def names(cls):
        return tuple(cls._types.keys())

# create class 'idx' class object with constants
EnumTypes.idx = _types.SimpleNamespace()
for k,v in EnumTypes._types.items():
    for i in range(len(v)):
        setattr(EnumTypes.idx, v[i], i)

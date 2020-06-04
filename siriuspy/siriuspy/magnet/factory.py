"""Definition of factories.

NormalizerFactory
    used to create magnet normalizers
"""

from ..search import PSSearch as _PSSearch
from ..search import MASearch as _MASearch

from . import util as _mutil
from . import normalizer as _norm


class NormalizerFactory:
    """Factory class for normalizer objects."""

    @staticmethod
    def create(maname):
        """Return appropriate normalizer."""
        psname = _MASearch.conv_maname_2_psnames(maname)[0]
        magfunc = _PSSearch.conv_psname_2_magfunc(psname)
        ma_class = _mutil.magnet_class(maname)
        if ma_class == 'dipole':
            return _norm.DipoleNormalizer(maname, magnet_conv_sign=-1.0)
        if ma_class == 'trim':
            return _norm.TrimNormalizer(maname, magnet_conv_sign=-1.0)
        if ma_class == 'id-apu':
            return _norm.APUNormalizer(maname, magnet_conv_sign=+1.0)
        if magfunc == 'corrector-horizontal':
            return _norm.MagnetNormalizer(maname, magnet_conv_sign=+1.0)
        if 'TB' in maname and 'QD' in maname:
            return _norm.MagnetNormalizer(maname, magnet_conv_sign=+1.0,)
        return _norm.MagnetNormalizer(maname, magnet_conv_sign=-1.0)

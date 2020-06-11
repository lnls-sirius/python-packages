"""Class of the Response Matrix."""

import os as _os
from copy import deepcopy as _dcopy
import logging as _log
from functools import partial as _part

import numpy as _np

from .base_class import BaseClass as _BaseClass


class BaseMatrix(_BaseClass):
    """."""


class EpicsMatrix(BaseMatrix):
    """Class of the Response Matrix."""

    def __init__(self, acc, prefix='', callback=None):
        """Initialize the instance."""
        super().__init__(acc, prefix=prefix, callback=callback)
        self.select_items = {
            'bpmx': _np.ones(self._csorb.nr_bpms, dtype=bool),
            'bpmy': _np.ones(self._csorb.nr_bpms, dtype=bool),
            'ch': _np.ones(self._csorb.nr_ch, dtype=bool),
            'cv': _np.ones(self._csorb.nr_cv, dtype=bool),
            }
        self.selection_pv_names = {
            'ch': 'CHEnblList-RB',
            'cv': 'CVEnblList-RB',
            'bpmx': 'BPMXEnblList-RB',
            'bpmy': 'BPMYEnblList-RB',
            }
        if self.acc == 'SI':
            self.select_items['rf'] = _np.zeros(1, dtype=bool)
            self.selection_pv_names['rf'] = 'RFEnbl-Sts'
        self.num_sing_values = self._csorb.nr_svals
        self.sing_values = _np.zeros(self._csorb.nr_corrs, dtype=float)
        self.respmat = _np.zeros(
            [2*self._csorb.nr_bpms, self._csorb.nr_corrs], dtype=float)
        self.inv_respmat = self.respmat.copy().T

        self.ring_extension = 1
        self.respmat_extended = self.respmat.copy()
        self.select_items_extended = _dcopy(self.select_items)
        self._load_respmat()

    @property
    def bpm_enbllist(self):
        """."""
        sel_ = self.select_items
        return _np.hstack([sel_['bpmx'], sel_['bpmy']])

    @property
    def corrs_enbllist(self):
        """."""
        sel_ = self.select_items
        seleccor = _np.hstack([sel_['ch'], sel_['cv']])
        if self.acc == 'SI':
            seleccor = _np.hstack([seleccor, sel_['rf']])
        return seleccor

    def get_map2write(self):
        """Get the write methods of the class."""
        dbase = {
            'RespMat-SP': self.set_respmat,
            'CHEnblList-SP': _part(self.set_enbllist, 'ch'),
            'CVEnblList-SP': _part(self.set_enbllist, 'cv'),
            'BPMXEnblList-SP': _part(self.set_enbllist, 'bpmx'),
            'BPMYEnblList-SP': _part(self.set_enbllist, 'bpmy'),
            'NrSingValues-SP': self.set_num_sing_values,
            }
        if self.acc == 'SI':
            dbase['RFEnbl-Sel'] = _part(self.set_enbllist, 'rf')
        return dbase

    def set_respmat(self, mat):
        """Set the response matrix in memory and save it in file."""
        msg = 'Setting New RespMat.'
        self._update_log(msg)
        _log.info(msg)
        mat, matb = self._set_respmat(mat)
        if mat is None:
            return False
        old_ = self.respmat.copy()
        self.respmat = mat
        if not self._calc_matrices():
            self.respmat = old_
            return False
        self.respmat_extended = matb
        self._save_respmat(matb)
        self.run_callbacks('RespMat-RB', list(self.respmat.ravel()))
        return True

    def _set_respmat(self, mat):
        mat = _np.array(mat, dtype=float)
        nrc = self._csorb.nr_corrs
        nrb = self._csorb.nr_bpms
        rext = self.ring_extension
        mat_rext = (mat.size // self._csorb.matrix_size)
        if mat.size % self._csorb.matrix_size:
            msg = 'ERR: Wrong RespMat Size.'
            self._update_log(msg)
            _log.error(msg[5:])
            return None, None
        elif mat_rext < rext:
            mat2 = _np.zeros([2, rext*self._csorb.nr_bpms, nrc], dtype=float)
            mat = mat.reshape(2, -1, nrc)
            mat2[:, :(mat_rext*nrb), :] = mat
            mat = mat2.reshape(-1)
            matb = mat
        elif mat_rext > rext:
            matb = mat
            mat = mat.reshape(2, -1, nrc)
            mat = mat[:, :(rext*nrb), :]
            mat = mat.reshape(-1)
        else:
            matb = mat
        mat = _np.reshape(mat, [-1, nrc])
        return mat, matb

    def set_enbllist(self, key, val):
        """."""
        msg = 'Setting {0:s} EnblList'.format(key.upper())
        self._update_log(msg)
        _log.info(msg)
        if key in {'bpmx', 'bpmy'}:
            new, newb = self._set_enbllist_bpms(key, val)
        elif key in {'ch', 'cv', 'rf'}:
            new, newb = self._set_enbllist(key, val)
        else:
            return False
        bkup = self.select_items[key]
        self.select_items[key] = new

        max_num = self.get_max_num_sing_values()
        num = self.num_sing_values
        num = num if num < max_num else max_num
        nrbkup = self.num_sing_values
        self.num_sing_values = num
        if not self._calc_matrices():
            self.num_sing_values = nrbkup
            self.select_items[key] = bkup
            return False
        self.select_items_extended[key] = newb
        if new.size == 1:  # Deal with RF
            self.run_callbacks(self.selection_pv_names[key], bool(new))
        else:
            self.run_callbacks(self.selection_pv_names[key], new)
        self.run_callbacks('NrSingValues-RB', self.num_sing_values)
        return True

    def _set_enbllist(self, key, val):
        bkup = self.select_items_extended[key]
        new = _np.array(val, dtype=bool)
        if key == 'rf':
            pass
        elif new.size >= bkup.size:
            new = new[:bkup.size]
        else:
            new2 = bkup.copy()
            new2[:new.size] = new
            new = new2
        return new, new.copy()

    def _set_enbllist_bpms(self, key, val):
        bkup = self.select_items_extended[key]
        new = _np.array(val, dtype=bool)
        if new.size < bkup.size:
            new2 = bkup.copy()
            new2[:new.size] = new
            new = new2
        nrb = self._csorb.nr_bpms
        nrb *= self.ring_extension
        if new.size < nrb:
            new2 = _np.zeros(nrb, dtype=bool)
            new2[:new.size] = new
            newb = new2
            new = new2.copy()
        elif new.size > nrb:
            newb = new
            new = new[:nrb]
        else:
            newb = new
        return new, newb

    def set_ring_extension(self, val):
        """."""
        val = 1 if val < 1 else int(val)
        val = self._csorb.MAX_RINGSZ if val > self._csorb.MAX_RINGSZ else val
        if val == self.ring_extension:
            return True
        bkup = self.ring_extension
        self.ring_extension = val
        mat, matb = self._set_respmat(self.respmat_extended)
        self.respmat = mat
        selbs = dict()
        sellist = ('bpmx', 'bpmy')
        for k in sellist:
            val = self.select_items_extended[k]
            sel, selbs[k] = self._set_enbllist_bpms(k, val)
            self.select_items[k] = sel

        if not self._calc_matrices():
            self.ring_extension = bkup
            self.respmat, _ = self._set_respmat(self.respmat_extended)
            for k in sellist:
                val = self.select_items_extended[k]
                self.select_items[k], _ = self._set_enbllist_bpms(k, val)
            return False

        self.respmat_extended = matb
        self.select_items_extended.update(selbs)
        self.run_callbacks('RespMat-RB', list(self.respmat.ravel()))
        for k in sellist:
            val = self.select_items[k]
            pvname = self.selection_pv_names[k]
            self.run_callbacks(pvname, val)
            pvname = pvname.replace('-RB', '-SP')
            self.run_callbacks(pvname, val)
        return True

    def calc_kicks(self, orbit):
        """Calculate the kick from the orbit distortion given."""
        if len(orbit) != self.inv_respmat.shape[1]:
            msg = 'ERR: Orbit and matrix size not compatible.'
            self._update_log(msg)
            _log.error(msg[5:])
            return
        kicks = _np.dot(-self.inv_respmat, orbit)
        nr_ch = self._csorb.nr_ch
        nr_chcv = self._csorb.nr_chcv
        self.run_callbacks('DeltaKickCH-Mon', list(kicks[:nr_ch]))
        self.run_callbacks('DeltaKickCV-Mon', list(kicks[nr_ch:nr_chcv]))
        if self.acc == 'SI':
            self.run_callbacks('DeltaKickRF-Mon', kicks[-1])
        return kicks

    def set_num_sing_values(self, num):
        """."""
        num = int(num) if int(num) > 0 else 1
        max_num = self.get_max_num_sing_values()
        num = num if num < max_num else max_num
        bkup = self.num_sing_values
        self.num_sing_values = num
        if not self._calc_matrices():
            self.num_sing_values = bkup
            return False
        self.run_callbacks('NrSingValues-RB', self.num_sing_values)
        return True

    def get_max_num_sing_values(self):
        """."""
        ncorr = _np.sum(self.select_items['ch'])
        ncorr += _np.sum(self.select_items['cv'])
        if self.acc == 'SI':
            ncorr += _np.sum(self.select_items['rf'])
        nbpm = _np.sum(self.select_items['bpmx'])
        nbpm += _np.sum(self.select_items['bpmy'])
        return min(ncorr, nbpm)

    def _calc_matrices(self):
        msg = 'Calculating Inverse Matrix.'
        self._update_log(msg)
        _log.info(msg)
        selecbpm = self.bpm_enbllist
        seleccor = self.corrs_enbllist
        if not any(selecbpm):
            msg = 'ERR: No BPM selected in EnblList'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        if not any(seleccor):
            msg = 'ERR: No Corrector selected in EnblList'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        sel_mat = selecbpm[:, None] * seleccor[None, :]
        if sel_mat.size != self.respmat.size:
            return False
        mat = self.respmat[sel_mat]
        mat = _np.reshape(mat, [sum(selecbpm), sum(seleccor)])
        try:
            uuu, sing, vvv = _np.linalg.svd(mat, full_matrices=False)
        except _np.linalg.LinAlgError():
            msg = 'ERR: Could not calculate SVD'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        inv_s = 1/sing
        nsv = _np.isfinite(inv_s).sum()
        if not nsv:
            msg = 'ERR: All Singular Values are zero.'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        elif nsv < self.num_sing_values:
            self.num_sing_values = nsv
            self.run_callbacks('NrSingValues-SP', nsv)
            self.run_callbacks('NrSingValues-RB', nsv)
            msg = 'WARN: NrSingValues had to be set to {0:d}.'.format(nsv)
            self._update_log(msg)
            _log.warning(msg[6:])
        inv_s[self.num_sing_values:] = 0
        inv_mat = _np.dot(vvv.T*inv_s, uuu.T)
        is_nan = _np.any(_np.isnan(inv_mat))
        is_inf = _np.any(_np.isinf(inv_mat))
        if is_nan or is_inf:
            msg = 'ERR: Inverse contains nan or inf.'
            self._update_log(msg)
            _log.error(msg[5:])
            return False

        self.sing_values[:] = 0
        self.sing_values[:len(sing)] = sing
        self.run_callbacks('SingValues-Mon', list(self.sing_values))
        self.inv_respmat = _np.zeros(self.respmat.shape, dtype=float).T
        self.inv_respmat[sel_mat.T] = inv_mat.ravel()
        self.run_callbacks('InvRespMat-Mon', list(self.inv_respmat.ravel()))
        msg = 'Ok!'
        self._update_log(msg)
        _log.info(msg)
        return True

    def _load_respmat(self):
        filename = self._csorb.respmat_fname
        boo = False
        if _os.path.isfile(filename):
            boo = self.set_respmat(_np.loadtxt(filename))
            if boo:
                msg = 'Loading RespMat from file.'
            else:
                msg = 'ERR: Problem loading RespMat from file.'
            self._update_log(msg)
            _log.info(msg)

    def _save_respmat(self, mat):
        path = _os.path.split(self._csorb.respmat_fname)[0]
        if not _os.path.isdir(path):
            _os.mkdir(path)
        _np.savetxt(self._csorb.respmat_fname, mat)

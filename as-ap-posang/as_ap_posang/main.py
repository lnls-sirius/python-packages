"""Main module of AS-AP-PosAng IOC."""

import time as _time
import epics as _epics
import siriuspy as _siriuspy
from siriuspy.servconf.conf_service import ConfigService as _ConfigService
import as_ap_posang.pvs as _pvs

# Coding guidelines:
# =================
# 01 - pay special attention to code readability
# 02 - simplify logic as much as possible
# 03 - unroll expressions in order to simplify code
# 04 - dont be afraid to generate simingly repeatitive flat code (they may be
#      easier to read!)
# 05 - 'copy and paste' is your friend and it allows you to code 'repeatitive'
#      (but clearer) sections fast.
# 06 - be consistent in coding style (variable naming, spacings, prefixes,
#      suffixes, etc)


# Constants
_ALLSET = 0xf
_ALLCLR = 0x0


class App:
    """Main application for handling injection in transport lines."""

    pvs_database = None

    def __init__(self, driver):
        """Class constructor."""
        _pvs.print_banner_and_save_pv_list()

        self._TL = _pvs.get_pvs_section()
        self._PREFIX_VACA = _pvs.get_pvs_vaca_prefix()
        self._PREFIX = _pvs.get_pvs_prefix()

        self._driver = driver

        self._status = _ALLSET
        self._orbx_deltapos = 0
        self._orby_deltapos = 0
        self._orbx_deltaang = 0
        self._orby_deltaang = 0
        self._setnewrefkick_cmd_count = 0
        self._config_ma_cmd_count = 0

        self._corr_check_connection = 4*[0]
        self._corr_check_pwrstate_sts = 4*[0]
        self._corr_check_opmode_sts = [1, 0, 1, 1]
        self._corr_check_ctrlmode_mon = 4*[1]

        config_name = self._get_config_name()
        [done, corrparams] = self._get_corrparams(config_name)
        if done:
            self.driver.setParam('ConfigName-SP', config_name)
            self.driver.setParam('ConfigName-RB', config_name)
            self._respmat_x = corrparams[0]
            self.driver.setParam('RespMatX-Mon', corrparams[0])
            self._respmat_y = corrparams[1]
            self.driver.setParam('RespMatY-Mon', corrparams[1])

        # The correctors are listed as:
        # First horizontal corretor, second horizontal corretor,
        # first vertical corretor and second vertical corretor.
        self._correctors = ['', '', '', '']
        if self._TL == 'TS':
            self._correctors[0] = 'TS-04:MA-CH'
            self._correctors[1] = 'TS-04:PM-InjSeptF'
            self._correctors[2] = 'TS-04:MA-CV-1'
            self._correctors[3] = 'TS-04:MA-CV-2'

        elif self._TL == 'TB':
            self._correctors[0] = 'TB-03:MA-CH'
            self._correctors[1] = 'TB-04:PM-InjSept'
            self._correctors[2] = 'TB-04:MA-CV-1'
            self._correctors[3] = 'TB-04:MA-CV-2'

        # Connect to correctors
        self._corr_kick_sp_pvs = {}
        self._corr_kick_rb_pvs = {}
        self._corr_pwrstate_sel_pvs = {}
        self._corr_pwrstate_sts_pvs = {}
        self._corr_opmode_sel_pvs = {}
        self._corr_opmode_sts_pvs = {}
        self._corr_ctrlmode_mon_pvs = {}
        self._corr_refkick = {}

        for corr in self._correctors:
            corr_index = self._correctors.index(corr)

            self._corr_kick_sp_pvs[corr] = _epics.PV(
                self._PREFIX_VACA + corr + ':Kick-SP')

            self._corr_refkick[corr] = 0
            self._corr_kick_rb_pvs[corr] = _epics.PV(
                self._PREFIX_VACA + corr + ':Kick-RB',
                callback=self._callback_init_refkick,
                connection_callback=self._connection_callback_corr_kick_pvs)

            self._corr_pwrstate_sel_pvs[corr] = _epics.PV(
                self._PREFIX_VACA + corr + ':PwrState-Sel')
            self._corr_pwrstate_sts_pvs[corr] = _epics.PV(
                self._PREFIX_VACA + corr + ':PwrState-Sts',
                callback=self._callback_corr_pwrstate_sts)

            self._corr_opmode_sel_pvs[corr] = _epics.PV(
                self._PREFIX_VACA + corr + ':OpMode-Sel')

            if corr_index != 1:
                self._corr_opmode_sts_pvs[corr] = _epics.PV(
                    self._PREFIX_VACA + corr + ':OpMode-Sts',
                    callback=self._callback_corr_opmode_sts)
            else:
                self._corr_opmode_sts_pvs[corr] = _epics.PV(
                    self._PREFIX_VACA + corr + ':OpMode-Sts')

            self._corr_ctrlmode_mon_pvs[corr] = _epics.PV(
                self._PREFIX_VACA + corr + ':CtrlMode-Mon',
                callback=self._callback_corr_ctrlmode_mon)

        self.driver.setParam('Log-Mon', 'Started.')
        self.driver.updatePVs()

    @staticmethod
    def init_class():
        """Init class."""
        App.pvs_database = _pvs.get_pvs_database()

    @property
    def driver(self):
        """Return driver."""
        return self._driver

    def process(self, interval):
        """Sleep."""
        _time.sleep(interval)

    def read(self, reason):
        """Read from IOC database."""
        return None

    def write(self, reason, value):
        """Write value to reason and let callback update PV database."""
        status = False
        if reason == 'DeltaPosX-SP':
            updated = self._update_delta(
                value, self._orbx_deltaang,
                self._respmat_x,
                self._corr_kick_sp_pvs[self._correctors[0]],
                self._corr_kick_sp_pvs[self._correctors[1]],
                self._corr_refkick[self._correctors[0]],
                self._corr_refkick[self._correctors[1]])
            if updated:
                self._orbx_deltapos = value
                self.driver.setParam('DeltaPosX-RB', value)
                self.driver.updatePVs()
                status = True

        elif reason == 'DeltaAngX-SP':
            updated = self._update_delta(
                self._orbx_deltapos, value,
                self._respmat_x,
                self._corr_kick_sp_pvs[self._correctors[0]],
                self._corr_kick_sp_pvs[self._correctors[1]],
                self._corr_refkick[self._correctors[0]],
                self._corr_refkick[self._correctors[1]])
            if updated:
                self._orbx_deltaang = value
                self.driver.setParam('DeltaAngX-RB', value)
                self.driver.updatePVs()
                status = True

        elif reason == 'DeltaPosY-SP':
            updated = self._update_delta(
                value, self._orby_deltaang,
                self._respmat_y,
                self._corr_kick_sp_pvs[self._correctors[2]],
                self._corr_kick_sp_pvs[self._correctors[3]],
                self._corr_refkick[self._correctors[2]],
                self._corr_refkick[self._correctors[3]])
            if updated:
                self._orby_deltapos = value
                self.driver.setParam('DeltaPosY-RB', value)
                self.driver.updatePVs()
                status = True

        elif reason == 'DeltaAngY-SP':
            updated = self._update_delta(
                self._orby_deltapos, value,
                self._respmat_y,
                self._corr_kick_sp_pvs[self._correctors[2]],
                self._corr_kick_sp_pvs[self._correctors[3]],
                self._corr_refkick[self._correctors[2]],
                self._corr_refkick[self._correctors[3]])
            if updated:
                self._orby_deltaang = value
                self.driver.setParam('DeltaAngY-RB', value)
                self.driver.updatePVs()
                status = True

        elif reason == 'SetNewRefKick-Cmd':
            updated = self._update_ref()
            if updated:
                self._setnewrefkick_cmd_count += 1
                self.driver.setParam('SetNewRefKick-Cmd',
                                     self._setnewrefkick_cmd_count)
                self.driver.updatePVs()

        elif reason == 'ConfigMA-Cmd':
            done = self._config_ma()
            if done:
                self._config_ma_cmd_count += 1
                self.driver.setParam('ConfigMA-Cmd',
                                     self._config_ma_cmd_count)
                self.driver.updatePVs()

        elif reason == 'ConfigName-SP':
            [done, corrparams] = self._get_corrparams(value)
            if done:
                self._set_config_name(value)
                self.driver.setParam('ConfigName-RB', value)
                self._respmat_x = corrparams[0]
                self.driver.setParam('RespMatX-Mon', corrparams[0])
                self._respmat_y = corrparams[1]
                self.driver.setParam('RespMatY-Mon', corrparams[1])
                updated = self._update_delta(
                    self._orbx_deltapos, self._orbx_deltaang,
                    self._respmat_x,
                    self._corr_kick_sp_pvs[self._correctors[0]],
                    self._corr_kick_sp_pvs[self._correctors[1]],
                    self._corr_refkick[self._correctors[0]],
                    self._corr_refkick[self._correctors[1]])
                updated = self._update_delta(
                    self._orby_deltapos, self._orby_deltaang,
                    self._respmat_y,
                    self._corr_kick_sp_pvs[self._correctors[2]],
                    self._corr_kick_sp_pvs[self._correctors[3]],
                    self._corr_refkick[self._correctors[2]],
                    self._corr_refkick[self._correctors[3]])
                self.driver.setParam('Log-Mon', 'Updated correction matrices.')
                self.driver.updatePVs()
                status = True
            else:
                self.driver.setParam(
                    'Log-Mon', 'ERR:Configuration not found in configdb.')
                self.driver.updatePVs()  # in case PV states change.

        return status  # return True to invoke super().write of PCASDriver

    def _get_corrparams(self, config_name):
        """Get response matrix from configurations database."""
        cs = _ConfigService()
        querry = cs.get_config(self._TL.lower()+'_posang_respm', config_name)
        querry_result = querry['code']

        if querry_result == 200:
            done = True
            mats = querry['result']['value']
            respmat_x = [item for sublist in mats['respm-x']
                         for item in sublist]
            respmat_y = [item for sublist in mats['respm-y']
                         for item in sublist]
            return [done, [respmat_x, respmat_y]]
        else:
            done = False
            return [done, []]

    def _get_config_name(self):
        f = open('/home/fac_files/lnls-sirius/machine-applications'
                 '/as-ap-posang/as_ap_posang/' + self._TL.lower() +
                 '-posang.txt', 'r')
        config_name = f.read().strip('\n')
        f.close()
        return config_name

    def _set_config_name(self, config_name):
        f = open('/home/fac_files/lnls-sirius/machine-applications'
                 '/as-ap-posang/as_ap_posang/' + self._TL.lower() +
                 '-posang.txt', 'w')
        f.write(config_name)
        f.close()

    def _update_delta(self, delta_pos, delta_ang, respmat, c1_kick_sp_pv,
                      c2_kick_sp_pv, c1_refkick, c2_refkick):
        if self._status == _ALLCLR:
            delta_pos_meters = delta_pos/1000
            delta_ang_rad = delta_ang/1000
            c1_refkick_rad = c1_refkick/1000
            c2_refkick_rad = c2_refkick/1000

            det = respmat[0] * respmat[3] - respmat[1] * respmat[2]
            delta_kick_c1 = (respmat[3] * delta_pos_meters-respmat[1] *
                             delta_ang_rad) / det
            delta_kick_c2 = (-respmat[2]*delta_pos_meters+respmat[0] *
                             delta_ang_rad) / det

            c1_kick_sp_pv.put(c1_refkick_rad + delta_kick_c1)
            c2_kick_sp_pv.put(c2_refkick_rad + delta_kick_c2)

            self.driver.setParam('Log-Mon', 'Applied new delta.')
            self.driver.updatePVs()
            return True
        else:
            self.driver.setParam('Log-Mon',
                                 'ERR:Failed on applying new delta.')
            self.driver.updatePVs()
            return False

    def _update_ref(self):
        if (self._status & 0x1) == 0:  # Check connection
            # updates reference
            corr_id = ['CH1', 'CH2', 'CV1', 'CV2']
            for corr in self._correctors:
                corr_index = self._correctors.index(corr)
                value = self._corr_kick_rb_pvs[
                        self._correctors[corr_index]].get()
                # Convert correctors kick from rad to mrad
                self._corr_refkick[self._correctors[corr_index]] = value*1000
                self.driver.setParam('RefKick' + corr_id[corr_index] + '-Mon',
                                     value*1000)

            # the deltas from new kick references are zero
            self._orbx_deltapos = 0
            self.driver.setParam('DeltaPosX-SP', 0)
            self.driver.setParam('DeltaPosX-RB', 0)
            self._orbx_deltaang = 0
            self.driver.setParam('DeltaAngX-SP', 0)
            self.driver.setParam('DeltaAngX-RB', 0)
            self._orby_deltapos = 0
            self.driver.setParam('DeltaPosY-SP', 0)
            self.driver.setParam('DeltaPosY-RB', 0)
            self._orby_deltaang = 0
            self.driver.setParam('DeltaAngY-SP', 0)
            self.driver.setParam('DeltaAngY-RB', 0)

            self.driver.setParam('Log-Mon', 'Updated Kick References.')
            updated = True
        else:
            self.driver.setParam('Log-Mon', 'ERR:Some pv is disconnected.')
            updated = False
        self.driver.updatePVs()
        return updated

    def _callback_init_refkick(self, pvname, value, cb_info, **kws):
        """Initialize RefKick-Mon pvs and remove this callback."""
        ps = pvname.split(self._PREFIX_VACA)[1]
        corr = ps.split(':')[0]+':'+ps.split(':')[1]
        corr_index = self._correctors.index(corr)

        # Get reference. Convert correctors kick from rad to mrad.
        self._corr_refkick[self._correctors[corr_index]] = value*1000
        corr_id = ['CH1', 'CH2', 'CV1', 'CV2']
        self.driver.setParam('RefKick' + corr_id[corr_index] + '-Mon',
                             self._corr_refkick[self._correctors[corr_index]])

        # Remove callback
        cb_info[1].remove_callback(cb_info[0])

    def _connection_callback_corr_kick_pvs(self, pvname, conn, **kws):
        ps = pvname.split(self._PREFIX_VACA)[1]
        if not conn:
            self.driver.setParam('Log-Mon', 'WARN:'+ps+' disconnected.')
            self.driver.updatePVs()

        corr = ps.split(':')[0]+':'+ps.split(':')[1]
        corr_index = self._correctors.index(corr)
        self._corr_check_connection[corr_index] = (1 if conn else 0)

        # Change the first bit of correction status
        if any(q == 0 for q in self._corr_check_connection):
            self._status = _siriuspy.util.update_integer_bit(
                integer=self._status, number_of_bits=4, value=1, bit=0)
        else:
            self._status = _siriuspy.util.update_integer_bit(
                integer=self._status, number_of_bits=4, value=0, bit=0)
        self.driver.setParam('Status-Mon', self._status)
        self.driver.updatePVs()

    def _callback_corr_pwrstate_sts(self, pvname, value, **kws):
        ps = pvname.split(self._PREFIX_VACA)[1]
        if value == 0:
            self.driver.setParam('Log-Mon', 'WARN:'+ps+' is Off.')

        corr = ps.split(':')[0]+':'+ps.split(':')[1]
        corr_index = self._correctors.index(corr)
        self._corr_check_pwrstate_sts[corr_index] = value

        # Change the second bit of correction status
        if any(q == 0 for q in self._corr_check_pwrstate_sts):
            self._status = _siriuspy.util.update_integer_bit(
                integer=self._status, number_of_bits=4, value=1, bit=1)
        else:
            self._status = _siriuspy.util.update_integer_bit(
                integer=self._status, number_of_bits=4, value=0, bit=1)
        self.driver.setParam('Status-Mon', self._status)
        self.driver.updatePVs()

    def _callback_corr_opmode_sts(self, pvname, value, **kws):
        ps = pvname.split(self._PREFIX_VACA)[1]
        self.driver.setParam('Log-Mon', 'WARN:'+ps+' changed.')
        self.driver.updatePVs()

        corr = ps.split(':')[0]+':'+ps.split(':')[1]
        corr_index = self._correctors.index(corr)
        self._corr_check_opmode_sts[corr_index] = value

        # Change the third bit of correction status
        if any(s != 0 for s in self._corr_check_opmode_sts):
            self._status = _siriuspy.util.update_integer_bit(
                integer=self._status, number_of_bits=4, value=1, bit=2)
        else:
            self._status = _siriuspy.util.update_integer_bit(
                integer=self._status, number_of_bits=4, value=0, bit=2)
        self.driver.setParam('Status-Mon', self._status)
        self.driver.updatePVs()

    def _callback_corr_ctrlmode_mon(self,  pvname, value, **kws):
        ps = pvname.split(self._PREFIX_VACA)[1]
        if value == 1:
            self.driver.setParam('Log-Mon', 'WARN:'+ps+' is Local.')
            self.driver.updatePVs()

        corr = ps.split(':')[0]+':'+ps.split(':')[1]
        corr_index = self._correctors.index(corr)
        self._corr_check_ctrlmode_mon[corr_index] = value

        # Change the fourth bit of correction status
        if any(q == 1 for q in self._corr_check_ctrlmode_mon):
            self._status = _siriuspy.util.update_integer_bit(
                integer=self._status, number_of_bits=4, value=1, bit=3)
        else:
            self._status = _siriuspy.util.update_integer_bit(
                integer=self._status, number_of_bits=4, value=0, bit=3)
        self.driver.setParam('Status-Mon', self._status)
        self.driver.updatePVs()

    def _config_ma(self):
        for corr in self._correctors:
            corr_index = self._correctors.index(corr)
            if self._corr_pwrstate_sel_pvs[corr].connected:
                self._corr_pwrstate_sel_pvs[corr].put(1)
                if corr_index != 1:
                    self._corr_opmode_sel_pvs[corr].put(0)
            else:
                self.driver.setParam('Log-Mon',
                                     'ERR:' + corr + ' is disconnected.')
                self.driver.updatePVs()
                return False
        self.driver.setParam('Log-Mon', 'Sent configuration to correctors.')
        self.driver.updatePVs()
        return True

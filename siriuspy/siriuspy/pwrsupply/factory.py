"""Power Supply factory classes."""

import time as _time
import re as _re
from copy import deepcopy as _deepcopy

from ..search import PSSearch as _PSSearch
from ..thread import DequeThread as _DequeThread
from ..bsmp.serial import Channel as _Channel

from .csdev import get_ps_propty_database as _get_ps_propty_database
from .beaglebone import BeagleBone as _BeagleBone
from .siggen import SigGenFactory as _SigGenfactory

from .bsmp.factory import PSBSMPFactory as _PSBSMPFactory

from .pructrl.pru import PRU as _PRU
from .pructrl.prucontroller import PRUController as _PRUController

from .psctrl.pscreaders import Constant as _Constant
from .psctrl.pscwriters import Setpoint as _Setpoint
from .psctrl.psmodel import PSModelFactory as _PSModelFactory


class BBBFactory:
    """BeagleBone factory."""

    # regexp of constant PVs whose initializations require bsmp communications.
    _regexp_constant_bsmp_init = _re.compile('^(Param|Version).*-Cte$')

    @staticmethod
    def create(ethbridgeclnt_class, bbbname=None):
        """Return BBB object."""
        # create timestamp used in all TimestampBoot-Cte PVs
        timestamp = _time.time()

        # create PRU used for low-level communication
        pru = _PRU(ethbridgeclnt_class, bbbname=bbbname)

        # create DequeThread that queue all serial operations
        prucqueue = _DequeThread()

        # build dicts for grouped udc.
        psmodels, devices, freqs = \
            BBBFactory._build_udcgrouped(bbbname)

        if len(psmodels) > 1:
            # more than one psmodel under the same beagle. there will be two 
            # PRUController objects pushing operation requests into the common 
            # DequeThread. we have to use to lock mechanism in bsmp.Channel in 
            # order to avoid one PRUController process thread interpreting the
            # operation request of the other PRUController scan thread.
            _Channel.create_lock()

        # power supply controllers and databases
        # dbase: a pvname-epicsdbase dictionary containing all
        # beaglebone PVs. the epics server database is initialized
        # using this dictionary.
        controllers, databases, dbase = \
            BBBFactory._build_controllers(
                timestamp, pru, prucqueue, psmodels, devices, freqs)

        return _BeagleBone(controllers, databases), dbase

    # --- private methods ---

    @staticmethod
    def _build_controllers(
            timestamp, pru, prucqueue, psmodels, devices, freqs):

        # dbase is a pvname to epics dbase dictionary will all PVs
        dbase = dict()
        controllers = dict()  # one controller per psmodel
        databases = dict()  # controllers databases

        for psmodel_name, psmodel in psmodels.items():

            # devices of that ps model
            devs = devices[psmodel_name]

            # create pru controller for devices
            freq = freqs[psmodel_name]
            freq = None if freq == 0 else freq
            pru_controller = _PRUController(pru, prucqueue,
                                            psmodel, devs,
                                            processing=False,
                                            scanning=False,
                                            freq=freq,
                                            init=False)

            devname2devid = dict()
            readers, writers = dict(), dict()

            for device in devs:

                # psname and bsmp device id
                psname, devid = device

                # get model database
                pstype = _PSSearch.conv_psname_2_pstype(psname)
                database = _get_ps_propty_database(psmodel_name, pstype)

                # build setpoints
                setpoints = BBBFactory._build_setpoints(
                    (device, ), database)

                # build readers and writers and add them to dicts
                _readers, _writers = BBBFactory._build_readers_writers(
                    timestamp, dbase, psmodel, setpoints, (device, ), database,
                    pru_controller)
                _ = readers.update(_readers), writers.update(_writers)

                # build device_ids dict
                devname2devid[psname] = devid

                # add database to dictionary
                databases[psname] = database

            # build controller
            controller = psmodel.controller(
                readers, writers, pru_controller, devname2devid)

            # add controller to dictionary
            for device in devs:
                psname, devid = device
                controllers[psname] = controller

        return controllers, databases, dbase

    @staticmethod
    def _build_udcgrouped(bbbname):

        # get names of all udcs under a beaglebone
        udcs = _PSSearch.conv_bbbname_2_udc(bbbname)
        
        psmodels, devices, freqs = dict(), dict(), dict()
        for udc in udcs:

            # add udc devices
            devs = _PSSearch.conv_udc_2_bsmps(udc)
            print('UDC: ', udc, ', DEVICES: ', devs)
            psmodel_name = BBBFactory._check_psmodels(devs)
            if psmodel_name in psmodels:
                devices[psmodel_name].extend(devs)
            else:
                devices[psmodel_name] = devs

            # add udc psmodel
            if psmodel_name not in psmodels:
                psmodel = _PSModelFactory.create(psmodel_name)
                psmodels[psmodel_name] = psmodel

            # add udc/bbb freqs
            try:
                freq = _PSSearch.conv_bbbname_2_freq(udc)
            except KeyError:
                try:
                    freq = _PSSearch.conv_bbbname_2_freq(bbbname)
                except KeyError:
                    freq = 0.0
            if psmodel_name not in freqs:
                freqs[psmodel_name] = freq
            else:
                freqs[psmodel_name] = max(freqs[psmodel_name], freq)

        return psmodels, devices, freqs

    @staticmethod
    def _build_setpoints(devices, database):
        # Build pvname-setpoints dictionary
        setpoints = dict()
        for field in database:
            for device in devices:
                devname = device[0]
                if _Setpoint.match(field):
                    setpoints[devname + ':' + field] = \
                        _Setpoint(field, database[field])
        return setpoints

    @staticmethod
    def _build_readers_writers(
            timestamp, dbase, model, setpoints, devices, database,
            pru_controller):

        readers, writers = dict(), dict()

        for field in database:
            if _Setpoint.match(field):
                # writers for setpoint field
                field_writers = \
                    BBBFactory._get_writers(
                        model, field, devices, setpoints, pru_controller)
                writers.update(field_writers)
                # corresponding readers
                for devname, devid in devices:
                    pvname = devname + ':' + field
                    dbase[pvname] = _deepcopy(database[field])
                    readers[pvname] = setpoints[pvname]
            elif _Constant.match(field) and \
                    not BBBFactory._regexp_constant_bsmp_init.match(field):
                # readers for const fields whose initializations
                # do not require bsmp communication
                for devname, devid in devices:
                    if field == 'TimestampBoot-Cte':
                        # update bootime in epics database with timestamp
                        database[field]['value'] = timestamp
                    pvname = devname + ':' + field
                    readers[pvname] = _Constant(database[field]['value'])
                    dbase[pvname] = _deepcopy(database[field])
            else:
                # readers for other fields
                for devname, devid in devices:
                    pvname = devname + ':' + field
                    dbase[pvname] = _deepcopy(database[field])
                    readers[pvname] = model.reader(
                        devid, field, pru_controller)
        return readers, writers

    @staticmethod
    def _check_psmodels(devices):
        """Check number of ps models.

        Raise exception in case the given devices have more than on psmodel
        type.
        """
        name2model = _PSSearch.conv_psname_2_psmodel
        psmodels = {name2model(psname) for psname, bsmp_id in devices}
        if len(psmodels) > 1:
            raise ValueError('Different psmodels in the same UDC')
        return psmodels.pop()

    @staticmethod
    def _get_writers(
            model, field, devices, setpoints, pru_controller):
        # NOTE: Each pwrsupply should have all variables independent
        #       in the near future.
        # if field in ('CycleType-Sel', 'CycleNrCycles-SP',
        #              'CycleFreq-SP', 'CycleAmpl-SP',
        #              'CycleOffset-SP', 'CycleAuxParam-SP'):
        #     # Make one object for all devices (UDC-shared)
        #     ids, sps = list(), list()
        #     for devname, devid in devices:
        #         pvname = devname + ':' + field
        #         ids.append(devid)
        #         sps.append(setpoints[pvname])
        #     writer = model.writer(
        #         ids, field, pru_controller, _Setpoints(sps))
        #     return {device[0] + ':' + field: writer
        #             for device in devices}
        writers = dict()
        for devname, devid in devices:
            setpoint = setpoints[devname + ':' + field]
            writers[devname + ':' + field] = model.writer(
                [devid], field, pru_controller, setpoint)
        return writers


class PSBSMPFactory:
    """Power supply BSMP factory.

    Class methods create return BSMP objects whose methods can be used to
    communicate with a given power supply,
    """

    @staticmethod
    def create(psname, pru=None):
        """."""
        udc = _PSSearch.conv_bbbname_2_udc(psname)
        psnames, devids = zip(*_PSSearch.conv_udc_2_bsmps(udc))
        idx = psnames.index(psname)

        # device ID and PS model
        devid = devids[idx]
        psmodel = _PSSearch.conv_psname_2_psmodel(psname)

        # pru
        if pru is None:
            bbbname = _PSSearch.conv_psname_2_bbbname(psname)
            pru = _PRU(bbbname)

        psbsmp = _PSBSMPFactory.create(
            psmodel=psmodel, slave_address=devid, pru=pru)

        return psbsmp


# Expose SigGenFactory class here
SigGenFactory = _SigGenfactory

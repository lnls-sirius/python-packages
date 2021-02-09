"""BSMP protocol implementation."""
from . import constants as _const
from .serial import Channel as _Channel
from .serial import Message as _Message
from .exceptions import SerialAnomResp as _SerialAnomResp


class BSMP:
    """BSMP protocol implementation for Master Node."""

    _timeout_execute_function = 100  # [ms]

    def __init__(self, pru, slave_address, entities):
        """_cructor."""
        self._entities = entities
        self._channel = _Channel(pru, slave_address)

    @property
    def entities(self):
        """Return BSMP entities."""
        return self._entities

    @property
    def channel(self):
        """Return serial channel to an address."""
        return self._channel

    # 0x0_
    def query_protocol_version(self):
        """Consult protocol version. Command 0x00."""
        # TODO: needs implementation!
        raise NotImplementedError()

    def query_list_of_variables(self):
        """Consult list of variables. Command 0x02."""
        # TODO: needs implementation!
        raise NotImplementedError()

    def query_list_of_group_of_variables(self, timeout):
        """Consult groups list. Command 0x04."""
        # command and expected response
        cmd, ack = _const.CMD_QUERY_LIST_OF_GROUP_OF_VARIABLES, \
            _const.CMD_LIST_OF_GROUP_OF_VARIABLES

        # build payload
        payload = []

        # send request package
        msg = _Message.message(cmd, payload=payload)
        res = self.channel.request(msg, timeout=timeout)

        # expected response
        if res.cmd == ack:
            groupdata = list()
            for groupchar in res.payload:
                byte = ord(groupchar)
                waccess = (byte & 0b10000000) > 0
                nrvars = (byte & 0b01111111)
                groupdata.append((waccess, nrvars))
            return _const.ACK_OK, groupdata

        # anomalous response
        return BSMP.anomalous_response(cmd, res.cmd)

    def query_group_of_variables(self, group_id, timeout):
        """Return id of the variables in the given group."""
        # command and expected response
        cmd, ack = _const.CMD_QUERY_GROUP_OF_VARIABLES, \
            _const.CMD_GROUP_OF_VARIABLES

        # build payload
        payload = [chr(group_id)]

        # send request package
        msg = _Message.message(cmd, payload=payload)
        res = self.channel.request(msg, timeout=timeout)

        # expected response
        if res.cmd == ack:
            return _const.ACK_OK, list(map(ord, res.payload))

        # anomalous response
        return BSMP.anomalous_response(cmd, res.cmd)

    def query_list_of_curves(self):
        """Consult curves_list. Command 0x08."""
        raise NotImplementedError()

    def query_curve_checksum(self, curve_id):
        """Consult curve checksum given curve id. Command 0x0A."""
        raise NotImplementedError()

    def query_list_of_functions(self):
        """Consult functions list. Command 0x0C."""
        raise NotImplementedError()

    # 0x1_
    def read_variable(self, var_id, timeout):
        """Read variable."""
        # command and expected response
        cmd, ack = _const.CMD_READ_VARIABLE, _const.CMD_VARIABLE_VALUE

        # build payload
        payload = [chr(var_id)]

        # send request package
        msg = _Message.message(cmd, payload=payload)
        res = self.channel.request(msg, timeout=timeout)

        if res.cmd == ack:
            variable = self.entities.variables[var_id]
            if len(res.payload) == variable.size:
                # expected response
                return _const.ACK_OK, variable.load_to_value(res.payload)
            # unexpected variable size
            fmts = 'Unexpected BSMP variable size for command 0x{:02X}: {}!'
            print(fmts.format(cmd, res.cmd))
            return None, None

        # anomalous response
        return BSMP.anomalous_response(
            cmd, res.cmd, var_id=var_id, payload=res.payload)

    def read_group_of_variables(self, group_id, timeout):
        """Read variable group."""
        # command and expected response
        cmd, ack = \
            _const.CMD_READ_GROUP_OF_VARIABLES, \
            _const.CMD_GROUP_OF_VARIABLES_VALUE

        # build payload
        payload = [chr(group_id)]

        # send request package
        msg = _Message.message(cmd, payload=payload)
        res = self.channel.request(msg, timeout=timeout)

        if res.cmd == ack:
            # expected response
            group = self.entities.groups[group_id]
            if len(res.payload) == group.variables_size():
                return _const.ACK_OK, group.load_to_value(res.payload)
            # unexpected group variables size
            return BSMP.anomalous_response(
                cmd, res.cmd,
                group_id=group_id,
                payload_len=len(res.payload),
                var_size=group.variables_size()
                )

        # anomalous response
        return BSMP.anomalous_response(cmd, res.cmd)

    # 0x2_
    def write_variable(self, var_id, value):
        """Write to variable. Command 0x20."""
        # TODO: needs implementation!
        raise NotImplementedError()

    def write_group_of_variables(self, group_id, value):
        """Write to the variables of a group. Command 0x22."""
        # TODO: needs implementation!
        raise NotImplementedError()

    def binoperation_variable(self, var_id, operation, mask):
        """Perform a binary operation to variable. Command 0x24."""
        # TODO: needs implementation!
        raise NotImplementedError()

    def binoperation_group(self, group_id, operation, mask):
        """Perform a binary oeration to the vars of a group. Command 0x26."""
        # TODO: needs implementation!
        raise NotImplementedError()

    def write_and_read_variable(self, w_var_id, r_var_id, value):
        """Write value to a var and read another var value. Command 0x28."""
        # TODO: needs implementation!
        raise NotImplementedError()

    # 0x3_
    def create_group_of_variables(self, var_ids, timeout):
        """Create new group with given variable ids."""
        cmd, ack = \
            _const.CMD_CREATE_GROUP_OF_VARIABLES, _const.ACK_OK

        print('-- create_group_of_variables --')
        print('address: ', self._channel.address)
        print('var_ids: ', var_ids)
        print()

        # build payload
        var_ids = sorted(var_ids)
        payload = [chr(var_id) for var_id in var_ids]

        # send request package
        msg = _Message.message(cmd, payload=payload)
        res = self.channel.request(msg, timeout=timeout)

        if res.cmd == ack:
            if not res.payload:
                # expected response
                # TODO: revise this. do we need to change entities?!
                # if so, should we make a local copy instead?
                self.entities.add_group(var_ids)
                return _const.ACK_OK, None
            # unexpected non-empty response payload
            fmts = ('Unexpected BSMP non-empty resp payload '
                    'for command 0x{:02X}: {}!')
            print(fmts.format(cmd, res.cmd))
            return None, None

        # anomalous response
        return BSMP.anomalous_response(cmd, res.cmd)

    def remove_all_groups_of_variables(self, timeout):
        """Remove all groups."""
        cmd, ack = \
            _const.CMD_REMOVE_ALL_GROUPS_OF_VARIABLES, _const.ACK_OK

        # build payload
        payload = []

        # send request package
        msg = _Message.message(cmd, payload=payload)
        res = self.channel.request(msg, timeout=timeout)

        if res.cmd == ack and not res.payload:
            # expected response
            # TODO: revise this. do we need to change entities?!
            # if so, should we make a local copy instead?
            self.entities.remove_all_groups_of_variables()
            return _const.ACK_OK, None

        # anomalous response
        return BSMP.anomalous_response(cmd, res.cmd, payload=res.payload)

    # 0x4_
    def request_curve_block(self, curve_id, block, timeout, print_error=True):
        """Read curve block."""
        # command and expected response
        cmd, ack = _const.CMD_REQUEST_CURVE_BLOCK, _const.CMD_CURVE_BLOCK

        # build payload
        lsb, hsb = block & 0xff, (block & 0xff00) >> 8
        payload = [chr(curve_id), chr(hsb), chr(lsb)]

        # send request package
        msg = _Message.message(cmd, payload=payload)
        res = self.channel.request(msg, timeout=timeout)

        if res.cmd == ack:
            data = res.payload[3:]
            curve = self.entities.curves[curve_id]
            if len(data) % curve.type.size:
                # unexpected curve size
                fmts = ('Curve size is not multiple of curve.type.size!\n'
                        ' received curce size: {}\n'
                        ' curve.type.size: {}')
                print(fmts.format(len(data), curve.type.size))
                return None, None
            cid = ord(res.payload[0])
            cblock = (ord(res.payload[1]) << 8) + ord(res.payload[2])
            if cid != curve_id or cblock != block:
                # unexpected curve id or block number
                fmts = ('Invalid curve id or block offset in response!\n'
                        ' expected - curve_id:{}, block_offset:{}\n'
                        ' received - curve_id:{}, block_offset:{}')
                print(fmts.format(curve_id, block, cid, cblock))
                return None, None

            # expected result
            data_float = curve.load_to_value(data)
            return _const.ACK_OK, data_float

        # anomalous response
        return BSMP.anomalous_response(cmd, res.cmd, print_error=print_error)

    def curve_block(self, curve_id, block, value, timeout):
        """Write to curve block."""
        # command and expected response
        cmd, ack = _const.CMD_CURVE_BLOCK, _const.ACK_OK

        # build payload
        curve = self.entities.curves[curve_id]
        lsb, hsb = block & 0xff, (block & 0xff00) >> 8
        payload = [chr(curve_id), chr(hsb), chr(lsb)] + \
            curve.value_to_load(value)

        # send request package
        msg = _Message.message(cmd, payload=payload)
        res = self.channel.request(msg, timeout=timeout)

        if res.cmd == ack:
            # expected response
            return res.cmd, res.payload

        # anomalous response
        return BSMP.anomalous_response(cmd, res.cmd)

    def recalculate_curve_checksum(self, curve_id, timeout):
        """Recalculate curve checksum."""
        # command and expected response
        cmd, ack = \
            _const.CMD_RECALCULATE_CURVE_CHECKSUM, _const.CMD_CURVE_CHECKSUM

        # build payload
        payload = [chr(curve_id)]

        # send request package
        msg = _Message.message(cmd, payload=payload)
        res = self.channel.request(msg, timeout=timeout)

        if res.cmd == ack:
            # expected response
            return res.cmd, res.payload

        # anomalous response
        return BSMP.anomalous_response(cmd, res.cmd)

    # 0x5_
    def execute_function(self, func_id, input_val=None,
                         timeout=_timeout_execute_function,
                         read_flag=True, print_error=True):
        """Execute a function.

        parameter:
            read_flag: whether to execute a read after a write.
        """
        # command and expected response
        cmd, ack = _const.CMD_EXECUTE_FUNCTION, _const.CMD_FUNCTION_RETURN

        # build payload
        function = self.entities.functions[func_id]
        payload = [chr(func_id)] + function.value_to_load(input_val)

        # send request package
        msg = _Message.message(cmd, payload=payload)
        res = self.channel.request(msg, timeout=timeout, read_flag=read_flag)

        # TODO: This should be temporary. It is used for ps F_RESET_UDC.
        # PS Firmware should change so that F_RESET_UDC returns ack.
        if not read_flag:
            return None

        if res.cmd == ack:
            # print(len(res.payload))
            # print(function.o_size)
            # print(res.payload)
            if len(res.payload) == function.o_size:
                # expected response
                return _const.ACK_OK, function.load_to_value(res.payload)
        if res.cmd == _const.CMD_FUNCTION_ERROR:
            # function error
            if len(res.payload) == 1:
                # return error code
                return res.cmd, res.payload[0]

        # anomalous response
        return BSMP.anomalous_response(
            cmd, res.cmd, func_id=func_id, print_error=print_error)

    @staticmethod
    def anomalous_response(cmd, ack, **kwargs):
        """Print information about anomalous response."""
        # response with error
        if _const.ACK_OK < ack <= _const.ACK_RESOURCE_BUSY:
            if 'print_error' not in kwargs or kwargs['print_error']:
                fmts = 'BSMP response (error) for command 0x{:02X}: 0x{:02X}!'
                print(fmts.format(cmd, ack))
                for key, value in kwargs.items():
                    print('{}: {}'.format(key, value))
            return ack, None

        # unexpected response, raise Exception
        if 'print_error' not in kwargs or kwargs['print_error']:
            fmts = 'BSMP response (unexpected) for command 0x{:02X}: 0x{:02X}!'
            print(fmts.format(cmd, ack))
            for key, value in kwargs.items():
                print('{}: {}'.format(key, value))
        raise _SerialAnomResp

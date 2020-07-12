"""BSMP entities."""
import struct as _struct

import numpy as _np


class Entity:
    """BSMP entity."""

    def _conv_value(self, fmt, value):
        if fmt == '<c':
            return value
        else:
            return [chr(c) for c in _struct.pack(fmt, value)]

    def _check_type(self, var_type, value):
        if not var_type.check(value):
            raise TypeError("{}, {}".format(var_type.type, value))

    def _calc_types_size(self, var_types):
        size = 0
        try:
            for var_type in var_types:
                size += var_type.size
        except TypeError:
            return var_types.size
        return size

    def _conv_value_to_load(self, var_types, size, values):
        if len(var_types) > 1:
            load = []
            for idx, value in enumerate(values):
                self._check_type(var_types[idx], value)
                load += self._conv_value(var_types[idx].fmt, value)
            while len(load) < size:
                load += chr(0)
            return load
        else:
            self._check_type(var_types[0], values[0])
            return self._conv_value(var_types[0].fmt, values[0])

    def _conv_load_to_value(self, var_types, size, load):
        # NOTE: optimize this critical function!
        load = [ord(c) for c in load]
        if len(var_types) > 1:
            values = []
            offset = 0
            for var_type in var_types:
                datum = load[offset:offset+var_type.size]
                values.append(_struct.unpack(var_type.fmt, bytes(datum))[0])
                offset += var_type.size
            return values
        else:
            return _struct.unpack(var_types[0].fmt, bytes(load))[0]


class Variable(Entity):
    """BSMP variable."""

    def __init__(self, eid, waccess, var_type, count=1):
        """Set variable properties."""
        if (var_type.size * count) > 128 or (var_type.size * count) < 1:
            errstr = ('Variable size incorrect: eid:{}, '
                      'vtype_size:{}, count:{}').format(eid, var_type.size,
                                                        count)
            raise ValueError(errstr)
        super().__init__()  # TODO: is it necessary?
        self.eid = eid
        self.waccess = waccess
        self.size = (var_type.size * count)  # 1..128 bytes
        self.type = var_type

        self._var_types = [var_type for _ in range(count)]

    def load_to_value(self, load):
        """Parse value from load."""
        return self._conv_load_to_value(self._var_types, self.size, load)

    def value_to_load(self, value):
        """Convert value to load."""
        if not isinstance(value, (list, tuple)):
            value = [value, ]
        return self._conv_value_to_load(self._var_types, self.size, value)


class VariablesGroup(Entity):
    """BSMP variables group entity."""

    ALL = 0
    READ_ONLY = 1
    WRITEABLE = 2

    def __init__(self, eid, waccess, variables):
        """Set group parameter."""
        super().__init__()
        self.eid = eid
        self.waccess = waccess
        self.size = len(variables)
        self.variables = variables

    def load_to_value(self, load):
        """Parse value from load."""
        value = list()
        offset = 0
        for variable in self.variables:
            i, j = offset, offset + variable.size
            value.append(variable.load_to_value(load[i:j]))
            offset += variable.size
        return value

    def value_to_load(self, value):
        """Parse load from value."""
        if len(value) != self.size:
            return []
        load = list()
        for i, variable in enumerate(self.variables):
            load.extend(variable.value_to_load(value[i]))
        return load

    def variables_size(self):
        """Return sum of variables size."""
        size = 0
        for variable in self.variables:
            size += variable.size
        return size


class Curve(Entity):
    """BSMP Curve entity."""

    def __init__(self, eid, waccess, var_type, nblocks, count):
        """Set curve properties."""
        super().__init__()
        self.eid = eid  # Entity ID
        self.waccess = waccess
        self.size = (var_type.size * count)  # 1..128 bytes
        self.type = var_type
        self.nblocks = nblocks  # Number of blocks
        self.max_size_t_float = self.nblocks * (self.size // self.type.size)
        self._var_types = [var_type for _ in range(count)]

    def load_to_value(self, load):
        """Parse value from load."""
        # print('self.size:', self.size)
        # print('len(self._var_types):', len(self._var_types))
        # print('self._var_types[0].size:', self._var_types[0].size)
        load = [ord(c) for c in load]
        values = []
        offset = 0
        for var_type in self._var_types:
            datum = load[offset:offset+var_type.size]
            values.append(_struct.unpack(var_type.fmt, bytes(datum))[0])
            offset += var_type.size
            if offset >= len(load):
                break
        return values

    def value_to_load(self, value):
        """Convert curve block number to load."""
        load = []
        for idx, val in enumerate(value):
            self._check_type(self._var_types[idx], val)
            load += self._conv_value(self._var_types[idx].fmt, val)
        return load

    def get_indices(self, data_length):
        """Return list of indices corresponding to data blocks."""
        block_len = self.size // self.type.size
        nblocks = int(_np.ceil(data_length / block_len))
        indices = []
        for i in range(nblocks-1):
            indices.append((block_len*i, block_len*(i+1)))
        indices.append((block_len*(nblocks-1), data_length))
        return indices


class Function(Entity):
    """BSMP function."""

    def __init__(self, eid, i_type, o_type):
        """Set function properties."""
        super().__init__()
        self.eid = eid
        i_size = self._calc_types_size(i_type)
        o_size = self._calc_types_size(o_type)
        if i_size < 0 or i_size > 64:
            raise ValueError("Input size {} is out of range".format(i_size))
        if o_size < 0 or o_size > 32:
            raise ValueError("Output size {} is out of range".format(o_size))
        self.i_size = i_size  # 0..64
        self.i_type = i_type
        self.o_size = o_size  # 0..32
        self.o_type = o_type

    def load_to_value(self, load):  # Parse output_size
        """Parse value from load."""
        if load is None or not load:
            return None
        # print('---')
        # print(self.o_type)
        # print(self.o_size)
        # print(load)
        return self._conv_load_to_value(self.o_type, self.o_size, load)

    def value_to_load(self, value):
        """Convert value to load."""
        if value is None:
            return []
        if not isinstance(value, (list, tuple)):
            value = [value, ]
        return self._conv_value_to_load(self.i_type, self.i_size, value)


class Entities:
    """BSMP entities."""

    def __init__(self, variables, curves, functions):
        """Constructor."""
        # Get variables
        self._variables = list()
        for variable in variables:
            var_id = variable['eid']
            waccess = variable['waccess']
            var_type = variable['var_type']
            count = variable['count']
            self.variables.append(
                Variable(var_id, waccess, var_type, count))

        # Standard groups
        self._groups = list()
        self.reset_group()

        self._curves = list()
        for curve in curves:
            curve_id = curve['eid']
            waccess = curve['waccess']
            nblocks = curve['nblocks']
            count = curve['count']
            var_type = curve['var_type']
            self.curves.append(
                Curve(curve_id, waccess, var_type, nblocks, count))

        self._functions = list()
        for function in functions:
            func_id = function['eid']
            i_type = function['i_type']
            o_type = function['o_type']
            self.functions.append(Function(func_id, i_type, o_type))

    @property
    def variables(self):
        """Variables."""
        return self._variables

    @property
    def groups(self):
        """Groups."""
        return self._groups

    @property
    def curves(self):
        """Curves."""
        return self._curves

    @property
    def functions(self):
        """Functions."""
        return self._functions

    def reset_group(self):
        """."""
        r_var = [var for var in self.variables if not var.waccess]
        w_var = [var for var in self.variables if var.waccess]
        self._groups = [
            VariablesGroup(0, False, self.variables),
            VariablesGroup(1, False, r_var),
            VariablesGroup(2, True, w_var),
        ]

    def add_group(self, var_ids):
        """Add group."""
        variables = []
        for var_id in var_ids:
            variables.append(self.variables[var_id])
        self.groups.append(VariablesGroup(len(self.groups), False, variables))

    def remove_all_groups_of_variables(self):
        """Remove all groups bigger than eid 2."""
        self._groups = self.groups[:3]

    def list_variables(self, group_id):
        """List variable ids."""
        return [var.eid for var in self.groups[group_id].variables]

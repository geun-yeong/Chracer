from minidump.minidumpfile import MinidumpFile

from chracer.validator import *
from chracer.interface import ChromiumInstanceInterface, Field
from chracer.common_lib import *



class U8String(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 24

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)

        data = self._read(24)

        self._length_or_flag = data[23]
        if self._length_or_flag < 23:
            self._string_pointer = va
            self._string_length = self._length_or_flag
        else:
            self._string_pointer = convert_int(data[:8])
            self._string_length = convert_int(data[8:12])

    @property
    def string(self):
        if self._length_or_flag == 0:
            return ''
        else:
            s = self._read_from(self._string_pointer, self._string_length)
            return s.decode('utf-8')

    def validate(self, debug=False):
        try:
            assert validate_pointer(
                self._mdmp, 
                self._string_pointer, 
                True if self._length_or_flag == 0 else False), \
            "INVALID POINTER VALUE (string_pointer=0x{:X}, length_or_flag={})".format(self._string_pointer, self._length_or_flag)
            
            for c in self.string: 
                assert c.isprintable(), "INVALID ENCODED CHAR"
        except Exception as e:
            if debug: print('std::u[8|16]string -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True

    def __string__(self):
        return self.string



class U16String(U8String):
    _INSTANCE_SIZE = 24

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)

    @property
    def string(self):
        if self._length_or_flag == 0: return ''

        s = self._read_from(self._string_pointer, self._string_length*2)
        return s.decode('utf-16-le')



class Vector(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 24

    def __init__(self, mdmp: MinidumpFile, va: int, entry_size: int):
        super().__init__(mdmp, va)
        
        # __begin_, __end_, __end_capacity_
        self._begin = Field(va, 0, 8, 'begin')
        self._end = Field(va, 8, 8, 'end')
        self._end_cap  = Field(va, 16, 8, 'end_cap')
        self._entry_size = entry_size
    
    @property
    def begin(self):
        return convert_int(self._read_field(self._begin))
    @property
    def end(self):
        return convert_int(self._read_field(self._end))
    @property
    def end_cap(self):
        return convert_int(self._read_field(self._end_cap))
    @property
    def entry_size(self):
        return self._entry_size
    @property
    def entries(self):
        if self.begin == 0 or self.end == 0: return tuple()

        _ = self._read_from(self.begin, self.end - self.begin)
        return tuple(_[i:i+self.entry_size] for i in range(0, len(_), self.entry_size)) 
    @property
    def va_of_entries(self):
        return tuple(range(self.begin, self.end, self.entry_size))
    @property
    def entry_count(self):
        return (self.end - self.begin) // self.entry_size

    def validate(self, debug=False):
        try:
            if self.begin != 0:
                assert validate_pointer(self._mdmp, self.begin, can_null=False), "INVALID POINTER VALUE (begin)"
                assert validate_rw_page(self._mdmp, self.begin), "INVALID POINTER VALUE (begin is not heap)"
            if self.end != 0:
                assert validate_pointer(self._mdmp, self.end, can_null=False), "INVALID POINTER VALUE (end)"
                assert validate_rw_page(self._mdmp, self.end), "INVALID POINTER VALUE (end is not heap)"
            if self.end_cap != 0:
                assert validate_pointer(self._mdmp, self.end_cap, can_null=False), "INVALID POINTER VALUE (end_cap)"
                assert validate_rw_page(self._mdmp, self.end_cap), "INVALID POINTER VALUE (end_cap is not heap)"
            if self.begin != 0 and self.end != 0:
                assert self.begin < self.end, "INVALID POINTER VALUE (begin > end)"
            assert self.end <= self.end_cap, "INVALID POINTER VALUE (end > end_cap)"
            assert ((self.end - self.begin) % self.entry_size) == 0, "INVALID POINTER VALUE (it is not multiple of entry size)"
            _ = self.entries
        except Exception as e:
            if debug: print('std::vector -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True



class Map(ChromiumInstanceInterface, dict):
    _INSTANCE_LAYOUT = '< QQQ'
    _INSTANCE_SIZE = 24
    _TREE_NODE_SIZE = 25

    def __init__(self, mdmp: MinidumpFile, va: int, key_type_size: int, value_type_size: int, key_func = None, value_func = None):
        super().__init__(mdmp, va)
        
        self._begin_node = Field(va, 0, 8, 'begin_node')
        self._pair1 = Field(va, 8, 8, 'pair1')
        self._pair3 = Field(va, 16, 8, 'pair3')

        self._key_type_size = key_type_size
        self._value_type_size = value_type_size
        self._key_func = key_func
        self._value_func = value_func

        self._parse(self.pair1, key_type_size, value_type_size)
    
    @property
    def begin_node(self):
        return convert_int(self._read_field(self._begin_node))
    @property
    def pair1(self):
        return convert_int(self._read_field(self._pair1))
    @property
    def pair3(self):
        return convert_int(self._read_field(self._pair3))
    
    def _parse(self, node_ptr: int, key_type_size: int, value_type_size: int):
        if not node_ptr: return

        tree_node_data = self._read_from(node_ptr, 25)

        left = Field(node_ptr, 0, 8, 'left_child')
        left = convert_int(tree_node_data[left.offset : left.offset+left.size])

        right = Field(node_ptr, 8, 8, 'right_child')
        right = convert_int(tree_node_data[right.offset : right.offset+right.size])

        parent = Field(node_ptr, 16, 8, 'parent')
        parent = convert_int(tree_node_data[parent.offset : parent.offset+parent.size])

        is_black = Field(node_ptr, 24, 1, 'is_black')
        is_black = convert_int(tree_node_data[is_black.offset : is_black.offset+is_black.size])

        self._parse(left, key_type_size, value_type_size)
        self._parse(right, key_type_size, value_type_size)

        key_type_align = self._alignment_offset(key_type_size)
        key_data_offset = self._TREE_NODE_SIZE + (key_type_align - (self._TREE_NODE_SIZE % key_type_align))
        key_data = self._read_from(node_ptr+key_data_offset, key_type_size)

        value_type_alignment = self._alignment_offset(value_type_size)
        if (key_data_offset + key_type_size) % value_type_alignment == 0:
            value_data_offset = key_data_offset + key_type_size
        else:
            value_data_offset = key_data_offset + key_type_size + (value_type_alignment - (key_type_size % value_type_alignment))
        value_data = self._read_from(node_ptr+value_data_offset, value_type_size)

        if self._key_func: key_data = self._key_func(key_data)
        if self._value_func: value_data = self._value_func(value_data)
        self[key_data] = value_data

    def _alignment_offset(self, variable_size):
        if variable_size > 4: return 8
        if variable_size > 2: return 4
        if variable_size > 1: return 2
        return 1
    
    def validate(self, debug=False):
        try:
            assert self.pair3 < 0, "NEGATIVE VALUE (pair3)"
            can_null = True if self.pair3 == 0 else False
            assert validate_pointer(self._mdmp, self.begin_node, can_null), "INVALID POINTER VALUE (begin_node)"
            assert validate_pointer(self._mdmp, self.pair1, can_null), "INVALID POINTER VALUE (pair1)"
        except Exception as e:
            if debug: print('std::map -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True
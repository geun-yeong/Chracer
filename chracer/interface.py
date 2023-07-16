from minidump.minidumpfile import MinidumpFile

from chracer import ChromiumSymbols
from chracer.common_lib import *

class Field:
    def __init__(self, base: int, offset: int, size: int, name: str):
        self._base = base
        self._offset = offset
        self._size = size
        self._name = name

    @property
    def base(self): return self._base
    @property
    def offset(self): return self._offset
    @property
    def size(self): return self._size
    @property
    def name(self): return self._name
    @property
    def va(self): return self.base + self.offset



class ChromiumInstanceInterface:
    _INSTANCE_SIZE = 0
    _INSTANCE_LAYOUT = ''

    def __init__(self, mdmp: MinidumpFile, va: int):
        self._mdmp = mdmp
        self._base = va
    
    @property
    def base(self): return self._base
    @classmethod
    def instance_size(self): return self._INSTANCE_SIZE

    def _read(self, size: int):
        return self._mdmp.get_reader().read(self.base, size)
    
    def _read_field(self, field: Field):
        return self._mdmp.get_reader().read(field.va, field.size)
    
    def _read_at(self, offset: int, size: int):
        return self._mdmp.get_reader().read(self.base + offset, size)
    
    def _read_from(self, va: int, size: int=0):
        return self._mdmp.get_reader().read(va, size if size > 0 else self._INSTANCE_SIZE)
    
    def _load_symbols(self, path: str):
        sym = ChromiumSymbols.find(path)
        members = sym.findall('member[@kind="Member"]')
        for mem in members:
            field_name = '_' + mem.attrib.get('name')
            if field_name[-1] == '_': field_name = field_name[:-1]

            field_offset = int(mem.attrib.get('offset'), base=16)
            
            field_size = int(mem.attrib.get('length'), base=16)
            if field_size == 0: field_size = get_type_size(mem.attrib.get('datatype'))
            
            self.__setattr__(field_name, Field(self.base, field_offset, field_size, field_name))

    def validate(self, debug=False):
        return True
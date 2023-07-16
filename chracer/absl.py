from minidump.minidumpfile import MinidumpFile

from chracer.validator import *
from chracer.interface import ChromiumInstanceInterface, Field
from chracer.std import *
from chracer.gfx import *
from chracer.time import *
from chracer.common_lib import *

class Optional(ChromiumInstanceInterface):

    def __init__(self, mdmp: MinidumpFile, va: int, entry_size: int):
        super().__init__(mdmp, va)

        # bool + padding for alignment + entry size + dummy
        alignment_offset = self._alignment_offset(entry_size)
        self._INSTANCE_SIZE = alignment_offset + entry_size

        self._engaged = Field(va, 0, 1, 'engaged')
        self._data = Field(va, alignment_offset, entry_size, 'data')
    
    @property
    def engaged(self):
        return convert_bool(self._read_field(self._engaged))
    @property
    def data(self):
        if self.engaged:
            return self._read_field(self._data)
        else:
            return None

    def va_of_data(self):
        return self.base + self._data.offset
    
    def _alignment_offset(self, variable_size):
        if variable_size > 4: return 8
        if variable_size > 2: return 4
        if variable_size > 1: return 2
        return 1
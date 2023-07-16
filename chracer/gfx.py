from minidump.minidumpfile import MinidumpFile

from chracer.interface import ChromiumInstanceInterface
from chracer.common_lib import *

class Point(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 8
    _INSTANCE_LAYOUT = '< ii'

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="gfx::Point"]')

    def __getattr__(self, name):
        if name == 'x':
            return convert_int(self._read_field(self._x), signed=True)
        if name == 'y':
            return convert_int(self._read_field(self._y), signed=True)

    def validate(self, debug=False):
        return False if self.x < 0 or self.y < 0 else True
    
    def __str__(self):
        return '({}, {})'.format(self.x, self.y)



class Size(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 8

    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="gfx::Size"]')

    def __getattr__(self, name):
        if name == 'width':
            return convert_int(self._read_field(self._width), signed=True)
        if name == 'height':
            return convert_int(self._read_field(self._height), signed=True)
    
    def validate(self, debug=False):
        return False if self.width < 0 or self.height < 0 else True

    def __str__(self):
        return '({}, {})'.format(self.width, self.height)



class Rect(ChromiumInstanceInterface):
    _INSTANCE_SIZE = 16
    
    def __init__(self, mdmp: MinidumpFile, va: int):
        super().__init__(mdmp, va)
        self._load_symbols('./classes/class[@name="gfx::Rect"]')
    
    def __getattr__(self, name):
        if name == 'origin':
            return Point(self._mdmp, self._origin.va)
        if name == 'size':
            return Size(self._mdmp, self._size.va)

    def validate(self, debug=False):
        try:
            assert self.origin.validate(debug), "INVALID gfx::Point"
            assert self.size.validate(debug), "INVALID gfx::Size"
        except Exception as e:
            if debug: print('gfx::Rect -> 0x{0:X} {1}'.format(self.base, e))
            return False
        return True
    
    def __str__(self):
        return '{}, {}'.format(str(self.point), str(self.size))



class Image(ChromiumInstanceInterface):
    pass
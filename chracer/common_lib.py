import struct

from chracer import ChromiumSymbols

def convert_float(data: bytes) -> float:
    if len(data) == 4: return struct.unpack('< f', data)[0]
    if len(data) == 8: return struct.unpack('< d', data)[0]
    return 0.0

def convert_int(data: bytes, signed=False) -> int:
    return int.from_bytes(data, 'little', signed=signed)

def convert_bool(data: bytes) -> bool:
    return True if convert_int(data) else False

def get_type_size(type_name: str) -> int:
    if type_name == 'bool':
        return 1
    elif type_name == 'short':
        return 2
    elif type_name == 'int':
        return 4
    elif type_name == 'float':
        return 4
    elif type_name == 'double':
        return 8
    
    e = ChromiumSymbols.find('./enums/enum[@name="{}"]'.format(type_name))
    if e: return int(e.attrib.get('length'), base=16)
    c = ChromiumSymbols.find('./classes/class[@name="{}"]'.format(type_name))
    if c: return int(c.attrib.get('length'), base=16)
    d = ChromiumSymbols.find('./datatypes/datatype[@name="{}"]'.format(type_name))
    if d: return int(d.attrib.get('length'), base=16)

    return 0

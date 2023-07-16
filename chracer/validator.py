from minidump.minidumpfile import MinidumpFile
from minidump.streams import MemoryType, MemoryState, AllocationProtect

def validate_pointer(mdmp: MinidumpFile, va: int, can_null=True) -> bool:
    if can_null and va == 0: return True
    if not can_null and va == 0: return False
    if va < 0x800000000000: return True
    try:
        mdmp.get_reader().read(va, 1)
    except:
        return False
    return True

def validate_rw_page(mdmp: MinidumpFile, va: int) -> bool:
    if va == 0: return False
    for m in mdmp.memory_info.infos:
        if m.BaseAddress < va < (m.BaseAddress + m.RegionSize) \
        and m.Type == MemoryType.MEM_PRIVATE \
        and m.State == MemoryState.MEM_COMMIT \
        and m.Protect == AllocationProtect.PAGE_READWRITE:
            return True
    return False

def validate_boolean(value):
    return value in (0, 1)
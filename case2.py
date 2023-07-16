import datetime
from tabulate import tabulate
from minidump.minidumpfile import MinidumpFile

print('### start to load symbols at', datetime.datetime.now())
from chracer.chromium import *
print('### end to load symbols at', datetime.datetime.now())



MINIDUMP_PATH = 'dumps/case2.dmp'
BROWSER_OBJECT_LOCATION = [2229826644976]

print('### start to extract information at', datetime.datetime.now())

mdmp = MinidumpFile.parse(MINIDUMP_PATH)
printed_table = []

for base in BROWSER_OBJECT_LOCATION:
    browser = Browser(mdmp, base)
    if not browser.validate():
        print('[WARN] 0x{:X} is not a Browser object'.format(base))
        continue
    
    tsm = browser.tab_strip_model
    groups = tsm.group_model.groups

    tabs = tsm.contents_data.entries
    for tab_idx, tab_base in enumerate(tabs):
        tab_base = int.from_bytes(tab_base, 'little')
        tab = Tab(mdmp, tab_base)
        if not tab.validate():
            print('[WARN] 0x{:X} is not a Tab object'.format(tab_base))
            continue
        
        group = groups[tab.grouphex]
        group_name = group.visual_data.title.string if group else ''
        group_color = group.visual_data.color.name if group else ''

        printed_table.append(
            (browser.session_id, group_name, group_color, tab_idx)
        )

print('### end to extract information at', datetime.datetime.now())

hdr = ['SessionID', 'TabGroup', 'TabGroupColor', 'Tab']
print(tabulate(printed_table, headers=hdr))
import datetime
from tabulate import tabulate
from minidump.minidumpfile import MinidumpFile

print('### start to load symbols at', datetime.datetime.now())
from chracer.chromium import *
print('### end to load symbols at', datetime.datetime.now())



MINIDUMP_PATH = 'dumps/case5.dmp'
BROWSER_OBJECT_LOCATION = [2417514995120, 2417528533216, 2417617828064, 2417629760992]

print('### start to extract information at', datetime.datetime.now())

mdmp = MinidumpFile.parse(MINIDUMP_PATH)
printed_table = []

for base in BROWSER_OBJECT_LOCATION:
    browser = Browser(mdmp, base)
    if not browser.validate():
        print('[WARN] 0x{:X} is not a Browser object'.format(base))
        continue

    incognito = 'Unk'
    if type(browser.profile) == Profile: incognito = False
    if type(browser.profile) == OffTheRecordProfile: incognito = True
    
    tsm = browser.tab_strip_model
    tabs = tsm.contents_data.entries
    for tab_idx, tab_base in enumerate(tabs):
        tab_base = int.from_bytes(tab_base, 'little')
        tab = Tab(mdmp, tab_base)
        if not tab.validate():
            print('[WARN] 0x{:X} is not a Tab object'.format(tab_base))
            continue

        nav_entries = tab.contents.primary_frame_tree.navigator.controller.entries.entries
        for nav_entry_base in nav_entries:
            nav_entry_base = int.from_bytes(nav_entry_base, 'little')
            nav_entry = NavigationEntry(mdmp, nav_entry_base)
            if not nav_entry.validate():
                print('[WARN] 0x{:X} is not a NavigationEntryImpl object'.format(nav_entry_base))
                continue
            frame_entry = nav_entry.frame_tree.frame_entry

            printed_table.append(
                (browser.session_id, 
                incognito, 
                tab_idx, 
                nav_entry.title.string, 
                frame_entry.url)
            )

print('### end to extract information at', datetime.datetime.now())

hdr = ['SessionID', 'Incognito', 'Tab', 'Title', 'URL']
print(tabulate(printed_table, headers=hdr))
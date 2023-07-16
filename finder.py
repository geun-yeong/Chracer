import os
import sys
import tqdm
import datetime
from tabulate import tabulate
from minidump.minidumpfile import MinidumpFile

if len(sys.argv) != 2:
    print('Usage: python {0} <minidump file>'.format(sys.argv[0]))
    exit()
if not os.path.exists(sys.argv[1]):
    print('{0} is not exists'.format(sys.argv[1]))
    exit()



print('### start to load symbols at', datetime.datetime.now())
from chracer.chromium import *
print('### end to load symbols at', datetime.datetime.now())



print('[NOTICE] The program is very slow because it hasn\'t been optimized yet.')
print('### start to find Browser objects at', datetime.datetime.now())

mdmp = MinidumpFile.parse(sys.argv[1])
browser_instances = []
for m in tqdm.tqdm(mdmp.memory_info.infos):
    if m.Type == MemoryType.MEM_PRIVATE \
    and m.State == MemoryState.MEM_COMMIT \
    and m.Protect == AllocationProtect.PAGE_READWRITE:
        
        for addr in range(m.BaseAddress, m.BaseAddress + m.RegionSize - Browser.instance_size(), 8):
            b = Browser(mdmp, addr)
            if not b.validate(): continue

            tabs = b.tab_strip_model.contents_data.entries
            if len(tabs) < 1: continue

            tab = Tab(mdmp, int.from_bytes(tabs[0], 'little'))
            if not tab.validate(): continue

            entries = tab.contents.primary_frame_tree.navigator.controller.entries.entries
            if len(entries) < 1: continue
            
            entry = NavigationEntry(mdmp, int.from_bytes(entries[0], 'little'))
            if not entry.validate(): continue
            
            browser_instances.append(b)

print('### end to find Browser objects at', datetime.datetime.now())



print('### start to extract information at', datetime.datetime.now())

hdr = ['SessionID', 'Tab', 'Time', 'Title', 'URL']
body = []
for b in browser_instances:
    for ti, tp in enumerate(b.tab_strip_model.contents_data.entries):
        t = Tab(mdmp, int.from_bytes(tp, 'little'))
        w = t.contents
        f = w.primary_frame_tree
        n = f.navigator
        nc = n.controller

        for ei, ep in enumerate(nc.entries.entries):
            e = NavigationEntry(mdmp, int.from_bytes(ep, 'little'))
            fe = e.frame_tree.frame_entry
            body.append((b.session_id, ti, e.timestamp.to_datetime(), e.title.string, fe.url.spec.string))

print('### end to extract information at', datetime.datetime.now())

print(tabulate(body, headers=hdr))
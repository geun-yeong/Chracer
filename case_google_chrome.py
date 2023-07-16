import tqdm
import datetime
from tabulate import tabulate
from minidump.minidumpfile import MinidumpFile
from minidump.streams import MemoryType, MemoryState, AllocationProtect

print('### start to load symbols at', datetime.datetime.now())
from chracer.chrome.chrome import *
print('### end to load symbols at', datetime.datetime.now())

print('### start to find Browser objects at', datetime.datetime.now())

mdmp = MinidumpFile.parse(r'dumps\case_google_chrome.dmp')

#browser_instances = [ChromeBrowser(mdmp, 0x1E2400106DD8)]
browser_instances = []
for m in tqdm.tqdm(mdmp.memory_info.infos):
    if m.Type == MemoryType.MEM_PRIVATE \
    and m.State == MemoryState.MEM_COMMIT \
    and m.Protect == AllocationProtect.PAGE_READWRITE:
        
        for addr in range(m.BaseAddress, m.BaseAddress + m.RegionSize - ChromeBrowser.instance_size(), 8):
            b = ChromeBrowser(mdmp, addr)
            if not b.validate(): continue

            tabs = b.tab_strip_model.contents_data.entries
            tab = ChromeTab(mdmp, int.from_bytes(tabs[0], 'little'))
            if not tab.validate(): continue

            entries = tab.contents.primary_frame_tree.navigator.controller.entries.entries
            entry = ChromeNavigationEntry(mdmp, int.from_bytes(entries[0], 'little'))
            if not entry.validate(): continue
            
            browser_instances.append(b)

print('### end to find Browser objects at', datetime.datetime.now())

print('### start to extract information at', datetime.datetime.now())

hdr = ['SessionID', 'Tab', 'Time', 'Title', 'URL']
body = []
for b in browser_instances:
    for ti, tp in enumerate(b.tab_strip_model.contents_data.entries):
        t = ChromeTab(mdmp, int.from_bytes(tp, 'little'))
        w = t.contents
        f = w.primary_frame_tree
        n = f.navigator
        nc = n.controller

        for ei, ep in enumerate(nc.entries.entries):
            e = ChromeNavigationEntry(mdmp, int.from_bytes(ep, 'little'))
            fe = e.frame_tree.frame_entry
            body.append((b.session_id, ti, e.timestamp.to_datetime(), e.title.string, fe.url.spec.string))

print('### end to extract information at', datetime.datetime.now())

print(tabulate(body, headers=hdr))
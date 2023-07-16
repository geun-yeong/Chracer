from xml.etree import ElementTree

class ChromiumSymbols:
    _chrome_dll_sym = ElementTree.parse('symbols/chrome.dll.pdb.xml')
    _content_dll_sym = ElementTree.parse('symbols/content.dll.pdb.xml')
    
    @classmethod
    def find(cls, path: str):
        _ = ChromiumSymbols._chrome_dll_sym.find(path)
        if _: return _
        _ = ChromiumSymbols._content_dll_sym.find(path)
        if _: return _

    @classmethod
    def findall(cls, path: str):
        _ = ChromiumSymbols._chrome_dll_sym.findall(path)
        if _: return _
        _ = ChromiumSymbols._content_dll_sym.findall(path)
        if _: return _
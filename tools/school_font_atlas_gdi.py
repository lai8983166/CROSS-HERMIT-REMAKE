"""Owned independent atlas DC, DIB and font with real original GDI preparation."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tools.school_d3d8_bridge import LiveD3D8
from tools.school_font_cache_platform import build_one, COMPILER, machine, sha
from tools.school_font_atlas import ROOT, FONT_ARGS, bitmap_header

SOURCE = ROOT/'tools/school_font_atlas_gdi_v2.cs'
HELPER = ROOT/'.venv-audit/school-font-atlas-gdi-v2.exe'


class AtlasGDI(LiveD3D8):
    def __init__(self):
        if machine(HELPER) != 0x14C: raise ValueError('atlas GDI helper must be x86')
        self.process = subprocess.Popen([str(HELPER)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
        self.reader = ThreadPoolExecutor(max_workers=1)
        self.sequence, self.closed, self.trace, self.cleanup = 0, False, [], None
        try:
            reply = self._read()
            if reply.get('ok') is not True or reply.get('id') != 0 or reply['hello']['pointer_bytes'] != 4:
                raise ValueError('actual atlas GDI hello/ABI')
            self.hello = reply['hello']
        except BaseException:
            self._terminate(); raise


def setup(platform):
    from tools.school_owner_startup import FONT_ARGS as FIRST_ARGS, source_contract
    platform.request('GetDC')
    font = platform.request('CreateFontA', args=FIRST_ARGS[:-1], face_hex=source_contract()['face_hex'])
    logfont = platform.request('GetObjectA', pointer=font['result'], before_hex='cc'*60)
    dc = platform.request('CreateCompatibleDC')['result']
    dib = platform.request('CreateDIBSection', pointer=dc, header_hex=bitmap_header().hex())
    for op, value in (('SetBkMode', 2), ('SetBkColor', 0), ('SetTextColor', 0xFFFFFF)):
        platform.request(op, pointer=dc, value=value)
    platform.request('SelectObject', pointer=dc, object=dib['result'])
    platform.request('CreateFontIndirectA', logfont_hex=logfont['hex'])


def prepare(platform):
    calls = []
    def call(op, **args):
        result = platform.request(op, **args); calls.append(dict(op=op, request=args, result=result)); return result
    dc = call('atlas_dc')['result']
    dib = call('atlas_dib', pointer=dc, header_hex=bitmap_header().hex())
    call('atlas_map', pointer=dc, value=1)
    call('atlas_muldiv', args=[12, 96, 72])
    font = call('atlas_font', args=FONT_ARGS, face_hex='4669786564537973')
    call('atlas_bitmap_select', pointer=dc, object=dib['result'])
    call('atlas_font_select', pointer=dc, object=font['result'])
    for op, value in (('atlas_text', 0xFFFFFF), ('atlas_background', 0), ('atlas_align', 0)):
        call(op, pointer=dc, value=value)
    return calls


def probe():
    with AtlasGDI() as platform:
        setup(platform); calls = prepare(platform)
    return dict(hello=platform.hello, calls=calls, trace=platform.trace, cleanup=platform.cleanup)


if __name__ == '__main__':
    path = ROOT/'analysis/school-font-atlas-gdi-v2-20261018.json'
    if path.exists(): raise ValueError('fresh immutable atlas GDI report required')
    build = build_one(SOURCE, HELPER)
    path.write_text(json.dumps(dict(build=build, probe=probe()), indent=2)+'\n', encoding='utf-8', newline='\n')

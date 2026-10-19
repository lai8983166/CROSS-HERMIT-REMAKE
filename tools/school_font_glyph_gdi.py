"""Owned real95-character GDI loop and explicit inspection-only DIB snapshots."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tools.school_font_atlas_gdi import setup, prepare
from tools.school_font_cache_platform import build_one, COMPILER, sha, machine
from tools.school_d3d8_bridge import LiveD3D8
from tools.school_font_glyph import ROOT, layout

SOURCE=ROOT/'tools/school_font_glyph_gdi.cs'
HELPER=ROOT/'.venv-audit/school-font-glyph-gdi-v1.exe'


class GlyphGDI(LiveD3D8):
    def __init__(self):
        if machine(HELPER)!=0x14C:raise ValueError('glyph x86 GDI required')
        self.process=subprocess.Popen([str(HELPER)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
        self.reader=ThreadPoolExecutor(max_workers=1);self.sequence,self.closed,self.trace,self.cleanup=0,False,[],None
        try:
            reply=self._read()
            if reply.get('ok') is not True or reply.get('id')!=0 or reply['hello']['pointer_bytes']!=4:raise ValueError('glyph actual GDI hello')
            self.hello=reply['hello']
        except BaseException:self._terminate();raise


def raster(platform):
    import struct
    calls=prepare(platform);dc=calls[0]['result']['result'];bits=calls[1]['result']['bits']
    before=platform.request('glyph_pixels',pointer=bits,stage='before')
    x=y=0;measurements=[];results=[];initial='cc'*8
    for ch in range(32,127):
        measured=platform.request('glyph_measure',pointer=dc,character=ch,before_hex=initial)
        w,h=struct.unpack('<2i',bytes.fromhex(measured['hex']));measurements.append((w,h))
        if x+w+1>256:x,y=0,y+h+1
        result=platform.request('glyph_draw',pointer=dc,character=ch,x=x,y=y)
        results.append(dict(character=ch,x=x,y=y,measure=measured,draw=result));x+=w+1;initial=measured['hex']
    after=platform.request('glyph_pixels',pointer=bits,stage='after')
    return dict(preparation=calls,before=before,after=after,glyphs=results)


def probe():
    with GlyphGDI() as platform:setup(platform);result=raster(platform)
    return dict(hello=platform.hello,**result,trace=platform.trace,cleanup=platform.cleanup)


if __name__=='__main__':
    path=ROOT/'analysis/school-font-glyph-gdi-v1-20261019.json'
    if path.exists():raise ValueError('fresh immutable glyph GDI report required')
    build=build_one(SOURCE,HELPER)
    path.write_text(json.dumps(dict(build=build,probe=probe()),indent=2)+'\n',encoding='utf-8',newline='\n')

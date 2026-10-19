"""Actual original-order GDI deletion, deferred lifetime inspection and cleanup."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tools.school_font_glyph_gdi import setup,raster
from tools.school_font_cache_platform import build_one,COMPILER,sha,machine
from tools.school_d3d8_bridge import LiveD3D8
from tools.school_font_state import ROOT

SOURCE=ROOT/'tools/school_font_state_gdi_v5.cs'
HELPER=ROOT/'.venv-audit/school-font-state-gdi-v5.exe'


class StateGDI(LiveD3D8):
    def __init__(self):
        if machine(HELPER)!=0x14C:raise ValueError('font state x86 GDI required')
        self.process=subprocess.Popen([str(HELPER)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
        self.reader=ThreadPoolExecutor(max_workers=1);self.sequence,self.closed,self.trace,self.cleanup=0,False,[],None
        try:
            reply=self._read()
            if reply.get('ok') is not True or reply.get('id')!=0 or reply['hello']['pointer_bytes']!=4:raise ValueError('font state actual GDI hello')
            self.hello=reply['hello']
        except BaseException:self._terminate();raise


def deletion(platform,preparation):
    dc=preparation[0]['result']['result'];bitmap=preparation[1]['result']['result'];font=preparation[4]['result']['result']
    return [dict(op=op,request=dict(pointer=pointer),result=platform.request(op,pointer=pointer))
        for op,pointer in (('font_delete_bitmap',bitmap),('font_delete_dc',dc),('font_delete_font',font))]


def probe():
    with StateGDI() as platform:
        setup(platform);result=raster(platform);calls=deletion(platform,result['preparation'])
    return dict(hello=platform.hello,deletion=calls,trace=platform.trace,cleanup=platform.cleanup)


if __name__=='__main__':
    path=ROOT/'analysis/school-font-state-gdi-v5-20261019.json'
    if path.exists():raise ValueError('fresh immutable state GDI report required')
    build=build_one(SOURCE,HELPER)
    path.write_text(json.dumps(dict(build=build,probe=probe()),indent=2)+'\n',encoding='utf-8',newline='\n')

"""Owned second glyph raster and independently locked second texture helpers."""
import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tools.school_device_init_bridge import DeviceBridge
from tools.school_d3d8_bridge import LiveD3D8
from tools.school_font_cache_platform import build_one,COMPILER,sha,machine
from tools.school_font_second_resource_platform import first_device,create_second,prepare_second,setup,raster,deletion
from tools.school_font_second_glyph import ROOT,layout

GDI_SOURCE=ROOT/'tools/school_font_second_glyph_gdi_v2.cs'
GDI_HELPER=ROOT/'.venv-audit/school-font-second-glyph-gdi-v2.exe'
DEVICE_SOURCE=ROOT/'tools/school_font_second_glyph_device.cs'
DEVICE_HELPER=ROOT/'.venv-audit/school-font-second-glyph-device-v1.exe'


class SecondGlyphGDI(LiveD3D8):
    def __init__(self):
        if machine(GDI_HELPER)!=0x14C:raise ValueError('second glyph x86 GDI required')
        self.process=subprocess.Popen([str(GDI_HELPER)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            text=True,encoding='utf8',creationflags=subprocess.CREATE_NO_WINDOW)
        self.reader=ThreadPoolExecutor(max_workers=1);self.sequence,self.closed,self.trace,self.cleanup=0,False,[],None
        try:
            r=self._read()
            if r.get('ok') is not True or r.get('id')!=0 or r['hello']['pointer_bytes']!=4:raise ValueError('second glyph actual hello')
            self.hello=r['hello']
        except BaseException:self._terminate();raise


class SecondGlyphDevice(DeviceBridge):
    def __init__(self,width=640,height=480):super().__init__(DEVICE_HELPER,width,height)


def owned_run(callback,width=640,height=480):
    refused=[]
    for attempt in range(6):
        try:
            with SecondGlyphDevice(width,height) as bridge:value=callback(bridge)
            return dict(value=value,trace=bridge.trace,cleanup=bridge.cleanup,refused_address_collisions=refused)
        except RuntimeError as error:
            if str(error)!='live interface mapping collides with audit ownership':raise
            if not bridge.cleanup or not bridge.cleanup['all_owned_resources_released']:raise RuntimeError('second glyph collision cleanup failed') from error
            refused.append(dict(error=str(error),trace=bridge.trace,cleanup=bridge.cleanup))
    raise RuntimeError('six second glyph processes collided with audit ownership')


def gdi_ready(p):
    setup(p);first=raster(p);released=deletion(p,first['preparation']);second=prepare_second(p)
    return dict(first=first,first_native_cleanup=released,second=second)


def second_raster(p,ready):
    import struct
    dc=ready['second'][0]['result']['result'];bits=ready['second'][1]['result']['bits']
    before=p.request('second_glyph_pixels',pointer=bits,stage='before');calls=[];measures=[];initial='cc'*8
    for ch in range(32,127):
        req=dict(pointer=dc,character=ch,before_hex=initial);r=p.request('second_glyph_measure',**req)
        calls.append(dict(op='second_glyph_measure',request=req,result=r));initial=r['hex'];measures.append(struct.unpack('<2I',bytes.fromhex(initial)))
        rows,end=layout(measures+[(1,1)]*(95-len(measures)));row=rows[len(measures)-1]
        req=dict(pointer=dc,character=ch,x=row['x'],y=row['y']);r=p.request('second_glyph_draw',**req)
        calls.append(dict(op='second_glyph_draw',request=req,result=r))
    after=p.request('second_glyph_pixels',pointer=bits,stage='after')
    return dict(before=before,calls=calls,after=after)


def gdi_probe():
    with SecondGlyphGDI() as p:
        ready=gdi_ready(p);second=second_raster(p,ready)
    return dict(hello=p.hello,ready=ready,second=second,trace=p.trace,cleanup=p.cleanup)


def device_ready(bridge):
    first=first_device(bridge);second=create_second(bridge,first['device'])
    return first,second


def device_probe():
    def run(bridge):
        first,second=device_ready(bridge);pointer=second['texture']['pointer']
        locked=bridge.request('second_atlas_lock',pointer=pointer,level=0,rect=0,flags=0)
        value=bytearray.fromhex(locked['before_hex'])
        for n in range(len(value)):value[n]=(n*13+7)&255
        unlocked=bridge.request('second_atlas_unlock',pointer=pointer,level=0,bytes_hex=value.hex())
        return dict(first=first,second=second,locked=locked,uploaded_hex=value.hex(),unlocked=unlocked)
    r=owned_run(run);return dict(**r.pop('value'),**r)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--kind',choices=('gdi','device'),required=True);a=p.parse_args()
    path=ROOT/('analysis/school-font-second-glyph-'+a.kind+('-v2' if a.kind=='gdi' else '-v1')+'-20261019.json')
    if path.exists():p.error('fresh immutable second glyph platform report required')
    source,helper=(GDI_SOURCE,GDI_HELPER) if a.kind=='gdi' else (DEVICE_SOURCE,DEVICE_HELPER)
    build=build_one(source,helper);probe=gdi_probe() if a.kind=='gdi' else device_probe()
    path.write_text(json.dumps(dict(build=build,probe=probe),indent=2)+chr(10),encoding='utf8',newline=chr(10))

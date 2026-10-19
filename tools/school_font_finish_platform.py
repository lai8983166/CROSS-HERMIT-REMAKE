"""Immutable owned second native GDI cleanup and two-font VB/state resources."""
import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tools.school_device_init_bridge import DeviceBridge
from tools.school_d3d8_bridge import LiveD3D8
from tools.school_font_cache_platform import build_one,COMPILER,sha,machine
from tools.school_font_second_glyph_platform import gdi_ready,second_raster,device_ready
from tools.school_font_finish import ROOT,plan

GDI_SOURCE=ROOT/'tools/school_font_finish_gdi.cs'
GDI_HELPER=ROOT/'.venv-audit/school-font-finish-gdi-v1.exe'
DEVICE_SOURCE=ROOT/'tools/school_font_finish_device.cs'
DEVICE_HELPER=ROOT/'.venv-audit/school-font-finish-device-v1.exe'


class FinishGDI(LiveD3D8):
    def __init__(self):
        if machine(GDI_HELPER)!=0x14C:raise ValueError('font finish x86 GDI required')
        self.process=subprocess.Popen([str(GDI_HELPER)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf8',creationflags=subprocess.CREATE_NO_WINDOW)
        self.reader=ThreadPoolExecutor(max_workers=1);self.sequence,self.closed,self.trace,self.cleanup=0,False,[],None
        try:
            r=self._read()
            if r.get('ok') is not True or r.get('id')!=0 or r['hello']['pointer_bytes']!=4:raise ValueError('font finish GDI hello')
            self.hello=r['hello']
        except BaseException:self._terminate();raise


class FinishDevice(DeviceBridge):
    def __init__(self,width=640,height=480):super().__init__(DEVICE_HELPER,width,height)


def owned_run(callback,width=640,height=480):
    refused=[]
    for attempt in range(6):
        try:
            with FinishDevice(width,height) as bridge:value=callback(bridge)
            return dict(value=value,trace=bridge.trace,cleanup=bridge.cleanup,refused_address_collisions=refused)
        except RuntimeError as error:
            if str(error)!='live interface mapping collides with audit ownership':raise
            if not bridge.cleanup or not bridge.cleanup['all_owned_resources_released']:raise RuntimeError('font finish collision cleanup failed') from error
            refused.append(dict(error=str(error),trace=bridge.trace,cleanup=bridge.cleanup))
    raise RuntimeError('six font finish processes collided with audit ownership')


def second_delete(p,ready):
    prep=ready['second'];pointers=[prep[1]['result']['result'],prep[0]['result']['result'],prep[4]['result']['result']]
    return [dict(op=op,request=dict(pointer=pointer),result=p.request(op,pointer=pointer)) for op,pointer in zip(
        ('second_font_delete_bitmap','second_font_delete_dc','second_font_delete_font'),pointers)]


def gdi_probe():
    with FinishGDI() as p:
        ready=gdi_ready(p);raster=second_raster(p,ready);deleted=second_delete(p,ready)
    return dict(hello=p.hello,ready=ready,raster=raster,deletion=deleted,trace=p.trace,cleanup=p.cleanup)


def ready_device(b):
    first,second=device_ready(b);pointer=second['texture']['pointer']
    locked=b.request('second_atlas_lock',pointer=pointer,level=0,rect=0,flags=0)
    b.request('second_atlas_unlock',pointer=pointer,level=0,bytes_hex=locked['before_hex'])
    return first,second


def device_probe():
    def run(b):
        first,second=ready_device(b);device=first['device']
        vb=b.request('second_font_vb',pointer=device,args=[8400,520,0,0])
        states=[dict(request=r,result=b.request('second_font_state',pointer=device,**r)) for r in plan(second['texture']['pointer'])]
        return dict(first=first,second=second,vertex=vb,states=states)
    r=owned_run(run);return dict(**r.pop('value'),**r)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--kind',choices=('gdi','device'),required=True);a=p.parse_args();path=ROOT/('analysis/school-font-finish-'+a.kind+'-v1-20261019.json')
    if path.exists():p.error('fresh immutable font finish platform required')
    source,helper=(GDI_SOURCE,GDI_HELPER) if a.kind=='gdi' else (DEVICE_SOURCE,DEVICE_HELPER)
    build=build_one(source,helper);probe=gdi_probe() if a.kind=='gdi' else device_probe()
    path.write_text(json.dumps(dict(build=build,probe=probe),indent=2)+chr(10),encoding='utf8',newline=chr(10))

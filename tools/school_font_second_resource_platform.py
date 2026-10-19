"""Immutable owned x86 second atlas and independently owned GDI setup."""
import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tools.school_device_init_bridge import DeviceBridge
from tools.school_d3d8_bridge import LiveD3D8
from tools.school_font_cache_platform import build_one,COMPILER,sha,machine
from tools.school_font_state_device import ready
from tools.school_font_state import plan
from tools.school_font_state_gdi import setup,raster,deletion
from tools.school_font_second_resource import ROOT,bitmap_header,FONT_ARGS,FACE

DEVICE_SOURCE=ROOT/'tools/school_font_second_resource_device_v2.cs'
DEVICE_HELPER=ROOT/'.venv-audit/school-font-second-resource-device-v2.exe'
GDI_SOURCE=ROOT/'tools/school_font_second_resource_gdi.cs'
GDI_HELPER=ROOT/'.venv-audit/school-font-second-resource-gdi-v1.exe'


class SecondDevice(DeviceBridge):
    def __init__(self,width=640,height=480):
        super().__init__(DEVICE_HELPER,width,height)


class SecondGDI(LiveD3D8):
    def __init__(self):
        if machine(GDI_HELPER)!=0x14C:raise ValueError('second GDI x86 required')
        self.process=subprocess.Popen([str(GDI_HELPER)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,text=True,encoding='utf8',creationflags=subprocess.CREATE_NO_WINDOW)
        self.reader=ThreadPoolExecutor(max_workers=1)
        self.sequence,self.closed,self.trace,self.cleanup=0,False,[],None
        try:
            reply=self._read()
            if reply.get('ok') is not True or reply.get('id')!=0 or reply['hello']['pointer_bytes']!=4:
                raise ValueError('second GDI actual hello')
            self.hello=reply['hello']
        except BaseException:self._terminate();raise


def owned_run(callback,width=640,height=480):
    refused=[]
    for attempt in range(6):
        try:
            with SecondDevice(width,height) as bridge:value=callback(bridge)
            return dict(value=value,trace=bridge.trace,cleanup=bridge.cleanup,refused_address_collisions=refused)
        except RuntimeError as error:
            if str(error)!='live interface mapping collides with audit ownership':raise
            if not bridge.cleanup or not bridge.cleanup['all_owned_resources_released']:
                raise RuntimeError('second atlas collision cleanup failed') from error
            refused.append(dict(error=str(error),trace=bridge.trace,cleanup=bridge.cleanup))
    raise RuntimeError('six second atlas processes collided with audit ownership')


def first_device(bridge):
    device,texture=ready(bridge)
    vertex=bridge.request('font_vb',pointer=device,args=[8400,520,0,0])
    states=[dict(request=command,result=bridge.request('font_state',pointer=device,**command)) for command in plan(texture)]
    return dict(device=device,texture=texture,vertex=vertex,states=states)


def create_second(bridge,device,**changes):
    request=dict(pointer=device,width=256,height=256,levels=1,usage=0,format=26,pool=1)
    request.update(changes)
    return bridge.request('second_atlas_create',**request)


def prepare_second(platform,limit=10):
    calls=[]
    for n in range(limit):
        op=('dc','dib','map','muldiv','font','bitmap_select','font_select','text','background','align')[n]
        if n==0:request={}
        elif n==1:request=dict(pointer=dc,header_hex=bitmap_header().hex())
        elif n==3:request=dict(args=[8,96,72])
        elif n==4:request=dict(args=FONT_ARGS,face_hex=FACE.hex())
        elif n in (5,6):request=dict(pointer=dc,object=bitmap if n==5 else font)
        else:request=dict(pointer=dc,value={2:1,7:0xFFFFFF,8:0,9:0}[n])
        op='second_atlas_'+op
        result=platform.request(op,**request)
        calls.append(dict(op=op,request=request,result=result))
        if n==0:dc=result['result']
        if n==1:bitmap=result['result']
        if n==4:font=result['result']
    return calls


def device_probe():
    def run(bridge):
        first=first_device(bridge)
        second=create_second(bridge,first['device'])
        return dict(hello=bridge.hello,first=first,second=second)
    r=owned_run(run)
    return dict(**r.pop('value'),**r)


def gdi_probe():
    with SecondGDI() as platform:
        setup(platform);first=raster(platform);released=deletion(platform,first['preparation'])
        second=prepare_second(platform)
    return dict(hello=platform.hello,first_native_cleanup=released,second=second,
                trace=platform.trace,cleanup=platform.cleanup)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--kind',choices=('device','gdi'),required=True);a=p.parse_args()
    path=ROOT/('analysis/school-font-second-resource-'+a.kind+('-v2' if a.kind=='device' else '-v1')+'-20261019.json')
    if path.exists():p.error('fresh immutable second resource platform report required')
    source,helper=(DEVICE_SOURCE,DEVICE_HELPER) if a.kind=='device' else (GDI_SOURCE,GDI_HELPER)
    build=build_one(source,helper)
    probe=device_probe() if a.kind=='device' else gdi_probe()
    path.write_text(json.dumps(dict(build=build,probe=probe),indent=2)+'\n',encoding='utf8',newline='\n')

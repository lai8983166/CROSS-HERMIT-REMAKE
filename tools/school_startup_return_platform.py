"""Immutable owned x86 gamma call, register observation and external restoration."""
import argparse
import json
from tools.school_font_finish_platform import (FinishGDI,FinishDevice,ready_device,
    GDI_SOURCE,GDI_HELPER,COMPILER,build_one,sha,machine,plan)
from tools.school_device_init_bridge import DeviceBridge
from tools.school_startup_return import ROOT,gamma_bytes

DEVICE_SOURCE=ROOT/'tools/school_startup_return_device.cs'
DEVICE_HELPER=ROOT/'.venv-audit/school-startup-return-device-v1.exe'


class ReturnDevice(DeviceBridge):
    def __init__(self,width=640,height=480):super().__init__(DEVICE_HELPER,width,height)


def owned_run(callback,width=640,height=480):
    refused=[]
    for attempt in range(6):
        try:
            with ReturnDevice(width,height) as bridge:value=callback(bridge)
            return dict(value=value,trace=bridge.trace,cleanup=bridge.cleanup,refused_address_collisions=refused)
        except RuntimeError as error:
            if str(error)!='live interface mapping collides with audit ownership':raise
            if not bridge.cleanup or not bridge.cleanup['all_owned_resources_released']:raise RuntimeError('startup return collision cleanup failed') from error
            refused.append(dict(error=str(error),trace=bridge.trace,cleanup=bridge.cleanup))
    raise RuntimeError('six startup return processes collided with audit ownership')


def ready_gamma(b):
    first,second=ready_device(b);pointer=first['device']
    vertex=b.request('second_font_vb',pointer=pointer,args=[8400,520,0,0])
    states=[dict(request=r,result=b.request('second_font_state',pointer=pointer,**r)) for r in plan(second['texture']['pointer'])]
    return dict(first=first,second=second,vertex=vertex,states=states,device=pointer)


def probe():
    def run(b):
        ready=ready_gamma(b);pointer=ready['device']
        prepare=b.request('gamma_prepare',pointer=pointer)
        result=b.request('gamma_set',pointer=pointer,flags=1,hex=gamma_bytes().hex())
        return dict(ready=ready,prepare=prepare,gamma=result)
    r=owned_run(run);return dict(**r.pop('value'),**r)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable startup return platform report required')
    build=build_one(DEVICE_SOURCE,DEVICE_HELPER)
    path.write_text(json.dumps(dict(build=build,probe=probe()),indent=2)+chr(10),encoding='utf8',newline=chr(10))

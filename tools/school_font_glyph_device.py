"""Owned real atlas lock, exact native-buffer transfer and readonly readback."""
import json
from tools.school_device_init_bridge import DeviceBridge
from tools.school_font_atlas_device import setup,create
from tools.school_font_cache_platform import build_one,COMPILER,sha,machine
from tools.school_font_glyph import ROOT

SOURCE=ROOT/'tools/school_font_glyph_device.cs'
HELPER=ROOT/'.venv-audit/school-font-glyph-device-v1.exe'


class GlyphDevice(DeviceBridge):
    def __init__(self,width=640,height=480):super().__init__(HELPER,width,height)


def owned_run(callback,width=640,height=480):
    refused=[]
    for attempt in range(6):
        try:
            with GlyphDevice(width,height) as bridge:value=callback(bridge)
            return dict(value=value,trace=bridge.trace,cleanup=bridge.cleanup,refused_address_collisions=refused)
        except RuntimeError as error:
            if str(error)!='live interface mapping collides with audit ownership':raise
            if not bridge.cleanup or not bridge.cleanup['all_owned_resources_released']:raise RuntimeError('glyph collision cleanup failed') from error
            refused.append(dict(error=str(error),trace=bridge.trace,cleanup=bridge.cleanup))
    raise RuntimeError('six glyph processes collided with audit ownership')


def probe():
    def run(bridge):
        device=setup(bridge);texture=create(bridge,device)['texture']['pointer']
        locked=bridge.request('atlas_lock',pointer=texture,level=0,rect=0,flags=0)
        value=bytearray.fromhex(locked['before_hex']);value[:2]=bytes((52,18));value[-2:]=bytes((205,171))
        uploaded=bridge.request('atlas_unlock',pointer=texture,level=0,bytes_hex=value.hex())
        return dict(hello=bridge.hello,locked=locked,uploaded=uploaded,written_hex=value.hex())
    result=owned_run(run);return dict(**result.pop('value'),**result)


if __name__=='__main__':
    path=ROOT/'analysis/school-font-glyph-device-v1-20261019.json'
    if path.exists():raise ValueError('fresh immutable glyph device report required')
    build=build_one(SOURCE,HELPER)
    path.write_text(json.dumps(dict(build=build,probe=probe()),indent=2)+'\n',encoding='utf-8',newline='\n')

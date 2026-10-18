"""Owned x86 sprite device references and cache GDI resources, with immutable builds."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tools.school_device_init_bridge import DeviceBridge
from tools.school_d3d8_bridge import LiveD3D8, ROOT, COMPILER, machine, sha
from tools.school_font_cache import bitmap_header

DEVICE_SOURCE = ROOT/'tools/school_font_cache_device.cs'
DEVICE_HELPER = ROOT/'.venv-audit/school-font-cache-device-v1.exe'
GDI_SOURCE = ROOT/'tools/school_font_cache_gdi.cs'
GDI_HELPER = ROOT/'.venv-audit/school-font-cache-gdi-v1.exe'


def build_one(source, helper):
    if helper.exists():
        raise ValueError('fresh immutable font cache helper required')
    result = subprocess.run([str(COMPILER), '/nologo', '/platform:x86',
                             '/r:System.Web.Extensions.dll', '/out:'+str(helper), str(source)],
                            capture_output=True, timeout=30, creationflags=subprocess.CREATE_NO_WINDOW)
    if result.returncode:
        raise RuntimeError((result.stdout+result.stderr).decode('cp936', errors='replace'))
    if machine(helper) != 0x14C:
        raise ValueError('actual x86 cache helper required')
    return dict(source_sha256=sha(source.read_bytes()), helper_sha256=sha(helper.read_bytes()),
                compiler_sha256=sha(COMPILER.read_bytes()), machine=machine(helper))


class SpriteDeviceBridge(DeviceBridge):
    def __init__(self, width=640, height=480):
        super().__init__(DEVICE_HELPER, width, height)


class CachePlatform(LiveD3D8):
    def __init__(self):
        if machine(GDI_HELPER) != 0x14C:
            raise ValueError('cache GDI helper must be x86')
        self.process = subprocess.Popen([str(GDI_HELPER)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, text=True, encoding='utf-8',
                                        creationflags=subprocess.CREATE_NO_WINDOW)
        self.reader = ThreadPoolExecutor(max_workers=1)
        self.sequence, self.closed, self.trace, self.cleanup = 0, False, [], None
        try:
            reply = self._read()
            if reply.get('ok') is not True or reply.get('id') != 0 or reply['hello']['pointer_bytes'] != 4:
                raise ValueError('actual cache GDI hello/ABI')
            self.hello = reply['hello']
        except BaseException:
            self._terminate()
            raise


def owned_run(callback, width=640, height=480):
    refused = []
    for attempt in range(6):
        try:
            with SpriteDeviceBridge(width, height) as bridge:
                value = callback(bridge)
            return dict(value=value, trace=bridge.trace, cleanup=bridge.cleanup, refused_address_collisions=refused)
        except RuntimeError as error:
            if str(error) != 'live interface mapping collides with audit ownership':
                raise
            if not bridge.cleanup or not bridge.cleanup['all_owned_resources_released']:
                raise RuntimeError('cache collision cleanup failed') from error
            refused.append(dict(error=str(error), trace=bridge.trace, cleanup=bridge.cleanup))
    raise RuntimeError('six cache processes collided with fixed audit mappings')


def gdi_probe():
    from tools.school_owner_startup import FONT_ARGS, source_contract
    with CachePlatform() as platform:
        platform.request('GetDC')
        font = platform.request('CreateFontA', args=FONT_ARGS[:-1], face_hex=source_contract()['face_hex'])
        logfont = platform.request('GetObjectA', pointer=font['result'], before_hex='cc'*60)
        dc = platform.request('CreateCompatibleDC')['result']
        bitmap = platform.request('CreateDIBSection', pointer=dc, header_hex=bitmap_header(True).hex())
        for op, value in (('SetBkMode', 2), ('SetBkColor', 0), ('SetTextColor', 0xFFFFFF)):
            platform.request(op, pointer=dc, value=value)
        platform.request('SelectObject', pointer=dc, object=bitmap['result'])
        indirect = platform.request('CreateFontIndirectA', logfont_hex=logfont['hex'])
    return dict(logfont=logfont, indirect=indirect, bitmap=bitmap, trace=platform.trace, cleanup=platform.cleanup)


def device_probe():
    from tools.school_font_texture_bridge import setup
    def run(bridge):
        device, _ = setup(bridge)
        tex = bridge.request('texture_create', pointer=device, width=64, height=16, levels=1, usage=512, format=21, pool=0)
        bridge.request('texture_surface', pointer=tex['texture']['pointer'], level=0)
        calls = [dict(op=op, result=bridge.request(op, pointer=device))
                 for op in ('sprite_addref', 'sprite_caps', 'sprite_creation', 'font_addref')]
        return dict(hello=bridge.hello, calls=calls)
    result = owned_run(run)
    return dict(**result.pop('value'), **result)


if __name__ == '__main__':
    path = ROOT/'analysis/school-font-cache-platform-v1-20261018.json'
    if path.exists():
        raise ValueError('fresh immutable cache platform report required')
    builds = dict(device=build_one(DEVICE_SOURCE, DEVICE_HELPER), gdi=build_one(GDI_SOURCE, GDI_HELPER))
    path.write_text(json.dumps(dict(builds=builds, gdi=gdi_probe(), device=device_probe()), indent=2)+'\n',
                    encoding='utf-8', newline='\n')

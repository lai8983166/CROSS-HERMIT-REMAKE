"""Owned real x86 texture/factory/debug methods for the original cache initializer."""
import json
import subprocess
from tools.school_device_init_bridge import DeviceBridge
from tools.school_d3d8_bridge import ROOT, COMPILER, machine, sha

SOURCE = ROOT/'tools/school_font_texture_bridge.cs'
HELPER = ROOT/'.venv-audit/school-font-texture-v1.exe'


def build():
    if HELPER.exists():
        raise ValueError('fresh immutable texture helper required')
    result = subprocess.run([str(COMPILER), '/nologo', '/platform:x86',
                             '/r:System.Web.Extensions.dll', '/out:'+str(HELPER), str(SOURCE)],
                            capture_output=True, timeout=30, creationflags=subprocess.CREATE_NO_WINDOW)
    if result.returncode:
        raise RuntimeError((result.stdout+result.stderr).decode('cp936', errors='replace'))
    if machine(HELPER) != 0x14C:
        raise ValueError('real x86 texture helper required')
    return dict(source_sha256=sha(SOURCE.read_bytes()), helper_sha256=sha(HELPER.read_bytes()),
                compiler_sha256=sha(COMPILER.read_bytes()), machine=machine(HELPER))


class TextureBridge(DeviceBridge):
    def __init__(self, width=640, height=480):
        super().__init__(HELPER, width, height)


def owned_run(callback, width=640, height=480):
    refused = []
    for attempt in range(6):
        try:
            with TextureBridge(width, height) as bridge:
                value = callback(bridge)
            return dict(value=value, trace=bridge.trace, cleanup=bridge.cleanup, refused_address_collisions=refused)
        except RuntimeError as error:
            if str(error) != 'live interface mapping collides with audit ownership':
                raise
            if not bridge.cleanup or not bridge.cleanup['all_owned_resources_released']:
                raise RuntimeError('texture address collision cleanup failed') from error
            refused.append(dict(error=str(error), trace=bridge.trace, cleanup=bridge.cleanup))
    raise RuntimeError('six owned texture processes collided with fixed audit mappings')


def setup(bridge):
    from tools.school_device_init_emulation import DeviceEmulator
    engine = DeviceEmulator(bridge)
    engine.run()
    device = engine.objects['device']['pointer']
    for op in ('cache_addref', 'cache_caps', 'cache_creation'):
        bridge.request(op, pointer=device)
    return device, engine.objects['factory']['pointer']


def probe():
    def run(bridge):
        device, factory = setup(bridge)
        bridge.request('debug_mute', value=1)
        bridge.request('texture_factory', pointer=device)
        bridge.request('texture_caps', pointer=device)
        mode = bridge.request('texture_mode', pointer=device)
        result = bridge.request('texture_format', pointer=factory, adapter=0, type=1,
                               adapter_format=int.from_bytes(bytes.fromhex(mode['hex'])[12:], 'little'),
                               usage=512, resource_type=3, format=21)
        bridge.request('texture_factory_release', pointer=factory)
        bridge.request('debug_mute', value=0)
        texture = bridge.request('texture_create', pointer=device, width=64, height=16, levels=1,
                                 usage=512, format=21, pool=0)
        surface = bridge.request('texture_surface', pointer=texture['texture']['pointer'], level=0)
        return dict(hello=bridge.hello, format_result=result, texture=texture, surface=surface)
    result = owned_run(run)
    return dict(**result.pop('value'), **result)


if __name__ == '__main__':
    path = ROOT/'analysis/school-font-texture-bridge-v1-20261018.json'
    if path.exists():
        raise ValueError('fresh immutable texture bridge report required')
    provenance = build()
    path.write_text(json.dumps(dict(build=provenance, probe=probe()), indent=2)+'\n', encoding='utf-8', newline='\n')

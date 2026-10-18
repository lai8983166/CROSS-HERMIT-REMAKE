"""Owned immutable x86 additional atlas alongside existing cache resources."""
import json
from tools.school_font_cache_platform import build_one, COMPILER, sha, machine
from tools.school_device_init_bridge import DeviceBridge
from tools.school_font_atlas import ROOT

SOURCE = ROOT/'tools/school_font_atlas_device.cs'
HELPER = ROOT/'.venv-audit/school-font-atlas-device-v1.exe'


class AtlasDevice(DeviceBridge):
    def __init__(self, width=640, height=480):
        super().__init__(HELPER, width, height)


def owned_run(callback, width=640, height=480):
    refused = []
    for attempt in range(6):
        try:
            with AtlasDevice(width, height) as bridge:
                value = callback(bridge)
            return dict(value=value, trace=bridge.trace, cleanup=bridge.cleanup, refused_address_collisions=refused)
        except RuntimeError as error:
            if str(error) != 'live interface mapping collides with audit ownership': raise
            if not bridge.cleanup or not bridge.cleanup['all_owned_resources_released']:
                raise RuntimeError('atlas collision cleanup failed') from error
            refused.append(dict(error=str(error), trace=bridge.trace, cleanup=bridge.cleanup))
    raise RuntimeError('six atlas processes collided with fixed audit mappings')


def setup(bridge):
    from tools.school_font_texture_bridge import setup as base_setup
    device, _ = base_setup(bridge)
    tex = bridge.request('texture_create', pointer=device, width=64, height=16, levels=1, usage=512, format=21, pool=0)
    bridge.request('texture_surface', pointer=tex['texture']['pointer'], level=0)
    for op in ('sprite_addref', 'sprite_caps', 'sprite_creation', 'font_addref'):
        bridge.request(op, pointer=device)
    return device


def create(bridge, device):
    return bridge.request('atlas_create', pointer=device, width=256, height=256, levels=1, usage=0, format=26, pool=1)


def probe():
    def run(bridge):
        device = setup(bridge)
        return dict(hello=bridge.hello, atlas=create(bridge, device))
    result = owned_run(run)
    return dict(**result.pop('value'), **result)


if __name__ == '__main__':
    path = ROOT/'analysis/school-font-atlas-device-v1-20261018.json'
    if path.exists(): raise ValueError('fresh immutable atlas device report required')
    build = build_one(SOURCE, HELPER)
    path.write_text(json.dumps(dict(build=build, probe=probe()), indent=2)+'\n', encoding='utf-8', newline='\n')

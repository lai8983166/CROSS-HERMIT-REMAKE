"""Immutable extension of the owned x86 startup bridge for font-cache queries."""
import subprocess
from tools.school_device_init_bridge import DeviceBridge
from tools.school_d3d8_bridge import ROOT, COMPILER, machine, sha

SOURCE = ROOT/'tools/school_font_device_bridge.cs'
HELPER = ROOT/'.venv-audit/school-font-device-v1.exe'


def build():
    if HELPER.exists():
        raise ValueError('fresh immutable font device helper required')
    result = subprocess.run([str(COMPILER), '/nologo', '/platform:x86',
                             '/r:System.Web.Extensions.dll', '/out:'+str(HELPER), str(SOURCE)],
                            capture_output=True, timeout=30, creationflags=subprocess.CREATE_NO_WINDOW)
    if result.returncode:
        raise RuntimeError((result.stdout+result.stderr).decode('cp936', errors='replace'))
    if machine(HELPER) != 0x14C:
        raise ValueError('font device helper must be x86')
    return dict(source_sha256=sha(SOURCE.read_bytes()), helper_sha256=sha(HELPER.read_bytes()),
                compiler_sha256=sha(COMPILER.read_bytes()), machine=machine(HELPER))


class FontDeviceBridge(DeviceBridge):
    def __init__(self, width=640, height=480):
        super().__init__(HELPER, width, height)


def owned_run(callback, width=640, height=480):
    """Reject address collisions, close that process, then obtain a fresh owned process."""
    refused = []
    for attempt in range(6):
        try:
            with FontDeviceBridge(width, height) as bridge:
                value = callback(bridge)
            return dict(value=value, trace=bridge.trace, cleanup=bridge.cleanup,
                        refused_address_collisions=refused)
        except RuntimeError as error:
            if str(error) != 'live interface mapping collides with audit ownership':
                raise
            if not bridge.cleanup or not bridge.cleanup['all_owned_resources_released']:
                raise RuntimeError('address collision resources not released') from error
            refused.append(dict(error=str(error), trace=bridge.trace, cleanup=bridge.cleanup))
    raise RuntimeError('six owned processes collided with fixed audit mappings')


def probe():
    from tools.school_device_init_emulation import DeviceEmulator

    def run(bridge):
        engine = DeviceEmulator(bridge)
        startup = engine.run()
        pointer = engine.objects['device']['pointer']
        calls = [dict(op=op, result=bridge.request(op, pointer=pointer))
                 for op in ('cache_addref', 'cache_caps', 'cache_creation')]
        return dict(hello=bridge.hello, startup=startup, calls=calls)
    result = owned_run(run)
    return dict(**result.pop('value'), **result)


if __name__ == '__main__':
    import json
    path = ROOT/'analysis/school-font-startup-bridge-v1-20261018.json'
    if path.exists():
        raise ValueError('fresh immutable font bridge report required')
    provenance = build() if not HELPER.exists() else dict(
        source_sha256=sha(SOURCE.read_bytes()), helper_sha256=sha(HELPER.read_bytes()),
        compiler_sha256=sha(COMPILER.read_bytes()), machine=machine(HELPER))
    path.write_text(json.dumps(dict(build=provenance, probe=probe()), indent=2)+'\n',
                    encoding='utf-8', newline='\n')

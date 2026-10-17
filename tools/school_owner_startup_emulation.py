"""Full native owner construction and natural first font prefix with live handles."""
import argparse
import json
import struct

from unicorn.x86_const import UC_X86_REG_EIP, UC_X86_REG_ESP, UC_X86_REG_EAX, UC_X86_REG_ECX
from tools.school_owner_startup import *
from tools.school_device_init import project_owner
from tools.school_device_init_emulation import DeviceEmulator, OWNER, STACK, TOP, RETURN, MANAGER, EXTERNAL
from tools.school_device_init_bridge import DeviceBridge
from tools.school_owner_platform import OwnerPlatform
from tools.school_renderer_init_emulation import REGISTERS, buffer_evidence, digest


class OwnerEmulator(DeviceEmulator):
    def __init__(self, device_bridge, owner_bridge, fill):
        self.owner_bridge = owner_bridge
        self.stop = RETURN
        self.win_calls = []
        super().__init__(device_bridge)
        self.ranges = functions()
        self.uc.mem_map(0, 4096)
        self.uc.mem_write(0, bytes(4096))
        self.uc.mem_write(OWNER, bytes([fill])*0xC000)
        self.fill = fill
        self.imports = {self.read(slot): (slot, rule) for slot, rule in IMPORTS.items()}
        for target in self.imports:
            self._foreign_write(target, b'\xC3')
        md = Cs(CS_ARCH_X86, CS_MODE_32)
        self.ret_addresses = {i.address for a, b in self.ranges.items()
                              for i in md.disasm(self.image[a-BASE:b-BASE], a) if i.mnemonic == 'ret'}

    def _write(self, uc, access, at, size, value, user):
        allowed = ((OWNER, OWNER+0xC000), (STACK, STACK+65536), (0, 4),
                   (0x765728, 0x79172A), (0x799AE0, 0x799AF0), (0x5FF530, 0x5FF534))
        if not any(a <= at and at+size <= b for a, b in allowed):
            raise RuntimeError('owner startup forbidden write '+hex(at))

    def _win(self, at, sp, ret, slot, rule):
        name, desc, expected_ret, count = rule
        if ret != expected_ret:
            raise RuntimeError('owner original platform caller '+name)
        args = [self.read(sp+4+i*4) for i in range(count)]
        request = {}
        if name == 'GetDC':
            if args != [0]:
                raise RuntimeError('owner original screen DC')
        elif name in ('QueryPerformanceCounter', 'QueryPerformanceFrequency'):
            if name.endswith('Counter') and not STACK <= args[0] < TOP:
                raise RuntimeError('owner actual counter output')
            if name.endswith('Frequency') and args != [OWNER+0xB188]:
                raise RuntimeError('owner actual frequency output')
        elif name == 'CreateFontA':
            if args != FONT_ARGS or bytes(self.uc.mem_read(args[-1], 8)).hex() != source_contract()['face_hex']+'00':
                raise RuntimeError('owner original font inputs')
            request = dict(args=args[:-1], face_hex=source_contract()['face_hex'])
        else:
            if args[:2] != [self.font_handle, 60] or not STACK <= args[2] <= TOP-60:
                raise RuntimeError('owner original LOGFONT input')
            request = dict(pointer=args[0], before_hex=bytes(self.uc.mem_read(args[2], 60)).hex())
        result = self.owner_bridge.request(name, **request)
        if name.startswith('QueryPerformance'):
            self._put(args[0], bytes.fromhex(result['hex']))
        elif name == 'CreateFontA':
            self.font_handle = result['result']
        elif name == 'GetObjectA':
            self._put(args[2], bytes.fromhex(result['hex']))
        self.win_calls.append(dict(name=name, slot=hex(slot), va=hex(at), return_va=hex(ret),
                                   sp=sp, args=args, request=request, result=result, live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX, u32(result['result']))
        self.uc.reg_write(UC_X86_REG_ESP, sp+4+count*4)
        self.uc.reg_write(UC_X86_REG_EIP, ret)

    def _code(self, uc, at, size, user):
        sp = uc.reg_read(UC_X86_REG_ESP)
        if at in (RETURN, self.stop):
            self.boundary = at
            uc.emu_stop()
            return
        ret = self.read(sp)
        if at in self.imports:
            slot, rule = self.imports[at]
            self._win(at, sp, ret, slot, rule)
            return
        if ret in EXTERNAL and (at == self.import_target or any(
                at in obj['methods'].values() for obj in self.objects.values())):
            self._platform(at, sp, ret, *EXTERNAL[ret])
            return
        if not any(a <= at and at+size <= b for a, b in self.ranges.items()):
            raise RuntimeError('undeclared owner native body '+hex(at))
        self.visited.add(at)
        if at in self.ranges and at != 0x56CE80:
            self.entries.append(dict(va=hex(at), return_va=hex(ret), sp=sp,
                                     receiver=uc.reg_read(UC_X86_REG_ECX),
                                     args=[self.read(sp+4+i*4) for i in range(ARGS.get(at, 0))]))
        if at in self.ret_addresses:
            self.returns.append(dict(va=hex(at), return_va=hex(ret), sp=sp,
                                     eax=uc.reg_read(UC_X86_REG_EAX)))

    def check(self, owner, image, seh):
        actual = bytes(self.uc.mem_read(OWNER, 0xC000))
        if actual != owner:
            bad = [hex(i) for i, (a, b) in enumerate(zip(actual, owner)) if a != b]
            raise RuntimeError('owner full source/native mismatch '+repr(bad[:24]))
        if bytes(self.uc.mem_read(BASE, len(image))) != image:
            raise RuntimeError('owner full source/global mutation mismatch')
        if bytes(self.uc.mem_read(0, 4096)) != struct.pack('<I', seh)+bytes(4092):
            raise RuntimeError('owner complete SEH/null page mismatch')
        for at, data in self.foreign.items():
            if bytes(self.uc.mem_read(at, 4096)) != data:
                raise RuntimeError('owner actual interface/trap map changed')
        for at, count in ((STACK, TOP-4096-STACK), (TOP+24, STACK+65536-TOP-24)):
            if bytes(self.uc.mem_read(at, count)) != bytes([0xA5])*count:
                raise RuntimeError('owner original stack guard')
        return dict(owner=buffer_evidence(actual), image_sha256=digest(image), SEH=seh,
                    foreign_maps=[dict(pointer=at, **buffer_evidence(bytes(data)))
                                  for at, data in sorted(self.foreign.items())],
                    stack_guards_unchanged=True)

    def construct(self):
        self.win_calls = []
        self.stop = RETURN
        native = self.call(CTOR)
        api = {row['name']: row['result'] for row in self.win_calls}
        before = bytes([self.fill])*0xC000
        expected = project_constructor(before, api)
        image = project_image(api)
        if native['boundary'] != hex(RETURN) or native['cpu']['EAX'] != OWNER:
            raise RuntimeError('owner original constructor natural return')
        row = dict(native=native, platform_calls=self.win_calls,
                   state=self.check(expected, image, 0))
        self.constructed_owner, self.constructed_image = expected, image
        return row

    def device(self):
        self.win_calls = []
        self.stop = 0x415F50
        hello = self.bridge.hello
        args = [hello['window'], 1, 1, hello['width'], hello['height']]
        native = self.call(0x413450, args)
        expected = project_owner(self.constructed_owner, hello['width'], hello['height'],
                                 hello['window'], native['live_results'])
        if self.win_calls:
            raise RuntimeError('owner device prefix unexpected GDI input')
        row = dict(native=native, state=self.check(expected, self.constructed_image, 0),
                   pending=dict(va='0x415f50', return_va=hex(self.read(TOP-92)),
                                sp=TOP-92, receiver=OWNER, args=[], first_instruction_executed=False))
        self.device_owner = expected
        return row

    def font(self):
        if self.uc.reg_read(UC_X86_REG_EIP) != 0x415F50:
            raise RuntimeError('owner actual pending font CPU required')
        before_cpu = {k: self.uc.reg_read(r) for k, r in REGISTERS.items()}
        self.win_calls, self.entries, self.returns, self.platform_calls, self.live_results = [], [], [], [], []
        self.visited, self.boundary, self.stop = set(), None, FONT_STOP
        self.uc.emu_start(0x415F50, RETURN+1, timeout=15_000_000, count=100000)
        native = dict(entries=self.entries, returns=self.returns, platform_calls=self.platform_calls,
                      live_results=self.live_results, visited=sorted(self.visited),
                      cpu={k: self.uc.reg_read(r) for k, r in REGISTERS.items()}, boundary=hex(self.boundary or 0))
        expected = bytearray(self.device_owner)
        store(expected, 0xB26C, self.font_handle)
        state = self.check(bytes(expected), self.constructed_image, TOP-108)
        pending_sp = TOP-404
        pending = dict(va=hex(FONT_STOP), return_va=hex(self.read(pending_sp)), sp=pending_sp,
                       args=[self.read(pending_sp+4+i*4) for i in range(3)],
                       first_instruction_executed=False)
        font_info = self.win_calls[-1]
        if bytes(self.uc.mem_read(TOP-388, 60)).hex() != font_info['result']['hex']:
            raise RuntimeError('owner complete live LOGFONT mirror')
        return dict(before_cpu=before_cpu, native=native, platform_calls=self.win_calls,
                    state=state, pending=pending, LOGFONT=font_info['result']['hex'],
                    font_object_constructed=False, owner_bound=False, queues_initialized=False)


def generate(phase):
    cases = []
    for fill, width, height in ((0xA5, 640, 480), (0xCC, 1024, 768)):
        with OwnerPlatform() as platform:
            with DeviceBridge(ROOT/'.venv-audit/school-device-init-bridge.exe', width, height) as bridge:
                engine = OwnerEmulator(bridge, platform, fill)
                case = dict(fill=fill, hello=bridge.hello, platform_hello=platform.hello,
                            constructor=engine.construct())
                if phase in ('device', 'font'):
                    case['device'] = engine.device()
                if phase == 'font':
                    case['font'] = engine.font()
            case.update(device_trace=bridge.trace, device_cleanup=bridge.cleanup)
        case.update(platform_trace=platform.trace, platform_cleanup=platform.cleanup)
        cases.append(case)
        print(hex(fill)+': native full owner '+phase+' verified', flush=True)
    platform_build = json.loads((ROOT/'analysis/school-owner-startup-platform-v2-20261017.json').read_text(encoding='utf-8'))['build']
    device_build = json.loads((ROOT/'analysis/school-device-init-bridge-v1-20261017.json').read_text(encoding='utf-8'))['build']
    return dict(schema_version=1, phase=phase, source_contract=source_contract(),
                platform_build=platform_build, device_build=device_build, cases=cases,
                inherited_source_globals=True, original_helpers_stubbed=False,
                retained_VM_advanced=False, drawing_or_Present=False, full_outer_frame=False,
                live_handles_resumable_after_cleanup=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--phase', choices=('constructor', 'device', 'font'), required=True)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    path = ROOT/a.out
    if path.exists():
        p.error('immutable fresh report required')
    report = generate(a.phase)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')

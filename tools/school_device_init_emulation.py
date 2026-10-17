"""Run original startup instructions through owned live32-bit D3D8 responses."""
import argparse
import json
import struct

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_EIP, UC_X86_REG_ESP, UC_X86_REG_EAX, UC_X86_REG_ECX
from tools.school_device_init import *
from tools.school_device_init_bridge import DeviceBridge, sha, machine
from tools.school_renderer_init_emulation import REGISTERS, buffer_evidence, digest

OWNER = 0x20000000
STACK = 0x21000000
TOP = STACK+0xF000
RETURN = 0x22000000
MANAGER = OWNER+0x1058
EXTERNAL = {
    0x4136F7: ('factory', 1), 0x413904: ('display_mode', 3),
    0x413A13: ('create_device', 7), 0x414064: ('caps', 2),
    0x4140FB: ('backbuffer', 4), 0x414129: ('describe_surface', 2),
    0x41414E: ('release_surface', 1), 0x414229: ('check_format', 7),
    0x413AD7: ('viewport', 2),
}


class DeviceEmulator:
    def __init__(self, bridge):
        source_contract()
        self.bridge = bridge
        self.uc = Uc(UC_ARCH_X86, UC_MODE_32)
        self.image = SOURCE.read_bytes()
        self.image_size = (len(self.image)+4095) & ~4095
        self.uc.mem_map(BASE, self.image_size)
        self.uc.mem_write(BASE, self.image)
        for at, size in ((OWNER, 0xC000), (STACK, 65536), (RETURN, 4096)):
            self.uc.mem_map(at, size)
            self.uc.mem_write(at, bytes([0xA5])*size)
        self.uc.mem_write(OWNER+0xB20C, bytes(8))
        self.foreign = {}
        self.objects = {}
        self.import_target = self.read(SLOT)
        self._foreign_write(self.import_target, b'\xC3')
        self.ret_addresses = set()
        decoder = Cs(CS_ARCH_X86, CS_MODE_32)
        for a, b in FUNCTIONS.items():
            self.ret_addresses.update(i.address for i in decoder.disasm(self.image[a-BASE:b-BASE], a)
                                      if i.mnemonic == 'ret')
        self.uc.hook_add(UC_HOOK_CODE, self._code)
        self.uc.hook_add(UC_HOOK_MEM_WRITE, self._write)

    def read(self, at):
        return struct.unpack('<I', bytes(self.uc.mem_read(at, 4)))[0]

    def _map_page(self, address):
        page = address & ~4095
        if (BASE <= page < BASE+self.image_size or OWNER <= page < OWNER+0xC000
                or STACK <= page < STACK+65536 or RETURN <= page < RETURN+4096):
            raise RuntimeError('live interface mapping collides with audit ownership')
        if page not in self.foreign:
            self.uc.mem_map(page, 4096)
            self.foreign[page] = bytearray(4096)

    def _foreign_write(self, at, raw):
        for offset, value in enumerate(raw):
            self._map_page(at+offset)
            self.foreign[(at+offset) & ~4095][(at+offset) & 4095] = value
        self.uc.mem_write(at, raw)

    def _identity(self, kind, row):
        if not row or not row['pointer'] or not row['vtable']:
            raise RuntimeError('live interface identity required')
        self.objects[kind] = row
        self._foreign_write(row['pointer'], struct.pack('<I', row['vtable']))
        for slot, target in row['methods'].items():
            if not target:
                raise RuntimeError('live interface method required')
            self._foreign_write(row['vtable']+int(slot), struct.pack('<I', target))
            # A one-byte trap terminator prevents speculative decode beyond a page.
            # The code hook dispatches to the real host method before it can execute.
            self._foreign_write(target, b'\xC3')

    def _put(self, at, raw):
        if not (OWNER <= at and at+len(raw) <= OWNER+0xC000
                or STACK <= at and at+len(raw) <= STACK+65536):
            raise RuntimeError('live output outside declared owner/stack')
        self.uc.mem_write(at, raw)

    def _write(self, uc, access, at, size, value, user):
        if not (OWNER <= at and at+size <= OWNER+0xC000
                or STACK <= at and at+size <= STACK+65536):
            raise RuntimeError('original startup unowned write '+hex(at))

    def _request(self, op, **args):
        result = self.bridge.request(op, **args)
        self.live_results.append(dict(op=op, request=args, result=result))
        return result

    def _platform(self, at, sp, ret, op, count):
        args = [self.read(sp+4+i*4) for i in range(count)]
        method = dict(factory=('factory', None), display_mode=('factory', 32),
                      create_device=('factory', 60), caps=('device', 28),
                      backbuffer=('device', 64), describe_surface=('surface', 32),
                      release_surface=('surface', 8), check_format=('factory', 40),
                      viewport=('device', 160))
        kind, slot = method[op]
        if op == 'factory':
            if at != self.import_target or args != [220]:
                raise RuntimeError('original factory import/SDK')
            result = self._request(op, sdk=220)
            self._identity('factory', result['factory'])
            eax = result['factory']['pointer']
        else:
            obj = self.objects[kind]
            if at != obj['methods'][str(slot)] or args[0] != obj['pointer']:
                raise RuntimeError('original owned live receiver/method')
            pointer = args[0]
            if op == 'display_mode':
                if args[1:] != [0, OWNER+0xB214]:
                    raise RuntimeError('original display-mode arguments')
                result = self._request(op, pointer=pointer)
                self._put(args[-1], bytes.fromhex(result['hex']))
            elif op == 'create_device':
                if args[1] != 0 or args[3] != self.bridge.hello['window'] or args[-2:] != [OWNER+0xB234, OWNER+0xB210]:
                    raise RuntimeError('original create-device arguments')
                pp = bytes(self.uc.mem_read(args[-2], 52)).hex()
                result = self._request(op, pointer=pointer, type=args[2], flags=args[4], presentation_hex=pp)
                self._put(args[-2], bytes.fromhex(result['presentation_hex']))
                device = result.get('device')
                self._put(args[-1], struct.pack('<I', device['pointer'] if device else 0))
                if device:
                    self._identity('device', device)
            elif op == 'caps':
                if args[1] != OWNER+0xB314:
                    raise RuntimeError('original caps output')
                result = self._request(op, pointer=pointer)
                self._put(args[1], bytes.fromhex(result['hex']))
            elif op == 'backbuffer':
                if args[1:3] != [0, 0] or not STACK <= args[3] <= TOP:
                    raise RuntimeError('original backbuffer arguments')
                result = self._request(op, pointer=pointer)
                self._identity('surface', result['surface'])
                self._put(args[3], struct.pack('<I', result['surface']['pointer']))
            elif op == 'describe_surface':
                if args[1] != OWNER+0xB3E8:
                    raise RuntimeError('original surface-description output')
                result = self._request(op, pointer=pointer)
                self._put(args[1], bytes.fromhex(result['hex']))
            elif op == 'release_surface':
                result = self._request(op, pointer=pointer)
            elif op == 'check_format':
                expected = [self.read(OWNER+0xB318), self.read(OWNER+0xB314), self.read(OWNER+0xB3E8), 1, 1]
                if args[1:6] != expected or args[6] not in FORMATS:
                    raise RuntimeError('original format-check arguments')
                result = self._request(op, pointer=pointer, adapter=args[1], type=args[2],
                                       adapter_format=args[3], format=args[6])
            else:
                if args[1] != OWNER+0xBA08:
                    raise RuntimeError('original viewport output')
                result = self._request(op, pointer=pointer, hex=bytes(self.uc.mem_read(args[1], 24)).hex())
            eax = result['count'] if op == 'release_surface' else result['hr']
        self.platform_calls.append(dict(op=op, va=hex(at), return_va=hex(ret), sp=sp,
                                        args=args, result=u32(eax), live_host_observed=True))
        # IPC supplies the observed EAX and stdcall stack cleanup; other registers are preserved.
        self.uc.reg_write(UC_X86_REG_EAX, u32(eax))
        self.uc.reg_write(UC_X86_REG_ESP, sp+4+count*4)
        self.uc.reg_write(UC_X86_REG_EIP, ret)

    def _code(self, uc, at, size, user):
        sp = uc.reg_read(UC_X86_REG_ESP)
        if at in (RETURN, STOP):
            self.boundary = at
            uc.emu_stop()
            return
        ret = self.read(sp)
        if ret in EXTERNAL and (at == self.import_target or any(
                at in obj['methods'].values() for obj in self.objects.values())):
            self._platform(at, sp, ret, *EXTERNAL[ret])
            return
        if not any(a <= at and at+size <= b for a, b in FUNCTIONS.items()):
            raise RuntimeError('undeclared original device instruction '+hex(at))
        self.visited.add(at)
        if at in FUNCTIONS and at != 0x56CE80:
            self.entries.append(dict(va=hex(at), return_va=hex(ret), sp=sp,
                                     receiver=uc.reg_read(UC_X86_REG_ECX),
                                     args=[self.read(sp+4+i*4) for i in range(ARG_COUNTS.get(at, 0))]))
        if at in self.ret_addresses:
            self.returns.append(dict(va=hex(at), return_va=hex(ret), sp=sp,
                                     eax=uc.reg_read(UC_X86_REG_EAX)))

    def call(self, va, args=(), receiver=OWNER):
        self.entries, self.returns, self.platform_calls, self.live_results = [], [], [], []
        self.visited = set()
        self.boundary = None
        for name, value in dict(ESP=TOP, EBP=0x11223344, EBX=0x55667788,
                                ESI=0x88776655, EDI=0x44332211, ECX=receiver,
                                EAX=0, EDX=0, EFLAGS=2).items():
            self.uc.reg_write(REGISTERS[name], value)
        self.uc.mem_write(TOP, struct.pack('<'+'I'*(len(args)+1), RETURN, *map(u32, args)))
        self.uc.emu_start(va, RETURN+1, timeout=15_000_000, count=100000)
        return dict(entries=self.entries, returns=self.returns, platform_calls=self.platform_calls,
                    live_results=self.live_results, visited=sorted(self.visited),
                    cpu={k: self.uc.reg_read(r) for k, r in REGISTERS.items()}, boundary=hex(self.boundary or 0))

    def run(self):
        declared = bytes(self.uc.mem_read(OWNER, 0xC000))
        ctor = self.call(0x40D7E0, receiver=MANAGER)
        expected = bytearray(declared)
        expected[0x1058:0x10B8] = constructor(expected[0x1058:0x10B8])
        if bytes(self.uc.mem_read(OWNER, 0xC000)) != bytes(expected) or ctor['boundary'] != hex(RETURN):
            raise RuntimeError('original manager constructor full-owner verification')
        initial = bytes(expected)
        hello = self.bridge.hello
        args = [hello['window'], 1, 1, hello['width'], hello['height']]
        actual = self.call(0x413450, args)
        expected = project_owner(initial, hello['width'], hello['height'], hello['window'], actual['live_results'])
        owner = bytes(self.uc.mem_read(OWNER, 0xC000))
        if owner != expected or self.boundary != STOP:
            bad = [hex(i) for i, (a, b) in enumerate(zip(owner, expected)) if a != b]
            raise RuntimeError('original startup full-owner/font boundary '+repr(bad[:24]))
        if bytes(self.uc.mem_read(BASE, len(self.image))) != self.image:
            raise RuntimeError('original startup image/IAT changed')
        maps = []
        for at, raw in sorted(self.foreign.items()):
            if bytes(self.uc.mem_read(at, 4096)) != raw:
                raise RuntimeError('foreign live interface memory changed')
            maps.append(dict(pointer=at, **buffer_evidence(bytes(raw))))
        if bytes(self.uc.mem_read(STACK, TOP-4096-STACK)) != bytes([0xA5])*(TOP-4096-STACK):
            raise RuntimeError('original startup lower stack guard')
        if bytes(self.uc.mem_read(TOP+24, STACK+65536-TOP-24)) != bytes([0xA5])*(STACK+65536-TOP-24):
            raise RuntimeError('original startup upper stack guard')
        return dict(hello=hello, declared_owner=buffer_evidence(declared), initial_owner=buffer_evidence(initial),
                    constructor=ctor, root_args=args, actual=actual, after_owner=buffer_evidence(owner),
                    source_image_sha256=digest(self.image), original_IAT_target=self.import_target,
                    original_IAT_unchanged=True, foreign_maps=maps, stack_guards_unchanged=True,
                    pending_font=dict(va=hex(STOP), return_va=hex(self.read(TOP-92)), sp=TOP-92,
                                      receiver=OWNER, args=[], first_instruction_executed=False),
                    retained_VM_advanced=False, owner_bound=False, queues_initialized=False,
                    drawing_or_Present=False, live_pointers_resumable_after_cleanup=False)


def generate():
    provenance = json.loads((ROOT/'analysis/school-device-init-bridge-v1-20261017.json').read_text(encoding='utf-8'))['build']
    helper = ROOT/'.venv-audit/school-device-init-bridge.exe'
    if sha(helper.read_bytes()) != provenance['helper_sha256']:
        raise ValueError('fixed live bridge identity required')
    cases = []
    for width, height in ((640, 480), (1024, 768)):
        with DeviceBridge(helper, width, height) as bridge:
            case = DeviceEmulator(bridge).run()
        case.update(bridge_trace=bridge.trace, cleanup=bridge.cleanup)
        if not bridge.cleanup['all_owned_resources_released']:
            raise ValueError('original startup live resource cleanup')
        cases.append(case)
        print(str(width)+'x'+str(height)+': original startup reached font boundary with real device', flush=True)
    return dict(schema_version=1, source_contract=source_contract(), bridge_build=provenance,
                cases=cases, live_device_initialization_executed=True, original_helpers_stubbed=False,
                retained_VM_advanced=False, drawing_or_Present=False, full_outer_frame=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    path = ROOT/a.out
    if path.exists():
        p.error('fresh immutable report required')
    report = generate()
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')

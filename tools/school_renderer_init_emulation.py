"""Execute isolated original renderer prerequisites with declared CRT allocations."""
import argparse
import base64
import hashlib
import json
import struct
import zlib

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import (
    UC_X86_REG_EIP, UC_X86_REG_ESP, UC_X86_REG_EBP, UC_X86_REG_EAX,
    UC_X86_REG_EBX, UC_X86_REG_ECX, UC_X86_REG_EDX, UC_X86_REG_ESI,
    UC_X86_REG_EDI, UC_X86_REG_EFLAGS,
)
from tools.school_renderer_init import *

OWNER = 0x2000000
MANAGER = OWNER + 0x1058
HEADS = 0x2101000
ARENA = 0x2201000
STACK = 0x2400000
TOP = STACK + 0xF000
RETURN = 0x2500000
COUNTER = 0x79FC74
REGISTERS = dict(EIP=UC_X86_REG_EIP, ESP=UC_X86_REG_ESP, EBP=UC_X86_REG_EBP,
                 EAX=UC_X86_REG_EAX, EBX=UC_X86_REG_EBX, ECX=UC_X86_REG_ECX,
                 EDX=UC_X86_REG_EDX, ESI=UC_X86_REG_ESI, EDI=UC_X86_REG_EDI,
                 EFLAGS=UC_X86_REG_EFLAGS)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def buffer_evidence(raw):
    return dict(bytes=len(raw), sha256=digest(raw),
                zlib_base64=base64.b64encode(zlib.compress(raw, 9)).decode('ascii'))


class RendererEmulator:
    def __init__(self, dimensions=(1024, 768), device=0x13572468, gate=1):
        source_contract()
        self.uc = Uc(UC_ARCH_X86, UC_MODE_32)
        self.image = SOURCE.read_bytes()
        self.uc.mem_map(BASE, (len(self.image)+4095) & ~4095)
        self.uc.mem_write(BASE, self.image)
        for address, count in ((OWNER, 0xC000), (HEADS-4096, 40960),
                               (ARENA-4096, ARENA_BYTES+8192), (STACK, 65536),
                               (RETURN, 4096)):
            self.uc.mem_map(address, count)
            self.uc.mem_write(address, bytes([0xA5])*count)
        self.uc.mem_write(OWNER+0xB210, struct.pack('<I', device))
        self.uc.mem_write(OWNER+0xB278, struct.pack('<2I', *map(u32, dimensions)))
        self.uc.mem_write(OWNER+0xB28E, struct.pack('<H', gate))
        self.uc.mem_write(HEADS, bytes([0xCD])*(LAYER_COUNT*8))
        self.uc.mem_write(ARENA, bytes([0xCD])*ARENA_BYTES)
        self.initial_owner = bytes(self.uc.mem_read(OWNER, 0xC000))
        self.counter = self.read(COUNTER)
        self.inputs = dict(dimensions=list(dimensions), device=device, gate=gate,
                           owner=OWNER, manager=MANAGER, heads=HEADS, arena=ARENA,
                           explicitly_declared_scratch_state=True)
        self.allocated = []
        self.calls = []
        self.uc.hook_add(UC_HOOK_CODE, self._code)
        self.uc.hook_add(UC_HOOK_MEM_WRITE, self._write)

    def read(self, at):
        return struct.unpack('<I', bytes(self.uc.mem_read(at, 4)))[0]

    def _write(self, uc, access, at, size, value, user):
        allowed = ((STACK, STACK+65536), (MANAGER, MANAGER+96),
                   (HEADS, HEADS+LAYER_COUNT*8), (ARENA, ARENA+ARENA_BYTES),
                   (COUNTER, COUNTER+4))
        if not any(a <= at and at+size <= b for a, b in allowed):
            raise RuntimeError('renderer forbidden native write: ' + hex(at))
        if COUNTER <= at < COUNTER+4 and self.root != 0x40DAB0:
            raise RuntimeError('renderer allocation counter outside initialization')

    def _code(self, uc, at, size, user):
        if at == RETURN:
            self.stopped = 'returned'
            uc.emu_stop()
            return
        sp = uc.reg_read(UC_X86_REG_ESP)
        if at == 0x424F80:
            self.stopped = 'unexecuted_debug'
            self.pending = dict(va=hex(at), return_va=hex(self.read(sp)), sp=sp,
                                args=[self.read(sp+4+i*4) for i in range(4)],
                                instruction_executed=False)
            uc.emu_stop()
            return
        if at == 0x56E810:
            args = [self.read(sp+4+i*4) for i in range(4)]
            count = args[0]
            ordinal = len(self.allocated)
            expected = (LAYER_COUNT*8, ARENA_BYTES)
            if (self.root != 0x40DAB0 or ordinal >= 2 or count != expected[ordinal]
                    or self.read(sp) != 0x428A73 or args[1] != 1
                    or args[2] != 0x594E28
                    or args[3] != struct.unpack_from('<h', self.image, 0x5FF6D8-BASE)[0]+3):
                raise RuntimeError('undeclared CRT allocation/caller/arguments')
            pointer = (HEADS, ARENA)[ordinal]
            self.allocated.append(dict(va=hex(at), return_va=hex(self.read(sp)),
                                       args=args, result=pointer,
                                       adapter='declared debug CRT allocation'))
            uc.reg_write(UC_X86_REG_EAX, pointer)
            uc.reg_write(UC_X86_REG_ESP, sp+4)
            uc.reg_write(UC_X86_REG_EIP, self.read(sp))
            return
        if not any(a <= at and at+size <= b for a, b in FUNCTIONS.items()):
            raise RuntimeError('undeclared renderer native instruction: ' + hex(at))
        self.visited.add(at)
        if at in FUNCTIONS and at != 0x56CE80:
            self.entries.append(dict(va=hex(at), return_va=hex(self.read(sp)), sp=sp,
                                     receiver=uc.reg_read(UC_X86_REG_ECX),
                                     args=[self.read(sp+4+i*4)
                                           for i in range(ARG_COUNTS.get(at, 0))]))

    def call(self, va, args=(), receiver=MANAGER, expected_debug=False):
        self.root = va
        self.stopped = None
        self.pending = None
        self.entries = []
        self.visited = set()
        for name, value in dict(ESP=TOP, EBP=0x11223344, EBX=0x55667788,
                                ESI=0x88776655, EDI=0x44332211,
                                ECX=receiver, EAX=0, EDX=0, EFLAGS=2).items():
            self.uc.reg_write(REGISTERS[name], value)
        self.uc.mem_write(TOP, struct.pack('<'+'I'*(1+len(args)), RETURN, *map(u32, args)))
        self.uc.emu_start(va, RETURN+1, timeout=10_000_000, count=1000000)
        cpu = {name: self.uc.reg_read(reg) for name, reg in REGISTERS.items()}
        if expected_debug:
            if self.stopped != 'unexecuted_debug':
                raise RuntimeError('expected original debug admission')
        else:
            cdecl = va in (0x428A40, 0x56DB00, 0x56CEC0)
            expected_sp = TOP+4+(0 if cdecl else len(args)*4)
            if self.stopped != 'returned' or cpu['ESP'] != expected_sp:
                raise RuntimeError('original renderer return/ABI mismatch')
            for name, expected in dict(EBP=0x11223344, EBX=0x55667788,
                                       ESI=0x88776655, EDI=0x44332211).items():
                if cpu[name] != expected:
                    raise RuntimeError('original renderer callee-save mismatch: '+name)
        result = dict(root=hex(va), args=list(map(u32, args)), receiver=receiver,
                      status=self.stopped, cpu=cpu, entries=self.entries,
                      visited=sorted(self.visited), pending=self.pending)
        self.calls.append(result)
        return result

    def check(self, manager, heads, arena, counter):
        actual = [bytes(self.uc.mem_read(MANAGER, 96)),
                  bytes(self.uc.mem_read(HEADS, LAYER_COUNT*8)),
                  bytes(self.uc.mem_read(ARENA, ARENA_BYTES))]
        for name, left, right in zip(('manager', 'heads', 'arena'), actual,
                                     (manager, heads, arena)):
            if left != right:
                raise RuntimeError('renderer full buffer mismatch: '+name)
        if self.read(COUNTER) != u32(counter):
            raise RuntimeError('original allocator counter mismatch')
        image = bytearray(self.uc.mem_read(BASE, len(self.image)))
        image[COUNTER-BASE:COUNTER-BASE+4] = self.image[COUNTER-BASE:COUNTER-BASE+4]
        if bytes(image) != self.image:
            raise RuntimeError('original image/global retention mismatch')
        owner = bytearray(self.uc.mem_read(OWNER, 0xC000))
        owner[0x1058:0x10B8] = self.initial_owner[0x1058:0x10B8]
        if bytes(owner) != self.initial_owner:
            raise RuntimeError('unowned owner bytes changed')
        for at, count in ((HEADS-4096, 4096), (HEADS+LAYER_COUNT*8, 4096),
                          (ARENA-4096, 4096), (ARENA+ARENA_BYTES, 4096)):
            if bytes(self.uc.mem_read(at, count)) != bytes([0xA5])*count:
                raise RuntimeError('renderer buffer guard changed')
        return dict(manager_hex=actual[0].hex(), heads=buffer_evidence(actual[1]),
                    arena=buffer_evidence(actual[2]), counter=u32(counter),
                    retained_image_sha256=digest(image),
                    retained_owner_sha256=digest(owner), guards_unchanged=True)


def initialize(device=0x13572468):
    e = RendererEmulator(device=device)
    manager = bytes([0xA5])*96
    heads = bytes([0xCD])*(LAYER_COUNT*8)
    arena = bytes([0xCD])*ARENA_BYTES
    records = []
    call = e.call(0x40D7E0)
    manager = constructor(manager)
    if call['cpu']['EAX'] != MANAGER:
        raise RuntimeError('constructor original receiver return')
    records.append(dict(stage='constructor', call=call,
                        state=e.check(manager, heads, arena, e.counter)))
    call = e.call(0x40D970, (OWNER,))
    manager = bind(manager, OWNER, device)
    if call['cpu']['EAX'] != 0:
        raise RuntimeError('owner binder original return')
    records.append(dict(stage='bind', call=call,
                        state=e.check(manager, heads, arena, e.counter)))
    call = e.call(0x40DAB0)
    manager = initialize_queues(manager, HEADS, ARENA)
    heads = bytes(LAYER_COUNT*8)
    arena = bytes(ARENA_BYTES)
    if call['cpu']['EAX'] != 0 or len(e.allocated) != 2:
        raise RuntimeError('queue initializer original return/allocations')
    records.append(dict(stage='queues', call=call,
                        state=e.check(manager, heads, arena,
                                      e.counter+LAYER_COUNT*8+ARENA_BYTES)))
    return e, manager, heads, arena, records


def initialization_report():
    cases = []
    # Null device is a declared getter value, not a valid D3D device assertion.
    for device in (0, 0x13572468):
        e, manager, heads, arena, records = initialize(device)
        cases.append(dict(inputs=e.inputs, stages=records, allocations=e.allocated))
    return dict(schema_version=1, source_contract=source_contract(), cases=cases,
                isolated_experiments=True, retained_VM_advanced=False,
                D3D_initialized=False, GPU_executed=False, full_outer_frame=False)


def write_report(path, report):
    if path.exists():
        raise ValueError('immutable report already exists: '+str(path))
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n',
                    encoding='utf-8', newline='\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    write_report(ROOT/a.out, initialization_report())

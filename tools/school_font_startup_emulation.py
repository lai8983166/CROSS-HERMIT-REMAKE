"""Original font factory on inherited cache state and an explicit empty-cache probe."""
import argparse
import json
import struct
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_owner_startup_emulation import OwnerEmulator, OWNER, STACK, TOP, RETURN
from tools.school_owner_platform import OwnerPlatform
from tools.school_font_device_bridge import owned_run
from tools.school_font_startup import *
from tools.school_renderer_init_emulation import REGISTERS, buffer_evidence, digest


class FontEmulator(OwnerEmulator):
    def __init__(self, bridge, platform, fill):
        self.factory_running = False
        super().__init__(bridge, platform, fill)

    def _write(self, uc, access, at, size, value, user):
        if self.factory_running:
            allowed = [(STACK, STACK+65536), (COUNTER, COUNTER+4)]
            allowed += [(r['pointer'], r['pointer']+r['bytes']) for r in self.allocations]
            if self.mode == 'empty':
                allowed.append((HEAD, HEAD+4))
            if not any(a <= at and at+size <= b for a, b in allowed):
                raise RuntimeError('font factory unowned native write '+hex(at))
            return
        return super()._write(uc, access, at, size, value, user)

    def _allocation(self, sp):
        ordinal = len(self.allocations)
        count = (80, 176)[ordinal] if ordinal < (2 if self.mode == 'empty' else 1) else None
        args = [self.read(sp+4+i*4) for i in range(4)]
        line = struct.unpack_from('<h', self.image, 0x5FF6D8-BASE)[0]+3
        if self.read(sp) != 0x428A73 or args != [count, 1, 0x594E28, line]:
            raise RuntimeError('font exact original debug CRT allocation boundary')
        pointer = (FONT, CACHE)[ordinal]
        self.uc.mem_write(pointer, b'\xcd'*count)
        self.allocations.append(dict(va='0x56e810', return_va='0x428a73', sp=sp, args=args,
                                     pointer=pointer, bytes=count, initial_hex='cd'*count,
                                     adapter='declared debug CRT allocation'))
        self.uc.reg_write(UC_X86_REG_EAX, pointer)
        self.uc.reg_write(UC_X86_REG_ESP, sp+4)
        self.uc.reg_write(UC_X86_REG_EIP, self.read(sp))

    def _cache_api(self, at, sp, ret):
        op, slot, count = {0x54875E: ('cache_addref', 4, 1),
                           0x54876E: ('cache_caps', 28, 2),
                           0x54877B: ('cache_creation', 36, 2)}[ret]
        obj = self.objects['device']
        args = [self.read(sp+4+i*4) for i in range(count)]
        expected = [obj['pointer']]
        if count == 2:
            expected.append(TOP-700 if op == 'cache_caps' else TOP-488)
        if at != obj['methods'][str(slot)] or args != expected:
            raise RuntimeError('font original cache device caller/ABI')
        request = dict(pointer=obj['pointer'])
        result = self.bridge.request(op, **request)
        if count == 2:
            self._put(args[1], bytes.fromhex(result['hex']))
        eax = result['count'] if count == 1 else result['hr']
        self.cache_calls.append(dict(op=op, va=hex(at), return_va=hex(ret), sp=sp,
                                     args=args, request=request, result=result, live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX, u32(eax))
        self.uc.reg_write(UC_X86_REG_ESP, sp+4+count*4)
        self.uc.reg_write(UC_X86_REG_EIP, ret)

    def _code(self, uc, at, size, user):
        if not self.factory_running:
            return super()._code(uc, at, size, user)
        sp = uc.reg_read(UC_X86_REG_ESP)
        if at == STOPS[self.mode]:
            self.boundary = at
            uc.emu_stop()
            return
        ret = self.read(sp)
        if at == 0x56E810:
            return self._allocation(sp)
        if ret in (0x54875E, 0x54876E, 0x54877B):
            return self._cache_api(at, sp, ret)
        if not any(a <= at and at+size <= b for a, b in {**RANGES, 0x56CE80: 0x56CE83}.items()):
            raise RuntimeError('font undeclared original native body '+hex(at))
        self.visited.add(at)
        if at in RANGES:
            self.entries.append(dict(va=hex(at), return_va=hex(ret), sp=sp,
                                     receiver=uc.reg_read(REGISTERS['ECX']),
                                     args=[self.read(sp+4+i*4) for i in range(ARGS.get(at, 0))]))
        if at in self.factory_rets:
            self.returns.append(dict(va=hex(at), return_va=hex(ret), sp=sp,
                                     eax=uc.reg_read(UC_X86_REG_EAX)))

    def factory(self, mode):
        if self.uc.reg_read(UC_X86_REG_EIP) != 0x52AE11:
            raise RuntimeError('font original pending factory CPU required')
        before_cpu = {k: self.uc.reg_read(r) for k, r in REGISTERS.items()}
        self.mode, self.allocations, self.cache_calls = mode, [], []
        self.entries, self.returns, self.visited, self.boundary = [], [], set(), None
        for pointer in (FONT, CACHE):
            self.uc.mem_map(pointer-4096, 12288)
            self.uc.mem_write(pointer-4096, b'\xa5'*12288)
        declared = dict(mode=mode, inherited_head=self.read(HEAD),
                        initial_head=0 if mode == 'empty' else self.read(HEAD),
                        empty_cache_explicitly_declared=mode == 'empty',
                        retained_VM_or_source_file_changed=False)
        expected_image = bytearray(self.constructed_image)
        if mode == 'empty':
            self.uc.mem_write(HEAD, bytes(4))
            store(expected_image, HEAD-BASE, 0)
        declared['initial_image_sha256'] = digest(expected_image)
        owner = bytes(self.uc.mem_read(OWNER, 0xC000))
        md = Cs(CS_ARCH_X86, CS_MODE_32)
        self.factory_rets = {i.address for a, b in {**RANGES, 0x56CE80: 0x56CE83}.items()
                             for i in md.disasm(self.image[a-BASE:b-BASE], a) if i.mnemonic == 'ret'}
        self.factory_running = True
        try:
            self.uc.emu_start(0x52AE11, RETURN+1, timeout=15_000_000, count=100000)
        finally:
            self.factory_running = False
        count = 80+(176 if mode == 'empty' else 0)
        store(expected_image, COUNTER-BASE, self.read_initial_counter()+count)
        if mode == 'empty':
            store(expected_image, HEAD-BASE, CACHE)
        state = self.check(owner, bytes(expected_image), TOP-108)
        heaps = []
        for pointer, size in ((FONT, 80), (CACHE, 176)):
            expected = bytearray(b'\xa5'*12288)
            if pointer == FONT:
                expected[4096:4096+size] = font_constructor(b'\xcd'*size)
            elif mode == 'empty':
                expected[4096:4096+size] = cache_prefix(b'\xcd'*size, self.objects['device']['pointer'],
                                                      bytes.fromhex(self.cache_calls[1]['result']['hex']))
            actual = bytes(self.uc.mem_read(pointer-4096, 12288))
            if actual != expected:
                raise RuntimeError('font full heap and guard source projection '+hex(pointer))
            heaps.append(dict(pointer=pointer-4096, **buffer_evidence(actual)))
        cpu = {k: self.uc.reg_read(r) for k, r in REGISTERS.items()}
        pending = dict(va=hex(self.boundary or 0), first_instruction_executed=False)
        if mode == 'inherited':
            pending.update(base=cpu['EAX'], effective_address=cpu['EAX']+4, target_read=False,
                           target_memory_mapped=any(a <= cpu['EAX']+4 <= b for a, b, _ in self.uc.mem_regions()))
        else:
            pending.update(return_va=hex(self.read(cpu['ESP'])), sp=cpu['ESP'],
                           args=[self.read(cpu['ESP']+4+i*4) for i in range(7)])
        if self.read(TOP-228) != 0xCCCCCCCC:
            raise RuntimeError('font factory output must remain unassigned')
        return dict(declared=declared, before_cpu=before_cpu, entries=self.entries, returns=self.returns,
                    visited=sorted(self.visited), cpu=cpu, allocations=self.allocations,
                    cache_calls=self.cache_calls, state=state, heaps=heaps, pending=pending,
                    output_slot=dict(pointer=TOP-228, value=self.read(TOP-228)),
                    font_initialization_complete=False, texture_body_executed=False,
                    retained_VM_advanced=False)

    def read_initial_counter(self):
        return dword(self.constructed_image, COUNTER-BASE)


def generate(mode):
    cases = []
    for fill, width, height in ((0xA5, 640, 480), (0xCC, 1024, 768)):
        def run(bridge):
            with OwnerPlatform() as platform:
                engine = FontEmulator(bridge, platform, fill)
                case = dict(fill=fill, hello=bridge.hello, platform_hello=platform.hello,
                            constructor=engine.construct(), device=engine.device(), font=engine.font())
                case['factory'] = engine.factory(mode)
            case.update(platform_trace=platform.trace, platform_cleanup=platform.cleanup)
            return case
        result = owned_run(run, width, height)
        case = result['value']
        case.update(device_trace=result['trace'], device_cleanup=result['cleanup'],
                    refused_address_collisions=result['refused_address_collisions'])
        cases.append(case)
        print(hex(fill)+': original font factory '+mode+' boundary verified', flush=True)
    return dict(schema_version=1, mode=mode, source_contract=source_contract(), cases=cases,
                device_build=json.loads((ROOT/'analysis/school-font-startup-bridge-v1-20261018.json').read_text())['build'],
                platform_build=json.loads((ROOT/'analysis/school-owner-startup-platform-v2-20261017.json').read_text())['build'],
                original_IAT_changed=False, game_helpers_stubbed=False, CRT_adapter_executed=True,
                retained_VM_advanced=False, drawing_or_Present=False, full_outer_frame=False,
                live_handles_resumable_after_cleanup=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=tuple(STOPS), required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    path = ROOT/args.out
    if path.exists():
        parser.error('fresh immutable report required')
    path.write_text(json.dumps(generate(args.mode), indent=2)+'\n', encoding='utf-8', newline='\n')

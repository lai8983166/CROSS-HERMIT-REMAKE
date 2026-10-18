"""Continue the live first-font CPU through native additional-slot atlas admission."""
import argparse
import json
import struct
from unicorn import UC_HOOK_MEM_READ
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_font_cache_emulation import CacheEmulator, OWNER, STACK, TOP, RETURN
from tools.school_font_cache_platform import CachePlatform, owned_run
from tools.school_font_cache import FONT, CACHE, SPRITE, HEAD, COUNTER
from tools.school_font_slots import *
from tools.school_renderer_init_emulation import REGISTERS, buffer_evidence


class SlotEmulator(CacheEmulator):
    def __init__(self, bridge, platform, fill):
        self.slot_running = False
        super().__init__(bridge, platform, fill)
        self.uc.hook_add(UC_HOOK_MEM_READ, self._slot_read)

    def _map_page(self, address):
        if SLOT-4096 <= address < SLOT+8192:
            raise RuntimeError('live interface mapping collides with audit ownership')
        return super()._map_page(address)

    def _slot_read(self, uc, access, at, size, value, user):
        if not self.slot_running:
            return
        allowed = [(BASE, BASE+len(self.image)), (OWNER, OWNER+0xC000), (STACK, STACK+65536), (0, 4)]
        allowed += [(p, p+n) for p, n in ((FONT, 80), (CACHE, 176), (SPRITE, 32), (SLOT, SIZE))]
        allowed += [(p, p+4096) for p in self.foreign]
        if not any(a <= at and at+size <= b for a, b in allowed):
            raise RuntimeError('font slot unowned native read '+hex(at))

    def _write(self, uc, access, at, size, value, user):
        if not self.slot_running:
            return super()._write(uc, access, at, size, value, user)
        if not any(a <= at and at+size <= b for a, b in ((STACK, STACK+65536),
                (SLOT, SLOT+SIZE), (COUNTER, COUNTER+4), (OWNER+0x1090, OWNER+0x1094))):
            raise RuntimeError('font slot unowned native write '+hex(at))

    def _slot_allocation(self, sp):
        args = [self.read(sp+4+i*4) for i in range(4)]
        line = struct.unpack_from('<h', self.image, 0x5FF6D8-BASE)[0]+3
        if self.read(sp) != 0x428A73 or args != [SIZE, 1, 0x594E28, line] or self.slot_allocations:
            raise RuntimeError('font slot exact original CRT allocation')
        self.uc.mem_write(SLOT, b'\xcd'*SIZE)
        self.slot_allocations.append(dict(va='0x56e810', return_va='0x428a73', sp=sp, args=args,
                                         pointer=SLOT, bytes=SIZE, initial_hex='cd'*SIZE,
                                         adapter='declared debug CRT allocation'))
        self.uc.reg_write(UC_X86_REG_EAX, SLOT)
        self.uc.reg_write(UC_X86_REG_ESP, sp+4)
        self.uc.reg_write(UC_X86_REG_EIP, self.read(sp))

    def _slot_caps(self, at, sp, ret):
        obj = self.objects['device']
        args = [self.read(sp+4), self.read(sp+8)]
        if at != obj['methods']['28'] or ret != 0x401173 or args != [obj['pointer'], TOP-440]:
            raise RuntimeError('font slot actual caps identity/ABI')
        request = dict(pointer=obj['pointer'])
        result = self.bridge.request('caps', **request)
        if result['hr'] != 0 or len(bytes.fromhex(result['hex'])) != 212:
            raise RuntimeError('font slot live complete device caps prerequisite')
        self._put(args[1], bytes.fromhex(result['hex']))
        self.slot_calls.append(dict(op='caps', va=hex(at), return_va=hex(ret), sp=sp,
                                    args=args, request=request, result=result, live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX, result['hr'])
        self.uc.reg_write(UC_X86_REG_ESP, sp+12)
        self.uc.reg_write(UC_X86_REG_EIP, ret)

    def _code(self, uc, at, size, user):
        if not self.slot_running:
            return super()._code(uc, at, size, user)
        sp = uc.reg_read(UC_X86_REG_ESP)
        if at == self.slot_stop:
            self.boundary = at
            uc.emu_stop()
            return
        ret = self.read(sp)
        if at == 0x56E810:
            return self._slot_allocation(sp)
        if ret == 0x401173 and at == self.objects['device']['methods']['28']:
            return self._slot_caps(at, sp, ret)
        if not any(a <= at and at+size <= b for a, b in RANGES.items()):
            raise RuntimeError('font slot undeclared native body '+hex(at))
        self.visited.add(at)
        if at in ARGS:
            self.entries.append(dict(va=hex(at), return_va=hex(ret), sp=sp,
                                     receiver=uc.reg_read(REGISTERS['ECX']),
                                     args=[self.read(sp+4+i*4) for i in range(ARGS[at])]))
        if at in self.slot_rets:
            self.returns.append(dict(va=hex(at), return_va=hex(ret), sp=sp,
                                     eax=uc.reg_read(UC_X86_REG_EAX)))

    def resume_slot(self, phase):
        start, stop = (0x416021, 0x4010D0) if phase == 'constructor' else (0x4010D0, 0x40120C)
        if self.uc.reg_read(UC_X86_REG_EIP) != start:
            raise RuntimeError('font slot same pending original CPU required')
        before_cpu = {k: self.uc.reg_read(r) for k, r in REGISTERS.items()}
        if phase == 'constructor':
            self.uc.mem_map(SLOT-4096, 12288)
            self.uc.mem_write(SLOT-4096, b'\xa5'*12288)
            self.slot_allocations = []
        prior_heaps = [bytes(self.uc.mem_read(p-4096, 12288)) for p in (FONT, CACHE, SPRITE)]
        self.entries, self.returns, self.slot_calls, self.visited, self.boundary = [], [], [], set(), None
        md = Cs(CS_ARCH_X86, CS_MODE_32)
        self.slot_rets = {i.address for a, b in RANGES.items() for i in md.disasm(self.image[a-BASE:b-BASE], a) if i.mnemonic == 'ret'}
        self.slot_stop, self.slot_running = stop, True
        try:
            self.uc.emu_start(start, RETURN+1, timeout=15_000_000, count=100000)
        finally:
            self.slot_running = False
        if self.boundary != stop:
            raise RuntimeError('font slot native boundary not reached')
        image = bytearray(self.constructed_image)
        store(image, COUNTER-BASE, dword(image, COUNTER-BASE)+288+SIZE)
        store(image, HEAD-BASE, CACHE)
        owner = bytearray(self.device_owner)
        for at, value in ((0xB26C, self.font_handle), (0xB270, FONT), (0x1090, SLOT)):
            store(owner, at, value)
        state = self.check(bytes(owner), bytes(image), TOP-108)
        value = constructor(b'\xcd'*SIZE)
        if phase == 'atlas':
            maximum = dword(bytes.fromhex(self.slot_calls[0]['result']['hex']), 88)
            value = atlas(value, self.objects['device']['pointer'], maximum)
        expected = bytearray(b'\xa5'*12288)
        expected[4096:4096+SIZE] = value
        actual = bytes(self.uc.mem_read(SLOT-4096, 12288))
        if actual != expected:
            raise RuntimeError('font slot full constructor/atlas/guard mismatch')
        heaps = []
        for p, before in zip((FONT, CACHE, SPRITE), prior_heaps):
            observed = bytes(self.uc.mem_read(p-4096, 12288))
            if observed != before:
                raise RuntimeError('font slot modified prior heap '+hex(p))
            heaps.append(dict(pointer=p-4096, **buffer_evidence(observed)))
        cpu = {k: self.uc.reg_read(r) for k, r in REGISTERS.items()}
        pending = dict(va=hex(stop), sp=cpu['ESP'], first_instruction_executed=False)
        if phase == 'constructor':
            pending.update(return_va=hex(self.read(cpu['ESP'])), args=[self.read(cpu['ESP']+4)], receiver=SLOT)
        else:
            pending.update(method_target=self.read(cpu['EDX']+80),
                           args=[self.read(cpu['ESP']+i*4) for i in range(8)], platform_call_executed=False)
        return dict(phase=phase, before_cpu=before_cpu, entries=self.entries, returns=self.returns,
                    allocations=list(self.slot_allocations) if phase == 'constructor' else [],
                    api_calls=self.slot_calls, visited=sorted(self.visited), state=state, heaps=heaps,
                    slot_heap=dict(pointer=SLOT-4096, **buffer_evidence(actual)), cpu=cpu, pending=pending,
                    native_CRT_face_copy_executed=phase == 'constructor', first_slot_bound=True,
                    second_slot_bound=False, atlas_texture_created=False, additional_fonts_completed=False,
                    full415F50_returned=False, state_blocks_created=False, retained_VM_advanced=False)


def generate(phase):
    cases = []
    for fill, width, height in ((0xA5, 640, 480), (0xCC, 1024, 768)):
        def run(bridge):
            with CachePlatform() as platform:
                e = SlotEmulator(bridge, platform, fill)
                case = dict(fill=fill, hello=bridge.hello, platform_hello=platform.hello,
                            constructor=e.construct(), device=e.device(), font=e.font(), factory=e.factory('empty'))
                e.source_logfont = case['font']['LOGFONT']
                case['requirements'], case['texture'] = e.resume('requirements'), e.resume('texture')
                case['sprite'], case['font_return'] = e.resume_cache('sprite'), e.resume_cache('font')
                case['slot_constructor'] = e.resume_slot('constructor')
                if phase == 'atlas':
                    case['atlas_admission'] = e.resume_slot('atlas')
            case.update(platform_trace=platform.trace, platform_cleanup=platform.cleanup)
            return case
        result = owned_run(run, width, height)
        case = result['value']
        case.update(device_trace=result['trace'], device_cleanup=result['cleanup'], refused_address_collisions=result['refused_address_collisions'])
        cases.append(case)
        print(hex(fill)+': additional slot '+phase+' verified', flush=True)
    builds = json.loads((ROOT/'analysis/school-font-cache-platform-v1-20261018.json').read_text())['builds']
    return dict(schema_version=1, phase=phase, source_contract=source_contract(), cases=cases,
                device_build=builds['device'], platform_build=builds['gdi'],
                explicit_empty_cache_experiment=True, CRT_adapter_executed=True, original_IAT_changed=False,
                game_helpers_stubbed=False, retained_VM_advanced=False, drawing_or_Present=False,
                full_outer_frame=False, live_handles_resumable_after_cleanup=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--phase', choices=('constructor', 'atlas'), required=True)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    path = ROOT/a.out
    if path.exists(): p.error('fresh immutable font slots report required')
    path.write_text(json.dumps(generate(a.phase), indent=2)+'\n', encoding='utf-8', newline='\n')

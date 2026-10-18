"""Resume the original pending additional atlas call with owned real resources."""
import argparse
import json
import struct
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_font_slots_emulation import SlotEmulator, OWNER, STACK, TOP, RETURN
from tools.school_font_atlas_device import owned_run
from tools.school_font_cache_platform import CachePlatform
from tools.school_font_cache import FONT, CACHE, SPRITE, COUNTER, HEAD
from tools.school_font_atlas import *
from tools.school_renderer_init_emulation import REGISTERS, buffer_evidence
from tools.school_device_init_verification import unpack


class AtlasEmulator(SlotEmulator):
    def __init__(self, bridge, platform, fill):
        self.atlas_running = False
        super().__init__(bridge, platform, fill)

    def _write(self, uc, access, at, size, value, user):
        if not self.atlas_running:
            return super()._write(uc, access, at, size, value, user)
        if not any(a <= at and at+size <= b for a, b in ((STACK, STACK+65536), (SLOT+0x5C, SLOT+0x60))):
            raise RuntimeError('atlas preparation unowned native write '+hex(at))

    def _slot_read(self, uc, access, at, size, value, user):
        if not self.atlas_running:
            return super()._slot_read(uc, access, at, size, value, user)
        allowed = [(BASE, BASE+len(self.image)), (OWNER, OWNER+0xC000), (STACK, STACK+65536)]
        allowed += [(p, p+n) for p, n in ((FONT, 80), (CACHE, 176), (SPRITE, 32), (SLOT, SIZE))]
        allowed += [(p, p+4096) for p in self.foreign]
        if not any(a <= at and at+size <= b for a, b in allowed):
            raise RuntimeError('atlas preparation unowned native read '+hex(at))

    def _put(self, at, raw):
        if self.atlas_running and at == SLOT+0x5C and len(raw) == 4:
            self.uc.mem_write(at, raw)
            return
        return super()._put(at, raw)

    def _create_atlas(self, at, sp, ret):
        device = self.objects['device']
        args = [self.read(sp+4+i*4) for i in range(8)]
        if at != device['methods']['80'] or ret != 0x40120F or args != [device['pointer'], 256, 256, 1, 0, 26, 1, SLOT+0x5C]:
            raise RuntimeError('atlas original real texture caller/ABI')
        request = dict(pointer=device['pointer'], width=256, height=256, levels=1, usage=0, format=26, pool=1)
        result = self.bridge.request('atlas_create', **request)
        if result['hr'] != 0: raise RuntimeError('atlas real texture prerequisite')
        self._identity('atlas_texture', result['texture'])
        self._put(args[-1], struct.pack('<I', result['texture']['pointer']))
        self.atlas_calls.append(dict(op='atlas_create', va=hex(at), return_va=hex(ret), sp=sp,
            args=args, request=request, result=result, live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX, result['hr'])
        self.uc.reg_write(UC_X86_REG_ESP, sp+36)
        self.uc.reg_write(UC_X86_REG_EIP, ret)

    def _code(self, uc, at, size, user):
        if not self.atlas_running: return super()._code(uc, at, size, user)
        sp = uc.reg_read(UC_X86_REG_ESP)
        if at == self.atlas_stop:
            self.boundary = at; uc.emu_stop(); return
        ret = self.read(sp)
        if ret == 0x40120F and at == self.objects['device']['methods']['80']:
            return self._create_atlas(at, sp, ret)
        if not any(a <= at and at+size <= b for a, b in RANGES.items()):
            raise RuntimeError('atlas preparation undeclared native body '+hex(at))
        self.visited.add(at)
        if at in (0x56CEC0, 0x56CFCC):
            self.entries.append(dict(va=hex(at), return_va=hex(ret), sp=sp,
                receiver=uc.reg_read(REGISTERS['ECX']), args=[self.read(sp+4+i*4) for i in range(3 if at == 0x56CEC0 else 0)]))
        if at in self.atlas_rets:
            self.returns.append(dict(va=hex(at), return_va=hex(ret), sp=sp, eax=uc.reg_read(UC_X86_REG_EAX)))

    def resume_atlas(self, phase, previous):
        if phase != 'texture': raise ValueError('atlas texture phase required')
        start, stop = 0x40120C, self.read(0x592094)
        if self.uc.reg_read(UC_X86_REG_EIP) != start:
            raise RuntimeError('atlas same pending original CPU required')
        before_cpu = {k: self.uc.reg_read(r) for k, r in REGISTERS.items()}
        self.entries, self.returns, self.atlas_calls, self.visited, self.boundary = [], [], [], set(), None
        md = Cs(CS_ARCH_X86, CS_MODE_32)
        self.atlas_rets = {i.address for a, b in RANGES.items() for i in md.disasm(self.image[a-BASE:b-BASE], a) if i.mnemonic == 'ret'}
        self.atlas_stop, self.atlas_running = stop, True
        try: self.uc.emu_start(start, RETURN+1, timeout=15_000_000, count=100000)
        finally: self.atlas_running = False
        if self.boundary != stop: raise RuntimeError('atlas native boundary not reached')
        image = bytearray(self.constructed_image)
        store(image, COUNTER-BASE, dword(image, COUNTER-BASE)+288+SIZE); store(image, HEAD-BASE, CACHE)
        state = self.check(unpack(previous['state']['owner']), bytes(image), TOP-108)
        value = texture_object(unpack(previous['slot_heap'])[4096:4096+SIZE], self.objects['atlas_texture']['pointer'])
        expected = bytearray(b'\xa5'*12288); expected[4096:4096+SIZE] = value
        actual = bytes(self.uc.mem_read(SLOT-4096, 12288))
        if actual != expected: raise RuntimeError('atlas complete slot/guard mismatch')
        for row in previous['heaps']:
            if bytes(self.uc.mem_read(row['pointer'], 12288)) != unpack(row):
                raise RuntimeError('atlas modified complete parent heap')
        cpu = {k: self.uc.reg_read(r) for k, r in REGISTERS.items()}
        pending = dict(va=hex(stop), sp=cpu['ESP'], first_instruction_executed=False,
                       return_va=hex(self.read(cpu['ESP'])), args=[self.read(cpu['ESP']+4)], platform_call_executed=False)
        return dict(phase=phase, before_cpu=before_cpu, entries=self.entries, returns=self.returns,
            api_calls=self.atlas_calls, visited=sorted(self.visited), state=state, heaps=previous['heaps'],
            slot_heap=dict(pointer=SLOT-4096, **buffer_evidence(actual)), cpu=cpu, pending=pending,
            bitmap_header=dict(pointer=TOP-488, hex=bytes(self.uc.mem_read(TOP-488, 40)).hex()),
            atlas_texture_created=True, GDI_prepared=False, glyph_measurement_executed=False,
            DIB_pixels_read=False, glyph_upload_executed=False, full415F50_returned=False,
            state_blocks_created=False, retained_VM_advanced=False)


def generate(phase):
    cases = []
    for fill, width, height in ((0xA5, 640, 480), (0xCC, 1024, 768)):
        def run(bridge):
            with CachePlatform() as platform:
                e = AtlasEmulator(bridge, platform, fill)
                case = dict(fill=fill, hello=bridge.hello, platform_hello=platform.hello,
                    constructor=e.construct(), device=e.device(), font=e.font(), factory=e.factory('empty'))
                e.source_logfont = case['font']['LOGFONT']
                case['requirements'], case['texture'] = e.resume('requirements'), e.resume('texture')
                case['sprite'], case['font_return'] = e.resume_cache('sprite'), e.resume_cache('font')
                case['slot_constructor'], case['atlas_admission'] = e.resume_slot('constructor'), e.resume_slot('atlas')
                case['atlas_texture'] = e.resume_atlas('texture', case['atlas_admission'])
            case.update(platform_trace=platform.trace, platform_cleanup=platform.cleanup)
            return case
        result = owned_run(run, width, height)
        case = result['value']
        case.update(device_trace=result['trace'], device_cleanup=result['cleanup'], refused_address_collisions=result['refused_address_collisions'])
        cases.append(case); print(hex(fill)+': original atlas '+phase+' verified', flush=True)
    device = json.loads((ROOT/'analysis/school-font-atlas-device-v1-20261018.json').read_text())['build']
    gdi = json.loads((ROOT/'analysis/school-font-cache-platform-v1-20261018.json').read_text())['builds']['gdi']
    return dict(schema_version=1, phase=phase, source_contract=source_contract(), cases=cases,
        device_build=device, platform_build=gdi, explicit_empty_cache_experiment=True, CRT_adapter_executed=True,
        original_IAT_changed=False, game_helpers_stubbed=False, retained_VM_advanced=False, drawing_or_Present=False,
        full_outer_frame=False, live_handles_resumable_after_cleanup=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--phase', choices=('texture',), required=True); p.add_argument('--out', required=True)
    a = p.parse_args(); path = ROOT/a.out
    if path.exists(): p.error('fresh immutable atlas execution report required')
    path.write_text(json.dumps(generate(a.phase), indent=2)+'\n', encoding='utf-8', newline='\n')

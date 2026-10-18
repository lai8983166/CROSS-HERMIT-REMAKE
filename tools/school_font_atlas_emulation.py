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

    def _atlas_gdi(self, at, sp, ret):
        slot, name, _, count, op = next(r for r in IMPORTS if r[2] == ret)
        if at != self.read(slot): raise RuntimeError('atlas original GDI target')
        args = [self.read(sp+4+i*4) for i in range(count)]
        if op == 'atlas_dc':
            expected, request = [0], {}
        elif op == 'atlas_dib':
            expected = [self.atlas_dc, TOP-488, 0, TOP-444, 0, 0]
            request = dict(pointer=self.atlas_dc, header_hex=bytes(self.uc.mem_read(TOP-488, 40)).hex())
        elif op == 'atlas_muldiv':
            expected, request = [12, 96, 72], dict(args=[12, 96, 72])
        elif op == 'atlas_font':
            expected = [v & 0xFFFFFFFF for v in FONT_ARGS]+[SLOT]
            request = dict(args=FONT_ARGS, face_hex=bytes(self.uc.mem_read(SLOT, 8)).hex())
        elif op in ('atlas_bitmap_select', 'atlas_font_select'):
            obj = self.atlas_bitmap if op == 'atlas_bitmap_select' else self.atlas_font
            expected, request = [self.atlas_dc, obj], dict(pointer=self.atlas_dc, object=obj)
        else:
            value = dict(atlas_map=1, atlas_text=0xFFFFFF, atlas_background=0, atlas_align=0)[op]
            expected, request = [self.atlas_dc, value], dict(pointer=self.atlas_dc, value=value)
        if args != expected: raise RuntimeError('atlas exact original GDI arguments '+op)
        result = self.owner_bridge.request(op, **request)
        if op == 'atlas_dc': self.atlas_dc = result['result']
        elif op == 'atlas_dib':
            self.atlas_bitmap, self.atlas_bits = result['result'], result['bits']
            self._put(TOP-444, struct.pack('<I', self.atlas_bits))
        elif op == 'atlas_font': self.atlas_font = result['result']
        self.atlas_calls.append(dict(op=op, name=name, slot=hex(slot), va=hex(at), return_va=hex(ret), sp=sp,
            args=args, request=request, result=result, live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX, result['result'] & 0xFFFFFFFF)
        self.uc.reg_write(UC_X86_REG_ESP, sp+4+count*4)
        self.uc.reg_write(UC_X86_REG_EIP, ret)

    def _code(self, uc, at, size, user):
        if not self.atlas_running: return super()._code(uc, at, size, user)
        sp = uc.reg_read(UC_X86_REG_ESP)
        if at == self.atlas_stop:
            self.boundary = at; uc.emu_stop(); return
        ret = self.read(sp)
        if ret == 0x40120F and at == self.objects['device']['methods']['80']:
            return self._create_atlas(at, sp, ret)
        if ret in {r[2] for r in IMPORTS} and at == self.read(next(r[0] for r in IMPORTS if r[2] == ret)):
            return self._atlas_gdi(at, sp, ret)
        if not any(a <= at and at+size <= b for a, b in RANGES.items()):
            raise RuntimeError('atlas preparation undeclared native body '+hex(at))
        self.visited.add(at)
        if at in (0x56CEC0, 0x56CFCC):
            self.entries.append(dict(va=hex(at), return_va=hex(ret), sp=sp,
                receiver=uc.reg_read(REGISTERS['ECX']), args=[self.read(sp+4+i*4) for i in range(3 if at == 0x56CEC0 else 0)]))
        if at in self.atlas_rets:
            self.returns.append(dict(va=hex(at), return_va=hex(ret), sp=sp, eax=uc.reg_read(UC_X86_REG_EAX)))

    def resume_atlas(self, phase, previous):
        if phase not in ('texture', 'gdi'): raise ValueError('atlas texture/GDI phase required')
        start, stop = (0x40120C, self.read(0x592094)) if phase == 'texture' else (self.read(0x592094), 0x401491)
        if self.uc.reg_read(UC_X86_REG_EIP) != start:
            raise RuntimeError('atlas same pending original CPU required')
        before_cpu = {k: self.uc.reg_read(r) for k, r in REGISTERS.items()}
        if phase == 'gdi':
            for slot, *_ in IMPORTS: self._foreign_write(self.read(slot), b'\xc3')
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
        pending = dict(va=hex(stop), sp=cpu['ESP'], first_instruction_executed=False, platform_call_executed=False)
        if phase == 'texture':
            pending.update(return_va=hex(self.read(cpu['ESP'])), args=[self.read(cpu['ESP']+4)])
        else:
            pending.update(method_target=self.read(0x5920BC), args=[self.read(cpu['ESP']+i*4) for i in range(4)])
        return dict(phase=phase, before_cpu=before_cpu, entries=self.entries, returns=self.returns,
            api_calls=self.atlas_calls, visited=sorted(self.visited), state=state, heaps=previous['heaps'],
            slot_heap=dict(pointer=SLOT-4096, **buffer_evidence(actual)), cpu=cpu, pending=pending,
            bitmap_header=dict(pointer=TOP-488, hex=bytes(self.uc.mem_read(TOP-488, 40)).hex()),
            GDI_locals=None if phase == 'texture' else dict(dc=self.read(TOP-492), bitmap=self.read(TOP-496),
                bits=self.read(TOP-444), font=self.read(TOP-516), height=self.read(TOP-504),
                weight=self.read(TOP-508), italic=self.read(TOP-512), x=self.read(TOP-520), y=self.read(TOP-524),
                text_hex=bytes(self.uc.mem_read(TOP-528, 2)).hex(), character=bytes(self.uc.mem_read(TOP-540, 1)).hex()),
            atlas_texture_created=True, GDI_prepared=phase == 'gdi', glyph_measurement_executed=False,
            DIB_pixels_read=False, glyph_upload_executed=False, full415F50_returned=False,
            state_blocks_created=False, retained_VM_advanced=False)


def generate(phase):
    cases = []
    for fill, width, height in ((0xA5, 640, 480), (0xCC, 1024, 768)):
        def run(bridge):
            from tools.school_font_atlas_gdi import AtlasGDI
            with (CachePlatform() if phase == 'texture' else AtlasGDI()) as platform:
                e = AtlasEmulator(bridge, platform, fill)
                case = dict(fill=fill, hello=bridge.hello, platform_hello=platform.hello,
                    constructor=e.construct(), device=e.device(), font=e.font(), factory=e.factory('empty'))
                e.source_logfont = case['font']['LOGFONT']
                case['requirements'], case['texture'] = e.resume('requirements'), e.resume('texture')
                case['sprite'], case['font_return'] = e.resume_cache('sprite'), e.resume_cache('font')
                case['slot_constructor'], case['atlas_admission'] = e.resume_slot('constructor'), e.resume_slot('atlas')
                case['atlas_texture'] = e.resume_atlas('texture', case['atlas_admission'])
                if phase == 'gdi': case['GDI_preparation'] = e.resume_atlas('gdi', case['atlas_texture'])
            case.update(platform_trace=platform.trace, platform_cleanup=platform.cleanup)
            return case
        result = owned_run(run, width, height)
        case = result['value']
        case.update(device_trace=result['trace'], device_cleanup=result['cleanup'], refused_address_collisions=result['refused_address_collisions'])
        cases.append(case); print(hex(fill)+': original atlas '+phase+' verified', flush=True)
    device = json.loads((ROOT/'analysis/school-font-atlas-device-v1-20261018.json').read_text())['build']
    gdi = (json.loads((ROOT/'analysis/school-font-cache-platform-v1-20261018.json').read_text())['builds']['gdi']
           if phase == 'texture' else json.loads((ROOT/'analysis/school-font-atlas-gdi-v2-20261018.json').read_text())['build'])
    return dict(schema_version=1, phase=phase, source_contract=source_contract(), cases=cases,
        device_build=device, platform_build=gdi, explicit_empty_cache_experiment=True, CRT_adapter_executed=True,
        original_IAT_changed=False, game_helpers_stubbed=False, retained_VM_advanced=False, drawing_or_Present=False,
        full_outer_frame=False, live_handles_resumable_after_cleanup=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--phase', choices=('texture', 'gdi'), required=True); p.add_argument('--out', required=True)
    a = p.parse_args(); path = ROOT/a.out
    if path.exists(): p.error('fresh immutable atlas execution report required')
    path.write_text(json.dumps(generate(a.phase), indent=2)+'\n', encoding='utf-8', newline='\n')

"""Resume original sprite/cache GDI and first static font factories without new roots."""
import argparse
import json
import struct
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_font_texture_emulation import TextureEmulator, OWNER, STACK, TOP, RETURN
from tools.school_font_cache_platform import CachePlatform, owned_run
from tools.school_font_cache import *
from tools.school_font_startup import font_constructor, cache_prefix
from tools.school_font_texture import texture_cache
from tools.school_renderer_init_emulation import REGISTERS, buffer_evidence

DEVICE = {0x53BC2B: ('sprite_addref', 4, 1), 0x53BC38: ('sprite_caps', 28, 2),
          0x53BC45: ('sprite_creation', 36, 2), 0x53BA3C: ('font_addref', 4, 1)}


class CacheEmulator(TextureEmulator):
    def __init__(self, bridge, platform, fill):
        self.cache_running = False
        super().__init__(bridge, platform, fill)

    def _map_page(self, address):
        if SPRITE-4096 <= address < SPRITE+8192:
            raise RuntimeError('live interface mapping collides with audit ownership')
        return super()._map_page(address)

    def _write(self, uc, access, at, size, value, user):
        if not self.cache_running:
            return super()._write(uc, access, at, size, value, user)
        allowed = ((STACK, STACK+65536), (CACHE, CACHE+176), (FONT, FONT+80),
                   (SPRITE, SPRITE+32), (COUNTER, COUNTER+4), (OWNER, OWNER+0xC000))
        if not any(a <= at and at+size <= b for a, b in allowed):
            raise RuntimeError('cache native unowned write '+hex(at))

    def _put(self, at, raw):
        if self.cache_running and CACHE <= at and at+len(raw) <= CACHE+176:
            self.uc.mem_write(at, raw)
            return
        return super()._put(at, raw)

    def _cache_device(self, at, sp, ret):
        op, slot, count = DEVICE[ret]
        obj = self.objects['device']
        args = [self.read(sp+4+i*4) for i in range(count)]
        if at != obj['methods'][str(slot)] or args[0] != obj['pointer']:
            raise RuntimeError('cache original actual device interface')
        request = dict(pointer=args[0])
        result = self.bridge.request(op, **request)
        if count == 2:
            self._put(args[1], bytes.fromhex(result['hex']))
        self.device_calls.append(dict(op=op, va=hex(at), return_va=hex(ret), sp=sp,
                                      args=args, request=request, result=result, live_host_observed=True))
        eax = result['count'] if count == 1 else result['hr']
        self.uc.reg_write(UC_X86_REG_EAX, eax & 0xFFFFFFFF)
        self.uc.reg_write(UC_X86_REG_ESP, sp+4+4*count)
        self.uc.reg_write(UC_X86_REG_EIP, ret)

    def _gdi(self, at, sp, ret):
        slot, (name, expected_ret, count) = self.cache_imports[at]
        args = [self.read(sp+4+i*4) for i in range(count)]
        if ret != expected_ret:
            raise RuntimeError('cache original GDI caller '+name)
        request = {}
        if name == 'CreateCompatibleDC':
            expected = [0]
        elif name == 'CreateDIBSection':
            expected = [self.cache_dc, CACHE+0x70, 0, CACHE+0xA0, 0, 0]
            request = dict(pointer=self.cache_dc, header_hex=bytes(self.uc.mem_read(CACHE+0x70, 40)).hex())
            if request['header_hex'] != bitmap_header(True).hex():
                raise RuntimeError('cache original negative-height header')
        elif name in ('SetBkMode', 'SetBkColor', 'SetTextColor'):
            value = dict(SetBkMode=2, SetBkColor=0, SetTextColor=0xFFFFFF)[name]
            expected = [self.cache_dc, value]
            request = dict(pointer=self.cache_dc, value=value)
        elif name == 'SelectObject':
            expected = [self.cache_dc, self.cache_bitmap]
            request = dict(pointer=self.cache_dc, object=self.cache_bitmap)
        else:
            expected = [TOP-388]
            request = dict(logfont_hex=bytes(self.uc.mem_read(TOP-388, 60)).hex())
        if args != expected:
            raise RuntimeError('cache exact original GDI arguments '+name)
        result = self.owner_bridge.request(name, **request)
        if name == 'CreateCompatibleDC':
            self.cache_dc = result['result']
        elif name == 'CreateDIBSection':
            self.cache_bitmap, self.cache_bits = result['result'], result['bits']
            self._put(CACHE+0xA0, struct.pack('<I', self.cache_bits))
        elif name == 'SelectObject':
            self.old_bitmap = result['result']
        elif name == 'CreateFontIndirectA':
            self.indirect_font = result['result']
        self.gdi_calls.append(dict(name=name, slot=hex(slot), va=hex(at), return_va=hex(ret), sp=sp,
                                   args=args, request=request, result=result, live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX, result['result'] & 0xFFFFFFFF)
        self.uc.reg_write(UC_X86_REG_ESP, sp+4+4*count)
        self.uc.reg_write(UC_X86_REG_EIP, ret)

    def _sprite_allocation(self, sp):
        args = [self.read(sp+4+i*4) for i in range(4)]
        line = struct.unpack_from('<h', self.image, 0x5FF6D8-BASE)[0]+3
        if self.read(sp) != 0x428A73 or args != [32, 1, 0x594E28, line] or self.sprite_allocations:
            raise RuntimeError('cache exact original32-byte CRT boundary')
        self.uc.mem_write(SPRITE, b'\xcd'*32)
        self.sprite_allocations.append(dict(va='0x56e810', return_va='0x428a73', sp=sp, args=args,
                                            pointer=SPRITE, bytes=32, initial_hex='cd'*32,
                                            adapter='declared debug CRT allocation'))
        self.uc.reg_write(UC_X86_REG_EAX, SPRITE)
        self.uc.reg_write(UC_X86_REG_ESP, sp+4)
        self.uc.reg_write(UC_X86_REG_EIP, self.read(sp))

    def _code(self, uc, at, size, user):
        if not self.cache_running:
            return super()._code(uc, at, size, user)
        sp = uc.reg_read(UC_X86_REG_ESP)
        if at == self.cache_stop:
            self.boundary = at
            uc.emu_stop()
            return
        ret = self.read(sp)
        if at == 0x56E810:
            return self._sprite_allocation(sp)
        if at in self.cache_imports:
            return self._gdi(at, sp, ret)
        if ret in DEVICE:
            return self._cache_device(at, sp, ret)
        if not any(a <= at and at+size <= b for a, b in RANGES.items()):
            raise RuntimeError('cache undeclared native body '+hex(at))
        self.visited.add(at)
        if at in RANGES and at != 0x56CE80:
            self.entries.append(dict(va=hex(at), return_va=hex(ret), sp=sp,
                                     receiver=uc.reg_read(REGISTERS['ECX']),
                                     args=[self.read(sp+4+i*4) for i in range(ARGS.get(at, 0))]))
        if at in self.cache_rets:
            self.returns.append(dict(va=hex(at), return_va=hex(ret), sp=sp, eax=uc.reg_read(UC_X86_REG_EAX)))

    def resume_cache(self, phase):
        start = 0x52AE80 if phase == 'sprite' else self.read(0x592094)
        if self.uc.reg_read(UC_X86_REG_EIP) != start:
            raise RuntimeError('cache same pending original CPU required')
        before_cpu = {k: self.uc.reg_read(r) for k, r in REGISTERS.items()}
        if phase == 'sprite':
            self.uc.mem_map(SPRITE-4096, 12288)
            self.uc.mem_write(SPRITE-4096, b'\xa5'*12288)
            self.cache_imports = {self.read(slot): (slot, rule) for slot, rule in IMPORTS.items()}
            for target in self.cache_imports:
                self._foreign_write(target, b'\xc3')
            self.sprite_allocations = []
        self.cache_stop = self.read(0x592094) if phase == 'sprite' else 0x416021
        self.entries, self.returns, self.device_calls, self.gdi_calls, self.visited, self.boundary = [], [], [], [], set(), None
        md = Cs(CS_ARCH_X86, CS_MODE_32)
        self.cache_rets = {i.address for a, b in RANGES.items() for i in md.disasm(self.image[a-BASE:b-BASE], a) if i.mnemonic == 'ret'}
        if phase == 'font':
            self.sprite_device_calls = self.saved_sprite_calls
        self.cache_running = True
        try:
            self.uc.emu_start(start, RETURN+1, timeout=15_000_000, count=100000)
        finally:
            self.cache_running = False
        if phase == 'sprite':
            self.saved_sprite_calls = list(self.device_calls)
            self.sprite_device_calls = self.saved_sprite_calls
        image = bytearray(self.constructed_image)
        store(image, COUNTER-BASE, dword(image, COUNTER-BASE)+288)
        store(image, HEAD-BASE, CACHE)
        owner = bytearray(self.device_owner)
        store(owner, 0xB26C, self.font_handle)
        if phase == 'font':
            store(owner, 0xB270, FONT)
        state = self.check(bytes(owner), bytes(image), TOP-108)
        caps = bytes.fromhex(self.sprite_device_calls[1]['result']['hex'])
        creation = bytes.fromhex(self.sprite_device_calls[2]['result']['hex'])
        base_cache = texture_cache(cache_prefix(b'\xcd'*176, self.objects['device']['pointer'], caps),
                                   self.objects['texture']['pointer'], self.objects['texture_surface']['pointer'])
        cache_value = cache_before_gdi(base_cache) if phase == 'sprite' else cache_after_gdi(
            base_cache, self.cache_dc, self.cache_bitmap, self.old_bitmap, self.cache_bits)
        logfont = bytes.fromhex(self.source_logfont)
        values = [font_constructor(b'\xcd'*80) if phase == 'sprite' else font_complete(
            self.objects['device']['pointer'], self.indirect_font, logfont), cache_value,
            sprite(b'\xcd'*32, self.objects['device']['pointer'], caps, creation)]
        heaps = []
        for ptr, value in zip((FONT, CACHE, SPRITE), values):
            expected = bytearray(b'\xa5'*12288)
            expected[4096:4096+len(value)] = value
            actual = bytes(self.uc.mem_read(ptr-4096, 12288))
            if actual != expected:
                raise RuntimeError('cache complete object/padding/guard mismatch '+hex(ptr))
            heaps.append(dict(pointer=ptr-4096, **buffer_evidence(actual)))
        cpu = {k: self.uc.reg_read(r) for k, r in REGISTERS.items()}
        pending = dict(va=hex(self.boundary or 0), sp=cpu['ESP'], first_instruction_executed=False)
        if phase == 'sprite':
            pending.update(return_va=hex(self.read(cpu['ESP'])), args=[self.read(cpu['ESP']+4)], platform_call_executed=False)
        return dict(phase=phase, before_cpu=before_cpu, entries=self.entries, returns=self.returns,
                    allocations=list(self.sprite_allocations) if phase == 'sprite' else [],
                    device_calls=self.device_calls, gdi_calls=self.gdi_calls, visited=sorted(self.visited),
                    state=state, heaps=heaps, cpu=cpu, pending=pending,
                    output_slot=dict(pointer=TOP-228, value=self.read(TOP-228)),
                    first_static_font_completed=phase == 'font', full415F50_returned=False,
                    state_blocks_created=False, DIB_bits_target_read=False, retained_VM_advanced=False)


def generate(phase):
    cases = []
    for fill, width, height in ((0xA5, 640, 480), (0xCC, 1024, 768)):
        def run(bridge):
            with CachePlatform() as platform:
                engine = CacheEmulator(bridge, platform, fill)
                case = dict(fill=fill, hello=bridge.hello, platform_hello=platform.hello,
                            constructor=engine.construct(), device=engine.device(), font=engine.font(),
                            factory=engine.factory('empty'))
                engine.source_logfont = case['font']['LOGFONT']
                case['requirements'] = engine.resume('requirements')
                case['texture'] = engine.resume('texture')
                case['sprite'] = engine.resume_cache('sprite')
                if phase == 'font':
                    case['font_return'] = engine.resume_cache('font')
            case.update(platform_trace=platform.trace, platform_cleanup=platform.cleanup)
            return case
        result = owned_run(run, width, height)
        case = result['value']
        case.update(device_trace=result['trace'], device_cleanup=result['cleanup'], refused_address_collisions=result['refused_address_collisions'])
        cases.append(case)
        print(hex(fill)+': original sprite/cache '+phase+' verified', flush=True)
    build = json.loads((ROOT/'analysis/school-font-cache-platform-v1-20261018.json').read_text())['builds']
    return dict(schema_version=1, phase=phase, source_contract=source_contract(), cases=cases,
                device_build=build['device'], platform_build=build['gdi'],
                explicit_empty_cache_experiment=True, CRT_adapter_executed=True,
                original_IAT_changed=False, game_helpers_stubbed=False, retained_VM_advanced=False,
                drawing_or_Present=False, full_outer_frame=False, live_handles_resumable_after_cleanup=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--phase', choices=('sprite', 'font'), required=True)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    path = ROOT/a.out
    if path.exists():
        p.error('fresh immutable report required')
    path.write_text(json.dumps(generate(a.phase), indent=2)+'\n', encoding='utf-8', newline='\n')

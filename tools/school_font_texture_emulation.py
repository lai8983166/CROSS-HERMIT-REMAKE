"""Resume the original empty-cache CPU through texture requirements and real resources."""
import argparse
import json
import struct
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_font_startup_emulation import FontEmulator, OWNER, STACK, TOP, RETURN
from tools.school_owner_platform import OwnerPlatform
from tools.school_font_texture_bridge import owned_run
from tools.school_font_texture import *
from tools.school_renderer_init_emulation import REGISTERS, buffer_evidence

EXTERNAL = {0x526D76: ('texture_factory', 'device', 24, 2),
            0x526D83: ('texture_caps', 'device', 28, 2),
            0x526D8D: ('texture_mode', 'device', 32, 2),
            0x526DCF: ('texture_format', 'factory', 40, 7),
            0x526E1C: ('texture_factory_release', 'factory', 8, 1),
            0x52736D: ('texture_caps', 'device', 28, 2),
            0x527631: ('texture_create', 'device', 80, 8),
            0x5486EC: ('texture_surface', 'texture', 60, 3)}
NATIVE = {**RANGES, 0x54864C: 0x548706, 0x548735: 0x548876}


class TextureEmulator(FontEmulator):
    def __init__(self, bridge, platform, fill):
        self.texture_running = False
        super().__init__(bridge, platform, fill)

    def _map_page(self, address):
        if any(ptr-4096 <= address < ptr+8192 for ptr in (FONT, CACHE)):
            raise RuntimeError('live interface mapping collides with audit ownership')
        return super()._map_page(address)

    def _write(self, uc, access, at, size, value, user):
        if not self.texture_running:
            return super()._write(uc, access, at, size, value, user)
        if not any(a <= at and at+size <= b for a, b in ((STACK, STACK+65536), (CACHE, CACHE+176))):
            raise RuntimeError('texture native unowned write '+hex(at))

    def _put(self, at, raw):
        if self.texture_running and CACHE <= at and at+len(raw) <= CACHE+176:
            self.uc.mem_write(at, raw)
            return
        return super()._put(at, raw)

    def _api(self, at, sp, ret):
        if at == DEBUG_TARGET:
            if ret != 0x52B098:
                raise RuntimeError('texture original inherited debug caller')
            args = [self.read(sp+4)]
            request = dict(value=args[0])
            result = self.bridge.request('debug_mute', **request)
            self.api_calls.append(dict(op='debug_mute', va=hex(at), return_va=hex(ret), sp=sp,
                                       args=args, request=request, result=result, live_host_observed=True))
            # Original external debug function has no defined return value; cdecl leaves its argument.
            self.uc.reg_write(UC_X86_REG_ESP, sp+4)
            self.uc.reg_write(UC_X86_REG_EIP, ret)
            return
        op, kind, slot, count = EXTERNAL[ret]
        obj = self.objects[kind]
        args = [self.read(sp+4+i*4) for i in range(count)]
        if at != obj['methods'][str(slot)] or args[0] != obj['pointer']:
            raise RuntimeError('texture actual owned interface caller')
        request = dict(pointer=args[0])
        if op in ('texture_factory', 'texture_caps', 'texture_mode'):
            size = 4 if op == 'texture_factory' else 212 if op == 'texture_caps' else 16
            if not STACK <= args[1] <= TOP-size:
                raise RuntimeError('texture original query output')
            result = self.bridge.request(op, **request)
            if op == 'texture_factory':
                if result['factory']['pointer'] != self.objects['factory']['pointer']:
                    raise RuntimeError('texture factory identity changed')
                self._identity('factory', result['factory'])
                self._put(args[1], struct.pack('<I', result['factory']['pointer']))
            else:
                self._put(args[1], bytes.fromhex(result['hex']))
        elif op == 'texture_format':
            request.update(dict(zip(('adapter', 'type', 'adapter_format', 'usage', 'resource_type', 'format'), args[1:])))
            result = self.bridge.request(op, **request)
        elif op == 'texture_factory_release':
            result = self.bridge.request(op, **request)
        elif op == 'texture_create':
            if args[1:] != [64, 16, 1, 512, 21, 0, CACHE+16]:
                raise RuntimeError('texture exact native creation arguments')
            request.update(dict(zip(('width', 'height', 'levels', 'usage', 'format', 'pool'), args[1:7])))
            result = self.bridge.request(op, **request)
            self._identity('texture', result['texture'])
            self._put(args[-1], struct.pack('<I', result['texture']['pointer']))
        else:
            if args[1:] != [0, CACHE+48]:
                raise RuntimeError('texture exact original level0 output')
            request.update(level=0)
            result = self.bridge.request(op, **request)
            self._identity('texture_surface', result['surface'])
            self._put(args[-1], struct.pack('<I', result['surface']['pointer']))
        eax = result['count'] if op == 'texture_factory_release' else result['hr']
        self.api_calls.append(dict(op=op, va=hex(at), return_va=hex(ret), sp=sp,
                                   args=args, request=request, result=result, live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX, eax & 0xFFFFFFFF)
        self.uc.reg_write(UC_X86_REG_ESP, sp+4+4*count)
        self.uc.reg_write(UC_X86_REG_EIP, ret)

    def _code(self, uc, at, size, user):
        if not self.texture_running:
            return super()._code(uc, at, size, user)
        sp = uc.reg_read(UC_X86_REG_ESP)
        if at == self.texture_stop:
            self.boundary = at
            uc.emu_stop()
            return
        ret = self.read(sp)
        if at == DEBUG_TARGET or ret in EXTERNAL:
            return self._api(at, sp, ret)
        if not any(a <= at and at+size <= b for a, b in NATIVE.items()):
            raise RuntimeError('texture undeclared native body '+hex(at))
        self.visited.add(at)
        if at in NATIVE:
            self.entries.append(dict(va=hex(at), return_va=hex(ret), sp=sp,
                                     receiver=uc.reg_read(REGISTERS['ECX']),
                                     edx=uc.reg_read(REGISTERS['EDX']),
                                     args=[self.read(sp+4+i*4) for i in range(ARGS.get(at, 0))]))
        if at in self.texture_rets:
            self.returns.append(dict(va=hex(at), return_va=hex(ret), sp=sp, eax=uc.reg_read(UC_X86_REG_EAX)))

    def resume(self, phase):
        start = 0x52755E if phase == 'requirements' else 0x5275D7
        if self.uc.reg_read(UC_X86_REG_EIP) != start:
            raise RuntimeError('texture original pending CPU required')
        before_cpu = {k: self.uc.reg_read(r) for k, r in REGISTERS.items()}
        self._foreign_write(DEBUG_TARGET, b'\xc3')
        self.texture_stop = STOPS[phase]
        self.entries, self.returns, self.api_calls, self.visited, self.boundary = [], [], [], set(), None
        md = Cs(CS_ARCH_X86, CS_MODE_32)
        self.texture_rets = {i.address for a, b in NATIVE.items() for i in md.disasm(self.image[a-BASE:b-BASE], a) if i.mnemonic == 'ret'}
        owner = bytes(self.uc.mem_read(OWNER, 0xC000))
        image = bytes(self.uc.mem_read(BASE, len(self.image)))
        self.texture_running = True
        try:
            self.uc.emu_start(start, RETURN+1, timeout=15_000_000, count=100000)
        finally:
            self.texture_running = False
        state = self.check(owner, image, TOP-108)
        caps = bytes.fromhex(self.cache_calls[1]['result']['hex'])
        projected = requirements(64, 16, 1, caps)
        if projected != dict(width=64, height=16, levels=1, format=21):
            raise RuntimeError('texture native case outside declared projection')
        heaps = []
        for ptr, size in ((FONT, 80), (CACHE, 176)):
            from tools.school_font_startup import font_constructor, cache_prefix
            expected = bytearray(b'\xa5'*12288)
            value = font_constructor(b'\xcd'*80) if ptr == FONT else cache_prefix(b'\xcd'*176, self.objects['device']['pointer'], caps)
            if ptr == CACHE and phase == 'texture':
                value = texture_cache(value, self.objects['texture']['pointer'], self.objects['texture_surface']['pointer'])
            expected[4096:4096+size] = value
            actual = bytes(self.uc.mem_read(ptr-4096, 12288))
            if actual != expected:
                raise RuntimeError('texture full cache/font/guards source mismatch '+hex(ptr))
            heaps.append(dict(pointer=ptr-4096, **buffer_evidence(actual)))
        cpu = {k: self.uc.reg_read(r) for k, r in REGISTERS.items()}
        count = 8 if phase == 'requirements' else 2
        pending = dict(va=hex(self.boundary or 0), return_va=hex(self.read(cpu['ESP'])), sp=cpu['ESP'],
                       args=[self.read(cpu['ESP']+4+i*4) for i in range(count)], first_instruction_executed=False)
        return dict(phase=phase, before_cpu=before_cpu, entries=self.entries, returns=self.returns,
                    api_calls=self.api_calls, visited=sorted(self.visited), cpu=cpu, state=state, heaps=heaps,
                    pending=pending, output_slot=dict(pointer=TOP-228, value=self.read(TOP-228)),
                    font_initialization_complete=False, sprite_body_executed=False, retained_VM_advanced=False)


def generate(phase):
    cases = []
    for fill, width, height in ((0xA5, 640, 480), (0xCC, 1024, 768)):
        def run(bridge):
            with OwnerPlatform() as platform:
                engine = TextureEmulator(bridge, platform, fill)
                case = dict(fill=fill, hello=bridge.hello, platform_hello=platform.hello,
                            constructor=engine.construct(), device=engine.device(), font=engine.font(),
                            factory=engine.factory('empty'))
                case['requirements'] = engine.resume('requirements')
                if phase == 'texture':
                    case['texture'] = engine.resume('texture')
            case.update(platform_trace=platform.trace, platform_cleanup=platform.cleanup)
            return case
        result = owned_run(run, width, height)
        case = result['value']
        case.update(device_trace=result['trace'], device_cleanup=result['cleanup'],
                    refused_address_collisions=result['refused_address_collisions'])
        cases.append(case)
        print(hex(fill)+': original cache '+phase+' verified', flush=True)
    return dict(schema_version=1, phase=phase, source_contract=source_contract(), cases=cases,
                device_build=json.loads((ROOT/'analysis/school-font-texture-bridge-v1-20261018.json').read_text())['build'],
                platform_build=json.loads((ROOT/'analysis/school-owner-startup-platform-v2-20261017.json').read_text())['build'],
                explicit_empty_cache_experiment=True, original_IAT_changed=False, game_helpers_stubbed=False,
                CRT_adapter_executed=True, retained_VM_advanced=False, drawing_or_Present=False,
                full_outer_frame=False, live_handles_resumable_after_cleanup=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--phase', choices=tuple(STOPS), required=True)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    path = ROOT/a.out
    if path.exists():
        p.error('fresh immutable report required')
    path.write_text(json.dumps(generate(a.phase), indent=2)+'\n', encoding='utf-8', newline='\n')

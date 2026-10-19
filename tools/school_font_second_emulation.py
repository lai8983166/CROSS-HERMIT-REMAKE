"""Continue the live original first-font return through second-slot prerequisites."""
import argparse
import json
import struct
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_font_state_emulation import StateEmulator, StateGDI, prefix, unpack_large
from tools.school_font_state_device import owned_run
from tools.school_font_slots_emulation import OWNER, STACK, TOP, RETURN, ARGS
from tools.school_font_slots import SLOT
from tools.school_font_cache import FONT, CACHE, SPRITE, COUNTER, HEAD, dword, store
from tools.school_font_second import *
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_emulation import REGISTERS, buffer_evidence


class SecondEmulator(StateEmulator):
    def __init__(self, bridge, platform, fill):
        self.second_running = False
        super().__init__(bridge, platform, fill)

    def _map_page(self, address):
        if SECOND-4096 <= address < SECOND+8192:
            raise RuntimeError('live interface mapping collides with audit ownership')
        return super()._map_page(address)

    def _shadow(self, name, pointer, data):
        start = (pointer & ~4095)-4096
        end = ((pointer+len(data)+4095) & ~4095)+4096
        if start < SECOND+8192 and SECOND-4096 < end:
            raise RuntimeError('live interface mapping collides with audit ownership')
        return super()._shadow(name, pointer, data)

    def _write(self, uc, access, at, size, value, user):
        if not self.second_running:
            return super()._write(uc, access, at, size, value, user)
        allowed = [(STACK, STACK+65536)]
        if self.second_phase != 'loop':
            allowed.append((SECOND, SECOND+SIZE))
        if self.second_phase == 'constructor':
            allowed += [(COUNTER, COUNTER+4), (OWNER+0x1094, OWNER+0x1098)]
        if not any(a <= at and at+size <= b for a,b in allowed):
            raise RuntimeError('second font unowned native write '+hex(at))

    def _slot_read(self, uc, access, at, size, value, user):
        if not self.second_running:
            return super()._slot_read(uc, access, at, size, value, user)
        allowed = [(BASE, BASE+len(self.image)), (OWNER, OWNER+0xC000), (STACK, STACK+65536)]
        allowed += [(p,p+n) for p,n in ((FONT,80),(CACHE,176),(SPRITE,32),(SLOT,SIZE))]
        if self.second_phase != 'loop':
            allowed.append((SECOND, SECOND+SIZE))
        allowed += [(p,p+4096) for p in self.foreign]
        if not any(a <= at and at+size <= b for a,b in allowed):
            raise RuntimeError('second font unowned native read '+hex(at))

    def _allocate_second(self, sp):
        args = [self.read(sp+4+i*4) for i in range(4)]
        line = struct.unpack_from('<h', self.image, 0x5FF6D8-BASE)[0]+3
        if (self.second_phase != 'constructor' or self.read(sp) != 0x428A73
                or args != [SIZE,1,0x594E28,line] or self.second_allocations):
            raise RuntimeError('second font exact original CRT allocation')
        self.uc.mem_write(SECOND, b'\xcd'*SIZE)
        self.second_allocations.append(dict(va='0x56e810', return_va='0x428a73', sp=sp,
            args=args, pointer=SECOND, bytes=SIZE, initial_hex='cd'*SIZE,
            adapter='declared debug CRT allocation'))
        self.uc.reg_write(UC_X86_REG_EAX, SECOND)
        self.uc.reg_write(UC_X86_REG_ESP, sp+4)
        self.uc.reg_write(UC_X86_REG_EIP, self.read(sp))

    def _code(self, uc, at, size, user):
        if not self.second_running:
            return super()._code(uc, at, size, user)
        if at == self.second_stop:
            self.boundary = at
            uc.emu_stop()
            return
        sp = uc.reg_read(UC_X86_REG_ESP)
        ret = self.read(sp)
        if at == 0x56E810:
            return self._allocate_second(sp)
        if (self.second_phase == 'atlas' and ret == 0x401173
                and at == self.objects['device']['methods']['28']):
            return self._slot_caps(at, sp, ret)
        if not any(a <= at and at+size <= b for a,b in RANGES.items()):
            raise RuntimeError('second font undeclared original body '+hex(at))
        self.visited.add(at)
        self.instruction_trace.append(at)
        if at in ARGS:
            self.entries.append(dict(va=hex(at), return_va=hex(ret), sp=sp,
                receiver=uc.reg_read(REGISTERS['ECX']),
                args=[self.read(sp+4+i*4) for i in range(ARGS[at])]))
        if at in self.second_rets:
            self.returns.append(dict(va=hex(at), return_va=hex(ret), sp=sp,
                eax=uc.reg_read(UC_X86_REG_EAX)))

    def resume_second(self, phase, previous):
        start, stop = PHASES[phase]
        if self.uc.reg_read(UC_X86_REG_EIP) != start:
            raise RuntimeError('second font same pending original CPU required')
        before_cpu = {k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        if phase == 'constructor':
            self.uc.mem_map(SECOND-4096,12288)
            self.uc.mem_write(SECOND-4096,b'\xa5'*12288)
        self.entries,self.returns,self.slot_calls,self.second_allocations = [],[],[],[]
        self.visited,self.instruction_trace,self.boundary = set(),[],None
        md = Cs(CS_ARCH_X86,CS_MODE_32)
        self.second_rets = {i.address for a,b in RANGES.items()
            for i in md.disasm(self.image[a-BASE:b-BASE],a) if i.mnemonic=='ret'}
        self.second_phase,self.second_stop,self.second_running = phase,stop,True
        try:
            self.uc.emu_start(start,RETURN+1,timeout=15_000_000,count=100000)
        finally:
            self.second_running = False
        if self.boundary != stop:
            raise RuntimeError('second font original boundary not reached')
        owner = bytearray(self.device_owner)
        for at,value in ((0xB26C,self.font_handle),(0xB270,FONT),(0x1090,SLOT)):
            store(owner,at,value)
        if phase != 'loop':
            store(owner,0x1094,SECOND)
        image = bytearray(self.constructed_image)
        store(image,HEAD-BASE,CACHE)
        store(image,COUNTER-BASE,dword(image,COUNTER-BASE)+288+SIZE*(1 if phase=='loop' else 2))
        state = self.check(bytes(owner),bytes(image),TOP-108)
        retained_heaps = previous.get('retained_heaps',previous['heaps']+[previous['slot_heap']])
        for row in retained_heaps:
            if bytes(self.uc.mem_read(row['pointer'],12288)) != unpack(row):
                raise RuntimeError('second font changed prior complete heap '+hex(row['pointer']))
        for row in previous['external_regions']:
            if bytes(self.uc.mem_read(row['base'],row['bytes'])) != unpack_large(row['buffer']):
                raise RuntimeError('second font changed prior pixel snapshot')
        second_heap = None
        if phase != 'loop':
            value = constructor(b'\xcd'*SIZE)
            if phase == 'atlas':
                maximum = dword(bytes.fromhex(self.slot_calls[0]['result']['hex']),88)
                value = atlas(value,self.objects['device']['pointer'],maximum)
            expected = bytearray(b'\xa5'*12288)
            expected[4096:4096+SIZE] = value
            actual = bytes(self.uc.mem_read(SECOND-4096,12288))
            if actual != expected:
                raise RuntimeError('second font full object/guard mismatch')
            second_heap = dict(pointer=SECOND-4096,**buffer_evidence(actual))
        cpu = {k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        pending = dict(va=hex(stop),sp=cpu['ESP'],first_instruction_executed=False)
        if phase == 'constructor':
            pending.update(return_va=hex(self.read(cpu['ESP'])),receiver=SECOND,args=[self.read(cpu['ESP']+4)])
        if phase == 'atlas':
            pending.update(method_target=self.read(cpu['EDX']+80),
                args=[self.read(cpu['ESP']+i*4) for i in range(8)],platform_call_executed=False)
        return dict(phase=phase,before_cpu=before_cpu,entries=self.entries,returns=self.returns,
            allocations=self.second_allocations,api_calls=self.slot_calls,visited=sorted(self.visited),
            instruction_trace=self.instruction_trace,state=state,heaps=previous['heaps'],
            slot_heap=previous['slot_heap'],retained_heaps=retained_heaps,second_heap=second_heap,
            external_regions=previous['external_regions'],external_regions_are_retained_snapshots=True,
            cpu=cpu,pending=pending,loop_locals=dict(index=self.read(TOP-120),status=self.read(TOP-116),
                owner=self.read(TOP-112)),first_additional_font_completed=True,
            second_additional_font_constructed=phase!='loop',second_atlas_caps_queried=phase=='atlas',
            second_atlas_texture_created=False,second_additional_font_completed=False,
            full415F50_returned=False,GPU_drawing_or_Present=False,retained_VM_advanced=False)


def generate(phase):
    cases = []
    for fill,width,height in ((0xA5,640,480),(0xCC,1024,768)):
        def run(bridge):
            with StateGDI() as platform:
                e = SecondEmulator(bridge,platform,fill)
                c = prefix(e,bridge,platform,fill)
                c['glyph_raster'] = e.resume_glyphs(c['GDI_preparation'])
                c['pixel_upload'] = e.resume_pixels(c['glyph_raster'])
                c['font_cleanup'] = e.resume_state('cleanup',c['pixel_upload'])
                c['font_vertex'] = e.resume_state('vertex',c['font_cleanup'])
                c['font_states'] = e.resume_state('states',c['font_vertex'])
                c['second_loop'] = e.resume_second('loop',c['font_states'])
                if phase != 'loop':
                    c['second_constructor'] = e.resume_second('constructor',c['second_loop'])
                if phase == 'atlas':
                    c['second_atlas'] = e.resume_second('atlas',c['second_constructor'])
            c.update(platform_trace=platform.trace,platform_cleanup=platform.cleanup)
            return c
        result = owned_run(run,width,height)
        c = result['value']
        c.update(device_trace=result['trace'],device_cleanup=result['cleanup'],
                 refused_address_collisions=result['refused_address_collisions'])
        cases.append(c)
        print(hex(fill)+': original second font '+phase+' verified',flush=True)
    return dict(schema_version=1,phase=phase,source_contract=source_contract(),cases=cases,
        device_build=json.loads((ROOT/'analysis/school-font-state-device-v1-20261019.json').read_text())['build'],
        platform_build=json.loads((ROOT/'analysis/school-font-state-gdi-v5-20261019.json').read_text())['build'],
        explicit_empty_cache_experiment=True,CRT_adapter_executed=True,original_IAT_changed=False,
        game_helpers_stubbed=False,retained_VM_advanced=False,GPU_drawing_or_Present=False,
        full_outer_frame=False,live_handles_resumable_after_cleanup=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--phase',choices=tuple(PHASES),required=True)
    p.add_argument('--out',required=True)
    a = p.parse_args()
    path = ROOT/a.out
    if path.exists():
        p.error('fresh immutable second font execution required')
    path.write_text(json.dumps(generate(a.phase),indent=2)+'\n',encoding='utf8',newline='\n')

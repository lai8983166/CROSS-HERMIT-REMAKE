import copy
import struct
import unittest
from types import SimpleNamespace

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn import x86_const as x86
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP, UC_X86_REG_EFLAGS
from tools import terminal_unit_frontends_trace as t


class Mini:
    def __init__(self, api=False):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_32)
        self.uc.mem_map(0x401000, 0x5000)
        code = (bytes.fromhex('e8fb0f0000a3') + struct.pack('<I',0x403000) + bytes.fromhex('c3')) if api else (bytes.fromhex('c705') + struct.pack('<II',0x403000,1) + bytes.fromhex('a1') + struct.pack('<I',0x403000) + bytes.fromhex('83c005c3'))
        self.uc.mem_write(0x401000, code)
        self.uc.mem_write(0x404F00, struct.pack('<I', 0x404000))
        self.uc.reg_write(UC_X86_REG_ESP, 0x404F00)
        self.recorder = None
        self.api = api
        self.mutable = [(0x403000, 0x404000), (0x404000, 0x406000)]
        self.uc.hook_add(UC_HOOK_CODE, self.code)
        self.uc.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def cpu(self):
        values = {name:self.uc.reg_read(getattr(x86,'UC_X86_REG_'+name)) for name in t.CPU_REGISTERS}
        return {k:list(v) if type(v) is tuple else v for k,v in values.items()}

    def snapshot(self):
        return [dict(pointer=a, bytes=b-a+1, hex=bytes(self.uc.mem_read(a,b-a+1)).hex())
                for a,b,p in self.uc.mem_regions()]

    def code(self, uc, pc, size, context):
        r = self.recorder
        if r is not None and not r.begin_code(pc):
            return
        try:
            if pc == 0x401000 and hasattr(self,'gpu'):
                self.gpu.request('observe',hex=bytes(uc.mem_read(0x403000,4)).hex())
            if self.api and pc == 0x402000:
                sp = uc.reg_read(UC_X86_REG_ESP)
                ret = struct.unpack('<I', uc.mem_read(sp, 4))[0]
                uc.mem_write(0x405000, b'actual platform output')
                uc.reg_write(UC_X86_REG_EAX, 123)
                uc.reg_write(UC_X86_REG_ESP, sp + 4)
                uc.reg_write(UC_X86_REG_EIP, ret)
        finally:
            if r is not None:
                r.end_code(pc)

    def write(self, uc, access, address, size, value, context):
        if self.recorder is not None:
            self.recorder.guest_write(uc.reg_read(UC_X86_REG_EIP), address, size, value)


class TransactionTraceTests(unittest.TestCase):
    def test_read_only_native_observer_has_exact_original_boundary(self):
        m=Mini()
        wires=[]
        def observe(op,**args):
            wires.append(dict(op=op,**args))
        m.gpu=SimpleNamespace(request=observe)
        m.boundary_wire_counts=lambda:dict(GPU=len(wires))
        recorder=t.Recorder(m);m.recorder=recorder
        try:
            m.uc.emu_start(0x401000,0x404000)
            report=recorder.finish()
        finally:
            recorder.detach()
        event=report['transactions'][0]['events'][0]
        self.assertEqual(event['pc'],0x401000)
        self.assertEqual(event['effects'],[])
        self.assertTrue(event['continues_guest'])
        self.assertEqual(event['wire'],dict(GPU=[0,1]))
        self.assertEqual(wires,[dict(op='observe',hex='00000000')])
        self.assertEqual(m.uc.mem_read(0x403000,4),bytes.fromhex('01000000'))
        fixture=Mini()
        code=bytearray(0x7000)
        first=fixture.snapshot()[0]
        code[first['pointer']-0x400000:first['pointer']-0x400000+first['bytes']]=bytes.fromhex(first['hex'])
        def initial(data,original,ranges):
            if data['initial_memory']!=fixture.snapshot():raise ValueError('initial fixture')
        def driver(replay,actions,row,history):
            if actions:raise ValueError('no driver')
        def boundary(replay,item):
            expected=dict(op='observe',hex=replay.read(0x403000,4).hex())
            if item!=event or wires[0]!=expected:raise ValueError('actual observer boundary bytes')
        result=t.Replay(report,bytes(code),[(0x401000,0x401100)],initial,driver,boundary).run()
        self.assertEqual(result['final_trace'],report['final_trace'])
        wires[0]['hex']='01000000'
        with self.assertRaises(ValueError):
            t.Replay(report,bytes(code),[(0x401000,0x401100)],initial,driver,boundary).run()
        self.assertIs(m.gpu.request,observe)

    def make_replay(self, report, api=False):
        fixture = Mini(api=api)
        def initial(data, code, ranges):
            if (data['initial_memory'], data['initial_CPU'], data['initial_regions']) != (
                    fixture.snapshot(), fixture.cpu(), [list(x) for x in fixture.uc.mem_regions()]):
                raise ValueError('independent source input fixture mismatch')
        def driver(replay, actions, row, history):
            if actions:
                raise ValueError('no driver state mutation in this fixture')

        def event(replay, item):
            sp = replay.cpu()['ESP']
            ret = struct.unpack('<I', replay.read(sp, 4))[0]
            expected = [dict(kind='mem_write',address=0x405000,hex=b'actual platform output'.hex()),
                        dict(kind='reg_write',register=UC_X86_REG_EAX,value=123),
                        dict(kind='reg_write',register=UC_X86_REG_ESP,value=sp+4),
                        dict(kind='reg_write',register=UC_X86_REG_EIP,value=ret)]
            if item['pc'] != 0x402000 or item['effects'] != expected:
                raise ValueError('independent platform contract mismatch')

        code = bytearray(0x7000)
        first = fixture.snapshot()[0]
        code[first['pointer']-0x400000:first['pointer']-0x400000+first['bytes']] = bytes.fromhex(first['hex'])
        return t.Replay(report, bytes(code), [(0x401000,0x401100)], initial, driver, event)

    def test_independent_machine_replays_original_code_and_validated_platform(self):
        for api in (False, True):
            m = Mini(api=api)
            r = t.Recorder(m)
            m.recorder = r
            try:
                m.uc.emu_start(0x401000, 0x404000)
                report = r.finish()
            finally:
                r.detach()
            replay = self.make_replay(report, api)
            proof = replay.run()
            self.assertTrue(proof['all_cumulative_original_digests_reproduced'])
            self.assertEqual(proof['final_trace'], report['final_trace'])
            for kind in ('memory', 'trace', 'platform', 'driver'):
                bad = copy.deepcopy(report)
                if kind == 'memory':
                    bad['transactions'][0]['after_memory']['sha256'] = '0'*64
                elif kind == 'trace':
                    bad['transactions'][0]['after_trace']['writes'] += 1
                elif kind == 'platform':
                    if not api:
                        continue
                    bad['transactions'][0]['events'][0]['effects'][1]['value'] = 122
                else:
                    bad['final_driver'] = [dict(kind='mem_write',address=0x403000,hex='00')]
                with self.subTest(api=api, mutation=kind), self.assertRaises(ValueError):
                    self.make_replay(bad, api).run()

    def test_original_cpu_writes_and_whole_memory_digest(self):
        m = Mini()
        r = t.Recorder(m)
        m.recorder = r
        try:
            m.uc.emu_start(0x401000, 0x404000, timeout=1, count=1)
            report = r.finish()
            self.assertEqual(m.cpu()['EAX'], 6)
            self.assertEqual(report['final_trace']['instructions'], 4)
            self.assertEqual(report['final_trace']['writes'], 1)
            self.assertEqual(report['final_memory_digest'], t.MemoryDigest(m.uc).capture())
            self.assertEqual(report['transactions'][0]['engine_count'], 0)
            self.assertFalse(report['accepted'])
        finally:
            r.detach()

    def test_platform_effects_are_separate_from_guest_execution(self):
        m = Mini(api=True)
        r = t.Recorder(m)
        m.recorder = r
        try:
            m.uc.emu_start(0x401000, 0x404000)
            report = r.finish()
            event = report['transactions'][0]['events'][0]
            self.assertEqual(event['pc'], 0x402000)
            self.assertFalse(event['continues_guest'])
            self.assertEqual(event['before_CPU']['EIP'], 0x402000)
            self.assertEqual(event['CPU_changes']['EAX'], 123)
            self.assertEqual(report['final_trace']['instructions'], 3)
            self.assertEqual(report['final_trace']['writes'], 2)  # CALL stack and MOV
            self.assertEqual(report['final_memory_digest'], t.MemoryDigest(m.uc).capture())
        finally:
            r.detach()

    def test_dirty_cache_tracks_host_changes_unmap_and_permissions(self):
        m = Mini()
        r = t.Recorder(m)
        m.recorder = r
        try:
            before = r.memory.capture()
            m.uc.mem_write(0x403000, b'x')
            m.uc.mem_protect(0x402000, 0x1000, 1)
            after = r.memory.capture()
            self.assertNotEqual(before, after)
            self.assertEqual(after, t.MemoryDigest(m.uc).capture())
            m.uc.mem_unmap(0x405000, 0x1000)
            self.assertEqual(r.memory.capture(), t.MemoryDigest(m.uc).capture())
            self.assertEqual([x['kind'] for x in r.driver], ['mem_write', 'mem_protect', 'mem_unmap'])
            m.uc.mem_map(0x405000, 0x1000)
            m.uc.mem_write(0x405000, b'old bytes')
            r.memory.capture()
            m.uc.mem_unmap(0x405000, 0x1000)
            m.uc.mem_map(0x405000, 0x1000)
            self.assertEqual(r.memory.capture(), t.MemoryDigest(m.uc).capture())
        finally:
            r.detach()

    def test_missing_architectural_register_is_rejected(self):
        m = Mini()
        r = t.Recorder(m)
        m.recorder = r
        try:
            m.uc.emu_start(0x401000, 0x404000)
            report = r.finish()
        finally:
            r.detach()
        report['initial_CPU'].pop('XMM7')
        with self.assertRaisesRegex(ValueError, 'complete57'):
            self.make_replay(report)


if __name__ == '__main__':
    unittest.main()

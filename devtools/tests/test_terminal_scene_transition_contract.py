import gzip
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from devtools import terminal_scene_transition_contract as m


def sample(*vtables):
    return dict(elapsed=1.0,VM_hex=bytes(128).hex(),registered_tasks=[dict(pointer=0x10000+n*0x100,
        head_hex=int(v).to_bytes(4,'little').hex()) for n,v in enumerate(vtables)])


class TransitionContractTests(unittest.TestCase):
    def test_empty_graph_idle_pending_only_is_a_narrow_preflight(self):
        result=m.require_empty_scene_preflight(bytes(0x120).hex(),bytes(8).hex(),[])
        self.assertTrue(result['empty_graph_and_idle_event'])
        self.assertFalse(result['renderer_queue_empty_proved'])
        self.assertFalse(result['natural_retirement_proved'])

    def test_existing_worker_always_rejected_before_roots(self):
        for vtable in (m.STARTUP_VTABLE,m.MENU_VTABLE,m.SCENE_VTABLE,0x123456):
            with self.subTest(vtable=vtable),self.assertRaisesRegex(ValueError,'existing'):
                m.require_empty_scene_preflight(bytes(0x120).hex(),bytes(8).hex(),
                    sample(vtable)['registered_tasks'])

    def test_pending_event_rejected_even_with_empty_graph(self):
        with self.assertRaisesRegex(ValueError,'event must be idle'):
            m.require_empty_scene_preflight(bytes(0x120).hex(),(b'\x01'+bytes(7)).hex(),[])

    def test_truncated_graph_or_untraversed_bucket_rejected(self):
        for offset in range(0,0x100,4):
            manager=bytearray(0x120);manager[offset]=1
            with self.subTest(offset=offset),self.assertRaisesRegex(ValueError,'bucket'):
                m.require_empty_scene_preflight(manager.hex(),bytes(8).hex(),[])

    def test_complete_preflight_bytes_required(self):
        for manager,event in ((bytes(0x100),bytes(8)),(bytes(0x120),bytes(4))):
            with self.assertRaises(ValueError):
                m.require_empty_scene_preflight(manager.hex(),event.hex(),[])

    def test_actual_original_contract(self):
        result=m.source_contract((m.ROOT/'analysis/hermit_game.exe').read_bytes(),
            (m.ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT/T0004.BIN').read_bytes())
        self.assertGreater(len(result['instructions']),35)
        self.assertFalse(result['transition_repaired'])
        self.assertFalse(result['resource_fault_cause_proved'])

    def test_modified_source_rejected(self):
        source=bytearray((m.ROOT/'analysis/hermit_game.exe').read_bytes())
        source[0x50A043-0x400000]^=1
        with self.assertRaisesRegex(ValueError,'source identity'):
            m.source_contract(bytes(source),b'')

    def test_short_source_rejected(self):
        with self.assertRaises(ValueError): m.source_contract(b'',b'')

    def test_overlapping_startup_is_not_safe(self):
        row=m.graph_timeline([sample(m.STARTUP_VTABLE,m.SCENE_VTABLE)])
        self.assertTrue(row['observed_overlap']['startup_and_scene'])
        self.assertFalse(row['safe_transition_proved'])

    def test_startup_to_menu_beside_battle(self):
        row=m.graph_timeline([sample(m.STARTUP_VTABLE,m.SCENE_VTABLE),
            sample(m.SCENE_VTABLE),sample(m.SCENE_VTABLE,m.MENU_VTABLE)])
        self.assertEqual(len(row['changes']),3)
        self.assertTrue(row['observed_overlap']['menu_and_scene'])
        self.assertFalse(row['causal_resource_link_proved'])

    def test_scene_alone_does_not_prove_transition(self):
        self.assertFalse(m.graph_timeline([sample(m.SCENE_VTABLE)])['safe_transition_proved'])

    def test_repeated_graph_deduplicated(self):
        self.assertEqual(len(m.graph_timeline([sample(m.SCENE_VTABLE)]*10)['changes']),1)

    def test_cycle_duplicate_node_rejected(self):
        s=sample(m.SCENE_VTABLE)
        s['registered_tasks']*=2
        with self.assertRaisesRegex(ValueError,'unique'): m.graph_timeline([s])

    def test_bad_pointer_rejected(self):
        for pointer in (0,-1,0xDDDDDDDD,True):
            s=sample(m.SCENE_VTABLE);s['registered_tasks'][0]['pointer']=pointer
            with self.subTest(pointer=pointer),self.assertRaises(ValueError):m.graph_timeline([s])

    def test_sample_and_node_bounds(self):
        for data in ([],[sample()]*1601,[sample(*range(65))]):
            with self.assertRaises(ValueError):m.graph_timeline(data)

    def test_bad_node_bytes(self):
        for text in ('00','zzzzzzzz','0'*514,'0'*9):
            s=sample(m.SCENE_VTABLE);s['registered_tasks'][0]['head_hex']=text
            with self.subTest(text=text[:10]),self.assertRaises(ValueError):m.graph_timeline([s])

    def test_report_sha_bound(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'r.gz'
            packed=gzip.compress(json.dumps(dict(probe=dict(samples=[sample(m.SCENE_VTABLE)]))).encode())
            p.write_bytes(packed)
            self.assertFalse(m.report_summary(p,m.sha(packed))['safe_transition_proved'])
            with self.assertRaisesRegex(ValueError,'SHA'):m.report_summary(p,'0'*64)

    def test_compressed_budget(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'r.gz';p.write_bytes(b'xxxx')
            with patch.object(m,'MAX_PACKED',3),self.assertRaisesRegex(ValueError,'compressed'):
                m.report_summary(p,m.sha(b'xxxx'))

    def test_decompressed_budget(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'r.gz';packed=gzip.compress(b' '*1000);p.write_bytes(packed)
            with patch.object(m,'MAX_RAW',100),self.assertRaisesRegex(ValueError,'decompressed'):
                m.report_summary(p,m.sha(packed))

    def test_original_pause_and_resume_bytes_preserve_other_flags_and_node(self):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
        from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_ESP, UC_X86_REG_EIP
        import struct
        source=(m.ROOT/'analysis/hermit_game.exe').read_bytes()
        self.assertEqual(m.sha(source),m.SOURCE_SHA)
        for root,expected in ((0x422560,0x10003),(0x4225A0,0x10001)):
            with self.subTest(root=hex(root)):
                u=Uc(UC_ARCH_X86,UC_MODE_32)
                u.mem_map(0x422000,0x1000)
                u.mem_write(0x422000,source[0x22000:0x23000])
                u.mem_map(0x100000,0x2000)
                u.mem_map(0x200000,0x1000)
                u.mem_map(0x300000,0x1000)
                initial=bytearray(b'\x5a'*48)
                struct.pack_into('<I',initial,4,0x10001 if root==0x422560 else 0x10003)
                u.mem_write(0x200000,bytes(initial))
                u.mem_write(0x101000,struct.pack('<II',0x300000,2))
                u.reg_write(UC_X86_REG_ECX,0x200000)
                u.reg_write(UC_X86_REG_ESP,0x101000)
                u.emu_start(root,0x300000,count=100)
                self.assertEqual(u.reg_read(UC_X86_REG_EIP),0x300000)
                self.assertEqual(u.reg_read(UC_X86_REG_ESP),0x101008)
                struct.pack_into('<I',initial,4,expected)
                self.assertEqual(bytes(u.mem_read(0x200000,48)),bytes(initial))


if __name__=='__main__':unittest.main()

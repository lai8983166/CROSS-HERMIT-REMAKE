import hashlib
import json
import struct
import unittest
from tools.school_unitctrl_map_emulation import (SchoolUnitCtrlMapEmulator, ROOT,
    UNITCTRL,UHEAP,UHEAP_SIZE,MAP_BIN,MAP_GRAPHICS,map_resource,checked_grid_code)
from tools.school_combat_records_emulation import CHAR_BASE

EVIDENCE=ROOT/'analysis/school-unitctrl-map-v1-20261009.json'
EVIDENCE_SHA256='a3153daa1b814e534f9791395bd51db891296db012a38e3b4d2751abe36d499c'


class UnitCtrlMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(EVIDENCE.read_text('utf-8'))

    def test_frozen_native_identity_and_ready_refusal_branches(self):
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
        self.assertEqual([c['name'] for c in self.data['cases']],
            ['initial','student9_waiting','fifth_class','teacher_only','teacher_waiting'])
        for c in self.data['cases'][:3]:
            self.assertTrue(c['ready']);self.assertTrue(c['unitctrl_constructed']);self.assertTrue(c['logical_map_loaded'])
            self.assertEqual(c['stop_reason'],'scene_graphics_resource_boundary')
            self.assertEqual(c['scene_graphics_request']['relative_path'],MAP_GRAPHICS)
            self.assertEqual(c['scene_graphics_request']['caller_return_va'],'0x43a989')
        for c in self.data['cases'][3:]:
            for flag in ('ready','unitctrl_constructed','logical_map_loaded'):self.assertFalse(c[flag])
            for key in ('unitctrl_allocations','requests','phases','logical_events'):self.assertEqual(c[key],[])
            for key in ('logical_unitctrl','appearance_grid','logical_map','scene_graphics_request'):self.assertIsNone(c[key])

    def test_native_constructor_lists_vectors_and_generic_grid(self):
        for c in self.data['cases'][:3]:
            state=c['logical_unitctrl'];grid=c['appearance_grid'];allocs=c['unitctrl_allocations']
            self.assertEqual(state['receiver'],hex(UNITCTRL));self.assertEqual(state['task_backpointer'],'0xe000000')
            self.assertEqual(state['map_size'],[65,65]);self.assertEqual(state['zero_counts'],[0,0,0])
            self.assertEqual(state['sentinel'],'0x87654321');self.assertEqual(state['mode'],0)
            self.assertEqual(state['allocation_sizes'],[3600]*3+[8450,25350,8450,6144,3000]+[240]*10)
            self.assertEqual([a['freed'] for a in allocs],[False]*3+[True]+[False]*14)
            for a in allocs:self.assertTrue(UHEAP<=a['pointer']<a['pointer']+a['bytes']<=UHEAP+UHEAP_SIZE)
            rows=grid['rows'];raw=b''.join(struct.pack('<bbHH',*r) for r in rows)
            self.assertEqual(len(rows),4225);self.assertEqual(hashlib.sha256(raw).hexdigest(),grid['sha256'])
            self.assertEqual(grid['sha256'],'902e81f8eff318965e9f61f592a5a7c0541be0529ab5871e4dc6b6c4cbfbe4fd')
            self.assertEqual({tuple(r[:2]) for r in rows},{(x,y) for y in range(-32,33) for x in range(-32,33)})
            self.assertTrue(all(r[2]==abs(r[0])+abs(r[1]) and r[3]==i for i,r in enumerate(rows)))
            self.assertEqual(grid['static_graph'],checked_grid_code());self.assertFalse(grid['per_instruction_trace'])
            self.assertEqual(sum(e['kind']=='vector' for e in c['logical_events']),9)

    def test_source_selected_map_buffer_and_native_scratch_ownership(self):
        raw,identity=map_resource('map05.bin')
        for c in self.data['cases'][:3]:
            m=c['logical_map'];self.assertEqual(m['source'],identity)
            self.assertEqual(m['header'],list(struct.unpack_from('<8H',raw)))
            self.assertEqual(m['scene_id'],5);self.assertEqual(m['phase'],2);self.assertEqual(m['initial_unit_work'],110)
            self.assertEqual(m['header'][2:4],[64,96])
            self.assertEqual([a['bytes'] for a in m['map_allocations']],[4,12288,6144,6144,6144])
            self.assertEqual([a['caller_return_va'] for a in m['map_allocations']],['0x43a7a5','0x43a828']+['0x43d050']*3)
            self.assertEqual([a['pointer'] for a in m['map_allocations']],[m['cm_pointer']]+[s['pointer'] for s in m['scratch']])
            for s in m['scratch']:self.assertEqual(s['sha256'],hashlib.sha256(bytes(s['bytes'])).hexdigest())
            r=c['requests'][-1];self.assertEqual(r['source']['relative_path'],MAP_BIN)
            self.assertEqual(r['loaded_sha256'],identity['sha256']);self.assertEqual(r['loaded_bytes'],len(raw))
            self.assertEqual(r['buffer_pointer'],m['pointer'])
            opened=[e['result'] for e in c['file_events'] if e['name']=='CreateFileA']
            closed=[e['args'][0] for e in c['file_events'] if e['name']=='CloseHandle']
            self.assertEqual(opened,closed);self.assertEqual(len(opened),5)
            visited=c['phases'][-1]['coverage']['visited_function_entries']
            for va in ('0x4519c0','0x451f50','0x4538d0','0x452fc0','0x43a640','0x43ce10','0x43cfe0'):
                self.assertIn(va,visited)

    def test_persistent_current_records_and_execution_boundaries(self):
        for c in self.data['cases']:
            self.assertTrue(c['persistent_ranges_unchanged'])
            self.assertEqual(c['handoff']['before'],c['handoff']['after'])
            for flag in ('graphics_subcomponents_constructed','gpu_textures_uploaded','battle_world_constructed',
                         'live_witness','authorizes_persistent_write'):self.assertFalse(c[flag])
        for c in self.data['cases'][:3]:
            self.assertTrue(c['current_combat_records_unchanged'])
            self.assertEqual([e for e in c['logical_events'] if e['kind']=='declared_CRT_rand'],
                             [{'kind':'declared_CRT_rand','return_value':0}])

    def test_finite_constructor_guard_and_allocations(self):
        e=SchoolUnitCtrlMapEmulator();e.logical=True
        for address in (CHAR_BASE,0x7CF34C,0x7A528E,UHEAP):
            with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,address,4,0,None)
        p=e._unit_allocate(3600,0x4276E1);e._write_hook(e.uc,0,p,4,1,None)
        with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,p+3599,4,0,None)
        e.unit_allocations[0]['freed']=True
        with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,p,4,0,None)
        for count,caller in ((3599,0x4276E1),(3600,0x400000),(25349,0x43ABA8)):
            with self.assertRaises(RuntimeError):e._unit_allocate(count,caller)


if __name__=='__main__':unittest.main()

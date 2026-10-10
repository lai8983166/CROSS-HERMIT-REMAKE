import hashlib,json,struct,unittest
from tools.school_scene_unit_constructor_emulation import (
    SchoolSceneUnitConstructorEmulator,ROOT,UNITCTRL,WORK_OFFSET,WORK_BYTES,
    SCENE_CONTROLLER,SCENE_ANIM,SCENE_PATH,SCENE_SHA,TASK,STACK,RECORD_OFFSET,
    CACHE_OFFSET,COUNTER_OFFSET,UC_X86_REG_ESP)

EVIDENCE=ROOT/'analysis/school-scene-unit-constructor-v1-20261010.json'
EVIDENCE_SHA256='fdf436b3dbea1491e7fd10bd129a44e0ecaff1b0a2ed6b490ccd95f3b2f42e20'
PALETTES=ROOT/'analysis/school-scene-unit-animation-palettes-v1-20261010.json'
PALETTE_SHA256='a501ecabb2f54f2050a0100b72c02dcba2b0ea428e202dffa800bfd18b057655'


class SceneUnitConstructorNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.full=json.loads(EVIDENCE.read_text('utf-8'))
        cls.palettes=json.loads(PALETTES.read_text('utf-8'))

    def test_actual_school_natural_return_and_refusal(self):
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
        self.assertEqual([c['scene_unit_constructor_completed'] for c in self.full['cases']],
                         [True,True,True,False,False])
        self.assertEqual([len(c['current_units']) for c in self.full['cases'][:3]],[3,2,2])
        for c in self.full['cases'][:3]:
            p,a,t=c['scene_unit_work'],c['scene_unit_animation'],c['scene_unit_constructor']
            self.assertEqual((p['index'],p['role'],p['job'],p['category'],a['variant']),(249,5,4,7,5))
            self.assertEqual(c['stop_reason'],'after_first_scene_unit_constructor_return')
            self.assertEqual((t['return_va'],t['return_eax']),('0x453630',0))
            self.assertTrue(t['constructor_completed']);self.assertEqual(t['constructor_coordinates'],[52,65])
            self.assertEqual([x['bytes'] for x in t['clears']],[88]*6+[42]+[236]*2)
            work=bytes.fromhex(t['work_hex'])
            self.assertEqual(struct.unpack_from('<H',work,0x56)[0],40)
            self.assertEqual(struct.unpack_from('<H',work,0x4FE)[0],600)
            self.assertEqual(struct.unpack_from('<I',work,0x44)[0],SCENE_CONTROLLER)
        for c in self.full['cases'][3:]:
            self.assertIsNone(c['scene_unit_animation']);self.assertIsNone(c['scene_unit_constructor'])

    def test_exact_file_allocation_vector_and_declared_gpu_boundaries(self):
        for c in self.full['cases'][:3]:
            a=c['scene_unit_animation']
            self.assertEqual(a['request']['source']['relative_path'],SCENE_PATH)
            self.assertEqual(a['request']['loaded_sha256'],SCENE_SHA)
            names=[x['name'] for x in a['file_events']]
            self.assertEqual(names[-4:],['CreateFileA','GetFileSize','ReadFile','CloseHandle'])
            self.assertTrue(set(names)<=set(['GetCurrentDirectoryA','CreateFileA','GetFileSize','ReadFile','CloseHandle']))
            self.assertEqual([x['bytes'] for x in a['allocations']],[1331256,17108,244*84+4])
            self.assertEqual([x['freed'] for x in a['allocations']],[True,False,False])
            self.assertEqual(a['vector']['native_constructors_completed'],244)
            self.assertEqual(len(a['entries']),244)
            self.assertEqual(sum(b['kind']=='texture_creation' for b in a['boundaries']),244)
            self.assertEqual(sum(b['kind']=='pixel_upload' for b in a['boundaries']),244)
            self.assertEqual(struct.unpack('<II',bytes.fromhex(a['texture_slot_hex'])),
                             (a['allocations'][2]['pointer']+4,244))
            self.assertFalse(a['constructor_completed'])

    def test_all_other_mapped_bytes_retained_and_declared_palette_scope(self):
        for c in self.full['cases']:
            self.assertTrue(c['persistent_ranges_unchanged']);self.assertFalse(c['battle_world_constructed'])
            self.assertFalse(c['live_witness'])
        for c in self.full['cases'][:3]:
            for n in (c['scene_unit_animation'],c['scene_unit_constructor']):
                self.assertTrue(n['retained_ranges_unchanged']);self.assertGreater(n['retained_bytes'],100_000_000)
                self.assertEqual(sum(x['bytes'] for x in n['retained_ranges']),n['retained_bytes'])
                self.assertFalse(n['scene_placement_executed'])
            self.assertFalse(c['scene_unit_constructor']['scene_vm_executed'])
        d=self.palettes
        self.assertEqual(hashlib.sha256(PALETTES.read_bytes()).hexdigest(),PALETTE_SHA256)
        self.assertEqual([n['variant'] for n in d['probes']],[1,40])
        self.assertFalse(d['school_enemy_loop_executed'])
        for n in d['probes']:
            self.assertEqual(n['declared_argument_write']['before'],5)
            self.assertEqual(n['prefix']['variant'],5)
            self.assertEqual(n['animation']['request']['args'][1],n['variant'])
            self.assertEqual(n['stop_reason'],'after_first_scene_unit_animation_binding')
            self.assertFalse(n['constructor_tail_executed'])

    def test_finite_write_and_resource_guard_reject_other_units_and_owners(self):
        e=SchoolSceneUnitConstructorEmulator();e.scene_complete_loading=True;e.scene_phase='tail'
        e.active_index=249;e.constructor_cell=0x1000100;e.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00)
        work=UNITCTRL+WORK_OFFSET+249*WORK_BYTES
        for at in (work-1,work+WORK_BYTES,UNITCTRL+RECORD_OFFSET+249*176,
                   UNITCTRL+CACHE_OFFSET,UNITCTRL+COUNTER_OFFSET,SCENE_CONTROLLER,SCENE_ANIM):
            with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,1,0,None)
        for at in (0x424F80,0x428A40,0x428AD0,0x4500B0,0x468910):
            with self.assertRaises(RuntimeError):e._hook(e.uc,at,1,None)
        e.scene_phase='animation';e.controller=SCENE_CONTROLLER;e.texture_table=TASK+0x844
        e.scene_texture_slot=113;e.animation_allocations=[]
        for at in (work,TASK+0x844+112*8,SCENE_CONTROLLER+84,SCENE_ANIM):
            with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,1,0,None)


if __name__=='__main__':unittest.main()

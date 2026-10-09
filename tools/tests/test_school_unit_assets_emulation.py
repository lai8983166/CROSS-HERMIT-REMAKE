import hashlib
import json
import unittest
from tools.school_unit_assets_emulation import (SchoolUnitAssetsEmulator,ROOT,
    ASSET_POOL,ASSET_POOL_SIZE,CHAR_BASE,UNITS,RESET_RANGES,TEXT_GROUPS,EFFECT_SHA)

EVIDENCE = ROOT/'analysis/school-unit-assets-v1-20261010.json'
SHA = '2fc5bcefd011b62f1486a3edf3699b3cd528843a21910c64a6eee022c6be987d'


class UnitAssetNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(EVIDENCE.read_text('utf-8'))

    def test_actual_school_cases_and_exact_read_only_file(self):
        self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),SHA)
        self.assertEqual([c['unit_assets_prepared'] for c in self.data['cases']],[True,True,True,False,False])
        for c in self.data['cases'][:3]:
            self.assertEqual(c['asset_requests'][0]['loaded_sha256'],EFFECT_SHA)
            self.assertEqual(c['asset_requests'][0]['loaded_bytes'],15662260)
            opened = [e['result'] for e in c['file_events'] if e['name']=='CreateFileA']
            closed = [e['args'][0] for e in c['file_events'] if e['name']=='CloseHandle']
            self.assertEqual(len(opened),9)
            self.assertEqual(opened,closed)
            for e in c['file_events']:
                if e['name']=='CreateFileA':
                    self.assertEqual(e['args'][1:],[0x80000000,1,0,3,1,0])

    def test_reset_text_and_owned_effect_metadata(self):
        for c in self.data['cases'][:3]:
            self.assertEqual(len(c['text_requests']),sum(n for _,n,_ in TEXT_GROUPS))
            self.assertEqual(len(c['asset_boundaries']),1536)
            reset = c['unit_reset_snapshot']
            for r,(offset,count) in zip(reset['regions'],RESET_RANGES):
                self.assertEqual(r['offset'],hex(offset))
                self.assertEqual(r['sha256'],hashlib.sha256(bytes(count)).hexdigest())
            for t in c['text_requests']:
                self.assertEqual(t['source_color_hex'],'ffffffff')
                self.assertFalse(t['platform_rendered'])
            allocs = c['asset_allocations']
            self.assertEqual([a['bytes'] for a in allocs],[84,15662260,77212])
            self.assertTrue(all(not a['freed'] for a in allocs))
            for a in allocs:
                self.assertTrue(ASSET_POOL <= a['pointer'] < a['pointer']+a['bytes'] <= ASSET_POOL+ASSET_POOL_SIZE)
            effect = c['unit_assets']
            self.assertEqual(effect['controller'],allocs[0]['pointer'])
            self.assertEqual(effect['metadata_pointer'],allocs[2]['pointer'])
            self.assertEqual(effect['animation_id'],0)
            self.assertEqual(effect['kind_field'],100)

    def test_retained_current_records_and_effect_texture_boundary(self):
        for c in self.data['cases']:
            self.assertTrue(c['persistent_ranges_unchanged'])
            self.assertFalse(c['battle_world_constructed'])
            self.assertFalse(c['live_witness'])
            self.assertFalse(c['authorizes_persistent_write'])
        for c in self.data['cases'][:3]:
            self.assertTrue(c['current_combat_records_unchanged'])
            self.assertEqual(c['stop_reason'],'before_effect_texture_binding')
            visited = c['phases'][-1]['coverage']['visited_function_entries']
            for va in ('0x467eb0','0x468bc0','0x4671f0','0x467380','0x467520','0x4676c0',
                       '0x408e30','0x466000','0x464c60','0x409900','0x41ead0','0x464d70','0x409b70'):
                self.assertIn(va,visited)
            for va in ('0x41ebf0','0x4680b0','0x453540','0x468910'):
                self.assertNotIn(va,visited)
        for c in self.data['cases'][3:]:
            self.assertEqual(c['text_requests'],[])
            self.assertEqual(c['asset_requests'],[])
            self.assertIsNone(c['unit_assets'])

    def test_finite_allocation_guard_and_protected_records(self):
        e = SchoolUnitAssetsEmulator()
        e.unit_loading = True
        for p in (CHAR_BASE,UNITS,0x7CF34C,0x7A528E,ASSET_POOL):
            with self.assertRaises(RuntimeError):
                e._write_hook(e.uc,0,p,4,0,None)
        p = e.asset_allocate(16,'declared_guard_test',0)
        e._write_hook(e.uc,0,p,4,0,None)
        with self.assertRaises(RuntimeError):
            e._write_hook(e.uc,0,p+15,4,0,None)
        e.asset_allocations[-1]['freed'] = True
        with self.assertRaises(RuntimeError):
            e._write_hook(e.uc,0,p,4,0,None)
        with self.assertRaises(RuntimeError):
            e.asset_allocate(ASSET_POOL_SIZE+1,'declared_guard_test',0)


if __name__ == '__main__':
    unittest.main()

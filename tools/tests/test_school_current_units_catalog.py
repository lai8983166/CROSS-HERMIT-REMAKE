from copy import deepcopy
import json
import struct
import unittest
from tools.dxanim_lib import DxAnimError
from tools.school_current_units_catalog import (
    source_catalog,native_fixture,expected_order,expected_progress,expected_cache,archive_inputs,
    expected_first_work,expected_current_constructor,expected_current_binding,EVIDENCE,CACHE_EVIDENCE,ROOT)


class CurrentUnitSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = source_catalog();cls.full = json.loads(EVIDENCE.read_text('utf-8'))
        cls.cache = json.loads(CACHE_EVIDENCE.read_text('utf-8'))

    def check_unit(self,u,first_case=None):
        r = self.rules
        if first_case:
            p,a = first_case['first_unit_work'],first_case['first_unit_animation']
            record,counter,controller = p['before_record_hex'],p['cache_input']['previous_counter'],a['controller']
            work_hex,record_hex = p['work_hex'],p['record_hex']
            before_controller,allocations = a['graphics_input']['controller_before_hex'],a['allocations']
            variant = bytes.fromhex(p['cache_hex'])[1];metadata = a['metadata_hex']
            entries = first_case['unit_texture_entries'];release = a['file_release']
            before_cm = first_case['first_unit_constructor']['before_cm_hex']
        else:
            record,counter,controller = u['before_record_hex'],u['counter_before'],u['controller']
            work_hex,record_hex = u['prefix_work_hex'],u['prefix_record_hex']
            before_controller,allocations = u.get('controller_before_hex'),u['animation_allocations']
            variant,metadata,entries,release,before_cm = u['variant'],u['metadata_hex'],u['entries'],u['file_release'],u['before_cm_hex']
        prefix = expected_first_work(record,u['index'],counter,0x1000000,controller,r['work'])
        self.assertEqual(prefix['work_hex'],work_hex);self.assertEqual(prefix['record_hex'],record_hex)
        self.assertEqual(prefix['resource_args'][1],variant)
        if not u.get('cache_hit'):
            self.assertEqual(prefix['controller_hex'],before_controller)
            pointers = {a['kind']:a['pointer'] for a in allocations}
            binding = expected_current_binding(before_controller,pointers['unit_file_buffer'],pointers['unit_metadata'],
                pointers['unit_texture_array'],0x1000844,variant,r,u['job'])
            actual_controller = first_case['first_unit_animation']['controller_hex'] if first_case else u['controller_hex']
            self.assertEqual(binding['controller_hex'],actual_controller);self.assertEqual(binding['metadata_hex'],metadata)
            self.assertEqual(binding['source_sha256_at_release'],release['sha256_at_release'])
            self.assertEqual(len(entries),len(binding['texture_entries']))
            for actual,e in zip(entries,binding['texture_entries']):
                for k in e:
                    if k!='upload_args':self.assertEqual(actual[k],e[k],(u['job'],actual['index'],k))
            boundaries = first_case['unit_animation_boundaries'] if first_case else u['animation_boundaries']
            uploads = [b for b in boundaries if b['kind']=='pixel_upload']
            self.assertEqual(len(uploads),len(binding['texture_entries']))
            for actual,e in zip(uploads,binding['texture_entries']):
                self.assertEqual(actual['args'],e['upload_args'],(u['job'],e['index']))
        tail = expected_current_constructor(work_hex,record_hex,u['work_pointer'],controller,u['metadata_pointer'],before_cm,r)
        for k in ('work_hex','record_hex'):self.assertEqual(u[k],tail[k],(u['job'],k))
        if not first_case:
            for k in ('shared_hex','cm_hex'):self.assertEqual(u[k],tail[k],k)
            cache = expected_cache(u['cache_before_hex'],u['job'],variant,controller,r)
            self.assertEqual(cache['cache_hex'],u['cache_after_hex']);self.assertEqual(cache['slot'],u['cache_slot'])
            self.assertEqual(cache['hit'],u['cache_hit']);self.assertEqual(counter+cache['counter_delta'],u['counter_after'])

    def test_every_actual_unit_full_prefix_binding_constructor_cache_bytes(self):
        for c in self.full['cases'][:3]:
            for i,u in enumerate(c['current_units']):self.check_unit(u,c if i==0 else None)

    def test_source_order_progress_and_all_original_archive_shapes(self):
        for c in self.full['cases'][:3]:
            loop = c['current_loop'];order = expected_order(loop['source_header_hex'],loop['source_records'],self.rules)
            self.assertEqual(order,[u['index'] for u in c['current_units']])
            progress = expected_progress(loop['before_progress_hex'],len(order),self.rules)
            self.assertEqual(progress['after_hex'],loop['after_progress_hex'])
            self.assertEqual(progress['events'],[{k:e[k] for k in ('before_hex','after_hex')} for e in loop['progress']])
            for copy in loop['copies']:self.assertEqual(copy['record_hex'],loop['source_records'][copy['index']])
        self.assertEqual([len(self.rules['jobs'][str(j)]['animation']['texture_entries']) for j in (6,7,10)],[219,147,193])
        self.assertEqual(expected_progress('8080',1,self.rules)['after_hex'],'8080')
        self.assertEqual(expected_progress('00ff',1,self.rules)['after_hex'],'ffff')
        self.assertEqual(expected_progress('81ff',1,self.rules)['after_hex'],'8080')
        # Declared mixed categories: A4 controls priority, independently of class94.
        loop = self.full['cases'][0]['current_loop'];header = bytearray.fromhex(loop['source_header_hex'])
        header[8] = 2;records = [bytearray.fromhex(s) for s in loop['source_records']]
        for record,category,group in zip(records,(1,2,0),(2,1,2)):
            record[0xA4] = category;record[0x94] = group
        self.assertEqual(expected_order(header.hex(),[s.hex() for s in records],self.rules),[1,0,2])

    def test_declared_cache_cpu_reuse_matches_source_without_resource_reload(self):
        a,b = self.cache['units'];self.check_unit(a);self.check_unit(b)
        self.assertEqual(b['metadata_hex'],a['metadata_hex']);self.assertEqual(b['controller_hex'],a['controller_hex'])
        self.assertTrue(b['retained_ranges_unchanged']);self.assertTrue(b['cache_hit'])

    def test_malformed_and_unsupported_source_inputs_refuse(self):
        c = self.full['cases'][0];loop = c['current_loop'];u = c['current_units'][1];r = self.rules
        for header,records in (('zz',[]),('00'*143,[]),(loop['source_header_hex'],[])):
            with self.assertRaises(ValueError):expected_order(header,records,r)
        for text,count in (('zz',1),('00',1),('0000',True),('0000',35)):
            with self.assertRaises(ValueError):expected_progress(text,count,r)
        for text,job,variant,controller in (('00',6,4,4),(u['cache_before_hex'],99,4,4),(u['cache_before_hex'],6,0,4),(u['cache_before_hex'],6,4,True)):
            with self.assertRaises(ValueError):expected_cache(text,job,variant,controller,r)
        cache = bytearray.fromhex(u['cache_before_hex']);cache[8]=2
        with self.assertRaises(ValueError):expected_cache(cache.hex(),6,4,u['controller'],r)
        for job in (6,7,10):
            raw = (ROOT/r['jobs'][str(job)]['source']['local_file']).read_bytes()
            for bad in (b'',raw[:20],raw[:-1]):
                with self.assertRaises((ValueError,struct.error,DxAnimError)):archive_inputs(bad)
        for at,value in ((0x28A,0),(0x290,7),(0x44,1)):
            work = bytearray.fromhex(u['prefix_work_hex']);work[at]=value
            with self.assertRaises(ValueError):expected_current_constructor(work.hex(),u['prefix_record_hex'],u['work_pointer'],u['controller'],u['metadata_pointer'],u['before_cm_hex'],r)
        p = {a['kind']:a['pointer'] for a in u['animation_allocations']}
        for variant in (0,41,True):
            with self.assertRaises(ValueError):expected_current_binding(u['controller_before_hex'],p['unit_file_buffer'],p['unit_metadata'],p['unit_texture_array'],0x1000844,variant,r,6)

    def test_fixed_native_fixture_and_independent_exports_separate(self):
        rules = json.loads((ROOT/'prototype/data/school_current_units_rules.json').read_text('utf-8'))
        fixture = json.loads((ROOT/'prototype/data/school_current_units_evidence.json').read_text('utf-8'))
        self.assertEqual(rules,self.rules);self.assertEqual(fixture,native_fixture())
        self.assertNotIn('cases',rules);self.assertNotIn('jobs',fixture)
        before = deepcopy(rules);fixture['cases'][0]['current_units'][0]['work_hex']='';self.assertEqual(rules,before)


if __name__=='__main__':unittest.main()

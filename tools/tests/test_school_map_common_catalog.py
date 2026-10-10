from copy import deepcopy
import hashlib
import json
import struct
import unittest
from unicorn.x86_const import UC_X86_REG_EBP, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_map_common_catalog import (
    source_catalog,native_fixture,map_common_inputs,prepare_current_records,ROOT)
from tools.school_map_common_emulation import (
    SchoolMapCommonEmulator,map_common_resource,MAP_POOL,UNITS,TACT,STACK,RETURN)


class MapCommonSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules,cls.fixture = source_catalog(),native_fixture()

    def test_all_offsets_and_current_bytes_against_independent_inputs(self):
        for c in self.fixture['cases'][:3]:
            m = c['map_common']
            roots = [MAP_POOL+s['offset'] for s in self.rules['sections']]
            nested = [MAP_POOL+s['file_offset'] for s in self.rules['first_section_entries']]
            self.assertEqual(m['top_level_pointers'],roots)
            self.assertEqual(m['nested_pointers'],nested)
            self.assertEqual([p['pointer'] for p in m['pointer_calls']],roots+nested)
            p = c['current_record_preparation']
            independent = prepare_current_records(p['header'],p['before_records'],self.rules['current_preparation_policy'])
            self.assertEqual(p['after_records'],independent['after_records'])
            self.assertEqual(c['current_copies'][0]['index'],independent['construction_order'][0])
        raw,_ = map_common_resource()
        for s in self.rules['sections']+self.rules['first_section_entries']:
            at = s.get('file_offset',s['offset'])
            self.assertEqual(s['sha256'],hashlib.sha256(raw[at:at+s['bytes']]).hexdigest())

    def test_policy_all_flag_branches_states_overflow_and_selection_against_native_cpu(self):
        # These are isolated declared inputs, separate from actual school evidence.
        policy = self.rules['current_preparation_policy']
        for a,b,c in ((a,b,c) for a in (0,1) for b in (0,1) for c in (0,1)):
            for selected in (0,4):
                e = SchoolMapCommonEmulator()
                e.map_loading = True
                e.combat_records = [{}]*7
                records = []
                for i,state in enumerate((0,1,2,3,4,5,6)):
                    r = bytearray(176)
                    r[0xF] = state
                    r[0x94] = 4 if i==6 else 0
                    struct.pack_into('<iI',r,0x20,20000,0x7FFFFFF0 if i==3 else 100)
                    records.append(r.hex())
                    e.uc.mem_write(UNITS+i*176,bytes(r))
                header = {'0x7f448f':a,'0x7f448c':b,'0x7f44b8':c,'0x7f448d':7,'0x7f4490':selected}
                for address,value in header.items():
                    e.write(int(address,16),value,'B')
                frame = STACK+0xFF00
                e.write(frame-4,TACT)
                e.uc.reg_write(UC_X86_REG_EBP,frame)
                e.uc.reg_write(UC_X86_REG_ESP,frame-0x100)
                e.uc.emu_start(0x4531A8,RETURN,count=100_000)
                self.assertEqual(e.uc.reg_read(UC_X86_REG_EIP),0x4680B0)
                independent = prepare_current_records(header,records,policy)
                actual = [bytes(e.uc.mem_read(UNITS+i*176,176)).hex() for i in range(7)]
                self.assertEqual(actual,independent['after_records'],(a,b,c,selected))
                self.assertEqual(e.current_copies[0]['index'],independent['construction_order'][0])
                copy = e.current_copies[0]
                self.assertEqual(bytes(e.uc.mem_read(copy['target'],176)).hex(),copy['record_hex'])

    def test_malformed_containers_and_preparation_inputs_rejected(self):
        raw,_ = map_common_resource()
        first = self.rules['sections'][0]['offset']
        cases = [b'',raw[:-1]]
        for offset,value in ((4,3),(8,0),(12,24),(first+4,32),(first+8,0),(first+12,140)):
            changed = bytearray(raw)
            struct.pack_into('<I',changed,offset,value)
            cases.append(changed)
        for case in cases:
            with self.assertRaises(ValueError):
                map_common_inputs(case)
        header = {'0x7f448f':0,'0x7f448c':0,'0x7f44b8':0,'0x7f448d':1,'0x7f4490':0}
        for records in ([],['00'],['zz'*176]):
            with self.assertRaises(ValueError):
                prepare_current_records(header,records,self.rules['current_preparation_policy'])
        for change in ({'0x7f448d':255},{'0x7f448f':-1}):
            with self.assertRaises(ValueError):
                prepare_current_records({**header,**change},['00'*176],self.rules['current_preparation_policy'])

    def test_exports_and_native_fixture_are_separate_and_exact(self):
        rules = json.loads((ROOT/'prototype/data/school_map_common_rules.json').read_text('utf-8'))
        fixture = json.loads((ROOT/'prototype/data/school_map_common_evidence.json').read_text('utf-8'))
        self.assertEqual(rules,self.rules)
        self.assertEqual(fixture,self.fixture)
        self.assertNotIn('cases',rules)
        self.assertNotIn('current_preparation_policy',fixture)
        original = deepcopy(self.rules)
        fixture['cases'][0]['current_copies'][0]['record_hex'] = ''
        self.assertEqual(self.rules,original)


if __name__ == '__main__':
    unittest.main()

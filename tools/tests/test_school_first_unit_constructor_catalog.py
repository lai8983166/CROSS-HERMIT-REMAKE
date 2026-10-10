from copy import deepcopy
import json
import struct
import unittest
from tools.school_first_unit_constructor_catalog import source_catalog,native_fixture,expected_constructor,ROOT,EVIDENCE
from tools.school_first_unit_work_catalog import expected_first_work


class FirstUnitConstructorSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules,cls.fixture = source_catalog(),native_fixture()

    def expected(self,w,**changes):
        args = {k:w[k] for k in ('before_work_hex','record_hex','work_pointer','before_cm_hex')}
        args.update(controller_pointer=0x14000000,metadata_pointer=0x150DFE00,rules=self.rules)
        args.update(changes)
        return expected_constructor(**args)

    def test_complete_native_work_record_shared_and_cell_against_independent_source(self):
        full = json.loads(EVIDENCE.read_text('utf-8'))
        for c in full['cases'][:3]:
            w,p = c['first_unit_constructor'],c['first_unit_work']
            prefix = expected_first_work(p['before_record_hex'],p['index'],p['cache_input']['previous_counter'],0x1000000,p['allocation']['pointer'])
            self.assertEqual(prefix['work_hex'],w['before_work_hex'])
            self.assertEqual(prefix['record_hex'],w['record_hex'])
            e = self.expected(w)
            for k in ('work_hex','record_hex','shared_hex','cm_hex','cm_sha256','constructor_coordinates'):
                self.assertEqual(e[k],w[k],k)
            self.assertEqual([e[k] for k in ('action','direction','mapped_direction','block','animation','flags','first_program_offset','descriptor_index')],
                             [18,2,1,0,89,0,2656,4095])

    def test_original_tables_no_descriptor_and_cell_wrap_or_nonzero_coordinates(self):
        r,w = self.rules,self.fixture['cases'][0]['first_unit_constructor']
        self.assertEqual(r['status_actions'][24],18)
        self.assertEqual(r['direction_map'],[0,5,1,7,2,0,3,4,0,6])
        cm = bytearray.fromhex(w['before_cm_hex']);cm[1]=255
        e = self.expected(w,before_cm_hex=cm.hex())
        self.assertEqual(bytes.fromhex(e['cm_hex'])[1],0)
        record = bytearray.fromhex(w['record_hex']);record[0x9B:0x9D]=bytes([63,95])
        e = self.expected(w,record_hex=record.hex())
        self.assertEqual(e['constructor_coordinates'],[63,95])
        self.assertEqual(bytes.fromhex(e['cm_hex'])[-1],1)
        self.assertEqual(e['fixed_coordinates'],[((63<<5)+16)<<16,((95<<4)+8)<<16])
        raw = bytes.fromhex(e['work_hex'])
        self.assertEqual(struct.unpack_from('<I',raw,0x60)[0],7)
        self.assertEqual(struct.unpack_from('<H',raw,0x56)[0],30)

    def test_bad_or_unsupported_inputs_are_rejected(self):
        w = self.fixture['cases'][0]['first_unit_constructor']
        for k,size in (('before_work_hex',0x520),('record_hex',176),('before_cm_hex',12288)):
            for value in (None,'zz','00'*(size-1)):
                with self.assertRaises(ValueError):self.expected(w,**{k:value})
        for k in ('work_pointer','controller_pointer','metadata_pointer'):
            for value in (0,-4,True,'4',0xFFFFFFFF,3):
                with self.assertRaises(ValueError):self.expected(w,**{k:value})
        with self.assertRaises(ValueError):self.expected(w,controller_pointer=w['work_pointer'])
        for at,value in ((0x290,0),(0x290,7),(0x28A,0),(0x28A,10),(0x44,1)):
            raw = bytearray.fromhex(w['before_work_hex']);raw[at]=value
            with self.assertRaises(ValueError):self.expected(w,before_work_hex=raw.hex())
        for at,value in ((2,255),(12,6),(0xA4,4),(0xF,0),(0x9B,64),(0x9C,96)):
            raw = bytearray.fromhex(w['record_hex']);raw[at]=value
            with self.assertRaises(ValueError):self.expected(w,record_hex=raw.hex())
        rules = deepcopy(self.rules);rules['position_words'][89]=0xFFFF
        with self.assertRaises(ValueError):self.expected(w,rules=rules)
        rules = deepcopy(self.rules);rules['programs'][0][89][0]['opcode']=1
        with self.assertRaises(ValueError):self.expected(w,rules=rules)

    def test_fixed_native_exports_separate_from_independent_rules(self):
        rules = json.loads((ROOT/'prototype/data/school_first_unit_constructor_rules.json').read_text('utf-8'))
        fixture = json.loads((ROOT/'prototype/data/school_first_unit_constructor_evidence.json').read_text('utf-8'))
        self.assertEqual(rules,self.rules);self.assertEqual(fixture,self.fixture)
        self.assertNotIn('cases',rules);self.assertNotIn('programs',fixture)
        saved = deepcopy(rules);fixture['cases'][0]['first_unit_constructor']['work_hex']=''
        self.assertEqual(rules,saved)


if __name__=='__main__':unittest.main()

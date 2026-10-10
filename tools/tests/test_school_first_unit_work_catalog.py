from copy import deepcopy
import hashlib
import json
import struct
import unittest
from unicorn.x86_const import UC_X86_REG_ECX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_first_unit_work_catalog import source_catalog,native_fixture,expected_first_work,ROOT
from tools.school_first_unit_work_emulation import (
    SchoolFirstUnitWorkEmulator,UNITCTRL,UNIT_POOL,WORK_OFFSET,WORK_BYTES,RECORD_OFFSET,
    CACHE_OFFSET,CACHE_COUNT,COUNTER_OFFSET,TASK,STACK,RETURN)


class FirstUnitSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules,cls.fixture = source_catalog(),native_fixture()

    def test_all_work_record_controller_cache_bytes_and_arguments_against_source(self):
        for c in self.fixture['cases'][:3]:
            w = c['first_unit_work']
            expected = expected_first_work(w['before_record_hex'],w['index'],w['cache_input']['previous_counter'],TASK,UNIT_POOL,self.rules)
            for key in ('work_hex','record_hex','controller_hex','cache_hex','counter'):
                self.assertEqual(w[key],expected[key],key)
            self.assertEqual(w['resource_request']['args'],expected['resource_args'])
            self.assertEqual(w['resource_request']['relative_path'],expected['relative_path'])
        for job in self.rules['jobs']:
            identity = job['resource_identity']
            raw = (ROOT/identity['path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),identity['sha256'])
            self.assertFalse(identity['loaded_by_native_stage'])

    def test_declared_jobs_states_and_indices_against_native_prefix(self):
        # Isolated inputs, never described as additional actual-school branches.
        base = bytearray(176)
        struct.pack_into('<H',base,2,3)
        for job in (6,7,10):
            for state in (0,1,2):
                for index in (0,2):
                    e = SchoolFirstUnitWorkEmulator()
                    e.stage = 'tactical_startup'
                    e.first_unit_loading = True
                    e.active_index = index
                    record = bytearray(base)
                    struct.pack_into('<H',record,0xC,job)
                    record[0xF] = state
                    e.uc.mem_write(0x7A49FC,struct.pack('<I',TASK))
                    e.uc.mem_write(0x7A4A00,struct.pack('<I',TASK+0x80000))
                    e.write(UNITCTRL+COUNTER_OFFSET,110)
                    target = UNITCTRL+RECORD_OFFSET+index*176
                    e.uc.mem_write(target,bytes(record))
                    sp = STACK+0xFF00
                    e.write(sp,RETURN)
                    e.write(sp+4,index)
                    e.uc.reg_write(UC_X86_REG_ESP,sp)
                    e.uc.reg_write(UC_X86_REG_ECX,UNITCTRL)
                    e.uc.emu_start(0x4680B0,RETURN,count=100_000)
                    self.assertEqual(e.uc.reg_read(UC_X86_REG_EIP),0x4500B0)
                    expected = expected_first_work(record.hex(),index,110,TASK,UNIT_POOL,self.rules)
                    for key,address,count in (('work_hex',UNITCTRL+WORK_OFFSET+index*WORK_BYTES,WORK_BYTES),
                            ('record_hex',target,176),('controller_hex',UNIT_POOL,84),
                            ('cache_hex',UNITCTRL+CACHE_OFFSET,CACHE_COUNT*8)):
                        self.assertEqual(bytes(e.uc.mem_read(address,count)).hex(),expected[key],(job,state,index,key))
                    self.assertEqual(e.unit_request['args'],expected['resource_args'])

    def test_malformed_and_unsupported_inputs_refused(self):
        record = bytearray(176)
        struct.pack_into('<H',record,2,3)
        struct.pack_into('<H',record,0xC,10)
        for raw in ('','zz'*176,'00'*175):
            with self.assertRaises(ValueError):
                expected_first_work(raw,0,110,TASK,UNIT_POOL,self.rules)
        for index,counter in ((-1,110),(250,110),(0,-1),(0,256)):
            with self.assertRaises(ValueError):
                expected_first_work(record.hex(),index,counter,TASK,UNIT_POOL,self.rules)
        for at,value in ((2,0),(2,35),(0xC,99),(0xA4,4)):
            changed = bytearray(record)
            struct.pack_into('<H' if at in (2,0xC) else '<B',changed,at,value)
            with self.assertRaises(ValueError):
                expected_first_work(changed.hex(),0,110,TASK,UNIT_POOL,self.rules)

    def test_exports_and_fixed_fixture_remain_independent_and_exact(self):
        rules = json.loads((ROOT/'prototype/data/school_first_unit_work_rules.json').read_text('utf-8'))
        fixture = json.loads((ROOT/'prototype/data/school_first_unit_work_evidence.json').read_text('utf-8'))
        self.assertEqual(rules,self.rules)
        self.assertEqual(fixture,self.fixture)
        self.assertNotIn('cases',rules)
        self.assertNotIn('jobs',fixture)
        original = deepcopy(self.rules)
        fixture['cases'][0]['first_unit_work']['controller_hex'] = ''
        self.assertEqual(self.rules,original)


if __name__ == '__main__':
    unittest.main()

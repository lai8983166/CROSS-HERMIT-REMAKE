import copy
import gzip
import hashlib
import json
import struct
import unittest
from unittest.mock import patch
from devtools import terminal_story_dispatch_verification as v
from devtools import terminal_school_handoff_verification as school


class ActualDispatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=school.ROOT/'analysis/terminal-school-handoff-guest-v5-20261109.json.gz'
        packed=path.read_bytes()
        if hashlib.sha256(packed).hexdigest()!='64976ca051fa42ae2e1e97561cc998ec85bacd11526810c8ec9f01fc7ac08ce6':raise ValueError('fixed actual source')
        cls.report=json.loads(gzip.decompress(packed));cls.action=cls.report['probe']['story_phases'][0]['actions'][153]
        a=cls.action['before_sample']['program_code']['assets'][0]
        raw=school.asset_bytes(a['path'],a['sha256'],a['bytes'])
        cls.code=raw[a['code_offset']:a['code_offset']+a['code_bytes']]
        cls.raw=school.menu.contract.read_source()

    def test_real_opcode30_transient_keeps_raw_samples(self):
        before=copy.deepcopy(self.action);rows=v.check_dispatch(self.action,self.code)
        self.assertEqual([r['index']for r in rows],[5,6]);self.assertEqual(rows[0]['PC'],104)
        self.assertEqual(self.action,before);v.contract(self.raw)
        self.assertTrue(callable(v.adapted(school.menu.ADV)))

    def test_exact_asset_header_and_advanced_state_required(self):
        bad=bytearray(self.code);bad[104]=40
        with self.assertRaises(ValueError):v.check_dispatch(self.action,bytes(bad))
        for offset,value in ((16,0x123456),(28,125),(32,0),(34,40),(36,4)):
            a=copy.deepcopy(self.action);s=a['samples'][7];vm=bytearray.fromhex(s['VM_hex'])
            struct.pack_into('<I'if offset in(16,28)else'<H',vm,offset,value);s['VM_hex']=vm.hex()
            with self.subTest(offset=offset),self.assertRaises(ValueError):v.check_dispatch(a,self.code)

    def test_frozen_parent_and_original_code_tamper_refused(self):
        with patch.object(v,'FROZEN_SHA','0'*64),self.assertRaises(ValueError):v.adapted(school.menu.ADV)
        bad=bytearray(self.raw);bad[0xCEDA2]^=1
        with self.assertRaises(ValueError):v.contract(bytes(bad))

    def test_supplemental_release_uses_actual_bracketed_original_frame(self):
        p=self.report['probe'];a=p['battle_inputs'][1];ready=self.report['lifecycle']['ready']
        workers={(w['pointer'],w['thread_id']):w for w in p['workers']}
        node=a['before_sample']['tasks'][0];key=(node['pointer'],node['thread_id'])
        args=('retreat_confirmation',p,self.raw,ready['game']['pointer'],ready['window']['hwnd'],workers,key)
        result=school.supplemental_release_rows(a,*args)
        self.assertEqual([(r['post_release_index'],r['before_input_index'],r['after_input_index'])for r in result],[(0,564,565)])
        for mutation in ('no_edge','time','foreground','owner','incoherent','before_up'):
            bad=copy.deepcopy(a);row=bad['post_release_snapshots'][0]
            if mutation=='no_edge':
                m=bytearray.fromhex(row['mouse_hex'])
                for offset in(28,32,36,48):struct.pack_into('<I',m,offset,0)
                row['mouse_hex']=m.hex();self.assertEqual(school.supplemental_release_rows(bad,*args),[]);continue
            if mutation=='time':row['elapsed']+=1
            elif mutation=='foreground':bad['input_samples'][565]['foreground_hwnd']+=1
            elif mutation=='owner':row['game']+=4
            elif mutation=='incoherent':
                m=bytearray.fromhex(row['mouse_hex']);struct.pack_into('<I',m,48,0);row['mouse_hex']=m.hex()
            else:bad['input_window']['finished_wall_time_ns']=bad['action']['up_wall_time_ns']-1
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):school.supplemental_release_rows(bad,*args)


if __name__=='__main__':unittest.main()

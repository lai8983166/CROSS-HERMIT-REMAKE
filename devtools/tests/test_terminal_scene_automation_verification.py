import copy
import gzip
import json
from pathlib import Path
import unittest

from devtools import terminal_scene_automation_verification as verify


class RecordedInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=verify.ROOT/'analysis/terminal-scene-auto-v4-20261107.json.gz'
        if not path.exists():raise unittest.SkipTest('retained native diagnostic not available')
        packed=path.read_bytes()
        if verify.owner.sha(packed)!='45dff6219eb8b6069ed3f729d61a4f07d99b0402ff2619a58d5ba4ad3e5b1b44':
            raise AssertionError('native source bytes changed')
        cls.report=json.loads(gzip.decompress(packed))
        cls.raw=(verify.ROOT/'analysis/hermit_game.exe').read_bytes()

    def test_original_query_observes_press_release(self):
        result=verify.verify_input(self.report,self.raw)
        self.assertEqual(result['query_results'],[0,0,0,1,1,0])
        self.assertEqual((result['press_index'],result['advanced_index'],result['release_index']),(3,4,5))
        self.assertFalse(result['full_instruction_causality_proved'])

    def test_explicit_historical_source_archive(self):
        args=(verify.ROOT/'analysis/terminal-scene-auto-v4-20261107.json.gz',
              '45dff6219eb8b6069ed3f729d61a4f07d99b0402ff2619a58d5ba4ad3e5b1b44',
              verify.ROOT/'analysis/terminal-scene-development-implementations-v1-20261107.zip',
              '9dc5de2971ec74d4140e01bc9ad6f27cf73d19ade562ad20f3d8a7d8ff02e2fa')
        result=verify.verify_archived_input(*args)
        self.assertFalse(result['resource_failure_fixed'])
        self.assertFalse(result['unsafe_construction_enabled'])
        with self.assertRaises(ValueError):verify.verify_archived_input(*args[:3],'0'*64)

    def test_actual_input_tamper_rejected(self):
        for mode in ('all_released','no_advance','bad_receipt','wrong_pid','wrong_hwnd',
                     'fake_boundary','short_input','no_action','source_changed','claim_complete',
                     'inactive_VM','wrong_opcode','long_hold','clock_disagreement'):
            r=copy.deepcopy(self.report);a=r['automation']['action'];receipt=a['backend']['receipt']
            if mode=='all_released':
                for row in a['samples']:row['keyboard_hex']=a['samples'][0]['keyboard_hex']
            elif mode=='no_advance':
                for row in a['samples']:row['VM_hex']=a['samples'][0]['VM_hex']
            elif mode=='bad_receipt':receipt['up_results']=[0]
            elif mode=='wrong_pid':receipt['pid']+=1
            elif mode=='wrong_hwnd':a['samples'][3]['foreground_hwnd']+=1
            elif mode=='fake_boundary':a['advanced_index']=3
            elif mode=='short_input':a['samples'][3]['keyboard_hex']='00'
            elif mode=='no_action':r['automation']['action_attempted']=False
            elif mode=='source_changed':a['input_code_identity'][0]['sha256']='0'*64
            elif mode=='claim_complete':r['automation']['complete_battle_exit_accepted']=True
            elif mode in ('inactive_VM','wrong_opcode'):
                row=a['samples'][0];vm=bytearray.fromhex(row['VM_hex'])
                if mode=='inactive_VM':vm[4]=0
                else:vm[32:36]=bytes(4)
                row['VM_hex']=vm.hex()
            elif mode=='long_hold':receipt['up_ns']+=1_000_000_000;receipt['end_ns']+=1_000_000_000
            elif mode=='clock_disagreement':receipt['end_wall_time_ns']+=1_000_000_000
            with self.subTest(mode=mode),self.assertRaises(ValueError):verify.verify_input(r,self.raw)


if __name__=='__main__':unittest.main()

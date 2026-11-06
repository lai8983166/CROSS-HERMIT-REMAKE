import copy
import gzip
import json
import unittest
from devtools import terminal_scene_preflight_verification as verify


class RefusalEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=verify.owner.ROOT/'analysis/terminal-scene-preflight-v2-20261107.json.gz'
        packed=path.read_bytes()
        if verify.owner.sha(packed)!='405f85f53f8f5079265eee6f9a17a0966ceefb20d8fd6599bb13d8590c76fd53':
            raise AssertionError('fixed refusal source changed')
        cls.report=json.loads(gzip.decompress(packed))
        cls.raw=(verify.owner.ROOT/'analysis/hermit_game.exe').read_bytes()

    def test_native_refusal_before_scene_and_input(self):
        result=verify.verify_report(self.report,self.raw)
        self.assertTrue(result['refusal_verified'])
        self.assertEqual(result['original_scene_roots'],0)
        self.assertEqual(result['input_actions'],0)
        self.assertFalse(result['full_battle_exit_accepted'])

    def test_tampering_rejected(self):
        for mode in ('accepted','called_root','input','authorized','missing_task','wrong_owner',
                     'forced_cleanup','leaked_allocation','wrong_write','changed_source','wrong_reason',
                     'null_IAT','wrong_image','overlapping_frees'):
            r=copy.deepcopy(self.report);p=r['probe'];pre=p['construction_preflight']
            if mode=='accepted':r['accepted']=True
            elif mode=='called_root':p['calls']=[{}]
            elif mode=='input':r['automation']['action_attempted']=True
            elif mode=='authorized':pre['authorized']=True
            elif mode=='missing_task':pre['registered_tasks']=[]
            elif mode=='wrong_owner':pre['pid']+=1
            elif mode=='forced_cleanup':r['lifecycle']['lifetime']['forced_termination']=True
            elif mode=='leaked_allocation':p['private_frees'][0]['released']=False
            elif mode=='wrong_write':p['host_private_writes'][0]['pointer']=0x7F4488
            elif mode=='changed_source':p['source_after']['code'][0]['sha256']='0'*64
            elif mode=='wrong_reason':pre['error']='another failure'
            elif mode=='null_IAT':
                for side in ('source_before','source_after'):
                    for row in p[side]['IAT']:row['hex']='00000000'
            elif mode=='wrong_image':p['process_image']='C:/Other/Game.exe'
            elif mode=='overlapping_frees':
                for row in p['private_frees']:row.update(pointer=0x400000,bytes=0x70000000)
            with self.subTest(mode=mode),self.assertRaises(ValueError):verify.verify_report(r,self.raw)


if __name__=='__main__':unittest.main()

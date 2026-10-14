import hashlib,json,unittest
from copy import deepcopy
from tools.school_world_command_verification import REPORT,REPORT_SHA,verify_case,load_verified_checkpoint
from tools.school_world_command import source_contract


class NativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(REPORT.read_bytes())

    def test_three_actual_complete_loops_and_scope(self):
        self.assertEqual(hashlib.sha256(REPORT.read_bytes()).hexdigest(),REPORT_SHA)
        self.assertEqual(self.data['source_contract'],source_contract())
        self.assertEqual([c['name'] for c in self.data['cases']],['initial','student9_waiting','fifth_class'])
        for c in self.data['cases']:self.assertTrue(verify_case(c))
        self.assertEqual([len(c['actual_suffix']['updated_indices']) for c in self.data['cases']],[38,37,37])
        self.assertEqual([len(c['actual_suffix']['active_indices']) for c in self.data['cases']],[14,13,13])
        for k in ('world_tick_completed','original_opening_completed','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_full_work_fog_tail_and_native_loop_corruption_refuse(self):
        original=self.data['cases'][0]
        for i in range(9):
            bad=deepcopy(original);r=bad['actual_suffix']['after'][i];r['hex']=r['hex'][:-2]+('00' if r['hex'][-2:]!='00' else '01')
            with self.assertRaises(ValueError):verify_case(bad)
        for k in ('tested_indices','updated_indices','native_vision_calls','native_clears'):
            bad=deepcopy(original);bad['actual_suffix'][k].pop()
            with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(original);bad['actual_suffix']['action_animation_AI_executed']=True
        with self.assertRaises(ValueError):verify_case(bad)

    def test_probe_input_stack_and_parent_provenance_refuse(self):
        original=self.data['cases'][0]
        bad=deepcopy(original);bad['declared_probes']['selection'][0]['declared_indices'].pop()
        with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(original);bad['declared_probes']['selection'][0]['restoration']['stack_after_sha256']='0'*64
        with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(original);bad['parent_checkpoint']['sha256']='0'*64
        with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(original);bad['actual_suffix']['pending']['return_va']='0x46b508'
        with self.assertRaises(ValueError):verify_case(bad)

    def test_private_checkpoint_preunpickle_identity_and_full_memory(self):
        for c in self.data['cases']:
            payload,cp=load_verified_checkpoint(c['name']);self.assertEqual(payload['pending_eip'],0x490FC0);self.assertFalse(cp['runtime_or_original_save'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial')


if __name__=='__main__':unittest.main()

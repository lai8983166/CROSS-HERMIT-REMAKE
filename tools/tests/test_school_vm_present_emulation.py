import gzip,hashlib,json,unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from tools.school_vm_present import SOURCE,SCRIPT,source_contract
from tools.school_vm_present_verification import REPORTS,SHAS,PARENT,verify_case,load_verified_checkpoint
from tools.school_world_life_codec import pack,unpack

class Checks:
    @classmethod
    def setUpClass(cls):cls.data=json.loads(gzip.decompress(REPORTS[cls.phase].read_bytes()))

    def test_three_original_cases_full_calls_state_CPU_and_scope(self):
        self.assertEqual(hashlib.sha256(REPORTS[self.phase].read_bytes()).hexdigest(),SHAS[self.phase]);self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual(len(self.data['cases']),3)
        for c in self.data['cases']:self.assertTrue(verify_case(c,self.phase))
        self.assertTrue(self.data['normal_first_opcode_executed'])
        for k in ('VM_returned','full_outer_frame_executed','live_rendering','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_every_owned_region_and_complete_packet_corruption_refused(self):
        for i in range(len(unpack(self.data['cases'][0]['actual'])['after'])):
            c=deepcopy(self.data['cases'][0]);a=unpack(c['actual']);r=a['after'][i];r['hex']=r['hex'][:-2]+('01' if r['hex'][-2:]=='00' else '00');c['actual']=pack(a)
            with self.assertRaises(ValueError):verify_case(c,self.phase)
        if self.phase!='command':
            for offset in range(128):
                c=deepcopy(self.data['cases'][0]);a=unpack(c['actual']);b=bytearray.fromhex(a['packet']['hex']);b[offset]^=1;a['packet']['hex']=b.hex();c['actual']=pack(a)
                with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_source_calls_inputs_SEH_boundary_and_authority_mutations_refused(self):
        c=deepcopy(self.data['cases'][0]);c['prior_checkpoint']['sha256']='0'*64
        with self.assertRaises(ValueError):verify_case(c,self.phase)
        changes=[lambda a:a['calls'].pop(),lambda a:a['calls'][1].update(sp=0),lambda a:a['calls'][0].update(receiver=0),lambda a:a['inputs']['texture_record'].update(hex='00'*84),lambda a:a['pending'].update(first_instruction_executed=True),lambda a:a['pending']['args'].pop(),lambda a:a['CPU'].update(EAX=9),lambda a:a.update(owned_bodies_stubbed=True),lambda a:a.update(VM_returned=True),lambda a:a.update(render_completed=True),lambda a:a['retained_ranges'].pop(),lambda a:a.update(seh_record='00'*12)]
        if self.phase=='command':changes.append(lambda a:a['commands'][0].update(opcode=0))
        if self.phase=='draw':changes.append(lambda a:a['returns'][0].update(eax=0))
        for mutate in changes:
            c=deepcopy(self.data['cases'][0]);a=unpack(c['actual']);mutate(a);c['actual']=pack(a)
            with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_private_full_memory_CPU_args_and_fresh_SHA_before_unpickle(self):
        for c in self.data['cases']:
            payload,cp=load_verified_checkpoint(c['name'],self.phase);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial',self.phase)
        original=Path.read_bytes
        for identity in (SOURCE,SCRIPT,PARENT,REPORTS[self.phase],Path.cwd()/self.data['cases'][0]['continuation_checkpoint']['path']):
            def changed(path):return b'{}' if path==identity else original(path)
            with patch.object(Path,'read_bytes',changed),patch('tools.school_vm_present_verification.pickle.loads') as unpickle:
                with self.assertRaises(ValueError):load_verified_checkpoint('initial',self.phase)
                self.assertEqual(unpickle.call_count,0)

class CommandTests(Checks,unittest.TestCase):phase='command'
class PacketTests(Checks,unittest.TestCase):phase='packet'
class DrawTests(Checks,unittest.TestCase):phase='draw'

if __name__=='__main__':unittest.main()

import gzip,hashlib,json,unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from tools.school_vm_draw import SOURCE,SCRIPT,REGIONS,PHASES,BASE_SP,VM,layout,source_contract
from tools.school_vm_draw_verification import REPORTS,SHAS,PARENT,verify_case,load_verified_checkpoint,envelope
from tools.school_world_life_codec import pack,unpack

class Checks:
    @classmethod
    def setUpClass(cls):cls.data=json.loads(gzip.decompress(REPORTS[cls.phase].read_bytes()))

    def test_three_original_cases_whole_state_calls_returns_and_scope(self):
        self.assertEqual(hashlib.sha256(REPORTS[self.phase].read_bytes()).hexdigest(),SHAS[self.phase]);envelope(self.data,self.phase)
        for c in self.data['cases']:self.assertEqual(len(verify_case(c,self.phase)),59)
        self.assertEqual(self.data['VM_returned'],self.phase!='cleanup');self.assertEqual(self.data['selected_task_returned'],self.phase=='task')

    def test_each_owned_region_and_cleanup_packet_byte_corruption_refused(self):
        for i in range(len(REGIONS)):
            c=deepcopy(self.data['cases'][0]);a=unpack(c['actual']);r=a['after'][i];v=bytearray.fromhex(r['hex']);v[-1]^=1;r['hex']=v.hex();c['actual']=pack(a)
            with self.assertRaises(ValueError):verify_case(c,self.phase)
        if self.phase=='cleanup':
            for offset in range(128):
                c=deepcopy(self.data['cases'][0]);a=unpack(c['actual']);v=bytearray.fromhex(a['packet']['hex']);v[offset]^=1;a['packet']['hex']=v.hex();c['actual']=pack(a)
                with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_calls_guards_returns_CPU_scope_and_retention_mutations_refused(self):
        changes=[lambda a:a['calls'].pop(),lambda a:a['calls'][0].update(sp=0),lambda a:a['calls'][0].update(receiver=0),lambda a:a['calls'][0]['args'].append(1),lambda a:a['inputs'].update(driver='patched'),lambda a:a['CPU'].update(EAX=2),lambda a:a['returns'][0].update(eax=9),lambda a:a['visited'].clear(),lambda a:a.update(owned_bodies_stubbed=True),lambda a:a.update(GPU_executed=True),lambda a:a.update(full_outer_frame_executed=True),lambda a:a.update(persistent_write_authority=True),lambda a:a.update(VM_return=0),lambda a:a.update(task_phase=3),lambda a:a.update(script_PC=16),lambda a:a['retained_ranges'].pop()]
        for mutate in changes:
            c=deepcopy(self.data['cases'][0]);a=unpack(c['actual']);mutate(a);c['actual']=pack(a)
            with self.assertRaises(ValueError):verify_case(c,self.phase)
        for key in ('GPU_executed','full_outer_frame_executed','persistent_write_authority','VM_returned','selected_task_returned'):
            r=deepcopy(self.data);r[key]=not r[key]
            with self.assertRaises(ValueError):envelope(r,self.phase)
        c=deepcopy(self.data['cases'][0]);c['prior_checkpoint']['sha256']='0'*64
        with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_private_full_memory_CPU_caller_and_fresh_SHA_before_unpickle(self):
        for c in self.data['cases']:
            payload,cp=load_verified_checkpoint(c['name'],self.phase);self.assertEqual(payload['pending_eip'],int(cp['pending_eip'],16))
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial',self.phase)
        original=Path.read_bytes
        for identity in (SOURCE,SCRIPT,PARENT,REPORTS[self.phase],Path.cwd()/self.data['cases'][0]['continuation_checkpoint']['path']):
            def changed(path):return b'{}' if path==identity else original(path)
            with patch.object(Path,'read_bytes',changed),patch('tools.school_vm_draw_verification.pickle.loads') as unpickle:
                with self.assertRaises(ValueError):load_verified_checkpoint('initial',self.phase)
                self.assertEqual(unpickle.call_count,0)
        from tools.school_vm_draw_verification import read_memory as original_read
        # Alter reads after a valid file hash: every owned buffer, retained coverage,
        # and caller stack must still be checked independently of serialized identity.
        targets=[a for a,n in REGIONS]+[BASE_SP-4]
        if self.phase=='cleanup':targets.extend([layout()['packet'],layout()['vm'],layout()['vm']-20])
        retained_row=unpack(self.data['cases'][0]['actual'])['retained_ranges'][0];targets.append(retained_row['pointer'])
        payload,_=load_verified_checkpoint('initial',self.phase)
        for target in targets:
            def changed_memory(p,at,n):
                b=original_read(p,at,n)
                return bytes([b[0]^1])+b[1:] if at==target else b
            with patch('tools.school_vm_draw_verification.pickle.loads',return_value=payload),patch('tools.school_vm_draw_verification.read_memory',side_effect=changed_memory):
                with self.assertRaises(ValueError):load_verified_checkpoint('initial',self.phase)
        bad=dict(payload);cpu=payload['cpu']
        class WrongCPU:
            def reg_read(self,reg):return cpu.reg_read(reg)^1
        bad['cpu']=WrongCPU()
        with patch('tools.school_vm_draw_verification.pickle.loads',return_value=bad):
            with self.assertRaises(ValueError):load_verified_checkpoint('initial',self.phase)

class CleanupTests(Checks,unittest.TestCase):phase='cleanup'
class VMTests(Checks,unittest.TestCase):phase='vm'
class TaskTests(Checks,unittest.TestCase):phase='task'

if __name__=='__main__':unittest.main()

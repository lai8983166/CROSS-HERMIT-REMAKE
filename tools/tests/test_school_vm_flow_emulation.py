import gzip,hashlib,json,unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from tools.school_vm_flow import SOURCE,SCRIPT,REGIONS,PHASES,PREVIOUS,VM,BASE_SP,layout
from tools.school_vm_flow_verification import REPORTS,SHAS,PARENT,verify_case,load_verified_checkpoint,verify_payload,envelope
from tools.school_world_life_codec import pack,unpack

class Checks:
    @classmethod
    def setUpClass(cls):cls.data=json.loads(gzip.decompress(REPORTS[cls.phase].read_bytes()));cls.actual=unpack(cls.data['cases'][0]['actual'])

    def mutated(self,mutate):
        c=deepcopy(self.data['cases'][0]);a=deepcopy(self.actual);mutate(a);c['actual']=pack(a)
        with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_three_cases_every_intermediate_call_return_state_CPU_and_checkpoint(self):
        self.assertEqual(hashlib.sha256(REPORTS[self.phase].read_bytes()).hexdigest(),SHAS[self.phase]);envelope(self.data,self.phase)
        for c in self.data['cases']:
            self.assertEqual(len(verify_case(c,self.phase)),61);payload,cp=load_verified_checkpoint(c['name'],self.phase);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
        for key in ('live_OS_observed','GPU_executed','full_outer_frame_executed','persistent_write_authority'):
            r=deepcopy(self.data);r[key]=True
            with self.assertRaises(ValueError):envelope(r,self.phase)

    def test_owned_buffers_packet_native_arguments_returns_adapters_and_waits_refused(self):
        for i in range(len(REGIONS)):
            def change(a):
                r=a['steps'][0]['after'][i];v=bytearray.fromhex(r['hex']);v[-1]^=1;r['hex']=v.hex()
            self.mutated(change)
        offsets=range(128) if self.phase=='branch' else (0,127)
        for offset in offsets:
            def change(a):
                r=a['steps'][0]['packet'];v=bytearray.fromhex(r['hex']);v[offset]^=1;r['hex']=v.hex()
            self.mutated(change)
        changes=[lambda a:a['steps'].pop(),lambda a:a['steps'][0]['calls'].pop(),lambda a:a['steps'][0]['calls'][0].update(sp=0),lambda a:a['steps'][0]['calls'][4].update(receiver=0),lambda a:a['steps'][0]['calls'][0]['args'].append(1),lambda a:a['steps'][0]['returns'][0].update(eax=9),lambda a:a['steps'][0]['adapters'][0].update(args=[1]),lambda a:a['steps'][0]['adapters'][1].update(result=1),lambda a:a['steps'][0]['declarations'][0].update(original_outer_callsite_observed=True),lambda a:a['steps'][0]['reset_CPU'].update(EAX=9),lambda a:a['steps'][-1]['CPU'].update(ESP=0),lambda a:a['steps'][0].update(owned_bodies_stubbed=True),lambda a:a['steps'][0]['visited'].clear(),lambda a:a['steps'][-1].update(wait=9),lambda a:a.update(declared_task_calls=0),lambda a:a['retained_ranges'].pop(),lambda a:a.update(GPU_executed=True),lambda a:a['inputs'].update(driver='live_OS_frame'),lambda a:a['after'][0].update(hex='00'*400)]
        if self.phase=='fade_finish':changes.extend([lambda a:a['steps'][29].update(fade_accumulator=38912),lambda a:a['steps'][58].update(fade_completed=False),lambda a:a['steps'][59].update(wait=4)])
        for change in changes:self.mutated(change)
        c=deepcopy(self.data['cases'][0]);c['prior_checkpoint']['sha256']='0'*64
        with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_fresh_report_source_file_SHA_and_private_memory_checks(self):
        # Warm all parent caches first; fresh identity gates must still run before
        # unpickling even when independent byte projections are already cached.
        payload,cp=load_verified_checkpoint('initial',self.phase)
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial',self.phase)
        identities=[SOURCE,SCRIPT,PARENT,REPORTS[self.phase],Path.cwd()/cp['path']]
        if self.phase=='fade_finish':identities.extend(REPORTS[p] for p in PHASES if p!=self.phase)
        original=Path.read_bytes
        for identity in identities:
            def changed(path):return b'{}' if path==identity else original(path)
            with patch.object(Path,'read_bytes',changed),patch('tools.school_vm_flow_verification.pickle.loads') as unpickle:
                with self.assertRaises(ValueError):load_verified_checkpoint('initial',self.phase)
                self.assertEqual(unpickle.call_count,0)
        if self.phase=='fade_finish':
            from tools.school_vm_flow_verification import read_memory as original_read
            c=self.data['cases'][0];after=verify_case(c,self.phase);targets=[a for a,n in REGIONS]+[BASE_SP-4,layout()['packet'],self.actual['retained_ranges'][0]['pointer']]
            for target in targets:
                def changed_memory(p,at,n):
                    b=original_read(p,at,n);return bytes([b[0]^1])+b[1:] if at==target else b
                with patch('tools.school_vm_flow_verification.read_memory',side_effect=changed_memory):
                    with self.assertRaises(ValueError):verify_payload(payload,c,self.phase,after)
            bad=dict(payload);cpu=payload['cpu']
            class WrongCPU:
                def reg_read(self,reg):return cpu.reg_read(reg)^1
            bad['cpu']=WrongCPU()
            with self.assertRaises(ValueError):verify_payload(bad,c,self.phase,after)

class BranchTests(Checks,unittest.TestCase):phase='branch'
class AssignTests(Checks,unittest.TestCase):phase='assign'
class GlobalTests(Checks,unittest.TestCase):phase='globals'
class SlotTests(Checks,unittest.TestCase):phase='slots'
class PoseTests(Checks,unittest.TestCase):phase='poses'
class FadeStartTests(Checks,unittest.TestCase):phase='fade_start'
class FadeFinishTests(Checks,unittest.TestCase):phase='fade_finish'

if __name__=='__main__':unittest.main()

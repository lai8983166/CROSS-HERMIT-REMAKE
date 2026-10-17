import gzip,hashlib,json,unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from tools.school_vm_graphics import SOURCE,SCRIPT,REGIONS,PHASES,VM,BASE_SP,layout,LAYER,FRAME,MANAGER,positions
from tools.school_vm_graphics_verification import REPORTS,SHAS,PARENT,verify_case,load_verified_checkpoint,verify_payload,envelope
from tools.school_world_life_codec import pack,unpack

class Checks:
 @classmethod
 def setUpClass(cls):cls.data=json.loads(gzip.decompress(REPORTS[cls.phase].read_bytes()));cls.actual=unpack(cls.data['cases'][0]['actual'])

 def mutated(self,mutate):
  c=deepcopy(self.data['cases'][0]);a=deepcopy(self.actual);mutate(a);c['actual']=pack(a)
  with self.assertRaises(ValueError):verify_case(c,self.phase)

 def test_three_cases_source_packets_ABI_returns_CPU_and_private_checkpoints(self):
  self.assertEqual(hashlib.sha256(REPORTS[self.phase].read_bytes()).hexdigest(),SHAS[self.phase]);envelope(self.data,self.phase)
  for c in self.data['cases']:
   self.assertEqual(len(verify_case(c,self.phase)),61);payload,cp=load_verified_checkpoint(c['name'],self.phase);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
  for key in ('queue_executed','clipping_returned','GPU_executed','dialogue_executed','VM_returned','task_returned','full_outer_frame_executed','persistent_write_authority'):
   r=deepcopy(self.data);r[key]=True
   with self.assertRaises(ValueError):envelope(r,self.phase)

 def test_owned_memory_every_sprite_byte_SEH_arguments_and_read_boundary_refused(self):
  for i in range(len(REGIONS)):
   def change(a):
    r=a['after'][i];v=bytearray.fromhex(r['hex']);v[-1]^=1;r['hex']=v.hex()
   self.mutated(change)
  if self.phase=='graphics':
   for i in range(4):
    for offset in range(128):
     def change(a):
      r=a['packets'][i];v=bytearray.fromhex(r['hex']);v[offset]^=1;r['hex']=v.hex()
     self.mutated(change)
   self.mutated(lambda a:a['packets'][0].update(seh=0));self.mutated(lambda a:a['packet'].update(hex='00'*128));self.mutated(lambda a:a['calls'][1]['args'].__setitem__(2,0))
  changes=[lambda a:a['calls'].pop(),lambda a:a['calls'][0].update(sp=0),lambda a:a['calls'][0].update(receiver=0),lambda a:a['calls'][0]['args'].append(1),lambda a:a['CPU'].update(ESP=0),lambda a:a['visited'].clear(),lambda a:a['visited'].append(0x40E2D0),lambda a:a.update(owned_bodies_stubbed=True),lambda a:a.update(new_root_calls=1),lambda a:a['platform_adapters'].append(dict(name='fake_clipping')),lambda a:a.update(VM_returned=True),lambda a:a.update(queue_executed=True),lambda a:a['retained_ranges'].pop(),lambda a:a['inputs'].update(driver='new_root'),lambda a:a['inputs'].update(manager_owner=1),lambda a:a['inputs']['frame_table'].update(hex='00'*50)]
  if self.phase!='owner_read':changes.append(lambda a:a['returns'][0].update(eax=9))
  else:changes.extend([lambda a:a['returns'].append(dict(eax=0)),lambda a:a['blocked_read'].update(effective_address=0),lambda a:a['blocked_read'].update(target_read=True),lambda a:a['blocked_read'].update(instruction_executed=True),lambda a:a['CPU'].update(ECX=1)])
  if self.phase=='rectangle':changes.extend([lambda a:a['pending'].update(first_instruction_executed=True),lambda a:a['pending']['args'].__setitem__(0,0),lambda a:a['calls'][0]['args'].__setitem__(1,45)])
  for change in changes:self.mutated(change)
  c=deepcopy(self.data['cases'][0]);c['prior_checkpoint']['sha256']='0'*64
  with self.assertRaises(ValueError):verify_case(c,self.phase)

 def test_fresh_identities_before_unpickle_private_memory_stack_and_CPU_refused(self):
  payload,cp=load_verified_checkpoint('initial',self.phase)
  with self.assertRaises(ValueError):load_verified_checkpoint('../initial',self.phase)
  identities=[SOURCE,SCRIPT,PARENT,REPORTS[self.phase],Path.cwd()/cp['path']]
  if self.phase=='owner_read':identities.extend(REPORTS[p] for p in PHASES if p!=self.phase)
  original=Path.read_bytes
  for identity in identities:
   def changed(path):return b'{}' if path==identity else original(path)
   with patch.object(Path,'read_bytes',changed),patch('tools.school_vm_graphics_verification.pickle.loads') as unpickle:
    with self.assertRaises(ValueError):load_verified_checkpoint('initial',self.phase)
    self.assertEqual(unpickle.call_count,0)
  from tools.school_vm_graphics_verification import read_memory as original_read
  c=self.data['cases'][0];after=verify_case(c,self.phase);v=layout()['vm'];targets=[a for a,n in REGIONS]+[BASE_SP-4,v,v-4,v-8,v-20,v-132,v-136,v-140,MANAGER,FRAME,self.actual['retained_ranges'][0]['pointer']]
  if self.phase=='graphics':targets.extend([positions()['packet'],v-264])
  else:targets.extend([v-276,v-280,v-284,v-272,v-384])
  if self.phase=='owner_read':targets.extend([v-388,v-392])
  for target in targets:
   def changed_memory(p,at,n):
    b=original_read(p,at,n);return bytes([b[0]^1])+b[1:] if at==target else b
   with patch('tools.school_vm_graphics_verification.read_memory',side_effect=changed_memory):
    with self.assertRaises(ValueError):verify_payload(payload,c,self.phase,after)
  bad=dict(payload);cpu=payload['cpu']
  class WrongCPU:
   def reg_read(self,reg):return cpu.reg_read(reg)^1
  bad['cpu']=WrongCPU()
  with self.assertRaises(ValueError):verify_payload(bad,c,self.phase,after)

class GraphicsTests(Checks,unittest.TestCase):phase='graphics'
class RectangleTests(Checks,unittest.TestCase):phase='rectangle'
class OwnerReadTests(Checks,unittest.TestCase):phase='owner_read'

if __name__=='__main__':unittest.main()

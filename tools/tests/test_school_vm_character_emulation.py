import gzip,hashlib,json,unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from tools.school_vm_character import SOURCE,SCRIPT,REGIONS,PHASES,VM,BASE_SP,layout,LAYER,TABLE
from tools.school_vm_character_verification import REPORTS,SHAS,PARENT,verify_case,load_verified_checkpoint,verify_payload,envelope
from tools.school_world_life_codec import pack,unpack

class Checks:
 @classmethod
 def setUpClass(cls):cls.data=json.loads(gzip.decompress(REPORTS[cls.phase].read_bytes()));cls.actual=unpack(cls.data['cases'][0]['actual'])

 def mutated(self,mutate):
  c=deepcopy(self.data['cases'][0]);a=deepcopy(self.actual);mutate(a);c['actual']=pack(a)
  with self.assertRaises(ValueError):verify_case(c,self.phase)

 def test_three_cases_full_calls_returns_CPU_and_private_checkpoints(self):
  self.assertEqual(hashlib.sha256(REPORTS[self.phase].read_bytes()).hexdigest(),SHAS[self.phase]);envelope(self.data,self.phase)
  for c in self.data['cases']:
   self.assertEqual(len(verify_case(c,self.phase)),61);payload,cp=load_verified_checkpoint(c['name'],self.phase);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
  for key in ('GPU_executed','graphics_list_executed','dialogue_executed','VM_returned','task_returned','full_outer_frame_executed','persistent_write_authority'):
   r=deepcopy(self.data);r[key]=True
   with self.assertRaises(ValueError):envelope(r,self.phase)

 def test_owned_memory_packet_full_arguments_returns_and_boundaries_refused(self):
  for i in range(len(REGIONS)):
   def change(a):
    r=a['after'][i];v=bytearray.fromhex(r['hex']);v[-1]^=1;r['hex']=v.hex()
   self.mutated(change)
  if self.phase=='overlay':
   for offset in range(128):
    def change(a):
     r=a['packet'];v=bytearray.fromhex(r['hex']);v[offset]^=1;r['hex']=v.hex()
    self.mutated(change)
  changes=[lambda a:a['calls'].pop(),lambda a:a['calls'][0].update(sp=0),lambda a:a['calls'][0].update(receiver=0),lambda a:a['calls'][0]['args'].append(1),lambda a:a['returns'][0].update(eax=9),lambda a:a['CPU'].update(ESP=0),lambda a:a['visited'].clear(),lambda a:a['visited'].append(0x4CA604),lambda a:a.update(owned_bodies_stubbed=True),lambda a:a.update(new_root_calls=1),lambda a:a['platform_adapters'].append(dict(name='new_OS_response')),lambda a:a.update(VM_returned=True),lambda a:a.update(task_returned=True),lambda a:a.update(graphics_list_executed=True),lambda a:a['retained_ranges'].pop(),lambda a:a['inputs'].update(driver='declared_new_root'),lambda a:a['inputs']['template'].update(hex='00'*38),lambda a:a['inputs'].update(script_pointer=1)]
  if self.phase in ('template','layer_entry'):changes.extend([lambda a:a['pending'].update(first_instruction_executed=True),lambda a:a['pending']['args'].__setitem__(0,0),lambda a:a['pending'].update(sp=0)])
  if self.phase=='template':changes.extend([lambda a:a['calls'][2]['args'].__setitem__(2,0xFFFFFFFF),lambda a:a['returns'][-1].update(ecx=LAYER)])
  if self.phase=='layer_entry':changes.append(lambda a:a['calls'][-2]['args'].__setitem__(0,0))
  for change in changes:self.mutated(change)
  c=deepcopy(self.data['cases'][0]);c['prior_checkpoint']['sha256']='0'*64
  with self.assertRaises(ValueError):verify_case(c,self.phase)

 def test_fresh_identities_before_unpickle_and_private_memory_stack_CPU_refused(self):
  payload,cp=load_verified_checkpoint('initial',self.phase)
  with self.assertRaises(ValueError):load_verified_checkpoint('../initial',self.phase)
  identities=[SOURCE,SCRIPT,PARENT,REPORTS[self.phase],Path.cwd()/cp['path']]
  if self.phase=='layer_entry':identities.extend(REPORTS[p] for p in PHASES if p!=self.phase)
  original=Path.read_bytes
  for identity in identities:
   def changed(path):return b'{}' if path==identity else original(path)
   with patch.object(Path,'read_bytes',changed),patch('tools.school_vm_character_verification.pickle.loads') as unpickle:
    with self.assertRaises(ValueError):load_verified_checkpoint('initial',self.phase)
    self.assertEqual(unpickle.call_count,0)
  if self.phase in ('template','overlay','layer_entry'):
   from tools.school_vm_character_verification import read_memory as original_read
   c=self.data['cases'][0];after=verify_case(c,self.phase);targets=[a for a,n in REGIONS]+[BASE_SP-4,layout()['vm'],layout()['vm']-4,layout()['vm']-8,layout()['vm']-20,self.actual['retained_ranges'][0]['pointer']]
   if self.actual['pending']:targets.append(self.actual['pending']['sp'])
   if self.phase=='template':targets.extend([layout()['vm']-144,layout()['vm']-148,layout()['vm']-152])
   elif self.phase=='layer_entry':targets.extend([layout()['vm']-132,layout()['vm']-136,layout()['vm']-140])
   else:targets.append(layout()['packet'])
   for target in targets:
    def changed_memory(p,at,n):
     b=original_read(p,at,n);return bytes([b[0]^1])+b[1:] if at==target else b
    with patch('tools.school_vm_character_verification.read_memory',side_effect=changed_memory):
     with self.assertRaises(ValueError):verify_payload(payload,c,self.phase,after)
  bad=dict(payload);cpu=payload['cpu']
  class WrongCPU:
   def reg_read(self,reg):return cpu.reg_read(reg)^1
  bad['cpu']=WrongCPU()
  with self.assertRaises(ValueError):verify_payload(bad,self.data['cases'][0],self.phase,verify_case(self.data['cases'][0],self.phase))

class TemplateTests(Checks,unittest.TestCase):phase='template'
class HandlerTests(Checks,unittest.TestCase):phase='handler'
class OverlayTests(Checks,unittest.TestCase):phase='overlay'
class LayerEntryTests(Checks,unittest.TestCase):phase='layer_entry'

if __name__=='__main__':unittest.main()

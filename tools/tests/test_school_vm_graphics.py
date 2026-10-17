import struct,unittest
from copy import deepcopy
from tools.tests import test_school_vm_character as fixtures
from tools.school_vm_graphics import *

class SourceTests(unittest.TestCase):
 def seed(self):
  x,b=fixtures.SourceTests().seed()
  from tools.school_vm_character import PHASES as phases,project as parent
  for phase in phases:b=parent(phase,x,b)['after']
  x=dict(x,driver='continuous_original_graphics_VM_task',frame_table=source_contract()['frame_table'],manager_owner=0);return x,b

 def test_original_table_packets_and_initializer_source(self):
  s=source_contract();self.assertEqual(len(s['functions']),91);self.assertEqual(len(s['frame_table']['rows']),4);self.assertEqual(s['renderer_prerequisite']['initializer'],'0x40d970');self.assertEqual(s['renderer_prerequisite']['original_caller'],'0x413500')
  x,b=self.seed();a=project('graphics',x,b)
  for p,row in zip(a['packets'],s['frame_table']['rows']):
   v=bytes.fromhex(p['hex']);self.assertEqual(len(v),128);self.assertEqual(struct.unpack_from('<2i',v,0x68),(256+row[0],568+row[1]));self.assertEqual(struct.unpack_from('<4H',v,0x78),(row[2],row[3],row[2]+row[4],row[3]+row[5]));self.assertEqual(v[0x67],0);self.assertEqual(struct.unpack_from('<H',v,0x76)[0],66)

 def test_all_phases_preserve_owned_memory_and_real_read_boundary(self):
  x,b=self.seed()
  for phase in PHASES:
   a=project(phase,x,b);self.assertEqual(a['after'],b);self.assertFalse(a['queue_executed']);self.assertFalse(a['VM_returned']);self.assertFalse(a['task_returned']);b=a['after']
  self.assertEqual(a['CPU']['ECX'],0);self.assertEqual(a['blocked_read']['effective_address'],0xB278);self.assertFalse(a['blocked_read']['target_read'])

 def test_every_original_E8_full_argument_and_nested_stack_rule(self):
  x,b=self.seed();r=SOURCE.read_bytes()
  for phase in PHASES:
   for va,ret,receiver,args in call_protocol(phase,x,b):
    op=r[ret-BASE-5:ret-BASE];self.assertEqual(op[0],0xE8);self.assertEqual(ret+struct.unpack_from('<i',op,1)[0],va)
  self.assertEqual(len(call_protocol('graphics',x,b)),89);self.assertEqual(call_protocol('rectangle',x,b)[0][3],[LAYER&0xFFFF0000,0xFFFF002D,204]);self.assertEqual(positions()['packet'],positions()['sprite']-4-0x90)

 def test_invalid_captured_owner_gate_table_or_state_refused(self):
  x,b=self.seed()
  for key,val in (('driver','patched_root'),('manager_owner',TASK),('frame_table',{}),('script_sha256','0'*64)):
   bad=deepcopy(x);bad[key]=val
   with self.assertRaises(ValueError):project('graphics',bad,b)
  for pointer,offset in ((TASK+0xB28E,0),(VM,0x1C),(VM,LAYER-VM+6)):
   bad=deepcopy(b);r=next(r for r in bad if r['pointer']==pointer);v=bytearray.fromhex(r['hex']);v[offset]^=1;r['hex']=v.hex()
   with self.assertRaises(ValueError):project('graphics',x,bad)

if __name__=='__main__':unittest.main()

import struct,unittest
from copy import deepcopy
from tools.tests import test_school_vm_panel as fixtures
from tools.school_vm_character import *

class SourceTests(unittest.TestCase):
 def seed(self):
  x,b=fixtures.SourceTests().seed()
  from tools.school_vm_panel import PHASES as phases,KINDS,project_step
  for phase in phases:
   for kind in KINDS[phase]:b=project_step(kind,x,b)['after']
  x=dict(x,driver='continuous_original_character_VM_task',template=source_contract()['template']);return x,b

 def test_source_template_literal_and_type3_dispatch(self):
  s=source_contract();self.assertEqual(len(s['functions']),88);self.assertEqual(s['decoded_operands'],[4,0xFFFFFFF,0xFFFFFFF]);self.assertEqual(s['template']['layer'],7);self.assertEqual(s['template']['bytes'],38)

 def test_complete_template_layout_show_and_active_boundary(self):
  x,b=self.seed()
  for phase in PHASES:
   p=project(phase,x,b);v=data(p['after'])[VM];o=LAYER-VM
   self.assertFalse(p['VM_returned']);self.assertFalse(p['task_returned']);self.assertFalse(p['graphics_list_executed'])
   self.assertEqual(struct.unpack_from('<3I',v,0x9250),(4,0xFFFFFFF,0xFFFFFFF))
   if phase=='template':self.assertEqual(struct.unpack_from('<H',v,o+2)[0],1);self.assertEqual(p['pending']['va'],'0x4cc0f0')
   else:self.assertEqual(struct.unpack_from('<H',v,o+2)[0],3);self.assertEqual(struct.unpack_from('<H',v,TEXT-VM)[0],24);self.assertEqual(struct.unpack_from('<H',v,TEXT-VM+6)[0],12)
   b=p['after']
  self.assertEqual((p['PC'],p['wait']),(224,1));self.assertEqual(p['pending']['args'],[(LAYER&0xFFFF0000)|256,(LAYER&0xFFFF0000)|568,1,0,66])

 def test_complete_original_E8_arguments_and_retained_ABI(self):
  x,b=self.seed();raw=SOURCE.read_bytes()
  for phase in PHASES:
   for va,ret,receiver,args in call_protocol(phase,x,b):
    op=raw[ret-BASE-5:ret-BASE];self.assertEqual(op[0],0xE8);self.assertEqual(ret+struct.unpack_from('<i',op,1)[0],va)
   b=project(phase,x,b)['after']
  interpolate=next(c for c in call_protocol('layer_entry',x,b) if c[0]==0x4CD850);self.assertEqual(interpolate[3],[LAYER&0xFFFF0000,45,255])

 def test_invalid_scope_source_or_owned_state_refused(self):
  x,b=self.seed()
  for key,value in (('driver','new_root'),('template',{}),('script_sha256','0'*64)):
   bad=deepcopy(x);bad[key]=value
   with self.assertRaises(ValueError):project('template',bad,b)
  for pointer,offset in ((TASK+0xB28E,0),(VM,0x1C),(VM,0x1CC),(VM,LAYER-VM+2)):
   bad=deepcopy(b);r=next(r for r in bad if r['pointer']==pointer);v=bytearray.fromhex(r['hex']);v[offset]^=1;r['hex']=v.hex()
   with self.assertRaises(ValueError):project('template',x,bad)
  with self.assertRaises(ValueError):project('unknown',x,b)

if __name__=='__main__':unittest.main()

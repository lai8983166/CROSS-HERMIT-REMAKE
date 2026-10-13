import unittest
from copy import deepcopy
from tools.school_character_animation_verification import *
from tools.school_character_animation_emulation import SchoolCharacterAnimationEmulator

class AnimationLiveTests(unittest.TestCase):
 def test_three_actual_parents_every_update_and_four_resources(self):
  data=fixture();self.assertEqual(len(data['cases']),3)
  for c in data['cases']:
   r=compare_animation(c);self.assertEqual(r['readiness_calls'],154);self.assertEqual(r['four_texture_bytes'],[16384,32768,8192,262144])
 def test_tampered_animation_state_draw_predicate_texture_or_scope_refused(self):
  for kind in ('state','draw','predicate','pixel','return','visited','scope','cleanup','order'):
   c=deepcopy(fixture()['cases'][0]);p=c['character_animation']
   if kind=='state':
    m=memory_regions(p['steps'][60]['after']);struct.pack_into('<H',m[VM],NODE-VM+34,2);p['steps'][60]['after']=regions(m)
   elif kind=='draw':p['steps'][31]['presentation'][16]['args'][2]+=1
   elif kind=='predicate':p['steps'][76]['predicates'][0]['return_value']=1
   elif kind=='pixel':p['actual_readbacks'][3]['sha256']='0'*64
   elif kind=='return':p['steps'][77]['natural_return']['sp']+=4
   elif kind=='visited':p['visited'].remove(0x4CD120)
   elif kind=='scope':p['GPU_draw_or_present_executed']=True
   elif kind=='cleanup':c['first_live_text']['COM_process_cleanup']['texture_releases'][0]['count']=1
   else:p['steps'][1],p['steps'][2]=p['steps'][2],p['steps'][1]
   with self.subTest(kind=kind):
    with self.assertRaises(ValueError):compare_animation(c)
 def test_write_guard_refuses_resource_pixels_previous_text_and_input(self):
  e=SchoolCharacterAnimationEmulator();e.animation_loading=True;e.animation_allowed=[(NODE+4,NODE+6)]
  e._write_hook(e.uc,0,NODE+4,2,2,None)
  for at in (NODE+0x60,OBJECT7+0x28,VM+0x92C0,TASK+0x1990):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,1,0,None)

if __name__=='__main__':unittest.main()

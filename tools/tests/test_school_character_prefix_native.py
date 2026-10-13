"""Frozen actual character prefix, complete source comparison and refusal cases."""
import unittest
from copy import deepcopy
from functools import lru_cache
from tools.school_character_prefix_verification import *

EVIDENCE=ROOT/'analysis/school-character-prefix-v1-20261013.json'
EVIDENCE_SHA256='66606d60959a28b49f5b469cad13b55d87f6d3298fc91b081cd11f56c2a1c2f5'

@lru_cache(maxsize=1)
def fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('character immutable native identity')
 return json.loads(raw)

class NativeCharacterPrefixTests(unittest.TestCase):
 def test_three_actual_cases_full_regions_stack_pixels_and_cleanup(self):
  d=fixture();self.assertEqual(len(d['cases']),3)
  for c in d['cases']:
   r=compare_case(c);self.assertEqual(r['layer'],5);self.assertEqual(r['texture_bytes'],[16384,32768])
   self.assertEqual(c['provenance']['helper_sha256'],d['bridge_build']['helper_sha256'])
   self.assertTrue(c['first_live_text']['process_exited'])
 def test_corrupted_full_state_stack_resource_and_scope_refused(self):
  for kind in ('state','stack','name_arg','pixel','scope','visit','parent'):
   c=deepcopy(fixture()['cases'][0]);p=c['character_prefix']
   if kind=='state':
    m=memory_regions(p['after']);m[VM][NODE_OFFSET+0xC]^=1;p['after']=regions(m)
   elif kind=='stack':p['pending_font']['frames']['name']+=4
   elif kind=='name_arg':p['pending_font']['name_argument']=4
   elif kind=='pixel':p['actual_readbacks'][1]['sha256']='0'*64
   elif kind=='scope':p['image_load_executed']=True
   elif kind=='visit':p['visited'].remove(0x4CA770)
   else:p['before']=p['after']
   with self.subTest(kind=kind):
    with self.assertRaises(ValueError):compare_case(c)

if __name__=='__main__':unittest.main()

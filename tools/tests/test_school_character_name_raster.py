"""Pinned real name raster and meaningful source/API corruption refusal."""
import unittest
from copy import deepcopy
from functools import lru_cache
from tools.school_character_name_verification import *

EVIDENCE=ROOT/'analysis/school-character-name-raster-v2-20261013.json'
SHA256='390720ac62b729046ccbb721e2af677287197092ec77939ef5aedd059cffd760'

@lru_cache(maxsize=1)
def fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SHA256:raise ValueError('name pinned actual raster identity')
 return json.loads(raw)

class NameRasterTests(unittest.TestCase):
 def test_three_actual_rasters_full_parent_state_stack_and_cleanup(self):
  d=fixture();self.assertEqual(len(d['cases']),3)
  for c in d['cases']:
   r=compare_raster(c);self.assertEqual(r['prior_texture_bytes'],[16384,32768]);self.assertFalse(r['name_texture_created'])
 def test_bad_gdi_stack_text_surface_or_scope_refused(self):
  for kind in ('api','stack','text','surface','memory','scope','cleanup'):
   c=deepcopy(fixture()['cases'][0]);p=c['name_raster']
   if kind=='api':p['font_api'][19]['args'][1]+=1
   elif kind=='stack':p['entry']['sp']+=4
   elif kind=='text':p['text_hex']='00'
   elif kind=='surface':p['raster']['sha256']='0'*64
   elif kind=='memory':
    m=memory_regions(p['after']);m[VM][TEXTURE_OFFSET+0x40]^=1;p['after']=regions(m)
   elif kind=='scope':p['name_texture_created']=True
   else:c['first_live_text']['remaining_GDI_cleanup']['dcs']=2
   with self.subTest(kind=kind):
    with self.assertRaises(ValueError):compare_raster(c)

if __name__=='__main__':unittest.main()

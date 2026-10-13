"""Pinned fourth real texture, all source rows, return and corruption refusal."""
import unittest
from copy import deepcopy
from functools import lru_cache
from tools.school_character_image_verification import *
from tools.school_character_image_live_emulation import SchoolCharacterImageLiveEmulator

EVIDENCE=ROOT/'analysis/school-character-image-live-v3-20261013.json'
SHA='725d85f5f757ebda961c8b55dbcdf15b645f5a341a1012c0e856e2ed5e9b1908'

@lru_cache(maxsize=1)
def fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SHA:raise ValueError('pinned actual image upload identity')
 return json.loads(raw)

class ImageLiveTests(unittest.TestCase):
 def test_three_actual_four_texture_cases_and_source_return(self):
  d=fixture();self.assertEqual(len(d['cases']),3)
  for c in d['cases']:
   r=compare_live(c);self.assertEqual(r['image_bytes'],262144);self.assertEqual(r['original_row_copies'],512);self.assertTrue(r['image_loader_returned'])
   self.assertEqual(memory_regions(c['image_live']['after'])[VM][0x92C0],1)
 def test_bad_pixels_rows_com_state_free_seh_return_or_scope_refused(self):
  for kind in ('pixel','row','COM','flag','record','free','SEH','return','scope','cleanup'):
   c=deepcopy(fixture()['cases'][0]);p=c['image_live']
   if kind=='pixel':p['actual_readback']['sha256']='0'*64
   elif kind=='row':p['rows'][511]['args'][1]-=512
   elif kind=='COM':p['COM_calls'][0]['args'][1]=512
   elif kind=='flag':
    m=memory_regions(p['after']);m[VM][0x92C0]=0;p['after']=regions(m)
   elif kind=='record':p['record_hex']='01'+p['record_hex'][2:]
   elif kind=='free':p['allocations'][0]['freed']=False
   elif kind=='SEH':p['SEH_after_hex']='01000000'
   elif kind=='return':p['natural_return']['sp']+=4
   elif kind=='scope':p['animation_executed']=True
   else:c['first_live_text']['COM_process_cleanup']['texture_releases'][0]['count']=1
   with self.subTest(kind=kind):
    with self.assertRaises(ValueError):compare_live(c)
 def test_finite_ownership_guard_refuses_old_textures_and_loaded_flags(self):
  e=SchoolCharacterImageLiveEmulator();e.image_loading=True;e.image_allowed=[(RECORD,RECORD+84)]
  e._write_hook(e.uc,0,RECORD+0x34,4,25,None)
  for address in (VM+0x92C0,VM+0x430+7*0xAB8+0x28,ARRAY-4):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,address,4,1,None)

if __name__=='__main__':unittest.main()

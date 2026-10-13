"""Actual Windows file lifecycle and pinned source image-prefix comparison."""
import unittest
from copy import deepcopy
from functools import lru_cache
from tools.school_character_image_verification import *
from tools.school_character_image_file import WindowsImageFile

EVIDENCE=ROOT/'analysis/school-character-image-prefix-v2-20261013.json'
SHA='fc03ed4a812e339ba57da1ed52121892dd1ba68f5cff594507114aa132136749'

@lru_cache(maxsize=1)
def fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SHA:raise ValueError('pinned image prefix identity')
 return json.loads(raw)

class ImagePrefixTests(unittest.TestCase):
 def test_actual_windows_file_and_foreign_handle_refusal(self):
  files=WindowsImageFile()
  try:
   for flags in ([0,1,0,3,1,0],[0x80000000,1,0,3,1,1]):
    with self.assertRaises(ValueError):files.open(flags)
   h=files.open([0x80000000,1,0,3,1,0]);self.assertEqual(files.size(h),262168)
   self.assertEqual(hashlib.sha256(files.read(h,262168)).hexdigest(),RESOURCE_SHA)
   for op in (lambda:files.size(0),lambda:files.read(h,262167),lambda:files.release(0)):
    with self.assertRaises(ValueError):op()
   files.release(h)
   with self.assertRaises(ValueError):files.release(h)
  finally:self.assertEqual(files.close(),{'actual_handles_closed':1,'open_handles':0,'all_owned_files_closed':True})
 def test_three_actual_prefixes_full_state_constructor_and_file_calls(self):
  d=fixture();self.assertEqual(len(d['cases']),3)
  for c in d['cases']:
   r=compare_prefix(c);self.assertEqual(r['loaded_bytes'],262168);self.assertEqual(r['prior_texture_bytes'],[16384,32768,8192])
 def test_file_stack_array_buffer_or_scope_corruption_refused(self):
  for kind in ('file','stack','array','buffer','scope','allocation'):
   c=deepcopy(fixture()['cases'][0]);p=c['image_prefix']
   if kind=='file':p['file_calls'][3]['args'][2]-=1
   elif kind=='stack':p['pending_texture']['sp']+=4
   elif kind=='array':p['array_hex']='00'+p['array_hex'][2:]
   elif kind=='buffer':p['file_buffer_sha256']='0'*64
   elif kind=='scope':p['image_texture_created']=True
   else:p['allocations'][0]['freed']=True
   with self.subTest(kind=kind):
    with self.assertRaises(ValueError):compare_prefix(c)

if __name__=='__main__':unittest.main()

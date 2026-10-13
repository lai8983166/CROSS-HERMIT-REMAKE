"""Actual third texture, original source arguments and corruption refusal."""
import unittest
from copy import deepcopy
from functools import lru_cache
from tools.school_character_name_verification import *
from tools.school_character_name_texture_emulation import SchoolCharacterNameTextureEmulator

EVIDENCE=ROOT/'analysis/school-character-name-texture-v3-20261013.json'
SHA256='de5d82eda44a0d3e773140c400bdacefd2fb4c06459fbc778b7de7ccf305ec56'

@lru_cache(maxsize=1)
def fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SHA256:raise ValueError('name pinned actual texture identity')
 return json.loads(raw)

class NameTextureTests(unittest.TestCase):
 def test_three_actual_owned_name_textures_and_natural_image_entry(self):
  d=fixture();self.assertEqual(len(d['cases']),3)
  for c in d['cases']:
   r=compare_texture(c);self.assertEqual(r['texture_size'],[128,32]);self.assertEqual(r['third_texture_bytes'],8192)
   self.assertEqual(r['image_slot'],32);self.assertEqual(c['name_texture']['pending_image']['args'][1],32)
   vm=memory_regions(c['name_texture']['after'])[VM]
   self.assertEqual(struct.unpack_from('<I',vm,NODE_OFFSET+0x5C)[0],c['name_raster']['font_api'][0]['result'])
   self.assertEqual(c['first_live_text']['remaining_GDI_cleanup']['fonts'],0)
 def test_bad_full_state_com_lock_pixels_path_stack_cleanup_or_scope_refused(self):
  for kind in ('state','COM','lock','pixel','path','stack','concat','cleanup','scope'):
   c=deepcopy(fixture()['cases'][0]);p=c['name_texture']
   if kind=='state':
    m=memory_regions(p['after']);m[VM][NODE_OFFSET+0x34]^=1;p['after']=regions(m)
   elif kind=='COM':p['COM_calls'][0]['args'][1]=256
   elif kind=='lock':p['lock']['host_bits']+=4
   elif kind=='pixel':p['actual_readback']['sha256']='0'*64
   elif kind=='path':p['path']='data\\adv\\bin\\sc005.bin'
   elif kind=='stack':p['pending_image']['args'][1]=0x620020
   elif kind=='concat':p['path_calls'][0]['source']+=1
   elif kind=='cleanup':c['first_live_text']['COM_process_cleanup']['texture_releases'][0]['count']=1
   else:p['image_loader_executed']=True
   with self.subTest(kind=kind):
    with self.assertRaises(ValueError):compare_texture(c)
 def test_finite_writes_protect_old_textures_and_scene_state(self):
  e=SchoolCharacterNameTextureEmulator();e.name_texture_loading=True;e.name_texture_allowed=[(NODE+0x34,NODE+0x36)]
  e._write_hook(e.uc,0,NODE+0x34,2,4,None)
  for address in (VM+0x430+7*0xAB8+0x28,NODE+2,0x1001990):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,address,2,1,None)
 def test_missing_natural_live_texture_and_bad_ownership_refused(self):
  e=SchoolCharacterNameTextureEmulator()
  with self.assertRaises(RuntimeError):e.complete_name_texture({}, {})
  p=fixture()['cases'][0]['name_raster']
  for texture,device in ((0,1),(1,0),(True,1),(1,-1)):
   with self.assertRaises(ValueError):expected_complete(p,texture,device,49152)

if __name__=='__main__':unittest.main()

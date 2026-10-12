import json,struct,subprocess,tempfile,unittest
from copy import deepcopy
from tools.school_d3d8_platform import *

class D3D8PlatformTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.helper=ROOT/'.venv-audit/school-d3d8-test-helper.exe';cls.build=build_helper(cls.helper)

 def test_three_real_texture_roundtrips_source_inputs_and_cleanup(self):
  report=json.loads((ROOT/'analysis/school-d3d8-platform-v1-20261012.json').read_text('utf-8'))
  self.assertEqual(report['build']['source_sha256'],sha(CS.read_bytes()));self.assertEqual(report['build']['compiler_sha256'],sha(COMPILER.read_bytes()))
  self.assertEqual(report['build']['helper_machine'],0x14C);self.assertEqual(len(report['cases']),3)
  for c,r in zip(native_fixture()['cases'],report['cases']):
   self.assertEqual(c['name'],r['name']);raw,size=original_upload(c);self.assertEqual(size,[256,32]);validate_result(r['platform'],raw,size)
   self.assertFalse(r['platform']['original_GPU_executed']);self.assertFalse(r['platform']['native_renderer_patched'])

 def test_live_x86_complete_pixel_pattern_and_release(self):
  raw=struct.pack('<8H',0,0x8000,0xFFFF,0xFC00,0x83E0,0x801F,0x8421,1)
  p=run_probe(self.helper,raw,[4,2]);self.assertEqual(bytes.fromhex(p['readback_hex']),raw);self.assertEqual(p['pointer_bytes'],4)
  self.assertEqual(p['cleanup'],{'texture_release_count':0,'device_release_count':0,'factory_release_count':0,'window_destroyed':True,'all_owned_resources_released':True})

 def test_malformed_input_refused_before_platform_and_evidence_tampering(self):
  for raw,size in ((b'',[4,2]),(bytes(8),[True,2]),(bytes(12),[3,2]),(bytes(2),[1,257])):
   with self.assertRaises(ValueError):validate_input(raw,size)
  with tempfile.TemporaryDirectory(prefix='d3d8-refusal-',dir=ROOT/'.venv-audit') as folder:
   folder=Path(folder);input_file=folder/'input.bin';input_file.write_bytes(bytes(16))
   for i,args in enumerate(([],[str(input_file),'3','2',str(folder/'wrong-size.json')],[str(input_file),'4','4',str(folder/'wrong-buffer.json')])):
    p=subprocess.run([str(self.helper),*args],capture_output=True,timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
    r=json.loads(p.stdout);self.assertEqual(p.returncode,2);self.assertFalse(r['platform_calls_started']);self.assertTrue(r['cleanup']['all_owned_resources_released'])
   output=folder/'exists.json';output.write_bytes(b'unchanged')
   p=subprocess.run([str(self.helper),str(input_file),'4','2',str(output)],capture_output=True,timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
   self.assertEqual(p.returncode,2);self.assertEqual(output.read_bytes(),b'unchanged');self.assertFalse(json.loads(p.stdout)['platform_calls_started'])
  report=json.loads((ROOT/'analysis/school-d3d8-platform-v1-20261012.json').read_text('utf-8'));raw,size=original_upload(native_fixture()['cases'][0]);original=report['cases'][0]['platform']
  for key,value in (('readback_sha256','0'*64),('window_visible',True),('native_renderer_patched',True),('device_pointer','0x00000000')):
   bad=deepcopy(original);bad[key]=value
   with self.assertRaises(ValueError):validate_result(bad,raw,size)
  bad=deepcopy(original);bad['calls'][-2]['flags']=0
  with self.assertRaises(ValueError):validate_result(bad,raw,size)

if __name__=='__main__':unittest.main()

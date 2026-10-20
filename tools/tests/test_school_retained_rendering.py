import struct,sys,unittest,copy
from tools.school_retained_rendering import AddressSpace,MappedPlatform,owner_configuration,OLD_OWNER,TASK

class FakeNative:
 def __init__(self,result):self.hello={};self.result=result;self.calls=[]
 def request(self,op,**kw):self.calls.append((op,kw));return self.result

class MarshalTests(unittest.TestCase):
 def test_addresses_are_typed_stable_and_separate_from_retained_maps(self):
  a=AddressSpace();p=a.guest('device',0x1001000);q=a.guest('GDI',0x1001000)
  self.assertNotEqual(p,q);self.assertEqual(a.guest('device',0x1001000),p)
  self.assertGreaterEqual(p,0x40000000);self.assertEqual(a.native('device',p),0x1001000)
  with self.assertRaises(ValueError):a.native('GDI',p)
  self.assertEqual(a.native('device',0),0)

 def test_full_interface_and_lock_metadata_map_without_changing_hresult_or_handles(self):
  a=AddressSpace();native=dict(hr=0,result=0x80000001,device=dict(pointer=0x1100000,vtable=0x1200000,methods={'72':0x65001000}),pitch=512,bits=0x2001000,locked_hex=struct.pack('<2I',512,0x2001000).hex())
  r=a.result('device',native)
  self.assertEqual(r['result'],native['result']);self.assertEqual(r['hr'],0)
  self.assertEqual(struct.unpack('<2I',bytes.fromhex(r['locked_hex'])),(512,r['bits']))
  self.assertEqual(a.native('device',r['device']['methods']['72']),0x65001000)
  self.assertEqual(native['device']['pointer'],0x1100000)

 def test_only_pointer_typed_parameters_are_reverse_translated(self):
  a=AddressSpace();device=a.guest('device',123);tex=a.guest('device',456);raw=FakeNative(dict(hr=0));b=MappedPlatform(raw,a,'device')
  b.request('render_call',pointer=device,slot=61,args=[0,tex],buffers=[])
  self.assertEqual(raw.calls[-1][1]['args'],[0,456]);self.assertEqual(raw.calls[-1][1]['pointer'],123)
  b.request('render_call',pointer=device,slot=50,args=[8,tex],buffers=[])
  self.assertEqual(raw.calls[-1][1]['args'],[8,tex])
  b.request('font_state',pointer=device,method='texture',args=[0,tex])
  self.assertEqual(raw.calls[-1][1]['args'],[0,456])

 def test_owner_configuration_is_scoped_and_restored_on_failure(self):
  modules=[m for n,m in list(sys.modules.items()) if n.startswith('tools.school_') and getattr(m,'OWNER',None)==OLD_OWNER]
  self.assertTrue(modules)
  with self.assertRaises(RuntimeError):
   with owner_configuration() as changed:
    self.assertTrue(changed);self.assertTrue(all(m.OWNER==TASK for m in modules));raise RuntimeError('intentional scope exit')
  self.assertTrue(all(m.OWNER==OLD_OWNER for m in modules))

class ReconstructionProofTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  from tools.school_retained_rendering_verification import read_report
  cls.record=read_report('analysis/school-retained-render-reconstruction-v1-20261021.json.gz')
 def test_original_reconstruction_and_unsubstituted_continuation(self):
  from tools.school_retained_rendering_verification import verify
  result=verify(self.record)
  self.assertEqual(result['full_parent_maps'],42);self.assertFalse(result['R2_complete']);self.assertFalse(result['GPU_output_accepted'])
 def test_rejects_changed_source_identity(self):
  from tools.school_retained_rendering_verification import verify
  r=copy.deepcopy(self.record);r['source_sha256']='0'*64
  with self.assertRaisesRegex(ValueError,'source identity'):verify(r)
 def test_rejects_undeclared_fresh_input(self):
  from tools.school_retained_rendering_verification import verify
  r=copy.deepcopy(self.record);r['initialization']['before_first_original_instruction']=False
  with self.assertRaisesRegex(ValueError,'fresh source-backed'):verify(r)
 def test_rejects_fabricated_native_reply(self):
  from tools.school_retained_rendering_verification import verify
  r=copy.deepcopy(self.record);r['device_proxy_trace'][0]['native_result']['hr']=-1
  with self.assertRaisesRegex(ValueError,'real native request/reply'):verify(r)

if __name__=='__main__':unittest.main()

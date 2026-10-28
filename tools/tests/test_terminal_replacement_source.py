"""Small source-recorder guards; no native execution or large report loading."""
import copy,gzip,json,struct,tempfile,types,unittest
from pathlib import Path
from tools import terminal_replacement_emulation as e

class TerminalReplacementSourceTests(unittest.TestCase):
 def test_unchanged_guest_code_and_host_write_guards(self):
  self.assertIs(e.ReplacementMachine.source_code,e.parent.FollowupMachine.source_code)
  self.assertIs(e.ReplacementMachine.put,e.parent.FollowupMachine.put)
  self.assertIs(e.ALLOWED,e.parent.ALLOWED);self.assertIs(e.RANGES,e.parent.RANGES)
  self.assertEqual(e.EXTRA_RANGES,())
 def test_exact_two_script_boundaries(self):
  for name,first,texts,pcs,ready,final,scene in (('neutral_running',198,[3,4],[210,216],226,230,76),('timeout_before_combat',194,[5,6],[206,212],222,226,77)):
   b=e.branch(name);self.assertEqual((b['first_PC'],b['text_indices'],b['text_PCs'],b['ready_PC'],b['final_PC'],b['scene_capture']),(first,texts,pcs,ready,final,scene));self.assertEqual((b['configuration'],b['layer']),(4,7))
 def test_unknown_branch_rejected(self):
  for n in ('fake','neutral_running ','timeout'):
   with self.subTest(name=n),self.assertRaises(ValueError):e.branch(n)
 def test_recorder_namespace_changes_only_code_names(self):
  for target,source in (('nx_mark','fu_mark'),('nx_capture','fu_capture'),('nx_segment','fu_segment'),('nx_font','fu_font'),('_nx_gpu_api','gpu_api'),('nx_actual_root','fu_actual_root')):
   old=getattr(e.parent.FollowupMachine,source);new=getattr(e.ReplacementMachine,target)
   self.assertIs(new.__globals__,old.__globals__);self.assertIs(new.__closure__,old.__closure__)
   self.assertEqual(new.__code__.replace(co_names=old.__code__.co_names),old.__code__)
   self.assertFalse(any(n.startswith(('fu_','followup_')) for n in new.__code__.co_names))
 def test_unknown_raster_rejected_before_native_access(self):
  m=e.ReplacementMachine.__new__(e.ReplacementMachine)
  for p in (0,e.parent.NAME_RASTER,e.parent.TEXT_RASTER,e.RASTERS[0]+4):
   with self.subTest(pointer=p),self.assertRaises(ValueError):m.nx_set_raster(p)
 def test_separate_new_DIB_addresses(self):self.assertEqual(e.RASTERS,(0x3EA00000,0x3EB00000))
 def test_unknown_or_overlapping_resource_rejected(self):
  m=e.ReplacementMachine.__new__(e.ReplacementMachine);m.nx_current=None
  with self.assertRaises(ValueError):m.nx_prepare('fake','x',0)
  m.nx_current={}
  with self.assertRaises(ValueError):m.nx_prepare('text','x',0)
 def test_release_synchronizes_parent_creation_only(self):
  a=dict(generation=7,texture=dict(pointer=1234),alive=True);b=dict(generation=8,texture=dict(pointer=4567),alive=True)
  m=types.SimpleNamespace(replacement_ready=True,nx_gpu=[],fu_resources=[a,b],fu_live={1234:a,4567:b})
  m._nx_gpu_api=lambda at:m.nx_gpu.append(dict(op='release',generation=7,wire_index=81,phase='forward'))
  e.ReplacementMachine.gpu_api(m,0)
  self.assertFalse(a['alive']);self.assertTrue(b['alive']);self.assertEqual(m.fu_live,{4567:b});self.assertEqual(a['release_wire_index'],81)
 def test_new_generation_pointer_reuse_does_not_retire_parent_again(self):
  a=dict(generation=7,texture=dict(pointer=1234),alive=False);before=copy.deepcopy(a)
  m=types.SimpleNamespace(replacement_ready=True,nx_gpu=[],fu_resources=[a],fu_live={})
  m._nx_gpu_api=lambda at:m.nx_gpu.append(dict(op='release',generation=99,wire_index=120,phase='cleanup'))
  e.ReplacementMachine.gpu_api(m,0);self.assertEqual(a,before);self.assertEqual(m.fu_live,{})
 def test_parent_wrong_live_generation_rejected(self):
  a=dict(generation=7,texture=dict(pointer=1234),alive=True)
  m=types.SimpleNamespace(replacement_ready=True,nx_gpu=[],fu_resources=[a],fu_live={1234:dict(a)})
  m._nx_gpu_api=lambda at:m.nx_gpu.append(dict(op='release',generation=7,wire_index=81,phase='forward'))
  with self.assertRaises(ValueError):e.ReplacementMachine.gpu_api(m,0)
 def test_no_cleanup_history_replacement(self):
  self.assertIn('super',e.ReplacementMachine.run.__code__.co_names)
  self.assertIn('run',e.ReplacementMachine.run.__code__.co_names)
  self.assertNotIn('fu_cleanup',e.ReplacementMachine.fu_actual_root.__code__.co_names)
 def test_frozen_clock_provider(self):
  self.assertEqual(e.fixed_parent_times.__code__.co_names,('parent','fixed_parent_times'))
 @staticmethod
 def prefix_space():
  s=e.overlay.AddressSpace();s.next=0x64001000
  s.result('overlay',dict(texture=dict(pointer=0x10000,vtable=0x20000,methods={'8':0x20100,'56':0x20200,'64':0x20300,'68':0x20400})))
  s.result('overlay',dict(bits=0x30000));return s
 @classmethod
 def marshal_fixture(cls,reuse,lifetime):
  # Declared bridge-only inputs, never claimed native captures or GPU success.
  s=cls.prefix_space();prefix=copy.deepcopy(s.ledger());m=types.SimpleNamespace(space=s,nx_current=None);projection=e.ReplacementProjection(m) if lifetime else s;out=[];native=[]
  for i in range(2):
   m.nx_current=dict(kind='text',record_index=i,record=e.TEXTURE+i*e.STRIDE,projection_domain=e.projection_domain(i))
   p=(0x10000 if reuse else 0x11000) if i==0 else 0x12000
   bits=(0x30000 if reuse else 0x31000) if i==0 else 0x32000
   create=dict(hr=0,texture=dict(pointer=p,vtable=0x20000,methods={'8':0x20100,'56':0x20200,'64':0x20300,'68':0x20400}))
   lock=dict(hr=0,pitch=8,bits=bits,locked_hex=struct.pack('<II',8,bits).hex(),hex='a500ff8001020304')
   native.append((copy.deepcopy(create),copy.deepcopy(lock)));out.append((projection.result('overlay',create),projection.result('overlay',lock)))
   cls().assertEqual((create,lock),native[-1])
  return out,s.ledger(),prefix,native
 def test_whole_process_mapper_depends_on_retired_native_reuse(self):
  reused=self.marshal_fixture(True,False);fresh=self.marshal_fixture(False,False)
  self.assertNotEqual(reused[0],fresh[0]);self.assertNotEqual(len(reused[1]),len(fresh[1]))
 def test_each_creation_domain_eliminates_retired_native_reuse_dependency(self):
  reused=self.marshal_fixture(True,True);fresh=self.marshal_fixture(False,True)
  self.assertEqual(reused[0],fresh[0]);self.assertEqual(len(reused[1]),len(fresh[1]))
  for result in (reused,fresh):
   self.assertEqual(result[1][:len(result[2])],result[2])
   self.assertEqual([sum(r['domain']==d for r in result[1]) for d in e.PROJECTION_DOMAINS],[7,7])
 def test_lifetime_projection_keeps_every_surface_byte(self):
  out,ledger,prefix,native=self.marshal_fixture(True,True)
  for (_,lock),(_,original) in zip(out,native):
   self.assertEqual(lock['hex'],original['hex']);self.assertEqual(bytes.fromhex(lock['locked_hex'])[:4],bytes.fromhex(original['locked_hex'])[:4]);self.assertEqual(struct.unpack('<II',bytes.fromhex(lock['locked_hex'])),(lock['pitch'],lock['bits']))
 def test_two_new_domains_have_distinct_live_guest_interfaces_and_surfaces(self):
  out,*_=self.marshal_fixture(True,True)
  self.assertNotEqual(out[0][0]['texture']['pointer'],out[1][0]['texture']['pointer'])
  self.assertNotEqual(out[0][1]['bits'],out[1][1]['bits'])
  self.assertNotEqual(out[0][0]['texture']['vtable'],out[1][0]['texture']['vtable'])
 def test_finite_creation_domain_before_access(self):
  for index in (-1,2,True,'0',None):
   with self.subTest(index=index),self.assertRaises(ValueError):e.projection_domain(index)
 def test_wrong_creation_domain_or_record_rejected(self):
  m=types.SimpleNamespace(space=self.prefix_space(),nx_current=dict(kind='text',record_index=0,record=e.TEXTURE,projection_domain=e.PROJECTION_DOMAINS[1]));p=e.ReplacementProjection(m)
  with self.assertRaises(ValueError):p.result('overlay',dict(bits=0x40000))
  m.nx_current.update(record=e.TEXTURE+e.STRIDE,projection_domain=e.PROJECTION_DOMAINS[0])
  with self.assertRaises(ValueError):p.result('overlay',dict(bits=0x40000))
 def test_namespace_capacity_stays_below_existing_GDI(self):
  self.assertEqual(e.PREFIX_NEXT_MAX+2*7*e.PROJECTION_STRIDE,e.REPLACEMENT_NEXT_MAX)
  self.assertEqual(e.REPLACEMENT_NEXT_MAX,0x66601000);self.assertLess(e.REPLACEMENT_NEXT_MAX,e.GDI_GUEST_START)
  s=self.prefix_space();s.next=e.PREFIX_NEXT_MAX+e.PROJECTION_STRIDE
  with self.assertRaises(ValueError):e.ReplacementProjection(types.SimpleNamespace(space=s))
 def test_CLI_gzip_changes_only_compression_not_JSON_bytes(self):
  data=dict(text='原始資料',raw='a500ff80',values=[1,2])
  with tempfile.TemporaryDirectory() as directory:
   p=Path(directory)/'source.json.gz';e.save_source(p,data);raw=p.read_bytes()
   self.assertEqual(gzip.decompress(raw),(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n').encode());self.assertEqual(raw[4:8],bytes(4))
   with self.assertRaises(ValueError):e.save_source(p,dict(changed=True))
   self.assertEqual(p.read_bytes(),raw)

if __name__=='__main__':unittest.main()

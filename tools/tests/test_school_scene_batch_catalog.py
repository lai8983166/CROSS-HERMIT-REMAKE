from copy import deepcopy
import json,struct,unittest
from tools.school_scene_batch_catalog import (
 source_catalog,native_fixture,expected_prefix,expected_binding,expected_constructor,animation_inputs,expected_record,ROOT)
from tools.school_scene_batch_emulation import batch_resource
from tools.dxanim_lib import DxAnimError
from tools.school_current_units_catalog import expected_progress,source_catalog as current_rules

class SceneBatchSourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.rules,cls.fixture=source_catalog(),native_fixture()

 def compare_batch(self,batch):
  r=self.rules;owned={};cache=None;counter=None
  for u in batch['units']:
   ordinal=u['ordinal'];actual_record=u['record_derivation']
   record=expected_record(r['records']['templates'][ordinal],rules=r['records'])
   self.assertEqual(record['record_hex'],actual_record['record_hex']);self.assertEqual(record['record_hex'],u['before_record_hex'])
   if cache is not None:self.assertEqual(u['cache_before_hex'],cache);self.assertEqual(u['counter_before'],counter)
   p=expected_prefix(u['before_record_hex'],ordinal,u['cache_before_hex'],u['counter_before'],u['renderer'],u['controller'],
    u['classification_selector'],u['relation_hex'],r['prefix'],controller_hex=owned.get(u['controller'],{}).get('controller_hex'))
   for k,v in (('work_hex','prefix_work_hex'),('record_hex','prefix_record_hex'),('cache_hex','cache_after_hex'),('counter','counter_after')):
    self.assertEqual(p[k],u[v],(ordinal,k))
   self.assertEqual(p['cache_slot'],u['cache_slot']);cache=p['cache_hex'];counter=p['counter']
   a=u['animation']
   if a:
    self.assertEqual(u['resource_request']['args'],p['resource_args'])
    self.assertEqual(p['controller_hex'],a['before_controller_hex'])
    binding=expected_binding(a['before_controller_hex'],a['request']['buffer_pointer'],a['metadata_pointer'],a['allocations'][2]['pointer'],
     a['texture_table'],job=u['job'],variant=u['variant'],rules=r['bindings'][str(u['job'])])
    for k in ('controller_hex','metadata_hex'):self.assertEqual(a[k],binding[k],(ordinal,k))
    self.assertEqual(a['binding']['args'],binding['binding_args'])
    self.assertEqual(a['file_release']['sha256_at_release'],binding['source_sha256_at_release'])
    uploads=[x for x in a['boundaries'] if x['kind']=='pixel_upload']
    self.assertEqual(len(uploads),binding['texture_count']);self.assertEqual(len(a['entries']),binding['texture_count'])
    for actual,x,upload in zip(a['entries'],binding['texture_entries'],uploads):
     for k in x:
      if k!='upload_args':self.assertEqual(actual[k],x[k],(ordinal,x['index'],k))
     self.assertEqual(upload['args'],x['upload_args'])
    owned[u['controller']]=binding
   binding=owned[u['controller']]
   t=u['tail'];e=expected_constructor(t['before_work_hex'],t['before_record_hex'],t['work_pointer'],u['controller'],
    int.from_bytes(bytes.fromhex(binding['controller_hex'])[:4],'little'),t['before_cm_hex'],
    selector=t['relation_selector'],relation_hex=t['relation_hex'],rules=r['constructors'][str(u['job'])])
   for k in ('work_hex','record_hex','shared_hex','cm_hex','cm_sha256','constructor_coordinates'):
    self.assertEqual(t[k],e[k],(ordinal,k))
   if u['cache_hit']:
    self.assertIsNone(p['resource_args']);self.assertIsNone(u['resource_request'])
    self.assertIsNone(a);self.assertIsNone(u['allocation']);self.assertEqual(u['file_events'],[])
    self.assertEqual(u['cache_before_hex'],cache);self.assertEqual(u['counter_before'],counter)
  return owned

 def test_actual_record_prefix_cache_binding_and_complete_constructor_bytes(self):
  for c in self.fixture['cases'][:3]:self.assertEqual(len(self.compare_batch(c['scene_batch'])),2)

 def test_original_progress_and_visible_initial_descriptors(self):
  progress_rules=current_rules()['progress']
  for c in self.fixture['cases'][:3]:
   progress=c['scene_batch']['progress'];self.assertEqual(len(progress),8)
   for i,p in enumerate(progress):
    self.assertEqual(p['ordinal_completed'],i+1)
    self.assertEqual(expected_progress(p['before_hex'],1,{'progress':progress_rules})['after_hex'],p['after_hex'])
    if i:self.assertEqual(progress[i-1]['after_hex'],p['before_hex'])
  for job in ('393','383'):
   initial=self.rules['constructors'][job]['initial_program']
   self.assertEqual(initial['first_instruction']['opcode'],0)
   self.assertTrue(initial['visible_layers'])
   count=len(self.rules['bindings'][job]['animation']['texture_entries'])
   self.assertTrue(all(0<=l['frame']<count for l in initial['visible_layers']))

 def test_cached_controller_and_complete_cell_boundaries_refuse_invalid_ownership(self):
  c=self.fixture['cases'][0];u=c['scene_batch']['units'][2];r=self.rules['prefix']
  args=[u['before_record_hex'],u['ordinal'],u['cache_before_hex'],u['counter_before'],u['renderer'],u['controller'],u['classification_selector'],u['relation_hex']]
  for invalid in (None,'00','zz','00'*84):
   with self.assertRaises(ValueError):expected_prefix(*args,rules=r,controller_hex=invalid)
  s=c['scene_batch']['units'][0];t=s['tail'];a=s['animation'];rules=self.rules['constructors']['393']
  args=[t['before_work_hex'],t['before_record_hex'],t['work_pointer'],s['controller'],a['metadata_pointer'],t['before_cm_hex']]
  x,y=t['constructor_coordinates'];cm=bytearray.fromhex(t['before_cm_hex']);cm[2*(y*64+x)+1]=255;args[-1]=cm.hex()
  e=expected_constructor(*args,selector=t['relation_selector'],relation_hex=t['relation_hex'],rules=rules)
  self.assertEqual(bytes.fromhex(e['cm_hex'])[2*(y*64+x)+1],0)
  record=bytearray.fromhex(t['before_record_hex']);record[155]=64;args[1]=record.hex()
  with self.assertRaises(ValueError):expected_constructor(*args,rules=rules)

 def test_malformed_archives_and_unsupported_resources_refuse(self):
  for job,variant in ((393,0),(383,1)):
   raw,_,_=batch_resource(job,variant);a=self.rules['bindings'][str(job)]['animation'];bad=bytearray(raw)
   bad[a['sections'][8]['offset']]=2
   for data in (None,'bad',b'',raw[:20],raw[:-1],bytes(bad)):
    with self.assertRaises((ValueError,DxAnimError)):animation_inputs(data)
  for job,variant in ((387,0),(393,1),(383,0),(True,1),(383,True)):
   with self.assertRaises(ValueError):batch_resource(job,variant)
  s=self.fixture['cases'][0]['scene_batch']['units'][0];a=s['animation'];saved=deepcopy(s)
  args=[a['before_controller_hex'],a['request']['buffer_pointer'],a['metadata_pointer'],a['allocations'][2]['pointer'],a['texture_table']]
  for pointer in (0,-4,True,3,0xFFFFFFFF):
   args[1]=pointer
   with self.assertRaises(ValueError):expected_binding(*args,rules=self.rules['bindings']['393'])
  self.assertEqual(s,saved)

 def test_separate_source_rules_and_immutable_fixture_exports(self):
  rules=json.loads((ROOT/'prototype/data/school_scene_batch_rules.json').read_text('utf-8'))
  fixture=json.loads((ROOT/'prototype/data/school_scene_batch_evidence.json').read_text('utf-8'))
  self.assertEqual(rules,self.rules);self.assertEqual(fixture,self.fixture)
  self.assertNotIn('cases',rules);self.assertNotIn('bindings',fixture)

if __name__=='__main__':unittest.main()

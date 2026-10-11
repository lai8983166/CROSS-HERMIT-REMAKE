from copy import deepcopy
import json,struct,unittest
from tools.school_scene_second_constructor_catalog import (
 source_catalog,native_fixture,expected_binding,expected_constructor,animation_inputs,ROOT)
from tools.school_scene_second_constructor_emulation import second_resource
from tools.school_scene_unit_work_catalog import expected_prefix,source_catalog as prefix_rules
from tools.school_enemy_records_catalog import source_catalog as record_rules,expected_record
from tools.dxanim_lib import DxAnimError

class SceneSecondConstructorSourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.rules,cls.fixture=source_catalog(),native_fixture()

 def binding(self,a,**changes):
  args={'before_controller_hex':a['before_controller_hex'],'file_pointer':a['request']['buffer_pointer'],
   'metadata_pointer':a['metadata_pointer'],'texture_allocation':a['allocations'][2]['pointer'],
   'texture_table':a['texture_table'],'variant':a['variant'],'rules':self.rules['binding']}
  args.update(changes);return expected_binding(**args)

 def tail(self,c,**changes):
  t,a=c['second_scene_constructor'],c['second_scene_animation']
  args={k:t[k] for k in ('before_work_hex','work_pointer','before_cm_hex')}
  args.update(record_hex=t['before_record_hex'],selector=t['relation_selector'],relation_hex=t['relation_hex'],
   controller_pointer=a['controller'],metadata_pointer=a['metadata_pointer'],rules=self.rules['constructor'])
  args.update(changes);return expected_constructor(**args)

 def test_native_mode0_controller_metadata_all_textures_palettes_pixels_and_release(self):
  for c in self.fixture['cases'][:3]:
   a=c['second_scene_animation'];e=self.binding(a)
   for k in ('controller_hex','metadata_hex'):self.assertEqual(a[k],e[k])
   self.assertEqual(a['binding']['args'],e['binding_args'])
   self.assertEqual(a['file_release']['sha256_at_release'],e['source_sha256_at_release'])
   self.assertEqual(e['texture_count'],126)
   uploads=[n for n in a['boundaries'] if n['kind']=='pixel_upload']
   self.assertEqual(len(a['entries']),126);self.assertEqual(len(uploads),126)
   for actual,x,upload in zip(a['entries'],e['texture_entries'],uploads):
    for k in x:
     if k!='upload_args':self.assertEqual(actual[k],x[k],(c['name'],x['index'],k))
    self.assertEqual(upload['args'],x['upload_args'])
   # Mode0 ignores archive palette-mask values for upload selection.
   r=deepcopy(self.rules['binding'])
   for entry in r['animation']['texture_entries']:entry['palette_mask']=0
   declared=self.binding(a,rules=r)
   self.assertEqual(declared['binding_args'][-2:],[0,0])
   self.assertTrue(all(t['palette_pointer']==0 for t in declared['texture_entries']))

 def test_complete_actual_prefix_and_special_tail_work_record_scratch_cell_bytes(self):
  r=prefix_rules();records=record_rules()
  original=expected_record(records['templates'][1],rules=records)['record_hex']
  for c in self.fixture['cases'][:3]:
   p,t=c['second_scene_work'],c['second_scene_constructor']
   self.assertEqual(p['before_record_hex'],original)
   prefix=expected_prefix(p['before_record_hex'],1,p['cache_before_hex'],p['counter_before'],
    p['renderer'],p['allocation']['pointer'],p['classification_selector'],p['relation_hex'],r)
   for k in ('work_hex','record_hex','cache_hex','controller_hex','counter','cache_slot'):
    self.assertEqual(prefix[k],p[k],k)
   self.assertEqual(prefix['work_hex'],t['before_work_hex']);self.assertEqual(prefix['record_hex'],t['before_record_hex'])
   self.assertEqual(prefix['controller_hex'],c['second_scene_animation']['before_controller_hex'])
   e=self.tail(c)
   for k in ('work_hex','record_hex','shared_hex','cm_hex','cm_sha256','constructor_coordinates'):
    self.assertEqual(t[k],e[k],(c['name'],k))
   self.assertEqual([e[k] for k in ('action','direction','mapped_direction','block','animation','flags','descriptor_index')],
    [1,3,7,0,4,1,132])
   before=bytearray.fromhex(t['before_record_hex']);before[159]=2
   self.assertEqual(bytes(before).hex(),e['record_hex'])

 def test_source_visible_frame_special_direction_classification_and_cell_wrap(self):
  c=self.fixture['cases'][0];r=self.rules['constructor'];initial=r['initial_program']
  self.assertEqual(r['special']['role_min'],387);self.assertEqual(r['special']['role_max'],404)
  self.assertEqual(initial['first_instruction']['raw'],'800084fffffff0ff0100')
  self.assertEqual(initial['first_instruction']['duration_ticks'],1)
  self.assertEqual(len(initial['visible_layers']),1)
  layer=initial['visible_layers'][0]
  self.assertEqual([layer[k] for k in ('descriptor','frame','x','y','draw_group')],[132,4,0,0,7])
  self.assertTrue(layer['flip_x'])
  # Native category==selector predicate bypasses the relation byte.
  self.assertEqual(self.tail(c,relation_hex=('ff'*256))['work_hex'],self.tail(c)['work_hex'])
  relation=bytearray(256);relation[16]=255
  with self.assertRaises(ValueError):self.tail(c,selector=1,relation_hex=relation.hex())
  t=c['second_scene_constructor'];x,y=t['constructor_coordinates'];cm=bytearray.fromhex(t['before_cm_hex'])
  cm[2*(y*64+x)+1]=255
  self.assertEqual(bytes.fromhex(self.tail(c,before_cm_hex=cm.hex())['cm_hex'])[2*(y*64+x)+1],0)
  record=bytearray.fromhex(t['before_record_hex']);record[155:157]=bytes([63,95])
  e=self.tail(c,record_hex=record.hex());self.assertEqual(e['constructor_coordinates'],[63,95])
  self.assertEqual(e['fixed_coordinates'],[((63<<5)+16)<<16,((95<<4)+8)<<16])

 def test_malformed_archives_and_unsupported_binding_tail_inputs_refuse_atomically(self):
  raw,_,_=second_resource();o=self.rules['binding']['animation']['sections']
  bad=bytearray(raw);bad[o[8]['offset']]=2
  bad_padding=bytearray(raw);bad_padding[-1]=1
  bad_bmp=bytearray(raw);at=o[6]['offset']+self.rules['binding']['animation']['texture_entries'][0]['offset'];bad_bmp[at:at+2]=b'XX'
  for data in (b'',raw[:20],raw[:-1],bytes(bad),bytes(bad_padding),bytes(bad_bmp)):
   with self.assertRaises((ValueError,DxAnimError)):animation_inputs(data)
  c=self.fixture['cases'][0];a=c['second_scene_animation'];saved=deepcopy(c)
  for variant in (1,-1,True,'0'):
   with self.assertRaises(ValueError):self.binding(a,variant=variant)
  for pointer in (0,-4,True,'4',3,0xFFFFFFFF):
   with self.assertRaises(ValueError):self.binding(a,file_pointer=pointer)
   with self.assertRaises(ValueError):self.tail(c,work_pointer=pointer)
  for k in ('before_work_hex','record_hex','before_cm_hex','relation_hex'):
   for v in (None,'zz','00'):
    with self.assertRaises(ValueError):self.tail(c,**{k:v})
  for selector in (-1,16,True,'0'):
   with self.assertRaises(ValueError):self.tail(c,selector=selector)
  with self.assertRaises(ValueError):self.binding(a,metadata_pointer=a['request']['buffer_pointer'])
  for at,value in ((2,0),(12,0),(164,7),(15,0),(155,64),(156,96)):
   record=bytearray.fromhex(c['second_scene_constructor']['before_record_hex']);record[at]=value
   with self.assertRaises(ValueError):self.tail(c,record_hex=record.hex())
  rules=deepcopy(self.rules['constructor']);rules['programs'][0][4][0]['opcode']=1
  with self.assertRaises(ValueError):self.tail(c,rules=rules)
  self.assertEqual(c,saved)

 def test_rules_and_frozen_evidence_exports_are_separate_and_exact(self):
  rules=json.loads((ROOT/'prototype/data/school_scene_second_constructor_rules.json').read_text('utf-8'))
  fixture=json.loads((ROOT/'prototype/data/school_scene_second_constructor_evidence.json').read_text('utf-8'))
  self.assertEqual(rules,self.rules);self.assertEqual(fixture,self.fixture)
  self.assertNotIn('cases',rules);self.assertNotIn('binding',fixture)
  saved=deepcopy(rules);fixture['cases'][0]['second_scene_constructor']['work_hex']=''
  self.assertEqual(saved,rules)

if __name__=='__main__':unittest.main()

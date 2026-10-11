import json,struct,unittest
from copy import deepcopy
from tools.school_deployment_tail_catalog import *

def project(p):return expected_tail(p['inputs'],p['units'],p['regions'],p['category_lists'])
class DeploymentSourceTests(unittest.TestCase):
 def test_complete_original_bytes_for_every_ready_case(self):
  for c in native_fixture()['cases']:
   p=c['deployment_tail'];result=project(p)
   for key,value in result.items():self.assertEqual(value,p[key],(c['name'],key))
   self.assertEqual(sum(a['bytes'] for a in result['allocations']),589824)
   # The pair allocation is intentionally never cleared by the original code.
   self.assertEqual(bytes.fromhex(result['allocations'][3]['hex']),bytes([205])*49152)

 def test_source_predicates_distinguish_state_role_and_category(self):
  p=deepcopy(native_fixture()['cases'][0]['deployment_tail'])
  original=project(p);unit=p['units'][0];record=bytearray.fromhex(unit['record_hex']);record[15]=0;unit['record_hex']=record.hex()
  self.assertEqual(project(p)['selected_indices'],original['selected_indices'])
  struct.pack_into('<H',record,2,46);unit['record_hex']=record.hex();out=project(p)
  self.assertNotIn(unit['index'],out['selected_indices'])
  count_region=next(r for r in out['regions'] if r['pointer']==UNITCTRL+0x108B30)
  self.assertEqual(struct.unpack('<H',bytes.fromhex(count_region['hex']))[0],4)
  record[164]=255;unit['record_hex']=record.hex();out=project(p)
  count_region=next(r for r in out['regions'] if r['pointer']==UNITCTRL+0x108B30)
  self.assertEqual(struct.unpack('<H',bytes.fromhex(count_region['hex']))[0],3)

 def test_malformed_shapes_types_and_unit_ownership_refuse(self):
  base=native_fixture()['cases'][0]['deployment_tail']
  for field,value in [('dimensions',[64,95]),('category',1),('mode',2),('pool',POOL+4),('malloc_fill_byte',0),('category',False)]:
   p=deepcopy(base);p['inputs'][field]=value
   with self.assertRaises(ValueError):project(p)
  for kind in ('order','record','work','region'):
   p=deepcopy(base)
   if kind=='order':p['units'].reverse()
   elif kind=='record':p['units'][0]['record_pointer']+=176
   elif kind=='work':p['units'][0]['before_work_hex']='00'
   else:p['regions'][0]['pointer']+=4
   with self.assertRaises(ValueError):project(p)

 def test_invalid_category_free_chain_and_record_category_refuse(self):
  base=native_fixture()['cases'][0]['deployment_tail']
  for kind in ('owner','chain','header','category','capacity'):
   p=deepcopy(base)
   if kind=='owner':p['category_lists'][0]['nodes_pointer']=POOL
   elif kind=='chain':p['category_lists'][0]['before_nodes_hex']='00'*240
   elif kind=='header':p['category_lists'][0]['before_hex']='00'*44
   elif kind=='category':
    r=bytearray.fromhex(p['units'][0]['record_hex']);r[152]=10;p['units'][0]['record_hex']=r.hex()
   else:
    units=[]
    for i in range(21):
     s=deepcopy(p['units'][0]);s['index']=i;s['work_pointer']=UNITCTRL+0x80AEC+i*1312;s['record_pointer']=UNITCTRL+0xD0C2C+i*176
     raw=bytearray.fromhex(s['before_work_hex']);struct.pack_into('<I',raw,600,s['record_pointer']);s['before_work_hex']=raw.hex();units.append(s)
    p['units']=units
   with self.assertRaises(ValueError):project(p)

 def test_separate_source_and_native_exports(self):
  rules=json.loads((ROOT/'prototype/data/school_deployment_tail_rules.json').read_text('utf-8'))
  evidence=json.loads((ROOT/'prototype/data/school_deployment_tail_evidence.json').read_text('utf-8'))
  self.assertEqual(rules,source_catalog());self.assertNotIn('cases',rules);self.assertFalse(rules['selection_uses_record_state'])
  self.assertEqual(evidence['native_report_sha256'],EVIDENCE_SHA256);self.assertEqual(evidence['cases'],native_fixture()['cases'])
  self.assertFalse(evidence['runtime_fixture']);self.assertEqual(len(evidence['inherited_refusals']),2)

if __name__=='__main__':unittest.main()

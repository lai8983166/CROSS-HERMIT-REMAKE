import copy,json,struct,unittest
from tools.school_startup_lifetime_verification import ROOT,verify_report,verify_case,source_contract,branch_probes

REPORT='analysis/school-startup-lifetime-native-v3-20261020.json'
PROOF='analysis/school-startup-lifetime-verification-v1-20261020.json'
def report():return json.loads((ROOT/REPORT).read_text(encoding='utf8'))

class LifetimeTests(unittest.TestCase):
 def test_original_integrated_startup_teardown_and_separate_R2(self):
  r=report();saved=copy.deepcopy(r);p=verify_report(r)
  self.assertEqual(r,saved)
  self.assertEqual(p,json.loads((ROOT/PROOF).read_text(encoding='utf8')))
  self.assertTrue(p['R1_original_initialization_and_game_cleanup'])
  self.assertFalse(p['R2_render_connection_complete'])
  self.assertTrue(all(x['normal_game_cleanup_observed'] for x in p['cases']))

 def test_rejects_expired_fabricated_or_foreign_native_ownership(self):
  for kind in ('game','manager','device','font','queue','cache','bitmap','window','foreign_close','forced','live','patch','VM'):
   c=report()['cases'][0]
   if kind in ('game','manager','device'):
    b=bytearray.fromhex(c['ready']['game']['hex']);off={'game':0xb278,'manager':0x1058,'device':0x105c}[kind];struct.pack_into('<I',b,off,0);c['ready']['game']['hex']=b.hex()
   elif kind=='font':c['ready']['fonts'][0]['pointer']+=4
   elif kind=='queue':c['ready']['queues'][1]['bytes']=4
   elif kind=='cache':c['ready']['cache_sprite']['pointer']=0
   elif kind=='bitmap':c['ready']['cache_bitmap']['bytes']=32
   elif kind=='window':c['ready']['window']['property']=0
   elif kind=='foreign_close':c['close_request']['pid']+=1
   elif kind=='forced':c['lifetime']['forced_termination']=True
   elif kind=='live':c['resumable_checkpoint']=True
   elif kind=='patch':c['original_IAT_written']=True
   else:c['retained_VM_advanced']=True
   with self.subTest(kind=kind),self.assertRaises(ValueError):verify_case(c,source_contract())

 def test_rejects_missing_initialization_caller_or_cleanup_evidence(self):
  for kind in ('factory','context','code','loop','COM','cleanup','duplicate','status','source'):
   r=report();c=r['cases'][0]
   if kind=='factory':c['factory']['frames']=[]
   elif kind=='context':c['ready']['frames'][0]['EIP']^=1
   elif kind=='code':c['ready']['source'][0]['sha256']='0'*64
   elif kind=='loop':c['ready']['frames']=[]
   elif kind=='COM':
    b=bytearray.fromhex(c['ready']['winmain_frame']['stack_hex']);struct.pack_into('<I',b,0xac-0x38,0x80004005);f=c['ready']['winmain_frame'];f['stack_hex']=b.hex();f['locals_hex']=b[0x10:0xac].hex()
   elif kind=='cleanup':c['shutdown']=[]
   elif kind=='duplicate':c['duplicate']['after_window']=0
   elif kind=='status':c['lifetime']['exits'][str(c['ready']['pid'])]['code']=0xc0000005
   else:r['observer_source_sha256']='0'*64
   with self.subTest(kind=kind),self.assertRaises(ValueError):verify_report(r)

 def test_source_imports_and_declared_failure_branches(self):
  names={k:v['symbol'] for k,v in source_contract()['imports'].items()}
  self.assertEqual(names['0x592424'],'GetClientRect');self.assertEqual(names['0x592420'],'GetWindowRect')
  self.assertEqual(names['0x592024'],'InitCommonControlsEx')
  a=branch_probes(123);b=branch_probes(456)
  self.assertEqual([c['name'] for c in a],['duplicate','window_failure','COM_failure','factory_failure','renderer_failure','post_renderer_failure'])
  self.assertEqual(a[3]['args'],[123]);self.assertEqual(b[3]['args'],[456])
  self.assertTrue(all(not c['external_call_executed'] and not c['game_function_substituted'] for c in a))

 def test_raw_report_source_identity_and_repeated_run_requirement(self):
  for kind in ('one','source','original'):
   r=report()
   if kind=='one':r['cases'].pop()
   elif kind=='source':r['source_image_sha256']='0'*64
   else:r['original_sha256']='0'*64
   with self.subTest(kind=kind),self.assertRaises(ValueError):verify_report(r)

if __name__=='__main__':unittest.main()

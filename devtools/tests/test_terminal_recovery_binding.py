"""Raw evidence tamper rejection and isolated recovery models, no desktop IO."""
import copy,unittest,struct
from devtools.prove_terminal_recovery_binding import model_source
from devtools.terminal_recovery_binding import authenticate,authenticated_recover
from devtools.terminal_recovery_session import binding_from_snapshot,attribute_mutations
from devtools.terminal_recovery_containment import receipt_after_exit
from devtools.terminal_recovery_native import BoundWindowsBackend
from devtools import terminal_graphics_desktop as d
from devtools.tests.test_terminal_graphics_desktop import ModelBackend

class BindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        r,b,a,l=model_source();cls.original={k:r[k] for k in ('owner','native_executed','native_trace','display_snapshots','texture_verifications','cleanup')};cls.b=b;cls.a=a;cls.l=l
    def run_audit(self,r=None,b=None,a=None,l=None,native=False):return authenticate(r or self.original,b or self.b,a or self.a,l or self.l,native=native)
    def test_completed_source_reused_without_new_original_execution(self):
        r=self.run_audit();self.assertEqual(len(r['events']),6);self.assertEqual(r['evidence_kind'],'model')
    def test_model_cannot_become_actual_native_proof(self):
        with self.assertRaises(ValueError):self.run_audit(native=True)
    def test_live_job_and_wrong_current_owner_rejected(self):
        for key,value in [('job_members',[1]),('process_exit',94),('same_job',False)]:
            live=copy.deepcopy(self.l);live[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.run_audit(l=live)
    def test_raw_cleanup_and_identity_mutations_rejected(self):
        cases=[('INPUT_RELEASE','remaining_owned_refs',1),('INPUT_UNACQUIRE','unacquired',0),('GFX_GAMMA_RESTORE','gamma_dirty',1),('STATUS','display_dc',5),('CB_DESTROY_WINDOW','result',0),('WINDOW_CLOSE','window_generation',2),('INPUT_CURSOR_RESTORE','show_delta_bits',1),('GFX_RELEASE','teb',99)]
        for op,key,value in cases:
            r=copy.deepcopy(self.original);q=next(x for x in r['native_trace'] if x.get('op')==op);response=next(x for x in r['native_trace'] if x['direction']=='response' and x.get('id')==q['id']);response[key]=value
            with self.subTest(op=op,key=key),self.assertRaises(ValueError):self.run_audit(r=r)
    def test_actual_gpu_read_bytes_cannot_be_replaced_by_hash(self):
        r=copy.deepcopy(self.original);proof=r['texture_verifications'][0];q=next(x for x in r['native_trace'] if x.get('direction')=='request' and x.get('id')==proof['receipt']['id']);out=q['args'][2]
        read=next(x for x in r['native_trace'] if x.get('op')=='MEM_READ' and x['id']>q['id'] and x['args']==[out,32768]);reply=next(x for x in r['native_trace'] if x['direction']=='response' and x.get('id')==read['id']);reply['hex']='ff'+reply['hex'][2:]
        with self.assertRaisesRegex(ValueError,'pixels persisted'):self.run_audit(r=r)
    def test_declared_display_target_does_not_override_actual_blob(self):
        snapshot=copy.deepcopy(self.a['snapshot']);snapshot['decoded']['target_device']='foreign'
        with self.assertRaises(ValueError):binding_from_snapshot(snapshot,self.b)
    def test_unarmed_native_backend_blocks_before_any_API(self):
        b=BoundWindowsBackend.__new__(BoundWindowsBackend);b.permit=None
        with self.assertRaises(ValueError):b.write('mode',{},device='x',baseline={})
        with self.assertRaises(ValueError):b._gamma('x','00'*1536)
        with self.assertRaises(ValueError):b.repair()
        self.assertFalse(d.NATIVE_ADMISSION)
    def test_raw_direction_metadata_does_not_break_matching(self):
        r=self.original;q=next(x for x in r['native_trace'] if x.get('op')=='GFX_GAMMA_SET');response=next(x for x in r['native_trace'] if x.get('direction')=='response' and x.get('id')==q['id'])
        before=copy.deepcopy(self.b['state']);after=copy.deepcopy(before);after['graphics']['gamma_hex']='00'*1536
        item=dict(sequence=1,op=q['op'],request_id=q['id'],before=before,after=after,response={k:v for k,v in response.items() if k!='direction'})
        receipt=self.run_audit();attribute_mutations(receipt,self.b,[item],r);self.assertEqual(receipt['mutations'],dict(gamma='00'*1536))
    def test_pending_intent_alone_never_authorizes_failure_recovery(self):
        report=dict(native_executed=True,owner=self.b['owner'],native_trace=[dict(direction='request',id=1,lane=0,op='GFX_CREATE_DEVICE',args=[])])
        live=dict(kind='retained-native-handles',owner=self.b['owner'],process_wait=0,process_exit=94,job_members=[],same_job=True)
        item=dict(sequence=1,op='GFX_CREATE_DEVICE',request_id=1,before=self.b['state'])
        with self.assertRaisesRegex(ValueError,'actual native MAIN BEGIN required'):receipt_after_exit(report,self.b,self.a,live,[item],self.b['state'])
    def test_actual_entry_only_authorizes_values_from_its_original_inputs(self):
        window=self.a['snapshot']['decoded'];args=[1,0,1,window['hwnd'],32,8192,12288]
        pp=[1024,768,22,1,0,1,window['hwnd'],0,0,0,0,0,0]
        event=dict(direction='response',event='NATIVE_MUTATION_BEGIN',request_id=1,op='GFX_CREATE_DEVICE',lane=0,pid=self.b['owner']['pid'],tid=self.b['owner']['main_tid'],teb=self.b['owner']['main_teb'],baseline_token_hex=self.b['baseline_token'],owned_hwnd=window['hwnd'],window_generation=window['window_generation'],argc=len(args),data_kind='presentation52',data_bytes=52,data_hex=struct.pack('<13I',*pp).hex(),**{'arg'+str(i):v for i,v in enumerate(args)})
        report=dict(native_executed=True,owner=self.b['owner'],native_trace=[dict(direction='request',id=1,lane=0,op='GFX_CREATE_DEVICE',args=args),event])
        live=dict(kind='retained-native-handles',owner=self.b['owner'],process_wait=0,process_exit=94,job_members=[],same_job=True)
        item=dict(sequence=1,op='GFX_CREATE_DEVICE',request_id=1,before=self.b['state']);state=copy.deepcopy(self.b['state']);state['monitors'][0]['mode'].update(width=1024,height=768)
        out=receipt_after_exit(report,self.b,self.a,live,[item],state)
        self.assertEqual(set(out['mutations']),{'mode'});self.assertFalse(out['normal_resource_cleanup_proven'])
        state['taskbars'][0]['visible']=not state['taskbars'][0]['visible']
        with self.assertRaisesRegex(ValueError,'taskbars: current value has no independent'):receipt_after_exit(report,self.b,self.a,live,[item],state)
    def test_native_orchestration_uses_explicit_model_backend_only(self):
        class Stub(ModelBackend):
            evidence_kind='native'
            def authorize(self,*a):self.armed=True
            def disarm(self):self.armed=False
        b=copy.deepcopy(self.b);b['evidence_kind']='native';b['baseline_token']=d.digest({k:v for k,v in b.items() if k!='baseline_token'})
        receipt=self.run_audit();receipt.update(evidence_kind='native',baseline_token=b['baseline_token'],mutations=dict(gamma='00'*1536))
        backend=Stub();backend.state=copy.deepcopy(b['state']);backend.state['graphics']['gamma_hex']='00'*1536
        out=authenticated_recover(b,receipt,backend,lambda:None,sleep=lambda _:None)
        self.assertTrue(out['restored'],out);self.assertEqual(backend.calls,['gamma']);self.assertFalse(backend.armed);self.assertFalse(d.NATIVE_ADMISSION)

if __name__=='__main__':unittest.main()

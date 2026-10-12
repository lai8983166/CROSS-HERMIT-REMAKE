"""Independent complete-region and original input-stack comparison for wait capture."""
from tools.school_dialogue_wait_catalog import *
from tools.school_second_live_text_catalog import compare_case as compare_second
from tools.school_text_preparation_catalog import source_catalog as text_rules

EVIDENCE=ROOT/'analysis/school-dialogue-wait-v1-20261013.json'
EVIDENCE_SHA256='7188b484705e4aa999ebfb04db2c2ad4425872479705eddffa89ada0f9035d27'
STACK=0x2000000;RETURN=0x3000000;TASK=0x1000000

def compare_step(step,before,task=TASK):
 e=advance(before,step['events']);vm=memory_regions(before)[VM];pc=struct.unpack_from('<I',vm,28)[0];wait=struct.unpack_from('<H',vm,32)[0];op=struct.unpack_from('<H',vm,34)[0]
 for k in ('after','state','predicates','text_draws','arrow_draws'):
  if step[k]!=e[k]:raise ValueError('wait complete independent step differs: '+k)
 vm_frame=STACK+0xFF00-4;wait_frame=vm_frame-text_rules()['stack_allocations']['vm']-24
 wanted=[]
 if wait:
  if op==50:
   wanted=[{'kind':'mouse','va':'0x4d5ec0','receiver':0x7E1110,'args':[wait_frame-0x20,0,0,1024,768],'return_va':'0x4cd402','output':wait_frame-0x20},
    {'kind':'keyboard','va':'0x4128f0','receiver':task+0x10B8,'args':[57,0],'return_va':'0x4cd432'}]
  else:
   wanted=[{'kind':'keyboard','va':'0x4128f0','receiver':task+0x10B8,'args':[57,0],'return_va':'0x4ccff7'},
    {'kind':'mouse_buttons','va':'0x4ccb30','receiver':VM,'args':[0,0,wait_frame-0xC,wait_frame-0x10],'return_va':'0x4cd02d','output':[wait_frame-0xC,wait_frame-0x10]}]
 if len(wanted)!=len(step['input_calls']):raise ValueError('wait original input call count')
 for record,w in zip(step['input_calls'],wanted):
  if any(record[k]!=v for k,v in w.items()):raise ValueError('wait original input stack/source caller')
  if record['kind']=='keyboard' and record['return_eax']!=0:raise ValueError('no-keyboard original result')
  # The final WORD is the original hit-test flag, not an event bit. Captured
  # position (0,0) is inside the inclusive original 1024x768 query rectangle.
  if record['kind']=='mouse' and record['output_hex']!='00'*12+'0100':raise ValueError('no-mouse original queried output and hit-test flag')
  if record['kind']=='mouse_buttons' and (record['return_eax']!=1 or record['output_hex']!=['00000000',struct.pack('<I',step['events']['mouse_buttons']).hex()]):raise ValueError('original queried confirmation event')
 handler=[]
 if not wait:
  r=source_catalog()['commands'][0 if pc==244 else 1]
  handler=[{'va':r['handler'],'receiver':VM,'args':[0,struct.unpack_from('<I',vm,16)[0]-452+r['offset'],1],'return_va':r['return_va']}]
 if step['handlers']!=handler:raise ValueError('original selected wait handler stack')
 origin=list(struct.unpack_from('<2H',vm,NODE_OFFSET+30))
 if step['text_updates']!=[{'args':[(VM+NODE_OFFSET)&0xFFFF0000|origin[0],origin[1]],'return_va':'0x4cd541','receiver':VM+OBJECT_OFFSET}] or step['natural_return']!={'va':RETURN,'sp':STACK+0xFF04,'eax':1}:raise ValueError('original natural text update/root return')
 return e

def compare_case(case):
 compare_second(case);p=case['waits'];second=case['second_live_text'];first=case['first_live_text'];inputs=p['inputs']
 if p['before']!=second['after'] or inputs['mouse_words']!=[0,0,0] or inputs['space_key_byte']!=0 or inputs['TASK']!=TASK or inputs['hold_updates']!=HOLD_UPDATES or inputs['mouse_position']!=[0,0] or inputs['driver']!='declared bounded original VM calls; captured zero input buffers':raise ValueError('wait actual live parent and captured input provenance')
 seq=expected_sequence(p['before']);current=p['before'];presentation_sha=hashlib.sha256(b''.join((json.dumps(r,sort_keys=True,separators=(',',':'))+'\n').encode() for r in second['presentation'])).hexdigest()
 if len(p['steps'])!=len(seq['steps']):raise ValueError('wait exact bounded update count')
 for index,step in enumerate(p['steps']):
  if step['index']!=index or step['events']!={'mouse_buttons':0,'space_key':0} or step['presentation_sha256']!=presentation_sha:raise ValueError('wait finite no-input sequence/presentation')
  e=compare_step(step,current);current=e['after']
 if p['after']!=current or any(p[k]!=seq[k] for k in ('text_wait_release_update','confirmation_started_update','held_confirmation_updates')):raise ValueError('wait final complete memory/cadence')
 if p['actual_readbacks']!=[first['actual_readback'],second['actual_readback']] or not p['resources_retained'] or not p['retained_ranges_unchanged']:raise ValueError('wait both complete real textures/retention')
 if not p['natural_text_readiness_executed'] or not p['original_input_query_bodies_executed'] or any(p[k] is not False for k in ('live_input_capture_executed','GPU_draw_or_present_executed','world_update_loop_executed','waves_executed','dialogue_playback_completed')):raise ValueError('wait original execution boundary')
 return {'updates':len(p['steps']),'complete_regions_per_update':len(REGIONS),'text_wait_release_update':seq['text_wait_release_update'],
  'confirmation_started_update':seq['confirmation_started_update'],'held_confirmation_updates':HOLD_UPDATES,'actual_texture_bytes':[len(bytes.fromhex(r['hex'])) for r in p['actual_readbacks']],
  'predicate_calls':sum(len(s['predicates']) for s in p['steps']),'text_draws':sum(len(s['text_draws']) for s in p['steps']),'arrow_draws':sum(len(s['arrow_draws']) for s in p['steps']),'retained_bytes':p['retained_bytes']}

@lru_cache(maxsize=1)
def native_fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('wait pinned native report identity')
 return json.loads(raw)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');a=p.parse_args()
 if a.verify:print(report_text({'source':source_catalog(),'native_report_sha256':EVIDENCE_SHA256,'cases':[{'name':c['name'],**compare_case(c)} for c in native_fixture()['cases']]}))

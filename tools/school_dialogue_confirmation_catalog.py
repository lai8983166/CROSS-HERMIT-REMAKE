"""Independent original confirmation return and following handler-entry prefix."""
from tools.school_dialogue_wait_verification import *
from tools.school_dialogue_wait_verification import compare_case as compare_wait

EVIDENCE=ROOT/'analysis/school-dialogue-confirmation-v1-20261013.json'
EVIDENCE_SHA256='94fc8592a2516586fac60dda54157ecbc5b733ab96da71b3714a4212584392c7'

def expected_boundary(before):
 mem=memory_regions(before);vm=mem[VM]
 if struct.unpack_from('<I',vm,28)[0]!=252 or struct.unpack_from('<3H',vm,32)!=(0,51,4):raise ValueError('actual released original confirmation parent')
 r=source_catalog()['commands'][2];pointer=struct.unpack_from('<I',vm,16)[0]-452
 if not 0xE000000<=pointer<0xF000000:raise ValueError('original selected script allocation')
 struct.pack_into('<2H',vm,34,30,20);vm[0x93E2]=0
 counters=mem[0x7A4E18];struct.pack_into('<2I',counters,0,(struct.unpack_from('<I',counters)[0]+1)&0xFFFFFFFF,0)
 frame=STACK+0xFF00-4;sp=frame-text_rules()['stack_allocations']['vm']-28
 return {'after':regions(mem),'pending_call':{'va':r['handler'],'receiver':VM,'args':[0,pointer+r['offset'],1],'return_va':r['return_va'],'root_return_va':hex(RETURN),
  'frames':{'vm':frame,'sp':sp},'natural_stack_verified':True,'first_instruction_executed':False}}

def compare_confirmation(case):
 compare_wait(case);p=case['confirmation'];w=case['waits'];step=p['confirmation_step']
 if p['before']!=w['after'] or p['binding']!={'slot':TASK+0x1990,'before':0,'bound':1,'origin':'declared isolated mouse-button input; no live input capture','live_game_input_modified':False}:raise ValueError('declared confirmation input provenance')
 if step['index']!=len(w['steps']) or step['events']!={'mouse_buttons':1,'space_key':0}:raise ValueError('declared confirmation sequence')
 e=compare_step(step,p['before']);derived=expected_boundary(e['after'])
 if any(p[k]!=v for k,v in derived.items()):raise ValueError('confirmation complete source boundary')
 if step['presentation_sha256']!=w['steps'][-1]['presentation_sha256'] or p['actual_readbacks']!=w['actual_readbacks'] or not p['resources_retained'] or not p['retained_ranges_unchanged'] or not p['prefix_retention']['retained_ranges_unchanged']:raise ValueError('confirmation original presentation/pixels/memory retention')
 if not p['confirmation_handler_completed'] or not p['original_input_query_bodies_executed'] or any(p[k] is not False for k in ('live_input_capture_executed','next_handler_executed','GPU_draw_or_present_executed','world_update_loop_executed','waves_executed')):raise ValueError('confirmation exact execution boundary')
 return {'complete_regions_compared':len(REGIONS),'declared_mouse_buttons':1,'confirmation_wait_cleared':True,'PC':252,'pending_opcode':30,'pending_handler':derived['pending_call']['va'],
  'next_handler_executed':False,'actual_texture_bytes':[len(bytes.fromhex(r['hex'])) for r in p['actual_readbacks']],'retained_bytes':p['retained_bytes']}

@lru_cache(maxsize=1)
def native_fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('confirmation pinned native report identity')
 return json.loads(raw)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');a=p.parse_args()
 if a.verify:print(report_text({'source':source_catalog(),'native_report_sha256':EVIDENCE_SHA256,'cases':[{'name':c['name'],**compare_confirmation(c)} for c in native_fixture()['cases']]}))

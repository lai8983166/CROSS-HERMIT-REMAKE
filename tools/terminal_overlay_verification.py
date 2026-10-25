"""Independent overlay/VM contracts and fresh current-native whole-state replay."""
import argparse,copy,gzip,json
from types import SimpleNamespace
from tools import terminal_overlay_emulation as e
from tools import terminal_overlay_model as model
from tools.battle_hit_damage_verification import full_cpu,root,platform as tls_platform
from tools.battle_lethal_combat import validate_pages
IMPLEMENTATIONS=('tools/terminal_overlay_emulation.py','tools/terminal_overlay_model.py','tools/terminal_overlay_verification.py','tools/terminal_overlay_platform.py','tools/terminal_overlay_crt_platform.cs','tools/terminal_overlay_d3d8_platform.cs')

def memory_equal(a,b,label):
 e.need([(r['pointer'],r['bytes']) for r in a]==[(r['pointer'],r['bytes']) for r in b],label+' all exact mappings')
 for x,y in zip(a,b):
  if x['hex']!=y['hex']:
   aa,bb=bytes.fromhex(x['hex']),bytes.fromhex(y['hex']);index=next(i for i,(u,v) in enumerate(zip(aa,bb)) if u!=v)
   raise ValueError(label+' full byte mismatch at '+hex(x['pointer']+index))

def native(row):
 e.need(row['current_GPU_hello']['pointer_bytes']==row['current_CRT_hello']['pointer_bytes']==4 and row['current_GPU_hello']['window_visible'] is False,'current x86 owned native helpers')
 e.need(row['current_GPU_hello']['image_size']==[512,512] and row['current_CRT_hello']['GPU_created'] is False,'separate current native GPU and CRT owners')
 ct=row['CRT_trace'];gt=row['GPU_trace']
 e.need(ct[-1]['request']['op']==gt[-1]['request']['op']=='close','both helpers normal protocol close')
 for name,trace in [('CRT',ct),('GPU',gt)]:
  for i,x in enumerate(trace):e.need(x['request']['id']==x['reply']['id']==i+1 and x['reply']['ok'] is True,'actual ordered '+name+' platform protocol')
 e.need([x['request']['op'] for x in gt]==['create','describe','lock','unlock','readback','describe','release','close'],'current GPU protocol includes actual whole surface readback')
 for i,(a,wire) in enumerate(zip(row['GPU_APIs'],[gt[j] for j in (0,1,2,3,5,6)])):
  e.need(a['op']==wire['request']['op'] and a['native_result']==wire['reply']['result'] and a['actual_API_executed'] is True,'each original COM leaf matches current actual receipt')
 e.need(gt[4]['reply']['result']==row['resource_loaded']['readback'] and gt[3]['request']['hex']==row['resource_loaded']['upload_hex'],'actual uploaded and readback whole surface records')
 e.need(gt[-1]['reply']['result']==row['GPU_cleanup'] and ct[-1]['reply']['result']==row['CRT_cleanup'],'exact complete native close receipts')
 covered=[]
 for x in row['CRT_APIs']:
  start,end=x['wire_start'],x['wire_end'];e.need(0<=start<end<len(ct),'every current CRT OS leaf has actual bounded wire interval');covered.extend(range(start,end))
  e.need(e.CODE[x['import_slot']-0x400000:x['import_slot']-0x400000+4]==x['target'].to_bytes(4,'little'),'unchanged original CRT IAT identity')
  if x['name']=='ReadFile':
   y=ct[end-1];e.need(y['request']['op']=='read' and y['reply']['result']['read']==len(e.RESOURCE) and y['reply']['result']['value']==1,'complete actual ReadFile receipt')
  if x['name']=='CreateFileA':e.need(ct[start]['request']['path']==e.RESOURCE_NAME and x['value']==0x62001000,'actual source-only read-only open with declared file token')
 e.need(covered==list(range(len(ct)-1)),'all native CRT calls covered exactly once by original OS leaf boundaries')
 e.need([x['name'] for x in row['task_APIs']]==['lstrlenA','ImmGetOpenStatus','lstrlenA','ImmGetOpenStatus','lstrlenA','ImmGetOpenStatus','lstrlenA','ImmGetOpenStatus','lstrlenA'],'five original input resets and four real null-IME leaves')
 for x in row['task_APIs']:
  e.need(x['actual_API_executed'] is True and x['result']==0,'actual task OS leaf result')
  if x['name']=='ImmGetOpenStatus':e.need(x['args']==[0] and x['observed']['actual_OS_observed'] is True,'actual null IME query')
  else:e.need(x['args']==[e.INPUT+0x528] and x['string_hex']=='','actual declared empty task text')

def verify_case(row,replay=False,helpers=None):
 result=model.verify(row);native(row);validate_pages(row,row['blobs'])
 e.need(row['image_before']==row['image_after'],'original image/IAT unchanged across complete forward run')
 for key in ('initial','final'):
  previous=-1
  for r in row[key]:e.need(r['pointer']>previous and r['bytes']>0 and len(bytes.fromhex(r['hex']))==r['bytes'],'all complete disjoint mapped memory');previous=r['pointer']+r['bytes']-1
 frames=row['world_frames'];events=row['events'];e.need(len(frames)==len(events)==(1 if row['input']['name']=='neutral_running' else 3),'fresh complete original world/event prefix')
 for i,(f,v) in enumerate(zip(frames,events)):
  root(f['call'],0x46B470,e.CTRL,[]);root(v['call'],0x432100,e.CTRL,[]);e.need(f['scanned_slots']==[e.parent.UNIT+j*0x520 for j in range(250)] and not f['controls'],'full250-slot source world without host actions');model.previous.combat.event_contract(row,i)
 combat=model.previous.combat.world_contracts(row);tls_platform(row['platform'],SimpleNamespace(crt_draws=combat['CRT_draws']))
 e.need(all(row[k] is False for k in ('game_function_results_stubbed','OS_input_submitted','host_unit_fields_changed_after_initialization')),'no original game stubs, system input or host unit-state writes')
 c=row['overlay_continuation'];expected=row['admission']['partial']['trace_after'];e.need(c['trace_before']==expected,'same uninterrupted original407870 boundary')
 e.need(c['first_task']['trace_after']['instructions']<c['frames'][0]['reset']['trace_before']['instructions'],'declared original queue roots precede next input reset')
 for f in c['frames']:
  root(f['reset']['call'],0x425DE0,e.INPUT,[]);root(f['task']['call'],0x454CF0,e.TASK,[])
  e.need(f['reset']['trace_after']==f['task']['trace_before'],'continuous reset and full-task original trace')
 e.need(row['pending_CPU']==c['after_CPU'],'final original task CPU retained')
 for name,p,n in [('VM',e.VM,0x9400),('task',e.TASK,0x190),('work',e.WORK,0x24C0),('owner',e.MAIN,65536)]:e.need(model.read(row['final'],p,n).hex()==c['after'][name],'final observed '+name+' matches complete actual memory')
 memory_equal(row['final'],c['memory'],'forward final whole-memory boundary')
 e.need(row['instructions']==c['trace_after']['instructions'] and row['writes']==c['trace_after']['writes'] and row['code_trace_sha256']==c['trace_after']['code_sha256'] and row['write_trace_sha256']==c['trace_after']['write_sha256'],'complete original forward instruction/write digests')
 if replay:
  ch,gh=helpers[:2];other=e.run_case(row['input'],ch,gh,[x['result'] for x in row['APIs'] if x['name']=='GetTickCount']);model.verify(other);native(other)
  for key in ('initial','final'):memory_equal(row[key],other[key],'fresh native replay '+key)
  for key in ('pending_CPU','image_before','image_after','instructions','writes','code_trace_sha256','write_trace_sha256','extra_original_instruction_counts','task_calls','task_writes','admission','resource_initialization','cleanup_steps','cleanup_state','accounting_baseline','final_state','world_frames','events','commands'):
   e.need(row[key]==other[key],'fresh actual-native exact CPU/state/trace replay '+key)
  memory_equal(row['resource_loaded']['memory'],other['resource_loaded']['memory'],'fresh current resource-loaded replay')
  for key in ('first_task','frames','before_CPU','after_CPU','trace_before','trace_after','after','calls','commands'):e.need(c[key]==other['overlay_continuation'][key],'fresh full original VM replay '+key)
 result.pop('source_rules');result['all_owned_memory_CPU_and_trace_replayed']=replay;return result

def verify(path):
 d=json.loads(gzip.decompress(path.read_bytes()));e.need(d['source_contract']==e.source_contract() and [x['input'] for x in d['cases']]==e.parent.corpus(),'exact source/case contracts');h=e.helpers();rows=[]
 for r in d['cases']:rows.append(verify_case(r,True,h));print('verified current native',r['input']['name'],flush=True)
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(e.ROOT).as_posix()),source_rules=model.source_rules(),cases=rows,implementation_sha256={p:e.sha((e.ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},independent_resource_pixels_packet_queue_VM_rules=True,all_current_native_resources_recreated_for_replay=True,all_owned_memory_CPU_and_trace_replayed=True,actual_draw_or_Present=False,terminal_presentation_complete=False,task_exit_complete=False,rewards_complete=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();e.need(not(e.ROOT/a.out).exists(),'fresh immutable overlay proof');e.terminal.save(a.out,verify(e.ROOT/a.report))

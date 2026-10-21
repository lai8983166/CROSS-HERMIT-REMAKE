"""Independent source-instruction/write replay of retained keyboard continuation."""
import gzip,json,struct
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_MEM_WRITE
from tools.school_retained_keyboard import (ROOT,SOURCE,KEYBOARD,STACK,VM,INPUT,IME_SLOT,ROOT_RETURN,
 inputs,prefix,memory_rows,REGISTERS,architectural_cpu,canonical,need,word,predict_keyboard)
from tools.school_task_frame_verification import TaskReplay


class Replay(TaskReplay):
 def api(self,a):
  need(a['key']=='offline_recorded_platform','no unrecorded platform substitution')
  r=a['call'];sp=self.u.reg_read(REGISTERS['ESP']);arg=word(self.read(sp+4));ret=word(self.read(sp))
  need(r['origin']=='frozen complete-task platform output under identical null/empty input; not a fresh OS call','explicit platform replay origin')
  if r['name']=='ImmGetOpenStatus':need(r['import_slot']==IME_SLOT and ret==0x425c99 and arg==word(self.read(INPUT+8))==0,'original null IMM boundary')
  else:
   from tools.school_font_raster_emulation import IMPORTS
   need(r['name']=='lstrlenA' and IMPORTS[r['import_slot']][0]=='lstrlenA' and ret==0x425a7e and self.read(arg,1)==bytes(1),'source empty string boundary')
  need(r['sp']==sp and r['return_va']==ret and r['args']==[arg] and r['result']==0 and word(self.read(r['import_slot']))==r['target']==a['va'],'exact source platform target/arguments/recorded zero')
  self.u.reg_write(REGISTERS['EAX'],0);self.u.reg_write(REGISTERS['ESP'],sp+8);self.u.reg_write(REGISTERS['EIP'],ret)


def state(r):
 pc,wait,op=struct.unpack('<IHH',r.read(VM+28,8))
 return dict(PC=pc,wait=wait,opcode=op,space_current=r.read(KEYBOARD+0x4b9,1)[0],IME_request=r.read(INPUT+0x630,1)[0])


def protocol(c,contract):
 need(c['name'] in contract['parents'] and c['scene_capture'] in (76,77),'retained case and native source stream')
 stream=contract['streams'][c['scene_capture']];need(c['stream']==stream,'exact pinned native captures')
 n=len(c['readiness']);need(1<=n<=80 and len(c['no_input_controls'])==2,'bounded natural readiness and controls')
 labels=['readiness_'+str(i) for i in range(n)]+['no_input_control_0','no_input_control_1','captured_space_confirmation','next_original_task_handler_boundary'];expected=[]
 for label in labels:
  if label=='readiness_0':expected.append(('captured_idle',None))
  if label=='captured_space_confirmation':expected.append(('captured_press',None))
  if label=='next_original_task_handler_boundary':expected.append(('captured_release',None))
  for suffix,va,recv in (('_IME',0x425de0,INPUT),('_queue_0x40db90',0x40db90,0x1001058),('_queue_0x40dc80',0x40dc80,0x1001058),('',0x454cf0,0xe000000)):
   expected.append((label+suffix,dict(va=va,receiver=recv,sp=STACK+0xf000,return_va=ROOT_RETURN)))
 need(len(c['steps'])==len(expected) and [(s['label'],s.get('root')) for s in c['steps']]==expected,'exact complete-task driver sequence; no independent VM roots')
 need([b['capture'] for b in c['bindings']]==stream['captures'] and len(c['bindings'])==3,'only pinned idle/press/release device inputs')
 for binding in c['bindings']:
  before=bytes.fromhex(binding['before_hex']);bound=bytearray(before);bound[12:268]=bytes.fromhex(binding['capture']['raw_device_hex'])
  need(len(before)==0xa00 and binding['bound_hex']==bound.hex() and binding['after_hex']==predict_keyboard(bytes(bound)).hex(),'independent full keyboard model and raw-only binding')
  need(binding['only_device_output_written']==dict(pointer=KEYBOARD+12,bytes=256),'only raw device-output guest write declared')
  i=binding['step_index'];need(type(i)is int and 0<=i<len(c['steps']) and c['steps'][i]['kind']=='keyboard' and c['steps'][i]['label']=='captured_'+binding['capture']['label'],'binding exact source fragment')
 need(c['readiness'][-1]['PC']==252 and c['readiness'][-1]['wait']==1 and c['readiness'][-1]['opcode']==51,'natural confirmation gate entered')
 need(all((s['PC'],s['wait'],s['opcode'],s['space_current'])==(252,1,51,0) for s in c['no_input_controls']),'no-input gate stays held')
 need((c['confirmation']['PC'],c['confirmation']['wait'],c['confirmation']['opcode'],c['confirmation']['space_current'])==(252,0,51,128),'captured space clears actual VM wait')
 need(c['next_handler']['va']==0x4c61c0 and c['next_handler']['return_va']==0x4ceda7 and c['next_handler']['first_instruction_executed'] is False,'next source opcode30 natural handler entry only')


def verify_case(c,contract):
 protocol(c,contract);parent=contract['parents'][c['name']];memory,cpu,provenance=prefix(c['name'],parent['path'],parent['sha256']);need(canonical(c['parent_replay'])==canonical(provenance),'entire frozen task-prefix provenance and memory')
 r=Replay.__new__(Replay);r.u=Uc(UC_ARCH_X86,UC_MODE_32);r.image=SOURCE.read_bytes();r.objects={};r.locks={}
 for at,b in memory:r.u.mem_map(at,len(b));r.u.mem_write(at,b)
 r.u.context_restore(cpu);bindings={b['step_index']:b for b in c['bindings']};instructions=0;observed_states={}
 for i,s in enumerate(c['steps']):
  hook=None
  if s['kind']=='keyboard':
   need(i in bindings and s['boundary']==0x4116a4,'source post-device interval boundary');b=bindings[i]
   need(r.read(KEYBOARD,0xa00).hex()==b['before_hex'],'independent live guest keyboard before device input')
   r.u.mem_write(KEYBOARD+12,bytes.fromhex(b['capture']['raw_device_hex']));bp=STACK+0xf800;r.u.mem_write(bp-4,struct.pack('<I',KEYBOARD))
   for k,v in dict(EIP=0x4113d5,EBP=bp,ESP=bp-0x70,EFLAGS=0x202).items():r.u.reg_write(REGISTERS[k],v)
   def finite(u,access,at,n,value,_):need(KEYBOARD<=at and at+n<=KEYBOARD+0xa00 or STACK<=at and at+n<=STACK+65536,'independent keyboard write extent')
   hook=r.u.hook_add(UC_HOOK_MEM_WRITE,finite)
  else:need(s['kind']=='task' and s['boundary']==(0x4c61c0 if s['label']=='next_original_task_handler_boundary' else ROOT_RETURN),'exact full-task/natural handler stop')
  calls=[dict(va=a['target'],key='offline_recorded_platform',call=a) for a in s['platform_replays']]
  result=dict(s,api_calls=calls)
  # The new driver records only zero-argument roots. Adapt that declaration to
  # the frozen renderer replayer's explicit args field without changing reports.
  root=dict(s['root'],args=[]) if s.get('root') else None
  try:instructions+=r.step(dict(label=s['label'],root=root,result=result))
  finally:
   if hook is not None:r.u.hook_del(hook)
  need(state(r)==s['state'],'independent VM/input/IME state after every original interval');observed_states[s['label']]=state(r)
  if s['kind']=='keyboard':need(r.read(KEYBOARD,0xa00).hex()==bindings[i]['after_hex'],'entire source-produced keyboard object')
  elif s['label'].split('_')[0] in ('readiness','no','captured') and s['root']['va']==0x454cf0:
   need(s['cpu']['EAX']==0 and s['cpu']['ESP']==STACK+0xf004,'complete task ABI natural return')
 need([observed_states['readiness_'+str(i)] for i in range(len(c['readiness']))]==c['readiness'] and [observed_states['no_input_control_'+str(i)] for i in range(2)]==c['no_input_controls'] and observed_states['captured_space_confirmation']==c['confirmation'],'all published progression states derived from source replay')
 sp=r.cpu()['ESP'];args=[word(r.read(sp+4+4*i)) for i in range(3)]
 need(args==c['next_handler']['args']==[0,word(r.read(0xe000064))+704,1] and sp==c['next_handler']['sp'] and r.cpu()['ECX']==VM,'full natural next-handler source stack/receiver')
 need(state(r)==c['next_handler']['state'] and (state(r)['PC'],state(r)['wait'],state(r)['opcode'],state(r)['space_current'])==(252,0,30,0),'released keyboard and natural next opcode')
 need(not any(x['va']==0x4c61c0 for x in c['steps'][-1]['instruction_counts']),'handler first instruction remains unexecuted')
 need(memory_rows(r.u)==c['final_memory'] and canonical(architectural_cpu(r.u))==canonical(c['final_architectural_cpu']),'all final memory mappings and architectural CPU independently reproduced')
 return dict(name=c['name'],native_capture_scene=c['scene_capture'],parent_instructions_replayed=provenance['original_instructions_replayed'],new_original_instructions_replayed=instructions,source_intervals=len(c['steps']),complete_original_tasks=len(c['readiness'])+3,next_task_prefix=True,independent_VM_roots=0,source_keyboard_updates=3,final_memory_regions=len(c['final_memory']),next_handler=c['next_handler'],offline_recorded_platform_only=True,R3_complete=False)


def verify(report):
 contract=inputs();need(canonical(report['contract'])==canonical(contract),'pinned source/recording contract')
 for k in ('new_OS_input','new_GPU_or_window','original_outer_scheduler','full_world_loop','R3_complete','Godot_changed'):need(report[k] is False,'honest offline scope '+k)
 need(report['schema_version']==1 and report['independent_VM_roots']==0,'source report schema/no VM shortcut')
 need([(c['name'],c['scene_capture']) for c in report['cases']]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'six complete case/stream combinations')
 # Reject malformed declarations before paying for the independent full replay.
 for c in report['cases']:protocol(c,contract)
 return dict(schema_version=1,cases=[verify_case(c,contract) for c in report['cases']],six_retained_keyboard_connections_verified=True,new_native_input_or_GPU=False,R3_complete=False)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof output required')
 result=verify(json.loads(gzip.decompress((ROOT/a.report).read_bytes())));out.write_text(json.dumps(result,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('independent retained keyboard replay verified',len(result['cases']),'cases',flush=True)

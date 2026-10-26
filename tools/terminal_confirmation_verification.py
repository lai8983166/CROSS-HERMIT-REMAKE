"""Independent captured keyboard, original panel27, complete tasks and font boundary."""
import argparse,copy,gzip,hashlib,json,struct
from functools import lru_cache
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
import unicorn.x86_const as x86
from tools import terminal_confirmation_emulation as e
from tools import terminal_dialogue_verification as previous
from tools import school_retained_keyboard as keyboard
from tools.school_native_dialogue_verification import predict_keyboard
need=e.need;num=previous.num;read=previous.read;equal=previous.equal
IMPLEMENTATIONS=('tools/terminal_confirmation_emulation.py','tools/terminal_confirmation_verification.py','tools/terminal_confirmation_preservation.py','tools/tests/test_terminal_confirmation.py')
QUERIES=(0x4C5EA0,0x4CC600,0x4CC0F0,0x4CC7D0,0x4CC810,0x4CA600,0x4CBDB0,0x407870,0x4079C0,0x4128F0,0x4CCFF7,0x4CD02D,0x4CD350,0x4CD402,0x4CD432)

class Replay(previous.Replay):
 def __init__(self,row):
  self.row=row;self.d=row['terminal_confirmation'];self.n=self.p=dict(before=self.d['before']);self.u=Uc(UC_ARCH_X86,UC_MODE_32);self.objects={};self.locks={};self.cleaning=False
  for r in self.d['before']['memory']:self.u.mem_map(r['pointer'],r['bytes']);self.u.mem_write(r['pointer'],bytes.fromhex(r['hex']))
  cpu=self.d['before']['CPU'];first=['GDTR','IDTR','LDTR','TR','CR0','CR2','CR3','CR4']
  for k in first+[k for k in cpu if k not in first]:
   reg=getattr(x86,'UC_X86_REG_'+k);v=tuple(cpu[k]) if isinstance(cpu[k],list) else cpu[k]
   if self.u.reg_read(reg)!=v:self.u.reg_write(reg,v)
  need(self.cpu()==cpu and len(cpu)==57,'all57 confirmation architectural registers restored')
 def capture(self,b,full=False):
  memory=self.snapshot() if full else [dict(pointer=a,bytes=z-a+1,sha256=e.sha(self.read(a,z-a+1))) for a,z,_ in self.u.mem_regions()]
  if full:equal(memory,b['memory'],'independent whole mapped region reread')
  else:need(memory==b['memory'],'independent every full region reread SHA and exact mappings')
  need(self.cpu()==b['CPU'] and self.state()==b['state'] and self.queue()==b['queue'],'independent full CPU/state/queue')
 def execute(self):
  d=self.d;index=count=writes=roots=0;ih=hashlib.sha256();wh=hashlib.sha256();observed=[];queries=[];commands=[];current=None;lookup_record=None
  def mark():return dict(instructions=count,writes=writes,code_sha256=ih.hexdigest(),write_sha256=wh.hexdigest())
  def code(u,at,size,_):
   nonlocal index,count,lookup_record
   if at==self.stop:u.emu_stop();return
   if index<len(d['leaves']) and at==d['leaves'][index]['call']['target']:
    c=d['leaves'][index];need(c['kind']=='TASK' and c['call']['new_mappings']==[] and c['call']['pop']==4 and c['call']['result']==c['call']['value']==0,'only exact actual task leaves during confirmation');previous.Replay.leaf(self,c);index+=1;return
   if at==0x4CE9C5:
    p=num(self.read(e.VM+16,4),0)+num(self.read(e.VM+28,4),0);op,n=struct.unpack('<HH',self.read(p,4));commands.append(dict(PC=num(self.read(e.VM+28,4),0),opcode=op,bytes=n,source_pointer=p))
   if at in QUERIES:
    cpu=self.cpu();queries.append(dict(entry=at,CPU=cpu,receiver=cpu['ECX'],stack_hex=self.read(cpu['ESP'],68).hex(),panel_hex=self.read(e.NODE,0xE0).hex(),object_hex=self.read(e.OBJECT,0xAB8).hex()))
    sp=cpu['ESP'];ret=num(self.read(sp,4),0);args=[num(self.read(sp+4+j*4,4),0) for j in range(11)]
    if at==0x4CC0F0:need(cpu['ECX']==e.VM and ret==0x4C5F8C and args[:3]==[4,0x0FFFFFFF,0x0FFFFFFF],'original27 decoded type2 literal ABI')
    if at==0x4128F0 and ret==0x4CCFF7:need(cpu['ECX']==e.MAIN+0x10B8 and args[:2]==[57,0],'original confirmation current keyboard query ABI')
    if at==0x407870 and ret==0x4CBE69:
     need(args[:2] in ([20,0],[32,0]) and num(self.read(cpu['ECX']+0x4C,4),0)==e.MAIN,'original panel/retained portrait group20/32 index0 and current owner')
     group=args[0];lookup_record=self.row['resource_loaded']['record'] if group==20 else self.row['terminal_portrait']['constructed']['record'];need(self.read(e.MAIN+0x844+group*8,8)==struct.pack('<II',lookup_record,1),'original current registered resource bank')
    if at==0x4079C0 and ret==0x4CBEB0:
     need(lookup_record is not None,'panel packet has preceding source resource lookup');packet=self.read(cpu['ECX'],128);record=read(d['before']['memory'],lookup_record,84);need(num(packet,0x48)==lookup_record and num(packet,0x28)==self.row['resource_loaded']['owner_device']['pointer'] and num(packet,0x4C)==e.MAIN and packet[0x34:0x38]==record[0x34:0x38] and packet[0x3C:0x40]==record[0x3C:0x40],'original packet retains current resource format/geometry/device/owner')

   need(0x400000<=at<0x592000 and self.read(at,size)==e.CODE[at-0x400000:at-0x400000+size] and e.CODE[at-0x400000]!=0xCC,'unchanged original confirmation instruction '+hex(at));count+=1;ih.update(struct.pack('<I',at))
  def write(u,access,at,size,value,_):
   nonlocal writes
   need(not 0x400000<=at<0x593000,'no original code or IAT mutation')
   if current['kind']=='keyboard':need(e.KEYBOARD<=at and at+size<=e.KEYBOARD+0xA00 or e.STACK<=at and at+size<=e.STACK+0x20000,'keyboard finite original write extent')
   writes+=1;wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if e.VM<=at<e.VM+0x9400 or e.KEYBOARD<=at<e.KEYBOARD+0xA00 or e.TASK<=at<e.TASK+0x190 or at==0:observed.append(dict(pc=self.cpu()['EIP'],address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
  hooks=[self.u.hook_add(UC_HOOK_CODE,code),self.u.hook_add(UC_HOOK_MEM_WRITE,write)]
  bindings={b['segment_index']:b for b in d['bindings']};frames={f['segments'][1]-1:f for f in d['frames']};starts={f['segments'][0]:f for f in d['frames']};last=d['before']['trace'];boundaries={k:d[k] for k in ('confirmed','panel_completion','ready','font_boundary','final')};seen=set()
  for i,s in enumerate(d['segments']):
   current=s
   if i in starts:need(self.state()==starts[i]['before'] and self.queue()==starts[i]['queue_before'],'entire frame input state and queue')
   need(self.cpu()==s['before_CPU'] and mark()==s['local_before'] and index==s['leaves'][0] and last==s['trace_before'],'continuous confirmation segment input')
   if i in bindings:
    b=bindings[i];f=b['fragment'];need(s['entry']==0x4113D5 and s['stop']==0x4116A4,'only exact original keyboard fragment');need(s['kind']=='keyboard' and s['root'] is None and self.read(e.KEYBOARD,0xA00).hex()==b['before_hex'] and b['before_CPU']==self.cpu() and b['trace_before']==last and b['local_before']==mark(),'exact prebinding keyboard memory/CPU/digests')
    self.u.mem_write(e.KEYBOARD+12,bytes.fromhex(b['capture']['raw_device_hex']));self.put(f['receiver_slot'],struct.pack('<I',e.KEYBOARD))
    for k,v in dict(EBP=f['bp'],ESP=f['sp'],EFLAGS=0x202).items():self.u.reg_write(getattr(x86,'UC_X86_REG_'+k),v)
    need(self.cpu()==s['bound_CPU'],'only declared keyboard root register values')
   else:
    va,recv=((0x40DB90,e.MANAGER),(0x40DC80,e.MANAGER),(0x425DE0,e.INPUT),(0x454CF0,e.TASK))[roots%4];roots+=1;need(s['kind']=='task' and s['entry']==va and s['root']==dict(receiver=recv,args=[]),'only four explicit queue/input/full-task roots')
    self.put(e.STACK+0xF000,struct.pack('<I',e.RETURN));self.u.reg_write(x86.UC_X86_REG_ESP,e.STACK+0xF000);self.u.reg_write(x86.UC_X86_REG_ECX,recv)
   if i not in bindings:need(s['stop']==(d['pending_font']['entry'] if i==len(d['segments'])-1 else e.RETURN),'only natural full roots and final unexecuted font stop')
   self.stop=s['stop'];self.u.emu_start(s['entry'],0,count=4_000_000,timeout=60_000_000)
   need(self.cpu()==s['CPU'] and mark()==s['local_after'] and index==s['leaves'][1],'all57 CPU and every original PC/write at every interval')
   for key in ('instructions','writes'):need(s['trace_after'][key]-last[key]==s['local_after'][key]-s['local_before'][key],'continuous cumulative original counts')
   last=s['trace_after']
   if i in bindings:self.capture(bindings[i]['after'],True);need(self.read(e.KEYBOARD,0xA00).hex()==bindings[i]['after_hex'] and bindings[i]['after']['trace']==last and bindings[i]['after']['local_trace']==mark(),'complete original keyboard after and trace')
   for k,b in boundaries.items():
    if mark()==b['local_trace']:self.capture(b,True);need(b['trace']==last,'whole key boundary original trace');seen.add(k)
   if i in frames:
    f=frames[i];self.capture(f['capture']);need(self.state()==f['after'] and self.queue()==f['queue_after'] and mark()==f['capture']['local_trace'] and last==f['capture']['trace'],'every complete frame original state/queue/digests')
  for h in hooks:self.u.hook_del(h)
  need(roots==4*len(d['frames']) and index==len(d['leaves']) and seen==set(boundaries) and observed==d['writes'] and queries==d['queries'] and commands==d['commands'],'all original intervals, queries, dispatches, writes and key boundaries')
  return dict(instructions=count,writes=writes,CPU_registers=57,whole_regions=len(self.snapshot()))

def source(row):
 d=row['terminal_confirmation'];before=d['before'];raw=(e.ROOT/e.terminal.SCRIPT_PATH).read_bytes();selector=num(bytes.fromhex(before['state']['task']),0x174);seg=next(s for s in previous.script_commands(raw)['segments'] if s['index']=={1:2,4:11}[selector]);start=seg['code_start'];ptr=num(read(before['memory'],e.VM+16,4),0)
 # Decode source command lengths, preserving type2 literal masks.
 commands=[];pc=118
 while len(commands)<3:
  op,n=struct.unpack_from('<HH',raw,start+pc);need(n>=4 and n%2==0,'original bounded script command');commands.append(dict(PC=pc,opcode=op,bytes=n,source_pointer=ptr+pc));pc+=n
 need([(c['PC'],c['opcode'],c['bytes']) for c in commands]==[(118,27,16),(134,43,8),(142,17,6)],'original27/43/17 order')
 need(struct.unpack_from('<3I',raw,start+122)==(0x20000004,0x2FFFFFFF,0x2FFFFFFF) and struct.unpack_from('<I',raw,start+138)[0]==0x20000004 and struct.unpack_from('<H',raw,start+146)[0]==1,'source template4 and type2 literal0fffffff overrides, next text1')
 need(read(before['memory'],ptr+118,30)==raw[start+118:start+148],'current selected script byte identity')
 cfg=list(struct.unpack_from('<19h',e.CODE,0x624520-0x400000+4*38));need(cfg==[7,256,568,0,0,0,0,308,600,715,691,0,0,4,18,12,473,154,1],'entire original template4')
 b=d['font_boundary'];sp=b['CPU']['ESP'];args=[num(read(b['memory'],sp+4+j*4,4),0) for j in range(14)];p=d['pending_font'];need(p==dict(entry=num(read(b['memory'],0x5920A0,4),0),caller=0x4CAD09,args=args,CPU=b['CPU'],first_instruction_executed=False) and b['CPU']['EIP']==p['entry'] and num(read(b['memory'],sp,4),0)==0x4CAD09,'unexecuted source next font complete ABI')
 obj=read(b['memory'],e.OBJECT,0x18);alternate=bool(obj[0x14]);width=num(obj,0xE if alternate else 0xC,'h')&0xFFFFFFFF;height=num(obj,0x12 if alternate else 0x10,'h')&0xFFFFFFFF
 need(num(obj,0,'H')==24 and num(obj,6,'H')==12 and args==[height,width,0,0,400,0,0,0,1,5,0,0,0,0x5BF62C],'template24/line12 and distinct original live text-font fields ABI')
 need(e.CODE[0x4CCFE6-0x400000:0x4CCFF7-0x400000]==bytes.fromhex('8b0dfc497a0081c1b8100000e8f958f4ff'),'original MAIN load and keyboard +10B8/query source bytes')
 rules={0x4CC874:('push','0x2d'),0x4CA410:('add','dx, 1'),0x4CA417:('mov','word ptr [eax + 6], dx'),0x4CA42D:('cmp','edx, ecx'),0x4CA42F:('jle','0x4ca443'),0x4CA434:('mov','word ptr [edx + 6], 0'),0x4CA43D:('mov','word ptr [eax + 2], 2')};md=previous.Cs(previous.CS_ARCH_X86,previous.CS_MODE_32);proof=[]
 for va,want in rules.items():
  ins=next(md.disasm(e.CODE[va-0x400000:va-0x400000+16],va,count=1));need((ins.mnemonic,ins.op_str)==want,'independent original panel45 transition rule');proof.append(dict(va=va,hex=ins.bytes.hex(),mnemonic=ins.mnemonic,operands=ins.op_str))
 return dict(segment=seg['index'],script_sha256=e.sha(raw),configuration4=cfg,commands=commands,panel_transition_rules=proof)

@lru_cache(maxsize=1)
def captured_contract():return keyboard.inputs()

def protocol(row):
 d=row['terminal_confirmation'];contract=captured_contract();scene=76 if row['input']['name']=='neutral_running' else 77;stream=contract['streams'][scene]
 need(d['scene_capture']==scene and d['stream']==stream and len(d['bindings'])==3 and [b['capture'] for b in d['bindings']]==stream['captures'],'pinned76/77 idle press release source capture order')
 for b in d['bindings']:
  old=bytes.fromhex(b['before_hex']);bound=bytearray(old);bound[12:268]=bytes.fromhex(b['capture']['raw_device_hex'])
  need(len(old)==0xA00 and len(bytes.fromhex(b['capture']['raw_device_hex']))==256 and bytes(bound).hex()==b['bound_hex'] and predict_keyboard(bytes(bound)).hex()==b['after_hex'],'independent whole A00 keyboard model')
  bp=e.STACK+0xF800;need(b['only_device_output_written']==dict(pointer=e.KEYBOARD+12,bytes=256) and b['fragment']==dict(va=0x4113D5,bp=bp,sp=bp-0x70,receiver_slot=bp-4,receiver=e.KEYBOARD,stop=0x4116A4),'only raw platform bytes and exact declared original fragment')
 need([bytes.fromhex(b['after_hex'])[0x4B9] for b in d['bindings']]==[0,128,0],'original key high-bit idle press release')
 gt=row['GPU_trace'];p=d['prefix']['GPU_wire'];need(p==26 and len(gt)==39,'four prior texture prefix, four extra observers and original cleanup')
 for i,x in enumerate(gt):need(x['request']['id']==x['reply']['id']==i+1 and x['reply']['ok'] is True,'entire unedited actual native GPU order')
 for j,(key,texture,upload) in enumerate((('GYBC',row['resource_loaded']['texture'],row['resource_loaded']['upload_hex']),('name',row['terminal_name']['texture'],row['terminal_name']['upload_hex']),('portrait',row['terminal_portrait']['texture'],row['terminal_portrait']['upload_hex']),('dialogue',row['terminal_dialogue']['texture'],row['terminal_dialogue']['upload_hex']))):
  original={'GYBC':row['resource_loaded'],'name':row['terminal_name'],'portrait':row['terminal_portrait'],'dialogue':row['terminal_dialogue']}[key]['readback'];need(d['readbacks'][key]==original,'all complete native readback fields preserved '+key)
  receipt=gt[p+j];native=next(x['native'] for x in row['typed_GPU_projection'] if x['guest']==texture['pointer']);need(receipt['request']==dict(id=p+j+1,op='readback',pointer=native) and receipt['reply']['result']==d['readbacks'][key] and receipt['reply']['result']['hex']==upload and receipt['reply']['result']['sha256']==e.sha(bytes.fromhex(upload)),'whole current same-owner texture preserved '+key)
 calls=[x['call'] for x in d['leaves']];actual=row['task_APIs'][d['prefix']['task_APIs']:];need(len(calls)==len(actual) and all(all(c[k]==v for k,v in a.items()) for c,a in zip(calls,actual)),'every added actual task leaf exactly once')


def timing(row):
 d=row['terminal_confirmation'];frames=d['frames'];need([f['phase'] for f in frames[:4]]==['held_confirmation']*2+['captured_press','panel27'],'two no-input tasks then pressed confirmation then released panel27')
 def state(s):v=bytes.fromhex(s['VM']);return num(v,28),num(v,32,'H')
 need(state(d['before']['state'])==(118,1) and all(state(f['after'])==(118,1) for f in frames[:2]) and state(frames[2]['after'])==(118,0) and state(d['confirmed']['state'])==(118,0),'only captured press releases original wait')
 need(state(d['panel_completion']['state'])==(134,1) and state(d['ready']['state'])==(134,0) and state(d['final']['state'])==(142,0),'natural panel complete/display readiness/next font boundary')
 need([c['PC'] for c in d['commands']]==[118,134,142] and [c['opcode'] for c in d['commands']]==[27,43,17],'exact three original dispatches')
 last=d['before']['state']
 for i,f in enumerate(frames):
  need(f['index']==i and f['segments'][1]-f['segments'][0]==4 and f['capture']['state']==f['after'] and f['capture']['queue']==f['queue_after'],'complete four-root frames')
  need(f['after']['remaining']==last['remaining'] and f['after']['elapsed']==last['elapsed'],'world remains paused')
 # Original4CA409..4CA43D zero-extends WORD+6 then uses signed jle45.
 # The VM query precedes the final layer update, requiring another task.
 need(len(frames)==52,'exact46 panel update calls and next readiness task')
 node=e.NODE-e.VM
 for i,f in enumerate(frames[3:50],3):
  raw=bytes.fromhex(f['after']['VM']);status=num(raw,node+2,'H');counter=num(raw,node+6,'H');duration=num(raw,node+0x10,'H')
  want=(3,i-2) if i<=47 else (2,0)
  need((status,counter)==want and duration==45 and state(f['after'])==(134,0 if i==49 else 1),'independent old-value45 fade and extra original VM query')
 need(struct.unpack_from('<3I',bytes.fromhex(d['panel_completion']['state']['VM']),0x9250)==(4,0x0FFFFFFF,0x0FFFFFFF),'literal decoded operands stay0fffffff, not signed minus1')
 need(frames[-2]['phase']=='select_layer7' and frames[-1]['phase']=='next_sentence_font' and all(f['phase']=='panel_readiness' for f in frames[4:-2]),'only panel wait frames followed by43 and partial17')
 return dict(frames=len(frames),complete_tasks=len(frames)-1,partial_tasks=1)

def prefix_view(row):
 """Validation-only old boundary; raw new receipts are checked separately."""
 d=row['terminal_confirmation'];b=d['before'];p=d['prefix'];r=dict(row);r.pop('terminal_confirmation');r.update(final=b['memory'],pending_CPU=b['CPU'],instructions=b['trace']['instructions'],writes=b['trace']['writes'],code_trace_sha256=b['trace']['code_sha256'],write_trace_sha256=b['trace']['write_sha256'],task_APIs=row['task_APIs'][:p['task_APIs']],resource_initialization=row['resource_initialization'][:p['resource_steps']],extra_original_instruction_counts=p['extra_counts'])
 r['GPU_trace']=copy.deepcopy(row['GPU_trace'][:p['GPU_wire']]+row['GPU_trace'][p['GPU_wire']+4:])
 for i,x in enumerate(r['GPU_trace']):x['request']['id']=x['reply']['id']=i+1
 # Only original cleanup CPU metadata differs when the accepted forward stop
 # moves inside the next task. Reconstruct its old-boundary view by executing
 # original destructor bytes; this never changes the raw report.
 old=Replay(row);old.u=Uc(UC_ARCH_X86,UC_MODE_32)
 for m in b['memory']:old.u.mem_map(m['pointer'],m['bytes']);old.u.mem_write(m['pointer'],bytes.fromhex(m['hex']))
 cpu=b['CPU'];first=['GDTR','IDTR','LDTR','TR','CR0','CR2','CR3','CR4']
 for k in first+[k for k in cpu if k not in first]:
  v=tuple(cpu[k]) if isinstance(cpu[k],list) else cpu[k];reg=getattr(x86,'UC_X86_REG_'+k)
  if old.u.reg_read(reg)!=v:old.u.reg_write(reg,v)
 c=copy.deepcopy(row['dialogue_cleanup']);s=copy.deepcopy(next(x for x in row['cleanup_steps'] if x['label']=='supplemental_original_dialogue_texture_destructor'));c['before_CPU']=s['before_cpu']=cpu;s['trace_before']=b['trace'];idx=count=writes=0;old.d=row['terminal_dialogue'];old.cfg=previous.geometry(old.d['raster']['measured']);old.cleaning=True
 def code(u,at,n,_):
  nonlocal idx,count
  if at==e.RETURN:u.emu_stop();return
  if idx<len(c['GPU_APIs']) and at==c['GPU_APIs'][idx]['target']:previous.Replay.leaf(old,dict(kind='GPU',call=c['GPU_APIs'][idx]));idx+=1;return
  need(old.read(at,n)==e.CODE[at-0x400000:at-0x400000+n],'original projected cleanup instruction');count+=1
 def write(*args):
  nonlocal writes
  writes+=1
 h=[old.u.hook_add(UC_HOOK_CODE,code),old.u.hook_add(UC_HOOK_MEM_WRITE,write)];old.put(e.STACK+0xF000,struct.pack('<I',e.RETURN));old.u.reg_write(x86.UC_X86_REG_ESP,e.STACK+0xF000);old.u.reg_write(x86.UC_X86_REG_ECX,e.parent.TEXTURE);old.u.emu_start(0x403730,0,count=10000)
 for x in h:old.u.hook_del(x)
 need(idx==2,'exact original projected cleanup leaves');c['CPU']=s['cpu_after']=old.cpu();s['trace_after']=dict(instructions=b['trace']['instructions']+count,writes=b['trace']['writes']+writes);r['dialogue_cleanup']=c;r['cleanup_steps']=[s if x['label']==s['label'] else x for x in row['cleanup_steps']];return r

def verify_case(row,replay=False,helpers=None):
 d=row['terminal_confirmation'];need(d['before']['local_trace']==dict(instructions=0,writes=0,code_sha256=e.sha(b''),write_sha256=e.sha(b'')),'separate zero-based new original trace');need(all(d['before'][k]==row['terminal_dialogue']['final'][k] for k in ('memory','CPU','state','queue','trace')),'same current live predecessor boundary')
 p=prefix_view(row);need(p['CRT_trace']==row['CRT_trace'] and p['CRT_APIs']==row['CRT_APIs'],'raw CRT protocol remains unprojected');previous.verify_case(p)
 provenance=source(row);protocol(row);timed=timing(row);r=Replay(row);counts=r.execute();f=d['final'];equal(row['final'],f['memory'],'whole actual current final memory');need(row['pending_CPU']==f['CPU'] and row['image_before']==row['image_after'],'all57 final CPU and unchanged original image')
 need((row['instructions'],row['writes'],row['code_trace_sha256'],row['write_trace_sha256'])==(f['trace']['instructions'],f['trace']['writes'],f['trace']['code_sha256'],f['trace']['write_sha256']),'actual cumulative source digests')
 # Raw supplemental destructor really starts from the new partial task CPU.
 r.d=dict(row['terminal_dialogue'],final=f);r.cfg=previous.geometry(row['terminal_dialogue']['raster']['measured']);cleanup=previous.Replay.cleanup(r)
 if replay:
  other=e.run_case(row['input'],helpers[0],helpers[1],[x['result'] for x in row['APIs'] if x['name']=='GetTickCount']);verify_case(other)
  for k in ('initial','final'):equal(row[k],other[k],'new current resources full '+k)
  for k in ('pending_CPU','after_fade','resource_initialization','cleanup_steps','cleanup_state','accounting_baseline','instructions','writes','code_trace_sha256','write_trace_sha256','world_frames','events','commands','task_calls','task_writes','admission'):need(row[k]==other[k],'new current original complete '+k)
  o=other['terminal_confirmation']
  for k in ('before','confirmed','panel_completion','ready','font_boundary','final','segments','frames','commands','writes','queries','pending_font','bindings'):need(d[k]==o[k],'new resources all mapped memory,57CPU,frames and source digests '+k)
 return dict(name=row['input']['name'],VM_PC=142,VM_wait=0,next_font_created=False,source=provenance,scene_capture=d['scene_capture'],no_input_hold_tasks=2,keyboard_fragments=3,full_keyboard_bytes=0xA00,frames=timed,added=counts,supplemental_original_dialogue_destructor=cleanup,predecessor_cleanup_projection=dict(entry=0x403730,source_PC=118,source_wait=1,CPU_independently_reconstructed=True,cumulative_digest_reconstructed=False,raw_report_mutated=False,raw_new_boundary_cleanup_independently_verified=True),current_native_resources_recreated=replay,independent_full_memory_CPU_and_original_trace_replayed=True,original_instructions=row['instructions'],original_writes=row['writes'])

def verify(path):
 data=json.loads(gzip.decompress(path.read_bytes()));need(data['source_contract']==e.source_contract() and [r['input'] for r in data['cases']]==e.parent.parent.overlay.parent.corpus(),'exact source and both terminal branches');h=e.helpers('terminal-confirmation-proof');rows=[]
 for row in data['cases']:rows.append(verify_case(row,True,h));print('independent current confirmation',row['input']['name'],flush=True)
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(e.ROOT).as_posix()),cases=rows,implementation_sha256={p:e.sha((e.ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},current_native_resources_recreated=True,independent_full_memory_CPU_and_original_trace_replayed=True,new_forward_VM_roots=0,derived_input_host_writes=0,PC_or_wait_host_writes=0,new_OS_input=False,next_font_created=False,draw_or_Present=False,terminal_presentation_complete=False,task_exit_complete=False,rewards_complete=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();need(not(e.ROOT/a.out).exists(),'fresh immutable proof');e.terminal.save(a.out,verify(e.ROOT/a.report))

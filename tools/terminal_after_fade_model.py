"""Independent complete task-state rules from WORK59 to the original name-font leaf."""
import copy,struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools import terminal_after_fade_emulation as e
from tools import terminal_overlay_model as old
need=e.need
num=old.number
read=old.read

def source_rules():
 checks={0x497B4D:('mov','dword ptr [ecx + 0x2490], edx'),0x497BB7:('mov','dword ptr [edx + 0x249c], ecx'),0x497BD1:('mov','byte ptr [ecx + 0x2499], 0'),0x497C0A:('mov','byte ptr [edx + 0x249a], 2'),0x497C11:('call','0x4977a0'),0x4977B8:('mov','byte ptr [0x7e0f08], 0'),0x4CFF41:('mov','word ptr [edx + ecx + 0x20], 0'),0x4CCC2C:('mov','word ptr [edi + ecx + 0x28], ax'),0x4CCC33:('jle','0x4ccc39'),0x4CCDFF:('mov','byte ptr [ecx + 0x1cd], 0'),0x4CA7C5:('call','dword ptr [0x5920a0]')}
 md=Cs(CS_ARCH_X86,CS_MODE_32);rows=[]
 for p,want in checks.items():
  i=next(md.disasm(e.CODE[p-0x400000:p-0x400000+16],p));need((i.mnemonic,i.op_str)==want,'exact original after-fade instruction '+hex(p));rows.append(dict(va=p,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
 need(struct.unpack_from('<f',e.CODE,0x59E8BC-0x400000)[0]==38912.0 and int(38912/60)==648,'original truncated fade constant')
 return rows

def prefix_view(row):
 r={k:copy.deepcopy(v) for k,v in row.items() if k!='after_fade'};p=row['after_fade']['prefix'];r.update(overlay_continuation=copy.deepcopy(p['continuation']),pending_CPU=p['CPU'],final=p['memory'],task_calls=p['task_calls'],task_writes=p['task_writes'],task_APIs=p['task_APIs'],resource_initialization=p['resource_steps'],instructions=p['trace']['instructions'],writes=p['trace']['writes'],code_trace_sha256=p['trace']['code_sha256'],write_trace_sha256=p['trace']['write_sha256'])
 return r

def queue(expected,actual,prefix,complete):
 # The verified prefix independently fixed all92 bytes. The original reset
 # resets cursor/heads but preserves arena bytes, including the pending tail.
 manager=bytearray.fromhex(prefix['manager']);arena=prefix['arena_pointer'];struct.pack_into('<I',manager,0x30,arena+(92 if complete else 0));heads=bytearray(4096*8)
 if complete:struct.pack_into('<II',heads,51*8,arena,0)
 block=bytes.fromhex(prefix['arena']);need(len(block)==92,'verified original sprite record')
 wanted=dict(manager=manager.hex(),heads=heads.hex(),arena_pointer=arena,used=92 if complete else 0,arena=block.hex() if complete else '',unused_tail_sha256=e.sha(bytes(65536-92) if complete else block+bytes(65536-92)))
 need(actual==wanted,'entire queue headers, sprite/cursor and preserved unused bytes')

def verify(row):
 rules=source_rules();f=row['after_fade'];p=f['prefix'];frames=f['frames'];need(len(frames)==96,'59 fade updates + poll/display/release/text/timer +31 polls + partial role')
 expected=copy.deepcopy(p['state']);need(expected==p['continuation']['after'] and p['CPU']==p['continuation']['after_CPU'],'exact complete preceding PC52 boundary')
 vm0=bytes.fromhex(expected['VM']);work0=bytes.fromhex(expected['work']);need(num(vm0,28)==52 and num(vm0,0x20,'H')==4 and vm0[0x92E0]==1 and num(work0,0x249C)==59,'genuine WORK59 and VM wait-kind4')
 base_queue=frames[0]['queue_before'];old.queue(p['memory'],row['resource_loaded']['record']);queue(None,base_queue,base_queue,True)
 selector=num(bytes.fromhex(expected['task']),0x174);start={1:788,4:2780}[selector];role={1:2,4:1}[selector];script=(e.ROOT/e.terminal.SCRIPT_PATH).read_bytes()
 want_commands=[]
 for pc,op,n in ((52,56,8),(60,20,8),(68,12,8),(76,30,20)):
  need(struct.unpack_from('<HH',script,start+pc)==(op,n),'actual terminal instruction header');want_commands.append(dict(PC=pc,opcode=op,bytes=n,source_offset=start+pc))
 need(f['commands']==want_commands,'only the four naturally nested post-fade VM commands')
 need(struct.unpack_from('<I',script,start+56)[0]==0x20000002 and struct.unpack_from('<I',script,start+64)[0]==0x20000000 and struct.unpack_from('<I',script,start+72)[0]==0x2000001E,'literal display2, text0 and timer30')
 operands=struct.unpack_from('<4I',script,start+80);need(operands==(0x20000008,0x20000000+role,0x20000000,0x2000001E),'complete literal role command')
 config=list(struct.unpack_from('<19h',e.CODE,0x624520-0x400000+8*38));need(config[0]==5,'source configuration8 selects layer5');node=0x6F60+5*0xE0;obj=0x430+5*0xAB8
 arena=base_queue['arena_pointer'];last_queue=base_queue
 def put(field,o,value,fmt='I'):
  b=bytearray.fromhex(expected[field]);struct.pack_into('<'+fmt,b,o,value);expected[field]=b.hex()
 def store(pc,address,value,n):return dict(pc=pc,address=address,bytes=n,value=value)
 total_calls=total_writes=0;api=len(p['task_APIs']);before_trace=p['trace']
 for i,frame in enumerate(frames):
  need(frame['index']==i and frame['before']==expected and frame['trace_before']==before_trace,'continuous independently predicted frame input and trace')
  need(frame['queue_before']==last_queue,'continuous exact queue contents')
  roots=row['resource_initialization'][frame['queue_roots'][0]:frame['queue_roots'][1]]
  need([x['entry'] for x in roots]==[0x40DB90,0x40DC80] and all(x['receiver']==e.MANAGER and x['args']==[] for x in roots),'two explicit source queue roots only')
  need(roots[0]['trace_before']==before_trace and roots[0]['trace_after']==roots[1]['trace_before'] and roots[1]['trace_after']==frame['reset']['trace_before'],'uninterrupted queue/root/reset digest chain')
  put('owner',0x1088,arena);reset=frame['reset'];need(reset['before']==expected,'source queue reset only changes owner arena cursor')
  put('owner',0x7B0,0,'B');need(reset['after']==expected and reset['call']['result']==0,'whole original input reset state')
  task=frame['task'];need(task['before']==expected and reset['trace_after']==task['trace_before'],'same reset state enters full source task')
  put('owner',0x7B0,255,'B')
  if i<59:
   value=648*(i+2);remaining=58-i;put('work',0x2490,value,'i');put('work',0x249C,remaining,'i')
   stores=[store(0x497B4D,e.WORK+0x2490,value,4),store(0x497BB7,e.WORK+0x249C,remaining,4)]
   if remaining:
    stores.append(store(0x497C22,e.WORK+0x249A,1,1))
   else:
    put('work',0x2499,0,'B');put('work',0x249A,2,'B');put('VM',0x92E0,0,'B');stores += [store(0x497BD1,e.WORK+0x2499,0,1),store(0x497C0A,e.WORK+0x249A,2,1),store(0x4977B8,e.VM+0x92E0,0,1)]
   observed=[x for x in f['writes'][frame['writes'][0]:frame['writes'][1]] if e.WORK+0x2490<=x['address']<e.WORK+0x24A0 or x['address']==e.VM+0x92E0]
   need(observed==stores,'all actual fade stores, original PCs and strict end order')
  elif i==59:put('VM',0x20,0,'H')
  elif i in (60,62,63,95):
   count=num(bytes.fromhex(expected['VM_counter']),0);put('VM_counter',0,count+1);put('VM_counter',4,0)
   pc,op,n={60:(60,56,8),62:(68,20,8),63:(76,12,8),95:(76,30,20)}[i];put('VM',28,pc);put('VM',0x22,op,'H');put('VM',0x24,n,'H')
   if i==60:
    put('VM',0x20,1,'H');put('VM',0x9250,2)
    for j,x in enumerate((0,2,0,16)):put('VM',0x9248+j*2,x,'H')
   elif i==62:put('VM',0x9228,0,'B');put('VM',0x9250,0)
   elif i==63:
    put('VM',0x20,1,'H');put('VM',0x1CD,1,'B');put('VM',0x26,12,'H');put('VM',0x28,0,'H');put('VM',0x2A,30,'H');put('VM',0x2C,0);put('VM',0x9250,30)
   else:
    for j,x in enumerate((8,role,0,30)):put('VM',0x9250+4*j,x)
    words={0:1,2:1,6:0,8:config[18],0xC:config[1],0xE:config[2],0x10:8,0x16:config[14],0x18:config[15],0x1A:config[16],0x1C:config[17],0x1E:config[7],0x20:config[8],0x30:config[4],0x40:32,0x42:33,0x4C:config[11],0x56:config[12],0x58:config[13]}
    for at,x in words.items():put('VM',node+at,x,'H')
    for at,x,fmt in ((0,24,'H'),(4,0,'B'),(6,12,'H'),(10,0,'B')):put('VM',obj+at,x,fmt)
  else:
   oldcount=num(bytes.fromhex(expected['VM_counter']),4);put('VM_counter',0,0);put('VM_counter',4,oldcount+1)
   if i==61:put('VM',0x20,0,'H')
   else:
    old_timer=i-64;put('VM',0x28,old_timer+1,'H')
    if old_timer>29:put('VM',0x1CD,0,'B');put('VM',0x20,0,'H')
  complete=i<95
  if complete:put('owner',0x1088,arena+92)
  need(task['after']==expected,'entire independent WORK/VM/owner/task/unit/clock frame '+str(i))
  need(task['returned'] is complete and task['CPU']['EIP']==(e.RETURN if complete else f['pending']['entry']),'actual complete vs suspended root')
  if complete:need(task['CPU']['ESP']==e.STACK+0xF004 and expected['SEH']=='00000000','natural original task return and exception head')
  queue(None,frame['queue_after'],base_queue,complete);last_queue=frame['queue_after'];before_trace=task['trace_after']
  need(frame['calls'][0]==total_calls and frame['writes'][0]==total_writes and frame['APIs']==[api,api+2],'all compact observations, writes and two actual input leaves per frame')
  total_calls=frame['calls'][1];total_writes=frame['writes'][1];api+=2
 need(total_calls==len(f['calls']) and total_writes==len(f['writes']) and api==len(row['task_APIs']),'all added observations included')
 need(f['final']==expected and f['CPU']==frames[-1]['task']['CPU'] and f['trace']==before_trace,'complete final independent state/CPU/trace')
 pfont=f['pending'];cpu=pfont['CPU'];need(pfont['kind']=='CreateFontA' and pfont['entry']==num(e.CODE,0x5920A0-0x400000) and pfont['first_instruction_executed'] is False,'original font IAT target before its first instruction')
 need(pfont['args']==[20,0,0,0,700,0,0,0,1,5,0,0,0,0x5BF62C] and pfont['caller']==0x4CA7CB and pfont['receiver']==e.VM+node,'exact source font14 ABI and layer receiver')
 stack=bytes.fromhex(pfont['stack']);need(len(stack)==0x20000 and pfont['SEH']=='00000000','whole retained source stack and SEH')
 bp=cpu['EBP'];chain=[]
 for ret in (0x4CC1DE,0x4C62D4,0x4CEDA7,0x454D90,e.RETURN):
  need(num(stack,bp-e.STACK+4)==ret,'natural original font ancestor '+hex(ret));chain.append(bp);bp=num(stack,bp-e.STACK)
 need(chain==[e.STACK+0xEE28,e.STACK+0xEEA0,e.STACK+0xEF08,e.STACK+0xEF98,e.STACK+0xEFFC] and cpu['ESP']==chain[0]-0x148-12-56-4,'independent five original stack-frame sizes')
 need(num(stack,chain[0]-e.STACK+8)==(e.VM&0xFFFF0000)|role,'original narrow role argument retains source high bits')
 need([f['calls'][j]['entry'] for j in pfont['open_calls']]==[0x454CF0,0x4CE8F0,0x4C61C0] and all('cpu_after' not in f['calls'][j] for j in pfont['open_calls']),'three observed pending roots remain suspended')
 need(row['pending_CPU']==cpu and read(row['final'],e.STACK,0x20000)==stack,'pending complete CPU and every source stack byte retained')
 need(num(bytes.fromhex(expected['work']),0x2490)==38880 and num(bytes.fromhex(expected['work']),0x249C)==0 and bytes.fromhex(expected['work'])[0x249A]==2,'unmodified residual fade endpoint')
 return dict(name=row['input']['name'],selector=selector,extra_complete_tasks=95,pending_tasks=1,total_complete_tasks=100,fade_updates=59,fade_value=38880,fade_remaining=0,WORK_wait=0,VM_PC=76,VM_wait=0,timer_polls=31,timer_count=31,post_fade_commands=[56,20,12,30],role=role,layer=5,font_entry=pfont['entry'],font_executed=False,owned_regions=len(row['final']),CPU_registers=57,original_instructions=row['instructions'],original_writes=row['writes'],source_rules=rules)

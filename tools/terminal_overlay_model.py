"""Independent GYBC bytes, source query packet, queue, branch and WORK wait rules."""
import copy,struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools import terminal_overlay_emulation as e
from tools import terminal_task_model as previous
from tools.battle_lethal_combat import expand
need=e.need

def number(b,o,f='I'):return struct.unpack_from('<'+f,b,o)[0]

def read(rows,p,n):
 parts=[];end=p+n;cursor=p
 for r in rows:
  lo,hi=r['pointer'],r['pointer']+r['bytes']
  if lo<=cursor<hi:
   b=bytes.fromhex(r['hex']);need(len(b)==r['bytes'],'complete mapped bytes');stop=min(hi,end);parts.append(b[cursor-lo:stop-lo]);cursor=stop
   if cursor==end:return b''.join(parts)
 raise ValueError('complete owned memory for '+hex(p))


def source_rules():
 raw=e.CODE;md=Cs(CS_ARCH_X86,CS_MODE_32)
 checks={0x4078FF:('call','0x41f5a0'),0x407907:('mov','dword ptr [ecx + 0x48], eax'),0x40799A:('mov','ecx, dword ptr [ebp - 4]'),0x4079A0:('call','0x4142b0'),0x407B15:('jne','0x407b21'),0x407B2F:('call','0x40dcd0'),0x40810A:('call','0x40df20'),0x416846:('call','0x41f090'),0x41F1E1:('mov','dword ptr [eax + edx*8], ecx'),0x41F1ED:('mov','dword ptr [eax + edx*8 + 4], ecx'),0x42D9C7:('mov','byte ptr [ecx + 0x92e0], 1'),0x4C20A4:('sete','cl'),0x4C24CF:('mov','dword ptr [ecx + eax + 0x1c], edx')}
 out=[]
 for a,want in checks.items():
  i=next(md.disasm(raw[a-0x400000:a-0x400000+16],a));need((i.mnemonic,i.op_str)==want,'exact original overlay instruction '+hex(a));out.append(dict(va=a,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
 return out

def prefix(row):
 # The prior independently proven task rules apply after factoring out the
 # immutable, explicitly source-initialized render-owner fields. Verify those
 # complete bytes before projecting the old empty-owner view.
 r=copy.deepcopy(row);a=r['admission'];loaded=r['resource_loaded'];owner=read(loaded['memory'],e.MAIN,65536)
 steps=[s for f in a['frames'] for s in f]+[a['reset'],a['partial']]
 for s in steps:
  for side in ('before','after'):
   actual=bytes.fromhex(s[side]['owner']);expected=bytearray(owner);expected[0x7B0]=actual[0x7B0]
   need(actual==bytes(expected),'all source-initialized owner bytes preserved through task admission')
   b=bytearray(65536);b[0x180:0x800]=actual[0x180:0x800];s[side]['owner']=b.hex()
 r['pending_CPU']=a['partial']['pending']['CPU']
 for index in a['partial']['pending']['open_calls']:
  for k in ('after','cpu_after','result'):r['task_calls'][index].pop(k,None)
 return previous.verify(r)

def expected_record(row):
 l=row['resource_loaded'];b=bytearray(84);struct.pack_into('<II',b,0x28,l['owner_device']['pointer'],l['texture']['pointer']);struct.pack_into('<I4H',b,0x34,25,512,512,512,512);struct.pack_into('<H',b,0x44,2);b[0x46:0x48]=b'\xcd\xcd';return bytes(b)

def queue(memory,record):
 manager=read(memory,e.MANAGER,0x38);heads=number(manager,16);arena=number(manager,20)
 need(number(manager,0)==e.MAIN and number(manager,8)==4096 and number(manager,12)==65536,'original initialized queue owner and capacities')
 need(number(manager,0x2C)==0 and number(manager,0x30)==arena+92,'one original 92-byte command in reset arena')
 tables=bytearray(4096*8);struct.pack_into('<II',tables,51*8,arena,0);need(read(memory,heads,len(tables))==bytes(tables),'all 4096 complete original queue heads/tails')
 q=bytearray(92);struct.pack_into('<II',q,0,0,1);q[8:10]=b'\x00\x01'
 for o,values in ((0xC,[-0.5,19.5,19.5,-0.5]),(0x1C,[-0.5,-0.5,29.5,29.5]),(0x2C,[424/512,444/512,444/512,424/512]),(0x3C,[24/512,24/512,54/512,54/512])):struct.pack_into('<4f',q,o,*values)
 struct.pack_into('<IIIH',q,0x4C,0xFF808080,record,0,51)
 need(read(memory,arena,92)==bytes(q),'every byte of original layer51 sprite queue record')
 need(read(memory,arena+92,65536-92)==bytes(65536-92),'entire bounded arena unused tail remains original zero fill')
 return dict(heads=heads,arena=arena,layer=51,record_bytes=92)

def verify(row):
 rules=source_rules();need(row['input'] in e.parent.corpus(),'exact terminal overlay cases');l=row['resource_loaded'];record=l['record'];raw=e.RESOURCE
 need(raw[:4]==bytes.fromhex('18000800') and number(raw,4)==1 and number(raw,8)==12 and raw[12:14]==b'DX','original one-entry GYBC container')
 need(struct.unpack_from('<5H',raw,14)==(2,512,512,512,512) and len(raw)==524312,'complete original DX2 geometry')
 need(bytes.fromhex(l['record_hex'])==expected_record(row) and read(l['memory'],record,84)==expected_record(row),'every original IMAGE byte including CD padding')
 need(l['bank']==struct.pack('<II',record,1).hex() and read(l['memory'],e.BANK,8).hex()==l['bank'],'original group20 record/count publication')
 need(l['owner_device']['pointer']==number(read(l['memory'],e.MAIN+0xB210,4),0) and read(l['memory'],e.MAIN+0xB28E,2)==b'\x01\x00','actual current device and enabled original drawing gate')
 pixels=raw[24:];need(bytes.fromhex(l['upload_hex'])==pixels and l['readback']['hex']==pixels.hex() and l['readback']['sha256']==e.sha(pixels),'all 262144 original pixels independently equal current actual whole surface readback')
 need(l['lock']['pitch']==1024 and len(bytes.fromhex(l['lock']['hex']))==524288,'actual whole512x512 bounded surface')
 prefix_result=prefix(row);c=row['overlay_continuation'];need(c['before_CPU']==row['admission']['partial']['pending']['CPU'],'exact same pending original CPU continues407870')
 first=c['first_task'];need(first['after_CPU']['EIP']==e.RETURN and first['after_CPU']['ESP']==e.STACK+0xF004 and number(bytes.fromhex(first['after']['VM']),28)==8,'third task naturally returns PC8')
 need(first['after']['SEH']=='00000000','original SEH restored at completed task');q=queue(first['memory'],record)
 need(len(c['frames'])==2 and [x['opcode'] for x in c['commands']]==[167,8,117] and [x['PC'] for x in c['commands']]==[0,8,44] and [x['bytes'] for x in c['commands']]==[8,20,8],'original three commands with taken conditional jump, no166/11')
 sub={1:788,4:2780}[number(bytes.fromhex(row['admission']['partial']['after']['task']),0x174)]
 for x in c['commands']:
  p=sub+x['PC'];need(x['source_offset']==p and struct.unpack_from('<HH',(e.ROOT/e.terminal.SCRIPT_PATH).read_bytes(),p)==(x['opcode'],x['bytes']),'actual selected script instruction identity')
 # Script8 uses relation1 (equal), variable0 and immediate1; original167 sets variable0=1.
 script=(e.ROOT/e.terminal.SCRIPT_PATH).read_bytes();need(struct.unpack_from('<HH4I',script,sub+8)==(8,20,1,0,0x20000001,44),'source equality variable0 == immediate1 jumps44');need(number(e.CODE,0x4C2106-0x400000)==0x4C209C,'source relation1 equality table');need(script[sub:sub+8]==struct.pack('<HHI',167,8,0),'source variable instruction')
 vm=bytes.fromhex(c['after']['VM']);work=bytes.fromhex(c['after']['work']);need(number(vm,28)==52 and number(vm,0x3C)==1 and vm[0x92E0]==1,'natural final PC52 variable1 and original WORK wait')
 need(number(vm,0x9250)==60 and number(work,0x2490)==648 and number(work,0x2494)==648 and work[0x2498:0x249B]==b'\x01\x01\x01' and number(work,0x249C)==59,'natural117 and first full-task work update, original truncation648')
 need(number(bytes.fromhex(c['frames'][0]['task']['after']['VM']),28)==44 and bytes.fromhex(c['frames'][0]['task']['after']['VM'])[0x92E0]==0,'conditional VM task naturally reaches44 before117')
 need(c['after_CPU']['EIP']==e.RETURN and c['after_CPU']['ESP']==e.STACK+0xF004 and c['after']['SEH']=='00000000','all original task and VM frames return with restored SEH');queue(c['memory'],record)
 need(c['after']['remaining']==row['admission']['partial']['after']['remaining'] and c['after']['elapsed']==row['admission']['partial']['after']['elapsed'],'original paused clock stays frozen')
 calls=c['calls'];need([x['entry'] for x in calls]==[0x407870,0x41F5A0,0x407AD0,0x40DCD0,0x40DF20]*3,'three complete original overlay query/queue call chains')
 expected=bytearray.fromhex(previous.packet_project(0x40));struct.pack_into('<I',expected,0x28,l['owner_device']['pointer']);struct.pack_into('<I',expected,0x48,record);struct.pack_into('<4H',expected,0x38,512,512,512,512);struct.pack_into('<H',expected,0x58,0xC0)
 for i,x in enumerate(calls):
  need('cpu_after' in x and len(x['cpu_before'])==len(x['cpu_after'])==57 and x['cpu_after']['EIP']==x['caller'] and x['cpu_after']['ESP']==x['return_ESP'],'actual complete nested CPU/return ABI')
  if x['entry'] in (0x407870,0x41F5A0):need(x['args']==[20,0],'original resource query args')
  if x['entry']==0x407870:need(x['result']==0 and x['packet_after']==expected.hex(),'all128 original query packet bytes and successful return')
  if x['entry']==0x41F5A0:need(x['result']==record,'actual source record pointer returned')
 need([x['op'] for x in row['GPU_APIs']]==['create','describe','lock','unlock','describe','release'] and all(x['actual_API_executed'] and x['value']==0 for x in row['GPU_APIs']),'six actual current COM calls, original supplemental destructor')
 need(row['cleanup_state']['bank']==bytes(8).hex() and {k:row['cleanup_state'][k] for k in row['accounting_baseline']}==row['accounting_baseline'],'original release/clear/free and unchanged accounting baselines')
 need(row['CRT_cleanup']['all_owned_resources_released'] and row['GPU_cleanup']['all_owned_resources_released'] and row['CRT_exit']==row['GPU_exit']==0,'normal current native helper and all resource cleanup')
 return dict(name=row['input']['name'],selector=number(bytes.fromhex(c['after']['task']),0x174),VM_PC=52,VM_commands=3,complete_task_returns=5,overlay_queries=3,original_pixels=262144,current_GPU_calls=6,actual_CRT_leaves=len(row['CRT_APIs']),actual_task_leaves=len(row['task_APIs']),queue=q,remaining=c['after']['remaining'],elapsed=c['after']['elapsed'],owned_regions=len(row['final']),CPU_registers=57,original_instructions=row['instructions'],original_writes=row['writes'],WORK_wait=1,WORK_remaining=59,source_rules=rules)

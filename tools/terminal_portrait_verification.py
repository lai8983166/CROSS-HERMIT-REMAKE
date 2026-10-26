"""Independent terminal portrait pixels, native contracts and original task replay."""
import argparse,copy,gzip,hashlib,json,struct,types
from types import SimpleNamespace
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
import unicorn.x86_const as x86
from tools import terminal_portrait_emulation as e
from tools import terminal_name_verification as previous
from tools import school_retained_crt_fixture_verification as crtcheck
from tools.school_retained_portrait_file_catalog import parse
from tools.school_character_animation_catalog import source_rules as animation_rules
need=e.need;num=previous.num;read=previous.read;equal=previous.overlay.memory_equal
IMPLEMENTATIONS=('tools/terminal_portrait_emulation.py','tools/terminal_portrait_verification.py','tools/terminal_portrait_preservation.py','tools/terminal_portrait_crt_platform.cs','tools/terminal_portrait_d3d8_platform.cs')

def prefix_view(row):
 r={k:copy.deepcopy(v) for k,v in row.items() if k not in ('terminal_portrait','portrait_cleanup')};p=row['terminal_portrait'];n=r['terminal_name'];before=p['prefix']
 r.update(final=n['memory'],pending_CPU=n['CPU'],instructions=n['trace']['instructions'],writes=n['trace']['writes'],code_trace_sha256=n['trace']['code_sha256'],write_trace_sha256=n['trace']['write_sha256'],resource_initialization=r['resource_initialization'][:before['resource_steps']],task_APIs=r['task_APIs'][:before['task_APIs']],extra_original_instruction_counts=before['extra_counts'])
 r['GPU_trace']=r['GPU_trace'][:11]+r['GPU_trace'][-5:]
 for i,x in enumerate(r['GPU_trace']):x['request']['id']=x['reply']['id']=i+1
 r['CRT_APIs']=r['CRT_APIs'][:before['CRT_APIs']]+r['CRT_APIs'][row['portrait_cleanup']['old_CRT_cleanup_start']:];trace=[]
 for api in r['CRT_APIs']:
  start,end=api['wire_start'],api['wire_end'];api['wire_start']=len(trace);trace.extend(copy.deepcopy(r['CRT_trace'][start:end]));api['wire_end']=len(trace)
 trace.append(copy.deepcopy(r['CRT_trace'][-1]));r['CRT_trace']=trace
 for i,x in enumerate(trace):x['request']['id']=x['reply']['id']=i+1
 r['cleanup_steps']=[x for x in r['cleanup_steps'] if x['label']!='supplemental_original_portrait_container_destructor']
 return r

def pixels(row):
 p=row['terminal_portrait'];role=2 if row['input']['name']=='neutral_running' else 1;catalog,_=previous.source_names();source=catalog['roles'][str(role)];raw=(e.ROOT/source['image_path']).read_bytes();need(e.sha(raw)==source['image_sha256'] and p['source']==source and p['container']==parse(raw) and p['role']==role,'fixed complete original portrait identity')
 need(p['path']=='data\\adv\\bin\\'+source['filename'] and p['constructed']['file_hex']==raw.hex(),'entire actual selected portrait file')
 need(struct.unpack_from('<3I6H',raw)==(262168,1,12,0x5844,2,256,512,256,512),'independent raw source container/header geometry');lock=p['lock'];need(lock['pitch']==512 and len(bytes.fromhex(lock['hex']))==262144,'entire current portrait surface extent')
 need(p['upload_hex']==p['readback']['hex']==raw[24:].hex() and p['readback']['sha256']==e.sha(raw[24:]),'all131072 original texels equal actual entire source GPU readback')
 need(len(p['copy_rows'])==512,'all source rows present')
 for i,x in enumerate(p['copy_rows']):need(x==dict(row=i,args=[lock['bits']+512*i,p['constructed']['file_pointer']+24+512*i,512],caller=0x40483F),'independent original memcpy row '+str(i))
 need(p['GYBC_readback']['hex']==row['resource_loaded']['upload_hex'] and p['name_readback']['hex']==row['terminal_name']['upload_hex'],'both current prior surfaces survive portrait/task updates')
 return raw

def native(row):
 p=row['terminal_portrait'];gt=row['GPU_trace'];ct=row['CRT_trace']
 for label,trace in [('GPU',gt),('CRT',ct)]:
  for i,x in enumerate(trace):need(x['request']['id']==x['reply']['id']==i+1 and x['reply']['ok'] is True,'raw actual ordered '+label+' protocol')
 need([x['request']['op'] for x in gt]==['create','describe','lock','unlock','readback']*2+['readback']+['create','describe','lock','unlock','readback']+['readback','readback']+['describe','release']*3+['close'],'three simultaneously owned textures / whole readbacks / original releases / close')
 calls=row['GPU_APIs'][:4]+row['terminal_name']['GPU_APIs']+p['GPU_APIs']+row['portrait_cleanup']['GPU_APIs']+row['name_cleanup']['GPU_APIs']+row['GPU_APIs'][4:]
 need(len(calls)==18 and len(p['GPU_APIs'])==4 and len(row['portrait_cleanup']['GPU_APIs'])==2,'all18 original COM leaves recorded')
 for a,i in zip(calls,(0,1,2,3,5,6,7,8,11,12,13,14,18,19,20,21,22,23)):
  need(a['native_result']==gt[i]['reply']['result'] and a['op']==gt[i]['request']['op'] and a['actual_API_executed'] is True,'every original COM leaf exact current native receipt')
 need(gt[15]['reply']['result']==p['readback'] and gt[14]['request']['hex']==p['upload_hex'] and gt[16]['reply']['result']==p['GYBC_readback'] and gt[17]['reply']['result']==p['name_readback'],'source full upload and retained current resource readbacks')
 need(row['GPU_cleanup']==gt[-1]['reply']['result'] and not row['GPU_cleanup']['texture_releases'] and row['CRT_cleanup']==ct[-1]['reply']['result'] and row['CRT_cleanup']['all_owned_resources_released'] and row['CRT_exit']==row['GPU_exit']==0,'no helper fallback releases and normal original cleanup/exit')
 covered=[]
 for a in row['CRT_APIs']:covered.extend(range(a['wire_start'],a['wire_end']))
 for r in p['constructed']['native_allocation_readbacks']:
  i=r['wire_index'];covered.extend((i-1,i));need(ct[i-1]['request']['op']=='sync' and ct[i]['request']==dict(id=i+1,op='readback',pointer=r['result']['pointer']) and ct[i]['reply']['result']==r['result'] and len(bytes.fromhex(r['result']['hex']))==r['bytes'],'explicit entire native file/vector readback')
 need(sorted(covered)==list(range(len(ct)-1)),'all actual native CRT operations classified once; only final close remains')
 need(row['portrait_cleanup']['bank_hex']==bytes(8).hex() and row['portrait_cleanup']['texture_bytes']==row['terminal_name']['accounting'] and row['portrait_cleanup']['game_bytes']==row['accounting_baseline']['game_bytes']+32768+65536+88,'original portrait/vector destructor preserves predecessor resources/accounting')

class Replay(previous.Replay):
 """Independent original bytes, strict CRT transcript and checked COM outputs."""
 def __init__(self,row):
  self.row=row;self.p=row['terminal_portrait'];self.n=dict(before=self.p['before']);self.u=Uc(UC_ARCH_X86,UC_MODE_32);self.image=e.CODE;self.objects={};self.locks={}
  for r in self.p['before']['memory']:self.u.mem_map(r['pointer'],r['bytes']);self.u.mem_write(r['pointer'],bytes.fromhex(r['hex']))
  c=self.n['before']['CPU'];first=['GDTR','IDTR','LDTR','TR','CR0','CR2','CR3','CR4']
  for k in first+[k for k in c if k not in first]:
   reg=getattr(x86,'UC_X86_REG_'+k);v=tuple(c[k]) if isinstance(c[k],list) else c[k]
   if self.u.reg_read(reg)!=v:self.u.reg_write(reg,v)
  need(self.cpu()==c,'all57 source CPU values restored at original IMAGE entry')
  self.case=dict(native_trace=row['CRT_trace'],native_hello=row['current_CRT_hello'],fixture_inputs=dict(heap_token_translation=dict(guest=num(self.read(0x80AB28),0))))
  self.blocks={int(k):copy.deepcopy(v) for k,v in self.p['prefix']['allocations'].items()};self.history=copy.deepcopy(self.p['prefix']['history']);self.files=set();self.depth=0;self.wire=row['CRT_APIs'][self.p['prefix']['CRT_APIs']]['wire_start'];self.filebytes=(e.ROOT/self.p['source']['image_path']).read_bytes();self.native_file=None
  sizes=tuple(r['bytes'] for r in self.history)+(262208,128);old=crtcheck.Replay.api
  def constants(code):
   values=[]
   for v in code.co_consts:
    if isinstance(v,types.CodeType):v=constants(v)
    elif v==(262208,128,262208):v=sizes
    elif v==(262168,88,262168):v=(0,262168)
    elif v==b'data\\adv\\bin\\sc004.bin':v=self.p['path'].encode()
    elif v=='data\\adv\\bin\\sc004.bin':v=self.p['path']
    values.append(v)
   return code.replace(co_consts=tuple(values))
  self.crt_api=types.FunctionType(constants(old.__code__),old.__globals__)
 def locate(self,p,n=1):return crtcheck.Replay.locate(self,p,n)
 def sync(self,p):return crtcheck.Replay.sync(self,p)
 def consume(self,op,**kw):
  if 'handle' in kw:need(kw['handle']==0x62001000 and self.native_file is not None,'current logical file only');kw['handle']=self.native_file
  need(self.wire<len(self.case['native_trace']),'bounded native cursor');t=self.case['native_trace'][self.wire];need(t['request']==dict(id=self.wire+1,op=op,**kw),'independent actual native request '+op);self.wire+=1;r=copy.deepcopy(t['reply']['result'])
  if op=='open':need(0<r['handle']<0xFFFFFFFF,'actual current file');self.native_file=r['handle'];r['handle']=0x62001000
  elif op=='file_close':self.native_file=None
  elif op in ('enter','leave'):
   b=bytearray.fromhex(r['critical_hex'])
   for off in (0,12,16):
    if num(b,off) not in (0,0xFFFFFFFF):struct.pack_into('<I',b,off,0x63000000+off+(0x80A4B0-0x80A480)*0x100)
   r['critical_hex']=b.hex()
  return r
 def leaf(self,item):
  kind=item['kind'];a=item['call'];sp=self.cpu()['ESP'];ret=num(self.read(sp),0);args=[num(self.read(sp+4+i),0) for i in range(0,a['pop'],4)]
  need((a['sp'],a['return_va'],a['args'])==(sp,ret,args),'full original platform stack ABI')
  if kind=='CRT':
   c=copy.deepcopy(a);c['va']=c['target'];c['void_return_normalized']=c.get('void_return_normalized',False)
   for o in c['memory_outputs']:
    if 'native_hex' in o:need(o['native_hex']==self.case['native_trace'][a['wire_end']-1]['reply']['result']['critical_hex'],'raw actual critical-section output');o.pop('native_hex')
   self.crt_api(self,c)
   if a['name']=='CreateFileA':need(a['native_handle']==self.native_file,'exact current file-token projection')
   return
  outputs=[]
  def out(p,b):outputs.append(dict(pointer=p,hex=b.hex()))
  if kind=='TASK':
   target=a['target'];name,slot,caller=e.TASK_APIS[target];need(ret==caller and a['name']==name and a['import_slot']==slot and num(self.read(slot),0)==target and a['actual_API_executed'] is True and a['value']==0 and a['memory_outputs']==[],'actual original empty/null task query')
   need(args==([0] if name=='ImmGetOpenStatus' else [e.INPUT+0x528]),'only declared null IME/empty input buffer');value=0
  else:
   need(kind=='GPU','no game function result substitutes');t=self.p['texture'];slot=a['slot'];bp=self.cpu()['EBP'];need(a['target']==(self.row['resource_loaded']['owner_device']['methods']['80'] if slot==80 else t['methods'][str(slot)]),'current actual COM identity')
   if slot==80:need(args==[self.row['resource_loaded']['owner_device']['pointer'],256,512,1,0,25,1,self.p['constructed']['record']+44] and ret==0x403C8A,'source portrait CreateTexture');self.identities(a['result']);out(args[-1],struct.pack('<I',t['pointer']))
   elif slot==56:need(args==[t['pointer'],0,bp-52] and ret==0x403CBE,'source portrait GetLevelDesc');need(struct.unpack('<8I',bytes.fromhex(a['result']['hex']))==(25,1,0,1,262144,0,256,512),'independent full portrait descriptor');out(args[2],bytes.fromhex(a['result']['hex']))
   elif slot==64:
    need(args==[t['pointer'],0,num(self.read(bp+8),0),0,2048] and ret==0x40395E,'source portrait LockRect');out(self.p['lock']['bits'],bytes.fromhex(self.p['lock']['hex']));out(args[2],struct.pack('<II',512,self.p['lock']['bits']))
   else:need(slot==68 and args==[t['pointer'],0] and ret==0x4039D3 and self.read(self.p['lock']['bits'],262144)==self.filebytes[24:],'all original memcpy pixels at UnlockRect')
   need(outputs==a['memory_outputs'] and a['value']==0,'all and only independent COM outputs');value=0
  for o in outputs:self.put(o['pointer'],bytes.fromhex(o['hex']))
  self.u.reg_write(x86.UC_X86_REG_EAX,value);self.u.reg_write(x86.UC_X86_REG_ESP,sp+4+a['pop']);self.u.reg_write(x86.UC_X86_REG_EIP,ret)
 def state(self):
  s=self.p['before']['state'];out=copy.deepcopy(s)
  for key,p,n in [('VM',e.VM,0x9400),('owner',e.MAIN,65536),('task',e.TASK,0x190),('work',e.overlay.WORK,0x24C0)]:out[key]=self.read(p,n).hex()
  out['SEH']=self.read(0,4).hex();out['VM_counter']=self.read(0x7A4E18,8).hex();out['task_input_flag']=self.read(e.TASK+0x117F20,1)[0]
  return out
 def queue(self):
  manager=self.read(e.MANAGER,0x38);heads=num(manager,16);arena=num(manager,20);used=num(manager,0x30)-arena;need(0<=used<=65536,'bounded independent queue')
  return dict(manager=manager.hex(),heads=self.read(heads,4096*8).hex(),arena_pointer=arena,used=used,arena=self.read(arena,used).hex(),unused_tail_sha256=e.sha(self.read(arena+used,65536-used)))
 def execute(self):
  p=self.p;self.index=0;self.count=self.writes=0;self.ih=hashlib.sha256();self.wh=hashlib.sha256()
  def mark():return dict(instructions=self.count,writes=self.writes,code_sha256=self.ih.hexdigest(),write_sha256=self.wh.hexdigest())
  def code(u,at,size,_):
   if at==self.stop:u.emu_stop();return
   if self.index<len(p['leaves']):
    item=p['leaves'][self.index]
    if at==item['call']['target']:self.leaf(item);self.index+=1;return
   need(0x400000<=at<0x592000 and self.read(at,size)==e.CODE[at-0x400000:at-0x400000+size] and e.CODE[at-0x400000]!=0xCC,'only original portrait/task instruction '+hex(at));self.count+=1;self.ih.update(struct.pack('<I',at))
  def write(u,access,at,size,value,_):need(not 0x400000<=at<0x593000,'no original code/IAT mutation');self.writes+=1;self.wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
  self.u.hook_add(UC_HOOK_CODE,code);self.u.hook_add(UC_HOOK_MEM_WRITE,write)
  frames={f['segments'][1]-1:f for f in p['frames']}
  for i,s in enumerate(p['segments']):
   need(self.cpu()==s['before_CPU'] and mark()==s['local_before'] and self.index==s['leaves'][0],'continuous complete original segment input')
   root=s['root']
   if root:
    va,recv=((0x40DB90,e.MANAGER),(0x40DC80,e.MANAGER),(0x425DE0,e.INPUT),(0x454CF0,e.TASK))[(i-3)%4];need(s['entry']==va and root==dict(receiver=recv,args=[]),'only explicit queue/input/full-task roots')
    self.put(e.STACK+0xF000,struct.pack('<I',e.RETURN));self.u.reg_write(x86.UC_X86_REG_ESP,e.STACK+0xF000);self.u.reg_write(x86.UC_X86_REG_ECX,recv)
   self.stop=s['stop'];self.u.emu_start(s['entry'],0,count=4000000,timeout=60_000_000);need(self.cpu()==s['CPU'] and mark()==s['local_after'] and self.index==s['leaves'][1],'all57 CPU and every local original PC/write after segment')
   boundary={0:'constructed',1:'image_return',2:'completion'}.get(i)
   if boundary:
    b=p[boundary];equal(self.snapshot(),b['memory'],'independent full '+boundary);need(self.state()==b['state'] and self.queue()==b['queue'],'entire independent task/VM/owner/queue '+boundary)
   if i==0:
    for q in p['constructed']['native_allocation_readbacks']:
     raw=self.sync(q['guest']);r=self.consume('readback',pointer=self.blocks[q['guest']]['native']);need(r==q['result'] and r['hex']==raw.hex() and self.wire==q['wire_index']+1,'independent complete native file/vector readback')
   if i in frames:need(self.state()==frames[i]['after'] and self.queue()==frames[i]['queue_after'],'full independent original frame state/queue')
  equal(self.snapshot(),p['final']['memory'],'all final original portrait/task memory');need(self.cpu()==p['final']['CPU'] and mark()==p['final']['local_trace'] and self.index==len(p['leaves']) and not self.files and self.depth==0,'complete final original CPU/digests/leaves/file/lock state')
  return dict(instructions=self.count,writes=self.writes)

def animation(row):
 p=row['terminal_portrait'];rules=animation_rules();need(len(p['frames'])==77,'original strict delay30/fade45 readiness sequence')
 states=[p['completion']['state']]+[f['after'] for f in p['frames']]
 for i,s in enumerate(states):
  v=bytes.fromhex(s['VM']);node=e.NODE-e.VM
  mode=6 if i<30 else 3 if i<76 else 2;bg=3 if i<61 else 2
  want={0:1,2:mode,4:mode,6:i-30 if 30<=i<76 else 0,8:5,16:45,18:i+1 if i<30 else 0,20:30,34:bg,36:i+1 if i<61 else 0,38:60}
  need(all(num(v,node+o,'H')==x for o,x in want.items()),'independent source role fade/background/delay '+str(i))
  need(num(v,28)==96 and num(v,0x20,'H')==int(i<77) and num(v,0x22,'H')==30,'only role30; readiness before following command')
  need(s['remaining']==p['before']['state']['remaining'] and s['elapsed']==p['before']['state']['elapsed'],'world remains paused')
 return rules

def resources(row):
 p=row['terminal_portrait'];c=p['constructed'];record=c['record'];base=bytearray(84);struct.pack_into('<I2H',base,0x34,25,256,512);base[0x46:0x48]=bytes([0xCD,0xCD]);bank=struct.pack('<2I',record,1)
 need(c['record_hex']==base.hex() and read(c['memory'],record,84)==bytes(base) and c['bank_hex']==bank.hex() and read(c['memory'],e.MAIN+0x844+32*8,8)==bank,'every original constructed IMAGE byte including two untouched CD bytes')
 need(c['CPU']['EIP']==0x403BD0 and c['CPU']['ECX']==record and read(c['memory'],c['file_pointer'],262168).hex()==c['file_hex'],'original source texture receiver and complete file buffer')
 b=bytearray(base);struct.pack_into('<2I',b,0x28,row['resource_loaded']['owner_device']['pointer'],p['texture']['pointer']);struct.pack_into('<2H',b,0x3C,256,512);struct.pack_into('<H',b,0x44,2)
 for label in ('image_return','completion','final'):
  need(read(p[label]['memory'],record,84)==bytes(b) and read(p[label]['memory'],e.MAIN+0x844+32*8,8)==bank and read(p[label]['memory'],e.VM+0x92A0+32,1)==b'\x01','all original loaded IMAGE/table/flag bytes '+label)
 need(read(c['memory'],e.VM+0x92A0+32,1)==b'\x00','loaded flag only after natural IMAGE completion')
 bp=c['CPU']['EBP'];returns=(0x41F3E0,0x41F25A,0x41F0C9,0x41684B,0x4167BF,0x4CDE8A,0x4CC0D2,0x4CC26D,0x4C62D4,0x4CEDA7,0x454D90,e.RETURN)
 for ret in returns:need(num(read(c['memory'],bp+4,4),0)==ret,'natural original constructor ancestor '+hex(ret));bp=num(read(c['memory'],bp,4),0)
 need(p['image_return']['CPU']['ESP']==p['before']['CPU']['ESP']+12 and p['image_return']['CPU']['EBP']==p['before']['CPU']['EBP'],'original IMAGE ret8 restores live resource frame')
 need(len(p['allocation_history'])==6 and p['allocation_history'][-2]['freed'] is True and p['allocation_history'][-1]['freed'] is False and len(p['live_allocations'])==4,'original file free; only current two vectors and queues remain')

def verify_case(row,replay=False,helpers=None):
 previous.verify_case(prefix_view(row));p=row['terminal_portrait'];pixels(row);native(row);resources(row);rules=animation(row);counts=Replay(row).execute()
 need(p['before']['CPU']==row['terminal_name']['CPU'] and p['before']['memory']==row['terminal_name']['memory'] and p['before']['trace']==row['terminal_name']['trace'],'same live original pending image source state')
 need(len(p['segments'])==3+4*77 and [s['entry'] for s in p['segments'][:3]]==[0x4CDE10,0x403BD0,0x4CC0D2] and all(s['root'] is None for s in p['segments'][:3]),'no new resource/VM/role handler forward root')
 f=p['final'];equal(row['final'],f['memory'],'entire actual final boundary');need(row['pending_CPU']==f['CPU'] and f['CPU']['EIP']==e.RETURN and f['CPU']['ESP']==e.STACK+0xF004 and f['state']['SEH']=='00000000','whole original task and SEH naturally returned')
 need(row['image_before']==row['image_after'],'original code and IAT unchanged');need((row['instructions'],row['writes'],row['code_trace_sha256'],row['write_trace_sha256'])==(f['trace']['instructions'],f['trace']['writes'],f['trace']['code_sha256'],f['trace']['write_sha256']),'all complete forward original trace digests')
 if replay:
  other=e.run_case(row['input'],helpers[0],helpers[1],[x['result'] for x in row['APIs'] if x['name']=='GetTickCount']);verify_case(other)
  for key in ('initial','final'):equal(row[key],other[key],'fresh resources whole '+key)
  for key in ('pending_CPU','after_fade','resource_initialization','cleanup_steps','cleanup_state','accounting_baseline','instructions','writes','code_trace_sha256','write_trace_sha256','world_frames','events','commands','task_calls','task_writes','admission'):
   need(row[key]==other[key],'fresh original full CPU/state/digest '+key)
  for key in p:
   if key in ('GPU_APIs','readback','GYBC_readback','name_readback','allocation_history','live_allocations'):continue
   if key=='prefix':
    for k in ('CRT_APIs','resource_steps','task_APIs','extra_counts','GPU_wire'):need(p[key][k]==other['terminal_portrait'][key][k],'fresh old prefix counter '+k)
   elif key=='constructed':
    for k in ('memory','CPU','state','queue','trace','local_trace','file_pointer','file_hex','record','record_hex','bank_hex'):need(p[key][k]==other['terminal_portrait'][key][k],'fresh full constructed '+k)
   elif key=='leaves':
    for a,b in zip(p[key],other['terminal_portrait'][key]):
     for k in ('kind',):need(a[k]==b[k],'same fresh API kind')
     for k in ('name','slot','target','sp','return_va','args','pop','value','memory_outputs','new_mappings'):
      if k in a['call'] and k!='memory_outputs':need(a['call'][k]==b['call'][k],'same fresh typed API '+k)
   else:need(p[key]==other['terminal_portrait'][key],'fresh complete portrait '+key)
 return dict(name=row['input']['name'],role=p['role'],VM_PC=96,VM_wait=0,complete_tasks=178,extra_complete_tasks=78,readiness_frames=77,portrait_file_bytes=262168,portrait_pixels=131072,portrait_rows=512,new_original_instructions=counts['instructions'],new_original_writes=counts['writes'],owned_regions=len(row['final']),CPU_registers=57,independent_original_full_memory_CPU_and_trace_replayed=True,current_native_resources_recreated_for_replay=replay,original_instructions=row['instructions'],original_writes=row['writes'])

def verify(path):
 d=json.loads(gzip.decompress(path.read_bytes()));need(d['source_contract']==e.source_contract() and [r['input'] for r in d['cases']]==e.overlay.parent.corpus(),'exact source and both terminal branches');h=e.helpers('terminal-portrait-proof');rows=[]
 for r in d['cases']:rows.append(verify_case(r,True,h));print('verified current terminal portrait',r['input']['name'],flush=True)
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(e.ROOT).as_posix()),cases=rows,implementation_sha256={p:e.sha((e.ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},all_source_portrait_pixels_and_native_buffers_verified=True,independent_original_full_memory_CPU_and_trace_replayed=True,current_native_resources_recreated=True,new_forward_VM_roots=0,next_instruction_executed=False,actual_draw_or_Present=False,terminal_presentation_complete=False,task_exit_complete=False,rewards_complete=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();need(not(e.ROOT/a.out).exists(),'fresh immutable proof');e.terminal.save(a.out,verify(e.ROOT/a.report))

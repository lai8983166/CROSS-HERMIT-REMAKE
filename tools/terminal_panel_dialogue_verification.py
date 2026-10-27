"""Independent layer7 text group, current native protocol and original task replay.

The accepted predecessor is immutable evidence, never a projected late cleanup.
Current native receipts are audited separately from its guest forward equality.
"""
import argparse,copy,gc,gzip,hashlib,json,struct,types
from functools import lru_cache
from types import SimpleNamespace
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
import unicorn.x86_const as x86
from tools import terminal_panel_dialogue_emulation as e
from tools import terminal_confirmation_verification as confirmation
from tools import terminal_dialogue_verification as dialogue
from tools.school_retained_name_verification import Replay as NameABI,NAMES
from tools.school_font_raster_catalog import geometry,convert_surface
from tools.school_second_live_text_catalog import bands
from tools.school_text_timing_catalog import expected_update
from tools.battle_hit_damage_verification import platform as tls_platform
from tools.battle_lethal_combat import validate_pages
from tools.battle_world_combat import expand

need=e.need;num=confirmation.num;read=confirmation.read
IMPLEMENTATIONS=('tools/terminal_panel_dialogue_emulation.py','tools/terminal_panel_dialogue_verification.py','tools/terminal_panel_dialogue_preservation.py','tools/tests/test_terminal_panel_dialogue.py')
PARENT_ACCEPTANCE='analysis/terminal-confirmation-acceptance-v1-20261026.json'
PARENT_ACCEPTANCE_SHA='3d2a114f3120d1eff89984dfa13cfd6a17ab7d8f513267026a9255f5f6754529'
PARENT_SOURCE='analysis/terminal-confirmation-source-v1-20261026.json.gz'
PARENT_SOURCE_SHA='b2a22addd13640b2a89f766b4703d2ede260d0279e7c4384124a36455e38a9c3'
PARENT_PROOF='analysis/terminal-confirmation-proof-v1-20261026.json'
PARENT_PROOF_SHA='559d652aa1131b39ee4d6d26a194c9cb52cd9f0c8e5f23e24840b30cc271e5ed'
OBJECT=e.VM+0x430+7*0xAB8;NODE=e.VM+0x6F60+7*0xE0

def equal(a,b,label):
 """Reject incomplete region bytes before the frozen first-difference helper."""
 for regions in (a,b):
  for r in regions:need(len(bytes.fromhex(r['hex']))==r['bytes'],label+' complete declared region bytes at '+hex(r['pointer']))
 confirmation.equal(a,b,label)

@lru_cache(maxsize=1)
def parent_report():
 for path,want in ((PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA),(PARENT_PROOF,PARENT_PROOF_SHA)):
  need(e.sha((e.ROOT/path).read_bytes())==want,'fixed predecessor '+path)
 raw=(e.ROOT/PARENT_SOURCE).read_bytes();need(e.sha(raw)==PARENT_SOURCE_SHA,'fixed predecessor source bytes')
 return json.loads(gzip.decompress(raw))

def parent_case(row):
 return next(x for x in parent_report()['cases'] if x['input']==row['input'])

def guest(value):
 """Compare guest semantics with explicit native-input provenance exceptions.

 Every captured boundary's mapped memory and CPU remains an exact comparison.
 """
 omitted={'native_result','native_args','native_handle','native_bits','native_hex','native','native_pointer','GDI_trace','GDI_handle_projection','native_allocation_readbacks'}
 if isinstance(value,dict):
  # A live run uses integer guest-pointer keys in CRT allocation dictionaries;
  # the immutable JSON report encodes those same object keys as strings.
  # Preserve every entry and reject collisions instead of losing one in JSON.
  keys={}
  for k in value:
   need(type(k) in (str,int),'only string/integer JSON guest object keys')
   encoded=str(k);need(encoded not in keys,'unambiguous JSON guest object key '+encoded);keys[encoded]=k
  out={encoded:guest(value[k]) for encoded,k in keys.items() if k not in omitted and not(value.get('name')=='GetTickCount' and k in ('actual_API_executed','captured_platform_input'))}
  if value.get('name')=='HeapAlloc' and 'memory_outputs' in value:
   # HeapAlloc(flags=0) supplies actual uninitialized bytes, not an identity
   # structure. Every byte is bound to this current native receipt in native(),
   # then consumed by independent original resource/portrait constructors.
   out['memory_outputs']=[dict(pointer=x['pointer'],current_uninitialized_native_input_bytes=len(bytes.fromhex(x['hex']))) for x in value['memory_outputs']]
  return out
 if isinstance(value,list):return [guest(x) for x in value]
 return value

def prefix(row,old=None,replay=True):
 old=parent_case(row) if old is None else old;d=row['terminal_panel_dialogue'];b=d['before'];p=d['prefix'];f=old['terminal_confirmation']['final']
 for k in ('memory','CPU','state','queue','trace'):need(b[k]==f[k]==row['terminal_confirmation']['final'][k],'same fixed entire predecessor boundary '+k)
 need(b['local_trace']==dict(instructions=0,writes=0,code_sha256=e.sha(b''),write_sha256=e.sha(b'')),'new trace starts at zero without inventing cumulative state')
 keys=('initial','input','APIs','world_frames','events','commands','task_calls','task_writes','admission','resource_loaded','overlay_continuation','after_fade','terminal_name','terminal_portrait','terminal_dialogue','terminal_confirmation','accounting_baseline','image_before','image_after')
 keys+=tuple(k for k in ('combat_input','initialization','target_bind','roots','bind_before','bind','bind_after','hit','hit_sides','contracts','both_hp_writes','calls','ownership','popped','entries','improved','reopened','original_coordinate_writes','action_events','resource_domain','IME_identity','game_function_results_stubbed','OS_input_submitted','host_unit_fields_changed_after_initialization') if k in old)
 for k in keys:need(guest(row[k])==guest(old[k]),'every fixed guest forward record '+k)
 def page_keys(x):
  if isinstance(x,dict):
   if set(x)=={'bytes','pages'}:return set(x['pages'])
   return set().union(*(page_keys(v) for v in x.values())) if x else set()
  if isinstance(x,list):return set().union(*(page_keys(v) for v in x)) if x else set()
  return set()
 retained=set().union(*(page_keys(old[k]) for k in keys));need(all(row['blobs'].get(k)==old['blobs'][k] for k in retained),'every fixed predecessor intermediate page retained byte for byte')
 need(all(e.sha(bytes.fromhex(v))==k for k,v in row['blobs'].items()),'every current blob independently rehashed');validate_pages(row,row['blobs'])
 for k,field in (('CRT_APIs','CRT_APIs'),('resource_initialization','resource_steps'),('task_APIs','task_APIs')):
  n=p[field];need(n==len(old[k]) if k!='CRT_APIs' else n==old['terminal_confirmation']['prefix']['CRT_APIs'],'fixed prefix length '+k)
  need(guest(row[k][:n])==guest(old[k][:n]),'all fixed guest forward '+k)
 allocations=[];allowed=set()
 for i,(a,b) in enumerate(zip(row['terminal_portrait']['leaves'],old['terminal_portrait']['leaves'])):
  if a['kind']=='CRT' and a['call']['name']=='HeapAlloc':
   c=a['call'];fixed=b['call'];allowed.add(c['wire_start']);allocations.append(dict(path='terminal_portrait/leaves/'+str(i)+'/call/memory_outputs/0/hex',wire_start=c['wire_start'],guest_pointer=c['memory_outputs'][0]['pointer'],bytes=len(bytes.fromhex(c['memory_outputs'][0]['hex'])),current_sha256=e.sha(bytes.fromhex(c['memory_outputs'][0]['hex'])),fixed_sha256=e.sha(bytes.fromhex(fixed['memory_outputs'][0]['hex']))))
 for i,(a,b) in enumerate(zip(row['CRT_APIs'][:p['CRT_APIs']],old['CRT_APIs'][:p['CRT_APIs']])):
  if a['name']=='HeapAlloc' and a['wire_start'] not in allowed:
   need(i<row['terminal_portrait']['prefix']['CRT_APIs'],'all other uninitialized inputs belong only to the independently replayed eight resource roots');allocations.append(dict(path='CRT_APIs/'+str(i)+'/memory_outputs/0/hex',wire_start=a['wire_start'],guest_pointer=a['memory_outputs'][0]['pointer'],bytes=len(bytes.fromhex(a['memory_outputs'][0]['hex'])),current_sha256=e.sha(bytes.fromhex(a['memory_outputs'][0]['hex'])),fixed_sha256=e.sha(bytes.fromhex(b['memory_outputs'][0]['hex']))))
 need(p['GPU_wire']==30 and p['extra_counts']==old['extra_original_instruction_counts'],'actual fixed predecessor wire and instruction accounting')
 ticks=[x['result'] for x in old['APIs'] if x['name']=='GetTickCount'];current_ticks=[x for x in row['APIs'] if x['name']=='GetTickCount'];need([x['result'] for x in current_ticks]==ticks and all(x['actual_API_executed'] is False and x['captured_platform_input'] is True for x in current_ticks),'fixed original captured clock sequence and honest replay provenance')
 tls_platform(row['platform'],SimpleNamespace(crt_draws=len(old['platform']['trace'])//3))
 def tls_guest(p):
  out=copy.deepcopy(p)
  for k in ('creation','cleanup'):
   for field in ('thread','native_index'):out[k].pop(field)
  for x in out['trace']:x.pop('actual_native_index')
  return out
 need(tls_guest(row['platform'])==tls_guest(old['platform']),'same original TLS token semantics with independently checked current owner')
 confirmation.source(row);confirmation.timing(row)
 initialization=ResourceInitializationReplay(row).execute() if replay else None
 if replay:
  fixed=ResourceInitializationReplay(old).execute();need(initialization['roots']==fixed['roots'],'every original resource-root PC/store local digest equals independently replayed fixed predecessor')
 portrait=dialogue.previous.Replay(row).execute() if replay else None
 added=confirmation.Replay(row).execute() if replay else None
 return dict(fixed_source_sha256=PARENT_SOURCE_SHA,fixed_acceptance_sha256=PARENT_ACCEPTANCE_SHA,fixed_proof_sha256=PARENT_PROOF_SHA,whole_forward_guest_equal_except_explicit_current_uninitialized_allocation_input=True,uninitialized_current_native_inputs=allocations,current_resource_initialization_fixture=initialization,portrait_constructor_replay=portrait,all_fixed_intermediate_pages_verified=True,new_terminal_state_pages_replaced=len(set(old['blobs'])-set(row['blobs'])),confirmation_original_replay=added,no_new_predecessor_cleanup_projection=True)

def source(row):
 d=row['terminal_panel_dialogue'];raw=(e.ROOT/e.terminal.SCRIPT_PATH).read_bytes();selector=num(bytes.fromhex(d['before']['state']['task']),0x174);seg=next(s for s in dialogue.script_commands(raw)['segments'] if s['index']=={1:2,4:11}[selector]);start=seg['code_start'];end=seg['code_end'];count=num(raw,end);n=1 if selector==1 else 3;pc=142;commands=[];texts=[];base=num(read(d['before']['memory'],e.VM+16,4),0)
 for i in range(1,n+1):
  op,size=struct.unpack_from('<HH',raw,start+pc);need((op,size)==(17,6) and num(raw,start+pc+4,'H')==i,'independent original next text table index')
  commands.append(dict(PC=pc,opcode=17,bytes=6,source_pointer=base+pc));packed=num(raw,end+4+i*4);span=packed>>20;at=end+(packed&0xFFFFF);text=raw[at:at+span]
  need(i<count and 2<=span<=512 and span%2==0 and at>=end+4+count*4 and at+span<=seg['end'] and text[-2:]==b'\0\0' and 0 not in text[:-2] and b'\\n' not in text,'bounded original single ANSI line')
  s=d['sentences'][i-1];b=s['font_boundary'];p=s['pending_font'];sp=b['CPU']['ESP'];args=[num(read(b['memory'],sp+4+j*4,4),0) for j in range(14)];obj=read(b['memory'],OBJECT,0x18);alternate=bool(obj[0x14]);width=num(obj,0xE if alternate else 0xC,'h')&0xFFFFFFFF;height=num(obj,0x12 if alternate else 0x10,'h')&0xFFFFFFFF
  need(s['text_index']==i and s['PC']==pc and p==dict(entry=num(read(b['memory'],0x5920A0,4),0),caller=0x4CAD09,args=args,CPU=b['CPU'],first_instruction_executed=False) and args==[height,width,0,0,400,0,0,0,1,5,0,0,0,0x5BF62C],'complete original line font ABI, not template font-size')
  need(b['CPU']['EIP']==p['entry'] and num(read(b['memory'],sp,4),0)==0x4CAD09 and num(obj,0x16,'H')==i-1 and s['record_index']==i-1 and s['record']==OBJECT+0x28+(i-1)*0x110 and s['raster_address']==e.RASTER+(i-1)*e.RASTER_STRIDE,'original count/stride-derived separate record and bounded distinct DIB')
  bp=b['CPU']['EBP']
  for caller in (0x4C4D04,0x4CEC2B,0x454D90,e.RETURN):need(num(read(b['memory'],bp+4,4),0)==caller,'original live font/text/VM/task ancestor '+hex(caller));bp=num(read(b['memory'],bp,4),0)
  need(read(b['memory'],base+pc,6)==raw[start+pc:start+pc+6],'unaltered current selected command bytes');texts.append(dict(index=i,PC=pc,source_offset=at,hex=text[:-2].hex()));pc+=6
 for op in (50,51):
  need(struct.unpack_from('<HH',raw,start+pc)==(op,4),'original readiness and new confirmation commands');commands.append(dict(PC=pc,opcode=op,bytes=4,source_pointer=base+pc));pc+=4
 # The first17 dispatch occurred before the predecessor stopped at CreateFontA.
 need(d['commands']==commands[1:],'only remaining original group command dispatches')
 need(len(d['sentences'])==n and num(read(d['before']['memory'],OBJECT+0x16,2),0,'H')==0,'original new layer7 group starts empty')
 rules={0x4CAD30:('xor','eax, eax'),0x4CAD32:('mov','ax, word ptr [edx + 0x16]'),0x4CAD36:('imul','eax, eax, 0x110'),0x4CAD3F:('lea','ecx, [ecx + eax + 0x28]'),0x4CAD97:('mov','cx, word ptr [eax + 0x16]'),0x4CAD9B:('add','cx, 1'),0x4CADA2:('mov','word ptr [edx + 0x16], cx')};md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
 for va,want in rules.items():
  ins=next(md.disasm(e.CODE[va-0x400000:va-0x400000+16],va,count=1));need((ins.mnemonic,ins.op_str)==want,'independent original record append instruction');proof.append(dict(va=va,hex=ins.bytes.hex(),mnemonic=ins.mnemonic,operands=ins.op_str))
 return dict(segment=seg['index'],script_sha256=e.sha(raw),texts=texts,commands=commands,final_PC=pc,record_append_rules=proof,draw_metadata_rules=dialogue.draw_rules())

def pixels(row):
 d=row['terminal_panel_dialogue'];provenance=source(row);refs=[]
 for s,t in zip(d['sentences'],provenance['texts']):
  args=s['pending_font']['args'];ref=dialogue.raster_dialogue(bytes.fromhex(t['hex']),args[:-1],dialogue.namecheck.original_text(args[-1]));r=s['raster'];cfg=geometry(ref['measured']);lock=s['lock'];w,h=[1<<(v-1).bit_length() for v in cfg['texture_size']]
  need(s['geometry']==cfg and (r['ACP'],r['measured'],r['selected_face'],r['raster_hex'])==(ref['ACP'],ref['measured'],ref['selected_face'],ref['raster_hex']),'independent current font/ACP/metrics and all DIB bytes')
  need([x['name'] for x in r['stages']]==['PatBlt','TextOutA','TextOutA'] and [x['hex'] for x in r['stages']]==[x['hex'] for x in ref['stages']],'three independent current clear/shadow/foreground stages')
  need([x['name'] for x in s['calls']]==NAMES+['SelectObject','DeleteObject','DeleteDC','DeleteObject'] and r['calls']==s['calls'][:23],'all original GDI raster and natural cleanup calls per line')
  need(lock['pitch']==w*2 and bytes.fromhex(lock['hex'])==bytes(w*h*2),'new current whole surface initially zero')
  conv=s.get('conversions',[x for x in d['conversions'] if x.get('sentence_index')==s['text_index']]);expected=bands(cfg);need([dict(rect=x['rect'],point=x['point']) for x in conv]==expected,'independent complete conversion band geometry')
  out=bytes.fromhex(lock['hex'])
  for b in expected:out=convert_surface(bytes.fromhex(ref['raster_hex']),cfg['raster_size'],b['rect'],out,lock['pitch'],b['point'])
  need(s['upload_hex']==s['readback']['hex']==out.hex() and s['readback']['sha256']==e.sha(out) and s['readback']['pitch']==lock['pitch'],'all independent converted texels equal actual GPU readback')
  need(num(read(s['completion']['memory'],OBJECT+0x16,2),0,'H')==s['text_index'],'original completed line appends exactly one record')
  refs.append((ref,cfg))
 return provenance,refs

def text_update(raw,origin):
 """Original timing plus the real draw metadata stores omitted by old fixtures."""
 result=expected_update(raw,origin,OBJECT);out=bytearray.fromhex(result['after_hex'])
 for draw in result['draws']:
  a=draw['args'];offset=a[0]-OBJECT;need(0<=offset and offset+0x78<=len(out),'bounded original appended draw record')
  struct.pack_into('<I',out,offset+0x4C,e.MAIN);struct.pack_into('<I',out,offset+0x5C,a[3]);out[offset+0x67]=a[4]&255;out[offset+0x66]=a[5]&255;out[offset+0x65]=a[6]&255;out[offset+0x64]=a[7]&255;struct.pack_into('<H',out,offset+0x76,a[8]&65535)
 result['after_hex']=out.hex();result['draws']=[{k:v for k,v in x.items() if k!='return_value'} for x in result['draws']];return result

def gpu_mapping(row):
 ledger=row['typed_GPU_projection'];m={x['native']:x['guest'] for x in ledger};need(len(m)==len(ledger) and len(set(m.values()))==len(m) and all(x['domain']=='overlay' for x in ledger),'unambiguous current typed GPU identity domain');return m

def gpu_value(v,m,key=None):
 if isinstance(v,dict):
  out={k:({s:m[p] for s,p in x.items()} if k=='methods' else gpu_value(x,m,k)) for k,x in v.items()}
  if 'locked_hex' in out:
   b=bytearray.fromhex(out['locked_hex']);struct.pack_into('<I',b,4,out['bits']);out['locked_hex']=b.hex()
  return out
 if isinstance(v,list):return [gpu_value(x,m,key) for x in v]
 return m[v] if type(v)is int and v and key in ('pointer','vtable','bits','method_pointer') else v

def crt_semantics(row):
 """Normalize owner tokens; byte payloads bind to API and original executors."""
 h=row['current_CRT_hello'];domains={};allocs={};files={};out=[];count=row.get('terminal_panel_dialogue',{}).get('prefix',row['terminal_confirmation']['prefix'])['CRT_APIs'];forward_end=row['CRT_APIs'][count-1]['wire_end']
 for name in ('heap','critical'):
  if h.get(name):domains[(name,h[name])]=name
 def token(name,p):need((name,p) in domains,'known current CRT '+name+' owner');return domains[(name,p)]
 for i,t in enumerate(row['CRT_trace']):
  need(t['request']['id']==t['reply']['id']==i+1 and t['reply']['ok'] is True,'unaltered actual current CRT order');q=copy.deepcopy(t['request']);r=copy.deepcopy(t['reply']['result']);op=q['op']
  if op=='heap_create':need(r['pointer']==h['heap'] and r['pointer']>0,'one actual current heap creator identity');domains[('heap',r['pointer'])]=domains[('pointer',r['pointer'])]='heap'
  if op=='initialize':
   p=r['pointer'];tag='critical'+hex(q['guest']);domains[('pointer',p)]=tag
   if q['guest']==0x80A4B0:need(p==h['critical'],'one actual current lock9 creator identity');domains[('critical',p)]=tag
  if op=='alloc':
   p=r['pointer'];need(p>0 and p not in allocs,'fresh current native allocation');allocs[p]='allocation'+str(sum(1 for x in out if x['request']['op']=='alloc'));domains[('pointer',p)]=allocs[p]
  if op=='open':
   p=r['handle'];need(p>0 and p not in files,'fresh current native file handle');files[p]='file'+str(sum(1 for x in out if x['request']['op']=='open'));domains[('handle',p)]=files[p]
  def norm(v):
   if isinstance(v,dict):
    z={}
    for k,x in v.items():
     if k in ('heap','critical','handle','pointer') and type(x)is int and x:z[k]=token(k,x)
     elif k=='critical_hex' or k=='hex' and op=='initialize':
      b=bytearray.fromhex(x);need(len(b)==24,'whole current critical structure')
      for off in (0,12,16):
       if num(b,off) not in (0,0xFFFFFFFF):struct.pack_into('<I',b,off,0x63000000+off)
      z[k]=b.hex()
     else:z[k]=norm(x)
    return z
   if isinstance(v,list):return [norm(x) for x in v]
   return v
  if op=='alloc':r['hex']=dict(current_uninitialized_native_input_bytes=len(bytes.fromhex(r['hex'])),verified_against_current_API_and_original_constructor=True)
  if i>=forward_end and op in ('sync','validate','free'):
   # The queue payload legitimately changes after the fixed predecessor.
   # The independent cleanup executor checks these complete current bytes.
   if op=='sync':need(q['hex']==r['hex'],'actual complete current cleanup sync result');q['hex']=dict(current_bytes=len(bytes.fromhex(q['hex'])),verified_against_independent_cleanup_memory=True);r['hex']=q['hex']
   else:r['before_hex']=dict(current_bytes=len(bytes.fromhex(r['before_hex'])),verified_against_independent_cleanup_memory=True)
  out.append(dict(request=norm(q),result=norm(r)))
  if op=='free':need(q['pointer'] in allocs,'free actual owned allocation');del allocs[q['pointer']]
  if op=='file_close':need(q['handle'] in files,'close actual owned file');del files[q['handle']]
 need(not allocs and not files,'all current native CRT blocks and files released')
 return out

def native(row,old=None):
 old=parent_case(row) if old is None else old;d=row['terminal_panel_dialogue'];gt=row['GPU_trace'];need(row['current_CRT_hello']['pointer_bytes']==row['current_GPU_hello']['pointer_bytes']==4 and row['current_GPU_hello']['window_visible'] is False and row['current_GPU_hello']['image_size']==[512,512] and row['current_CRT_hello']['GPU_created'] is False,'current bounded headless x86 owners');m=gpu_mapping(row);om=gpu_mapping(old);need(gpu_value(gt[:30],m)==gpu_value(old['GPU_trace'][:30],om),'complete current native GPU prefix semantics equal fixed parent')
 need(crt_semantics(row)==crt_semantics(old),'every current raw CRT control/forward byte matches fixed original semantics; cleanup buffer bytes checked by independent executor')
 need(guest(row['CRT_APIs'])==guest(old['CRT_APIs']),'all current original CRT ABI and complete logical outputs')
 covered=[]
 for a in row['CRT_APIs']:
  need(e.CODE[a['import_slot']-0x400000:a['import_slot']-0x400000+4]==struct.pack('<I',a['target']),'original unchanged current CRT IAT');covered.extend(range(a['wire_start'],a['wire_end']));r=row['CRT_trace'][a['wire_end']-1]['reply']['result'];nm=a['name'];outputs=[]
  if nm in ('InitializeCriticalSection','EnterCriticalSection','LeaveCriticalSection'):
   raw=r['hex'] if nm=='InitializeCriticalSection' else r['critical_hex'];b=bytearray.fromhex(raw)
   for off in (0,12,16):
    if num(b,off) not in (0,0xFFFFFFFF):struct.pack_into('<I',b,off,0x63000000+off+(a['args'][0]-0x80A480)*0x100)
   outputs=[dict(pointer=a['args'][0],hex=b.hex(),native_hex=raw)];value=0
  elif nm=='HeapAlloc':outputs=[dict(pointer=a['value'],hex=r['hex'])];value=a['value'];need(len(bytes.fromhex(r['hex']))==a['args'][2] and a['new_mappings']==[dict(pointer=value,bytes=(a['args'][2]+4095)&~4095)],'whole actual allocation output and guest mapping')
  elif nm=='ReadFile':outputs=[dict(pointer=a['memory_outputs'][0]['pointer'],hex=r['after_hex']),dict(pointer=a['args'][3],hex=struct.pack('<I',r['read']).hex())];value=r['value']
  elif nm in ('GetVersionExA','GetCurrentDirectoryA'):outputs=[dict(pointer=a['args'][0 if nm=='GetVersionExA' else 1],hex=r['hex'])];value=r['value']
  elif nm=='CreateFileA':value=0x62001000;need(a['native_handle']==r['handle'],'actual current read-only file token projection')
  elif nm=='HeapCreate':value=0x61001000
  elif nm=='DeleteCriticalSection':value=0
  else:value=r['value']
  need(a['memory_outputs']==outputs and a['value']==value,'every complete current CRT receipt output and result')
 for x in row['terminal_portrait']['constructed']['native_allocation_readbacks']:
  i=x['wire_index'];covered.extend((i-1,i));need(row['CRT_trace'][i]['reply']['result']==x['result'],'current complete native file/vector observation')
 need(sorted(covered)==list(range(len(row['CRT_trace'])-1)),'every current CRT wire operation classified once')
 # Audit all current GDI lifetimes, including both retained name/first-line calls.
 blocks=[row['terminal_name'],row['terminal_dialogue']]+d['sentences'];ledger=d['GDI_handle_projection'];gm={x['guest']:x['native'] for x in ledger};need(len(gm)==len(ledger) and len(set(gm.values()))==len(gm) and all(x['domain']=='GDI' for x in ledger),'all current GDI typed identities');need(d['prefix']['GDI_trace']==sum(len(x['GDI_trace']) for x in blocks[:2]),'exact retained current GDI trace prefix')
 for block in blocks:
  calls=block['calls'];trace=block['GDI_trace'];need(len(calls)==len(trace),'every current GDI call actual receipt')
  for c,t in zip(calls,trace):
   args=c['args'];nm=c['name'];na=list(args)
   if nm not in ('CreateFontA','lstrlenA','CreateCompatibleDC','GetStockObject'):na[0]=gm[args[0]]
   if nm=='SelectObject':na[1]=gm[args[1]]
   result=gm[c['result']] if nm in ('CreateFontA','CreateCompatibleDC','CreateDIBSection','GetStockObject','SelectObject') else c['result'];nr=t['native_result']
   need(t['name']==nm and t['args']==args and t['native_args']==nr['args']==na and t['logical_result']==c['result'] and nr['result']==result and c['actual_API_executed'] is True,'each current GDI complete native ABI/result')
   output=copy.deepcopy(nr);output.pop('dc_translated_args',None);output.pop('native_bits',None);output.update(args=args,result=c['result'],actual_API_executed=True);need(all(c[k]==v for k,v in output.items()),'all actual current GDI outputs and source raster bytes')
 # In raw GPU order, no observer may masquerade as a game COM call.
 calls=row['GPU_APIs'][:4]+row['terminal_name']['GPU_APIs']+row['terminal_portrait']['GPU_APIs']+row['terminal_dialogue']['GPU_APIs']
 calls+=sum((s['GPU_APIs'] for s in d['sentences']),[])
 need(d['GPU_APIs']==sum((s['GPU_APIs'] for s in d['sentences']),[]) and d['calls']==sum((s['calls'] for s in d['sentences']),[]) and d['GDI_trace']==sum((s['GDI_trace'] for s in d['sentences']),[]),'complete nonduplicated current sentence platform ledgers')
 cleanups=row.get('panel_dialogue_cleanup',d.get('cleanup',[]));cleanups=cleanups.get('records',[]) if isinstance(cleanups,dict) else cleanups
 calls+=sum((c['GPU_APIs'] for c in cleanups),[])+row['dialogue_cleanup']['GPU_APIs']+row['portrait_cleanup']['GPU_APIs']+row['name_cleanup']['GPU_APIs']+row['GPU_APIs'][4:]
 uploads={row['resource_loaded']['texture']['pointer']:row['resource_loaded']['upload_hex'],row['terminal_name']['texture']['pointer']:row['terminal_name']['upload_hex'],row['terminal_portrait']['texture']['pointer']:row['terminal_portrait']['upload_hex'],row['terminal_dialogue']['texture']['pointer']:row['terminal_dialogue']['upload_hex']};uploads.update({s['texture']['pointer']:s['upload_hex'] for s in d['sentences']})
 ci=0;live=set();readbacks=0
 for i,t in enumerate(gt):
  q=t['request'];r=t['reply'];need(q['id']==r['id']==i+1 and r['ok'] is True,'all unedited current native GPU order');op=q['op']
  if op=='readback':
   tex=m[q['pointer']];need(tex in live and r['result']['hex']==uploads[tex] and r['result']['sha256']==e.sha(bytes.fromhex(uploads[tex])),'whole current readback of an actually live owned texture');readbacks+=1;continue
  if op=='close':need(i==len(gt)-1 and not live and r['result']==row['GPU_cleanup'],'close only after all original current releases');continue
  need(ci<len(calls),'no unclassified native GPU operation');c=calls[ci];ci+=1;need(c.get('wire_index',i)==i and c['op']==op and c['native_result']==r['result'] and c['result']==gpu_value(r['result'],m) and c['actual_API_executed'] is True,'each original COM leaf exact actual current native receipt')
  qg=gpu_value(q,m);expected=dict(id=i+1,op=op)
  if op=='create':
   a=c['args'];expected.update(width=a[1],height=a[2],levels=a[3],usage=a[4],format=a[5],pool=a[6]);tex=c['result']['texture']['pointer'];need(tex not in live,'unique current simultaneous texture');live.add(tex)
  else:
   tex=c['args'][0];expected['pointer']=tex;need(tex in live,'every COM call uses a current live owned texture')
   if op=='lock':expected['flags']=c['args'][-1]
   elif op=='unlock':expected['hex']=uploads[tex]
   elif op=='release':need(c['value']==c['result']['count']==0,'actual last texture release');live.remove(tex)
  need(qg==expected,'complete independently translated current original COM request')
 need(ci==len(calls) and readbacks==18+6*len(d['sentences']),'all original COM leaves and only declared retained/sentence/final observers')
 observers=[i for i,x in enumerate(gt[:30]) if x['request']['op']=='readback'];oldkeys=('GYBC','name','portrait','dialogue');oldsurfaces=[row['resource_loaded'],row['terminal_name'],row['terminal_portrait'],row['terminal_dialogue']]
 for s in d['sentences']:
  observers.append(s['readback_wire_index']);need(gt[s['readback_wire_index']]['reply']['result']==s['readback'],'entire actual sentence observer receipt')
  need(len(s['observer_wire_indices'])==4,'four declared retained observers per append')
  for i,key,b in zip(s['observer_wire_indices'],oldkeys,oldsurfaces):observers.append(i);need(gt[i]['reply']['result']==s['readbacks_old4'][key]==b['readback'],'all original current surface fields retained per append')
 for i,key,b in zip(d['old_observer_wire_indices'],oldkeys,oldsurfaces):observers.append(i);need(gt[i]['reply']['result']==d['readbacks_old4'][key]==b['readback'],'four final whole retained observer receipts')
 for i,s,b in zip(d['new_observer_wire_indices'],d['sentences'],d['new_readbacks']):observers.append(i);need(gt[i]['reply']['result']==b==s['readback'],'all new lines simultaneously retained through new confirmation')
 need(sorted(observers)==[i for i,x in enumerate(gt) if x['request']['op']=='readback'],'each raw readback index explicitly classified once')
 need(len(uploads)==4+len(d['sentences']) and row['GPU_exit']==row['CRT_exit']==0 and not row['GPU_cleanup']['texture_releases'] and row['CRT_cleanup']['all_owned_resources_released'],'all current owners normally closed without fallback release')
 return dict(current_GPU_calls=ci,whole_readbacks=readbacks,current_GDI_calls=sum(len(x['calls']) for x in blocks),current_CRT_wire_operations=len(row['CRT_trace'])-1)

class Replay(dialogue.Replay):
 """Separate original x86 executor from the exact pending API and live stack."""
 def __init__(self,row,refs):
  self.row=row;self.d=row['terminal_panel_dialogue'];self.n=self.p=dict(before=self.d['before']);self.refs=refs;self.u=Uc(UC_ARCH_X86,UC_MODE_32);self.objects={};self.locks={};self.cleaning=False;self.current_sentence=None
  for r in self.d['before']['memory']:self.u.mem_map(r['pointer'],r['bytes']);self.u.mem_write(r['pointer'],bytes.fromhex(r['hex']))
  self.restore(self.d['before']['CPU']);need(self.cpu()==self.d['before']['CPU'] and len(self.cpu())==57,'all57 original pending architectural registers restored')
 def restore(self,cpu):
  first=['GDTR','IDTR','LDTR','TR','CR0','CR2','CR3','CR4']
  for k in first+[k for k in cpu if k not in first]:
   v=tuple(cpu[k]) if isinstance(cpu[k],list) else cpu[k];reg=getattr(x86,'UC_X86_REG_'+k)
   if self.u.reg_read(reg)!=v:self.u.reg_write(reg,v)
 def capture(self,b):
  full=all('hex' in x for x in b['memory']);mem=self.snapshot() if full else [dict(pointer=a,bytes=z-a+1,sha256=e.sha(self.read(a,z-a+1))) for a,z,_ in self.u.mem_regions()]
  if full:equal(mem,b['memory'],'independent every complete mapped region bytes')
  else:need(mem==b['memory'],'independent every complete mapped region reread SHA')
  need(self.cpu()==b['CPU'] and self.state()==b['state'] and self.queue()==b['queue'],'complete independent CPU/state/queue')
 def setup_raster(self,index):
  self.current_sentence=index;s=self.d['sentences'][index];self.cfg=self.refs[index][1];self.reference=self.refs[index][0];calls=s['calls'];self.raw=bytes.fromhex(self.reference['text_hex']);self.local_text=None;self.old_font=self.brush=0
  o=dict(logical_measurement_dc=num(self.read(e.MAIN+0xB208,4),0),font=calls[0]['result'],raster_dc=calls[6]['result'],bitmap=calls[7]['result'],ACP=self.reference['ACP'],measured=self.reference['measured'],selected_face=self.reference['selected_face']);o['fresh_owned_measurement_dc']=o['logical_measurement_dc'];self.case=dict(offscreen=o,parent_boundary=dict(pending_font=s['pending_font']))
  from tools import school_retained_name_raster as work
  dib=next(x for x in calls if x['name']=='CreateDIBSection');raster=e.RASTER+index*e.RASTER_STRIDE;need(dib['guest_bits']==s['raster_address']==raster,'source-contract derived distinct line DIB mapping');proxy=SimpleNamespace(**dict(vars(work),RASTER=raster,IMPORTS=dialogue.e.GDI))
  def constants(code):
   vals=[]
   for v in code.co_consts:
    if isinstance(v,types.CodeType):v=constants(v)
    elif v==0x4CA7CB:v=0x4CAD09
    vals.append(v)
   return code.replace(co_consts=tuple(vals))
  self.check_raster_API=types.FunctionType(constants(NameABI.api.__code__),dict(NameABI.api.__globals__,work=proxy))
 def leaf(self,item):
  c=item['call'];kind=item['kind'];sp=self.cpu()['ESP'];ret=num(self.read(sp,4),0);args=[num(self.read(sp+4+j,4),0) for j in range(0,c['pop'],4)];need((sp,ret,args)==(c['sp'],c['return_va'],c['args']),'complete original platform stack ABI')
  if kind=='GDI':
   si=next(i for i,s in enumerate(self.d['sentences']) if s['leaves'][0]<=self.leaf_cursor<s['leaves'][1]);s=self.d['sentences'][si];idx=s['calls'].index(c)
   if idx==0:self.setup_raster(si)
   need(self.current_sentence==si and num(self.read(c['import_slot'],4),0)==c['target'],'unchanged original per-line GDI IAT')
   if idx<23:
    if c['name']=='lstrlenA' and self.local_text is None:self.local_text=args[0]
    r=copy.deepcopy(c);r['dc_translated_args']=r['args']
    if c['name']=='CreateDIBSection':r['native_bits']=s['GDI_trace'][idx]['native_result']['native_bits']
    self.check_raster_API(self,dict(key='retained_name_GDI',va=c['target'],call=r));return
   o=self.case['offscreen'];want=[('SelectObject',0x4058D8,[o['raster_dc'],s['calls'][8]['result']]),('DeleteObject',0x405921,[o['bitmap']]),('DeleteDC',0x40596A,[o['raster_dc']]),('DeleteObject',0x4D1C1B,[o['font']])][idx-23];need((c['name'],ret,args)==want and c['memory_outputs']==[] and c['result']==(o['bitmap'] if idx==23 else 1),'all natural original per-line GDI cleanup');value=c['result']
  elif kind=='TASK':
   name,slot,caller=dialogue.e.parent.TASK_APIS[c['target']];need((c['name'],c['import_slot'],ret)==(name,slot,caller) and num(self.read(slot,4),0)==c['target'] and c['value']==c['result']==0 and c['actual_API_executed'] is True and c['memory_outputs']==[] and c['new_mappings']==[] and args==([0] if name=='ImmGetOpenStatus' else [e.INPUT+0x528]),'only actual null IME/empty task input leaves');value=0
  else:
   need(kind=='GPU','no game-function result substitution');si=next((i for i,s in enumerate(self.d['sentences']) if c in s['GPU_APIs'] or self.cleaning and s['texture']['pointer']==args[0]),None);need(si is not None,'known current sentence COM record');s=self.d['sentences'][si];t=s['texture'];slot=c['slot'];bp=self.cpu()['EBP'];out=[];w,h=[1<<(v-1).bit_length() for v in self.refs[si][1]['texture_size']]
   need(c['target']==(self.row['resource_loaded']['owner_device']['methods']['80'] if slot==80 else t['methods'][str(slot)]),'same current actual GPU identity')
   def output(p,b):out.append(dict(pointer=p,hex=b.hex()))
   if slot==80:need(args==[self.row['resource_loaded']['owner_device']['pointer'],w,h,1,0,25,1,s['record']+44] and ret==0x403C8A,'original count-derived current texture creation');self.identities(c['result']);output(args[-1],struct.pack('<I',t['pointer']))
   elif slot==56:
    need(args==[t['pointer'],0,bp-(36 if self.cleaning else 52)] and ret==(0x403A44 if self.cleaning else 0x403CBE) and struct.unpack('<8I',bytes.fromhex(c['result']['hex']))==(25,1,0,1,w*h*2,0,w,h),'complete independent original texture descriptor');output(args[-1],bytes.fromhex(c['result']['hex']))
   elif slot==64:need(args==[t['pointer'],0,num(self.read(bp+8,4),0),0,2048] and ret==0x40395E,'original current sentence LockRect');output(s['lock']['bits'],bytes.fromhex(s['lock']['hex']));output(args[2],struct.pack('<II',s['lock']['pitch'],s['lock']['bits']))
   elif slot==68:need(not self.cleaning and args==[t['pointer'],0] and ret==0x4039D3 and self.read(s['lock']['bits'],len(bytes.fromhex(s['upload_hex']))).hex()==s['upload_hex'],'every original converted texel at current UnlockRect')
   else:need(slot==8 and self.cleaning and args==[t['pointer']] and ret==0x40378D,'original supplemental current texture Release')
   need(out==c['memory_outputs'] and c['value']==0,'all and only independent current COM outputs')
   for x in out:self.put(x['pointer'],bytes.fromhex(x['hex']))
   value=0
  self.u.reg_write(x86.UC_X86_REG_EAX,value);self.u.reg_write(x86.UC_X86_REG_ESP,sp+4+c['pop']);self.u.reg_write(x86.UC_X86_REG_EIP,ret)
 def execute(self):
  d=self.d;index=count=writes=root=0;ih=hashlib.sha256();wh=hashlib.sha256();observed=[];commands=[];conversions=[];queries=[];updates=[];last=d['before']['trace'];current=None
  def mark():return dict(instructions=count,writes=writes,code_sha256=ih.hexdigest(),write_sha256=wh.hexdigest())
  def code(u,at,size,_):
   nonlocal index,count
   if at==self.stop:u.emu_stop();return
   if index<len(d['leaves']) and at==d['leaves'][index]['call']['target']:self.leaf_cursor=index;self.leaf(d['leaves'][index]);index+=1;return
   if at==0x4CE9C5:
    p=num(self.read(e.VM+16,4),0)+num(self.read(e.VM+28,4),0);op,n=struct.unpack('<HH',self.read(p,4));commands.append(dict(PC=num(self.read(e.VM+28,4),0),opcode=op,bytes=n,source_pointer=p))
   if at==0x405869:
    sp=self.cpu()['ESP'];a=[num(self.read(sp+j,4),0) for j in range(0,24,4)];conversions.append(dict(entry=at,args=a,rect=list(struct.unpack('<4I',self.read(a[4],16))),point=list(struct.unpack('<2I',self.read(a[5],8)))))
   if at==0x4CB220 and self.cpu()['ECX']==OBJECT:
    origin=[num(self.read(NODE+30,2),0,'H'),num(self.read(NODE+32,2),0,'H')];updates.append(dict(before=self.read(OBJECT,0xAB8),expected=text_update(self.read(OBJECT,0xAB8),origin),draw_returns=0))
   if at==0x4CD541 and updates and not updates[-1].get('complete'):
    need(self.read(OBJECT,0xAB8).hex()==updates[-1]['expected']['after_hex'],'independent original full AB8 timing update');updates[-1]['complete']=True
   if at==0x4CBF00 and updates and not updates[-1].get('complete'):
    sp=self.cpu()['ESP'];args=[num(self.read(sp+4+j*4,4),0) for j in range(9)];want=updates[-1].setdefault('draws',[]);want.append(dict(va='0x4cbf00',receiver=self.cpu()['ECX'],args=args,return_va=hex(num(self.read(sp,4),0))))
   if at==0x4CB4B2 and updates and not updates[-1].get('complete'):
    need(self.cpu()['EAX']&255==1,'original real draw metadata body naturally returns AL1');updates[-1]['draw_returns']+=1
   query_entries=getattr(e,'QUERIES',(0x4CB5F0,0x4CD3B7,0x4D5EC0,0x4CD402,0x4128F0,0x4CD432,0x4CCFF7,0x4CCB30,0x4CD02D))
   if at in query_entries:
    cpu=self.cpu();queries.append(dict(entry=at,CPU=cpu,receiver=cpu['ECX'],stack_hex=self.read(cpu['ESP'],68).hex(),object_hex=self.read(OBJECT,0xAB8).hex(),node_hex=self.read(NODE,0xE0).hex()))
   need(0x400000<=at<0x592000 and self.read(at,size)==e.CODE[at-0x400000:at-0x400000+size] and e.CODE[at-0x400000]!=0xCC,'only unchanged original group instruction '+hex(at));count+=1;ih.update(struct.pack('<I',at))
  def write(u,access,at,size,value,_):
   nonlocal writes
   need(not 0x400000<=at<0x593000,'no original code or IAT mutation');writes+=1;wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if e.VM<=at<e.VM+0x9400 or e.parent.KEYBOARD<=at<e.parent.KEYBOARD+0xA00 or e.TASK<=at<e.TASK+0x190 or at==0:observed.append(dict(pc=self.cpu()['EIP'],address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
  hs=[self.u.hook_add(UC_HOOK_CODE,code),self.u.hook_add(UC_HOOK_MEM_WRITE,write)];frames={x['segments'][1]-1:x for x in d['frames']};boundaries=[(k,d[k]) for k in ('ready','confirmation','final')]
  for j,s in enumerate(d['sentences']):boundaries.extend((str(j)+k,s[k]) for k in ('font_boundary','raster','completion'))
  seen=set()
  for key,b in boundaries:
   if b['local_trace']==mark():self.capture(b);need(b['trace']==last,'initial unexecuted font boundary exact original trace');seen.add(key)
  shapes={}
  for fi,f in enumerate(d['frames']):
   start,end=f['segments'];n=end-start
   if fi==0:want=[(False,d['before']['CPU']['EIP'],0x403BD0),(False,0x403BD0,e.RETURN)];need(f['kind']=='resume','initial original pending task continuation')
   else:
    want=[(True,0x40DB90,e.RETURN),(True,0x40DC80,e.RETURN),(True,0x425DE0,e.RETURN),(True,0x454CF0,e.RETURN)]
    if fi<len(d['sentences']):want[-1]=(True,0x454CF0,d['sentences'][fi]['pending_font']['entry']);want.extend([(False,d['sentences'][fi]['pending_font']['entry'],0x403BD0),(False,0x403BD0,e.RETURN)])
    need(f['kind']=='root','subsequent task uses explicit existing roots')
   need(n==len(want),'exact complete frame segment count and split points');shapes.update({start+j:v for j,v in enumerate(want)})
   if fi<len(d['sentences']):need(d['sentences'][fi]['leaves']==[d['segments'][end-2]['leaves'][0],d['segments'][end-1]['leaves'][1]],'per-line platform interval derived from natural pending-font/raster/completion segments')
  need(sorted(shapes)==list(range(len(d['segments']))),'all segments belong to exactly one declared complete frame')
  for i,s in enumerate(d['segments']):
   current=s;need(self.cpu()==s['before_CPU'] and mark()==s['local_before'] and index==s['leaves'][0] and last==s['trace_before'],'continuous original full group segment input')
   rooted,entry,stop=shapes[i];need(bool(s['root'])==rooted and s['entry']==entry and s['stop']==stop and s['kind']==('root' if rooted else 'continuation'),'only exact original roots and natural continuation stop boundaries')
   if s['root']:
    va,recv=((0x40DB90,e.MANAGER),(0x40DC80,e.MANAGER),(0x425DE0,e.INPUT),(0x454CF0,e.TASK))[root%4];root+=1;need(s['entry']==va and s['root']==dict(receiver=recv,args=[]),'only four existing complete forward roots');self.put(e.STACK+0xF000,struct.pack('<I',e.RETURN));self.u.reg_write(x86.UC_X86_REG_ESP,e.STACK+0xF000);self.u.reg_write(x86.UC_X86_REG_ECX,recv)
   else:need(s['entry']==self.cpu()['EIP'],'continuation uses exact pending original CPU and stack')
   self.stop=s['stop'];self.u.emu_start(s['entry'],0,count=4_000_000,timeout=60_000_000);need(self.cpu()==s['CPU'] and mark()==s['local_after'] and index==s['leaves'][1],'all57 CPU and every independent original PC/store per interval')
   if s['stop']==e.RETURN:need(self.cpu()['ESP']==e.STACK+0xF004,'every complete original root/task naturally restores full stack')
   for k in ('instructions','writes'):need(s['trace_after'][k]-last[k]==s['local_after'][k]-s['local_before'][k],'actual cumulative count extends fixed prefix')
   last=s['trace_after']
   for key,b in boundaries:
    if mark()==b['local_trace']:self.capture(b);need(b['trace']==last,'key whole boundary actual original trace');seen.add(key)
   if i in frames:
    f=frames[i];self.capture(f['capture']);need(f['after']==self.state() and f['queue_after']==self.queue() and f['capture']['local_trace']==mark() and f['capture']['trace']==last,'complete every frame memory/57CPU/queue/counts')
  for h in hs:self.u.hook_del(h)
  need(index==len(d['leaves']) and observed==d['writes'] and commands==d['commands'] and seen=={x[0] for x in boundaries},'all original leaves/stores/dispatches/full boundaries consumed')
  need(root==4*(len(d['frames'])-1),'first frame finishes pending task; all subsequent tasks use exactly four roots')
  need(conversions==[{k:v for k,v in x.items() if k not in ('sentence_index','record')} for x in d['conversions']],'all observed original conversion arguments')
  need(queries==d['queries'],'all original readiness/query ABI and full object observations')
  for x in updates:need(x.get('complete') and x.get('draws',[])==x['expected']['draws'] and x['draw_returns']==len(x['expected']['draws']),'independent original full timing/draw metadata and all natural original returns')
  return dict(instructions=count,writes=writes,CPU_registers=57,whole_regions=len(self.snapshot()),completed_pending_task=True,new_complete_task_roots=root//4)
 def cleanup(self):
  """Execute the actual new-boundary original teardown, with no old-CPU view."""
  d=self.d;new=self.row['panel_dialogue_cleanup'];steps=self.row['cleanup_steps'];need(len(new)==len(d['sentences']) and len(steps)==len(new)+8,'all line records and original predecessor teardown roots')
  rootkeys=('label','entry','args','receiver','cdecl');roots=[dict(label='supplemental_original_panel_dialogue_line_'+str(s['text_index'])+'_destructor',entry=0x403730,args=[],receiver=s['record'],cdecl=False) for s in reversed(d['sentences'])]+[{k:s[k] for k in rootkeys} for s in parent_case(self.row)['cleanup_steps']]
  need([{k:s[k] for k in rootkeys} for s in steps]==roots,'only authorized original new-record and predecessor cleanup roots')
  gpu=sum((x['GPU_APIs'] for x in new),[])+self.row['dialogue_cleanup']['GPU_APIs']+self.row['portrait_cleanup']['GPU_APIs']+self.row['name_cleanup']['GPU_APIs']+self.row['GPU_APIs'][4:];crt=self.row['CRT_APIs'][d['prefix']['CRT_APIs']:];gi=ci=0;self.cleaning=True
  resources=[(self.row['resource_loaded']['record'],self.row['resource_loaded'],[512,512]),(dialogue.e.name.TEXTURE,self.row['terminal_name'],None),(self.row['terminal_portrait']['constructed']['record'],self.row['terminal_portrait'],[256,512]),(dialogue.e.TEXTURE,self.row['terminal_dialogue'],None)]+[(s['record'],s,None) for s in d['sentences']]
  by_texture={b['texture']['pointer']:(record,b,size) for record,b,size in resources}
  allocations={x['native']:x for x in self.row['terminal_portrait']['allocation_history'] if not x['freed']};total_i=total_w=0;last=d['final']['trace'];seen_new=0
  for step in steps:
   need(self.cpu()==step['before_cpu'] and step['trace_before']==last,'actual continuous cleanup begins at current full57 CPU');before_count=total_i;before_writes=total_w
   c=next((x for x in new if x['record']==step['receiver'] and step['entry']==0x403730),None)
   if c is not None:self.capture(c['before']);need(c['before']['trace']==last and c['text_index']==len(new)-seen_new and c['before']['local_trace']==d['final']['local_trace'],'reverse original appended record cleanup order and frozen forward hash');seen_new+=1
   sp=e.STACK+0xF000;self.put(sp,struct.pack('<I',e.RETURN))
   for j,a in enumerate(step['args']):self.put(sp+4+j*4,struct.pack('<I',a))
   self.u.reg_write(x86.UC_X86_REG_ESP,sp);self.u.reg_write(x86.UC_X86_REG_ECX,step['receiver'])
   def platform_leaf(a,kind):
    here=self.cpu()['ESP'];ret=num(self.read(here,4),0);args=[num(self.read(here+4+j,4),0) for j in range(0,a['pop'],4)];need((here,ret,args)==(a['sp'],a['return_va'],a['args']),'full actual cleanup platform stack ABI');outputs=[]
    if kind=='GPU':
     need(args[0] in by_texture,'current known cleanup texture receiver');record,b,size=by_texture[args[0]];t=b['texture'];need(a['target']==t['methods'][str(a['slot'])],'same current typed original cleanup method')
     if a['slot']==56:
      if size is None:
       cfg=b.get('geometry',geometry(b['raster']['measured']));size=[1<<(v-1).bit_length() for v in cfg['texture_size']]
      w,h=size;desc=struct.pack('<8I',25,1,0,1,w*h*2,0,w,h);need(args==[t['pointer'],0,self.cpu()['EBP']-36] and ret==0x403A44 and a['result']['hex']==desc.hex(),'entire independent original cleanup descriptor');outputs=[dict(pointer=args[-1],hex=desc.hex())]
     else:need(a['slot']==8 and args==[t['pointer']] and ret==0x40378D,'only actual original cleanup Release')
     need(a['memory_outputs']==outputs and a['value']==0,'all and only current GPU cleanup outputs');value=0
    else:
     need(num(self.read(a['import_slot'],4),0)==a['target'] and not a['new_mappings'],'unchanged actual cleanup CRT IAT and no allocation')
     for wire in self.row['CRT_trace'][a['wire_start']:a['wire_end']]:
      q=wire['request'];r=wire['reply']['result'];op=q['op']
      if op in ('sync','validate','free','badread','badwrite'):
       need(q['pointer'] in allocations,'current original cleanup uses only owned live CRT allocation');block=allocations[q['pointer']];raw=self.read(block['guest'],block['bytes'])
       if op=='sync':need(q['hex']==r['hex']==raw.hex(),'all actual current native cleanup mirror bytes independently reread')
       elif op in ('validate','free'):need(r['before_hex']==raw.hex() and r['pointer']==q['pointer'] and r['value']==1,'all actual current native validation/free bytes independently reread')
       else:need(q['offset']==a['args'][0]-block['guest'] and q['bytes']==a['args'][1] and r==dict(value=0,pointer=q['pointer'],offset=q['offset'],bytes=q['bytes']),'actual original cleanup readable/writeable block subrange')
       if op=='free':del allocations[q['pointer']]
     outputs=[{k:v for k,v in x.items() if k!='native_hex'} for x in a['memory_outputs']];value=a['value']
    for out in outputs:self.put(out['pointer'],bytes.fromhex(out['hex']))
    self.u.reg_write(x86.UC_X86_REG_EAX,value);self.u.reg_write(x86.UC_X86_REG_ESP,here+4+a['pop']);self.u.reg_write(x86.UC_X86_REG_EIP,ret)
   def code(u,at,size,_):
    nonlocal gi,ci,total_i
    if at==e.RETURN:u.emu_stop();return
    if gi<len(gpu) and at==gpu[gi]['target']:platform_leaf(gpu[gi],'GPU');gi+=1;return
    if ci<len(crt) and at==crt[ci]['target']:platform_leaf(crt[ci],'CRT');ci+=1;return
    need(0x400000<=at<0x592000 and self.read(at,size)==e.CODE[at-0x400000:at-0x400000+size] and e.CODE[at-0x400000]!=0xCC,'only original actual cleanup instruction');total_i+=1
   def write(u,access,at,size,value,_):
    nonlocal total_w
    need(not 0x400000<=at<0x593000,'no original code or IAT cleanup mutation');total_w+=1
   hs=[self.u.hook_add(UC_HOOK_CODE,code),self.u.hook_add(UC_HOOK_MEM_WRITE,write)];self.u.emu_start(step['entry'],0,count=4_000_000,timeout=60_000_000)
   for h in hs:self.u.hook_del(h)
   need(self.cpu()==step['cpu_after'] and self.cpu()['EIP']==e.RETURN and self.cpu()['ESP']==sp+4+(0 if step['cdecl'] else 4*len(step['args'])),'all actual cleanup57 CPU and natural root return')
   need(total_i-before_count==step['trace_after']['instructions']-last['instructions'] and total_w-before_writes==step['trace_after']['writes']-last['writes'],'every actual original cleanup instruction/write count');last=step['trace_after']
   if c is not None:
    self.capture(c['after']);need(c['after']['trace']==last and c['after']['local_trace']==d['final']['local_trace'] and self.read(c['record'],0x68).hex()==c['record_hex'] and num(self.read(c['record']+44,4),0)==0 and num(self.read(0x765720,4),0)==c['accounting'],'all current cleanup mapped bytes,57CPU,record and accounting')
   if step['label']=='supplemental_original_dialogue_texture_destructor':
    old=self.row['dialogue_cleanup'];need(old['before_CPU']==step['before_cpu'] and old['CPU']==step['cpu_after'] and self.read(dialogue.e.TEXTURE,0x68).hex()==old['record_hex'] and num(self.read(0x765720,4),0)==old['texture_bytes'],'complete actual old dialogue cleanup57CPU/record/accounting without projection')
   elif step['label']=='supplemental_original_portrait_container_destructor':
    old=self.row['portrait_cleanup'];need(self.read(e.MAIN+0x844+32*8,8).hex()==old['bank_hex']==bytes(8).hex() and num(self.read(0x765720,4),0)==old['texture_bytes'] and num(self.read(0x79FC74,4),0)==old['game_bytes'],'actual original portrait container and heap accounting')
   elif step['label']=='supplemental_original_name_texture_destructor':need(num(self.read(0x765720,4),0)==self.row['name_cleanup']['texture_bytes'],'actual original name texture cleanup accounting')
  need(gi==len(gpu) and ci==len(crt) and seen_new==len(new) and not allocations,'all actual original cleanup leaves exactly once and owned native allocations freed')
  state=self.row['cleanup_state'];need(num(self.read(0x765720,4),0)==state['texture_bytes']==self.row['accounting_baseline']['texture_bytes'] and num(self.read(0x79FC74,4),0)==state['game_bytes']==self.row['accounting_baseline']['game_bytes'] and self.read(e.MAIN+0x844+20*8,8).hex()==state['bank'],'actual original complete resource/accounting restoration')
  for record,b,_ in resources:
   if e.VM<=record<e.VM+0x9400:need(num(self.read(record+44,4),0)==0,'every live VM texture record naturally released')
  return dict(instructions=total_i,writes=total_w,CPU_registers=57,new_line_full_memory_boundaries=seen_new,all_current_original_teardown_roots=len(steps),predecessor_cleanup_projection=False)

class ResourceInitializationReplay(Replay):
 """Explicit resource fixture from initial method inputs and recorded root CPU.

Battle-only memory and untouched old stack bytes are not reconstructed. Every
original/API write, involved resource domain and new mapping is checked at the
actual loaded-resource boundary, and all57 CPU/counts at each of eight roots.
"""
 def __init__(self,row):
  self.row=row;self.n=self.p=dict(before=dict(CPU=row['resource_initialization'][0]['before_cpu']));self.u=Uc(UC_ARCH_X86,UC_MODE_32);self.objects={};self.locks={};self.image=e.CODE;self.touched=set();self.record_host_writes=False
  for x in row['initial']:self.u.mem_map(x['pointer'],x['bytes']);self.u.mem_write(x['pointer'],bytes.fromhex(x['hex']))
  self.initial_regions={(a,b) for a,b,_ in self.u.mem_regions()};self.restore(row['resource_initialization'][0]['before_cpu']);self.record_host_writes=True
 def put(self,p,b):
  super().put(p,b)
  if self.record_host_writes:self.touched.update(range(p,p+len(b)))
 def execute(self):
  from tools.school_crt_init_fixture import IMPORTS
  row=self.row;steps=row['resource_initialization'][:8];expected_labels=['original_heap_initialization','original_lock_initialization','original_queue_owner_binding','original_queue_4096_heads','original_bounded_64KiB_arena','original_complete_GYBC_file','original_GYBC_register_and_upload','original_file_buffer_free'];need([s['label'] for s in steps]==expected_labels,'exact eight declared resource construction roots')
  file_pointer=steps[5]['cpu_after']['EAX'];roots_expected=[(0x57B9D0,[1],0,True),(0x576F60,[],0,False),(0x40D970,[e.MAIN],e.MANAGER,False),(0x40DB10,[4096],e.MANAGER,False),(0x40DBF0,[65536],e.MANAGER,False),(0x42AE20,[dialogue.previous.e.overlay.PATH],0,True),(0x416790,[file_pointer,20],e.MAIN,False),(0x428AD0,[file_pointer],0,True)]
  need([(s['entry'],s['args'],s['receiver'],s['cdecl']) for s in steps]==roots_expected,'only original declared resource initialization roots/receivers/arguments')
  ci=gi=0;count=writes=0;ih=hashlib.sha256();wh=hashlib.sha256();roots=[];apis=row['CRT_APIs'];gpu=row['GPU_APIs'][:4];loaded=row['resource_loaded'];texture=loaded['texture'];lock=loaded['lock']
  def mark():return dict(instructions=count,writes=writes,code_sha256=ih.hexdigest(),write_sha256=wh.hexdigest())
  def leaf(c,kind):
   sp=self.cpu()['ESP'];ret=num(self.read(sp,4),0);args=[num(self.read(sp+4+i,4),0) for i in range(0,c['pop'],4)];need((sp,ret,args)==(c['sp'],c['return_va'],c['args']),'independent resource construction full original API ABI');outputs=[]
   if kind=='CRT':
    nm,pop=IMPORTS[c['import_slot']];need((nm,pop)==(c['name'],c['pop']) and num(self.read(c['import_slot'],4),0)==c['target'],'unchanged construction CRT IAT and declared Windows leaf');r=row['CRT_trace'][c['wire_end']-1]['reply']['result']
    if nm in ('InitializeCriticalSection','EnterCriticalSection','LeaveCriticalSection'):
     raw=r['hex'] if nm=='InitializeCriticalSection' else r['critical_hex'];b=bytearray.fromhex(raw)
     for off in (0,12,16):
      if num(b,off) not in (0,0xFFFFFFFF):struct.pack_into('<I',b,off,0x63000000+off+(args[0]-0x80A480)*0x100)
     outputs=[dict(pointer=args[0],hex=b.hex(),native_hex=raw)];value=0
    elif nm=='HeapAlloc':
     need(len(bytes.fromhex(r['hex']))==args[2] and args[:2]==[0x61001000,0] and c['new_mappings']==[dict(pointer=c['value'],bytes=(args[2]+4095)&~4095)],'entire actual uninitialized HeapAlloc platform input and exact guest allocation');outputs=[dict(pointer=c['value'],hex=r['hex'])];value=c['value']
    elif nm=='ReadFile':outputs=[dict(pointer=c['memory_outputs'][0]['pointer'],hex=r['after_hex']),dict(pointer=args[3],hex=struct.pack('<I',r['read']).hex())];value=r['value']
    elif nm in ('GetVersionExA','GetCurrentDirectoryA'):outputs=[dict(pointer=args[0 if nm=='GetVersionExA' else 1],hex=r['hex'])];value=r['value']
    elif nm=='CreateFileA':need(c['native_handle']==r['handle'],'current native file projection');value=0x62001000
    elif nm=='HeapCreate':value=0x61001000
    else:value=r['value']
    need(outputs==c['memory_outputs'] and value==c['value'],'all construction CRT output bytes equal current raw native receipt')
   else:
    slot=c['slot'];bp=self.cpu()['EBP'];need(c['target']==(loaded['owner_device']['methods']['80'] if slot==80 else texture['methods'][str(slot)]),'same current source GYBC COM identity')
    if slot==80:need(args==[loaded['owner_device']['pointer'],512,512,1,0,25,1,loaded['record']+44] and ret==0x403C8A,'original current GYBC CreateTexture');self.identities(c['result']);outputs=[dict(pointer=args[-1],hex=struct.pack('<I',texture['pointer']).hex())]
    elif slot==56:
     desc=struct.pack('<8I',25,1,0,1,524288,0,512,512);need(args==[texture['pointer'],0,bp-52] and ret==0x403CBE and c['result']['hex']==desc.hex(),'entire independently derived original GYBC descriptor');outputs=[dict(pointer=args[-1],hex=desc.hex())]
    elif slot==64:need(args==[texture['pointer'],0,num(self.read(bp+8,4),0),0,2048] and ret==0x40395E and lock['pitch']==1024 and bytes.fromhex(lock['hex'])==bytes(524288),'entire actual source GYBC initial LockRect');outputs=[dict(pointer=lock['bits'],hex=lock['hex']),dict(pointer=args[2],hex=struct.pack('<II',1024,lock['bits']).hex())]
    else:need(slot==68 and args==[texture['pointer'],0] and ret==0x4039D3 and self.read(lock['bits'],524288)==dialogue.previous.e.overlay.RESOURCE[24:],'every independently executed original GYBC uploaded texel')
    need(outputs==c['memory_outputs'] and c['value']==0,'all predicted original GYBC COM outputs');value=0
   for out in outputs:self.put(out['pointer'],bytes.fromhex(out['hex']))
   self.u.reg_write(x86.UC_X86_REG_EAX,value);self.u.reg_write(x86.UC_X86_REG_ESP,sp+4+c['pop']);self.u.reg_write(x86.UC_X86_REG_EIP,ret)
  def code(u,at,size,_):
   nonlocal ci,gi,count
   if at==e.RETURN:u.emu_stop();return
   if ci<len(apis) and at==apis[ci]['target']:leaf(apis[ci],'CRT');ci+=1;return
   if gi<len(gpu) and at==gpu[gi]['target']:leaf(gpu[gi],'GPU');gi+=1;return
   need(at in e.ALLOWED and self.read(at,size)==e.CODE[at-0x400000:at-0x400000+size] and e.CODE[at-0x400000]!=0xCC,'only unchanged finite original resource construction instruction');count+=1;ih.update(struct.pack('<I',at))
  def write(u,access,at,size,value,_):
   nonlocal writes
   need(not 0x400000<=at<0x593000,'construction cannot change original code/IAT');writes+=1;wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF));self.touched.update(range(at,at+size))
  hooks=[self.u.hook_add(UC_HOOK_CODE,code),self.u.hook_add(UC_HOOK_MEM_WRITE,write)]
  for s in steps:
   need(self.cpu()==s['before_cpu'],'all57 recorded actual resource root input registers');before=mark();sp=e.STACK+0xF000;self.put(sp,struct.pack('<I',e.RETURN))
   for i,a in enumerate(s['args']):self.put(sp+4+i*4,struct.pack('<I',a))
   self.u.reg_write(x86.UC_X86_REG_ESP,sp);self.u.reg_write(x86.UC_X86_REG_ECX,s['receiver']);self.u.emu_start(s['entry'],0,count=4_000_000,timeout=60_000_000)
   need(self.cpu()==s['cpu_after'] and self.cpu()['EIP']==e.RETURN and self.cpu()['ESP']==sp+4+(0 if s['cdecl'] else len(s['args'])*4),'all57 exact original resource root registers and natural stack return');after=mark()
   need(after['instructions']-before['instructions']==s['trace_after']['instructions']-s['trace_before']['instructions'] and after['writes']-before['writes']==s['trace_after']['writes']-s['trace_before']['writes'],'all original construction instruction/write counts');roots.append(dict(label=s['label'],before=before,after=after))
  for h in hooks:self.u.hook_del(h)
  need(ci==row['terminal_portrait']['prefix']['CRT_APIs'] and gi==4 and self.cpu()==loaded['CPU'],'all current construction native leaves and final57 CPU')
  expected=[(x['pointer'],bytes.fromhex(x['hex'])) for x in loaded['memory']]
  def bytes_at(p,n):
   chunks=[];cursor=p;end=p+n
   for a,b in expected:
    if a<=cursor<a+len(b):
     stop=min(end,a+len(b));chunks.append(b[cursor-a:stop-a]);cursor=stop
     if cursor==end:return b''.join(chunks)
   raise ValueError('complete resource construction expected memory '+hex(p))
  ordered=sorted(self.touched);ranges=[]
  for at in ordered:
   if ranges and at==ranges[-1][1]:ranges[-1][1]+=1
   else:ranges.append([at,at+1])
  for a,b in ranges:need(self.read(a,b-a)==bytes_at(a,b-a),'every independently reconstructed original/API resource-write byte at '+hex(a))
  for x in row['resource_domain']:need(self.read(x['pointer'],x['bytes'])==bytes_at(x['pointer'],x['bytes']),'whole involved CRT domain')
  need(self.read(e.MAIN,65536)==bytes_at(e.MAIN,65536),'whole involved current renderer owner')
  for a,b,_ in self.u.mem_regions():
   if (a,b) not in self.initial_regions:need(self.read(a,b-a+1)==bytes_at(a,b-a+1),'entire newly mapped owned resource region')
  return dict(kind='explicit initial resource method-input fixture with recorded actual root CPU; untouched battle and old stack bytes not reconstructed',roots=roots,CPU_registers=57,actual_CRT_leaves=ci,current_original_COM_leaves=gi,all_original_and_API_write_bytes_verified=len(self.touched),new_resource_domains_and_maps_verified=True,uninitialized_native_inputs_consumed_by_original_constructors=True)

def timing(row):
 d=row['terminal_panel_dialogue'];n=len(d['sentences']);pc=156 if n==1 else 168
 def vw(b):v=bytes.fromhex(b['state']['VM']);return num(v,28),num(v,32,'H')
 need(vw(d['before'])==(142,0) and vw(d['ready'])==(pc-4,0) and vw(d['confirmation'])==(pc,1) and vw(d['final'])==(pc,1),'original group readiness then new confirmation wait')
 for i,s in enumerate(d['sentences']):need(vw(s['completion'])==(148+i*6,0),'each original17 complete task advances exactly six bytes')
 frames=d['frames'];need(len(frames)>=n+4 and frames[0]['kind']=='resume' and all(f['kind']=='root' for f in frames[1:]),'pending continuation then complete task frames')
 need(frames[0]['before']==d['before']['state'] and frames[0]['queue_before']==d['before']['queue'],'first frame starts at complete original pending state and queue')
 need([f['phase'] for f in frames[:n]]==['resume_first_sentence']+['append_sentence']*(n-1) and all(f['phase']=='text_readiness' for f in frames[n:-3]) and [f['phase'] for f in frames[-3:]]==['enter_confirmation','held_confirmation','held_confirmation'],'only original group append/readiness/confirmation/hold phases')
 for b,f in ((d['ready'],frames[-4]),(d['confirmation'],frames[-3]),(d['final'],frames[-1])):need(b['local_trace']==f['capture']['local_trace'] and b['CPU']==f['capture']['CPU'] and b['state']==f['after'] and b['queue']==f['queue_after'],'key boundary exactly matches its complete original frame')
 for i,f in enumerate(frames):
  need(f['index']==i and f['capture']['state']==f['after'] and f['capture']['queue']==f['queue_after'],'complete frame index/state/queue')
  if i:need(f['before']==frames[i-1]['after'] and f['queue_before']==frames[i-1]['queue_after'],'continuous frames and queues')
  need(f['after']['remaining']==d['before']['state']['remaining'] and f['after']['elapsed']==d['before']['state']['elapsed'],'world stays paused during terminal text')
 for f in frames[-2:]:need(vw(dict(state=f['before']))==vw(dict(state=f['after']))==(pc,1),'two no-input complete tasks hold new confirmation')
 need(num(read(d['final']['memory'],OBJECT+0x16,2),0,'H')==n,'all group records simultaneously retained')
 for i in range(n):need(not 2<=num(read(d['ready']['memory'],OBJECT+i*0x110+24,2),0,'H')<=4,'all original lines actually ready before50 returns')
 previous_account=num(read(d['before']['memory'],0x765720,4),0)
 for s in d['sentences']:
  w,h=[1<<(v-1).bit_length() for v in s['geometry']['texture_size']];previous_account+=w*h*2;need(num(read(s['completion']['memory'],0x765720,4),0)==previous_account,'original append texture accounting retains all prior resources')
  record=read(d['final']['memory'],s['record'],0x68);need(num(record,0x28)==row['resource_loaded']['owner_device']['pointer'] and num(record,0x2C)==s['texture']['pointer'] and num(record,0x4C)==e.MAIN and s['alive'] is True,'each appended original record retains current device,texture and owner')
 need(d['accounting']==previous_account==num(read(d['final']['memory'],0x765720,4),0),'all new and four predecessor textures simultaneously accounted')
 return dict(VM_PC=pc,VM_wait=1,lines=n,additional_complete_tasks=len(frames),new_confirmation_released=False,no_input_hold_tasks=2)

def final_summary(row):
 """Bind the replacement terminal page references to the verified final bytes."""
 d=row['terminal_panel_dialogue'];memory=d['final']['memory'];t=e.terminal;s=expand(row['final_state']['terminal_state'],row['blobs']);want=dict(task=read(memory,e.TASK,0x190).hex(),records=[read(memory,t.RECORD+i*256,256).hex() for i in (0,1)],counters=read(memory,t.CTRL+0x2EF14,0x31).hex(),remaining=num(read(memory,t.CTRL+0x2E6F4,4),0,'i'),elapsed=num(read(memory,t.CTRL+0x2E6F8,4),0,'i'),result=read(memory,0x7F4000,0x2000).hex(),work=read(memory,t.WORK,3).hex(),VM=read(memory,e.VM,0x9400).hex(),units=[read(memory,p,0x520).hex() for p in (t.UNIT,t.TARGET)])
 need(s==want,'every current final-state page and selected field equals independently replayed whole final memory');return True

def verify_case(row,old=None):
 d=row['terminal_panel_dialogue'];p=prefix(row,old);provenance,refs=pixels(row);platform=native(row,old);timed=timing(row);r=Replay(row,refs);counts=r.execute();equal(row['final'],d['final']['memory'],'all actual final mapped bytes');need(row['pending_CPU']==d['final']['CPU'] and row['image_before']==row['image_after'],'all actual final CPU and unchanged original image')
 need((row['instructions'],row['writes'],row['code_trace_sha256'],row['write_trace_sha256'])==tuple(d['final']['trace'][k] for k in ('instructions','writes','code_sha256','write_sha256')),'actual complete cumulative source digest retained without reconstruction')
 summary=final_summary(row);cleanup=r.cleanup();return dict(name=row['input']['name'],prefix=p,source=provenance,native=platform,timing=timed,added=counts,cleanup=cleanup,current_terminal_summary_pages_equal_verified_final_memory=summary,independent_whole_memory_CPU_and_new_original_trace=True,no_new_predecessor_cleanup_projection=True)

def verify(path):
 e.fixed_parent_times()
 data=json.loads(gzip.decompress(path.read_bytes()));need(data['source_contract']==e.source_contract(),'exact source contract');h=e.helpers('terminal-panel-dialogue-proof');rows=[]
 for row in data['cases']:
  old=parent_case(row);proof=verify_case(row,old);ticks=[x['result'] for x in old['APIs'] if x['name']=='GetTickCount'];other=e.run_case(row['input'],h[0],h[1],ticks);verify_case(other,old)
  for k in ('initial','final'):equal(row[k],other[k],'fresh current owners complete '+k)
  for k in ('pending_CPU','instructions','writes','code_trace_sha256','write_trace_sha256','cleanup_steps','cleanup_state','resource_initialization','world_frames','events','commands','task_calls','task_writes','admission'):need(row[k]==other[k],'fresh full original run '+k)
  need(guest(row['terminal_panel_dialogue'])==guest(other['terminal_panel_dialogue']),'fresh current resources all logical group boundaries,57CPU,bytes,frames and digests');proof['current_native_resources_recreated']=True;rows.append(proof);print('independent current panel dialogue',row['input']['name'],flush=True)
  need(guest(row['panel_dialogue_cleanup'])==guest(other['panel_dialogue_cleanup']),'fresh current full-memory/57CPU new-record teardown boundaries')
  del other;gc.collect()
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(e.ROOT).as_posix()),implementation_sha256={p:e.sha((e.ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},cases=rows,whole_current_native_protocol_independently_verified=True,current_native_resources_recreated=True,new_predecessor_cleanup_projection=False,cumulative_digest_reconstructed=False,next_confirmation_released=False,new_OS_input=False,draw_or_Present=False,terminal_presentation_complete=False,task_exit_complete=False,rewards_complete=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();need(not(e.ROOT/a.out).exists(),'fresh immutable independent proof');e.terminal.save(a.out,verify(e.ROOT/a.report))

"""Independent name GDI/geometry/pixels, original-code replay and fresh resources."""
import argparse,copy,gzip,hashlib,json,struct,types
from types import SimpleNamespace
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
import unicorn.x86_const as x86
from tools import terminal_name_emulation as e
from tools import terminal_after_fade_verification as old
from tools import terminal_after_fade_model as fade
from tools import terminal_overlay_verification as overlay
from tools.school_retained_name_verification import Replay as NameABI,NAMES
from tools.school_retained_name_corpus import raster_name,source_names
from tools.school_font_raster_catalog import geometry,convert_surface,source_catalog
from tools.school_second_live_text_catalog import bands
from tools.school_retained_render_pipeline_verification import Replay as MemoryReplay
need=e.need;read=fade.read;num=fade.num
IMPLEMENTATIONS=('tools/terminal_name_emulation.py','tools/terminal_name_verification.py','tools/terminal_name_preservation.py')

def prefix_view(row):
 r={k:copy.deepcopy(v) for k,v in row.items() if k not in ('terminal_name','name_cleanup')};f=r['after_fade']
 r.update(final=f['memory'],pending_CPU=f['CPU'],instructions=f['trace']['instructions'],writes=f['trace']['writes'],code_trace_sha256=f['trace']['code_sha256'],write_trace_sha256=f['trace']['write_sha256'])
 # The additive name operations are omitted only in this old-contract view.
 # Raw real sequence IDs and every new operation are verified separately.
 trace=r['GPU_trace'];r['GPU_trace']=trace[:5]+trace[-3:]
 for i,x in enumerate(r['GPU_trace']):x['request']['id']=x['reply']['id']=i+1
 r['cleanup_steps']=[x for x in r['cleanup_steps'] if x['label']!='supplemental_original_name_texture_destructor']
 return r

def original_text(pointer):
 raw=e.CODE[pointer-0x400000:];return raw[:raw.index(0)]

def independent_pixels(row):
 n=row['terminal_name'];role={1:2,4:1}[num(bytes.fromhex(n['state']['task']),0x174)];catalog,provenance=source_names();source=catalog['roles'][str(role)];raw=original_text(source['name_pointer']);need(raw.hex()==source['name_hex'],'pinned source role name bytes')
 args=row['after_fade']['pending']['args'];reference=raster_name(raw,args[:-1],original_text(args[-1]));r=n['raster']
 need((r['ACP'],r['measured'],r['selected_face'],r['raster_hex'])==(reference['ACP'],reference['measured'],reference['selected_face'],reference['raster_hex']),'separate actual GDI metrics/face/complete bitmap')
 need([s['hex'] for s in r['stages']]==[s['hex'] for s in reference['stages']] and [s['name'] for s in r['stages']]==['PatBlt','TextOutA','TextOutA'],'all three independently rendered source GDI stages')
 cfg=geometry(r['measured']);need([s['name'] for s in n['calls']]==NAMES+['SelectObject','DeleteObject','DeleteDC','DeleteObject'],'exact original23 GDI raster calls and4 natural cleanup leaves')
 need(r['calls']==n['calls'][:23],'frozen pending upload GDI prefix');need(n['path']=='data\\adv\\bin\\'+source['filename'],'original selected portrait relative path')
 w,h=[1<<(v-1).bit_length() for v in cfg['texture_size']];lock=n['lock'];pixels=bytes.fromhex(lock['hex'])
 need(lock['pitch']==w*2 and len(pixels)==w*h*2 and pixels==bytes(len(pixels)),'actual new bounded texture initially zero')
 expected=[]
 for b in bands(cfg):pixels=convert_surface(bytes.fromhex(r['raster_hex']),cfg['raster_size'],b['rect'],pixels,lock['pitch'],b['point']);expected.append(b)
 need([dict(rect=x['rect'],point=x['point']) for x in n['conversions']]==expected,'all original conversion rectangles and destinations')
 need(n['upload_hex']==n['readback']['hex']==pixels.hex() and n['readback']['sha256']==e.sha(pixels) and n['readback']['pitch']==lock['pitch'],'every independent A1R5G5B5 texel equals actual entire GPU readback')
 need(n['GYBC_readback']['hex']==row['resource_loaded']['upload_hex'],'original current GYBC resource survives name upload')
 return role,source,reference,cfg

def native(row):
 n=row['terminal_name'];gt=row['GPU_trace'];ct=row['CRT_trace']
 for label,trace in [('GPU',gt),('CRT',ct)]:
  for i,x in enumerate(trace):need(x['request']['id']==x['reply']['id']==i+1 and x['reply']['ok'] is True,'raw actual ordered '+label+' native protocol')
 ops=['create','describe','lock','unlock','readback']*2+['readback','describe','release','describe','release','close']
 need([x['request']['op'] for x in gt]==ops,'two current textures / independent GYBC readback / original separate destructors / close')
 need(n['before']['GPU_wire']==5 and n['GPU_wire_end']==11,'source resource lifetime intervals')
 calls=row['GPU_APIs'][:4]+n['GPU_APIs']+row['name_cleanup']['GPU_APIs']+row['GPU_APIs'][4:]
 for a,i in zip(calls,(0,1,2,3,5,6,7,8,11,12,13,14)):
  need(a['native_result']==gt[i]['reply']['result'] and a['op']==gt[i]['request']['op'] and a['actual_API_executed'] is True,'each original COM leaf exact current native receipt')
 need(gt[9]['reply']['result']==n['readback'] and gt[10]['reply']['result']==n['GYBC_readback'] and gt[8]['request']['hex']==n['upload_hex'],'whole actual readback and upload wire evidence')
 need(gt[-1]['reply']['result']==row['GPU_cleanup'] and not row['GPU_cleanup']['texture_releases'],'all actual textures originally released before helper close')
 need(row['name_cleanup']['GDI']==dict(fonts=0,bitmaps=0,dcs=1,all_resources_released=True),'natural name font/bitmap/rasterDC cleanup; supplemental measurementDC only')
 need(row['name_cleanup']['texture_bytes']==row['accounting_baseline']['texture_bytes']+524288,'supplemental original name destructor preserves current GYBC accounting')
 ledger=n['GDI_handle_projection'];mapping={x['guest']:x['native'] for x in ledger};need(len(mapping)==len(ledger) and all(x['domain']=='GDI' for x in ledger),'single current typed GDI owner')
 def nat(p):need(p in mapping,'known current native GDI handle');return mapping[p]
 need(read(n['before']['memory'],e.MAIN+0xB208,4)==struct.pack('<I',ledger[0]['guest']),'measurementDC declared before first original task')
 need(len(n['GDI_trace'])==len(n['calls']),'every original GDI leaf actual receipt')
 for c,t in zip(n['calls'],n['GDI_trace']):
  name=c['name'];args=c['args'];expected=list(args)
  if name not in ('CreateFontA','lstrlenA','CreateCompatibleDC','GetStockObject'):expected[0]=nat(args[0])
  if name=='SelectObject':expected[1]=nat(args[1])
  result=nat(c['result']) if name in ('CreateFontA','CreateCompatibleDC','CreateDIBSection','GetStockObject','SelectObject') else c['result']
  need(t['name']==name and t['args']==args and t['native_args']==expected and t['logical_result']==c['result'] and t['native_result']['args']==expected and t['native_result']['result']==result and c['actual_API_executed'] is True,'exact current GDI typed arguments/result')
  outputs=copy.deepcopy(t['native_result']);outputs.pop('dc_translated_args',None);outputs.pop('native_bits',None);outputs.update(args=args,result=c['result'],actual_API_executed=True)
  need(all(c[k]==v for k,v in outputs.items()),'every actual GDI output retained')

class Replay(MemoryReplay):
 """Separate executor: original bytes + independently checked platform outputs."""
 def put(self,p,b):
  for page in range(p&~4095,(p+len(b)+4095)&~4095,4096):
   if not any(lo<=page<=hi for lo,hi,_ in self.u.mem_regions()):self.u.mem_map(page,4096)
  self.u.mem_write(p,b)
 def __init__(self,row,reference,cfg):
  self.row=row;self.n=row['terminal_name'];self.u=Uc(UC_ARCH_X86,UC_MODE_32);self.image=e.CODE;self.objects={};self.locks={};self.cfg=cfg;self.reference=reference
  for r in self.n['before']['memory']:self.u.mem_map(r['pointer'],r['bytes']);self.u.mem_write(r['pointer'],bytes.fromhex(r['hex']))
  # Descriptor/control state precedes segment and ordinary register restoration.
  cpu=self.n['before']['CPU'];first=['GDTR','IDTR','LDTR','TR','CR0','CR2','CR3','CR4'];names=first+[k for k in cpu if k not in first]
  for k in names:
   reg=getattr(x86,'UC_X86_REG_'+k);value=tuple(cpu[k]) if isinstance(cpu[k],list) else cpu[k]
   if self.u.reg_read(reg)!=value:self.u.reg_write(reg,value)
  need(self.cpu()==cpu,'all57 source architectural registers restored')
  calls=self.n['calls'];o=dict(logical_measurement_dc=num(read(self.n['before']['memory'],e.MAIN+0xB208,4),0),font=calls[0]['result'],raster_dc=calls[6]['result'],bitmap=calls[7]['result'],ACP=self.n['raster']['ACP'],measured=self.n['raster']['measured'],selected_face=self.n['raster']['selected_face'])
  o['fresh_owned_measurement_dc']=o['logical_measurement_dc'];self.case=dict(offscreen=o,parent_boundary=dict(pending_font=row['after_fade']['pending']))
  self.local_text=cpu['EBP']-0x108;self.raw=bytes.fromhex(reference['text_hex']);self.old_font=self.brush=0
  from tools import school_retained_name_raster as work
  proxy=SimpleNamespace(**dict(vars(work),RASTER=e.RASTER,IMPORTS=e.GDI))
  self.check_raster_API=types.FunctionType(NameABI.api.__code__,dict(NameABI.api.__globals__,work=proxy))
 def cpu(self):
  out={}
  for k in self.n['before']['CPU']:
   v=self.u.reg_read(getattr(x86,'UC_X86_REG_'+k));out[k]=list(v) if isinstance(v,tuple) else v
  return out
 def identities(self,r):
  if not isinstance(r,dict):return
  if {'pointer','vtable','methods'}<=r.keys():
   self.put(r['pointer'],struct.pack('<I',r['vtable']))
   for off,target in r['methods'].items():
    self.put(r['vtable']+int(off),struct.pack('<I',target))
    if not any(a<=target<=b for a,b,_ in self.u.mem_regions()):self.u.mem_map(target&~4095,4096)
  for v in r.values():
   if isinstance(v,dict):self.identities(v)
 def leaf(self,kind,c):
  sp=self.cpu()['ESP'];args=[num(self.read(sp+4+i,4),0) for i in range(0,c['pop'],4)];ret=num(self.read(sp),0)
  need((sp,args,ret)==(c['sp'],c['args'],c['return_va']),'every original platform stack argument and return')
  if kind=='GDI':
   slot=c['import_slot'];need(num(self.read(slot),0)==c['target'] and e.GDI[slot][0]==c['name'],'unmodified source GDI IAT')
   idx=self.n['calls'].index(c)
   if idx<23:
    r=copy.deepcopy(c);r['dc_translated_args']=r['args']
    if c['name']=='CreateDIBSection':r['native_bits']=self.n['GDI_trace'][idx]['native_result']['native_bits']
    self.check_raster_API(self,dict(key='retained_name_GDI',va=c['target'],call=r));return
   o=self.case['offscreen'];expect=[('SelectObject',0x4058D8,[o['raster_dc'],self.n['calls'][8]['result']]),('DeleteObject',0x405921,[o['bitmap']]),('DeleteDC',0x40596A,[o['raster_dc']]),('DeleteObject',0x4D1C1B,[o['font']])][idx-23]
   need((c['name'],ret,args)==expect and c['memory_outputs']==[] and (c['result']==o['bitmap'] if idx==23 else c['result']==1),'exact original GDI restoration/deletion contract');value=c['result']
  else:
   t=self.n['texture'];slot=c['slot'];need(c['target']==(self.row['resource_loaded']['owner_device']['methods']['80'] if slot==80 else t['methods'][str(slot)]),'current original COM identity')
   w,h=[1<<(v-1).bit_length() for v in self.cfg['texture_size']];bp=self.cpu()['EBP'];expected=[]
   def out(p,b):expected.append(dict(pointer=p,hex=b.hex()))
   if slot==80:
    need(args==[self.row['resource_loaded']['owner_device']['pointer'],w,h,1,0,25,1,e.TEXTURE+44] and ret==0x403C8A,'source name CreateTexture request');self.identities(c['result']);out(args[-1],struct.pack('<I',t['pointer']))
   elif slot==56:
    need(args==[t['pointer'],0,bp-52] and ret==0x403CBE,'source initial texture descriptor');out(args[-1],bytes.fromhex(c['result']['hex']))
   elif slot==64:
    need(args==[t['pointer'],0,num(self.read(bp+8),0),0,2048] and ret==0x40395E,'source name texture lock');b=bytes.fromhex(self.n['lock']['hex']);out(self.n['lock']['bits'],b);out(args[2],struct.pack('<II',self.n['lock']['pitch'],self.n['lock']['bits']))
   else:need(slot==68 and args==[t['pointer'],0] and ret==0x4039D3 and self.read(self.n['lock']['bits'],len(bytes.fromhex(self.n['upload_hex']))).hex()==self.n['upload_hex'],'source entire original converted upload')
   need(expected==c['memory_outputs'] and c['value']==0,'all independently predicted COM memory outputs/result')
   for r in expected:self.put(r['pointer'],bytes.fromhex(r['hex']))
   value=c['value']
  self.u.reg_write(x86.UC_X86_REG_EAX,value);self.u.reg_write(x86.UC_X86_REG_ESP,sp+4+c['pop']);self.u.reg_write(x86.UC_X86_REG_EIP,ret)
 def execute(self):
  n=self.n;index=0;count=writes=0;ih=hashlib.sha256();wh=hashlib.sha256()
  def check_boundary(b):
   overlay.memory_equal(self.snapshot(),b['memory'],'independent original source whole boundary');need(self.cpu()==b['CPU'],'all57 independent original source registers');need(dict(instructions=count,writes=writes,code_sha256=ih.hexdigest(),write_sha256=wh.hexdigest())==b['local_trace'],'independent all original local PCs and writes')
  def code(u,at,size,_):
   nonlocal index,count
   if at==0x4CDE10:check_boundary(n);u.emu_stop();return
   if at==0x403BD0:check_boundary(n['raster'])
   if index<len(n['leaves']):
    item=n['leaves'][index];c=n['calls' if item['kind']=='GDI' else 'GPU_APIs'][item['index']]
    if at==c['target']:self.leaf(item['kind'],c);index+=1;return
   need(0x400000<=at<0x592000 and self.read(at,size)==e.CODE[at-0x400000:at-0x400000+size] and e.CODE[at-0x400000]!=0xCC,'only unchanged original name machine code '+hex(at));count+=1;ih.update(struct.pack('<I',at))
  def write(u,access,at,size,value,_):
   nonlocal writes
   need(not 0x400000<=at<0x592000 and not 0x592000<=at<0x593000,'no original code/IAT writes');writes+=1;wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
  self.u.hook_add(UC_HOOK_CODE,code);self.u.hook_add(UC_HOOK_MEM_WRITE,write);self.u.emu_start(self.cpu()['EIP'],0,count=2000000,timeout=60_000_000)
  need(self.cpu()['EIP']==0x4CDE10 and index==len(n['leaves']),'all exact original source leaves consumed without new root')
  return count,writes
 def snapshot(self):return [dict(pointer=a,bytes=b-a+1,hex=self.read(a,b-a+1).hex()) for a,b,_ in self.u.mem_regions()]

def verify_case(row,replay=False,helpers=None):
 prefix=prefix_view(row);prior=old.verify_case(prefix);n=row['terminal_name'];need(prior['VM_PC']==76,'full inherited original terminal rules')
 need(n['before']['CPU']==row['after_fade']['CPU'] and n['before']['memory']==row['after_fade']['memory'] and n['before']['trace']==row['after_fade']['trace'],'same pending font source state before continuation')
 native(row);role,source,reference,cfg=independent_pixels(row);count,writes=Replay(row,reference,cfg).execute()
 need(row['image_before']==row['image_after'],'entire original image/IAT retained');overlay.memory_equal(row['final'],n['memory'],'entire actual final source state');need(row['pending_CPU']==n['CPU']==n['pending']['CPU'],'entire final source CPU')
 need(n['state']==dict(row['after_fade']['final'],VM=n['state']['VM']),'whole work/world/owner/task/clock unchanged outside VM')
 v0=bytes.fromhex(n['before']['state']['VM']);v=bytearray(v0);t=e.TEXTURE-e.VM;node=e.NODE-e.VM;gdi=n['calls'];w,h=[1<<(x-1).bit_length() for x in cfg['texture_size']]
 config=struct.unpack_from('<19h',e.CODE,0x624520-0x400000+8*38)
 for o,value,fmt in ((node+0x5C,gdi[0]['result'],'I'),(t+0x28,row['resource_loaded']['owner_device']['pointer'],'I'),(t+0x2C,n['texture']['pointer'],'I'),(t+0x34,25,'I'),(t+0x38,cfg['texture_size'][0],'H'),(t+0x3A,cfg['texture_size'][1],'H'),(t+0x3C,w,'H'),(t+0x3E,h,'H'),(t+0x40,cfg['raster_size'][0],'H'),(t+0x42,cfg['raster_size'][1],'H'),(t+0x44,6,'H'),(t+0x4C,e.MAIN,'I'),(t+0x64,0xFFFFFFFF,'I'),(node+0x2C,config[5],'H'),(node+0x2E,config[6],'H'),(node+0x30,config[4],'H'),(node+0x34,role,'H'),(node+0x44,source['resource_row'],'I')):struct.pack_into('<'+fmt,v,o,value)
 need(n['state']['VM']==v.hex() and read(n['memory'],e.VM,0x9400)==bytes(v),'every independent final VM byte including name geometry and role table')
 need(n['accounting']==row['accounting_baseline']['texture_bytes']+524288+w*h*2,'exact current two-texture accounting')
 p=n['pending'];sp=p['CPU']['ESP'];bp=p['CPU']['EBP'];stack=bytes.fromhex(p['stack']);need(len(stack)==0x20000 and stack==read(n['memory'],e.STACK,0x20000) and p['SEH']=='00000000' and p['first_instruction_executed'] is False,'entire original stack/SEH at unexecuted image entry')
 need((p['entry'],p['receiver'],p['caller'],p['args'])==(0x4CDE10,e.VM,0x4CC0D2,[0x7A4D4C,32]),'original portrait entry ABI, no image function substitute')
 for expected in (0x4C62D4,0x4CEDA7,0x454D90,e.RETURN):
  # The resource cdecl frame precedes layer, handler, VM and task frames.
  if expected==0x4C62D4:need(num(stack,bp-e.STACK+4)==0x4CC26D,'natural resource ancestor');bp=num(stack,bp-e.STACK)
  need(num(stack,bp-e.STACK+4)==expected,'natural pending original ancestor');bp=num(stack,bp-e.STACK)
 need(n['trace']['instructions']==row['instructions'] and n['trace']['writes']==row['writes'] and n['trace']['code_sha256']==row['code_trace_sha256'] and n['trace']['write_sha256']==row['write_trace_sha256'],'all forward trace counters and digests')
 need(n['trace']['instructions']-n['before']['trace']['instructions']==count and n['trace']['writes']-n['before']['trace']['writes']==writes,'continuous original source added counters')
 if replay:
  other=e.run_case(row['input'],helpers[0],helpers[1],[x['result'] for x in row['APIs'] if x['name']=='GetTickCount']);verify_case(other)
  for k in ('initial','final'):overlay.memory_equal(row[k],other[k],'fresh resources / full '+k)
  for k in ('after_fade','pending_CPU','resource_initialization','cleanup_steps','cleanup_state','accounting_baseline','instructions','writes','code_trace_sha256','write_trace_sha256','world_frames','events','commands','task_calls','task_writes','admission','resource_loaded'):
   if k=='resource_loaded':
    for z in ('memory','CPU','trace','record_hex','bank','upload_hex','texture'):need(row[k][z]==other[k][z],'fresh current source-loaded '+z)
   else:need(row[k]==other[k],'fresh original full state/CPU/trace '+k)
  for k in n:
   if k in ('GDI_trace','GDI_handle_projection','GPU_APIs','readback','GYBC_readback'):continue
   need(n[k]==other['terminal_name'][k],'fresh current name full memory/CPU/pixels '+k)
 return dict(name=row['input']['name'],role=role,VM_PC=76,complete_tasks=100,pending_tasks=1,new_name_instructions=count,new_name_writes=writes,GDI_calls=len(gdi),name_raster_size=cfg['raster_size'],name_texture_size=[w,h],portrait_path=n['path'],image_entry_executed=False,owned_regions=len(row['final']),CPU_registers=57,independent_original_code_all_memory_CPU_and_trace_replayed=True,current_native_resources_recreated_for_replay=replay,original_instructions=row['instructions'],original_writes=row['writes'])

def verify(path):
 d=json.loads(gzip.decompress(path.read_bytes()));need(d['source_contract']==e.source_contract() and [r['input'] for r in d['cases']]==e.parent.parent.parent.corpus(),'exact new source and two terminal cases');h=e.helpers('terminal-name-proof');rows=[]
 for r in d['cases']:rows.append(verify_case(r,True,h));print('verified current terminal name',r['input']['name'],flush=True)
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(e.ROOT).as_posix()),cases=rows,implementation_sha256={p:e.sha((e.ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},source_raster_rules=source_catalog(),all_three_GDI_pixel_stages_independently_reproduced=True,all_memory_CPU_and_original_trace_replayed=True,current_native_resources_recreated=True,original_forward_game_roots_added=0,portrait_loading_executed=False,draw_or_Present=False,terminal_presentation_complete=False,task_exit_complete=False,rewards_complete=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();need(not(e.ROOT/a.out).exists(),'fresh immutable proof');e.terminal.save(a.out,verify(e.ROOT/a.report))

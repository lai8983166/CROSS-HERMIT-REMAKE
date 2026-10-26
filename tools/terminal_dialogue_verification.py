"""Independent original first-dialogue bytes, native pixels, ABI and task replay."""
import argparse,copy,ctypes,gzip,hashlib,json,struct,types
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from types import SimpleNamespace
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
import unicorn.x86_const as x86
from tools import terminal_dialogue_emulation as e
from tools import terminal_portrait_verification as previous
from tools import terminal_name_verification as namecheck
from tools.school_retained_portrait_catalog import commands as script_commands
from tools.school_gdi_platform import WindowsGDI
from tools.school_retained_name_verification import Replay as NameABI,NAMES
from tools.school_font_raster_catalog import geometry,convert_surface,source_catalog as raster_rules
from tools.school_second_live_text_catalog import bands
from tools.school_text_timing_catalog import expected_update,BYTES as TEXT_BYTES,source_catalog as timing_rules
need=e.need;num=previous.num;read=previous.read;equal=previous.equal
IMPLEMENTATIONS=('tools/terminal_dialogue_emulation.py','tools/terminal_dialogue_verification.py','tools/terminal_dialogue_preservation.py','tools/tests/test_terminal_dialogue.py')

def raster_dialogue(raw,args,face):
 """Separate current GDI experiment, including naturally blank ANSI punctuation."""
 gd=WindowsGDI()
 try:
  dc=gd.dc();font=gd.font(args,face);gd.select(dc,font);measured,selected=gd.measure(dc,raw);cfg=geometry(measured);bitmap=gd.dib(dc,bytes.fromhex(cfg['header_hex']));gd.select(dc,bitmap);gd.select(dc,gd.handle(gd.g.GetStockObject(4)));w,h=cfg['raster_size'];p=cfg['padding']
  for nm,values in [('SetMapMode',[dc,1]),('PatBlt',[dc,0,0,w,h,0xF00021]),('SetBkMode',[dc,1]),('SetBkColor',[dc,0]),('SetTextAlign',[dc,0])]:
   value=int(getattr(gd.g,nm)(*values));need(value!=0xFFFFFFFF and (nm not in ('SetMapMode','PatBlt','SetBkMode') or value!=0),'independent actual dialogue GDI setup')
  stages=[dict(name='clear',hex=gd.raster(bitmap).hex())]
  for nm,color,xy in [('shadow',0x080808,[2*p,2*p]),('foreground',0xFFFFFF,[p,p])]:
   need(int(gd.g.SetTextColor(dc,color))!=0xFFFFFFFF and int(gd.g.TextOutA(dc,*xy,raw,len(raw)))==1,'independent actual dialogue ANSI output');stages.append(dict(name=nm,hex=gd.raster(bitmap).hex()))
  pixels=gd.raster(bitmap);wide=ctypes.create_unicode_buffer(256);n=ctypes.windll.kernel32.MultiByteToWideChar(gd.acp,0,raw,len(raw),wide,256);need(n>0,'actual Windows ANSI decoding observation')
  result=dict(text_hex=raw.hex(),ACP=gd.acp,ANSI_unicode_codepoints=[ord(c) for c in wide[:n]],measured=measured,selected_face=selected,raster_hex=pixels.hex(),stages=stages,nonzero_bytes=sum(bool(x) for x in pixels))
 finally:cleanup=gd.close()
 need(cleanup==dict(fonts=1,bitmaps=1,dcs=1,all_resources_released=True),'independent dialogue GDI resources closed');return result

def prefix_view(row):
 """Old contract projection; the producer report and native order stay intact."""
 r={k:copy.deepcopy(v) for k,v in row.items() if k not in ('terminal_dialogue','dialogue_cleanup')};d=row['terminal_dialogue'];b=d['before'];p=d['prefix']
 r.update(final=b['memory'],pending_CPU=b['CPU'],instructions=b['trace']['instructions'],writes=b['trace']['writes'],code_trace_sha256=b['trace']['code_sha256'],write_trace_sha256=b['trace']['write_sha256'],task_APIs=r['task_APIs'][:p['task_APIs']],resource_initialization=r['resource_initialization'][:p['resource_steps']],extra_original_instruction_counts=p['extra_counts'])
 r['GPU_trace']=r['GPU_trace'][:p['GPU_wire']]+r['GPU_trace'][-7:]
 for i,x in enumerate(r['GPU_trace']):x['request']['id']=x['reply']['id']=i+1
 r['cleanup_steps']=[s for s in r['cleanup_steps'] if s['label']!='supplemental_original_dialogue_texture_destructor']
 return r

def source(row):
 d=row['terminal_dialogue'];raw=(e.ROOT/e.terminal.SCRIPT_PATH).read_bytes();catalog=script_commands(raw);selector=num(bytes.fromhex(d['before']['state']['task']),0x174);segment=next(s for s in catalog['segments'] if s['index']=={1:2,4:11}[selector]);start=segment['code_start'];end=segment['code_end']
 want=[];script_pointer=num(read(d['before']['memory'],e.VM+16,4),0)
 for pc,op,n in ((96,43,8),(104,17,6),(110,50,4),(114,51,4)):
  need(struct.unpack_from('<HH',raw,start+pc)==(op,n),'original first dialogue opcode/header')
  want.append(dict(PC=pc,opcode=op,bytes=n,source_pointer=script_pointer+pc))
 need(d['commands']==want and struct.unpack_from('<I',raw,start+100)[0]==0x20000008 and struct.unpack_from('<H',raw,start+108)[0]==0,'only original config8 / first text0 / wait50 / confirm51')
 count=num(raw,end);packed=num(raw,end+4);span=packed>>20;at=end+(packed&0xFFFFF);text=raw[at:at+span]
 need(1<=count<=1000 and 2<=span<=256 and span%2==0 and text[-2:]==bytes(2) and 0 not in text[:-2] and at+span<=segment['end'],'independent original bounded ANSI table entry0')
 text=text[:-2];need(b'\\n' not in text,'bounded single original dialogue line')
 cfg=list(struct.unpack_from('<19h',e.CODE,0x624520-0x400000+8*38));need(cfg[0]==5,'source configuration8 layer5')
 font=d['pending_font'];b=d['font_boundary'];obj=read(b['memory'],e.OBJECT,0x18);alternate=bool(obj[0x14]);width=num(obj,0xE if alternate else 0xC,'h')&0xFFFFFFFF;height=num(obj,0x12 if alternate else 0x10,'h')&0xFFFFFFFF
 args=[height,width,0,0,400,0,0,0,1,5,0,0,0,0x5BF62C]
 # The text font comes from the live original object, not the role-name font.
 need(font['args']==args and font['caller']==0x4CAD09,'all14 original text-font arguments/caller')
 need(e.CODE[0x4CACF0-0x400000:0x4CACF5-0x400000]==bytes.fromhex('6890010000'),'original dialogue weight400 push differs from name weight700')
 sp=b['CPU']['ESP'];slot=0x5920A0;target=num(read(b['memory'],slot,4),0)
 need(font==dict(entry=target,caller=0x4CAD09,args=args,CPU=b['CPU'],first_instruction_executed=False) and b['CPU']['EIP']==target and read(b['memory'],sp,60)==struct.pack('<15I',0x4CAD09,*args),'unexecuted original text font with all source ABI stack bytes')
 need(read(d['before']['memory'],script_pointer+96,22)==raw[start+96:start+118],'live script commands match original source bytes')
 return text,cfg,dict(script_sha256=e.sha(raw),segment=segment['index'],source_offset=at,text_hex=text.hex(),text_big5=text.decode('cp950'),commands=[dict(PC=pc,source_offset=start+pc) for pc in (96,104,110,114)])

def draw_rules():
 pairs={0x4CBF31:('mov','dword ptr [ecx + 0x5c], edx'),0x4CBF3A:('mov','byte ptr [eax + 0x67], cl'),0x4CBF43:('mov','byte ptr [edx + 0x66], al'),0x4CBF4C:('mov','byte ptr [ecx + 0x65], dl'),0x4CBF55:('mov','byte ptr [eax + 0x64], cl'),0x4CBF5F:('mov','word ptr [edx + 0x76], ax')};md=Cs(CS_ARCH_X86,CS_MODE_32);out=[]
 for at,pair in pairs.items():
  i=next(md.disasm(e.CODE[at-0x400000:at-0x400000+16],at,count=1));need((i.mnemonic,i.op_str)==pair,'independent original text draw metadata store');out.append(dict(va=at,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
 return out

def pixels(row):
 d=row['terminal_dialogue'];raw,cfg,provenance=source(row);args=d['pending_font']['args'];reference=raster_dialogue(raw,args[:-1],namecheck.original_text(args[-1]));r=d['raster'];geo=geometry(reference['measured'])
 need(d['geometry']==geo and d['texture_record']==e.TEXTURE,'independent source dialogue geometry and texture record')
 need((r['ACP'],r['measured'],r['selected_face'],r['raster_hex'])==(reference['ACP'],reference['measured'],reference['selected_face'],reference['raster_hex']),'independent current GDI ANSI metrics/face/all pixels')
 need([s['name'] for s in r['stages']]==['PatBlt','TextOutA','TextOutA'] and [s['hex'] for s in r['stages']]==[s['hex'] for s in reference['stages']],'all three independently redrawn real GDI stages')
 need([a['name'] for a in d['calls']]==NAMES+['SelectObject','DeleteObject','DeleteDC','DeleteObject'] and r['calls']==d['calls'][:23],'all27 original dialogue raster/cleanup leaves')
 w,h=[1<<(v-1).bit_length() for v in geo['texture_size']];lock=d['lock'];out=bytes.fromhex(lock['hex'])
 need(lock['pitch']==w*2 and out==bytes(w*h*2),'whole newly created current dialogue surface initially zero')
 expected=bands(geo);need([dict(rect=x['rect'],point=x['point']) for x in d['conversions']]==expected,'all source-derived original conversion bands')
 for b in expected:out=convert_surface(bytes.fromhex(reference['raster_hex']),geo['raster_size'],b['rect'],out,lock['pitch'],b['point'])
 need(d['upload_hex']==d['readback']['hex']==out.hex() and d['readback']['sha256']==e.sha(out) and d['readback']['pitch']==lock['pitch'],'every independently converted texel equals current actual full GPU readback')
 need(d['accounting']==num(read(d['before']['memory'],0x765720,4),0)+w*h*2==num(read(d['final']['memory'],0x765720,4),0),'independent fourth-texture original accounting')
 for key,want in [('GYBC_readback',row['resource_loaded']['upload_hex']),('name_readback',row['terminal_name']['upload_hex']),('portrait_readback',row['terminal_portrait']['upload_hex'])]:need(d[key]['hex']==want,'prior live whole texture preserved '+key)
 return reference,geo,provenance

def native(row):
 d=row['terminal_dialogue'];gt=row['GPU_trace'];ct=row['CRT_trace'];p=d['prefix'];first=p['GPU_wire'];need(first==18,'exact three current textures before dialogue')
 for label,trace in [('GPU',gt),('CRT',ct)]:
  for i,x in enumerate(trace):need(x['request']['id']==x['reply']['id']==i+1 and x['reply']['ok'] is True,'complete actual ordered '+label+' native protocol')
 need([x['request']['op'] for x in gt]==['create','describe','lock','unlock','readback']*2+['readback']+['create','describe','lock','unlock','readback','readback','readback']+['create','describe','lock','unlock','readback','readback','readback','readback']+['describe','release']*4+['close'],'four same-lifetime textures, whole readbacks and all original releases')
 calls=d['GPU_APIs']+row['dialogue_cleanup']['GPU_APIs'];need(len(calls)==6,'four original dialogue COM leaves and two original destruction leaves')
 ledger=row['typed_GPU_projection'];gpu_map={x['native']:x['guest'] for x in ledger};need(len(gpu_map)==len(ledger) and len(set(gpu_map.values()))==len(ledger) and all(x['domain']=='overlay' for x in ledger),'one current typed GPU owner with unambiguous identity')
 def translated(v,key=None):
  if isinstance(v,dict):return {k:({s:gpu_map[p] for s,p in x.items()} if k=='methods' else translated(x,k)) for k,x in v.items()}
  if isinstance(v,list):return [translated(x) for x in v]
  return gpu_map[v] if type(v)is int and v and key in ('pointer','vtable','bits','method_pointer') else v
 native_texture=calls[0]['native_result']['texture']['pointer'];w,h=[1<<(v-1).bit_length() for v in d['geometry']['texture_size']]
 for a,i in zip(calls,(18,19,20,21,26,27)):
  req=gt[i]['request'];op=a['op'];expected=dict(id=i+1,op=op)
  if op=='create':expected.update(width=w,height=h,levels=1,usage=0,format=25,pool=1)
  else:
   expected['pointer']=native_texture
   if op=='lock':expected['flags']=2048
   elif op=='unlock':expected['hex']=d['upload_hex']
  need(req==expected and a['native_result']==gt[i]['reply']['result'] and a['result']==translated(a['native_result']) and a['actual_API_executed'] is True,'each complete original dialogue COM request, typed output and current native receipt')
 need(gt[21]['request']['hex']==d['upload_hex'] and gt[22]['reply']['result']==d['readback'],'actual dialogue whole upload/readback wire')
 for i,key in ((23,'GYBC_readback'),(24,'name_readback'),(25,'portrait_readback')):need(gt[i]['reply']['result']==d[key],'actual preserved texture wire '+key)
 need(not row['GPU_cleanup']['texture_releases'] and row['GPU_cleanup']==gt[-1]['reply']['result'] and row['CRT_cleanup']==ct[-1]['reply']['result'] and row['CRT_cleanup']['all_owned_resources_released'] and row['CRT_exit']==row['GPU_exit']==0,'normal all-original owned cleanup and platform exit')
 # Check the old leaves against the unedited raw wire, including exact identity.
 oldcalls=row['GPU_APIs'][:4]+row['terminal_name']['GPU_APIs']+row['terminal_portrait']['GPU_APIs']+row['portrait_cleanup']['GPU_APIs']+row['name_cleanup']['GPU_APIs']+row['GPU_APIs'][4:]
 need(len(oldcalls)==18,'every retained original COM leaf present')
 for a,i in zip(oldcalls,(0,1,2,3,5,6,7,8,11,12,13,14,28,29,30,31,32,33)):need(a['native_result']==gt[i]['reply']['result'] and a['op']==gt[i]['request']['op'] and a['actual_API_executed'] is True,'retained original COM exact actual native wire')
 ledger=d['GDI_handle_projection'];mapping={x['guest']:x['native'] for x in ledger};need(len(mapping)==len(ledger) and all(x['domain']=='GDI' for x in ledger),'one typed current native GDI lifetime')
 old=row['terminal_name']['GDI_handle_projection'];need(ledger[:len(old)]==old,'same actual GDI/DC service retained from role name')
 measure=num(read(d['before']['memory'],e.MAIN+0xB208,4),0);need(measure==old[0]['guest'],'unchanged live measurement DC')
 def nat(v):need(v in mapping,'known GDI typed handle');return mapping[v]
 need(len(d['calls'])==len(d['GDI_trace']),'every original dialogue GDI leaf has current native receipt')
 for c,t in zip(d['calls'],d['GDI_trace']):
  args=c['args'];name=c['name'];native_args=list(args)
  if name not in ('CreateFontA','lstrlenA','CreateCompatibleDC','GetStockObject'):native_args[0]=nat(args[0])
  if name=='SelectObject':native_args[1]=nat(args[1])
  result=nat(c['result']) if name in ('CreateFontA','CreateCompatibleDC','CreateDIBSection','GetStockObject','SelectObject') else c['result']
  need(t['name']==name and t['args']==args and t['native_args']==native_args and t['logical_result']==c['result'] and t['native_result']['args']==native_args and t['native_result']['result']==result and c['actual_API_executed'] is True,'every typed GDI argument and logical/native result')
  outputs=copy.deepcopy(t['native_result']);outputs.pop('dc_translated_args',None);outputs.pop('native_bits',None);outputs.update(args=args,result=c['result'],actual_API_executed=True)
  need(all(c[k]==v for k,v in outputs.items()),'complete current GDI native output contract')
 need(row['dialogue_cleanup']['texture_bytes']==row['terminal_name']['accounting']+262144,'original dialogue destructor preserves exact prior-three-texture accounting')
 task_calls=[x['call'] for x in d['leaves'] if x['kind']=='TASK'];actual=row['task_APIs'][p['task_APIs']:]
 need(len(task_calls)==len(actual) and all(all(c[k]==v for k,v in a.items()) for c,a in zip(task_calls,actual)),'every actual current task query is consumed exactly once')

class Replay(namecheck.Replay):
 """A new Unicorn executor; source bytes execute every new instruction."""
 def __init__(self,row,reference,cfg):
  self.row=row;self.d=row['terminal_dialogue'];self.n=self.p=dict(before=self.d['before']);self.reference=reference;self.cfg=cfg;self.u=Uc(UC_ARCH_X86,UC_MODE_32);self.image=e.CODE;self.objects={};self.locks={};self.cleaning=False
  for r in self.d['before']['memory']:self.u.mem_map(r['pointer'],r['bytes']);self.u.mem_write(r['pointer'],bytes.fromhex(r['hex']))
  cpu=self.d['before']['CPU'];first=['GDTR','IDTR','LDTR','TR','CR0','CR2','CR3','CR4']
  for k in first+[k for k in cpu if k not in first]:
   reg=getattr(x86,'UC_X86_REG_'+k);v=tuple(cpu[k]) if isinstance(cpu[k],list) else cpu[k]
   if self.u.reg_read(reg)!=v:self.u.reg_write(reg,v)
  need(self.cpu()==cpu and len(cpu)==57,'all57 initial architectural registers restored')
  calls=self.d['calls'];o=dict(logical_measurement_dc=num(self.read(e.MAIN+0xB208,4),0),font=calls[0]['result'],raster_dc=calls[6]['result'],bitmap=calls[7]['result'],ACP=reference['ACP'],measured=reference['measured'],selected_face=reference['selected_face']);o['fresh_owned_measurement_dc']=o['logical_measurement_dc']
  self.case=dict(offscreen=o,parent_boundary=dict(pending_font=self.d['pending_font']));self.old_font=self.brush=0;self.raw=bytes.fromhex(reference['text_hex']);self.local_text=None
  from tools import school_retained_name_raster as work
  proxy=SimpleNamespace(**dict(vars(work),RASTER=e.RASTER,IMPORTS=e.GDI))
  def constants(code):
   values=[]
   for v in code.co_consts:
    if isinstance(v,types.CodeType):v=constants(v)
    elif v==0x4CA7CB:v=0x4CAD09
    values.append(v)
   return code.replace(co_consts=tuple(values))
  self.check_raster_API=types.FunctionType(constants(NameABI.api.__code__),dict(NameABI.api.__globals__,work=proxy))
 def state(self):return previous.Replay.state(self)
 def queue(self):return previous.Replay.queue(self)
 def leaf(self,item):
  c=item['call'];kind=item['kind'];sp=self.cpu()['ESP'];ret=num(self.read(sp,4),0);args=[num(self.read(sp+4+i,4),0) for i in range(0,c['pop'],4)]
  need((sp,ret,args)==(c['sp'],c['return_va'],c['args']),'all original platform source stack arguments/return')
  if kind=='GDI':
   idx=next(i for i,a in enumerate(self.d['calls']) if a is c or a==c);slot=c['import_slot'];need(num(self.read(slot,4),0)==c['target'] and e.GDI[slot][0]==c['name'],'unchanged original GDI IAT')
   if idx<23:
    if c['name']=='lstrlenA' and self.local_text is None:self.local_text=args[0]
    r=copy.deepcopy(c);r['dc_translated_args']=r['args']
    if c['name']=='CreateDIBSection':r['native_bits']=self.d['GDI_trace'][idx]['native_result']['native_bits']
    self.check_raster_API(self,dict(key='retained_name_GDI',va=c['target'],call=r));return
   o=self.case['offscreen'];expect=[('SelectObject',0x4058D8,[o['raster_dc'],self.d['calls'][8]['result']]),('DeleteObject',0x405921,[o['bitmap']]),('DeleteDC',0x40596A,[o['raster_dc']]),('DeleteObject',0x4D1C1B,[o['font']])][idx-23]
   need((c['name'],ret,args)==expect and c['memory_outputs']==[] and c['result']==(o['bitmap'] if idx==23 else 1),'original natural GDI object restoration/deletion');value=c['result']
  elif kind=='TASK':
   name,slot,caller=e.parent.TASK_APIS[c['target']];need((c['name'],c['import_slot'],ret)==(name,slot,caller) and num(self.read(slot,4),0)==c['target'] and c['actual_API_executed'] is True and c['value']==0 and c['memory_outputs']==[] and args==([0] if name=='ImmGetOpenStatus' else [e.INPUT+0x528]),'actual original null-IME and empty-input query');value=0
  else:
   need(kind=='GPU','no game function return substitution');t=self.d['texture'];slot=c['slot'];bp=self.cpu()['EBP'];out=[]
   need(c['target']==(self.row['resource_loaded']['owner_device']['methods']['80'] if slot==80 else t['methods'][str(slot)]),'current original COM identity')
   def output(p,b):out.append(dict(pointer=p,hex=b.hex()))
   w,h=[1<<(v-1).bit_length() for v in self.cfg['texture_size']]
   if slot==80:need(args==[self.row['resource_loaded']['owner_device']['pointer'],w,h,1,0,25,1,e.TEXTURE+44] and ret==0x403C8A,'original dialogue creation ABI');self.identities(c['result']);output(args[-1],struct.pack('<I',t['pointer']))
   elif slot==56:
    need(args==[t['pointer'],0,bp-(36 if self.cleaning else 52)] and ret==(0x403A44 if self.cleaning else 0x403CBE) and struct.unpack('<8I',bytes.fromhex(c['result']['hex']))==(25,1,0,1,w*h*2,0,w,h),'complete independent original dialogue descriptor');output(args[-1],bytes.fromhex(c['result']['hex']))
   elif slot==64:need(args==[t['pointer'],0,num(self.read(bp+8,4),0),0,2048] and ret==0x40395E,'original dialogue LockRect ABI');output(self.d['lock']['bits'],bytes.fromhex(self.d['lock']['hex']));output(args[2],struct.pack('<II',self.d['lock']['pitch'],self.d['lock']['bits']))
   elif slot==8:need(self.cleaning and args==[t['pointer']] and ret==0x40378D,'original supplemental dialogue Release ABI')
   else:need(slot==68 and not self.cleaning and args==[t['pointer'],0] and ret==0x4039D3 and self.read(self.d['lock']['bits'],len(bytes.fromhex(self.d['upload_hex']))).hex()==self.d['upload_hex'],'every original converted texel at UnlockRect')
   need(out==c['memory_outputs'] and c['value']==0,'all and only predicted original COM outputs')
   for r in out:self.put(r['pointer'],bytes.fromhex(r['hex']))
   value=0
  self.u.reg_write(x86.UC_X86_REG_EAX,value);self.u.reg_write(x86.UC_X86_REG_ESP,sp+4+c['pop']);self.u.reg_write(x86.UC_X86_REG_EIP,ret)
 def execute(self):
  d=self.d;index=count=writes=0;ih=hashlib.sha256();wh=hashlib.sha256();root_index=0;observed=[];queries=[];commands=[];conversions=[]
  def mark():return dict(instructions=count,writes=writes,code_sha256=ih.hexdigest(),write_sha256=wh.hexdigest())
  def code(u,at,size,_):
   nonlocal index,count
   if at==self.stop:u.emu_stop();return
   if index<len(d['leaves']) and at==d['leaves'][index]['call']['target']:self.leaf(d['leaves'][index]);index+=1;return
   if at==0x4CE9C5:
    p=num(self.read(e.VM+16,4),0)+num(self.read(e.VM+28,4),0);op,n=struct.unpack('<HH',self.read(p,4));commands.append(dict(PC=num(self.read(e.VM+28,4),0),opcode=op,bytes=n,source_pointer=p))
   if at==0x405869:
    sp=self.cpu()['ESP'];a=[num(self.read(sp+j,4),0) for j in range(0,24,4)];conversions.append(dict(entry=at,args=a,rect=list(struct.unpack('<4I',self.read(a[4],16))),point=list(struct.unpack('<2I',self.read(a[5],8)))))
   if at in (0x4CB5F0,0x4CD3B7,0x4D5EC0,0x4CD402,0x4128F0,0x4CD432,0x4CCFF7,0x4CCB30,0x4CD02D):
    cpu=self.cpu();queries.append(dict(entry=at,CPU=cpu,receiver=cpu['ECX'],stack_hex=self.read(cpu['ESP'],28).hex(),object_hex=self.read(e.OBJECT,0xAB8).hex()))
   need(0x400000<=at<0x592000 and self.read(at,size)==e.CODE[at-0x400000:at-0x400000+size] and e.CODE[at-0x400000]!=0xCC,'only unchanged original dialogue instruction '+hex(at));count+=1;ih.update(struct.pack('<I',at))
  def write(u,access,at,size,value,_):
   nonlocal writes
   need(not 0x400000<=at<0x593000,'no original code or IAT mutation');writes+=1;wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if e.VM<=at<e.VM+0x9400 or at==0:observed.append(dict(pc=self.cpu()['EIP'],address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
  hooks=[self.u.hook_add(UC_HOOK_CODE,code),self.u.hook_add(UC_HOOK_MEM_WRITE,write)]
  boundaries={k:d[k] for k in ('font_boundary','raster','completion','ready','confirmation','final')};seen=set();frames={f['segments'][1]-1:f for f in d['frames']};last=d['before']['trace']
  for i,s in enumerate(d['segments']):
   need(self.cpu()==s['before_CPU'] and mark()==s['local_before'] and index==s['leaves'][0] and last==s['trace_before'],'continuous full source segment input')
   if s['root']:
    va,recv=((0x40DB90,e.MANAGER),(0x40DC80,e.MANAGER),(0x425DE0,e.INPUT),(0x454CF0,e.TASK))[root_index%4];root_index+=1;need(s['entry']==va and s['root']==dict(receiver=recv,args=[]),'only original queue/input/full-task roots')
    self.put(e.STACK+0xF000,struct.pack('<I',e.RETURN));self.u.reg_write(x86.UC_X86_REG_ESP,e.STACK+0xF000);self.u.reg_write(x86.UC_X86_REG_ECX,recv)
   else:need(s['entry']==self.cpu()['EIP'],'continuation starts at same pending original PC')
   self.stop=s['stop'];self.u.emu_start(s['entry'],0,count=4_000_000,timeout=60_000_000)
   need(self.cpu()==s['CPU'] and mark()==s['local_after'] and index==s['leaves'][1],'all57 registers, original PCs and original writes at every segment')
   need(s['trace_after']['instructions']-s['trace_before']['instructions']==s['local_after']['instructions']-s['local_before']['instructions'] and s['trace_after']['writes']-s['trace_before']['writes']==s['local_after']['writes']-s['local_before']['writes'],'continuous added original counters');last=s['trace_after']
   for key,b in boundaries.items():
    if mark()==b['local_trace']:
     equal(self.snapshot(),b['memory'],'all original mapped bytes at '+key);need(self.cpu()==b['CPU'] and self.state()==b['state'] and self.queue()==b['queue'] and b['trace']==last,'whole source CPU/state/queue at '+key);seen.add(key)
   if i in frames:
    f=frames[i];b=f['capture'];equal(self.snapshot(),b['memory'],'all independently replayed mapped bytes after frame '+str(f['index']))
    need(self.state()==f['after']==b['state'] and self.queue()==f['queue_after']==b['queue'] and self.cpu()==b['CPU'] and mark()==b['local_trace'] and last==b['trace'],'all57 CPU registers, full state, queues and digests after every original frame')
  need(root_index==4*len(d['frames']) and seen==set(boundaries) and index==len(d['leaves']) and observed==d['writes'],'every full boundary, platform leaf and original VM store replayed')
  need(queries==d['queries'] and commands==d['commands'] and conversions==d['conversions'],'all observed original query CPU/objects, command dispatches and conversion stack bytes')
  equal(self.snapshot(),d['final']['memory'],'all final source memory')
  for h in hooks:self.u.hook_del(h)
  cleanup=self.cleanup();return dict(instructions=count,writes=writes,cleanup=cleanup)
 def cleanup(self):
  """Continue the original supplemental destructor from the verified final CPU."""
  c=self.row['dialogue_cleanup'];s=next(x for x in self.row['cleanup_steps'] if x['label']=='supplemental_original_dialogue_texture_destructor');calls=c['GPU_APIs'];index=count=writes=0
  need(self.cpu()==c['before_CPU']==s['before_cpu'] and s['trace_before']==self.d['final']['trace'] and (s['entry'],s['receiver'],s['args'],s['cdecl'])==(0x403730,e.TEXTURE,[],False),'explicit supplemental original destructor begins after the frozen forward boundary')
  self.put(e.STACK+0xF000,struct.pack('<I',e.RETURN));self.u.reg_write(x86.UC_X86_REG_ESP,e.STACK+0xF000);self.u.reg_write(x86.UC_X86_REG_ECX,e.TEXTURE);self.cleaning=True
  def code(u,at,size,_):
   nonlocal index,count
   if at==e.RETURN:u.emu_stop();return
   if index<len(calls) and at==calls[index]['target']:self.leaf(dict(kind='GPU',call=calls[index]));index+=1;return
   need(0x400000<=at<0x592000 and self.read(at,size)==e.CODE[at-0x400000:at-0x400000+size] and e.CODE[at-0x400000]!=0xCC,'only unchanged original supplemental destructor instruction');count+=1
  def write(u,access,at,size,value,_):
   nonlocal writes
   need(not 0x400000<=at<0x593000,'no original code or IAT mutation during destruction');writes+=1
  hooks=[self.u.hook_add(UC_HOOK_CODE,code),self.u.hook_add(UC_HOOK_MEM_WRITE,write)];self.u.emu_start(0x403730,0,count=10000,timeout=60_000_000)
  need(index==2 and self.cpu()==c['CPU']==s['cpu_after'] and self.cpu()['EIP']==e.RETURN and self.cpu()['ESP']==e.STACK+0xF004,'all supplemental original COM leaves and57 CPU values at natural return')
  need(count==s['trace_after']['instructions']-s['trace_before']['instructions'] and writes==s['trace_after']['writes']-s['trace_before']['writes'],'all supplemental original instruction/write counts')
  need(self.read(e.TEXTURE,0x68).hex()==c['record_hex'] and num(self.read(e.TEXTURE+44,4),0)==0 and num(self.read(0x765720,4),0)==c['texture_bytes'],'entire original destroyed record and unchanged predecessor accounting')
  for h in hooks:self.u.hook_del(h)
  return dict(instructions=count,writes=writes,CPU_registers=57)

def timing(row):
 d=row['terminal_dialogue'];before=d['before']['state'];obj=0x430+5*0xAB8;node=0x6F60+5*0xE0;frames=d['frames'];need(len(frames)>=7,'complete source activation and waiting frames')
 def vw(s,o,f='H'):return num(bytes.fromhex(s['VM']),o,f)
 need((vw(before,28,'I'),vw(before,0x20))==(96,0),'source PC96 role readiness precedes43')
 need((vw(frames[0]['after'],28,'I'),vw(frames[0]['after'],0x20))==(104,0) and frames[1]['before']==frames[0]['after'],'config43 completes its own original full task before17')
 need((vw(d['completion']['state'],28,'I'),vw(d['completion']['state'],0x20))==(110,0),'first text17 full task completes at110')
 need((vw(d['ready']['state'],28,'I'),vw(d['ready']['state'],0x20))==(114,0) and (vw(d['confirmation']['state'],28,'I'),vw(d['confirmation']['state'],0x20))==(118,1),'original text readiness then confirmation wait')
 states=[d['completion']['state']];states.extend(f['after'] for f in frames if vw(f['before'],28,'I')>=110)
 prev=None
 for i,f in enumerate(frames):
  need(f['index']==i and f['segments'][1]-f['segments'][0]==(6 if i==1 else 4) and f['phase']==('select_text_config' if i==0 else 'first_sentence' if i==1 else 'enter_confirmation' if i==len(frames)-3 else 'held_confirmation' if i>=len(frames)-2 else 'text_readiness'),'one full original four-root frame with first raster continuation segments')
  if prev is not None:need(f['before']==prev['after'] and f['queue_before']==prev['queue_after'],'continuous frame state/queue')
  prev=f
  need(f['after']['remaining']==before['remaining'] and f['after']['elapsed']==before['elapsed'] and f['after']['SEH']=='00000000','paused world and natural original task return')
 for a,b in zip(states,states[1:]):
  raw=bytes.fromhex(a['VM']);origin=[num(raw,node+0x1E,'H'),num(raw,node+0x20,'H')];update=expected_update(raw[obj:obj+TEXT_BYTES],origin,e.VM+obj)
  out=bytearray.fromhex(update['after_hex'])
  for draw in update['draws']:
   args=draw['args'];o=args[0]-(e.VM+obj);struct.pack_into('<I',out,o+0x5C,args[3]);out[o+0x64:o+0x68]=bytes([args[7]&255,args[6]&255,args[5]&255,args[4]&255]);struct.pack_into('<H',out,o+0x76,args[8])
  need(bytes.fromhex(b['VM'])[obj:obj+TEXT_BYTES]==bytes(out),'independent original text fade/cadence and source draw metadata for the whole object')
 last=frames[-2:];need(len(last)==2 and all((vw(f['before'],28,'I'),vw(f['after'],28,'I'),vw(f['before'],0x20),vw(f['after'],0x20))==(118,118,1,1) for f in last),'two separate no-input full tasks preserve original confirmation wait')
 need(d['final']['state']==last[-1]['after'] and all(vw(f['after'],28,'I')<=118 for f in frames),'successor27 remains unexecuted')
 return dict(timing=timing_rules(),original_draw_metadata_stores=draw_rules())

def verify_case(row,replay=False,helpers=None):
 prefix=prefix_view(row);need(prefix['CRT_trace']==row['CRT_trace'] and prefix['CRT_APIs']==row['CRT_APIs'],'complete raw CRT order and ABI remain unprojected for frozen independent validation');previous.verify_case(prefix);d=row['terminal_dialogue']
 need(all(d['before'][k]==row['terminal_portrait']['final'][k] for k in ('memory','CPU','state','queue','trace')) and d['before']['local_trace']==dict(instructions=0,writes=0,code_sha256=e.sha(b''),write_sha256=e.sha(b'')),'same live three-resource original boundary with a separate zero-based dialogue trace')
 reference,cfg,provenance=pixels(row);native(row);timing(row);counts=Replay(row,reference,cfg).execute();f=d['final']
 equal(row['final'],f['memory'],'actual final whole memory');need(row['pending_CPU']==f['CPU'] and f['CPU']['EIP']==e.RETURN and f['CPU']['ESP']==e.STACK+0xF004 and row['image_before']==row['image_after'],'natural full task return and unchanged whole source image/IAT')
 need((row['instructions'],row['writes'],row['code_trace_sha256'],row['write_trace_sha256'])==(f['trace']['instructions'],f['trace']['writes'],f['trace']['code_sha256'],f['trace']['write_sha256']),'actual cumulative original instruction/write digest')
 if replay:
  other=e.run_case(row['input'],helpers[0],helpers[1],[x['result'] for x in row['APIs'] if x['name']=='GetTickCount']);verify_case(other)
  for k in ('initial','final'):equal(row[k],other[k],'new current resources complete '+k)
  for k in ('pending_CPU','after_fade','resource_initialization','cleanup_steps','cleanup_state','accounting_baseline','instructions','writes','code_trace_sha256','write_trace_sha256','world_frames','events','commands','task_calls','task_writes','admission'):need(row[k]==other[k],'new current original complete state '+k)
  for key in ('before','font_boundary','raster','completion','ready','confirmation','final'):
   for k in ('memory','CPU','state','queue','trace','local_trace'):need(d[key][k]==other['terminal_dialogue'][key][k],'new current resources all mapped memory/registers/state/digests '+key+'/'+k)
  for k in ('segments','frames','commands','writes','calls','conversions','upload_hex','pending_font'):
   need(d[k]==other['terminal_dialogue'][k],'new current resource complete original dialogue '+k)
 return dict(name=row['input']['name'],VM_PC=118,VM_wait=1,next_opcode27_executed=False,no_input_hold_tasks=2,source=provenance,dialogue_GDI_calls=len(d['calls']),font_args=d['pending_font']['args'],selected_face=reference['selected_face'],ANSI_code_page=reference['ACP'],ANSI_unicode_codepoints=reference['ANSI_unicode_codepoints'],raster_stages_nonzero_bytes=[sum(bool(v) for v in bytes.fromhex(s['hex'])) for s in reference['stages']],raster_nonzero_bytes=reference['nonzero_bytes'],dialogue_texture_size=[1<<(v-1).bit_length() for v in cfg['texture_size']],dialogue_pixels=len(bytes.fromhex(d['upload_hex']))//2,new_original_instructions=counts['instructions'],new_original_writes=counts['writes'],supplemental_original_dialogue_destructor=counts['cleanup'],owned_regions=len(row['final']),CPU_registers=57,independent_original_full_memory_CPU_and_trace_replayed=True,current_native_resources_recreated_for_replay=replay,original_instructions=row['instructions'],original_writes=row['writes'])

def verify(path):
 d=json.loads(gzip.decompress(path.read_bytes()));need(d['source_contract']==e.source_contract() and [r['input'] for r in d['cases']]==e.parent.overlay.parent.corpus(),'exact original source and both terminal branches');h=e.helpers('terminal-dialogue-proof');rows=[]
 for row in d['cases']:rows.append(verify_case(row,True,h));print('verified current terminal first dialogue',row['input']['name'],flush=True)
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(e.ROOT).as_posix()),cases=rows,implementation_sha256={p:e.sha((e.ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},source_raster_rules=raster_rules(),source_text_timing_rules=timing_rules(),source_text_draw_metadata_stores=draw_rules(),all_three_GDI_pixel_stages_independently_reproduced=True,all_pixels_native_protocol_and_ABI_verified=True,independent_original_full_memory_CPU_and_trace_replayed=True,current_native_resources_recreated=True,new_forward_VM_roots=0,next_instruction27_executed=False,ANSI_encoding_fixed=False,visible_dialogue_confirmed=False,actual_draw_or_Present=False,terminal_presentation_complete=False,task_exit_complete=False,rewards_complete=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();need(not(e.ROOT/a.out).exists(),'fresh immutable proof');e.terminal.save(a.out,verify(e.ROOT/a.report))

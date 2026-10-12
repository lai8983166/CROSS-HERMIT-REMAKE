"""Natural first text texture upload and VM return through owned real platform objects."""
import argparse,hashlib,json,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EDX
from tools.school_font_raster_emulation import *
from tools.school_d3d8_bridge import LiveD3D8,build
from tools.school_board_opening_emulation import CODE as BOARD_CODE
from tools.school_script_opening_emulation import CODE as SCRIPT_CODE
from tools.school_text_preparation_emulation import CODE as TEXT_CODE

MIRROR=0x37000000;MIRROR_BYTES=0x100000
LIVE_RANGES=((0x403BD0,0x403D44),(0x403B70,0x403BCA),(0x403910,0x40398A),(0x403990,0x4039FD),
 (0x405779,0x4059D4),(0x405A80,0x405BB4),(0x4CAD7C,0x4CADD3),(0x4D1BF0,0x4D1C5D))
LIVE_CODE=frozenset(a for lo,hi in LIVE_RANGES for a in range(lo,hi))

class SchoolLiveTextEmulator(SchoolFontRasterEmulator):
 def __init__(self):
  self.live_loading=False;super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if not self.live_loading:return super()._write_hook(uc,access,address,size,value,context)
  if MIRROR<=address<MIRROR+MIRROR_BYTES and address+size>MIRROR+getattr(self,'lock_bytes',0):raise RuntimeError('live actual locked extent')
  if not any(a<=address and address+size<=b for a,b in self.live_allowed):raise RuntimeError(f'live finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')

 def _live_write(self,address,raw):
  self._write_hook(self.uc,0,address,len(raw),0,None);self.uc.mem_write(address,raw)

 def _remote_load(self,address,reg,pointer,identity):
  if pointer!=identity['pointer']:raise RuntimeError('original remote object ownership')
  self.remote_reads.append({'source_va':hex(address),'pointer':pointer,'vtable':identity['vtable']})
  self.uc.reg_write(reg,identity['vtable']);self.uc.reg_write(UC_X86_REG_EIP,address+2)

 def _dispatch(self,address,table,offset,args,pop,result):
  identity=self.bridge.device if address==0x403C87 else self.bridge.texture
  if table!=identity['vtable'] or args[0]!=identity['pointer']:raise RuntimeError('original live COM dispatch ownership')
  target=identity['methods'][str(offset)]
  self.com_records.append({'source_va':hex(address),'vtable':table,'offset':offset,'actual_method':target,'args':args,'result':deepcopy(result)})
  sp=self.uc.reg_read(UC_X86_REG_ESP);self.uc.reg_write(UC_X86_REG_EAX,result['hr']);self.uc.reg_write(UC_X86_REG_ESP,sp+pop);self.uc.reg_write(UC_X86_REG_EIP,address+3)

 def _hook(self,uc,address,size,context):
  if not self.live_loading:return super()._hook(uc,address,size,context)
  sp=uc.reg_read(UC_X86_REG_ESP);frame=uc.reg_read(UC_X86_REG_EBP)
  reg=lambda r:uc.reg_read(r)
  if address in (0x403C81,0x403CB8,0x403958,0x4039CD):
   specs={0x403C81:(UC_X86_REG_ECX,UC_X86_REG_EAX,self.bridge.device),0x403CB8:(UC_X86_REG_EAX,UC_X86_REG_ECX,self.bridge.texture),
    0x403958:(UC_X86_REG_ECX,UC_X86_REG_EDX,self.bridge.texture),0x4039CD:(UC_X86_REG_EAX,UC_X86_REG_ECX,self.bridge.texture)}
   target,source,identity=specs[address];self._remote_load(address,target,reg(source),identity);return
  if address in (0x403C87,0x403CBB,0x40395B,0x4039D0):
   count={0x403C87:8,0x403CBB:3,0x40395B:5,0x4039D0:2}[address];args=[self.read(sp+4*i) for i in range(count)]
   if address==0x403C87:
    if args!=[self.device,256,32,1,0,25,1,TEXTURE+0x2C]:raise RuntimeError('original exact live CreateTexture')
    result=self.bridge.create(*args[1:3],*args[3:7]);self._live_write(args[-1],struct.pack('<I',result['texture']['pointer']));table=reg(UC_X86_REG_ECX);offset=0x50
   elif address==0x403CBB:
    if args!=[self.bridge.texture['pointer'],0,frame-0x34]:raise RuntimeError('original live level descriptor')
    result=self.bridge.describe(args[0]);self._live_write(args[2],bytes.fromhex(result['hex']));table=reg(UC_X86_REG_EAX);offset=0x38
   elif address==0x40395B:
    if args!=[self.bridge.texture['pointer'],0,self.lock_output,0,0x800]:raise RuntimeError('original exact texture lock')
    result=self.bridge.lock(args[0]);raw=bytes.fromhex(result['hex']);self.lock_before=raw;self.lock_bytes=len(raw);self.lock_pitch=result['pitch'];self.host_bits=result['bits']
    self._live_write(MIRROR,raw);self._live_write(args[2],struct.pack('<2I',self.lock_pitch,MIRROR));table=reg(UC_X86_REG_ECX);offset=0x40
   else:
    if args!=[self.bridge.texture['pointer'],0]:raise RuntimeError('original exact texture unlock')
    raw=bytes(uc.mem_read(MIRROR,self.lock_bytes));self.lock_after=raw;result=self.bridge.unlock(args[0],raw);table=reg(UC_X86_REG_EAX);offset=0x44
   self._dispatch(address,table,offset,args,4*count,result);return
  if address==0x403910:
   if self.read(sp)!=0x405796 or reg(UC_X86_REG_ECX)!=TEXTURE:raise RuntimeError('natural font lock caller')
   self.lock_output=self.read(sp+4)
  if address in (0xE310000,0xE310010,0xE310020):
   ret=self.read(sp);g=self.platform
   if address==0xE310000:
    args=[self.read(sp+4),self.read(sp+8)]
    if ret!=0x4058D8 or args!=[self.raster_dc,self.native_old_bitmap]:raise RuntimeError('original raster bitmap restoration')
    result=g.select(*args);pop=8;name='SelectObject'
   elif address==0xE310010:
    args=[self.read(sp+4)];wanted=self.bitmap if ret==0x405921 else self.font_handle
    if ret not in (0x405921,0x4D1C1B) or args!=[wanted]:raise RuntimeError('original raster/font deletion')
    result=g.delete_object(wanted);pop=4;name='DeleteObject'
   else:
    args=[self.read(sp+4)]
    if ret!=0x40596A or args!=[self.raster_dc]:raise RuntimeError('original raster DC deletion')
    result=g.delete_dc(self.raster_dc);pop=4;name='DeleteDC'
   self.cleanup_calls.append({'name':name,'args':args,'return_va':hex(ret),'result':result});self._stub_return(result,pop);return
  if address==0x405869:
   # Actual original caller supplies the captured DIB and the real-lock mirror.
   args=[self.read(sp+4*i) for i in range(6)];self.conversion_calls.append({'source_va':hex(address),'args':args,
    'lock_hex':bytes(uc.mem_read(args[1],8)).hex(),'rect':list(struct.unpack('<4I',uc.mem_read(args[4],16))),
    'point':list(struct.unpack('<2I',uc.mem_read(args[5],8)))})
  if address==RETURN:uc.emu_stop();return
  if 0x4CB220<=address<0x4CB5D8:
   if address==0x4CB220:
    args=[self.read(sp+4),self.read(sp+8)]
    if uc.reg_read(UC_X86_REG_ECX)!=OBJECT or self.read(sp)!=0x4CD541 or args!=[(NODE&0xFFFF0000)|self.read(NODE+30,'H'),self.read(NODE+32,'H')]:raise RuntimeError('natural first text update exact source caller/origin')
    self.text_updates.append({'args':args,'return_va':hex(self.read(sp)),'receiver':OBJECT})
   self.visited.add(address);return
  if address in LIVE_CODE or address in RASTER_CODE or address in TEXT_CODE:self.visited.add(address);return
  if address==0x56CE80:return SchoolBoardOpeningEmulator._hook(self,uc,address,size,context)
  if address in BOARD_CODE or address in SCRIPT_CODE or address in (0x4D29E0,0x4CA1B0,0x4C99E0,0x4CD4D0,0x4C7770,0x4CBA60,0x4CBDB0,0x410310):return SchoolBoardOpeningEmulator._hook(self,uc,address,size,context)
  raise RuntimeError(f'live unsupported original instruction {address:#x}')

 def run_live_text(self,parent,helper):
  if self.uc.reg_read(UC_X86_REG_EIP)!=0xE300000 or self.live_loading:raise RuntimeError('live actual pending font required')
  self.bridge=LiveD3D8(helper);self.live_loading=False;result=None
  try:
   renderer=self.read(0x7A49FC);slot=renderer+0xB210;old=self.read(slot)
   if old!=0:raise RuntimeError('explicit empty original renderer device slot required')
   self.write(slot,self.bridge.device['pointer'])
   binding={'slot':slot,'before':old,'bound':self.bridge.device['pointer'],'origin':'actual live owned host device; declared platform input, not original renderer startup'}
   raster=self.run_font_raster(parent,keep_resources=True)
   self.native_old_bitmap=next(r['result'] for r in raster['font_api'] if r['name']=='SelectObject' and r['return_va']=='0x40541b')
   self.uc.mem_map(0xE310000,4096)
   cleanup_bindings=[]
   for at,value in ((0x5920A4,0xE310000),(0x5920C4,0xE310010),(0x592060,0xE310020)):
    cleanup_bindings.append({'slot':at,'before':self.read(at),'bound':value});self.write(at,value)
   self.uc.mem_map(MIRROR,MIRROR_BYTES)
   self.live_allowed=[(STACK,STACK+65536),(TEXTURE+0x28,TEXTURE+0x44),(TEXTURE+0x44,TEXTURE+0x46),
    (OBJECT+0x16,OBJECT+0x18),(OBJECT+0x18,OBJECT+0x24),(VM+0x1C,VM+0x2C),(VM+0x93E2,VM+0x93E3),(NODE+4,NODE+6),
    (0x765720,0x765724),(MIRROR,MIRROR+MIRROR_BYTES)]
   before=self.script_regions();retained=self.capture_scene_memory(self.live_allowed[1:]);self.account_before=self.read(0x765720)
   entry={'sp':self.uc.reg_read(UC_X86_REG_ESP),'ebp':self.uc.reg_read(UC_X86_REG_EBP),'return_va':self.read(self.uc.reg_read(UC_X86_REG_ESP))}
   font_frame=parent['pending_font']['frames']['font']
   if entry!={'sp':font_frame-0x2E0,'ebp':font_frame-0x1DC,'return_va':0x405779}:raise RuntimeError('source-derived natural texture frame chain')
   self.remote_reads=[];self.com_records=[];self.cleanup_calls=[];self.conversion_calls=[];self.text_updates=[];self.lock_before=self.lock_after=b''
   self.live_loading=True;self.board_loading=True;self.board_index=46;self.board_inputs={'overlay_origin':parent['inputs']['overlay_origin']};self.board_records=[]
   self.uc.emu_start(0x403BD0,RETURN,timeout=10_000_000,count=200000)
   if (self.uc.reg_read(UC_X86_REG_EIP),self.uc.reg_read(UC_X86_REG_ESP))!=(RETURN,STACK+0xFF04):raise RuntimeError('live natural root VM return')
   readback=self.bridge.readback(self.bridge.texture['pointer'])
   if bytes.fromhex(readback['hex'])!=self.lock_after or readback['pitch']!=self.lock_pitch:raise RuntimeError('natural uploaded pixels differ from actual texture')
   result={'binding':binding,'cleanup_import_bindings':cleanup_bindings,'before':before,'after':self.script_regions(),'raster':raster,'platform_hello':self.bridge.hello,
    'remote_reads':self.remote_reads,'COM_calls':self.com_records,'conversion_calls':self.conversion_calls,'GDI_cleanup_calls':self.cleanup_calls,'first_text_updates':self.text_updates,
    'lock':{'mirror':MIRROR,'host_bits':self.host_bits,'pitch':self.lock_pitch,'before_hex':self.lock_before.hex(),'after_hex':self.lock_after.hex()},
    'actual_readback':readback,'texture':self.bridge.texture,'presentation':self.board_records,'accounting_before':self.account_before,'accounting_after':self.read(0x765720),
    'natural_return':{'va':RETURN,'sp':self.uc.reg_read(UC_X86_REG_ESP),'eax':self.uc.reg_read(UC_X86_REG_EAX)},
    'original_texture_create_upload_executed':True,'text_record_completed':True,'text_handler_completed':True,'natural_VM_returned':True,
    'text_readiness_executed':False,'GPU_draw_or_present_executed':False,'original_renderer_startup_executed':False,'dialogue_playback_completed':False,
    'waves_executed':False,'world_update_loop_executed':False,'full_task_wrapper_executed':False,**self.verify_scene_memory(retained)}
  finally:
   self.live_loading=False;self.board_loading=False
   try:gdi=self.platform.close() if hasattr(self,'platform') else None
   finally:cleanup=self.bridge.close()
   if result is not None:result['remaining_GDI_cleanup']=gdi;result['COM_process_cleanup']=cleanup;result['process_exited']=self.bridge.process.poll()==0
  return result

def restored_case(index,parents):
 name,expected=CHECKPOINTS[index];raw=(ROOT/f'.venv-audit/formation-actual-checkpoint-{index}.pkl').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=expected:raise ValueError('live actual checkpoint identity')
 payload=pickle.loads(raw)
 if payload['source_sha']!=SOURCE_SHA256 or payload['evidence_kind']!='private_actual_cpu_after_full35_before_placement':raise ValueError('live checkpoint provenance')
 e=SchoolLiveTextEmulator();e.__dict__.update({k:v for k,v in payload['state'].items() if k!='uc' and not k.startswith('_audit_')})
 for at,data in payload['memory']:e.uc.mem_write(at,data)
 e.uc.context_restore(payload['cpu']);original=e.uc.emu_start
 def bounded(begin,end,timeout=0,count=0):
  if (begin,timeout,count)==(0x468A49,30_000_000,4_000_000):timeout=120_000_000
  return original(begin,end,timeout=timeout,count=count)
 e.uc.emu_start=bounded
 try:
  for fn,key,parent in zip((e.run_placement,e.run_deployment_tail,e.run_initialization_and_opening,e.run_entry_control,e.run_script_preflight,e.run_script_opening,e.run_board_opening),
   ('formation_placement','deployment_tail','scene_opening','entry_control','script_preflight','script_opening','board_opening'),parents):
   if fn()!=parent['cases'][index][key]:raise ValueError('live full parent mismatch')
   print('Parent '+name+'/'+key+': complete frozen equality',flush=True)
 finally:e.uc.emu_start=original
 text=e.run_text_preparation()
 if text!=read_text_parent()['cases'][index]['text_preparation']:raise ValueError('live complete text parent mismatch')
 return e,text,{'name':name,'provenance':{'checkpoint_sha256':expected,'complete_parent_stages':8,'complete_parent_stages_equal':True,'parent_text_sha256':TEXT_SHA,'upstream_rerun':False}}

def report():
 helper,build_info=build();parents=(parent_evidence(),read_deployment(),read_opening(),read_entry(),read_preflight(),read_script_opening(),read_parent());cases=[]
 for i in range(3):
  e,text,c=restored_case(i,parents);c['live_text']=e.run_live_text(text,helper);cases.append(c);print('Native '+c['name']+': real texture and natural text/VM return',flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'bridge_build':build_info,'cases':cases,'inherited_refusals':deepcopy(read_text_parent()['inherited_refusals']),**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('use new immutable path')
 out.write_text(report_text(report()),encoding='utf-8',newline='\n')

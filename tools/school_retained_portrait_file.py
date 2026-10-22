"""Original retained name conversion and actual read-only image-file handoff.

GPU and GDI cleanup responses are explicitly historical platform replay. All
game/CRT functions execute original source bytes. The first game allocation is
left unexecuted, and the probe closes its outstanding real file explicitly.
"""
import copy,ctypes as C,gzip,hashlib,json,struct,types
from collections import Counter
from functools import lru_cache
from ctypes import wintypes as W
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from tools import school_retained_name_raster as name
from tools import school_retained_name_verification as prior_proof
from tools import school_retained_portrait_file_catalog as catalog
from tools.school_retained_rendering import AddressSpace
from tools.school_character_name_catalog import TEXTURE,PATH,expected_complete
from tools.school_character_image_file import WindowsImageFile
from tools.school_font_raster_catalog import convert_surface,geometry
from tools.school_second_live_text_catalog import bands

ROOT=name.ROOT;base=name.base;need=name.need;sha=name.sha;word=name.word;canonical=name.canonical
IMAGE=0x4cde10;ALLOCATOR=0x428a40
IMPORTS={0x5920a4:('SelectObject',8),0x5920c4:('DeleteObject',4),0x592060:('DeleteDC',4),0x592214:('GetCurrentDirectoryA',8),0x5921ec:('CreateFileA',28),0x5921f0:('GetFileSize',8)}


@lru_cache(maxsize=2)
def boundary(branch,scene):
 report,_,provenance=catalog.contracts();c=next(c for c in report['cases'] if (c['name'],c['scene_capture'])==(branch,scene));accepted=json.loads(base.pinned(catalog.ACCEPTANCE,catalog.ACCEPTANCE_SHA));m={r['path']:r['sha256'] for r in accepted['artifact_manifest']};path=accepted['corpus_report'];names=json.loads(gzip.decompress(base.pinned(path,m[path])));reference=next(r for r in names['cases'] if r['role']==4);observed=[]
 def capture(u):
  rows=base.memory_rows(u);observed.append((tuple((a,bytes(u.mem_read(a,b-a+1))) for a,b,_ in u.mem_regions()),u.context_save()));return rows
 proxy=types.SimpleNamespace(**dict(vars(base),memory_rows=capture));verify=types.FunctionType(prior_proof.verify_case.__code__,dict(prior_proof.verify_case.__globals__,base=proxy),'observe_verified_name_raster_boundary');checked=verify(c,reference);need(len(observed)==1,'one fully independently verified name-raster state');memory,cpu=observed[0]
 return memory,cpu,dict(source=provenance,name=branch,scene_capture=scene,independent_parent=checked,pending_texture=c['pending_texture'],offscreen=c['offscreen'],parent_raster=c['raster'],parent_step=c['step'],parent_font_frames=c['parent_boundary']['pending_font']['frames'],final_memory=c['final_memory'],final_architectural_cpu=c['final_architectural_cpu'])


class Files(WindowsImageFile):
 def __init__(self):
  super().__init__();self.k.GetCurrentDirectoryA.argtypes=[W.DWORD,C.c_char_p];self.k.GetCurrentDirectoryA.restype=W.DWORD;self.k.GetHandleInformation.argtypes=[W.HANDLE,C.POINTER(W.DWORD)];self.k.GetHandleInformation.restype=W.BOOL
 def directory(self):
  b=C.create_string_buffer(260);n=int(self.k.GetCurrentDirectoryA(260,b));need(0<n<260,'actual bounded current directory');return n,b.raw[:n+1]
 def close_checked(self):
  handles=list(self.handles);r=super().close();checks=[]
  for h in handles:
   flags=W.DWORD();C.set_last_error(0);result=int(self.k.GetHandleInformation(h,C.byref(flags)));error=C.get_last_error();need(result==0 and error==6,'closed actual source file is invalid');checks.append(dict(handle=h,result=result,error=error))
  return dict(r,explicit_probe_cleanup=True,original_CloseHandle_executed=False,invalid_handle_checks=checks)


def mapped_texture():
 _,old,_=catalog.contracts();space=AddressSpace();space.next=0x68001000;creation=space.result('recorded_name',old['COM_calls'][0]['result']);lock=space.result('recorded_name',old['COM_calls'][2]['result']);return creation,lock,space.ledger()


class Guest(base.Guest):
 def __init__(self,restored):
  super().__init__(restored);self.parent=restored[2];self.old=catalog.contracts()[1];self.creation,self.lock,self.ledger=mapped_texture();self.texture=self.creation['texture'];self.graphics=word(self.read(0x7a49fc));self.device=word(self.read(self.graphics+0xb210));self.device_method=word(self.read(word(self.read(self.device))+80));self.methods={target:int(offset) for offset,target in self.texture['methods'].items()};self.gpu_count=self.cleanup_count=0;self.api_targets={word(self.read(slot)):(slot,*v) for slot,v in IMPORTS.items()};self.files=None
 def apply(self,maps,outputs):
  for at,n in maps:
   need(at%4096==0 and n%4096==0 and all(not(a<at+n and at<=b) for a,b,_ in self.u.mem_regions()),'fresh bounded platform response mapping');self.u.mem_map(at,n)
  for row in outputs:self.u.mem_write(row['pointer'],bytes.fromhex(row['hex']))
 def response(self,at):
  sp=self.cpu()['ESP'];ret=word(self.read(sp));outputs=[];maps=[];extra={}
  def put(p,b):outputs.append(dict(pointer=p,hex=b.hex()))
  if at==self.device_method or at in self.methods:
   slot=80 if at==self.device_method else self.methods[at];index=self.gpu_count;need(index<4 and slot==[80,56,64,68][index],'exact historical four-call texture order');n={80:8,56:3,64:5,68:2}[slot];args=[word(self.read(sp+4+4*i)) for i in range(n)];old=self.old['COM_calls'][index];need(ret==int(old['source_va'],16)+3,'original COM call return');result=copy.deepcopy(old['result']);kind='recorded_GPU'
   if slot==80:
    need(args==[self.device,128,32,1,0,25,1,TEXTURE+0x2c],'exact source CreateTexture dimensions/format/pool');result=copy.deepcopy(self.creation);t=self.texture
    for p in [t['pointer'],t['vtable'],*t['methods'].values()]:maps.append((p&~4095,4096))
    maps=list(dict.fromkeys(maps));put(t['pointer'],struct.pack('<I',t['vtable']))
    for offset,target in t['methods'].items():put(t['vtable']+int(offset),struct.pack('<I',target))
    put(args[-1],struct.pack('<I',t['pointer']))
   elif slot==56:
    need(args==[self.texture['pointer'],0,self.cpu()['EBP']-0x34],'source texture descriptor output');put(args[2],bytes.fromhex(result['hex']))
   elif slot==64:
    need(args[0:2]==[self.texture['pointer'],0] and args[3:]==[0,0x800],'source texture lock arguments');result=copy.deepcopy(self.lock);b=bytes.fromhex(result['hex']);need(len(b)==8192 and result['pitch']==256,'recorded complete 128x32 lock');start=result['bits']&~4095;maps.append((start,((result['bits']-start+len(b)+4095)&~4095)));put(result['bits'],b);put(args[2],struct.pack('<2I',result['pitch'],result['bits']))
   else:
    need(args==[self.texture['pointer'],0],'source texture unlock receiver/level');b=self.read(self.lock['bits'],8192);need(sha(b)==result['uploaded_sha256'],'source converter matches complete historical native upload');extra['uploaded_hex']=b.hex()
   self.gpu_count+=1;value=result['hr'];pop=n*4;extra.update(slot=slot,historical_call_index=index,historical_response=old['result'],result=result)
  else:
   need(at in self.api_targets,'only declared original platform target '+hex(at));slot,api,pop=self.api_targets[at];args=[word(self.read(sp+4+4*i)) for i in range(pop//4)];extra.update(import_slot=slot,name=api);o=self.parent['offscreen']
   if api in ('SelectObject','DeleteObject','DeleteDC'):
    index=self.cleanup_count;need(index<4,'bounded original GDI cleanup');old=self.old['GDI_cleanup_calls'][index];need(api==old['name'] and ret==int(old['return_va'],16),'exact original recorded cleanup caller');old_bitmap=next(a['result'] for a in self.parent['parent_step']['api_calls'] if a['name']=='SelectObject' and a['return_va']==0x40541b);expected=[[o['raster_dc'],old_bitmap],[o['bitmap']],[o['raster_dc']],[o['font']]][index];need(args==expected,'source-owned logical GDI cleanup roles');value=o['bitmap'] if index==0 else old['result'];kind='recorded_GDI_cleanup';self.cleanup_count+=1;extra.update(historical_call_index=index,historical_response=old,logical_object_roles_rebased=True)
   else:
    need(self.files is not None,'actual owned source-file service');kind='actual_read_only_file'
    if api=='GetCurrentDirectoryA':
     need(ret==0x42ac7a and args==[260,0x7a0ebc],'source current-directory caller');value,b=self.files.directory();put(args[1],b);extra['directory_hex']=b.hex()
    elif api=='CreateFileA':
     path=name.text(self,args[0]);need(ret==0x42ac9c and path==b'data\\adv\\bin\\sc004.bin','source natural portrait filename');value=self.files.open(args[1:]);extra.update(source_path_hex=path.hex(),native_absolute_read_only_path=str(catalog.INSTALLED/'DATA/ADV/BIN/SC004.BIN'),declared_relative_path_binding=True)
    else:
     need(api=='GetFileSize' and ret==0x42ad0d and args[1]==0,'source original file-size caller');value=self.files.size(args[0])
  row=dict(kind=kind,target=at,sp=sp,return_va=ret,args=args,pop=pop,value=value,new_mappings=[dict(pointer=p,bytes=n) for p,n in maps],memory_outputs=outputs,**extra);self.apply(maps,outputs);self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret);return row
 def execute_new(self,label,stop):
  before=self.cpu();counts=Counter();ih=hashlib.sha256();wh=hashlib.sha256();writes=0;calls=[];iat={slot:self.read(slot) for slot in IMPORTS};entry_maps=[]
  # Map only missing platform-entry pages. Existing bytes/IAT remain untouched;
  # these pages are never executed, and every call stops in the API hook.
  for at in [self.device_method,*self.api_targets]:
   if not any(a<=at<=b for a,b,_ in self.u.mem_regions()):p=at&~4095;self.u.mem_map(p,4096);entry_maps.append(dict(pointer=p,bytes=4096))
  def code(u,at,n,_):
   if at==stop:u.emu_stop();return
   if at==self.device_method or at in self.methods or at in self.api_targets:calls.append(self.response(at));return
   need(base.BASE<=at<0x592000 and self.read(at,n)==self.source[at-base.BASE:at-base.BASE+n],'original instruction/CRT identity '+hex(at));counts[at]+=1;ih.update(struct.pack('<I',at)+self.read(at,n))
  def write(u,access,at,n,value,_):
   nonlocal writes
   need(not base.BASE<=at<0x592000,'no original code writes');writes+=1;wh.update(struct.pack('<IIQ',at,n,value&0xffffffffffffffff))
  c=self.u.hook_add(UC_HOOK_CODE,code);w=self.u.hook_add(UC_HOOK_MEM_WRITE,write)
  try:self.u.ctl_remove_cache(before['EIP'],before['EIP']+1);self.u.emu_start(before['EIP'],0,count=2000000,timeout=120000000)
  finally:self.u.hook_del(c);self.u.hook_del(w)
  need(self.cpu()['EIP']==stop,'natural original continuation boundary');need(iat=={slot:self.read(slot) for slot in IMPORTS},'original IAT unchanged')
  return dict(label=label,before_cpu=before,cpu=self.cpu(),boundary=stop,instruction_counts=[dict(va=a,count=n) for a,n in sorted(counts.items())],instruction_sha256=ih.hexdigest(),writes=writes,write_sha256=wh.hexdigest(),api_calls=calls,entry_mappings=entry_maps,IAT_unchanged=True)


def frames(g,expected):
 p=g.cpu()['EBP'];rows=[]
 for label,ret in expected:
  need(word(g.read(p+4))==ret,'original '+label+' frame');rows.append(dict(label=label,bp=p,return_va=ret));p=word(g.read(p))
 return rows


def image_pending(g):
 sp=g.cpu()['ESP'];outer=g.parent['parent_font_frames'][1:];chain=frames(g,[('resource',0x4cc26d),*[(r['label'],r['return_va']) for r in outer]])
 return dict(va=IMAGE,sp=sp,receiver=g.cpu()['ECX'],args=[word(g.read(sp+4)),word(g.read(sp+8))],return_va=word(g.read(sp)),frames=chain,first_instruction_executed=False)


def run_case(branch,scene):
 restored=boundary(branch,scene);g=Guest(restored);need(g.cpu()['EIP']==0x403bd0,'verified original pending name texture');before=name.portrait.regions(g);account=word(g.read(0x765720));first=g.execute_new('continuous_original_name_texture_and_resource_path',IMAGE);after=name.portrait.regions(g);expected=expected_complete(dict(after=before,measured=g.parent['offscreen']['measured']),g.texture['pointer'],g.device,account);need(after==expected['after'] and word(g.read(0x765720))==expected['accounting_after'],'independent complete original name resource projection');pixels=g.read(g.lock['bits'],8192);model=bytes.fromhex(g.lock['hex']);cfg=geometry(g.parent['offscreen']['measured'])
 for band in bands(cfg):model=convert_surface(bytes.fromhex(g.parent['parent_raster']['hex']),cfg['raster_size'],band['rect'],model,g.lock['pitch'],band['point'])
 need(model==pixels,'independent every-pixel original name conversion');pending=image_pending(g);need((pending['receiver'],pending['args'],pending['return_va'])==(base.VM,[PATH,32],0x4cc0d2),'natural original image-loader call');g.files=Files();result=None
 try:
  second=g.execute_new('continuous_original_image_file_open_size_to_allocation',ALLOCATOR);sp=g.cpu()['ESP'];need(word(g.read(sp))==0x42ad54 and word(g.read(sp+4))==262168,'first unexecuted original allocation count/caller');chain=frames(g,[('file_loader',0x42ae47),('file_wrapper',0x4cde36),('image',0x4cc0d2),*[(r['label'],r['return_va']) for r in pending['frames']]])
  result=dict(name=branch,scene_capture=scene,parent_boundary=restored[2],before=before,after_name_texture=after,expected_name=expected,accounting_before=account,accounting_after=word(g.read(0x765720)),typed_projection=g.ledger,converted_texture_hex=pixels.hex(),converted_texture_sha256=sha(pixels),pending_image=pending,steps=[first,second],pending_allocation=dict(va=ALLOCATOR,sp=sp,args=[word(g.read(sp+4))],return_va=word(g.read(sp)),frames=chain,first_instruction_executed=False),actual_open_files_at_boundary=sorted(g.files.handles),final_memory=base.memory_rows(g.u),final_architectural_cpu=base.architectural_cpu(g.u))
 finally:cleanup=g.files.close_checked()
 result['file_cleanup']=cleanup;return result


def run():
 cases=[]
 for branch in ('initial','student9_waiting','fifth_class'):
  for scene in (76,77):
   c=run_case(branch,scene);cases.append(c);print(branch,scene,'source name texture/path -> actual file open/size -> original allocation boundary',flush=True)
 return dict(schema_version=1,platform_contract=catalog.contracts()[2],cases=cases,new_game_roots=0,game_function_substitutions=0,IAT_rebindings=0,recorded_GPU_and_GDI_cleanup_only=True,new_GPU=False,new_window=False,new_OS_input=False,actual_read_only_file_open_and_size=True,original_allocator_executed=False,original_ReadFile_executed=False,original_CloseHandle_executed=False,image_loader_completed=False,same_native_lifetime=False,R3_complete=False)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable continuation report required')
 r=run();out.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0));print('portrait file handoff report bytes',out.stat().st_size,flush=True)

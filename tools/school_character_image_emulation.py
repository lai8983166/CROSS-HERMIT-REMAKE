"""Real file/original container and DX prefix with three live prior textures."""
from tools.school_character_name_texture_emulation import *
from tools.school_character_image_catalog import (
 resource,source_rules,frames,expected_prefix as image_expected_prefix,HEAP,HEAP_BYTES,FILE_BUFFER,ARRAY,RECORD,FILE_API,FILE_IMPORTS)
from tools.school_character_image_file import WindowsImageFile

IMAGE_NATIVE=((0x4CDE10,0x4CDEC3),(0x42AE20,0x42AE6B),(0x42AC50,0x42ADCE),(0x416790,0x4167D2),(0x4167E0,0x416864),
 (0x41F090,0x41F0DC),(0x41F0E0,0x41F292),(0x41F4E0,0x41F59F),(0x41F340,0x41F47F),(0x41F830,0x41F887),
 (0x403620,0x4036C0),(0x41F930,0x41F9D5),(0x420990,0x4209C0),(0x4214F0,0x421538),(0x4209F0,0x420A38),
 (0x420B50,0x420B98),(0x404FB0,0x405129))
IMAGE_CODE=frozenset(a for lo,hi in IMAGE_NATIVE for a in range(lo,hi))

class SchoolCharacterImageEmulator(SchoolCharacterNameTextureEmulator):
 def __init__(self):
  self.image_loading=False;super().__init__()
 def _write_hook(self,uc,access,address,size,value,context):
  if not self.image_loading:return super()._write_hook(uc,access,address,size,value,context)
  if not any(a<=address and address+size<=b for a,b in self.image_allowed):raise RuntimeError(f'image finite write {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
 def _image_write(self,address,raw):
  self._write_hook(self.uc,0,address,len(raw),0,None);self.uc.mem_write(address,raw)
 def _file_api(self,address,sp):
  slot,(name,pop)=list(FILE_IMPORTS.items())[(address-FILE_API)//16];args=[self.read(sp+4+i*4) for i in range(pop//4)];ret=self.read(sp)
  if name=='GetCurrentDirectoryA':
   if args!=[260,0x7A0EBC] or ret!=0x42AC7A:raise RuntimeError('image original current-directory caller')
   raw=str((ROOT/'CROSS HERMIT/CROSS HERMIT').resolve()).encode('ascii');self._image_write(args[1],raw+b'\0');result=len(raw)
  elif name=='CreateFileA':
   if ret!=0x42AC9C or self.bounded_text(args[0]).decode('ascii')!=name_rules()['image_path']:raise RuntimeError('image exact original read-only path')
   result=self.files.open(args[1:])
  elif name=='GetFileSize':
   if args[1]!=0 or ret!=0x42AD0D:raise RuntimeError('image original size caller')
   result=self.files.size(args[0])
  elif name=='ReadFile':
   if (args[1],args[2],args[4],ret)!=(FILE_BUFFER,262168,0,0x42AD82):raise RuntimeError('image original full read input')
   raw=self.files.read(args[0],args[2]);self._image_write(args[1],raw);self._image_write(args[3],struct.pack('<I',len(raw)));result=1
   self.actual_file_sha=hashlib.sha256(raw).hexdigest()
  else:
   if ret!=0x42ADA5:raise RuntimeError('image original successful close caller')
   result=self.files.release(args[0])
  self.file_calls.append({'name':name,'slot':hex(slot),'args':args,'return_va':hex(ret),'result':result});self._stub_return(result,pop)
 def _hook(self,uc,address,size,context):
  if not self.image_loading:return super()._hook(uc,address,size,context)
  sp=uc.reg_read(UC_X86_REG_ESP);ret=self.read(sp)
  if FILE_API<=address<FILE_API+len(FILE_IMPORTS)*16 and (address-FILE_API)%16==0:return self._file_api(address,sp)
  if address==0x403BD0:
   f=frames(self.image_parent);pending={'va':address,'receiver':uc.reg_read(UC_X86_REG_ECX),'args':[self.read(sp+4),self.read(sp+8)],'return_va':ret,'sp':sp,'ebp':uc.reg_read(UC_X86_REG_EBP),'first_instruction_executed':False}
   expected={'va':address,'receiver':RECORD,'args':[self.bridge.device['pointer'],0],'return_va':0x4050B4,'sp':f['texture_sp'],'ebp':f['dx'],'first_instruction_executed':False}
   if pending!=expected:raise RuntimeError('image exact natural texture stack '+repr(pending))
   self.pending_image_texture=pending;uc.emu_stop();return
  if address==0x428A40:
   count=self.read(sp+4);expected=(FILE_BUFFER,262168,'file_buffer') if ret==0x42AD54 else (ARRAY,88,'texture_array') if ret==0x41F142 else None
   if expected is None or count!=expected[1] or any(a['pointer']==expected[0] for a in self.image_allocations):raise RuntimeError('image bounded declared allocation')
   self.image_allocations.append({'pointer':expected[0],'bytes':count,'kind':expected[2],'return_va':hex(ret),'freed':False});self._stub_return(expected[0],0);return
  if address==0x56D810:
   target,fmt,source=[self.read(sp+4+i*4) for i in range(3)]
   if (ret,target,fmt,source)!=(0x42ACB9,0x7A0EBC,0x592A18,self.read(frames(self.image_parent)['file_loader']+8)):raise RuntimeError('image exact diagnostic formatter')
   raw=self.bounded_text(source);self._image_write(target,raw+b'\0');self._stub_return(len(raw),0);return
  if address==0x56DDA0:
   args=[self.read(sp+4+i*4) for i in range(5)]
   if ret!=0x41F179 or args!=[RECORD,84,1,0x41F830,0x41F890]:raise RuntimeError('image exact vector primitive')
   self.vector_pending=True;uc.emu_stop();return
  if address==0x56CEC0:
   args=[self.read(sp+4+i*4) for i in range(3)]
   if (ret,args)!=(0x41F9BE,[RECORD+36,0,4]):raise RuntimeError('image exact constructor zero')
   self._image_write(args[0],bytes(4));self._stub_return(args[0],0);return
  if address in IMAGE_CODE:self.visited.add(address);self.image_visited.add(address);return
  return SchoolLiveTextEmulator._hook(self,uc,address,size,context)
 def run_image_prefix(self,parent):
  if self.uc.reg_read(UC_X86_REG_EIP)!=0x4CDE10 or not self.live_loading or self.bridge.closed:raise RuntimeError('actual live image entry required')
  self.image_parent=parent;self.image_renderer=self.read(0x7A49FC);self.image_table=self.image_renderer+0x844+32*8
  before=self.script_regions();expected=image_expected_prefix(before)
  if bytes(self.uc.mem_read(self.image_table,8))!=bytes(8):raise RuntimeError('captured empty resource32 slot required')
  self.uc.mem_map(HEAP,HEAP_BYTES);self.uc.mem_map(FILE_API,0x1000);bindings=[]
  for index,(slot,(name,pop)) in enumerate(FILE_IMPORTS.items()):
   bindings.append({'slot':slot,'before':self.read(slot),'bound':FILE_API+index*16,'name':name});self.write(slot,FILE_API+index*16)
  self.image_allowed=[(STACK,STACK+65536),(0,4),(FILE_BUFFER,FILE_BUFFER+262168),(ARRAY,ARRAY+88),(0x7A0EBC,0x7A0FC0),(self.image_table,self.image_table+8)]
  retained=self.capture_scene_memory(self.image_allowed[1:]);self.image_null_before=bytes(self.uc.mem_read(0,4))
  self.files=WindowsImageFile();self.file_calls=[];self.image_allocations=[];self.image_visited=set();self.vector_pending=False;self.pending_image_texture=None;self.image_loading=True;result=None
  try:
   self.uc.ctl_remove_cache(0x4CDE10,0x4CDE11);self.uc.emu_start(0x4CDE10,RETURN,timeout=5_000_000,count=200000)
   if not self.vector_pending:raise RuntimeError('image original vector not reached')
   cpu=self.uc.context_save();saved=bytes(self.uc.mem_read(STACK,65536));self.call(0x41F830,receiver=RECORD)
   self.uc.mem_write(STACK,saved);self.uc.context_restore(cpu);self._stub_return(0,20);self.vector_pending=False
   self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=5_000_000,count=200000)
   if self.pending_image_texture is None:raise RuntimeError('image natural texture entry not reached')
   record=bytes(self.uc.mem_read(RECORD,84));table=bytes(self.uc.mem_read(self.image_table,8))
   if self.script_regions()!=expected['after'] or record.hex()!=expected['record_hex'] or table.hex()!=expected['table_hex']:raise RuntimeError('image independent complete prefix')
   pixels=[self.bridge.readback(t['pointer']) for t in self.image_prior_textures]
   if pixels!=self.image_prior_pixels:raise RuntimeError('image all three real prior textures retained')
   result={'before':before,'after':self.script_regions(),'renderer':self.image_renderer,'table_address':self.image_table,'table_hex':table.hex(),'record_hex':record.hex(),
    'file_calls':self.file_calls,'actual_file_sha256':self.actual_file_sha,'import_bindings':bindings,'allocations':deepcopy(self.image_allocations),'pending_texture':self.pending_image_texture,
    'file_buffer_sha256':hashlib.sha256(bytes(self.uc.mem_read(FILE_BUFFER,262168))).hexdigest(),'array_hex':bytes(self.uc.mem_read(ARRAY,88)).hex(),'SEH_before_hex':self.image_null_before.hex(),'SEH_pending_hex':bytes(self.uc.mem_read(0,4)).hex(),'prior_actual_readbacks':pixels,'visited':sorted(self.image_visited),
    'working_directory':'declared original game directory; actual file open resolves fixed absolute source path','real_file_API_executed':True,'original_vector_constructor_executed':True,
    'image_texture_created':False,'image_loader_returned':False,'GPU_draw_or_present_executed':False,**self.verify_scene_memory(retained)}
  finally:
   self.image_loading=False;cleanup=self.files.close()
   if result is not None:result['file_cleanup']=cleanup
  return result
 def complete_second(self,first):
  result=super().complete_second(first);self.image_prior_textures=self.resource_textures+[result['name_texture']['texture']]
  self.image_prior_pixels=self.resource_pixels+[result['name_texture']['actual_readback']];result['image_prefix']=self.run_image_prefix(result['name_texture']);return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use immutable evidence path')
 path.write_text(report_text(report(ROOT/'.venv-audit'/f'{path.stem}-bridge.exe',SchoolCharacterImageEmulator)),encoding='utf-8',newline='\n')

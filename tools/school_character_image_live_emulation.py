"""Fourth real DX texture and natural original image-loader return."""
from tools.school_character_image_emulation import *
from tools.school_d3d8_image_bridge import ImageD3D8,build as build_image
from tools.school_character_image_catalog import IMAGE_MIRROR,expected_complete as image_expected_complete,expected_pixels

class SchoolCharacterImageLiveEmulator(SchoolCharacterImageEmulator):
 def __init__(self):
  self.image_uploading=False;super().__init__()
 def _hook(self,uc,address,size,context):
  if not self.image_uploading:return super()._hook(uc,address,size,context)
  sp=uc.reg_read(UC_X86_REG_ESP)
  if address==0x4CC0D2:
   self.image_return={'va':address,'sp':sp,'ebp':uc.reg_read(UC_X86_REG_EBP),'eax':uc.reg_read(UC_X86_REG_EAX)};uc.emu_stop();return
  if address==0x403910:
   if self.read(sp)!=0x4047D3 or uc.reg_read(UC_X86_REG_ECX)!=RECORD:raise RuntimeError('image original DX lock input')
   self.lock_output=self.read(sp+4);self.visited.add(address);return
  if address==0x56D4D0:
   args=[self.read(sp+4+i*4) for i in range(3)];row=len(self.image_rows)
   if row>=512 or (self.read(sp),args)!=(0x40483F,[IMAGE_MIRROR+row*self.lock_pitch,FILE_BUFFER+24+row*512,512]):raise RuntimeError('image exact original row copy')
   self._image_write(args[0],bytes(uc.mem_read(args[1],args[2])));self.image_rows.append({'row':row,'args':args,'return_va':'0x40483f'});self._stub_return(args[0],0);return
  if address==0x428AD0:
   if (self.read(sp),self.read(sp+4))!=(0x4CDEAD,FILE_BUFFER) or self.image_allocations[0]['freed']:raise RuntimeError('image owned file-buffer free')
   self.image_allocations[0]['freed']=True;self._stub_return(0,0);return
  if 0x4046F0<=address<0x40486C:self.visited.add(address);return
  if address==0x403BD0 or address in LIVE_CODE:return SchoolLiveTextEmulator._hook(self,uc,address,size,context)
  return SchoolCharacterImageEmulator._hook(self,uc,address,size,context)
 def complete_image(self,parent,prefix):
  if self.uc.reg_read(UC_X86_REG_EIP)!=0x403BD0 or self.bridge.closed or not self.live_loading:raise RuntimeError('actual live image texture entry required')
  self.image_parent=parent;self.live_texture_address=RECORD;self.live_texture_size=(256,512);self.live_mirror_address=IMAGE_MIRROR
  self.uc.mem_map(IMAGE_MIRROR,MIRROR_BYTES)
  self.image_allowed += [(IMAGE_MIRROR,IMAGE_MIRROR+MIRROR_BYTES),(VM+0x92C0,VM+0x92C1),(0x765720,0x765724)]
  retained=self.capture_scene_memory(self.image_allowed[1:]);self.image_uploading=True;self.image_loading=True
  self.remote_reads=[];self.com_records=[];self.lock_before=self.lock_after=b'';self.lock_bytes=0;self.image_rows=[];self.image_return=None
  account=self.read(0x765720);before=self.script_regions();result=None
  try:
   self.uc.ctl_remove_cache(0x403BD0,0x403BD1);self.uc.emu_start(0x403BD0,RETURN,timeout=10_000_000,count=300000)
   if self.image_return is None or len(self.image_rows)!=512:raise RuntimeError('original image loader did not return')
   texture=deepcopy(self.bridge.texture);pixels=self.bridge.readback(texture['pointer']);prior=[self.bridge.readback(t['pointer']) for t in self.image_prior_textures]
   expected=image_expected_complete(before,self.bridge.device['pointer'],texture['pointer']);record=bytes(self.uc.mem_read(RECORD,84))
   if self.script_regions()!=expected['after'] or record.hex()!=expected['record_hex'] or bytes(self.uc.mem_read(self.image_table,8)).hex()!=expected['table_hex']:raise RuntimeError('image independent complete return state')
   if pixels['hex']!=expected_pixels(self.lock_before,self.lock_pitch).hex() or pixels['hex']!=self.lock_after.hex() or prior!=self.image_prior_pixels:raise RuntimeError('image all four actual texture pixels')
   if bytes(self.uc.mem_read(0,4))!=self.image_null_before or not self.image_allocations[0]['freed'] or self.read(0x765720)!=account+262144:raise RuntimeError('image original SEH/free/accounting')
   result={'before':before,'after':self.script_regions(),'table_address':self.image_table,'table_hex':bytes(self.uc.mem_read(self.image_table,8)).hex(),'record_hex':record.hex(),
    'texture':texture,'actual_readback':pixels,'prior_actual_readbacks':prior,'rows':self.image_rows,'remote_reads':self.remote_reads,'COM_calls':self.com_records,
    'lock':{'mirror':IMAGE_MIRROR,'host_bits':self.host_bits,'pitch':self.lock_pitch,'before_hex':self.lock_before.hex(),'after_hex':self.lock_after.hex()},
    'allocations':deepcopy(self.image_allocations),'accounting_before':account,'accounting_after':self.read(0x765720),'natural_return':self.image_return,
    'file_buffer_sha256':hashlib.sha256(bytes(self.uc.mem_read(FILE_BUFFER,262168))).hexdigest(),'array_hex':bytes(self.uc.mem_read(ARRAY,88)).hex(),'SEH_after_hex':bytes(self.uc.mem_read(0,4)).hex(),'image_texture_created':True,'original_rows_uploaded':True,'image_loader_returned':True,
    'animation_executed':False,'GPU_draw_or_present_executed':False,'world_update_loop_executed':False,**self.verify_scene_memory(retained)}
  finally:self.image_uploading=False;self.image_loading=False
  return result
 def complete_second(self,first):
  result=super().complete_second(first);result['image_live']=self.complete_image(result['name_texture'],result['image_prefix']);return result

def report(helper_path):
 helper,identity=build_image(helper_path);parents=(parent_evidence(),read_deployment(),read_opening(),read_entry(),read_preflight(),read_script_opening(),read_parent());cases=[]
 for index in range(3):
  e,text,case=restored_case(index,parents,SchoolCharacterImageLiveEmulator)
  if hashlib.sha256(helper.read_bytes()).hexdigest()!=identity['helper_sha256']:raise ValueError('image fixed helper identity')
  case['provenance']['helper_sha256']=identity['helper_sha256'];first=e.run_live_text(text,helper,bridge_type=ImageD3D8,continuation=e.complete_second)
  case.update(first.pop('continuation'));case['first_live_text']=first;cases.append(case)
  print('Native '+case['name']+': four real textures, original sc004 loader returned',flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'bridge_build':identity,'cases':cases,**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use immutable evidence path')
 path.write_text(report_text(report(ROOT/'.venv-audit'/f'{path.stem}-bridge.exe')),encoding='utf-8',newline='\n')

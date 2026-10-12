"""Source-pinned Direct3D8 texture contract and isolated original entry probes."""
import argparse,hashlib,json,struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_ECX,UC_X86_REG_EAX
from tools.school_font_raster_catalog import ROOT,SOURCE,SOURCE_SHA256,BASE,native_fixture,TEXTURE_OFFSET,AUTHORITY,report_text

STACK=0x2000000;RETURN=0x3000000;OBJECT=0x12000000

def power_of_two(value):
 if type(value)is not int or not 1<=value<=16384:raise ValueError('positive signed WORD with terminating power-of-two result required')
 return 1<<(value-1).bit_length()

def source_catalog():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('texture source identity')
 expected={0x4136ED:('push','0xdc'),0x4136F2:('call','0x526c40'),0x4136FA:('mov','dword ptr [ecx + 0xb20c], eax'),
  0x413750:('mov','dword ptr [eax + 0xb1f8], 1'),0x41375D:('mov','dword ptr [ecx + 0xb1fc], 0x40'),
  0x413797:('mov','dword ptr [edx + 0xb1fc], 0x20'),0x4137C1:('mov','dword ptr [edx + 0xb1f8], 2'),
  0x4137CE:('mov','dword ptr [eax + 0xb1fc], 0x40'),0x4137F8:('mov','dword ptr [eax + 0xb1f8], 2'),0x413805:('mov','dword ptr [ecx + 0xb1fc], 0x20'),
  0x4139CD:('add','eax, 0xb210'),0x4139E8:('or','al, 4'),0x413A10:('call','dword ptr [eax + 0x3c]'),0x413C76:('call','dword ptr [ecx + 0x3c]'),
  0x403BA2:('movsx','ecx, word ptr [ebp - 0xc]'),0x403BA6:('movsx','edx, word ptr [ebp + 8]'),0x403BB4:('shl','ax, 1'),
  0x403BF0:('movsx','ecx, word ptr [eax + 0x38]'),0x403C06:('cmp','dword ptr [ecx + 0x34], 0'),
  0x403C2F:('call','0x403730'),0x403C3F:('call','0x403b70'),0x403C53:('call','0x403b70'),
  0x403C65:('push','1'),0x403C72:('push','1'),0x403C81:('mov','ecx, dword ptr [eax]'),0x403C87:('call','dword ptr [ecx + 0x50]'),
  0x403C98:('jge','0x403ca4'),0x403CBB:('call','dword ptr [eax + 0x38]'),0x403D2C:('mov','dword ptr [ecx + 0x28], edx')}
 md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
 for at,pair in expected.items():
  i=next(md.disasm(raw[at-BASE:at-BASE+16],at,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError(f'texture code differs at {at:x}')
  proof.append({'va':hex(at),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'code_inputs':proof,'sdk_version':220,
  'device_fallbacks':[[1,0x44],[1,0x24],[2,0x44],[2,0x24]],'renderer_factory_offset':0xB20C,'renderer_device_offset':0xB210,
  'CreateDevice_vtable_offset':0x3C,'CreateTexture_vtable_offset':0x50,'GetLevelDesc_vtable_offset':0x38,
  'texture_levels':1,'texture_pool':1,'font_texture_format':25,'scope':'isolated source contract, not natural native device initialization',**AUTHORITY}

def cpu():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('texture source identity')
 u=Uc(UC_ARCH_X86,UC_MODE_32)
 for a,n in ((BASE,(len(raw)+4095)&~4095),(STACK,65536),(RETURN,4096),(OBJECT,4096)):u.mem_map(a,n)
 u.mem_write(BASE,raw);return u

def run_dimension(value):
 power_of_two(value);u=cpu();sp=STACK+0xFF00;u.mem_write(sp,struct.pack('<2I',RETURN,value));u.reg_write(UC_X86_REG_ESP,sp)
 def code(uc,at,n,_):
  if at!=RETURN and not 0x403B70<=at<0x403BCA:raise RuntimeError('dimension original range')
 def write(uc,access,at,n,v,_):
  if not (STACK<=at and at+n<=STACK+65536):raise RuntimeError('dimension stack-only writes')
 u.hook_add(UC_HOOK_CODE,code);u.hook_add(UC_HOOK_MEM_WRITE,write);u.emu_start(0x403B70,RETURN,count=1000)
 if (u.reg_read(UC_X86_REG_EIP),u.reg_read(UC_X86_REG_ESP))!=(RETURN,sp+8):raise RuntimeError('dimension original return')
 return u.reg_read(UC_X86_REG_EAX)&65535

def run_null_device(record,usage_mode=0):
 if not isinstance(record,bytes) or len(record)!=0x48 or type(usage_mode)is not int or usage_mode not in (0,1):raise ValueError('texture bounded record/mode')
 if any(struct.unpack_from('<I',record,o)[0] for o in (0x28,0x2C,0x30)):raise ValueError('isolated texture must have no existing COM objects')
 width,height=struct.unpack_from('<2h',record,0x38);fmt=struct.unpack_from('<I',record,0x34)[0]
 if width and height and fmt:power_of_two(width);power_of_two(height)
 u=cpu();u.mem_write(OBJECT,record);sp=STACK+0xFF00;u.mem_write(sp,struct.pack('<3I',RETURN,0,usage_mode));u.reg_write(UC_X86_REG_ESP,sp);u.reg_write(UC_X86_REG_ECX,OBJECT);pending=[]
 def code(uc,at,n,_):
  if at==0x403C81:
   if uc.reg_read(UC_X86_REG_EAX)!=0:raise RuntimeError('expected source null device')
   args=list(struct.unpack('<7I',uc.mem_read(uc.reg_read(UC_X86_REG_ESP),28)))
   pending.append({'va':hex(at),'device':0,'prepared_args':args,'device_this_not_yet_pushed':True,'null_dereference_executed':False,'COM_call_executed':False});uc.emu_stop();return
  if at==RETURN or at in (0x56CE80,0x56CE82) or 0x403BD0<=at<0x403D44 or 0x403730<=at<0x4037EF or 0x403B70<=at<0x403BCA:return
  raise RuntimeError(f'isolated texture unsupported source {at:x}')
 def write(uc,access,at,n,v,_):
  if STACK<=at and at+n<=STACK+65536:return
  if at==OBJECT+0x28 and n==4:return
  raise RuntimeError('isolated texture finite writes')
 u.hook_add(UC_HOOK_CODE,code);u.hook_add(UC_HOOK_MEM_WRITE,write);u.emu_start(0x403BD0,RETURN,count=10000)
 after=bytes(u.mem_read(OBJECT,len(record)))
 if after!=record:raise RuntimeError('null-device/precondition record retention')
 returned=u.reg_read(UC_X86_REG_EIP)==RETURN
 if returned and (u.reg_read(UC_X86_REG_ESP)!=sp+12 or u.reg_read(UC_X86_REG_EAX)!=1):raise RuntimeError('texture invalid geometry original return')
 if not returned and not pending:raise RuntimeError('isolated texture did not reach bounded endpoint')
 return {'before_hex':record.hex(),'after_hex':after.hex(),'pending':pending,'original_returned':returned,'return_value':1 if returned else None,'GPU_executed':False,'native_VM_continuation_executed':False}

def report():
 values=[1,2,3,24,174,255,256,257,1024,16384];cases=[]
 for c in native_fixture()['cases']:
  raw=bytes.fromhex(c['font_raster']['after'][3]['hex'])[TEXTURE_OFFSET:TEXTURE_OFFSET+0x48]
  cases.append({'name':c['name'],'texture':run_null_device(raw)})
 invalid=[]
 for width,height,fmt in ((0,24,25),(174,0,25),(174,24,0)):
  raw=bytearray(0x48);struct.pack_into('<I2h',raw,0x34,fmt,width,height);invalid.append(run_null_device(bytes(raw)))
 return {'schema_version':1,'source':source_catalog(),'dimensions':[{'input':v,'original':run_dimension(v),'independent':power_of_two(v)} for v in values],'cases':cases,'invalid_geometry':invalid,**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('use new immutable path')
 out.write_text(report_text(report()),encoding='utf-8',newline='\n')

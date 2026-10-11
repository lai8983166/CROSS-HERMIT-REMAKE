"""Original405A80 CPU conversion, isolated from the pending GPU continuation."""
import argparse,hashlib,json,struct
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_ECX
from tools.school_font_raster_catalog import ROOT,SOURCE,SOURCE_SHA256,BASE,report_text,AUTHORITY,validate_surface,native_fixture

STACK=0x2000000;RETURN=0x3000000;SRC=0x11000000;DST=0x11200000;META=0x11400000

def run_conversion(raw,size,rect,dest,pitch,target):
 validate_surface(raw,size,rect,dest,pitch,target);image=SOURCE.read_bytes()
 if hashlib.sha256(image).hexdigest()!=SOURCE_SHA256:raise ValueError('pixel source identity')
 uc=Uc(UC_ARCH_X86,UC_MODE_32)
 for a,n in ((BASE,(len(image)+4095)&~4095),(STACK,65536),(RETURN,4096),(SRC,0x100000),(DST,0x100000),(META,4096)):uc.mem_map(a,n)
 uc.mem_write(BASE,image);uc.mem_write(SRC,raw);uc.mem_write(DST,dest)
 uc.mem_write(META,struct.pack('<2I',pitch,DST)+struct.pack('<4I',*rect)+struct.pack('<2I',*target))
 sp=STACK+0xFF00;uc.mem_write(sp,struct.pack('<7I',RETURN,SRC,META,size[0],size[1],META+8,META+24))
 uc.reg_write(UC_X86_REG_ESP,sp);uc.reg_write(UC_X86_REG_ECX,META+64)
 writes=[]
 def code(u,address,n,_):
  if address!=RETURN and not 0x405A80<=address<0x405BB4:raise RuntimeError('isolated pixel source range')
 def guard(u,access,address,n,value,_):
  if STACK<=address and address+n<=STACK+65536:return
  if address<DST or address+n>DST+len(dest):raise RuntimeError('isolated pixel finite destination')
  row,column=divmod(address-DST,pitch)
  if n!=2 or not target[1]<=row<target[1]+rect[3] or not 2*target[0]<=column<2*(target[0]+rect[2]):raise RuntimeError('isolated pixel finite rectangle')
  writes.append([address-DST,n])
 uc.hook_add(UC_HOOK_CODE,code);uc.hook_add(UC_HOOK_MEM_WRITE,guard)
 uc.emu_start(0x405A80,RETURN,timeout=10_000_000,count=10_000_000)
 if (uc.reg_read(UC_X86_REG_EIP),uc.reg_read(UC_X86_REG_ESP))!=(RETURN,sp+28):raise RuntimeError('isolated pixel original stdcall return')
 if bytes(uc.mem_read(SRC,len(raw)))!=raw or bytes(uc.mem_read(META,32))!=struct.pack('<2I',pitch,DST)+struct.pack('<4I',*rect)+struct.pack('<2I',*target):raise RuntimeError('isolated pixel input retention')
 out=bytes(uc.mem_read(DST,len(dest)))
 return {'scope':'declared_isolated_CPU_memory_surface_not_native_GPU_continuation','source_sha256':hashlib.sha256(raw).hexdigest(),
  'source_size':size,'rect':rect,'destination_point':target,'destination_pitch':pitch,'before_hex':dest.hex(),'after_hex':out.hex(),
  'output_sha256':hashlib.sha256(out).hexdigest(),'write_count':len(writes),'writes_sha256':hashlib.sha256(json.dumps(writes,separators=(',',':')).encode()).hexdigest(),
  'source_and_metadata_retained':True,'original_function_returned':True,'GPU_executed':False}

def report():
 cases=[]
 for c in native_fixture()['cases']:
  r=c['font_raster']['raster'];raw=bytes.fromhex(r['hex']);w,h=r['size'];pitch=2*w+12;dest=bytes([0xA5])*(pitch*(h+2))
  p=run_conversion(raw,[w,h],[0,0,w,h],dest,pitch,[0,1]);cases.append({'name':c['name'],'conversion':p})
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use new immutable evidence path')
 path.write_text(report_text(report()),encoding='utf-8',newline='\n')

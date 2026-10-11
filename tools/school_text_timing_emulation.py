"""Declared isolated original text fade/cadence/readiness, no fake GPU result."""
import argparse,hashlib,struct
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_ECX,UC_X86_REG_EAX
from tools.school_text_timing_catalog import ROOT,SOURCE,SOURCE_SHA256,BASE,BYTES,STRIDE,encode_records
from tools.school_font_raster_catalog import report_text,AUTHORITY

STACK=0x2000000;RETURN=0x3000000;OBJECT=0x12000000

def run_timing(records,updates,origin=None):
 raw=encode_records(records)
 if type(updates)is not int or not 1<=updates<=256:raise ValueError('isolated timing bounded updates')
 origin=[715,691] if origin is None else origin
 if not isinstance(origin,list) or len(origin)!=2 or any(type(v)is not int or not 0<=v<=65535 for v in origin):raise ValueError('isolated timing origin')
 image=SOURCE.read_bytes()
 if hashlib.sha256(image).hexdigest()!=SOURCE_SHA256:raise ValueError('timing source identity')
 u=Uc(UC_ARCH_X86,UC_MODE_32)
 for a,n in ((BASE,(len(image)+4095)&~4095),(STACK,65536),(RETURN,4096),(OBJECT,4096)):u.mem_map(a,n)
 u.mem_write(BASE,image);u.mem_write(OBJECT,raw);draws=[]
 def hook(uc,address,n,_):
  if address==0x4CBF00:
   sp=uc.reg_read(UC_X86_REG_ESP);ret=struct.unpack('<I',uc.mem_read(sp,4))[0];args=list(struct.unpack('<9I',uc.mem_read(sp+4,36)))
   if ret!=0x4CB4B2 or uc.reg_read(UC_X86_REG_ECX)!=0x7D7C28 or args[0] not in [OBJECT+i*STRIDE+0x28 for i in range(len(records))] or args[2]>65535 or args[1]!=origin[0] or args[3]!=1 or args[5:]!=[255,255,255,55]:raise RuntimeError('isolated exact terminal text draw')
   draws.append({'va':hex(address),'receiver':0x7D7C28,'args':args,'return_va':hex(ret),'return_value':0})
   uc.reg_write(UC_X86_REG_EAX,0);uc.reg_write(UC_X86_REG_ESP,sp+40);uc.reg_write(UC_X86_REG_EIP,ret);return
  if address==RETURN or address in (0x56CE80,0x56CE82) or 0x4CB220<=address<0x4CB5DA or 0x4CB5F0<=address<0x4CB698:return
  raise RuntimeError(f'isolated unsupported text instruction {address:#x}')
 owned=[(OBJECT+i*STRIDE+o,2) for i in range(len(records)) for o in (24,26,30,34)]
 def guard(uc,access,address,n,value,_):
  if STACK<=address and address+n<=STACK+65536:return
  if not any(a<=address and address+n<=a+s for a,s in owned):raise RuntimeError('isolated text finite record guard')
 u.hook_add(UC_HOOK_CODE,hook);u.hook_add(UC_HOOK_MEM_WRITE,guard)
 def call(va,args):
  sp=STACK+0xFF00;u.mem_write(sp,struct.pack('<'+'I'*(len(args)+1),RETURN,*args));u.reg_write(UC_X86_REG_ESP,sp);u.reg_write(UC_X86_REG_ECX,OBJECT)
  u.emu_start(va,RETURN,timeout=1_000_000,count=100000)
  if (u.reg_read(UC_X86_REG_EIP),u.reg_read(UC_X86_REG_ESP))!=(RETURN,sp+4+4*len(args)):raise RuntimeError('isolated original text return')
  return u.reg_read(UC_X86_REG_EAX)&255
 initial=bool(call(0x4CB5F0,[]));timeline=[]
 for index in range(updates):
  draws.clear();call(0x4CB220,origin);after=bytes(u.mem_read(OBJECT,BYTES));ready=bool(call(0x4CB5F0,[]))
  timeline.append({'update':index+1,'after_hex':after.hex(),'draws':draws.copy(),'readiness':ready})
 return {'scope':'declared_isolated_text_records_not_pending_GPU_or_VM_continuation','records':records,'origin':origin,'object_pointer':OBJECT,
  'before_hex':raw.hex(),'initial_readiness':initial,'updates':timeline,'original_update_and_predicate_executed':True,
  'GPU_executed':False,'native_VM_continuation_executed':False,'native_dialogue_completed':False}

def record(mode=2,fade=0,limit=24,interval=0,delay=12,following=0,height=24):
 return {'mode':mode,'fade_count':fade,'fade_limit':limit,'interval_count':interval,'interval_limit':delay,'following_ready':following,'height':height}

def cases():
 return [('single_source',[record()],26),('two_source_zero_intermediate_interval',[record(delay=0),record()],26),
  ('two_overlapping_intervals',[record(),record()],38),('single_short_fade',[record(limit=1,delay=0)],3),
  ('signed_counter_wrap',[record(mode=3,fade=32767,limit=32767,interval=32767,delay=32767)],2),
  ('mode4_stays_pending',[record(mode=4)],2),('word_counter_rollover',[record(mode=3,fade=65535,limit=24,interval=65535)],2),
  ('ten_source_lines',[record(delay=0) for _ in range(9)]+[record()],26)]

def report():return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':[{'name':name,'timing':run_timing(records,count)} for name,records,count in cases()],**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use new immutable path')
 path.write_text(report_text(report()),encoding='utf-8',newline='\n')

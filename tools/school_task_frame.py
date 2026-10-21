"""Source-backed input request reset and complete task frames on R2 resources."""
import ctypes as C,hashlib,json,struct
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_retained_rendering import ROOT,SOURCE,SOURCE_SHA256,BASE,RetainedStartup,REGISTERS
from tools.school_retained_render_pipeline import Pipeline,VM

INPUT=0x1080180
TACT=0xe000000
IME_SLOT=0x5920ec

def source_contract():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('original source identity')
 md=Cs(CS_ARCH_X86,CS_MODE_32)
 checks={0x425e07:('movsx','ecx, byte ptr [eax + 0x630]'),0x425e34:('call','0x425e60'),0x425e3f:('mov','byte ptr [ecx + 0x630], 0'),
  0x425e87:('call','0x425c70'),0x425c94:('call','0x56cd4a'),0x56cd4a:('jmp','dword ptr [0x5920ec]'),
  0x425ef0:('movsx','ecx, byte ptr [eax + 0x630]'),0x425ef9:('je','0x425f1f'),0x425f12:('call','0x424f80'),0x425f34:('mov','byte ptr [ecx + 0x630], 0xff'),
  0x49e5a4:('call','0x425de0'),0x49e5cd:('call','0x40db90'),0x49e5de:('call','0x40dc80'),0x49e60f:('call','0x4217c0'),0x454d8b:('call','0x4ce8f0')}
 rows=[]
 for at,want in checks.items():
  i=next(md.disasm(raw[at-BASE:at-BASE+16],at))
  if (i.mnemonic,i.op_str)!=want:raise ValueError('source input/frame operand '+hex(at))
  rows.append(dict(va=at,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
 descriptor=struct.unpack_from('<5I',raw,0x5fd6d0-BASE);name=raw[descriptor[3]:].split(b'\0',1)[0]
 symbol_rva=struct.unpack_from('<I',raw,descriptor[0]+8*4)[0];symbol=raw[symbol_rva+2:].split(b'\0',1)[0]
 if name!=b'IMM32.dll' or symbol!=b'ImmGetOpenStatus' or descriptor[4]+BASE+8*4!=IME_SLOT:raise ValueError('original IMM import identity')
 return dict(source_sha256=SOURCE_SHA256,original_instructions=rows,import_slot=IME_SLOT,dll=name.decode(),symbol=symbol.decode(),input_object=INPUT,request_flag_offset=0x630,assertion='A prior IME request is pending; this is not an input index',full_outer_thread_scheduler_executed=False)

class ActualIME:
 def __init__(self):
  self.dll=C.WinDLL('imm32',use_last_error=True);self.fn=self.dll.ImmGetOpenStatus;self.fn.argtypes=[C.c_void_p];self.fn.restype=C.c_int;self.trace=[]
  kernel=C.WinDLL('kernel32',use_last_error=True);kernel.GetModuleFileNameW.argtypes=[C.c_void_p,C.c_wchar_p,C.c_uint];kernel.GetModuleFileNameW.restype=C.c_uint
  path=C.create_unicode_buffer(32768)
  if not kernel.GetModuleFileNameW(self.dll._handle,path,len(path)):raise RuntimeError('actual loaded IMM32 module path')
  p=Path(path.value);self.identity=dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),host_pointer_bytes=C.sizeof(C.c_void_p),guest_pointer_bytes=4)
 def query(self,context):
  if type(context)is not int or context!=0:raise ValueError('only captured null IME context is authorized/owned')
  C.set_last_error(0);result=int(self.fn(None));row=dict(name='ImmGetOpenStatus',args=[context],result=result,last_error=C.get_last_error(),actual_OS_observed=True)
  self.trace.append(row);return row

class TaskFrameEmulator(RetainedStartup):
 def bind_ime(self,ime):
  self.ime=ime;self.ime_target=self.read(IME_SLOT);self.map_missing(self.ime_target,1);self.uc.mem_write(self.ime_target,b'\xc3')
 def continuation_code(self,uc,at,size):
  if hasattr(self,'ime_target') and at==self.ime_target:
   sp=self.read_register('ESP');args=[self.read(sp+4)]
   if self.read(sp)!=0x425c99 or args!=[self.read(INPUT+8)]:raise ValueError('actual IME original exact caller/input context')
   observed=self.ime.query(args[0]);self.vm_apis.append(dict(va=at,key='system',sp=sp,return_va=self.read(sp),import_slot=IME_SLOT,call=observed))
   return self.platform_return(sp,observed['result'],4)
  return super().continuation_code(uc,at,size)

class TaskFramePipeline(Pipeline):
 def frame(self,index):
  e=self.e;flag_before=bytes(e.uc.mem_read(INPUT+0x630,1))[0]
  reset=self.root('original_input_request_reset_'+str(index),0x425de0,INPUT)
  flag_reset=bytes(e.uc.mem_read(INPUT+0x630,1))[0]
  if flag_reset:raise ValueError('original reset must consume IME request')
  self.reset();task=self.root('complete_original_task_'+str(index),0x454cf0,TACT)
  if task['cpu']['EAX']!=0 or task['pending'] or not any(x['va']==0x4ce8f0 for x in task['instruction_counts']):raise ValueError('original complete task/VM execution and natural return')
  return dict(index=index,PC=e.read(VM+28),wait=struct.unpack('<H',e.uc.mem_read(VM+32,2))[0],flag_before=flag_before,flag_after_original_reset=flag_reset,flag_after_task=bytes(e.uc.mem_read(INPUT+0x630,1))[0],task_phase=bytes(e.uc.mem_read(TACT+0x44,1))[0],original_instructions=sum(x['count'] for x in task['instruction_counts']),reset_APIs=len(reset['api_calls']))

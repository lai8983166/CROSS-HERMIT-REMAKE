"""Independent raw-source keyboard queries and native dialogue observation checks."""
import copy,gzip,json,struct,types
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from unicorn.x86_const import UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_EFLAGS
from tools import school_native_scene_verification as base
ROOT=base.ROOT;SOURCE=base.SOURCE;need=base.need;sha=base.sha;word=base.word
INPUT_RANGES=((0x411290,0x411cf0),(0x4128f0,0x412a70),(0x4cce20,0x4cd060))
CHECKS={0x49e78a:('call','0x412a30'),0x412a50:('call','0x411290'),0x412a58:('call','0x411df0'),0x411310:('call','dword ptr [ecx + 0x24]'),0x4113dd:('add','ecx, 0x480'),0x411444:('mov','byte ptr [edx + 0x480], cl'),0x41149b:('mov','byte ptr [eax + 0x580], dl'),0x4114d5:('mov','byte ptr [eax + 0x780], dl'),0x412935:('mov','cl, byte ptr [eax + edx + 0x480]'),0x4ccff2:('call','0x4128f0'),0x4cd028:('call','0x4ccb30')}

class OriginalKeyQuery:
 def __init__(self):
  raw=SOURCE.read_bytes();need(sha(raw)==base.SOURCE_SHA256,'query original source identity');self.u=Uc(UC_ARCH_X86,UC_MODE_32);self.u.mem_map(0x400000,(len(raw)+4095)&~4095);self.u.mem_write(0x400000,raw)
  for at in (0x31000000,0x32000000,0x33000000):self.u.mem_map(at,65536)
 def query(self,body,key=0x39,mode=0):
  need(len(body)==0xa00 and type(key)is int and 0<=key<=0xffffffff and type(mode)is int and 0<=mode<=0xffffffff,'query full object and uint32 ABI');u=self.u;u.mem_write(0x31000000,body);u.mem_write(0x3200ff00,struct.pack('<3I',0x33000000,key,mode));u.reg_write(UC_X86_REG_ESP,0x3200ff00);u.reg_write(UC_X86_REG_ECX,0x31000000);u.reg_write(UC_X86_REG_EFLAGS,0x202);u.emu_start(0x4128f0,0x33000000,count=1000)
  need(u.reg_read(UC_X86_REG_ESP)==0x3200ff0c and bytes(u.mem_read(0x31000000,0xa00))==body,'original key query read-only object/ret8 ABI');return u.reg_read(UC_X86_REG_EAX)

def source_contract(s):
 raw=SOURCE.read_bytes();need(sha(raw)==base.SOURCE_SHA256==s['source_sha256'],'input source identity');need(s['ranges']==[dict(pointer=a,bytes=b-a,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in INPUT_RANGES],'complete input source ranges');need(len(s['instructions'])==len(CHECKS) and {r['va'] for r in s['instructions']}==set(CHECKS),'all exact input graph operands');md=Cs(CS_ARCH_X86,CS_MODE_32)
 for r in s['instructions']:
  i=next(md.disasm(raw[r['va']-0x400000:r['va']-0x400000+16],r['va']));need((i.mnemonic,i.op_str)==CHECKS[r['va']] and r==dict(va=i.address,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str),'raw source input operand')
 fields=dict(input_owner_offset=0x10b8,scan_code=0x39,current_offset=0x480,previous_offset=0x380,press_offset=0x580,release_offset=0x780,query=0x4128f0,confirmation_wait=0x4cce20,confirmation_opcode=51,human_physical_input_claimed=False,host_input_object_writes=False)
 need(all(s[k]==v and type(s[k])is type(v) for k,v in fields.items()),'exact input contract and honest scope');return s['ranges']

def verify_report(report,require_input=False,action=None):
 need(report['human_physical_input_claimed'] is False and report['R3_complete'] is False,'no physical/R3 completion overclaim');ranges=source_contract(report['input_source_contract']);p=report['case']['probe'];need(p is not None,'native probe exists');samples=p['samples'];need(1<=len(samples)<=12000,'extended bounded native sampling')
 for phase in ('source_before','source_after'):need(p[phase]['input_code']==ranges,'live original input source identity')
 # The frozen validator owns the bootstrap/scene contracts only. Its unchanged
 # no-physical-input claim is retained; OS injection is separately checked below.
 projection=copy.deepcopy(report)
 for phase in ('source_before','source_after'):projection['case']['probe'][phase].pop('input_code')
 code=base.verify_report.__code__;code=code.replace(co_consts=tuple(12000 if type(x)is int and x==1600 else x for x in code.co_consts));native=types.FunctionType(code,base.verify_report.__globals__)(projection)
 game=report['case']['lifecycle']['ready']['game']['pointer'];query=OriginalKeyQuery();results=[]
 for r in samples:
  x=r['input'];need(x['game']==game and x['pointer']==game+0x10b8 and len(bytes.fromhex(x['hex']))==0xa00 and len(bytes.fromhex(x['mouse_hex']))==8,'complete actual input owner/window');need(type(r['wall_time_ns'])is int and r['wall_time_ns']>0,'actual wall timestamp')
  if r.get('ordinary_scene_loop_wait'):
   body=bytes.fromhex(x['hex']);expected=int(bool(body[0x4b9]&0x80));actual=query.query(body);need(actual==expected,'raw original space query');results.append(dict(index=r['index'],result=actual))
 need(all(a['wall_time_ns']<=b['wall_time_ns'] for a,b in zip(samples,samples[1:])),'ordered wall samples')
 b=p['dialogue_boundary'];start,ready=b['no_input_start'],b['ready_index'];need(type(start)is int and type(ready)is int and 0<=start<ready<len(samples),'actual no-input confirmation boundary')
 pc=b['wait_PC'];script=bytes.fromhex(p['script_file']['loaded_memory_hex']);need(script[452+pc-4:452+pc]==struct.pack('<HH',51,4),'PC follows actual original confirmation opcode')
 for r in samples[start:ready+1]:
  v=bytes.fromhex(r['VM_hex']);body=bytes.fromhex(r['input']['hex']);need(word(v,28)==pc and struct.unpack_from('<HH',v,32)==(1,51) and not body[0x4b9]&0x80 and not word(bytes.fromhex(r['input']['mouse_hex']),4)&7,'stable native no-input wait and zero confirmation input')
 need(samples[ready]['elapsed']-samples[start]['elapsed']>=.99,'at least one real second of no-input confirmation wait')
 press,release,advance=(b[k] for k in ('press_index','release_index','advanced_index'))
 if require_input:
  need(isinstance(action,dict) and action.get('method')=='computer-use sky.press_key' and action.get('key')=='space' and action.get('input_returned') is True,'successful actual computer-use action receipt required')
  w=action.get('window',{});need(w.get('id')==report['case']['lifecycle']['ready']['window']['hwnd'] and w.get('app','').startswith('process:') and __import__('pathlib').Path(w['app'][8:]).resolve()==__import__('pathlib').Path(p['process_image']).resolve(),'input receipt belongs to actual owned window/image')
  need(type(action.get('start_ms'))is int and type(action.get('end_ms'))is int and action['start_ms']<=action['end_ms'],'bounded actual action timestamps')
  need(report['case']['system_input_expected'] is True and report['input_method']=='computer-use sky.press_key space via OS; no host object writes','actual OS input mode')
  need(all(type(x)is int for x in (press,release,advance)) and ready<press<release<len(samples) and press<=advance<len(samples),'actual input/release/advancing indexes')
  need(action['start_ms']-100<=samples[press]['wall_time_ns']/1000000<=action['end_ms']+500,'observed key press temporally belongs to successful action')
  need(bytes.fromhex(samples[press]['input']['hex'])[0x4b9]&0x80 and not bytes.fromhex(samples[release]['input']['hex'])[0x4b9]&0x80 and word(bytes.fromhex(samples[advance]['VM_hex']),28)!=pc,'observed OS key press/release and subsequent script transition')
 else:need(report['case']['system_input_expected'] is False and report['input_method']=='no input observation' and press is release is advance is None,'no-input evidence cannot claim input transition')
 return dict(schema_version=1,native_bootstrap_and_scene=native,input_source_checked=True,original_space_query_replays=len(results),query_results=results,no_input_wait=dict(PC=pc,first_index=start,ready_index=ready,seconds=samples[ready]['elapsed']-samples[start]['elapsed']),system_input_transition_verified=require_input,R3_complete=False)


# Explicit platform-boundary experiment: run original post-GetDeviceState bytes.
# This is not a native input capture and never writes the real game object.
def keyboard_update(before):
 need(len(before)==0xa00,'complete declared keyboard state');raw=SOURCE.read_bytes();need(sha(raw)==base.SOURCE_SHA256,'keyboard source identity');u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x400000,(len(raw)+4095)&~4095);u.mem_write(0x400000,raw)
 for at in (0x31000000,0x32000000):u.mem_map(at,65536)
 u.mem_write(0x31000000,before);bp=0x3200f000;u.mem_write(bp-4,struct.pack('<I',0x31000000))
 from unicorn.x86_const import UC_X86_REG_EBP
 u.reg_write(UC_X86_REG_EBP,bp);u.reg_write(UC_X86_REG_ESP,bp-0x70);u.reg_write(UC_X86_REG_EFLAGS,0x202);u.emu_start(0x4113d5,0x4116a4,count=100000)
 need(u.reg_read(UC_X86_REG_EBP)==bp and u.reg_read(UC_X86_REG_ESP)==bp-0x70,'original input-transform stack balance');return bytes(u.mem_read(0x31000000,0xa00))

def predict_keyboard(before):
 need(len(before)==0xa00,'complete keyboard model input');after=bytearray(before);old=before[0x480:0x580];new=bytes(x&128 for x in before[12:268]);pressed=bytes((a^b)&b for a,b in zip(old,new));released=bytes((a^b)&a for a,b in zip(old,new));repeat=pressed;count=word(before,0x888);phase=word(before,0x88c)
 if old==new and any(new):
  delay=word(before,0x884 if phase else 0x880)
  if delay<=count:phase=1;count=0;repeat=bytes(a|b for a,b in zip(repeat,new))
  count=(count+1)&0xffffffff
 else:phase=0;count=0
 for at,value in ((0x380,old),(0x480,new),(0x580,pressed),(0x680,repeat),(0x780,released)):after[at:at+256]=value
 struct.pack_into('<II',after,0x888,count,phase);return bytes(after)

def keyboard_experiment():
 rows=[]
 for label,prior,device,phase,count,first,interval in (
  ('first_press',0,255,0,0,3,2),('low_bits_ignored',0,127,0,0,3,2),('hold_before_first',128,128,0,2,3,2),('first_repeat_at_threshold',128,128,0,3,3,2),('hold_before_repeat',128,128,1,1,3,2),('repeat_at_threshold',128,128,1,2,3,2),('release',128,0,1,1,3,2),('idle_resets',0,0,1,5,3,2),('counter_wrap',128,128,1,0xffffffff,3,0xffffffff)):
  before=bytearray([0xa5]*0xa00);before[12:268]=bytes(256);before[0x480:0x580]=bytes(256);before[12+57]=device;before[0x480+57]=prior;struct.pack_into('<4I',before,0x880,first,interval,count,phase);before=bytes(before);expected=predict_keyboard(before);actual=keyboard_update(before);need(actual==expected,'complete original keyboard transform '+label);rows.append(dict(label=label,before_hex=before.hex(),after_hex=actual.hex(),independent_full_object_equal=True))
 return dict(schema_version=1,source_sha256=base.SOURCE_SHA256,source_interval=[0x4113d5,0x4116a4],platform_boundary='declared GetDeviceState buffer in emulator; no live OS event or game object writes',cases=rows,system_input_transition_verified=False)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report');p.add_argument('--out',required=True);p.add_argument('--require-input',action='store_true');p.add_argument('--action');p.add_argument('--keyboard-source',action='store_true');a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof required')
 if a.keyboard_source:
  if a.report or a.action or a.require_input:p.error('keyboard experiment is a declared platform boundary')
  r=keyboard_experiment()
 else:
  if not a.report:p.error('native report required')
  if a.require_input and not a.action:p.error('successful OS action receipt required')
  action=json.loads((ROOT/a.action).read_text(encoding='utf8')) if a.action else None
  r=verify_report(json.loads(gzip.decompress((ROOT/a.report).read_bytes())),a.require_input,action)
 out.write_text(json.dumps(r,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('source or native wait checked; OS transition',r['system_input_transition_verified'])

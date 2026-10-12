"""Source-derived original text/confirmation wait sequencing, not live input."""
import argparse,hashlib,json,struct
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_second_live_text_catalog import ROOT,SOURCE,SOURCE_SHA256,BASE,VM,OBJECT_OFFSET,NODE_OFFSET,REGIONS,memory_regions,AUTHORITY,report_text
from tools.school_text_preparation_catalog import script_layout
from tools.school_text_timing_catalog import expected_update,BYTES

COMMAND_TABLE=0x4D03CF;WAIT_INDEX=0x4D06AB;WAIT_TABLE=0x4D066F
TASK=0x10000000
HOLD_UPDATES=14

@lru_cache(maxsize=1)
def source_catalog():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('dialogue wait original image identity')
 script,layout=script_layout();commands=[];md=Cs(CS_ARCH_X86,CS_MODE_32)
 for offset,expected in ((696,(50,4)),(700,(51,4)),(704,(30,20))):
  op,size=struct.unpack_from('<2H',script,offset)
  if (op,size)!=expected:raise ValueError('selected original wait order')
  entry=struct.unpack_from('<I',raw,COMMAND_TABLE-BASE+(op-5)*4)[0]
  call=next(i for i in md.disasm(raw[entry-BASE:entry-BASE+40],entry) if i.mnemonic=='call')
  row={'offset':offset,'PC':offset-layout['code_span'][0],'opcode':op,'size':size,'dispatch_entry':hex(entry),'handler':call.op_str,'return_va':hex(call.address+call.size)}
  if op in (50,51):
   selector=raw[WAIT_INDEX-BASE+op-12];target=struct.unpack_from('<I',raw,WAIT_TABLE-BASE+selector*4)[0]
   row['wait_selector']=selector;row['wait_dispatch_entry']=hex(target)
  commands.append(row)
 if [(r['handler'],r.get('wait_dispatch_entry')) for r in commands]!=[('0x4c5260','0x4d0153'),('0x4c4210','0x4d0181'),('0x4c61c0',None)]:raise ValueError('original dispatcher table differs')
 pairs={0x4CEA7A:('sub','ecx, 5'),0x4CEA90:('jmp','dword ptr [edx*4 + 0x4d03cf]'),0x4CFF94:('sub','eax, 0xc'),
  0x4CFFAC:('mov','cl, byte ptr [edx + 0x4d06ab]'),0x4CFFB2:('jmp','dword ptr [ecx*4 + 0x4d066f]'),
  0x4D0160:('call','0x4cd350'),0x4D018D:('call','0x4cce20'),0x4CD3B2:('call','0x4cb5f0'),
  0x4CD3FD:('call','0x4d5ec0'),0x4CD42D:('call','0x4128f0'),0x4CD483:('call','0x4cb6a0'),
  0x4CD49F:('call','0x41e500'),0x4CCFF2:('call','0x4128f0'),0x4CD028:('call','0x4ccb30'),
  0x4CCFCA:('call','0x4d29e0'),0x4D01B5:('mov','word ptr [eax + edx + 0x20], 0')}
 proof=[]
 for at,pair in pairs.items():
  i=next(md.disasm(raw[at-BASE:at-BASE+16],at,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError('original wait instruction differs '+hex(at))
  proof.append({'va':hex(at),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'script':layout,'commands':commands,'code_inputs':proof,
  'readiness_objects':10,'mouse_result_words':4,'space_key':57,'keyboard_mode':0,'confirmation_arrow_delay':5,
  'scope':'Bounded original VM wait sequence with retained real textures; declared input, terminal drawing, no GPU/world/live input.',**AUTHORITY}

def regions(mem):return [{'pointer':a,'bytes':n,'hex':mem[a].hex()} for a,n in REGIONS]
def readiness(raw):
 if not isinstance(raw,bytes) or len(raw)!=BYTES:raise ValueError('bounded text readiness object')
 count=struct.unpack_from('<H',raw,22)[0]
 if count>10:raise ValueError('bounded text readiness count')
 return not any(2<=struct.unpack_from('<H',raw,i*0x110+24)[0]<=4 for i in range(count))

def validate_events(events):
 if not isinstance(events,dict) or set(events)!={'mouse_buttons','space_key'} or any(type(v)is not int for v in events.values()) or events['mouse_buttons'] not in (0,1) or events['space_key']!=0:raise ValueError('bounded declared mouse event/no-keyboard input')

def advance(before,events):
 validate_events(events);source_catalog();mem=memory_regions(before);vm=mem[VM];counters=mem[0x7A4E18]
 def word(o):return struct.unpack_from('<H',vm,o)[0]
 def store(o,v):struct.pack_into('<H',vm,o,v)
 pc=struct.unpack_from('<I',vm,28)[0];wait=word(32);op=word(34);predicates=[];arrow=[];input_calls=[]
 if vm[4:6]!=b'\x01\x01' or vm[0x92E0] or vm[0x92E1] or word(OBJECT_OFFSET+22)!=2 or word(NODE_OFFSET)!=1 or word(NODE_OFFSET+2)!=2:raise ValueError('unsupported actual two-line wait parent')
 for j in range(10):
  if j!=7 and word(0x430+j*0xAB8+22):raise ValueError('additional active text objects unsupported')
 if (pc,wait) in ((244,0),(248,0)):
  opcode=50 if pc==244 else 51;store(34,opcode);store(36,4);store(32,1)
  struct.pack_into('<I',vm,28,pc+4);struct.pack_into('<2I',counters,0,(struct.unpack_from('<I',counters)[0]+1)&0xFFFFFFFF,0)
  if opcode==51:store(48,0);store(50,0)
 elif (pc,wait,op) in ((248,1,50),(252,1,51)):
  struct.pack_into('<2I',counters,0,0,(struct.unpack_from('<I',counters,4)[0]+1)&0xFFFFFFFF)
  if op==50:
   for j in range(10):predicates.append({'receiver':VM+0x430+j*0xAB8,'return_value':int(readiness(bytes(vm[0x430+j*0xAB8:0x430+(j+1)*0xAB8])))})
   if events['mouse_buttons']:raise ValueError('text-skip input outside this bounded natural-wait scope')
   ready=all(p['return_value']==1 for p in predicates)
   if ready:store(32,0)
   input_calls=['mouse','keyboard']
  else:
   if word(48)>6 or word(50)>3:raise ValueError('unsupported original arrow state')
   previous=word(48);store(48,previous+1)
   if previous>5:store(50,(word(50)+1)&3);store(48,0)
   phase=word(50);arrow=[{'va':'0x4d29e0','receiver':0x7E1110,'args':[20,0,1,54,word(52),word(54),424+phase*18,0,18,24,100,100,255,128,128,128],'return_va':'0x4ccfcf','return_value':0}]
   input_calls=['keyboard','mouse_buttons']
   if events['mouse_buttons']:store(32,0)
 else:raise ValueError('unsupported original PC/wait/opcode state')
 origin=[word(NODE_OFFSET+30),word(NODE_OFFSET+32)];update=expected_update(bytes(vm[OBJECT_OFFSET:OBJECT_OFFSET+BYTES]),origin,VM+OBJECT_OFFSET)
 vm[OBJECT_OFFSET:OBJECT_OFFSET+BYTES]=bytes.fromhex(update['after_hex']);store(NODE_OFFSET+4,word(NODE_OFFSET+2))
 return {'after':regions(mem),'text_draws':update['draws'],'arrow_draws':arrow,'predicates':predicates,'input_call_order':input_calls,
  'state':{'PC':struct.unpack_from('<I',vm,28)[0],'wait':word(32),'opcode':word(34),'arrow_count':word(48),'arrow_phase':word(50),
   'records':[{k:word(OBJECT_OFFSET+j*0x110+o) for k,o in (('mode',24),('fade',26),('interval',30),('following_ready',34))} for j in range(2)]}}

def expected_sequence(before,hold=HOLD_UPDATES):
 if type(hold)is not int or not 1<=hold<=32:raise ValueError('bounded confirmation hold updates')
 current=before;steps=[]
 for index in range(80):
  e=advance(current,{'mouse_buttons':0,'space_key':0});steps.append(e);current=e['after']
  if e['state']['PC']==248 and not e['state']['wait']:break
 else:raise ValueError('natural text wait failed bounded completion')
 released=index;steps.append(advance(current,{'mouse_buttons':0,'space_key':0}));current=steps[-1]['after']
 for index in range(hold):
  e=advance(current,{'mouse_buttons':0,'space_key':0});steps.append(e);current=e['after']
  if e['state']['PC']!=252 or e['state']['wait']!=1:raise ValueError('no-input confirmation unexpectedly released')
 return {'steps':steps,'text_wait_release_update':released,'confirmation_started_update':released+1,'held_confirmation_updates':hold,'after':current}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--rules',action='store_true');a=p.parse_args()
 if a.rules:print(report_text(source_catalog()))

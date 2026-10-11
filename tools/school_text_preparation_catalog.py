"""Independent first text preparation and original Big5 opening catalog."""
import argparse, hashlib, json, struct
from functools import lru_cache
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools.school_board_opening_catalog import source_catalog as board_catalog
from tools.school_script_opening_catalog import (
 ROOT, SOURCE, SOURCE_SHA256, BASE, VM, WORK, TACT, TASK, CONTROL, REGIONS,
 memory_regions, script_layout, presentation_records, trace_bytes, AUTHORITY, report_text)

STACK=0x2000000
NODE_OFFSET=0x6F60+7*0xE0
OBJECT_OFFSET=0x430+7*0xAB8
EVIDENCE=ROOT/'analysis/school-text-preparation-v1-20261012.json'
EVIDENCE_SHA256='fca8be507e3fa52273cf14db51f325c2fa70395e31b4a8b855a664112e50856a'

def decode_opening(script,layout):
 if not isinstance(script,bytes) or not isinstance(layout,dict):raise ValueError('text source types')
 code_start,code_end=layout['code_span'];sub_start,sub_end=layout['selected_span']
 if not 0<=sub_start<code_start<code_end<sub_end<=len(script):raise ValueError('text source bounds')
 count=struct.unpack_from('<I',script,code_end)[0]
 if count!=10 or code_end+4+count*4>sub_end:raise ValueError('text table count')
 entries=[];previous=code_end+4+count*4
 for index in range(count):
  packed=struct.unpack_from('<I',script,code_end+4+index*4)[0];span=packed>>20;at=code_end+(packed&0xFFFFF)
  if span<2 or span>255 or span%2 or at<previous or at+span>sub_end:raise ValueError('text entry span')
  raw=script[at:at+span]
  if raw[-2:]!=b'\0\0' or 0 in raw[:-2]:raise ValueError('text entry null padding')
  try:text=raw[:-2].decode('cp950')
  except UnicodeDecodeError as error:raise ValueError('text Big5 encoding') from error
  entries.append({'index':index,'offset':at,'span_bytes':span,'hex':raw[:-2].hex(),'text':text});previous=at+span
 sequence=[];at=code_start
 while at<code_end:
  op,n=struct.unpack_from('<2H',script,at)
  if n<4 or n%2 or at+n>code_end:raise ValueError('text opcode span')
  if op==17:
   if n!=6:raise ValueError('text opcode size')
   index=struct.unpack_from('<H',script,at+4)[0]
   if index>=count:raise ValueError('text opcode index')
   sequence.append({'offset':at,'text_index':index})
  at+=n
 if [r['text_index'] for r in sequence]!=list(range(10)):raise ValueError('text opening instruction order')
 return entries,sequence

def split_original(raw):
 if not isinstance(raw,bytes) or len(raw)>254 or 0 in raw or len(raw)%2:raise ValueError('text split bounded pairs')
 lines=[bytearray()];at=0
 while at<len(raw):
  if raw[at]==0x5C:
   if raw[at+1]!=ord('n') or len(lines)>=10:raise ValueError('text unsupported split separator')
   lines.append(bytearray())
  else:lines[-1].extend(raw[at:at+2])
  at+=2
 return [bytes(v) for v in lines]

@lru_cache(maxsize=1)
def source_catalog():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('text source identity')
 expected={0x4CE8F3:('sub','esp, 0x70'),0x4C4B83:('sub','esp, 0xa74'),0x4CABD3:('sub','esp, 0x150'),
  0x4C4E2E:('mov','byte ptr [ecx + 0x1cc], al'),0x4C4E47:('mov','word ptr [edx + ecx + 0x34], ax'),
  0x4C4E5F:('mov','word ptr [edx + ecx + 0x36], ax'),0x4C4E86:('mov','dword ptr [eax + edx + 0x38], ecx'),
  0x4C4BC7:('call','0x4c2120'),0x4C216C:('and','edx, 0xfffff'),
  0x4C4C1B:('imul','ecx, ecx, 0xff'),0x4C4C21:('lea','edx, [ebp + ecx - 0xa04]'),
  0x4C4C33:('mov','dword ptr [ebp + eax*4 - 0xa2c], edx'),0x4C4C4A:('call','0x4cd5b0'),
  0x4CD618:('je','0x4cd61c'),0x4CD64D:('add','cx, 2'),0x4CD686:('mov','ecx, dword ptr [ebp + 8]'),
  0x4CD68C:('mov','byte ptr [eax], dl'),0x4CD6B5:('mov','byte ptr [eax], dl'),
  0x4CD672:('mov','word ptr [ebp - 0x14], 1'),0x4CD6ED:('mov','ax, word ptr [ebp - 8]'),
  0x4C4CCB:('call','0x4cb080'),0x4C4CFF:('call','0x4cabd0'),
  0x4CAC1C:('mov','word ptr [edx + ecx + 0x18], 2'),0x4CAC35:('mov','word ptr [edx + ecx + 0x1a], 0'),
  0x4CAC56:('mov','word ptr [ecx + edx + 0x1c], ax'),0x4CAC6D:('mov','word ptr [ecx + eax + 0x1e], 0'),
  0x4CAC8A:('mov','word ptr [ecx + eax + 0x20], dx'),0x4CACA1:('mov','word ptr [edx + ecx + 0x24], 0x16'),
  0x4CACBA:('mov','word ptr [edx + ecx + 0x22], 0'),0x4CACFE:('movsx','ecx, word ptr [ebp - 0xc]'),
  0x4CAD03:('call','dword ptr [0x5920a0]')}
 md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
 for va,pair in expected.items():
  i=next(md.disasm(raw[va-BASE:va-BASE+16],va,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError(f'text source instruction {va:#x}: {i.mnemonic} {i.op_str}')
  proof.append({'va':hex(va),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 script,layout=script_layout();entries,sequence=decode_opening(script,layout)
 face_at=0x5BF62C;end=raw.index(0,face_at-BASE);face=raw[face_at-BASE:end]
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'code_inputs':proof,'script':layout,
  'entries':entries,'text_sequence':sequence,'face':{'va':hex(face_at),'hex':face.hex(),'decoded_cp932':face.decode('cp932')},
  'stack_allocations':{'vm':112,'text':2676,'font':336},
  'first_font_arguments':[0,0,0,0,400,0,0,0,1,5,0,0,0,face_at],
  'scope':'Original activation and first text prefix to unexecuted font API. Source ten-text preview is read-only and separate from native font/layout/playback.',**AUTHORITY}

def stable_board_records(origin):
 rules=board_catalog();cfg=rules['configuration']['words'];x,y=cfg[1:3];table=int(rules['frame_pieces']['va'],16)
 def call(va,recv,args,ret):return {'va':hex(va),'receiver':recv,'args':args,'return_va':hex(ret),'return_value':0}
 records=presentation_records(origin);start=1+7*3;records[start:start+3]=[]
 draws=[call(0x4CBDB0,VM,[x+r[0],y+r[1],(table&0xFFFF0000)|255,0xFFFFFFFF,66,*r[2:],20,0],0x4CA6FC) for r in rules['frame_pieces']['rows']]
 draws.append(call(0x410310,TASK+0x1058,[x+cfg[14],y+cfg[15],cfg[16],cfg[17],0xFFFF0043,0xCC223438,1],0x4CA319))
 records[start:start]=draws;return records

def expected_preparation(inputs,before):
 rules=source_catalog();board=board_catalog();script,layout=script_layout()
 if not isinstance(inputs,dict) or set(inputs)!={'script_pointer','overlay_origin','completed_updates','driver','font_api'}:raise ValueError('text input shape')
 pointer=inputs['script_pointer'];origin=inputs['overlay_origin']
 if type(pointer)!=int or not 0xE000000<=pointer<=0xF000000-len(script) or type(inputs['completed_updates'])!=int or inputs['completed_updates']!=1 or inputs['driver']!='natural_text_activation_then_original_vm_to_font_entry' or type(inputs['font_api'])!=int or inputs['font_api']!=0xE300000:raise ValueError('text unsupported driver')
 if not isinstance(origin,list) or len(origin)!=2 or any(type(v)!=int or not 0<=v<=65535 for v in origin):raise ValueError('text overlay types')
 mem=memory_regions(before);vm=mem[VM];task=mem[TACT];control=mem[CONTROL];counter=mem[0x7A4E18];node=NODE_OFFSET;obj=OBJECT_OFFSET
 def get(o,fmt='H'):return struct.unpack_from('<'+fmt,vm,o)[0]
 def put(o,v,fmt='H'):struct.pack_into('<'+fmt,vm,o,v)
 if vm[4:6]!=b'\x01\x01' or vm[0x92E0] or vm[0x92E1] or (get(0x1C,'I'),get(0x20),get(0x22),get(0x24),get(node),get(node+2),get(node+34),get(obj+22))!=(224,0,43,8,1,2,1,0):raise ValueError('text actual board VM state')
 if get(0x10,'I')!=pointer+layout['code_span'][0] or get(0x18,'I')!=pointer+948 or struct.unpack_from('<I',task,0x64)[0]!=pointer or control[12]!=7 or struct.unpack_from('<I',task,0x38)[0]!=5 or task[0x171] or task[0x43]!=1:raise ValueError('text parent binding')
 if origin!=[struct.unpack('<H',mem[TASK+o])[0] for o in (0x196C,0x1970)]:raise ValueError('text overlay binding')
 if any(get(0x6F60+i*0xE0) for i in range(10) if i!=7) or get(0x9248) or any(vm[0x228+i*0x1A] for i in range(20)) or any(vm[0x1CF+i*0x12] for i in range(5)):raise ValueError('text unsupported active presentation')
 if get(obj)!=24 or get(obj+6)!=12 or vm[obj+4] or vm[obj+10] or vm[obj+20] or get(obj+12) or get(obj+16):raise ValueError('text unsupported dimensions/font selection')
 cfg=board['configuration']['words'];put(0x9250,4,'I');vm[0x1CC]=7;put(0x34,cfg[9]);put(0x36,cfg[10]);put(0x38,VM+node,'I');put(0x1C,232,'I');put(0x20,0);put(node+4,2)
 activated={'pc':232,'wait':0,'target':7,'origin':cfg[9:11],'layer_pointer':VM+node}
 vm[0x93E2]=0;put(0x22,17);put(0x24,6);struct.pack_into('<2I',counter,0,2,0)
 for o,v in ((24,2),(26,0),(28,24),(30,0),(32,12),(34,0),(36,22)):put(obj+o,v)
 alloc=rules['stack_allocations'];vm_frame=STACK+0xFF00-4;text_frame=vm_frame-alloc['vm']-32;font_frame=text_frame-alloc['text']-28;font_sp=font_frame-alloc['font']-12-56-4
 array=text_frame-0xA2C;line=text_frame-0xA04;first=rules['entries'][0];parts=split_original(bytes.fromhex(first['hex']))
 if len(parts)!=1:raise ValueError('text unsupported first line count')
 records=stable_board_records(origin)
 return {'after':[{'pointer':a,'bytes':n,'hex':mem[a].hex()} for a,n in REGIONS],'activated':activated,
  'first_text':{'index':0,'pointer':pointer+first['offset'],'hex':first['hex'],'decoded_big5':first['text']},
  'split':{'count':1,'source_pointer':pointer+first['offset'],'array_pointer':array,'lines':[{'pointer':line,'hex':parts[0].hex()}]},
  'calls':[{'va':'0x4c4dc0','receiver':VM,'args':[0,pointer+676,0],'return_va':'0x4cef42'},
   {'va':'0x4c4b80','receiver':VM,'args':[0,pointer+684,0],'return_va':'0x4cec2b'},
   {'va':'0x4c2120','receiver':VM,'args':[pointer+948,0],'return_va':'0x4c4bcc'},
   {'va':'0x4cabd0','receiver':VM+obj,'args':[line,((VM+obj)&0xFFFF0000)|12],'return_va':'0x4c4d04'}],
  'presentation_calls':54,'presentation_sha256':hashlib.sha256(trace_bytes(records)).hexdigest(),'presentation':records,
  'pending_font':{'api':'CreateFontA','va':'0xe300000','import_slot':'0x5920a0','args':rules['first_font_arguments'],'face_hex':rules['face']['hex'],
   'return_va':'0x4cad09','root_return_va':'0x3000000','frames':{'vm':vm_frame,'text':text_frame,'font':font_frame,'sp':font_sp},
   'natural_stack_verified':True,'first_instruction_executed':False}}

@lru_cache(maxsize=1)
def native_fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('text evidence identity')
 return json.loads(raw)

def dialogue_catalog():
 rules=source_catalog();entries=rules['entries'];pages=[{'text_index':r['text_index'],'text':entries[r['text_index']]['text']} for r in rules['text_sequence']]
 return {'schema_version':1,'adventure_id':5,'scene_id':5,'source_script_sha256':rules['script']['source_script_sha256'],
  'encoding':'Big5','mode':'read_only_opening_preview','pages':pages}

def export():
 rules=source_catalog();data=native_fixture()
 evidence={'schema_version':1,'native_report':EVIDENCE.relative_to(ROOT).as_posix(),'native_report_sha256':EVIDENCE_SHA256,
  'cases':data['cases'],'inherited_refusals':data['inherited_refusals'],'runtime_fixture':False}
 for name,value in (('rules',rules),('evidence',evidence)):
  (ROOT/f'prototype/data/school_text_preparation_{name}.json').write_text(report_text(value),encoding='utf-8',newline='\n')
 (ROOT/'prototype/data/school_opening_dialogue.json').write_text(report_text(dialogue_catalog()),encoding='utf-8',newline='\n')

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--export',action='store_true');a=p.parse_args()
 if a.export:export()

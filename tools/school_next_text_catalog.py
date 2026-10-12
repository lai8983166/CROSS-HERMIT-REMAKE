"""Independent source rules for the natural consecutive second text prefix."""
import argparse, hashlib, json, struct
from functools import lru_cache
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools.school_text_preparation_catalog import (
 ROOT,SOURCE,SOURCE_SHA256,BASE,VM,OBJECT_OFFSET,NODE_OFFSET,REGIONS,memory_regions,
 script_layout,split_original,source_catalog as text_catalog,AUTHORITY,report_text)
from tools.school_live_text_catalog import expected as first_expected

STACK=0x2000000;RETURN=0x3000000
EVIDENCE=ROOT/'analysis/school-next-text-v4-20261012.json'
# Filled only after real native capture, never used to generate expected bytes.
EVIDENCE_SHA256='47e76776fc4eaddf701e99242bccd0968029093ce2faf6056cf3492f0614f69a'

@lru_cache(maxsize=1)
def source_catalog():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('next source image identity')
 rules=text_catalog();script,layout=script_layout();start=layout['code_span'][0]
 commands=[]
 for offset in (684,690):
  op,size,index=struct.unpack_from('<3H',script,offset)
  if (op,size,index)!=(17,6,len(commands)):raise ValueError('next consecutive source command')
  commands.append({'offset':offset,'pc':offset-start,'opcode':op,'advance':size,'text_index':index})
 pairs={0x4CE99E:('mov','cx, word ptr [eax + edx + 0x20]'),
  0x4CE9DD:('mov','word ptr [edx + ecx + 0x22], ax'),0x4CE9FB:('mov','word ptr [edx + ecx + 0x24], ax'),
  0x4CEA45:('mov','dword ptr [0x7a4e18], edx'),0x4CEA4B:('mov','dword ptr [0x7a4e1c], 0'),
  0x4CABF8:('mov','cx, word ptr [eax + 0x16]'),0x4CAC13:('imul','ecx, ecx, 0x110'),
  0x4CB610:('mov','cx, word ptr [eax + 0x16]'),0x4CB663:('cmp','dword ptr [ebp - 0x14], 2'),
  0x4CB669:('cmp','dword ptr [ebp - 0x14], 4'),0x4CB68B:('mov','al, 1'),0x4CB68F:('xor','al, al')}
 md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
 for at,pair in pairs.items():
  ins=next(md.disasm(raw[at-BASE:at-BASE+16],at,count=1))
  if (ins.mnemonic,ins.op_str)!=pair:raise ValueError(f'next source instruction differs {at:x}')
  proof.append({'va':hex(at),'hex':ins.bytes.hex(),'mnemonic':ins.mnemonic,'operands':ins.op_str})
 parts=split_original(bytes.fromhex(rules['entries'][1]['hex']))
 if len(parts)!=1:raise ValueError('next supported second line count')
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'code_inputs':proof,
  'inherited_text_code_inputs':rules['code_inputs'],'script':layout,'commands':commands,'second_text':rules['entries'][1],
  'stack_allocations':rules['stack_allocations'],'font_arguments':rules['first_font_arguments'],'font_face':rules['face'],
  'row_stride':0x110,'initial_row_fields':{'24':2,'26':0,'28':24,'30':0,'32':12,'34':0,'36':22},
  'scope':'Native next VM prefix; declared separate original readiness observation. Second font/texture and natural fade remain pending.',**AUTHORITY}

def expected_next(inputs,before):
 rules=source_catalog()
 if not isinstance(inputs,dict) or set(inputs)!={'script_pointer','driver','font_api'}:raise ValueError('next input shape')
 pointer=inputs['script_pointer']
 if type(pointer)is not int or not 0xE000000<=pointer<=0xF000000-rules['script']['file_size'] or inputs['driver']!='next declared original VM update without first-fade delay' or type(inputs['font_api'])is not int or inputs['font_api']!=0xE300000:raise ValueError('next supported binding/driver')
 mem=memory_regions(before);vm=mem[VM];obj=OBJECT_OFFSET;node=NODE_OFFSET;row=obj+0x110
 def get(o,fmt='H'):return struct.unpack_from('<'+fmt,vm,o)[0]
 if vm[4:6]!=b'\x01\x01' or vm[0x92E0] or vm[0x92E1] or vm[0x93E2] or (get(0x1C,'I'),get(0x20),get(0x22),get(0x24),get(node),get(node+2),get(obj+22))!=(238,0,17,6,1,2,1):raise ValueError('next source actual parent state')
 if get(0x10,'I')!=pointer+452 or get(0x18,'I')!=pointer+948 or vm[0x1CC]!=7 or (get(obj+24),get(obj+26),get(obj+28),get(obj+30),get(obj+32),get(obj+34))!=(3,0,24,1,12,0):raise ValueError('next retained first text state')
 if (get(obj),get(obj+6),get(obj+8),vm[obj+4],vm[obj+10],get(obj+12),get(obj+16))!=(24,12,0,0,0,0,0):raise ValueError('next source object timing/font')
 for offset,value in rules['initial_row_fields'].items():struct.pack_into('<H',vm,row+int(offset),value)
 struct.pack_into('<H',vm,0x22,17);struct.pack_into('<H',vm,0x24,6);vm[0x93E2]=0
 counter=mem[0x7A4E18];struct.pack_into('<I',counter,0,(struct.unpack_from('<I',counter)[0]+1)&0xFFFFFFFF);struct.pack_into('<I',counter,4,0)
 alloc=rules['stack_allocations'];vm_frame=STACK+0xFF00-4;text_frame=vm_frame-alloc['vm']-32;font_frame=text_frame-alloc['text']-28;font_sp=font_frame-alloc['font']-12-56-4
 line=text_frame-0xA04;array=text_frame-0xA2C;entry=rules['second_text'];parts=split_original(bytes.fromhex(entry['hex']))
 return {'after':[{'pointer':at,'bytes':n,'hex':mem[at].hex()} for at,n in REGIONS],
  'second_text':{'index':1,'pointer':pointer+entry['offset'],'hex':entry['hex']},
  'split':{'count':1,'source_pointer':pointer+entry['offset'],'array_pointer':array,'lines':[{'pointer':line,'hex':parts[0].hex()}]},
  'calls':[{'va':'0x4c4b80','receiver':VM,'args':[0,pointer+690,0],'return_va':'0x4cec2b'},
   {'va':'0x4c2120','receiver':VM,'args':[pointer+948,1],'return_va':'0x4c4bcc'},
   {'va':'0x4cabd0','receiver':VM+obj,'args':[line,((VM+obj)&0xFFFF0000)|12],'return_va':'0x4c4d04'}],
  'pending_font':{'api':'CreateFontA','va':'0xe300000','import_slot':'0x5920a0','args':rules['font_arguments'],'face_hex':rules['font_face']['hex'],
   'return_va':'0x4cad09','root_return_va':hex(RETURN),'frames':{'vm':vm_frame,'text':text_frame,'font':font_frame,'sp':font_sp},
   'natural_stack_verified':True,'first_instruction_executed':False}}

def compare_case(case):
 first=case['first_live_text'];next_=case['next_text'];first_rule=first_expected(first)
 if first_rule['after']!=first['after'] or first['after']!=next_['before']:raise ValueError('next complete live first parent mismatch')
 for key,result in expected_next(next_['inputs'],next_['before']).items():
  if next_[key]!=result:raise ValueError('next complete source mismatch: '+key)
 readiness=next_['first_readiness']
 if readiness['va']!='0x4cb5f0' or readiness['receiver']!=VM+OBJECT_OFFSET or readiness['return_value']!=0 or readiness['original_VM_called_predicate'] is not False or not all(readiness[k] is True for k in ('actual_record','program_regions_unchanged','CPU_and_stack_restored')):raise ValueError('next original readiness observation')
 if next_['first_owner_alive_at_boundary'] is not True or next_['first_resource_retained'] is not True or next_['first_actual_readback']!=first['actual_readback'] or next_['first_actual_readback']['hex']!=first_rule['pixel_hex']:raise ValueError('next complete retained actual texture')
 if not next_['retained_ranges_unchanged'] or not first['process_exited'] or not first['COM_process_cleanup']['all_owned_resources_released']:raise ValueError('next retained memory/owned cleanup')
 if any(next_[k] is not False for k in ('second_font_executed','second_texture_created','second_handler_completed','first_fade_completed','GPU_draw_or_present_executed','world_update_loop_executed','waves_executed')):raise ValueError('next source execution boundary')
 return {'complete_regions_compared':len(REGIONS),'pending_stack_arguments':14,'actual_texture_bytes':len(bytes.fromhex(first_rule['pixel_hex'])),
  'first_predicate_ready':False,'second_font_pending':True,'retained_bytes':next_['retained_bytes']}

@lru_cache(maxsize=1)
def native_fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('next evidence identity')
 return json.loads(raw)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');a=p.parse_args()
 if a.verify:
  data=native_fixture();result={'source':source_catalog(),'native_report_sha256':EVIDENCE_SHA256,
   'cases':[{'name':case['name'],**compare_case(case)} for case in data['cases']]}
  print(report_text(result))

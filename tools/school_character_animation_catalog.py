"""Source-derived character fades, readiness and third-text prefix; no live GPU draw."""
from functools import lru_cache
from tools.school_character_image_catalog import *
from tools.school_character_prefix_catalog import source_catalog as character_rules
from tools.school_board_opening_catalog import interpolate,TASK
from tools.school_text_preparation_catalog import stable_board_records,source_catalog as text_rules,split_original
from tools.school_text_timing_catalog import expected_update,BYTES

NODE7=VM+0x6F60+7*0xE0;OBJECT7=VM+0x430+7*0xAB8
NAME_TEXTURE=NODE+0x60

@lru_cache(maxsize=1)
def source_rules():
 c=character_rules();raw=SOURCE.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32)
 pairs={0x4CC406:('call','0x4cc420'),0x4CC48D:('call','0x4c9610'),0x4CC49A:('call','0x4c9650'),
  0x4CA225:('jle','0x4ca239'),0x4CA42F:('jle','0x4ca443'),0x4C9D88:('jle','0x4c9d9c'),
  0x4D0074:('call','0x4cd060'),0x4D0089:('call','0x4cd120'),0x4CD1B2:('jle','0x4cd1b6'),
  0x4CA8DF:('call','0x4077c0'),0x40780D:('mov','dword ptr [ecx + 0x4c], edx'),0x4CA936:('call','0x408f90'),
  0x4C4E9A:('mov','eax, dword ptr [ebp + 0x10]'),0x4CFF1B:('jmp','0x4d01e1')}
 proof=[]
 for at,pair in pairs.items():
  i=next(md.disasm(raw[at-BASE:at-BASE+16],at,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError('character animation source instruction '+hex(at))
  proof.append({'va':hex(at),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 def table(at,count):return list(struct.unpack_from('<'+'I'*count,raw,at-BASE))
 mode=table(0x4CA5E3,6);background=table(0x4CA03F,7)
 if mode!=[0x4CA280,0x4CA330,0x4CA452,0x4CA585,0x4CA203,0x4CA244] or background!=[0x4C9C06,0x4C9CCB,0x4C9AD3,0x4C9DB1,0x4C9F0A,0x4C9C84,0x4C9BC4]:raise ValueError('actual mode dispatch tables')
 if table(0x4D03CF+25*4,1)!=[0x4CED8F] or table(0x4D066F+raw[0x4D06AB-BASE+18]*4,1)!=[0x4D0068]:raise ValueError('actual opcode30 dispatch tables')
 at=table(0x624834+5*4,1)[0];pieces=[]
 for n in range(16):
  r=list(struct.unpack_from('<6h',raw,at-BASE+n*12))
  if r[0]==-1:break
  pieces.append(r)
 else:raise ValueError('character frame sentinel')
 if at!=0x6247E8 or len(pieces)!=6:raise ValueError('character frame geometry')
 sc=0x622758;scraw=raw[sc-BASE:sc-BASE+60]
 if struct.unpack_from('<5H',scraw,8)!=(108,108,0,0,296):raise ValueError('character face source rectangle')
 script,layout=script_layout()
 if struct.unpack_from('<2HI',script,724)!=(43,8,0x20000008) or struct.unpack_from('<3H',script,732)!=(17,6,2):raise ValueError('third-text source commands')
 text=text_rules();entry=text['entries'][2]
 if len(split_original(bytes.fromhex(entry['hex'])))!=1:raise ValueError('third-text single-line contract')
 return {'source_image_sha256':SOURCE_SHA256,'configuration':c['configuration'],'code_inputs':proof,
  'frame_table':{'va':at,'pieces':pieces},'face_table':{'va':sc,'hex':scraw.hex()},'mode_dispatch':mode,'background_dispatch':background,
  'delay_limit':30,'fade_limit':45,'background_limit':60,'updates':78,'third_text':entry,
  'scope':'Native character animation and readiness, third text to unexecuted CreateFontA. Draw queue, GPU, world and full dialogue remain boundaries.'}

def state(before):
 m=memory_regions(before);v=m[VM];n=NODE-VM
 def get(o):return struct.unpack_from('<H',v,n+o)[0]
 return {'pc':struct.unpack_from('<I',v,28)[0],'wait':struct.unpack_from('<H',v,32)[0],
  'mode':get(2),'previous_mode':get(4),'fade_count':get(6),'fade_limit':get(16),'delay_count':get(18),'delay_limit':get(20),
  'background_mode':get(34),'background_count':get(36),'background_limit':get(38),
  'instruction_count':struct.unpack_from('<I',m[0x7A4E18])[0],'waiting_count':struct.unpack_from('<I',m[0x7A4E18],4)[0]}

def advance(before,index,renderer):
 rules=source_rules();m=memory_regions(before);v=m[VM];n=NODE-VM;o=OBJECT-VM
 if type(index)is not int or not 0<=index<78 or type(renderer)is not int or not renderer:raise ValueError('bounded character update driver')
 def get(off):return struct.unpack_from('<H',v,n+off)[0]
 def put(off,value):struct.pack_into('<H',v,n+off,value)
 if get(0)!=1 or get(8)!=5 or get(0x30) or v[n+0x32] or struct.unpack_from('<H',v,o+22)[0] or struct.unpack_from('<2H',v,n+0xA0)!=(88,24):raise ValueError('supported character object/configuration')
 if any(struct.unpack_from('<H',v,0x6F60+i*0xE0)[0] for i in range(10) if i not in (5,7)):raise ValueError('extra active presentation refused')
 predicates=[];old=state(before)
 if index==0:
  if struct.unpack_from('<I3H',v,28)!=(252,0,30,20) or (get(2),get(34))!=(1,0):raise ValueError('natural image return parent')
  for at,value in {2:6,6:0,16:45,18:0,20:30,34:3,36:0,38:60,40:0,42:0,56:0}.items():put(at,value)
  struct.pack_into('<IH',v,28,272,1)
 else:
  if struct.unpack_from('<I3H',v,28)!=(272,1,30,20) or get(2) not in (2,3,6) or get(34) not in (2,3):raise ValueError('character held animation parent')
  v[0x93E2]=0;struct.pack_into('<2I',m[0x7A4E18],0,0,old['waiting_count']+1)
  for at,off,hi,ret in ((0x4CD060,2,7,0x4D0079),(0x4CD120,34,8,0x4D008E)):
   ready=int(not any(struct.unpack_from('<H',v,0x6F60+i*0xE0)[0] and 3<=struct.unpack_from('<H',v,0x6F60+i*0xE0+off)[0]<=hi for i in range(10)))
   predicates.append({'va':hex(at),'receiver':VM,'args':[0],'return_va':hex(ret),'return_value':ready})
  if all(p['return_value'] for p in predicates):struct.pack_into('<H',v,32,0)
 def call(va,recv,args,ret):return {'va':hex(va),'receiver':recv,'args':args,'return_va':hex(ret),'return_value':0}
 draws=[];mode=get(2);count=get(6)
 if mode in (2,3):
  alpha=interpolate(count,45,255) if mode==3 else 255;color=interpolate(count,45,204) if mode==3 else 204
  draws=[call(0x4CBDB0,VM,[254+r[0],368+r[1],0x620000|alpha,0xFFFFFFFF,66,*r[2:],20,0],0x4CA6FC) for r in rules['frame_table']['pieces']]
  draws.append(call(0x410310,TASK+0x1058,[277,381,695,154,67 if mode==3 else 0xFFFF0043,(color<<24)|0x223438,1],0x4CA409 if mode==3 else 0x4CA319))
  if mode==2:
   struct.pack_into('<I',v,n+0xAC,renderer);struct.pack_into('<I',v,n+0xBC,1);v[n+0xC4:n+0xC8]=b'\xff'*4;put(0xD6,53)
   draws.append(call(0x408F90,NAME_TEXTURE,[811,517],0x4CA93B))
 if mode==6:
  put(18,get(18)+1)
  if get(18)>get(20):put(18,0);put(2,3)
 elif mode==3:
  put(6,count+1)
  if get(6)>45:put(6,0);put(2,2)
 bg=get(34);bgcount=get(36);alpha=interpolate(bgcount,60,255) if bg==3 else 255
 draws += [call(0x4CBDB0,VM,[736,214,alpha,0xFFFFFFFF,64,0,0,256,296,32,0],0x4C9778),
  call(0x4CBDB0,VM,[736,214,alpha,0xFFFFFFFF,63,0,296,108,108,32,0],0x4C99BF)]
 if bg==3:
  put(36,bgcount+1)
  if bgcount>60:put(36,0);put(34,2)
 put(4,get(2))
 records=stable_board_records([struct.unpack('<H',m[TASK+x])[0] for x in (0x196C,0x1970)])
 records[1+5*3:1+5*3+3]=draws
 updates=[];textdraws=[]
 for node,obj in ((NODE,OBJECT),(NODE7,OBJECT7)):
  if node==NODE and get(2)!=2:continue
  off=obj-VM;origin=list(struct.unpack_from('<2H',v,node-VM+30));raw=bytes(v[off:off+BYTES])
  if obj==OBJECT7:
   text=expected_update(raw,origin,obj);v[off:off+BYTES]=bytes.fromhex(text['after_hex']);textdraws+=text['draws']
  updates.append({'receiver':obj,'args':[(node&0xFFFF0000)|origin[0],origin[1]],'return_va':'0x4cd541'})
 after=regions(m)
 return {'index':index,'before_state':old,'after_state':state(after),'after':after,'predicates':predicates,'presentation':records,'text_draws':textdraws,'text_updates':updates,'natural_return':{'va':RETURN,'sp':STACK+0xFF04,'eax':1}}

def third_prefix(before,pointer):
 rules=source_rules();text=text_rules();m=memory_regions(before);v=m[VM];n=NODE-VM;o=OBJECT-VM
 if type(pointer)is not int or not 0xE000000<=pointer<=0xF000000-text['script']['file_size']:raise ValueError('third source binding')
 if struct.unpack_from('<I3H',v,28)!=(272,0,30,20) or struct.unpack_from('<2H',v,n)!=(1,2) or struct.unpack_from('<H',v,n+34)[0]!=2 or struct.unpack_from('<H',v,o+22)[0]:raise ValueError('third natural released animation parent')
 if struct.unpack_from('<I',v,16)[0]!=pointer+452 or struct.unpack_from('<I',v,24)[0]!=pointer+948:raise ValueError('third original script binding')
 struct.pack_into('<I',v,0x9250,8);v[0x1CC]=5;struct.pack_into('<2HI',v,0x34,715,491,NODE)
 struct.pack_into('<I3H',v,28,280,0,43,8);v[0x93E2]=0;struct.pack_into('<2I',m[0x7A4E18],0,1,0)
 # The original interpreter executes one command per update even for return0.
 # Presentation is the already steady layer5/layer7 frame; no readiness query.
 records=stable_board_records([struct.unpack('<H',m[TASK+x])[0] for x in (0x196C,0x1970)])
 def call(va,recv,args,ret):return {'va':hex(va),'receiver':recv,'args':args,'return_va':hex(ret),'return_value':0}
 draws=[call(0x4CBDB0,VM,[254+r[0],368+r[1],0x6200FF,0xFFFFFFFF,66,*r[2:],20,0],0x4CA6FC) for r in rules['frame_table']['pieces']]
 draws += [call(0x410310,TASK+0x1058,[277,381,695,154,0xFFFF0043,0xCC223438,1],0x4CA319),call(0x408F90,NAME_TEXTURE,[811,517],0x4CA93B),
  call(0x4CBDB0,VM,[736,214,255,0xFFFFFFFF,64,0,0,256,296,32,0],0x4C9778),call(0x4CBDB0,VM,[736,214,255,0xFFFFFFFF,63,0,296,108,108,32,0],0x4C99BF)]
 records[16:19]=draws
 textdraws=expected_update(bytes(v[OBJECT7-VM:OBJECT7-VM+BYTES]),list(struct.unpack_from('<2H',v,NODE7-VM+30)),OBJECT7)['draws']
 activation={'after':regions(m),'presentation':records,'text_draws':textdraws,'text_updates':[{'receiver':obj,'args':[(node&0xFFFF0000)|struct.unpack_from('<H',v,node-VM+30)[0],struct.unpack_from('<H',v,node-VM+32)[0]],'return_va':'0x4cd541'} for node,obj in ((NODE,OBJECT),(NODE7,OBJECT7))],
  'predicates':[],'natural_return':{'va':RETURN,'sp':STACK+0xFF04,'eax':1}}
 struct.pack_into('<2H',v,34,17,6);struct.pack_into('<2I',m[0x7A4E18],0,2,0)
 for at,value in ((24,2),(26,0),(28,24),(30,0),(32,12),(34,0),(36,22)):struct.pack_into('<H',v,o+at,value)
 vm=STACK+0xFF00-4;t=vm-112-32;f=t-2676-28;sp=f-336-12-56-4;line=t-0xA04;array=t-0xA2C;entry=rules['third_text']
 return {'after':regions(m),'activation':activation,'third_text':{'index':2,'pointer':pointer+entry['offset'],'hex':entry['hex'],'decoded_big5':entry['text']},
  'calls':[{'va':'0x4c4dc0','receiver':VM,'args':[0,pointer+724,0],'return_va':'0x4cef42'},
   {'va':'0x4c4b80','receiver':VM,'args':[0,pointer+732,0],'return_va':'0x4cec2b'},
   {'va':'0x4c2120','receiver':VM,'args':[pointer+948,2],'return_va':'0x4c4bcc'},
   {'va':'0x4cabd0','receiver':OBJECT,'args':[line,(OBJECT&0xFFFF0000)|12],'return_va':'0x4c4d04'}],
  'split':{'count':1,'source_pointer':pointer+entry['offset'],'array_pointer':array,'lines':[{'pointer':line,'hex':entry['hex']}]},
  'pending_font':{'api':'CreateFontA','va':'0xe300000','import_slot':'0x5920a0','args':text['first_font_arguments'],'face_hex':text['face']['hex'],
   'return_va':'0x4cad09','root_return_va':hex(RETURN),'frames':{'vm':vm,'text':t,'font':f,'sp':sp},'natural_stack_verified':True,'first_instruction_executed':False}}

if __name__=='__main__':
 import sys
 sys.stdout.reconfigure(encoding='utf-8');print(report_text(source_rules()),end='')

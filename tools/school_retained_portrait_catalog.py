"""Installed script instruction inventory and source-derived portrait dependencies."""
import hashlib,json,struct
from collections import Counter
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_retained_keyboard import ROOT,SOURCE,SOURCE_SHA256,BASE,sha,need
from tools.school_script_preflight_catalog import package_offsets,vm_offsets

INSTALLED=ROOT/'CROSS HERMIT/CROSS HERMIT'
PRIVATE=ROOT/'.venv-audit/scene-callback-runtime/CROSS HERMIT/CROSS HERMIT'
SCRIPTS=INSTALLED/'DATA/TACTICS/SCRIPT'


def commands(raw):
 size,groups=package_offsets(raw);need(size==len(raw) and len(groups)==2,'complete two-group script package')
 g=groups[0];n,subs=package_offsets(raw,g);need(g+n==groups[1],'VM group exact extent');segments=[];empty=0;rows=[]
 for i,offset in enumerate(subs):
  start=g+offset;end=g+(subs[i+1] if i+1<len(subs) else n)
  if end-start==4:
   need(raw[start:end]==b'dmf\0','four-byte source dmf marker');empty+=1;continue
  offsets=vm_offsets(raw,start,end);need(len(offsets)>=2,'VM code endpoints');at=start+offsets[0];limit=start+offsets[1];first=len(rows)
  while at<limit:
   need(at+4<=limit,'complete instruction header');op,step=struct.unpack_from('<HH',raw,at);need(step>=4 and step%2==0 and at+step<=limit,'complete bounded instruction')
   rows.append(dict(segment=i,offset=at,PC=at-start-offsets[0],opcode=op,bytes=step,sha256=sha(raw[at:at+step])));at+=step
  need(at==limit,'exact code extent');segments.append(dict(index=i,start=start,end=end,offsets=offsets,code_start=start+offsets[0],code_end=limit,first_command=first,command_count=len(rows)-first))
 return dict(empty_segments=empty,segments=segments,commands=rows)


def string(raw,at):
 need(type(at)is int and BASE<=at<BASE+len(raw),'source string pointer');b=raw[at-BASE:at-BASE+256];end=b.find(bytes(1));need(end>=0,'bounded source string');return b[:end]


def role(raw,index):
 need(type(index)is int and 0<=index<256,'literal portrait role range')
 name_pointer=struct.unpack_from('<I',raw,0x621f2c-BASE+index*4)[0];table=0x622668+index*60;entry=raw[table-BASE:table-BASE+60];filename=string(raw,struct.unpack_from('<I',entry)[0]).decode('ascii')
 need(filename and '/' not in filename and '\\' not in filename and filename.lower().endswith('.bin'),'source portrait basename')
 path=INSTALLED/'DATA/ADV/BIN'/filename;data=path.read_bytes();need(data==(PRIVATE/path.relative_to(INSTALLED)).read_bytes(),'installed/private image bytes')
 name=string(raw,name_pointer)
 return dict(index=index,name_pointer=name_pointer,name_hex=name.hex(),name_big5=name.decode('big5'),resource_row=table,resource_row_hex=entry.hex(),filename=filename,image_path=path.relative_to(ROOT).as_posix(),image_bytes=len(data),image_sha256=sha(data))


def configuration(raw,index):
 need(type(index)is int and 0<=index<16,'literal portrait configuration range');at=0x624520+index*38;b=raw[at-BASE:at-BASE+38];words=list(struct.unpack('<19h',b));need(0<=words[0]<10,'source layer index')
 return dict(index=index,pointer=at,hex=b.hex(),words=words,layer=words[0])


def dependency(raw,command):
 need(len(command) in (12,20) and struct.unpack_from('<HH',command)==(30,len(command)),'sourced opcode30 declared encoding');encoded=list(struct.unpack_from('<'+'I'*((len(command)-4)//4),command,4));expressions=[dict(raw=x,type=x>>28,payload=x&0xfffffff,literal=(x&0xfffffff) if x>>28==2 else None) for x in encoded]
 need(expressions[0]['literal'] is not None and expressions[1]['literal'] is not None,'literal configuration and role for installed portrait corpus')
 return dict(expressions=expressions,configuration=expressions[0]['literal'],role=expressions[1]['literal'],expression_is_dynamic=any(x['type']!=2 for x in expressions),declared_bytes=len(command),missing_declared_operands=4-len(expressions),encoding_status='complete_four_operands' if len(command)==20 else 'short_two_operands; original fixed handler reads beyond declared command; runtime unresolved')


def dispatch(raw,op):
 if op==19:return dict(opcode=19,kind='END special before switch',entry=0x4cea19,direct_call_targets=[0x4ce090,0x4ce800])
 need(5<=op<=172,'source opcode dispatch range');at=struct.unpack_from('<I',raw,0x4d03cf-BASE+(op-5)*4)[0];need(0x4cea97<=at<0x4cff1b,'source opcode switch target')
 md=Cs(CS_ARCH_X86,CS_MODE_32);instructions=[];calls=[]
 for i in md.disasm(raw[at-BASE:at-BASE+128],at):
  instructions.append(dict(va=i.address,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
  if i.mnemonic=='call' and i.op_str.startswith('0x'):calls.append(int(i.op_str,16))
  if i.mnemonic in ('jmp','ret'):break
 need(instructions,'source dispatch block')
 return dict(opcode=op,kind='original switch block; not full handler semantics',table_slot=0x4d03cf+(op-5)*4,entry=at,direct_call_targets=calls,instructions=instructions)


def build():
 raw=SOURCE.read_bytes();need(sha(raw)==SOURCE_SHA256,'source executable identity');files=sorted(SCRIPTS.glob('*.BIN'));need(files,'installed script corpus');scripts=[];counts=Counter();portraits=[];configs={};roles={}
 for path in files:
  data=path.read_bytes();need(data==(PRIVATE/path.relative_to(INSTALLED)).read_bytes(),'installed/private script identity');decoded=commands(data)
  for c in decoded['commands']:
   counts[c['opcode']]+=1
   if c['opcode']==30:
    d=dependency(raw,data[c['offset']:c['offset']+c['bytes']]);portraits.append(dict(script=path.name,segment=c['segment'],offset=c['offset'],PC=c['PC'],source_handler_read_window_hex=data[c['offset']:c['offset']+20].hex(),**d))
    configs[d['configuration']]=configuration(raw,d['configuration']);roles[d['role']]=role(raw,d['role'])
  scripts.append(dict(name=path.name,path=path.relative_to(ROOT).as_posix(),bytes=len(data),sha256=sha(data),**decoded))
 return dict(schema_version=1,source_sha256=SOURCE_SHA256,scripts=scripts,opcode_counts={str(op):counts[op] for op in sorted(counts)},dispatch=[dispatch(raw,op) for op in sorted(counts)],portraits=portraits,configurations={str(k):v for k,v in sorted(configs.items())},roles={str(k):v for k,v in sorted(roles.items())},summary=dict(script_files=len(scripts),VM_segments=sum(len(s['segments']) for s in scripts),empty_segments=sum(s['empty_segments'] for s in scripts),commands=sum(counts.values()),opcode_classes=len(counts),portrait_commands=len(portraits),portrait_configurations=len(configs),portrait_roles=len(roles),dynamic_portrait_expressions=sum(d['expression_is_dynamic'] for d in portraits),short_portrait_commands=sum(bool(d['missing_declared_operands']) for d in portraits)),scope='All installed script bytes statically parsed; not dynamic reachability, full opcode semantics or R6 completion')


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable catalog output required')
 result=build();out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+chr(10),encoding='utf8',newline=chr(10));print(result['summary'])

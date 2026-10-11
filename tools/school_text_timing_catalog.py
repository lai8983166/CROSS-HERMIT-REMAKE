"""Independent original text fade, line cadence and readiness rules."""
import argparse,hashlib,json,struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_font_raster_catalog import ROOT,SOURCE,SOURCE_SHA256,BASE,AUTHORITY,report_text

STRIDE=0x110;BYTES=0xAB8
EVIDENCE=ROOT/'analysis/school-text-timing-v1-20261012.json'
EVIDENCE_SHA256='3eda53dd563a2db79be61e6f40b9e0471a2123c1047f460490e657bccc4aef11'
def signed(v):return v if v<32768 else v-65536

def validate_records(records):
 if not isinstance(records,list) or not 1<=len(records)<=10:raise ValueError('text bounded record count')
 for r in records:
  if not isinstance(r,dict) or set(r)!={'mode','fade_count','fade_limit','interval_count','interval_limit','following_ready','height'} or any(type(v)is not int for v in r.values()):raise ValueError('text isolated record shape')
  if r['mode'] not in (1,2,3,4) or not 0<=r['fade_count']<=65535 or not 1<=r['fade_limit']<=32767 or not 0<=r['interval_count']<=65535 or not 0<=r['interval_limit']<=32767 or r['following_ready'] not in (0,1) or not 1<=r['height']<=256:raise ValueError('text isolated record bounds')

def encode_records(records):
 validate_records(records);raw=bytearray(BYTES);struct.pack_into('<H',raw,22,len(records))
 for i,r in enumerate(records):
  at=i*STRIDE
  for o,k in ((24,'mode'),(26,'fade_count'),(28,'fade_limit'),(30,'interval_count'),(32,'interval_limit'),(34,'following_ready'),(0x6A,'height')):struct.pack_into('<H',raw,at+o,r[k])
 return bytes(raw)

def expected_update(raw,origin,object_pointer):
 if not isinstance(raw,bytes) or len(raw)!=BYTES or not isinstance(origin,list) or len(origin)!=2 or any(type(v)is not int or not 0<=v<=65535 for v in origin) or type(object_pointer)is not int:raise ValueError('text isolated input bytes/origin')
 count=struct.unpack_from('<H',raw,22)[0]
 records=[]
 for i in range(count):
  records.append({k:struct.unpack_from('<H',raw,i*STRIDE+o)[0] for o,k in ((24,'mode'),(26,'fade_count'),(28,'fade_limit'),(30,'interval_count'),(32,'interval_limit'),(34,'following_ready'),(0x6A,'height'))})
 validate_records(records);out=bytearray(raw);draws=[];y=origin[1]
 def store(i,o,v):struct.pack_into('<H',out,i*STRIDE+o,v)
 def word(i,o):return struct.unpack_from('<H',out,i*STRIDE+o)[0]
 for i,r in enumerate(records):
  mode=r['mode'];visible=mode in (1,3);alpha=255;raw_alpha=255
  if mode==2:
   if i==0 or word(i-1,34):store(i,24,3)
  elif mode==3:
   fade=(r['fade_count']+1)&65535;store(i,26,fade)
   if signed(fade)>r['fade_limit']:fade=r['fade_limit'];store(i,24,1);store(i,26,fade)
   numerator=signed(fade)*255;alpha=abs(numerator)//r['fade_limit']*(-1 if numerator<0 else 1)
   # Original4CB44A clears EDX after division and before loading DX for drawing.
   raw_alpha=alpha&65535
  if visible:
   draws.append({'va':'0x4cbf00','receiver':0x7D7C28,'args':[object_pointer+i*STRIDE+0x28,origin[0],y,1,raw_alpha,255,255,255,55],'return_va':'0x4cb4b2','return_value':0})
   y=(y+r['height'])&65535
  if i==0 or word(i-1,34)==1:
   interval=(r['interval_count']+1)&65535;store(i,30,interval)
   if signed(interval)>r['interval_limit']:store(i,30,r['interval_limit']);store(i,34,1)
 ready=not any(2<=word(i,24)<=4 for i in range(count))
 return {'after_hex':out.hex(),'draws':draws,'readiness':ready}

def source_catalog():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('timing original image identity')
 expected={0x4CB2AF:('ja','0x4cb454'),0x4CB30D:('mov','word ptr [eax + edx + 0x18], 3'),
  0x4CB32D:('mov','ax, word ptr [edx + ecx + 0x22]'),0x4CB371:('add','ax, 1'),0x4CB3BA:('jle','0x4cb402'),
  0x4CB3CE:('mov','word ptr [edx + ecx + 0x18], 1'),0x4CB443:('cdq',''),0x4CB444:('idiv','ecx'),0x4CB44A:('xor','edx, edx'),
  0x4CB4AD:('call','0x4cbf00'),0x4CB4C7:('add','dx, word ptr [ecx + eax + 0x6a]'),
  0x4CB503:('cmp','ecx, 1'),0x4CB524:('add','cx, 1'),0x4CB56F:('jle','0x4cb5b6'),
  0x4CB5AF:('mov','word ptr [ecx + eax + 0x22], 1'),0x4CB663:('cmp','dword ptr [ebp - 0x14], 2'),
  0x4CB669:('cmp','dword ptr [ebp - 0x14], 4'),0x4CB68B:('mov','al, 1'),0x4CB68F:('xor','al, al')}
 md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
 for at,pair in expected.items():
  i=next(md.disasm(raw[at-BASE:at-BASE+16],at,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError('text timing instruction differs')
  proof.append({'va':hex(at),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'code_inputs':proof,'line_stride':STRIDE,
  'first_line_fade_limit':24,'last_line_interval_limit':12,'mode2_changes_to3_before_fade':True,'scope':'declared isolated counters; no natural GPU/VM continuation',**AUTHORITY}

def native_fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('isolated timing report identity')
 return json.loads(raw)

def export():
 for label,value in (('rules',source_catalog()),('evidence',{'schema_version':1,'native_report_sha256':EVIDENCE_SHA256,'cases':native_fixture()['cases'],'runtime_fixture':False})):
  (ROOT/f'prototype/data/school_text_timing_{label}.json').write_text(report_text(value),encoding='utf-8',newline='\n')

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--export',action='store_true');a=p.parse_args()
 if a.export:export()

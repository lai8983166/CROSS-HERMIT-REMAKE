"""Independent original raster geometry, BGRA conversion and finite surfaces."""
import argparse,hashlib,json,struct
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_text_preparation_catalog import ROOT,SOURCE,SOURCE_SHA256,BASE,VM,memory_regions,REGIONS,report_text,AUTHORITY

EVIDENCE=ROOT/'analysis/school-font-raster-v1-20261012.json'
EVIDENCE_SHA256='b95eead169b1962e33cf59f6b365d58fa31645f45591d297c42d0cda0c35e6c0'
TEXTURE_OFFSET=0x430+7*0xAB8+0x28

@lru_cache(maxsize=1)
def source_catalog():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('raster source image identity')
 expected={0x4CAD1E:('call','0x56d810'),0x4CAD43:('call','0x4077c0'),0x4CAD5B:('call','0x4142b0'),0x4CAD77:('call','0x408e30'),
  0x40780D:('mov','dword ptr [ecx + 0x4c], edx'),0x4142D0:('mov','eax, dword ptr [eax + 0xb210]'),
  0x4051A9:('call','0x403730'),0x4037D5:('mov','dword ptr [eax + 0x28], 0'),
  0x405240:('call','dword ptr [0x5920bc]'),0x4052C2:('mov','ecx, 0xa'),0x4052CC:('cmp','dword ptr [ebp - 0x6c], 0'),
  0x4052D9:('cmp','dword ptr [ebp - 0x6c], 3'),0x4052EC:('lea','ecx, [eax + edx*2]'),0x4052F8:('lea','ecx, [eax + edx*2]'),
  0x4052FE:('mov','eax, 0x100'),0x405304:('idiv','dword ptr [ebp - 0x50]'),0x40530A:('shl','eax, 8'),
  0x405340:('mov','dword ptr [ebp - 0x38], 0x28'),0x405353:('mov','dword ptr [ebp - 0x30], eax'),
  0x405356:('mov','word ptr [ebp - 0x2c], 1'),0x405363:('mov','word ptr [ebp - 0x2a], 0x20'),
  0x4053C6:('call','dword ptr [0x592098]'),0x405652:('mov','esi, esp'),0x405654:('push','0x80808'),
  0x40568E:('add','ecx, dword ptr [ebp - 0x6c]'),0x4056A5:('push','0xffffff'),
  0x405701:('mov','word ptr [edx + 0x40], ax'),0x40570C:('mov','word ptr [ecx + 0x42], dx'),
  0x405713:('shr','eax, 8'),0x405716:('add','eax, 1'),0x405745:('mov','word ptr [edx + 0x3a], cx'),
  0x405764:('mov','dword ptr [eax + 0x34], 0x19'),0x405774:('call','0x403bd0'),
  0x405B30:('and','eax, 0xffffff'),0x405B3C:('and','ecx, 0xf80000'),0x405B42:('shr','ecx, 9'),
  0x405B4C:('and','edx, 0xf800'),0x405B52:('shr','edx, 6'),0x405B5C:('and','eax, 0xf8'),
  0x405B61:('shr','eax, 3'),0x405B71:('or','ch, 0x80'),0x405B9B:('mov','word ptr [edx + ecx*2], 0')}
 md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
 for at,pair in expected.items():
  i=next(md.disasm(raw[at-BASE:at-BASE+16],at,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError(f'raster original code {at:#x}: {i.mnemonic} {i.op_str}')
  proof.append({'va':hex(at),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'code_inputs':proof,'shadow_mode':2,
  'geometry':{'padding_divisor':10,'padding_min':1,'padding_max':3,'band_width':256,'texture_height_cap':256,'texture_format':25},
  'conversion':{'function':'0x405a80','alpha_rule':'RGB == 0 transparent; otherwise opaque; input alpha ignored','red_mask':0xF80000,'red_shift':9,
   'green_mask':0xF800,'green_shift':6,'blue_mask':0xF8,'blue_shift':3,'opaque_bit':0x8000},
  'scope':'Natural host raster pending texture creation; conversion separately executed on declared CPU memory surface; no GPU or native text completion.',**AUTHORITY}

def geometry(measured):
 if not isinstance(measured,list) or len(measured)!=2 or any(type(v)is not int for v in measured) or not 1<=measured[0]<=100000 or not 1<=measured[1]<=250:raise ValueError('unsupported measured extent')
 width,height=measured;pad=max(1,min(3,height//10));height+=2*pad;width=min(width+2*pad,(256//height+1)*256);bands=(width>>8)+1
 return {'padding':pad,'raster_size':[width,height],'texture_size':[min(width,256),min(bands*height,256)],'bands':bands,
  'header_hex':struct.pack('<IiiHHIIiiII',40,width,-height,1,32,0,0,0,0,0,0).hex()}

def expected_raster(inputs,before,measured):
 if not isinstance(inputs,dict) or inputs.get('platform')!='real_host_GDI_offscreen_measurement_DC' or type(inputs.get('graphics_context'))is not int or not inputs['graphics_context'] or type(inputs.get('device'))is not int or inputs['device']!=0 or type(inputs.get('host_ansi_code_page'))is not int or inputs['host_ansi_code_page']<=0:raise ValueError('raster platform inputs')
 mem=memory_regions(before);vm=mem[VM];o=TEXTURE_OFFSET;cfg=geometry(measured)
 if struct.unpack_from('<2I',vm,o+0x2C)!=(0,0):raise ValueError('raster existing native texture')
 struct.pack_into('<I',vm,o+0x28,0);struct.pack_into('<I',vm,o+0x4C,inputs['graphics_context']);vm[o+0x64:o+0x68]=bytes([255]*4)
 struct.pack_into('<I',vm,o+0x34,25);struct.pack_into('<2H',vm,o+0x38,*cfg['texture_size']);struct.pack_into('<2H',vm,o+0x40,*cfg['raster_size'])
 return {'after':[{'pointer':a,'bytes':n,'hex':mem[a].hex()} for a,n in REGIONS],**cfg}

def convert_pixel(bgra):
 if type(bgra)is not int or not 0<=bgra<=0xFFFFFFFF:raise ValueError('raster pixel DWORD')
 if not bgra&0xFFFFFF:return 0
 return 0x8000|((bgra&0xF80000)>>9)|((bgra&0xF800)>>6)|((bgra&0xF8)>>3)

def validate_surface(raw,size,rect,dest,pitch,target):
 if not isinstance(raw,bytes) or len(raw)>0x100000 or not isinstance(size,list) or len(size)!=2 or any(type(v)is not int or not 1<=v<=1024 for v in size) or len(raw)!=size[0]*size[1]*4:raise ValueError('raster source size')
 if not isinstance(rect,list) or len(rect)!=4 or any(type(v)is not int or v<0 for v in rect):raise ValueError('raster source rectangle')
 x,y,w,h=rect
 if not w or not h or x+w>size[0] or y+h>size[1]:raise ValueError('raster rectangle outside source')
 if not isinstance(target,list) or len(target)!=2 or any(type(v)is not int or v<0 for v in target):raise ValueError('raster destination point')
 if type(pitch)is not int or pitch<2*(target[0]+w) or pitch>4096 or pitch%2 or not isinstance(dest,bytes) or len(dest)%pitch or len(dest)//pitch<target[1]+h or len(dest)>0x100000:raise ValueError('raster destination pitch/extent')

def convert_surface(raw,size,rect,dest,pitch,target):
 validate_surface(raw,size,rect,dest,pitch,target);out=bytearray(dest);x,y,w,h=rect;tx,ty=target
 for row in range(h):
  for col in range(w):
   pixel=struct.unpack_from('<I',raw,4*((y+row)*size[0]+x+col))[0];struct.pack_into('<H',out,(ty+row)*pitch+2*(tx+col),convert_pixel(pixel))
 return bytes(out)

@lru_cache(maxsize=1)
def native_fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('raster native report identity')
 return json.loads(raw)

def export():
 rules=source_catalog();native=native_fixture()
 for label,value in (('rules',rules),('evidence',{'schema_version':1,'native_report_sha256':EVIDENCE_SHA256,'cases':native['cases'],'inherited_refusals':native['inherited_refusals'],'runtime_fixture':False})):
  (ROOT/f'prototype/data/school_font_raster_{label}.json').write_text(report_text(value),encoding='utf-8',newline='\n')

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--export',action='store_true');a=p.parse_args()
 if a.export:export()

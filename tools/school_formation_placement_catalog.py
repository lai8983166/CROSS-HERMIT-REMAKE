"""Independent original formation inputs and pure complete byte projection."""
import argparse,hashlib,json,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_map_common_catalog import map_common_inputs
from tools.school_map_common_emulation import map_common_resource
from tools.school_unitctrl_map_emulation import map_resource
from tools.school_formation_placement_emulation import ROOT,UNITCTRL,WORK_OFFSET,WORK_BYTES,RECORD_OFFSET,AUTHORITY,report_text,NATIVE
from tools.tactics_exit_emulation import SOURCE,SOURCE_SHA256,BASE

EVIDENCE=ROOT/'analysis/school-formation-placement-v1-20261011.json'
EVIDENCE_SHA256='49539eef42ffb378a48935a0509675a2412fd5c2649956fb93c4f69df973d383'

@lru_cache(maxsize=1)
def source_catalog():
 image=SOURCE.read_bytes()
 if hashlib.sha256(image).hexdigest()!=SOURCE_SHA256:raise ValueError('formation source image identity')
 md=Cs(CS_ARCH_X86,CS_MODE_32);inputs=[]
 expected={0x45349C:('call','0x468910'),0x468A44:('call','0x49a480'),
  0x49A4C4:('je','0x49a5e2'),0x49A51A:('cmp','eax, 1'),0x49A5A9:('call','0x468690'),
  0x468E70:('cmp','ecx, 1'),0x468E84:('cmp','ecx, 0x2d'),
  0x43D724:('mov','dword ptr [ebp - 0x2c], 5'),0x43D7CC:('imul','eax, eax, 3'),
  0x43D6A0:('jle','0x43d6c6'),0x43D8F0:('cmp','dword ptr [ebp + 0x14], 4'),
  0x43BF3D:('imul','eax, eax, 0x4c'),0x43BF4E:('shl','eax, 4'),
  0x43BF51:('mov','ecx, dword ptr [edx + eax + 0xc]'),0x43BF75:('test','eax, eax')}
 for va,(mn,op) in expected.items():
  ins=next(md.disasm(image[va-BASE:va-BASE+16],va,count=1))
  if (ins.mnemonic,ins.op_str)!=(mn,op):raise ValueError('formation source instruction differs')
  inputs.append({'va':hex(va),'hex':ins.bytes.hex(),'mnemonic':mn,'operands':op})
 common,identity=map_common_resource();parts=map_common_inputs(common)['sections'];terrain=common[parts[1]['offset']:parts[1]['offset']+parts[1]['bytes']]
 logical,map_identity=map_resource('map05.bin')
 grid=appearance_grid()
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'scene_id':5,'code_inputs':inputs,
  'native_ranges':[[hex(a),hex(b)] for a,b in NATIVE],
  'native_code_sha256':hashlib.sha256(b''.join(image[a-BASE:b-BASE] for a,b in NATIVE)).hexdigest(),
  'formation_sizes_hex':image[0x59558C-BASE:0x59558C-BASE+66].hex(),
  'terrain_source':identity,'terrain_offset':parts[1]['offset'],'terrain_hex':terrain.hex(),
  'logical_source':map_identity,'map_hex':logical.hex(),'grid_hex':grid.hex(),
  'grid_sha256':hashlib.sha256(grid).hexdigest(),'grid_dimensions':[65,65],
  'permutation_size':5,'rotation_multiplier':3,'reservation_capacity':40,
  'scope':'School formation only; stops468A49 before search allocation, full deployment or VM.',**AUTHORITY}

@lru_cache(maxsize=1)
def appearance_grid():
 # 43AB10: row-major coordinates; reverse-row-major rank within distance;
 # nearby odd/even checkerboard pairs receive unsigned key+8000 before sort.
 coordinates=[(x,y) for y in range(-32,33) for x in range(-32,33)]
 ranks={};keys={}
 for x,y in reversed(coordinates):
  d=abs(x)+abs(y);rank=ranks.get(d,0);ranks[d]=rank+1
  key=(d<<8)+rank
  if abs(x)<7 and abs(y)<7 and (x%2)!=(y%2):key+=0x8000
  keys[x,y]=key&65535
 ordered=sorted(coordinates,key=lambda p:keys[p])
 return b''.join(struct.pack('<bbHH',x,y,abs(x)+abs(y),i) for i,(x,y) in enumerate(ordered))

def _hex(value,size,label):
 if not isinstance(value,str):raise ValueError(label+' encoding')
 try:raw=bytes.fromhex(value)
 except ValueError as error:raise ValueError(label+' encoding') from error
 if len(raw)!=size:raise ValueError(label+' bytes')
 return raw

def expected_placement(inputs,units,rules=None):
 r=source_catalog() if rules is None else rules
 if not isinstance(inputs,dict) or not isinstance(units,list):raise ValueError('formation inputs shape')
 selected=inputs.get('selected_class');origin=inputs.get('origin');radius=inputs.get('formation_radius');rotation=inputs.get('before_rotation')
 if inputs.get('scene_id')!=5 or type(selected)is not int or not 0<=selected<=4 or type(radius)is not int or not 0<=radius<=32 \
  or not isinstance(origin,list) or len(origin)!=2 or any(type(v)is not int for v in origin) or not (0<=origin[0]<64 and 0<=origin[1]<96) \
  or type(rotation)is not int or not 0<=rotation<5:raise ValueError('unsupported formation header')
 for name in ('map_hex','grid_hex','formation_sizes_hex'):
  if inputs.get(name)!=r[name]:raise ValueError('formation source '+name)
 if inputs.get('grid_dimensions')!=[65,65]:raise ValueError('formation grid dimensions')
 terrain=bytes.fromhex(r['terrain_hex']);actual=_hex(inputs.get('terrain_hex'),7600,'formation terrain')
 if actual!=terrain:raise ValueError('formation source terrain')
 cm=bytearray(_hex(inputs.get('before_cm_hex'),12288,'formation CM'))
 _hex(inputs.get('before_reservation_hex'),164,'formation reservations')
 mapraw=bytes.fromhex(r['map_hex']);rows=list(struct.iter_unpack('<bbHH',bytes.fromhex(r['grid_hex'])))
 reservation=bytearray(164);placed=[];slots=[];indices=[];previous=-1
 for s in units:
  if not isinstance(s,dict):raise ValueError('formation slot shape')
  index=s.get('index')
  if type(index)is not int or not previous<index<250:raise ValueError('formation ordered unique slots')
  previous=index
  w=bytearray(_hex(s.get('before_work_hex'),WORK_BYTES,'formation work'));record=bytearray(_hex(s.get('before_record_hex'),176,'formation record'))
  if s.get('work_pointer')!=UNITCTRL+WORK_OFFSET+index*WORK_BYTES or s.get('record_pointer')!=UNITCTRL+RECORD_OFFSET+index*176 \
   or struct.unpack_from('<I',w,600)[0]!=s['record_pointer'] or struct.unpack_from('<h',w)[0]==0:raise ValueError('formation slot ownership')
  role=struct.unpack_from('<H',record,2)[0]
  if 1<=role<=45 and record[164]==selected and record[15]==1:
   mode=record[48]
   if mode>4:raise ValueError('formation movement mode source assertion')
   rotation=(rotation+1)%5;perm=list(range(5))
   for j in range(rotation*3):perm[0],perm[j%5]=perm[j%5],perm[0]
   point=None
   for j in range(4225):
    dx,dy,d,_=rows[(j//5)*5+perm[j%5]]
    if d>radius:continue
    x,y=origin[0]+dx,origin[1]+dy
    if not (0<=x<64 and 0<=y<96):continue
    cell=y*64+x;terrain_id=mapraw[16+6*cell]
    if terrain_id>=len(terrain)//76:raise ValueError('formation terrain index')
    if mode!=4 and (struct.unpack_from('<i',terrain,76*terrain_id+16*mode+12)[0]==0 or cm[2*cell+1]!=0):continue
    if (x,y) in placed:continue
    point=x,y;break
   if point is None:raise ValueError('formation has no available original candidate')
   if len(placed)>=40:raise ValueError('formation reservation capacity')
   x,y=point;struct.pack_into('<hh',reservation,4+len(placed)*4,x,y);placed.append(point);struct.pack_into('<I',reservation,0,len(placed))
   oldx,oldy=w[1255:1257]
   if not (oldx==255 or oldy==255):
    if not (oldx<64 and oldy<96):raise ValueError('formation previous grid bounds')
    pos=2*(oldy*64+oldx)+1;cm[pos]=(cm[pos]-1)&255
   struct.pack_into('<ii',w,748,(x*32+16)<<16,(y*16+8)<<16)
   w[1257:1259]=bytes((oldx,oldy));w[1255:1257]=bytes((x,y));record[155:157]=bytes((x,y))
   pos=2*(y*64+x)+1;cm[pos]=(cm[pos]+1)&255;indices.append(index)
  slots.append({'index':index,'work_hex':w.hex(),'record_hex':record.hex()})
 return {'units':slots,'selected_indices':indices,'positions':[list(p) for p in placed],
  'rotation':rotation,'reservation_hex':reservation.hex(),'cm_hex':cm.hex()}

def native_fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('formation frozen evidence identity')
 data=json.loads(raw)
 return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,
  'cases':[{k:deepcopy(c[k]) for k in ('name','ready','formation_placement_completed','formation_placement','stop_reason')} for c in data['cases']],**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--rules-out',required=True);p.add_argument('--fixture-out',required=True);a=p.parse_args()
 for name,data in ((a.rules_out,source_catalog()),(a.fixture_out,native_fixture())):
  (ROOT/name).write_text(report_text(data),encoding='utf-8',newline='\n')

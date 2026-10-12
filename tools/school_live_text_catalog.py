"""Independent original first texture completion, full memory and actual pixel rules."""
import argparse,hashlib,json,struct
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_font_raster_catalog import ROOT,SOURCE,SOURCE_SHA256,BASE,VM,REGIONS,memory_regions,geometry,convert_surface,AUTHORITY,report_text,TEXTURE_OFFSET
from tools.school_text_preparation_catalog import OBJECT_OFFSET,NODE_OFFSET
from tools.school_text_timing_catalog import expected_update,BYTES

EVIDENCE=ROOT/'analysis/school-live-text-v2-20261012.json'
EVIDENCE_SHA256='2f503342934a8c1e89cee8f893e66ec4d625cf041309a2d8d41c03664d69ecef'

@lru_cache(maxsize=1)
def source_catalog():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('live text source identity')
 pairs={0x408E33:('sub','esp, 0x44'),0x405163:('sub','esp, 0xec'),0x403BD3:('sub','esp, 0x74'),
  0x403CF9:('mov','word ptr [edx + 0x3c], ax'),0x403D04:('mov','word ptr [ecx + 0x3e], dx'),
  0x403D0D:('add','eax, dword ptr [ebp - 0x24]'),0x403D10:('mov','dword ptr [0x765720], eax'),
  0x403D1C:('or','dl, 2'),0x403D2C:('mov','dword ptr [ecx + 0x28], edx'),
  0x40393F:('push','0x800'),0x40395B:('call','dword ptr [ecx + 0x40]'),0x4039D0:('call','dword ptr [eax + 0x44]'),
  0x405869:('call','0x405a80'),0x40588B:('or','al, 4'),0x4058D2:('call','dword ptr [0x5920a4]'),
  0x40591B:('call','dword ptr [0x5920c4]'),0x405964:('call','dword ptr [0x592060]'),
  0x4D1C15:('call','dword ptr [0x5920c4]'),0x4CAD9B:('add','cx, 1'),0x4CADA2:('mov','word ptr [edx + 0x16], cx'),
  0x4CD52C:('mov','cx, word ptr [eax + 0x20]'),0x4CD534:('mov','ax, word ptr [edx + 0x1e]'),
  0x4CD53C:('call','0x4cb220'),0x4CD54B:('mov','word ptr [ecx + 4], ax')}
 md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
 for at,pair in pairs.items():
  i=next(md.disasm(raw[at-BASE:at-BASE+16],at,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError(f'live source code differs {at:x}')
  proof.append({'va':hex(at),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'code_inputs':proof,'pixel_rule':'original source RGB-nonzero A1R5G5B5',
  'source_stack':{'font_to_raster_frame':0x1DC,'font_to_texture_entry_sp':0x2E0},'first_update_mode':3,'first_update_interval_count':1,
  'scope':'native first text/VM return with explicit live platform binding; no original renderer startup or GPU draws',**AUTHORITY}

def expected(p):
 if not isinstance(p,dict) or p['binding']['before']!=0 or p['binding']['bound']!=p['platform_hello']['device']['pointer'] or type(p['binding']['bound'])is not int or not 0<p['binding']['bound']<0xFFFFFFFF:raise ValueError('live real device binding')
 raster=p['raster'];cfg=geometry(raster['measured']);mem=memory_regions(raster['before']);vm=mem[VM];o=TEXTURE_OFFSET
 if p['binding']['slot']!=raster['inputs']['graphics_context']+0xB210 or raster['inputs']['device']!=p['binding']['bound'] or p['platform_hello']['pointer_bytes']!=4 or p['platform_hello']['sdk']!=220 or p['platform_hello']['window_visible'] is not False:raise ValueError('declared live platform scope')
 if cfg['raster_size']!=[174,24] or cfg['texture_size']!=[174,24]:raise ValueError('supported source first glyph geometry')
 struct.pack_into('<I',vm,o+0x28,0);struct.pack_into('<I',vm,o+0x4C,raster['inputs']['graphics_context']);vm[o+0x64:o+0x68]=bytes([255]*4)
 struct.pack_into('<I',vm,o+0x34,25);struct.pack_into('<2H',vm,o+0x38,174,24);struct.pack_into('<2H',vm,o+0x40,174,24)
 prefix=[{'pointer':a,'bytes':n,'hex':mem[a].hex()} for a,n in REGIONS]
 if prefix!=p['before'] or prefix!=raster['after']:raise ValueError('independent complete raster prefix differs')
 if struct.unpack_from('<H',vm,OBJECT_OFFSET+22)[0]!=0:raise ValueError('native first empty line required')
 texture=p['texture'];device=p['binding']['bound']
 if type(texture['pointer'])is not int or not 0<texture['pointer']<0xFFFFFFFF:raise ValueError('live real texture pointer')
 struct.pack_into('<2I',vm,o+0x28,device,texture['pointer']);struct.pack_into('<2H',vm,o+0x3C,256,32)
 struct.pack_into('<H',vm,o+0x44,struct.unpack_from('<H',vm,o+0x44)[0]|6)
 struct.pack_into('<H',vm,OBJECT_OFFSET+22,1)
 origin=list(struct.unpack_from('<2H',vm,NODE_OFFSET+30));before_update=bytes(vm[OBJECT_OFFSET:OBJECT_OFFSET+BYTES])
 update=expected_update(before_update,origin,VM+OBJECT_OFFSET)
 if update['draws'] or update['readiness']:raise ValueError('first activation is not drawing/ready')
 vm[OBJECT_OFFSET:OBJECT_OFFSET+BYTES]=bytes.fromhex(update['after_hex'])
 struct.pack_into('<I',vm,0x1C,struct.unpack_from('<I',vm,0x1C)[0]+6)
 struct.pack_into('<H',vm,NODE_OFFSET+4,struct.unpack_from('<H',vm,NODE_OFFSET+2)[0])
 lock=p['lock'];pitch=lock['pitch'];raw=bytes.fromhex(raster['raster']['hex']);before=bytes.fromhex(lock['before_hex'])
 if type(pitch)is not int or not 512<=pitch<=4096 or pitch%2 or len(before)!=pitch*32:raise ValueError('live complete locked extent')
 out=convert_surface(raw,[174,24],[0,0,174,24],before,pitch,[0,0])
 return {'after':[{'pointer':a,'bytes':n,'hex':mem[a].hex()} for a,n in REGIONS],'pixel_hex':out.hex(),
  'accounting_after':(p['accounting_before']+16384)&0xFFFFFFFF,'first_update_args':[(VM+NODE_OFFSET)&0xFFFF0000|origin[0],origin[1]]}

@lru_cache(maxsize=1)
def native_fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('live evidence identity')
 return json.loads(raw)

def export():
 for label,value in (('rules',source_catalog()),('evidence',{'schema_version':1,'native_report_sha256':EVIDENCE_SHA256,'cases':native_fixture()['cases'],'runtime_fixture':False})):
  (ROOT/f'prototype/data/school_live_text_{label}.json').write_text(report_text(value),encoding='utf-8',newline='\n')

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--export',action='store_true');a=p.parse_args()
 if a.export:export()

"""Independent source rules for character-name GDI, texture and image entry."""
from tools.school_character_prefix_catalog import *
from tools.school_font_raster_catalog import geometry,convert_surface
from tools.school_second_live_text_catalog import bands
from tools.school_texture_contract import power_of_two

TEXTURE=NODE+0x60
TEXTURE_OFFSET=NODE_OFFSET+0x60
RASTER=0x3A000000
MIRROR=0x3B000000
PATH=0x7A4D4C
PREFIX_SHA='66606d60959a28b49f5b469cad13b55d87f6d3298fc91b081cd11f56c2a1c2f5'

def name_rules():
 c=source_catalog();raw=SOURCE.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32)
 pairs={0x4CA773:('sub','esp, 0x148'),0x408E33:('sub','esp, 0x44'),0x405163:('sub','esp, 0xec'),0x4CA7D5:('mov','dword ptr [ecx + 0x5c], eax'),0x4CA800:('call','0x4077c0'),0x4CA81B:('call','0x4142b0'),
  0x4CA827:('call','0x408e30'),0x4CA838:('call','0x4d1bf0'),0x4CC25F:('mov','word ptr [ecx + eax*2 + 0x34], dx'),
  0x4CC268:('call','0x4cbf90'),0x4CC091:('mov','dword ptr [ecx + eax*4 + 0x44], edx'),
  0x4CC0A4:('call','0x4cd7b0'),0x4CC0B9:('call','0x4cd810'),0x4CC0CD:('call','0x4cde10'),0x4CD7E3:('xor','edx, edx'),
  0x4D1C15:('call','dword ptr [0x5920c4]')}
 proof=[]
 for at,pair in pairs.items():
  i=next(md.disasm(raw[at-BASE:at-BASE+16],at,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError('name original instruction '+hex(at))
  proof.append({'va':hex(at),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 return {'prefix':c,'code_inputs':proof,'texture':TEXTURE,'raster':RASTER,'mirror':MIRROR,
  'font_to_raster_frame':0x1D4,'font_to_texture_entry_sp':0x2D8,'image_entry':0x4CDE10,'image_return':0x4CC0D2,
  'image_path':'data\\adv\\bin\\sc004.bin','image_slot':32,'image_path_buffer':PATH,
  'font_cleanup':{'function':'0x4d1bf0','handle_field':NODE+0x5C,'API_release':True,'stored_handle_cleared':False},
  'scope':'Name GDI/upload and natural image-loader entry; image loading not executed.'}

def expected_raster(before,measured,graphics,font_handle):
 name_rules();mem=memory_regions(before);v=mem[VM];o=TEXTURE_OFFSET;cfg=geometry(measured)
 if type(graphics)is not int or graphics<=0 or type(font_handle)is not int or not 0<font_handle<0xFFFFFFFF:raise ValueError('actual name graphics/font handle')
 if struct.unpack_from('<I3H',v,28)!=(252,0,30,20) or any(v[o:o+0x78]) or struct.unpack_from('<I',v,NODE_OFFSET+0x5C)[0]:raise ValueError('actual empty name texture parent')
 struct.pack_into('<I',v,NODE_OFFSET+0x5C,font_handle)
 struct.pack_into('<I',v,o+0x28,0);struct.pack_into('<I',v,o+0x4C,graphics);v[o+0x64:o+0x68]=b'\xff'*4
 struct.pack_into('<I',v,o+0x34,25);struct.pack_into('<2H',v,o+0x38,*cfg['texture_size']);struct.pack_into('<2H',v,o+0x40,*cfg['raster_size'])
 return {'after':regions(mem),**cfg}

def expected_complete(raster,texture_pointer,device,before_accounting):
 mem=memory_regions(raster['after']);v=mem[VM];o=TEXTURE_OFFSET;cfg=geometry(raster['measured'])
 if any(type(x)is not int or not 0<x<0xFFFFFFFF for x in (texture_pointer,device)) or type(before_accounting)is not int:raise ValueError('name real texture/device/accounting')
 if struct.unpack_from('<2I',v,o+0x2C)!=(0,0):raise ValueError('name empty pending native texture')
 width,height=[power_of_two(x) for x in cfg['texture_size']]
 struct.pack_into('<2I',v,o+0x28,device,texture_pointer);struct.pack_into('<2H',v,o+0x3C,width,height)
 struct.pack_into('<H',v,o+0x44,struct.unpack_from('<H',v,o+0x44)[0]|6)
 # Original caller selects first slot and scene row before executing the loader.
 for at,val in ((0x2C,736),(0x2E,214),(0x30,0),(0x34,4)):struct.pack_into('<H',v,NODE_OFFSET+at,val)
 struct.pack_into('<I',v,NODE_OFFSET+0x44,0x622758)
 return {'after':regions(mem),'texture_size':[width,height],'accounting_after':(before_accounting+width*height*2)&0xFFFFFFFF,
  'path':name_rules()['image_path'],'args':[PATH,32]}

def pending_texture(prefix):
 f=prefix['pending_font']['frames']['name']
 return {'sp':f-0x2D8,'ebp':f-0x1D4,'return_va':0x405779}

def pending_image(prefix):
 frames=prefix['pending_font']['frames'];resource=frames['layer']-120
 return {'va':0x4CDE10,'receiver':VM,'args':[PATH,32],'return_va':0x4CC0D2,
  'frames':{'resource':resource,'layer':frames['layer'],'handler':frames['handler'],'vm':frames['vm'],'sp':resource-116},'first_instruction_executed':False}

if __name__=='__main__':
 import sys
 sys.stdout.reconfigure(encoding='utf-8');print(report_text(name_rules()),end='')

"""Pinned character configuration and independent original name-font prefix."""
from tools.school_dialogue_confirmation_catalog import (
 ROOT, SOURCE, SOURCE_SHA256, BASE, VM, STACK, RETURN, REGIONS,
 memory_regions, regions, struct, hashlib, json, argparse, report_text,
 native_fixture as confirmation_fixture, compare_confirmation)
from tools.school_dialogue_wait_catalog import source_catalog as wait_catalog, script_layout, Cs, CS_ARCH_X86, CS_MODE_32

LAYER=5
NODE_OFFSET=0x6F60+LAYER*0xE0
OBJECT_OFFSET=0x430+LAYER*0xAB8
NODE=VM+NODE_OFFSET
OBJECT=VM+OBJECT_OFFSET
FONT_API=0xE300000

def source_catalog():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('character original image identity')
 script,layout=script_layout();op,size=struct.unpack_from('<2H',script,704)
 encoded=list(struct.unpack_from('<4I',script,708))
 if (op,size,encoded)!=(30,20,[0x20000008,0x20000004,0x20000000,0x2000001E]):raise ValueError('character selected command')
 config_at=0x624520+8*38;config=raw[config_at-BASE:config_at-BASE+38];w=list(struct.unpack('<19h',config))
 if w!=[5,254,368,1,0,736,214,308,400,715,491,1,855,529,23,13,695,154,5]:raise ValueError('character selected configuration')
 def string(at):
  if not BASE<=at<BASE+len(raw):raise ValueError('source string address')
  data=raw[at-BASE:at-BASE+256];end=data.find(b'\0')
  if end<0:raise ValueError('source bounded string')
  return data[:end]
 name_at=struct.unpack_from('<I',raw,0x621F2C-BASE+4*4)[0]
 resource_at=0x622668+4*60;resource_ptr=struct.unpack_from('<I',raw,resource_at-BASE)[0]
 pairs={0x4C62A9:('call','0x4cc600'),0x4C62CF:('call','0x4cc0f0'),0x4C62E1:('call','0x4cc3e0'),0x4C62FD:('call','0x4cc810'),
  0x4CC168:('call','0x4caf10'),0x4CC172:('call','0x4caff0'),0x4CC1D9:('call','0x4ca770'),
  0x4CA7C5:('call','dword ptr [0x5920a0]'),0x4CA7DC:('mov','eax, dword ptr [edx*4 + 0x621f2c]'),
  0x4CC6F1:('call','0x4ca720'),0x4CC728:('call','0x4ca130'),0x4CC732:('call','0x4ca0b0')}
 md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
 for at,pair in pairs.items():
  i=next(md.disasm(raw[at-BASE:at-BASE+16],at,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError('character source instruction '+hex(at))
  proof.append({'va':hex(at),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 return {'source_image_sha256':SOURCE_SHA256,'command':wait_catalog()['commands'][2],'encoded_operands':encoded,'operands':[v&0xFFFFFFF for v in encoded],
  'configuration':{'va':hex(config_at),'hex':config.hex(),'words':w},'layer':LAYER,'node':NODE,'text_object':OBJECT,
  'name':{'index':4,'pointer':name_at,'hex':string(name_at).hex(),'text_big5':string(name_at).decode('big5')},
  'image_dependency':{'table_row':hex(resource_at),'filename':string(resource_ptr).decode('ascii'),'directory':'data\\adv\\bin\\','resource_slot':32,'executed':False},
  'font_face_hex':string(0x5BF62C).hex(),'font_args':[20,0,0,0,700,0,0,0,1,5,0,0,0,0x5BF62C],
  'code_inputs':proof,'scope':'Original prefix only; name font/raster, image load, animation and GPU/world remain pending.'}

def expected_prefix(before):
 c=source_catalog();mem=memory_regions(before);v=mem[VM];n=NODE_OFFSET;o=OBJECT_OFFSET;w=c['configuration']['words']
 if struct.unpack_from('<I3H',v,28)!=(252,0,30,20):raise ValueError('character pending original opcode30 parent')
 initial=bytearray(0xE0);initial[0x34:0x38]=b'\xff'*4
 if v[n:n+0xE0]!=initial or any(v[o:o+0xAB8]):raise ValueError('character unused original layer required')
 struct.pack_into('<4I',v,0x9250,*c['operands'])
 stores={0:1,2:1,6:0,8:w[18],0xC:w[1],0xE:w[2],0x10:8,0x16:w[14],0x18:w[15],0x1A:w[16],0x1C:w[17],
  0x1E:w[7],0x20:w[8],0x30:w[4],0x40:32,0x42:33,0x4C:w[11],0x56:w[12],0x58:w[13]}
 for at,value in stores.items():struct.pack_into('<H',v,n+at,value)
 struct.pack_into('<H',v,o,24);v[o+4]=0;struct.pack_into('<H',v,o+6,12);v[o+10]=0
 # Original prologues: VM112; handler72; layer96; name328, plus saved registers/arguments.
 vm=STACK+0xFF00-4;handler=vm-112-28-4;layer=handler-72-12-12-8;name=layer-96-12-4-8;sp=name-328-12-56-4
 return {'after':regions(mem),'pending_font':{'va':FONT_API,'return_va':0x4CA7CB,'receiver':NODE,'args':c['font_args'],
  'frames':{'vm':vm,'handler':handler,'layer':layer,'name':name,'sp':sp},'name_argument':(NODE&0xFFFF0000)|4,'first_instruction_executed':False},
  'node_word_stores':stores}

if __name__=='__main__':
 import sys
 sys.stdout.reconfigure(encoding='utf-8')
 print(report_text(source_catalog()))

"""Pinned sc004 container, DX pixels and independent resource prefix rules."""
from tools.school_character_name_catalog import *

RESOURCE=ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/ADV/BIN/SC004.BIN'
RESOURCE_SHA='a4443ca63b9889503e35170da0c8b976a799c25ec3f0bd1b0f80dc97c38a6164'
HEAP=0x3C000000;HEAP_BYTES=0x100000;FILE_BUFFER=HEAP
ARRAY=HEAP+0x40020;RECORD=ARRAY+4;IMAGE_MIRROR=0x3D000000
FILE_API=0xE330000
FILE_IMPORTS={0x592214:('GetCurrentDirectoryA',8),0x5921EC:('CreateFileA',28),0x5921F0:('GetFileSize',8),0x5921E8:('ReadFile',20),0x592270:('CloseHandle',4)}

def parse_resource(raw):
 if not isinstance(raw,bytes) or len(raw)!=262168:raise ValueError('bounded original sc004 byte length')
 if struct.unpack_from('<3I',raw)!=(len(raw),1,12):raise ValueError('sc004 exact one-entry container')
 if struct.unpack_from('<6H',raw,12)!=(0x5844,2,256,512,256,512):raise ValueError('sc004 supported DX mode/geometry')
 return {'bytes':len(raw),'entries':1,'offset':12,'header_hex':raw[12:24].hex(),'format':25,'size':[256,512],
  'pixel_offset':24,'pixel_bytes':262144,'pixel_sha256':hashlib.sha256(raw[24:]).hexdigest()}

def resource():
 raw=RESOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=RESOURCE_SHA:raise ValueError('pinned original sc004 identity')
 return raw,parse_resource(raw)

def source_rules():
 raw,c=resource();src=SOURCE.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32)
 if hashlib.sha256(src).hexdigest()!=SOURCE_SHA256:raise ValueError('original image source identity')
 pairs={0x4CDE31:('call','0x42ae20'),0x4CDE85:('call','0x416790'),0x4CDE96:('mov','byte ptr [edx + ecx + 0x92a0], 1'),
  0x4CDEA8:('call','0x428ad0'),0x41F174:('call','0x56dda0'),0x4050AF:('call','0x403bd0'),0x4050CE:('call','0x4046f0'),
  0x42AC96:('call','dword ptr [0x5921ec]'),0x42AD07:('call','dword ptr [0x5921f0]'),0x42AD7C:('call','dword ptr [0x5921e8]'),0x42AD9F:('call','dword ptr [0x592270]')}
 proof=[]
 for at,pair in pairs.items():
  i=next(md.disasm(src[at-BASE:at-BASE+16],at,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError('original image instruction '+hex(at))
  proof.append({'va':hex(at),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 return {'source_image_sha256':SOURCE_SHA256,'resource_sha256':RESOURCE_SHA,'container':c,'code_inputs':proof,
  'heap':{'file_buffer':FILE_BUFFER,'array':ARRAY,'record':RECORD,'array_bytes':88,'kind':'declared finite emulator heap'},
  'resource_slot':32,'renderer_table_offset':0x844,'row_bytes':512,'rows':512,'scope':'Original resource loading and real fourth texture; GPU draw/world and animation remain later work.'}

def frames(parent):
 i=parent['pending_image']['frames']['sp']-4
 reg=i-104;ereg=reg-100;f090=ereg-104;f0e0=f090-112;entry=f0e0-160;dx=entry-128
 return {'image':i,'file_wrapper':i-100,'file_loader':i-204,'register':reg,'extended_register':ereg,'container_wrapper':f090,'container':f0e0,'entry':entry,'dx':dx,'texture_sp':dx-100}

def record_prefix():
 r=bytearray(84);struct.pack_into('<I2H',r,0x34,25,256,512);return bytes(r)

def expected_prefix(before):
 resource();mem=memory_regions(before);v=mem[VM]
 if struct.unpack_from('<I3H',v,28)!=(252,0,30,20) or v[0x92A0+32]!=0:raise ValueError('actual original unloaded image parent')
 return {'after':regions(mem),'record_hex':record_prefix().hex(),'table_hex':struct.pack('<2I',RECORD,1).hex()}

def expected_complete(before,device,texture):
 p=expected_prefix(before);mem=memory_regions(p['after']);mem[VM][0x92A0+32]=1;r=bytearray(record_prefix())
 if any(type(x)is not int or not 0<x<0xFFFFFFFF for x in (device,texture)):raise ValueError('actual image device/texture pointers')
 struct.pack_into('<2I',r,0x28,device,texture);struct.pack_into('<2H',r,0x3C,256,512);struct.pack_into('<H',r,0x44,2)
 return {'after':regions(mem),'record_hex':r.hex(),'table_hex':p['table_hex']}

def expected_pixels(initial,pitch):
 raw,_=resource()
 if type(pitch)is not int or not 512<=pitch<=4096 or pitch%2 or not isinstance(initial,bytes) or len(initial)!=pitch*512:raise ValueError('bounded actual image lock')
 out=bytearray(initial)
 for row in range(512):out[row*pitch:row*pitch+512]=raw[24+row*512:24+(row+1)*512]
 return bytes(out)

if __name__=='__main__':
 import sys
 sys.stdout.reconfigure(encoding='utf-8');print(report_text(source_rules()),end='')

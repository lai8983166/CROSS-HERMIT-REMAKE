"""Independent palette and full-pitch model of original 404150 BMP8 upload."""
import struct
from tools.terminal_battle_exit_contract import need,CODE

def indexed_bmp_image(buffer,offset,before,pitch,texture_width,texture_height,transparency=1,palette_offset=None):
 need(buffer[offset:offset+2]==b'BM','original indexed bitmap signature')
 width,height=struct.unpack_from('<ii',buffer,offset+18)
 planes,bpp=struct.unpack_from('<HH',buffer,offset+26)
 compression=struct.unpack_from('<I',buffer,offset+30)[0]
 need(width>0 and height>0 and (planes,bpp,compression)==(1,8,0),'original positive uncompressed BMP8 input')
 need(width<=texture_width<=1024 and height<=texture_height<=512 and texture_width&(texture_width-1)==0 and texture_height&(texture_height-1)==0,'source-sized power-of-two texture')
 need(pitch>=texture_width*2 and len(before)==pitch*texture_height,'entire actual native locked span including padding')
 palette_offset=offset+54 if palette_offset is None else palette_offset
 need(palette_offset>=0 and palette_offset+1024<=len(buffer),'all256 original palette reads remain inside owned complete file')
 palette=[buffer[palette_offset+i*4:palette_offset+i*4+3] for i in range(256)]
 table=[]
 for index,(blue,green,red) in enumerate(palette):
  value=0 if index==0 or transparency==1 and palette[index]==palette[0] else 0x8000|(red>>3)<<10|(green>>3)<<5|blue>>3
  table.append(struct.pack('<H',value))
 stride=1 if width==1 else (width+3)&~3
 pixels=offset+struct.unpack_from('<I',buffer,offset+10)[0]
 need(stride<=texture_width and pixels+stride*height<=len(buffer),'every original pixel and source padding read bounded')
 result=bytearray(before)
 for y in range(height):
  indices=buffer[pixels+(height-1-y)*stride:pixels+(height-y)*stride]
  converted=b''.join(table[index] for index in indices)
  result[y*pitch:y*pitch+len(converted)]=converted
 return bytes(result)

def original_palette_contract():
 from capstone import Cs,CS_ARCH_X86,CS_MODE_32
 md=Cs(CS_ARCH_X86,CS_MODE_32)
 expected={0x40429D:('cmp','dword ptr [ebp + 0xc], 1'),0x4042EC:('mov','word ptr [ecx*2 + 0x765520], 0'),0x404304:('sar','ecx, 3'),0x40430D:('shl','ecx, 0xa'),0x40431C:('sar','ebx, 3'),0x404325:('shl','ebx, 5'),0x404340:('or','ch, 0x80'),0x404353:('mov','word ptr [0x765520], 0'),0x404272:('cmp','edx, 1'),0x404277:('mov','dword ptr [ebp - 0x24], 1'),0x4043AD:('sub','edx, 1'),0x4043B0:('imul','edx, dword ptr [ebp - 0x24]'),0x4043D3:('mov','word ptr [eax + edx*2], cx'),0x40440A:('ret','0x10'),0x420A89:('sub','ecx, dword ptr [ebp - 8]'),0x420A92:('shr','edx, 2'),0x420A9B:('cmp','dword ptr [eax + 0x2e], 0'),0x420AA7:('mov','dword ptr [ecx + 0x2e], edx'),0x40495D:('cmp','dword ptr [ebp + 0x18], 1'),0x404967:('cmp','dword ptr [ebp + 0x20], 0'),0x40498E:('cmp','ecx, dword ptr [eax + 0x2e]'),0x4049C2:('cmp','dword ptr [ebp - 0x10], 0'),0x4049CB:('mov','eax, dword ptr [edx]'),0x4049D3:('mov','dword ptr [edx + ecx*4], eax')}
 for address,want in expected.items():
  decoded=next(md.disasm(CODE[address-0x400000:address-0x400000+16],address))
  need((decoded.mnemonic,decoded.op_str)==want,'original palette conversion instruction '+hex(address))
 return dict(original=0x404150,instruction_checks=len(expected),index0_transparent=True,equal_palette0_RGB_transparent=True,format='A1R5G5B5',bottom_up=True,source_stride_padding_written=True,full_native_pitch_padding_retained=True)


def bitmap_loader_palette(buffer,offset,replace_black,palette_override=0):
 """Original 4048D0 preprocessing before its 404150 conversion call."""
 need(palette_override==0,'only actual COMMON in-file palette branch')
 out=bytearray(buffer)
 # Original 420A40 is called before 4048D0 examines or rewrites the palette.
 bpp=struct.unpack_from('<H',out,offset+28)[0]
 if bpp in (4,8) and struct.unpack_from('<I',out,offset+46)[0]==0:
  pixel_offset=struct.unpack_from('<I',out,offset+10)[0]
  need(pixel_offset>=54,'original indexed header palette span')
  struct.pack_into('<I',out,offset+46,(pixel_offset-54)>>2)
 if replace_black==1:
  count=struct.unpack_from('<I',out,offset+46)[0]
  need(0<=count<=256 and offset+54+count*4<=len(out),'explicit original palette-count loop bound')
  key=bytes(out[offset+54:offset+58])
  for index in range(1,count):
   p=offset+54+index*4
   if out[p:p+3]==bytes(3):out[p:p+4]=key
 return bytes(out)

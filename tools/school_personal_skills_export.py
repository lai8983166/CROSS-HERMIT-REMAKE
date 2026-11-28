"""Personal-screen skill names, class slot bounds and original equip/replace writes."""
import hashlib
import json
import struct

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
from unicorn.x86_const import UC_X86_REG_EBP, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256

# These five active effects have battle commands and replay handlers.
NAME_OFFSETS = {11:0x1964, 20:0x1cfa, 31:0x21ae, 57:0x2ca2, 59:0x2dba}


def read_rules():
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('Changed original executable')
    text = (ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/YSTEXT/BIG5/SKILLEXP.YBC').read_bytes()
    if text[0x2108:text.index(0,0x2108)].decode('cp950')!='復原（使用）':raise ValueError('Changed initial recovery skill name')
    names = {str(i):text[p:text.index(0,p)].decode('cp950').split('（')[0] for i,p in NAME_OFFSETS.items()}
    return {'source_image_sha256':SOURCE_SHA256,'text_sha256':hashlib.sha256(text).hexdigest(),
            'names':names, 'slots':[image[0x2b2d88+64*i+3] for i in range(31)],
            'families':[image[0x2c2dc8+i*72+4] for i in range(85)],
            'incompatible':list(image[0x2e4158:0x2e4158+13]),
            'personal_menu_sha256':hashlib.sha256(image[0xae370:0xafb70]).hexdigest(),
            'eligibility_sha256':hashlib.sha256(image[0xb5c90:0xb5fc0]).hexdigest()}


def original_equipment(member, job, skill, slot, equipped, statuses, inventory=None):
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:raise ValueError('Changed original executable')
    cpu = Uc(UC_ARCH_X86, UC_MODE_32)
    cpu.mem_map(0x400000, (len(image)+4095)//4096*4096)
    cpu.mem_write(0x400000,image)
    cpu.mem_map(0x10000,0x4000)
    frame,stack,stop=0x11800,0x13800,0x10000
    char=0x7e17e8+member*0x4a0
    cpu.mem_write(char+6,struct.pack('<H',job))
    cpu.mem_write(char+0x52,struct.pack('<8H',*equipped))
    for i,v in enumerate(statuses):cpu.mem_write(char+0xb8+i*12,bytes([v]))
    def refresh():
        for index in range(1,85):
            cpu.mem_write(stack,struct.pack('<III',stop,char,index))
            cpu.reg_write(UC_X86_REG_ESP,stack)
            cpu.emu_start(0x4b5c90,stop,count=1250)
            if cpu.reg_read(UC_X86_REG_EIP)!=stop:raise ValueError('Original eligibility did not finish')

    refresh()
    if not 0<=slot<image[0x2b2d88+job*64+3] or cpu.mem_read(char+0xb8+(skill-1)*12,1)!=bytes([3]):
        raise ValueError('Personal screen does not admit this slot or skill')
    cpu.mem_write(0x7d6a3c,struct.pack('<H',skill))
    cpu.reg_write(UC_X86_REG_EBP,frame)
    for offset,value in [(8,slot),(0x38,member),(0x40,char),(0x50,1)]:
        cpu.mem_write(frame-offset,struct.pack('<I',value))
    # Start at the source write after confirming status=3 and the personal screen is editable.
    cpu.mem_write(frame-0x34,struct.pack('<I',skill))
    cpu.emu_start(0x4aedc8,0x4aedf1,count=12)
    if cpu.reg_read(UC_X86_REG_EIP)!=0x4aedf1 or cpu.mem_read(char+0xb8+(skill-1)*12,1)!=b'\x06':
        raise ValueError('Original drag did not select the skill')
    cpu.emu_start(0x4ae72f,0x4ae7cd,count=42)
    if cpu.reg_read(UC_X86_REG_EIP)!=0x4ae7cd:raise ValueError('Original slot write did not finish')
    refresh()
    result=(list(struct.unpack('<8H',cpu.mem_read(char+0x52,16))),list(cpu.mem_read(char+0xb8,84*12)[::12]))
    if inventory is None:return result
    level,flags=inventory
    cpu.mem_write(char+0x50,bytes([level]))
    cpu.mem_write(0x7aacac,struct.pack('<360H',*flags))
    for item in range(1,361):
        cpu.mem_write(stack,struct.pack('<III',stop,char,item))
        cpu.reg_write(UC_X86_REG_ESP,stack)
        cpu.emu_start(0x4b5af0,stop,count=1200)
        if cpu.reg_read(UC_X86_REG_EIP)!=stop:raise ValueError('Original item refresh did not finish')
    return (*result,list(struct.unpack('<360H',cpu.mem_read(0x7aacac,720))))


if __name__=='__main__':
    data=read_rules()
    for previous in [0,59]:
        states=[3]*84
        if previous:states[previous-1]=6
        slots,result=original_equipment(13,10,57,0,[previous]+[0]*7,states)
        if slots!=[57]+[0]*7 or result[56]!=6:raise ValueError('Original slot case failed')
    (ROOT/'prototype/data/school_personal_skills.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')

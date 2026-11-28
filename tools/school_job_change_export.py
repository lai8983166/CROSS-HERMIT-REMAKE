"""Export post-transfer equipment rules and an original-instruction regression case."""
import hashlib
import json
import struct

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
from unicorn.x86_const import UC_X86_REG_EBP, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256


def build(played_case=None):
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('source differs')
    cpu = Uc(UC_ARCH_X86, UC_MODE_32)
    cpu.mem_map(0x400000, (len(image)+4095)//4096*4096)
    cpu.mem_write(0x400000, image)
    cpu.mem_map(0x10000, 0x4000)
    character, stack, stop = 0x11000, 0x13800, 0x10000

    def call(address, index):
        cpu.mem_write(stack, struct.pack('<III', stop, character, index))
        cpu.reg_write(UC_X86_REG_ESP, stack)
        cpu.emu_start(address, stop, count=1200)
        if cpu.reg_read(UC_X86_REG_EIP) != stop or cpu.reg_read(UC_X86_REG_ESP) != stack+12:
            raise ValueError('incomplete equipment eligibility call')

    def statuses():
        return list(cpu.mem_read(character+0xb8, 84*12)[::12])

    def set_statuses(values):
        for i, status in enumerate(values):
            cpu.mem_write(character+0xb8+i*12, bytes([status]))

    classes = []
    for job in range(1, 31):
        cpu.mem_write(character+6, struct.pack('<h', job))
        set_statuses([3]*84)
        for skill in range(1, 85):
            call(0x4b5c90, skill)
        classes.append({'item_types': [i for i in range(15) if image[0x2e45f8+job*15+i]],
                        'skills': [i for i, s in enumerate(statuses(),1) if s==3]})
    items = [[struct.unpack_from('<H',image,0x2d511a+i*56)[0],image[0x2d5122+i*56]] for i in range(1,361)]
    # Exercise signed/untouched status values, both ownership categories and nonzero owner bits.
    before = {'job': 4, 'level_50': 19, 'equipped_items':[6,100]+[0]*6, 'equipped_skills':[3,22]+[0]*6,
              'skill_statuses': [i%7 for i in range(84)], 'item_flags':[0x8011 | ((i%5)<<8) for i in range(360)]}
    target=14
    if played_case is not None:
        before=played_case['before']
        target=played_case['target']
        if not 1<=target<=30:raise ValueError('invalid played job')
    cpu.mem_write(character+6, struct.pack('<H',target))
    cpu.mem_write(character+0x50, bytes([before['level_50']]))
    cpu.mem_write(character+0x52, struct.pack('<16H',*before['equipped_skills'],*before['equipped_items']))
    cpu.mem_write(0x7aacac, struct.pack('<360H',*before['item_flags']))
    set_statuses(before['skill_statuses'])
    frame=stack-0x100
    cpu.reg_write(UC_X86_REG_EBP,frame)
    cpu.mem_write(frame+8,struct.pack('<I',character))
    cpu.mem_write(frame+0x14,b'\x01')
    cpu.emu_start(0x4b687f,0x4b699b,count=600)
    if cpu.reg_read(UC_X86_REG_EIP)!=0x4b699b:raise ValueError('incomplete unequip loop')
    for item in range(1,361):call(0x4b5af0,item)
    for skill in range(1,85):call(0x4b5c90,skill)
    after={'job':target,'level_50':before['level_50'],'equipped_items':list(struct.unpack('<8H',cpu.mem_read(character+0x62,16))),
           'equipped_skills':list(struct.unpack('<8H',cpu.mem_read(character+0x52,16))),
           'skill_statuses':statuses(),'item_flags':list(struct.unpack('<360H',cpu.mem_read(0x7aacac,720)))}
    return {'source_image_sha256':SOURCE_SHA256,'classes':classes,'items':items,
            'case':{'before':before,'target':target,'after':after}}


if __name__=='__main__':
    path=ROOT/'prototype/data/school_job_change.json'
    path.write_text(json.dumps(build(),separators=(',',':'))+'\n',encoding='utf8',newline='\n')

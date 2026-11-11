"""Own hardware PIT/PIC pending IRQ restored before STI, then #DB/RF path."""
import argparse,struct
from pathlib import Path
from devtools import terminal_tcg_ram_event_probe_v3 as runner


base_image=runner.image
def image(root,point):
    raw,expected=base_image(root,'before_call');elf=bytearray(raw)
    w=lambda x:struct.pack('<I',x)
    def out(port,value):return bytes((0xb0,value,0xe6,port))
    code=bytes.fromhex('66b810008ed88ec08ed0bc00401000')
    for vector,handler in ((1,0x100400),(32,0x100500)):
        gate=struct.pack('<HHBBH',handler&0xffff,8,0,0x8e,handler>>16)
        for offset in (0,4):code+=bytes.fromhex('c705')+w(0x101000+vector*8+offset)+gate[offset:offset+4]
    code+=bytes.fromhex('0f011d')+w(0x100828)
    code+=b'\xb8'+w(0x100305)+bytes.fromhex('0f23c0b8010400000f23f8')
    # Architectural PIC initialization; IRQ0 only, vector 0x20. PIT one-shot.
    for port,value in ((0x20,0x11),(0xa0,0x11),(0x21,0x20),(0xa1,0x28),
                       (0x21,4),(0xa1,2),(0x21,1),(0xa1,1),(0x21,0xfe),(0xa1,0xff),
                       (0x43,0x30),(0x40,0x10),(0x40,0)):
        code+=out(port,value)
    # Poll real IRR while IF=0. The saved source must contain HARD pending.
    code+=bytes.fromhex('b00ae620e420a80174f6')
    code+=out(0xe9,ord('S'))
    code+=b'\xe9'+w(0x1002f0-(0x100120+len(code)+5))
    if len(code)>0x1d0:raise ValueError('fixture overlap')
    elf[4096+0x120:4096+0x120+len(code)]=code
    elf[4096+0x2f0:4096+0x2f7]=bytes.fromhex('fb90e909000000')
    handler=bytes.fromhex('60ff0504201000b051e6e9b020e62061cf')
    elf[4096+0x500:4096+0x500+len(handler)]=handler
    expected.update(a=0x1002f0,point='pending_irq')
    return bytes(elf),expected


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('binary','firmware','output'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();a.point='pending_irq';runner.image=image
    raise SystemExit(not runner.run(a))

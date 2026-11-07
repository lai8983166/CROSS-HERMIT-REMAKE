"""Original workroom input/exit contract; synthetic x86 only, never native input."""
import argparse
import hashlib
import json
from pathlib import Path
import struct

from devtools import terminal_menu_transition_contract as menu

RECTANGLE=(847,726,141,30)
TARGET=(917,741)
CHECKS={
    0x49FEA1:('push','0x1e'),0x49FEA3:('push','0x8d'),
    0x49FEA8:('push','0x2d6'),0x49FEAD:('push','0x34f'),
    0x49FEBB:('call','0x4d5ec0'),0x49FEC0:('mov','eax, dword ptr [ebp - 0x10]'),
    0x49FEC3:('and','eax, 1'),0x49FEC8:('je','0x49ff45'),
    0x49FF3D:('mov','word ptr [ebp - 0x18], 4'),
    0x49FF52:('call','0x422360'),0x49FFDA:('mov','ax, word ptr [ebp - 0x18]'),
    0x4D5F6A:('mov','eax, dword ptr [edx + 0x1990]'),
    0x4D5FA4:('ret','0x14'),
    0x4A15CB:('call','0x49fd50'),0x4A15D3:('mov','word ptr [edx + 0x30], ax'),
    0x4A163A:('call','0x422360'),0x4A163F:('movsx','eax, word ptr [0x7a4e62]'),
    0x4A1648:('jne','0x4a1676'),0x4A164A:('mov','word ptr [0x7a4e62], 1'),
    0x4A1653:('push','9'),0x4A1655:('push','0x5a090c'),
    0x4A165F:('call','0x4ce210'),0x4A1664:('push','6'),
    0x4A166F:('call','0x439e30'),0x4A167F:('push','9'),
    0x4A168A:('call','0x439e30'),0x4A169F:('ret','4'),
}


def original_hit(raw,x,y,held=0,pressed=0,released=0,auxiliary=0):
    """Run original 4D5EC0, 4D5B70 and balanced-stack check through RET 14h."""
    from unicorn.x86_const import UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_ECX
    menu.need(all(type(v) is int and -32768<=v<=32767 for v in (x,y)), 'signed original cursor words')
    menu.need(all(type(v) is int and 0<=v<=7 for v in (held,pressed,released,auxiliary)), 'bounded masks')
    u=menu._guest(raw);u.mem_map(0x30000000,0x1000)
    out=0x3200C000
    u.mem_write(0x3200196C,struct.pack('<ii',x,y))
    for offset,value in ((0x198C,held),(0x1990,pressed),(0x199C,released),(0x19A0,auxiliary)):
        u.mem_write(0x32000000+offset,struct.pack('<I',value))
    u.mem_write(out,b'\xA5'*16)
    u.mem_write(0x31008000,struct.pack('<7I',0x30000000,out,*RECTANGLE,0x12345678))
    u.reg_write(UC_X86_REG_ECX,0x7E1110)
    result=menu._run(u,0x4D5EC0,{0x30000000})
    menu.need(u.reg_read(UC_X86_REG_ESP)==0x31008018 and u.reg_read(UC_X86_REG_EBP)==0x31009000,
              'actual RET 14h preserves caller frame and stack')
    data=bytes(u.mem_read(out,16));h,p,a,inside=struct.unpack_from('<IIIH',data)
    menu.need(data[14:]==b'\xA5'*2,'output boundary untouched')
    result.update(held=h,pressed=p,auxiliary=a,inside=inside,exit_press_observed=bool(p&1))
    return result


def contract(raw):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_32
    menu.authenticate(raw);decoder=Cs(CS_ARCH_X86,CS_MODE_32);checks=[]
    for address,expected in CHECKS.items():
        ins=next(decoder.disasm(raw[address-menu.BASE:address-menu.BASE+15],address))
        menu.need((ins.mnemonic,ins.op_str)==expected,'original workroom instruction '+hex(address))
        checks.append(dict(address=address,hex=ins.bytes.hex(),instruction=ins.mnemonic+' '+ins.op_str))
    menu.need(struct.unpack_from('<I',raw,0x5A0904-menu.BASE)[0]==0x4A1570,'original workroom vtable')
    chapter=raw[0x5A090C-menu.BASE:0x5A090C-menu.BASE+64].split(b'\0',1)[0]
    menu.need(chapter==b'Data\\Adv\\dat\\CH002.ybc','original first workroom exit script')
    return dict(source_sha256=menu.SOURCE_SHA,checks=checks,rectangle=list(RECTANGLE),target=list(TARGET),
        rectangle_edges='inclusive signed-16-bit deltas; unlike title menu strict edges',
        input='GAME+1990 pressed bit0; held and GAME+199C release alone do not select',
        ready=dict(vtable=0x5A0904,node_state_offset=0x30,node_state=1,
            wait_return=0x49FF57,selector_caller=0x4A15D0,selector_this_offset=-4),
        selected_state=4,first_exit=dict(flag=0x7A4E62,script=chapter.decode('ascii'),script_next_event=9,event=6),
        later_exit_event=9,native_workroom_input_implemented=False,native_workroom_exit_observed=False,
        full_battle_exit_accepted=False,synthetic_memory_is_not_native_source=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True,type=Path);args=parser.parse_args()
    result=contract(menu.read_source());result['implementation_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with args.out.open('x',encoding='utf-8',newline='\n') as stream:
        stream.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':main()

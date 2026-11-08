"""Original school task-1 UI contract. Bounded synthetic x86; no native input.

Date/empty ledger in local probes are declared inputs, never native mutations.
The probes do not establish that a running school has these initial conditions.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

from devtools import terminal_menu_transition_contract as original

DEPART_RECT = (223, 42, 303, 31)
DEPART_TARGET = (374, 57)
CONFIRM_RECT = (405, 390, 102, 29)
CONFIRM_TARGET = (456, 404)
RANGES = {
    'task_registration': (0x4A17B0, 0x4A191E),
    'task_ledger_insert': (0x4A9D90, 0x4AA060),
    'task_list_and_mandatory_selection': (0x4A1C70, 0x4A1FF0),
    'school_initialization': (0x4A5A60, 0x4A5F40),
    'input_dispatch': (0x4A3CA0, 0x4A4620),
    'modal_dispatch': (0x4A6F90, 0x4A7C40),
    'selector': (0x4A7C40, 0x4A7D30),
    'readiness': (0x4A7D30, 0x4A8140),
    'rating': (0x4A95F0, 0x4A9AB0),
    'button_selection': (0x4AA4B0, 0x4AA590),
    'button_collision': (0x4D5A60, 0x4D5FA7),
    'group_callback': (0x4AB7A0, 0x4ABA2F),
    'producer_callback': (0x4B8FF0, 0x4B9111),
    'prepared_roster': (0x4A6A10, 0x4A6F90),
}
CHECKS = {
    0x4A18E4: ('call', '0x4a9d90'),
    0x4A1E87: ('mov', 'word ptr [0x7a55fa], 1'),
    0x4A1EA9: ('mov', 'word ptr [0x7aab0a], 1'),
    0x4A1F1B: ('mov', 'word ptr [0x7aab16], ax'),
    0x4A5CB7: ('call', '0x4a17b0'),
    0x4A5D1C: ('call', '0x4a1c70'),
    0x4A5D24: ('call', '0x4a5f40'),
    0x4A454B: ('mov', 'dl, byte ptr [0x7d6a26]'),
    0x4A4588: ('mov', 'word ptr [edx + 0x76c6], 0xe'),
    0x4A714D: ('call', '0x4d5ec0'),
    0x4A7162: ('and', 'edx, 1'),
    0x4A71A9: ('mov', 'word ptr [ecx + 0x76c6], 3'),
    0x4A71B5: ('mov', 'word ptr [edx + 0x30], 1'),
    0x4A7574: ('mov', 'word ptr [eax + 0x76c4], 0'),
    0x4A7580: ('mov', 'word ptr [ecx + 0x7950], 8'),
    0x4A7CE5: ('call', '0x422360'),
    0x4A7D06: ('call', '0x4a1920'),
    0x4A7D0E: ('mov', 'ax, word ptr [edx + 0x7950]'),
    0x4A7ECC: ('call', '0x4a95f0'),
    0x4A7F0F: ('cmp', 'dword ptr [ebp - 0xa0], 2'),
    0x4AB7EC: ('call', '0x4a7c40'),
    0x4AB8A5: ('call', '0x4a6a10'),
    0x4AB989: ('push', '0xa'),
    0x4AB994: ('call', '0x439e30'),
    0x4ABA17: ('call', '0x422360'),
    0x4ABA2C: ('ret', '4'),
    0x4B9052: ('call', '0x4da860'),
    0x4B90DA: ('push', '0x10'),
    0x4B90E5: ('call', '0x439e30'),
    0x4B90F9: ('call', '0x422360'),
    0x4B910E: ('ret', '4'),
}


def _call(u, address, arguments=()):
    from unicorn.x86_const import UC_X86_REG_ESP, UC_X86_REG_EBP, UC_X86_REG_ECX
    u.reg_write(UC_X86_REG_ESP, 0x31008000)
    u.reg_write(UC_X86_REG_EBP, 0x31009000)
    u.reg_write(UC_X86_REG_ECX, 0x32000000)
    u.mem_write(0x31008000, struct.pack('<'+'I'*(1+len(arguments)), 0x30000000, *arguments))
    result = original._run(u, address, {0x30000000}, 200000)
    original.need(u.reg_read(UC_X86_REG_EBP) == 0x31009000, 'original caller BP preserved')
    result['return_esp'] = u.reg_read(UC_X86_REG_ESP)
    return result


def _guest(raw):
    u = original._guest(raw)
    u.mem_map(0x30000000, 4096)
    return u


def original_task_registration(raw, month=4, week=1, already_registered=False):
    """Execute original register/list functions with a declared empty local ledger."""
    original.need(type(month) is int and 1 <= month <= 15, 'bounded month')
    original.need(type(week) is int and 0 <= week <= 5, 'bounded week')
    original.need(type(already_registered) is bool, 'registered flag type')
    u = _guest(raw)
    u.mem_write(0x7A55FA, bytes(0x56A))
    u.mem_write(0x7AAB08, bytes(0x14))
    u.mem_write(0x7A528E, struct.pack('<HH', month, week))
    if already_registered:
        u.mem_write(0x7A55FD, b'\x01')
    calls = [_call(u, a) for a in (0x4A17B0, 0x4A1C70)]
    original.need(all(c['return_esp'] == 0x31008004 for c in calls), 'original cdecl stack')
    count = int.from_bytes(u.mem_read(0x7A5B62, 2), 'little')
    original.need(count <= 100, 'bounded ledger output')
    return dict(calls=calls, month=month, week=week, ledger_count=count,
                ledger_hex=bytes(u.mem_read(0x7A5662, count*16)).hex(),
                gate=int.from_bytes(u.mem_read(0x7A55FA, 2), 'little'),
                selected=int.from_bytes(u.mem_read(0x7AAB0A, 2), 'little'),
                task_id=int.from_bytes(u.mem_read(0x7AAB16, 2), 'little'))


def original_depart_hit(raw, x, y, *, held=0, pressed=0, released=0):
    """Run original full control lookup, collision and pressed-edge selection."""
    from unicorn.x86_const import UC_X86_REG_EAX
    original.need(all(type(v) is int and -32768 <= v <= 32767 for v in (x,y)), 'cursor words')
    original.need(all(type(v) is int and 0 <= v <= 7 for v in (held,pressed,released)), 'mouse masks')
    u = _guest(raw)
    u.mem_write(0x3200196C, struct.pack('<ii', x,y))
    for offset,value in ((0x198C,held),(0x1990,pressed),(0x199C,released)):
        u.mem_write(0x32000000+offset, struct.pack('<I',value))
    result = _call(u, 0x4AA4B0)
    result['control'] = struct.unpack('<h', struct.pack('<H',u.reg_read(UC_X86_REG_EAX)&0xFFFF))[0]
    original.need(result['return_esp'] == 0x31008004, 'control lookup original cdecl return')
    return result


def original_confirm_hit(raw, x, y, *, held=0, pressed=0, released=0):
    original.need(all(type(v) is int and -32768 <= v <= 32767 for v in (x,y)), 'cursor words')
    original.need(all(type(v) is int and 0 <= v <= 7 for v in (held,pressed,released)), 'mouse masks')
    u = _guest(raw)
    u.mem_write(0x3200196C, struct.pack('<ii', x,y))
    for offset,value in ((0x198C,held),(0x1990,pressed),(0x199C,released)):
        u.mem_write(0x32000000+offset, struct.pack('<I',value))
    out = 0x3200F000
    u.mem_write(out,b'\xA5'*16)
    result = _call(u,0x4D5EC0,(out,*CONFIRM_RECT))
    h,p,a,hit=struct.unpack('<IIIH',bytes(u.mem_read(out,14)))
    original.need(bytes(u.mem_read(out+14,2))==b'\xA5'*2,'output write bound')
    original.need(result['return_esp']==0x31008018,'original RET14h')
    result.update(held=h,pressed=p,auxiliary=a,hit=hit,selected=bool(hit and p&1))
    return result


def contract(raw):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_32
    original.authenticate(raw);decoder=Cs(CS_ARCH_X86,CS_MODE_32);checks=[]
    for a,expected in CHECKS.items():
        ins=next(decoder.disasm(raw[a-original.BASE:a-original.BASE+15],a))
        original.need((ins.mnemonic,ins.op_str)==expected,'school instruction '+hex(a))
        checks.append(dict(address=a,hex=ins.bytes.hex(),instruction=ins.mnemonic+' '+ins.op_str))
    table=raw[0x61B628-original.BASE:0x61B63A-original.BASE]
    original.need(struct.unpack_from('<3h',table)==(50,0,0),'depart original control descriptor')
    original.need(struct.unpack_from('<4h',raw,0x625558-original.BASE)==DEPART_RECT,'depart original rectangle')
    task=raw[0x73BFD0-original.BASE:0x73C0D0-original.BASE]
    original.need(task[:20].hex()=='0101040100010401000000000000010101000100','original task1 template')
    registration=original_task_registration(raw)
    original.need((registration['ledger_count'],registration['gate'],registration['selected'],registration['task_id'])==(1,1,1,1),'original task1 registration')
    return dict(kind='static_original_school_preparation_contract',source_sha256=original.SOURCE_SHA,
        source_bytes=original.SOURCE_BYTES,checks=checks,
        ranges=[dict(name=n,start=a,end_exclusive=b,sha256=original.hashlib.sha256(raw[a-original.BASE:b-original.BASE]).hexdigest()) for n,(a,b) in RANGES.items()],
        task1=dict(pointer=0x73BFD0,bytes=256,sha256=hashlib.sha256(task).hexdigest(),header20_hex=task[:20].hex(),month=4,week=1,rounds=1,scene_id=1,selection_word=1),
        local_registration_probe=registration,
        input=dict(edge='GAME+1990 bit0 pressed; held/release alone do not select',
            departure=dict(rectangle=DEPART_RECT,target=DEPART_TARGET,control=0,accepted_integer_cursor_bounds=[222,41,524,71],collision='original 2x2 cursor strict center-distance test, not generic inclusive rectangle'),
            confirmation=dict(rectangle=CONFIRM_RECT,target=CONFIRM_TARGET,collision='original generic inclusive signed-16 rectangle')),
        wait=dict(group_vtable=0x5A0A40,companion_ui_vtable=0x5A0C18,return_address=0x4A7CEA,
            selector_caller=0x4AB7F1,selector_this_offset=-4,worker_ancestors=[0x421F8A,0x56E183],
            fields_u16={'+30':0,'+76C0':1,'+76C4':1,'+76C6':'0 departure; 14 confirmation','+7950':0},
            main_event='MAIN+2C eight bytes; event idle; both school tasks and same-owner TLS required'),
        required_live_data=[dict(pointer=0x7A528E,bytes=4,meaning='month/week 4/1'),
            dict(pointer=0x7A55FA,bytes=2,meaning='mandatory gate1'),
            dict(pointer=0x7A5B62,bytes=2,meaning='ledger count; bound before reading rows'),
            dict(pointer=0x7A5662,bytes=16,meaning='first task1 ledger row: ID+0,type+3,category+5,disabled+6'),
            dict(pointer=0x7AAA12,bytes=140,meaning='five classes stride28: teacher+0,activity+3,students+16 four i16'),
            dict(pointer=0x7AAB08,bytes=20,meaning='selected/task view; selected+2, taskID+14'),
            dict(pointer=0x7D6A26,bytes=1,meaning='actual readiness returned by original4A7D30')],
        readiness='five original ratings must be 0 or2, at least one2; teacher101 and students3/4/9 in first adventure class suffice only with task selected; rating is not a persistent global',
        path=['original4A17B0 inserts dated task1','original4A1C70 selects mandatory task1','original4A5F40 organizes initial class','actual press depart changes mode0 to14','actual press confirm changes mode14 to3 and node+30 to1','original fade clears+76C4 and sets selection8','original4A1920 commits;4A6A10 prepares rounds','school UI observes99 and exits; group publishes10','original producer4B8FF0 loads scene and publishes16','original451080/451170 constructs battle'],
        prepared=dict(base=0x7A5294,task_offset=0,cursor_offset=2,count_offset=4,round_base=0x7A529A,round_stride=112,scene_offset=110,student_count_offset=94,teacher_count_offset=106),
        ownership='event10 producer publishes16 before its final yield/RET4; this original transient overlap is legal, unlike host-injected roots',
        native_school_preparation_observed=False,native_battle_handoff_observed=False,
        original_wait_return_accepted=False,full_battle_exit_accepted=False,
        restrictions=['no native execution or input in this module','no runtime writes or fabricated task selection/results','synthetic original CPU probes are not native provenance or full cleanup proof'])


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);args=p.parse_args()
    result=contract(original.read_source());result['implementation_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with args.out.open('x',encoding='utf-8',newline='\n') as stream:
        stream.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':main()

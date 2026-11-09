"""Original battle exit ownership endpoints and bounded synthetic x86 probes.

No process is opened, no native input is sent, and no historical source changes.
The PTD probe substitutes explicitly declared free/TLS leaf results; it proves
only original argument selection and control flow, never actual heap release.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'analysis/hermit_game.exe'
SOURCE_SHA = '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
BASE = 0x400000
PTD_NESTED = (0x24, 0x28, 0x30, 0x38, 0x40, 0x44)
PTD_STATIC = 0x761D68
FREE_SITES = (0x575491,0x5754AB,0x5754C5,0x5754DF,0x5754F9,0x575513,0x575530,0x57553E)
RANGES = {
    'scene_callback': (0x451670,0x4519A3),
    'scene_destructor': (0x451470,0x451666),
    'controller_cleanup': (0x465E60,0x465F81),
    'controller_destructor': (0x465BC0,0x465E5A),
    'scene_base_destructor': (0x439F80,0x43A021),
    'task_base_destructor': (0x4222D0,0x4222FD),
    'scheduler_dispatch': (0x421850,0x421BE3),
    'scheduler_unlink': (0x421D50,0x421E99),
    'manager_destructor': (0x4215F0,0x421657),
    'manager_cancel_all': (0x421BF0,0x421C64),
    'forced_node_stop_not_normal_exit': (0x422090,0x422289),
    'worker_callback_tail': (0x421F50,0x422026),
    'CRT_thread_entry_and_end': (0x56E110,0x56E225),
    'CRT_TLS_and_PTD_free': (0x5753B0,0x575557),
    'game_free_wrapper': (0x428AD0,0x428B59),
    'CRT_free_debug': (0x56F3B0,0x56F80B),
    'CRT_heap_free': (0x5787E0,0x578926),
    'scene_vtable': (0x59A430,0x59A438),
}
CHECKS = {
    0x451774: ('call','0x465e60'),
    0x4517D6: ('call','0x439e30'),
    0x4519A0: ('ret','4'),
    0x421F88: ('call','dword ptr [eax]'),
    0x421FBC: ('call','0x4225a0'),
    0x421FC1: ('push','4'),
    0x421FC6: ('call','0x422560'),
    0x421FD4: ('call','dword ptr [0x592228]'),
    0x421FED: ('call','dword ptr [0x59222c]'),
    0x42201F: ('push','0'),
    0x422021: ('call','0x56e1e0'),
    0x56E1ED: ('call','dword ptr [0x761980]'),
    0x56E1F3: ('call','0x5753b0'),
    0x5753C5: ('call','dword ptr [0x592154]'),
    0x56E20F: ('call','0x575450'),
    0x57553E: ('call','0x56f3b0'),
    0x57554F: ('call','dword ptr [0x5921a8]'),
    0x56E21B: ('call','dword ptr [0x5921a4]'),
    0x421AE2: ('call','dword ptr [0x592268]'),
    0x421B1C: ('cmp','dword ptr [ebp - 0x14], 0x103'),
    0x421B48: ('mov','ecx, dword ptr [eax + 0x1c]'),
    0x421B4C: ('call','dword ptr [0x592270]'),
    0x421B97: ('call','0x421d50'),
    0x421E09: ('mov','dword ptr [eax], edx'),
    0x421BB2: ('call','dword ptr [edx + 4]'),
    0x421BC6: ('call','0x428ad0'),
    0x451650: ('call','0x451470'),
    0x451505: ('call','0x428ad0'),
    0x451574: ('call','dword ptr [0x5920c4]'),
    0x451597: ('call','0x465e60'),
    0x4515D9: ('call','0x465bc0'),
    0x465BFC: ('call','0x465e60'),
    0x451609: ('call','0x439f80'),
    0x43A001: ('call','0x4222d0'),
    0x465E99: ('call','0x428ad0'),
    0x465EA4: ('mov','dword ptr [ecx + 0x117c40], 0'),
    0x465F22: ('call','dword ptr [0x5920c4]'),
    0x465F32: ('mov','dword ptr [edx + 0xdb80c], 0'),
    0x465F54: ('call','dword ptr [0x5920c4]'),
    0x465F64: ('mov','dword ptr [eax + 0xdb810], 0'),
    0x421620: ('call','dword ptr [0x592280]'),
    0x421639: ('call','dword ptr [0x592270]'),
    0x4220DD: ('call','dword ptr [0x592260]'),
    0x56F480: ('call','dword ptr [0x762130]'),
    0x56F4B3: ('jmp','0x56f805'),
    0x56F4F2: ('sub','ecx, 0x20'),
    0x56F6F9: ('and','ecx, 2'),
    0x56F6FE: ('jne','0x56f7dc'),
    0x56F7D2: ('call','0x5787e0'),
    0x56F7DF: ('mov','dword ptr [ecx + 0x14], 0'),
    0x578879: ('call','dword ptr [0x592258]'),
    0x5788FA: ('call','dword ptr [0x592258]'),
    0x57890F: ('call','dword ptr [0x592258]'),
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def authenticate(raw):
    need(len(raw) == 5980160 and sha(raw) == SOURCE_SHA, 'fixed unpacked original image identity')


def source_contract(raw):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
    authenticate(raw)
    decoder = Cs(CS_ARCH_X86, CS_MODE_32)
    instructions = []
    for address, expected in CHECKS.items():
        ins = next(decoder.disasm(raw[address-BASE:address-BASE+15],address),None)
        need(ins is not None and (ins.mnemonic,ins.op_str)==expected,'original cleanup instruction '+hex(address))
        instructions.append(dict(address=address,hex=ins.bytes.hex(),mnemonic=ins.mnemonic,operands=ins.op_str))
    need(struct.unpack_from('<II',raw,0x59A430-BASE)==(0x451670,0x451630),'actual scene callback/destructor vtable')
    for site in FREE_SITES:
        ins = next(decoder.disasm(raw[site-BASE:site-BASE+15],site))
        need((ins.mnemonic,ins.op_str)==('call','0x56f3b0'),'all PTD free sites')
    close_sites = []
    for lo,hi in ((0x421850,0x421BE3),(0x451470,0x451666),(0x439F80,0x43A021),(0x4222D0,0x4222FD)):
        close_sites.extend(i.address for i in decoder.disasm(raw[lo-BASE:hi-BASE],lo)
                           if i.mnemonic=='call' and i.op_str=='dword ptr [0x592270]')
    need(close_sites==[0x421B4C],'normal scheduler and task destructor chain has only node-event CloseHandle')
    direct_calls = {}
    for name in ('controller_cleanup','controller_destructor','scene_destructor'):
        lo,hi=RANGES[name]
        direct_calls[name]=[dict(site=i.address,target=i.op_str)for i in decoder.disasm(raw[lo-BASE:hi-BASE],lo)if i.mnemonic=='call']
    return dict(source=dict(path='analysis/hermit_game.exe',bytes=len(raw),sha256=sha(raw),mapping='offset=VA-0x400000'),
                checked_instructions=instructions,
                ranges=[dict(name=name,start=lo,end=hi,bytes=hi-lo,sha256=sha(raw[lo-BASE:hi-BASE]))for name,(lo,hi)in RANGES.items()],
                resource_direct_calls=direct_calls,normal_owner_close_sites=close_sites)


def observation_plan():
    return dict(
        required_API_slots={
            '0x592154':'TlsGetValue','0x5921A8':'TlsSetValue','0x5921A4':'ExitThread',
            '0x592268':'GetExitCodeThread','0x592270':'CloseHandle',
            '0x592228':'ResetEvent','0x59222C':'SetEvent','0x59226C':'WaitForSingleObject',
            '0x592234':'EnterCriticalSection','0x592238':'LeaveCriticalSection',
            '0x592280':'DeleteCriticalSection','0x592258':'HeapFree',
            '0x5920C4':'DeleteObject','0x592260':'TerminateThread (reject on normal path)',
        },
        normal_path=[
            'Worker451774 calls controller465E60 before completion polling451783 and retreat event1 publication4517D6.',
            'Scene4519A0 RET4 reaches worker421F8A. Worker clears flags, sets4, resets node event and signals manager, then calls56E1E0(0) at422021.',
            'CRT56E1E0 optionally invokes[761980], looks up PTD5753B0, calls575450, then ExitThread(0) at56E21B. Normal421F50 does not return to56E183.',
            'Manager421AE2 polls node+20 until exit!=259, closes only node+1C at421B4C, clears flags, unlinks421D50, optionally calls vtable+4 then frees node428AD0.',
            'Scene vtable59A430+4=451630 calls451470; scene/controller destructors call465E60 again. Cleanup must tolerate observed zero resource pointers without counting nonexistent repeated frees.',
        ],
        endpoints=[
            dict(name='controller_cleanup',entry=0x465E60,returns=[0x451779,0x45159C,0x465C01],owner='worker first; MAIN destructor later',capture='CTRL=this; full inputs/output changes of all descendants, pointers+117C40/+DB80C/+DB810, GDI/COM/CRT resource ledger'),
            dict(name='callback_return',address=0x421F8A,owner='original worker',capture='same callback frame/this/argument, full CPU/stack, scene return EAX; do not require56E183'),
            dict(name='completion_flags',address=0x421FCB,owner='original worker',capture='node flags=4 under actual manager lock; successful ResetEvent/SetEvent and same manager/node handles'),
            dict(name='endthread',entry=0x56E1E0,address=0x422021,owner='original worker',capture='argument0, optional runtime exit pointer761980 and called body if nonzero'),
            dict(name='PTD_lookup',address=0x5753CB,owner='same OS TID and TEB',capture='TlsGetValue actual return equals pre-exit PTD; full116 bytes and nested allocation identities; reject unexpected new PTD allocation path'),
            dict(name='PTD_release',entry=0x575450,free_sites=list(FREE_SITES),owner='same worker CRT heap/lock9',capture='each nonnull nested pointer, +50 sentinel exception, original type2 frees and actual allocator branch/outcome; PTD headers before invalidation'),
            dict(name='TLS_clear',call=0x57554F,after=0x575555,owner='same worker',capture='TlsSetValue(index,0) actual success and same TEB slot zero before ExitThread; original ignores BOOL'),
            dict(name='thread_exit',call=0x56E21B,owner='same worker',capture='ExitThread argument0 and OS exit event/signaled retained duplicate. No normal return from ExitThread; distinguish access to already-freed PTD'),
            dict(name='scheduler_exit_poll',call=0x421AE2,after=0x421AE8,owner='MAIN',capture='actual GetExitCodeThread BOOL and out DWORD; require0, original only rejects259'),
            dict(name='node_event_close',call=0x421B4C,after=0x421B52,owner='MAIN',capture='argument=node+1C; actual CloseHandle BOOL; retain original object identity to avoid numerical handle reuse ambiguity'),
            dict(name='unlink',entry=0x421D50,write=0x421E09,after=0x421B9C,owner='MAIN',capture='all32 bucket heads/full bounded chain before+after; preceding link receives removed.next; removed.next remains unchanged'),
            dict(name='auto_delete',call=0x421BB2,after=0x421BB5,free=0x421BC6,owner='MAIN',capture='node+28 !=0; actual vtable+4 target451630; original destructor descendants and final node CRT allocation release; no post-free node dereference'),
            dict(name='manager_lifetime',delete_lock=0x421620,close_event=0x421639,owner='MAIN at complete runtime shutdown',capture='manager+100 lock and+118 event stay owned across successor menu; do not close at battle retirement'),
        ],
        PTD=dict(bytes=116,nested_nonnull_offsets=list(PTD_NESTED),conditional_pointer_offset=0x50,
                 static_pointer_not_freed=PTD_STATIC,free_block_type=2,TLS_index_global=0x761BC0,
                 nested_pointers_not_zeroed_by_575450=True,TLS_clear_result_checked_by_original=False),
        allocator=dict(debug_header_user_minus=0x20,debug_flags=0x7619C0,allocation_hook=0x762130,
                       debug_list=[0x80A430,0x80A438],current_bytes=0x80A43C,heap=0x80AB28,heap_mode=0x80AB2C,
                       warning='Hook may reject free. Debug flag&2 retains a marked-free block. Heap modes2/3 may use small-block free instead of HeapFree. Authenticate and capture actual branch; a call to_free_dbg or dead fill alone is not physical release.'),
        supplemental_thread_owner=dict(required=True,original_handle='node+20',normal_original_close=False,
            scope='Static normal completion path leaks the original CRT thread handle until explicit owner closure or process teardown; this report does not prove guest-v5 handle-table state.',
            protocol='Record same-process original handle and immutable TID/object identity before node free; retain a query duplicate. After observed normal exit0 and scheduler completion, close that exact original remote handle only through an explicitly authorized same-owner cleanup capability, separately recording result. Closing the observer duplicate alone does not close original node+20. Avoid raw numeric late-close after potential reuse.',
            original_node_event='Already closed by original421B4C; never supplement-close it blindly.',
            manager_event='Remains live for successor tasks; only original manager destructor closes it.'),
        capture_strategy=[
            'Start continuous same-guest observation before retreat; authenticate executable ranges, OS modules/exports/IAT, original CRT heap/TLS ownership and resource ledger before first release.',
            'Correlate worker and MAIN events by actual PID/TID, monotonic sequence and objects. Worker SetEvent and MAIN GetExitCodeThread may interleave before worker PTD free finishes.',
            'Collect call entry plus post-call CPU/arguments/out-memory and actual API result; sparse stop-point samples do not establish successful waits or complete cleanup.',
            'Debugger/trace must preserve original bytes/registers and disclose its intervention. Do not mutate fields, synthesize events, call roots, or introduce success stubs in native sources.',
            'Keep one bounded incremental trace with content deduplication; preserve required original bytes and checksums, not repeated full memory. Full formal CPU/RAM/ABI/digest coverage remains mandatory.',
            'Treat422090/592260 TerminateThread or manager forced-cancel traversal as a separate failure/cancellation path, never natural worker cleanup.',
        ],
        unknown_dependencies=[
            'Runtime optional CRT exit callback[761980], allocator hook[762130], debug flags/heap mode and nested PTD allocation state require live evidence.',
            'All controller/scene destructor descendant GDI/COM/resource releases need continuous full-state evidence; this contract lists direct calls, not a completed descendant-resource proof.',
            'Original thread handle leakage must be checked dynamically against object identity; static absence of closure is not a current native handle-table snapshot.',
            'Successful OS waits, scheduler interleavings, full PTD/resource lifetime, successor semantics and two fresh complete independent replay cases remain unproved.',
        ])


def ptd_probe(raw, nested=None, *, locale=PTD_STATIC, tls_index=2, argument_is_null=False, lookup_is_null=False, tls_success=True):
    """Execute575450 only, replacing its external calls with declared results."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_ESP, UC_X86_REG_EIP, UC_X86_REG_EAX
    authenticate(raw)
    nested = {} if nested is None else dict(nested)
    need(set(nested)<=set(PTD_NESTED),'only original nested PTD slots')
    need(all(type(x)is int and 0<=x<=0xFFFFFFFF for x in [locale,tls_index,*nested.values()]),'uint32 probe inputs')
    u=Uc(UC_ARCH_X86,UC_MODE_32)
    u.mem_map(0x575000,0x1000);u.mem_write(0x575000,raw[0x175000:0x176000])
    u.mem_map(0x761000,0x1000);u.mem_write(0x761BC0,struct.pack('<I',tls_index))
    ptd=0x20000000;sp=0x30000800;stop=0x10000000
    for address in (ptd,sp&~0xFFF,stop):u.mem_map(address,0x1000)
    data=bytearray(116)
    for offset,value in nested.items():struct.pack_into('<I',data,offset,value)
    struct.pack_into('<I',data,0x50,locale);u.mem_write(ptd,bytes(data))
    u.mem_write(sp,struct.pack('<II',stop,0 if argument_is_null else ptd));u.reg_write(UC_X86_REG_ESP,sp)
    calls=[];instructions=[0]
    def hook(machine,address,size,user):
        instructions[0]+=1
        stack=machine.reg_read(UC_X86_REG_ESP)
        if address in FREE_SITES:
            pointer,block=struct.unpack('<II',machine.mem_read(stack,8))
            calls.append(dict(site=address,kind='declared_free_boundary',pointer=pointer,block_type=block))
            machine.reg_write(UC_X86_REG_EIP,address+5)
        elif address==0x57546C:
            index=struct.unpack('<I',machine.mem_read(stack,4))[0]
            result=0 if lookup_is_null else ptd
            calls.append(dict(site=address,kind='declared_TLS_lookup',index=index,result=result))
            machine.reg_write(UC_X86_REG_ESP,stack+4);machine.reg_write(UC_X86_REG_EAX,result)
            machine.reg_write(UC_X86_REG_EIP,address+6)
        elif address==0x57554F:
            index,value=struct.unpack('<II',machine.mem_read(stack,8))
            calls.append(dict(site=address,kind='declared_TLS_clear',index=index,value=value,result=int(tls_success)))
            machine.reg_write(UC_X86_REG_ESP,stack+8);machine.reg_write(UC_X86_REG_EAX,int(tls_success))
            machine.reg_write(UC_X86_REG_EIP,address+6)
    u.hook_add(UC_HOOK_CODE,hook);u.emu_start(0x575450,stop,count=500)
    need(u.reg_read(UC_X86_REG_EIP)==stop and u.reg_read(UC_X86_REG_ESP)==sp+4,'bounded original PTD cdecl return')
    need(bytes(u.mem_read(ptd,116))==bytes(data),'PTD pointer fields not cleared by original selector')
    return dict(accepted=False,native_execution=False,synthetic_leaf_results=True,actual_heap_release_proved=False,
                instructions=instructions[0],calls=calls,PTD=ptd,PTD_bytes_unchanged=True,
                TLS_result_checked_by_original=False,return_reached=True)


def unlink_probe(raw, position=0, bucket=0):
    """Execute original unlink/search and ABI checker; no leaf substitutions."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EBX,UC_X86_REG_ESI,UC_X86_REG_EDI,UC_X86_REG_ECX,UC_X86_REG_EAX,UC_X86_REG_EIP
    authenticate(raw);need(position in (0,1,2) and type(bucket)is int and 0<=bucket<32,'bounded existing-node unlink fixture')
    u=Uc(UC_ARCH_X86,UC_MODE_32)
    for address,size in ((0x421000,0x1000),(0x56C000,0x1000)):
        u.mem_map(address,size);u.mem_write(address,raw[address-BASE:address-BASE+size])
    manager=0x20000000;nodes=[manager+0x200+i*0x80 for i in range(3)];sp=0x30000800;stop=0x10000000
    for address in (manager,sp&~0xFFF,stop):u.mem_map(address,0x1000)
    memory=bytearray(0x400)
    for i,node in enumerate(nodes):
        offset=node-manager;memory[offset:offset+0x80]=b'\xA5'*0x80
        struct.pack_into('<I',memory,offset+0xC,nodes[i+1]if i<2 else 0)
    struct.pack_into('<I',memory,bucket*8,nodes[0]);u.mem_write(manager,bytes(memory))
    u.mem_write(sp,struct.pack('<II',stop,nodes[position]));u.reg_write(UC_X86_REG_ESP,sp);u.reg_write(UC_X86_REG_ECX,manager)
    preserved={UC_X86_REG_EBP:0x13572468,UC_X86_REG_EBX:0x12345678,UC_X86_REG_ESI:0x23456789,UC_X86_REG_EDI:0x3456789A}
    for reg,value in preserved.items():u.reg_write(reg,value)
    count=[0]
    def hook(machine,address,size,user):count[0]+=1
    u.hook_add(UC_HOOK_CODE,hook);u.emu_start(0x421D50,stop,count=4000)
    need(u.reg_read(UC_X86_REG_EIP)==stop and u.reg_read(UC_X86_REG_ESP)==sp+8 and u.reg_read(UC_X86_REG_EAX)==0,'original unlink ret4/return0')
    need(all(u.reg_read(reg)==value for reg,value in preserved.items()),'original unlink preserved registers')
    link=bucket*8 if position==0 else nodes[position-1]-manager+0xC
    expected=bytearray(memory);struct.pack_into('<I',expected,link,nodes[position+1]if position<2 else 0)
    actual=bytes(u.mem_read(manager,len(memory)));need(actual==expected,'only predecessor or bucket link changed, removed node bytes preserved')
    return dict(accepted=False,native_execution=False,synthetic_memory=True,leaf_substitutions=False,
                instructions=count[0],bucket=bucket,position=position,changed_link=manager+link,
                removed_next_preserved=True,ABI_preserved=True,before_sha256=sha(memory),after_sha256=sha(actual))


def build(raw):
    return dict(schema_version=1,kind='terminal_exit_cleanup_static_and_local_contract',accepted=False,
                native_execution=False,full_cleanup_proved=False,formal_terminal_boundary_advanced=False,
                analyzer_sha256=sha(Path(__file__).read_bytes()),
                contract=source_contract(raw),observation_plan=observation_plan(),
                local_probes=dict(PTD=ptd_probe(raw,{o:0x21000000+i*0x100 for i,o in enumerate(PTD_NESTED)}),
                                  unlink=[unlink_probe(raw,pos,bucket)for pos,bucket in ((0,0),(1,31),(2,7))]))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();out=args.out.resolve()
    need(out.is_relative_to((ROOT/'analysis').resolve())and not out.exists(),'fresh bounded analysis report')
    payload=(json.dumps(build(SOURCE.read_bytes()),ensure_ascii=False,indent=2)+'\n').encode('utf8')
    need(len(payload)<65536,'small cleanup contract report')
    with out.open('xb')as stream:stream.write(payload)
    print(json.dumps(dict(path=str(out),bytes=len(payload),sha256=sha(payload),accepted=False,native_execution=False)))


if __name__=='__main__':main()

"""Fixed original-byte startup retirement contract. No native process access.

The bounded Unicorn check executes only the counter/dispatch blocks, with
synthetic local memory. It is a branch regression, never a native lifetime proof.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
SOURCE_BYTES = 5980160
IMAGE_BASE = 0x400000
THRESHOLD = 0x3F4C
CHECKS = {
    0x5061CA: ('mov', 'byte ptr [edx + 0x28], 1'),
    0x506218: ('call', '0x4216c0'),
    0x506268: ('mov', 'dword ptr [eax], 0x5caa48'),
    0x5063C3: ('push', '0x3c'),
    0x5063C5: ('push', '1'),
    0x5063CD: ('call', '0x415480'),
    0x50649E: ('mov', 'dword ptr [ebp - 0xc], 0'),
    0x5064D3: ('call', '0x525060'),
    0x525080: ('mov', 'byte ptr [eax + 0x30], 0'),
    0x506692: ('mov', 'ecx, dword ptr [ebp - 0xc]'),
    0x506695: ('add', 'ecx, 1'),
    0x506698: ('mov', 'dword ptr [ebp - 0xc], ecx'),
    0x506718: ('mov', 'dl, byte ptr [ecx + 0x30]'),
    0x506722: ('ja', '0x50a026'),
    0x50672D: ('mov', 'al, byte ptr [ecx + 0x50a183]'),
    0x506733: ('jmp', 'dword ptr [eax*4 + 0x50a11f]'),
    0x50A00D: ('cmp', 'dword ptr [ebp - 0x80], 0x3f4c'),
    0x50A014: ('je', '0x50a018'),
    0x50A01B: ('mov', 'byte ptr [ecx + 0x30], 0x64'),
    0x50A01F: ('jmp', '0x50a026'),
    0x50A021: ('jmp', '0x50a104'),
    0x50A02B: ('call', '0x422360'),
    0x50A03C: ('and', 'eax, 1'),
    0x50A043: ('jmp', '0x50a0ff'),
    0x50A048: ('jmp', '0x50655f'),
    0x50A04D: ('push', '0x3c'),
    0x50A04F: ('call', '0x4db230'),
    0x50A057: ('call', '0x4db270'),
    0x50A065: ('call', '0x422360'),
    0x50A071: ('call', '0x422360'),
    0x50A07B: ('call', '0x422360'),
    0x50A08C: ('call', '0x41e500'),
    0x50A091: ('push', '0xa'),
    0x50A09F: ('call', '0x41f4e0'),
    0x50A0E6: ('call', '0x464d30'),
    0x50A0ED: ('push', '1'),
    0x50A0F8: ('call', '0x439e30'),
    0x50A104: ('jmp', '0x50a04d'),
    0x50A11C: ('ret', '4'),
    0x421F88: ('call', 'dword ptr [eax]'),
    0x421F8A: ('cmp', 'esi, esp'),
    0x421FC1: ('push', '4'),
    0x421FC6: ('call', '0x422560'),
    0x421FD4: ('call', 'dword ptr [0x592228]'),
    0x421FED: ('call', 'dword ptr [0x59222c]'),
    0x42201F: ('push', '0'),
    0x422021: ('call', '0x56e1e0'),
    0x56E180: ('call', 'dword ptr [edx + 0x48]'),
    0x56E184: ('call', '0x56e1e0'),
    0x56E20F: ('call', '0x575450'),
    0x56E21B: ('call', 'dword ptr [0x5921a4]'),
    0x57553E: ('call', '0x56f3b0'),
    0x57554F: ('call', 'dword ptr [0x5921a8]'),
    0x421AA9: ('and', 'ecx, 4'),
    0x421AE2: ('call', 'dword ptr [0x592268]'),
    0x421B1C: ('cmp', 'dword ptr [ebp - 0x14], 0x103'),
    0x421B4C: ('call', 'dword ptr [0x592270]'),
    0x421B97: ('call', '0x421d50'),
    0x421BB2: ('call', 'dword ptr [edx + 4]'),
    0x421BC6: ('call', '0x428ad0'),
    0x439EAC: ('mov', 'dword ptr [ecx + 0x20], edx'),
    0x439EB2: ('mov', 'dword ptr [eax + 0x1c], 1'),
    0x49E053: ('call', '0x49e2b0'),
    0x49E30B: ('call', '0x45e8d0'),
    0x49E4B8: ('call', '0x49e540'),
    0x49E60F: ('call', '0x4217c0'),
    0x49E64E: ('call', '0x415610'),
    0x415667: ('call', 'dword ptr [0x592440]'),
    0x41571C: ('call', 'dword ptr [0x592284]'),
    0x415859: ('call', '0x415930'),
    0x4158E2: ('mov', 'eax, dword ptr [ecx + 0xb1f0]'),
    0x415967: ('call', '0x415990'),
}
RANGES = (
    (0x506150, 0x506280), (0x5063A0, 0x50673A),
    (0x50A007, 0x50A1E8), (0x525060, 0x525084),
    (0x421F50, 0x422026), (0x56E110, 0x56E225),
    (0x575450, 0x575557), (0x421A9B, 0x421BD0),
    (0x4217C0, 0x421850), (0x421D50, 0x421E20),
    (0x439E30, 0x439EE4), (0x49E044, 0x49E092),
    (0x49E2B0, 0x49E537), (0x49E540, 0x49E845),
    (0x415480, 0x415A90),
)


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def authenticate(raw):
    need(len(raw) == SOURCE_BYTES and sha(raw) == SOURCE_SHA,
         'fixed original image identity')


def source_contract(raw):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
    authenticate(raw)
    decoder = Cs(CS_ARCH_X86, CS_MODE_32)
    instructions = []
    for address, expected in CHECKS.items():
        ins = next(decoder.disasm(raw[address-IMAGE_BASE:address-IMAGE_BASE+15], address), None)
        need(ins is not None and (ins.mnemonic, ins.op_str) == expected,
             'original instruction at ' + hex(address))
        instructions.append(dict(address=address, hex=ins.bytes.hex(),
                                 mnemonic=ins.mnemonic, operands=ins.op_str))
    table = struct.unpack_from('<25I', raw, 0x50A11F-IMAGE_BASE)
    selectors = raw[0x50A183-IMAGE_BASE:0x50A1E8-IMAGE_BASE]
    need(table[selectors[0]] == 0x50673A and table[selectors[22]] == 0x50A007
         and table[selectors[100]] == 0x50A021, 'startup stage dispatch')
    events = struct.unpack_from('<25I', raw, 0x49E4D3-IMAGE_BASE)
    need(events[1] == 0x49E30B, 'menu event dispatch')
    return dict(
        format='terminal-startup-handoff-static-v1',
        source=dict(path='analysis/hermit_game.exe',bytes=len(raw),sha256=sha(raw)),
        instructions=instructions,
        ranges=[dict(start=a,end=b,sha256=sha(raw[a-IMAGE_BASE:b-IMAGE_BASE])) for a,b in RANGES],
        startup=dict(factory=0x506150, callback=0x5063A0, vtable=0x5CAA48,
            stage_offset=0x30, counter_from_callback_ebp=-12, this_from_callback_ebp=-4,
            initial_counter=0, initial_stage=0, threshold=THRESHOLD,
            threshold_stage=22, terminating_stage=100,
            dispatch=[dict(stage=s,selector=v,target=table[v]) for s,v in enumerate(selectors)],
            threshold_rule='Equality only at stage22. Counter16204 sets stage100 and still yields; next ordinary iteration increments to16205 and dispatches natural tail.',
            alternate_exit='game+1990 bit0 after the ordinary wait also enters50A04D. No input alone does not prove which edge was taken.',
            initial_state_rule='50649E clears counter;5064D3 calls525060, whose525080 clears stage. Do not attribute this to malloc or the base constructor.'),
        clock=dict(timing_game_start=0xB17C,timing_bytes=0x7C,
            rate_selector_offset=0xB17C,frequency_qword_offset=0xB188,
            enabled_offset=0xB1D0,catch_up_limit_offset=0xB1F0,
            nominal_qpc_microseconds={'default':16666,'1':33333,'2':50000,'3':66666},
            fallback_milliseconds={'default':16,'1':33,'2':50,'3':66},
            explanation='Counter advances once per resumed startup loop. MAIN4217C0 then415610 uses QPC or timeGetTime to pace frames;415930/415990 wait when ahead. Startup415480(1,60) sets catch-up/skip limit60, not a60Hz rate. Initialization, audio polling, focus and scheduling add wall time; no fixed wall-clock deadline proves retirement.'),
        original_order=[
            'stage22 equality sets100; ordinary yield; next dispatch case100 enters50A04D',
            'audio fade4DB230(60), poll4DB270 with yields, two further yields',
            '41E500 audio action;41F4E0(game+844,10) releases group10; ten464D30 embedded object calls',
            '439E30(MAIN+10,1) publishes MAIN+30 event1 and MAIN+2C pending1;callback RET4',
            '421F8A callback return;clear task flags,set4,ResetEvent(node+1C),SetEvent(manager+118)',
            '421F50 calls56E1E0(0) itself;575450 frees PTD and clears TLS;ExitThread(0)',
            'MAIN manager observes completion4,GetExitCodeThread!=STILL_ACTIVE,CloseHandle(node+1C),unlink421D50;auto-delete destructor then428AD0',
            'manager frame returns to outer49E053 loop; next49E2B0 dispatch event1 calls45E8D0 and clears pending',
        ],
        critical_distinctions=[
            '421F8A is the normal callback return.56E183 is the generic CRT callback return and is not on the normal421F50 path.',
            'Event1 publication precedes startup thread termination; menu construction follows manager termination polling and unlink on MAIN. Pending1 alone does not certify retirement.',
            'Manager accepts any non259 exit code, not only0; observer must independently require normal exit0 and a signaled duplicated original worker handle.',
            '32 buckets are singly linked: head at bucket+0,next at node+0C. Bucket+4 is not a proven tail;node+10 is not a previous pointer.',
            'Task flags4 and eventual absence are not evidence of every intermediate API, PTD free, TLS clear, destructor, or resource release.',
            'Absence in sparse samples cannot prove no transient overlap. Static unmodified MAIN ordering supports a qualified handoff observation, not a complete instruction trace.',
            'Original global8097A0 is not guaranteed cleared after startup deletion; do not dereference it after graph retirement or require zero.',
        ],
        required_observations=[
            'Fixed source and live code/IAT identities before and after; authenticated collector and backend; exact private process/Job lifetime.',
            'Coherent suspended snapshots of all32 bucket heads and every bounded node, rejecting cycles/duplicates/foreign manager owners.',
            'Same startup node/worker PID,TID,original handle and duplicated query/synchronize handle; full contexts and stack bounds; TLS PTD116 bytes binds callback421F50 and node.',
            'Callback frame return421F8A,frame-local this==registered startup,counter>=16204 and stage100 observed before retirement; preserve source bytes of locals.',
            'Original worker handle becomes signaled with GetExitCodeThread0; sampling after WM_CLOSE or forced shutdown cannot establish pre-cleanup retirement.',
            'Startup absent, sole menu callback45EB90 registered with same manager, pending0 stable interval; reject observed startup/menu overlap or unrelated tasks.',
            'Mouse/input samples and no host input/calls/writes; acknowledge unsampled external input cannot be excluded by sparse reads.',
            'Pool10/90 identities,renderer boundaries and thread/handle cleanup recorded with limited claims; full resource lifecycle needs additional evidence.',
        ],
        acceptance=dict(native_execution=False,native_handoff_observed=False,
            full_instruction_trace=False,PTD_cleanup_observed=False,
            resource_lifetime_repaired=False,battle_natural_exit=False,
            complete_battle_accepted=False,formal_terminal_boundary_advanced=False))


def local_counter_dispatch(raw, counter, stage):
    """Execute two original basic blocks; stop before any call or OS boundary."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_EBP, UC_X86_REG_EIP
    authenticate(raw)
    need(type(counter) is int and 0 <= counter <= 0xFFFFFFFF, 'counter uint32')
    need(type(stage) is int and 0 <= stage <= 255, 'stage byte')
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.mem_map(0x506000, 0x1000)
    uc.mem_write(0x506000, raw[0x106000:0x107000])
    uc.mem_map(0x50A000, 0x1000)
    uc.mem_write(0x50A000, raw[0x10A000:0x10B000])
    uc.mem_map(0x1000000, 0x2000)
    bp, node = 0x1000800, 0x1001000
    uc.reg_write(UC_X86_REG_EBP, bp)
    uc.mem_write(bp-12, struct.pack('<I', counter))
    uc.mem_write(bp-4, struct.pack('<I', node))
    uc.mem_write(node+0x30, bytes([stage]))
    visited = []
    stops = {0x50A026,0x50A04D,0x50673A}
    targets = struct.unpack_from('<25I', raw, 0x10A11F)
    stops.update(set(targets)-{0x50A007,0x50A021})
    def hook(machine,address,size,user):
        visited.append(address)
        if address in stops:
            machine.emu_stop()
    uc.hook_add(UC_HOOK_CODE, hook)
    uc.emu_start(0x506692,0x50669B,count=4)
    need(uc.reg_read(UC_X86_REG_EIP)==0x50669B, 'counter block stop')
    uc.emu_start(0x506713,0xFFFFFFFF,count=40)
    end = uc.reg_read(UC_X86_REG_EIP)
    need(end in stops, 'bounded dispatch stop')
    return dict(counter=struct.unpack('<I',uc.mem_read(bp-12,4))[0],
        stage=uc.mem_read(node+0x30,1)[0],stop=end,instructions=visited,
        synthetic_local_fixture=True,native_lifetime_proved=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args()
    raw = (ROOT/'analysis/hermit_game.exe').read_bytes()
    report = source_contract(raw)
    report['local_regressions'] = [local_counter_dispatch(raw,c,s) for c,s in
        [(THRESHOLD-2,22),(THRESHOLD-1,22),(THRESHOLD,100),(THRESHOLD,22),(0,0)]]
    blob = (json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    need(len(blob)<65536,'contract evidence budget')
    need(not args.out.exists(),'immutable output already exists')
    args.out.write_bytes(blob)
    print(json.dumps(dict(path=str(args.out),bytes=len(blob),sha256=sha(blob))))


if __name__ == '__main__':
    main()

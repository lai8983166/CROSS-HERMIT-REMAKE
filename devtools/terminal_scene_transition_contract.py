"""Read-only original scene-transition contract; never opens a native process.

The three remote setup roots do not retire an existing scene worker.  This
module authenticates the relevant original instructions and summarizes bounded
existing task graphs.  It does not certify an execution or a repaired lifetime.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
SCRIPT_SHA = 'dfeffff8e6a7e1582797af89c9836058596b65b2fe91049f2466754a8a86eae0'
SOURCE_BYTES = 5980160
STARTUP_VTABLE = 0x5CAA48
SCENE_VTABLE = 0x59A430
MENU_VTABLE = 0x59B060
MAX_PACKED = 8 * 1024 * 1024
MAX_RAW = 32 * 1024 * 1024
CHECKS = {
    0x49E39E: ('call', '0x451080'),
    0x49E30B: ('call', '0x45e8d0'),
    0x439EAC: ('mov', 'dword ptr [ecx + 0x20], edx'),
    0x439EB2: ('mov', 'dword ptr [eax + 0x1c], 1'),
    0x49E5CD: ('call', '0x40db90'),
    0x49E5DE: ('call', '0x40dc80'),
    0x49E60F: ('call', '0x4217c0'),
    0x49E6D9: ('call', '0x40e330'),
    0x42182A: ('call', '0x421850'),
    0x42192B: ('call', 'dword ptr [0x59226c]'),
    0x50A036: ('mov', 'eax, dword ptr [edx + 0x1990]'),
    0x50A03C: ('and', 'eax, 1'),
    0x50A043: ('jmp', '0x50a0ff'),
    0x50A091: ('push', '0xa'),
    0x50A09F: ('call', '0x41f4e0'),
    0x50A0ED: ('push', '1'),
    0x50A0F8: ('call', '0x439e30'),
    0x50A11C: ('ret', '4'),
    0x4CCB6B: ('mov', 'edx, dword ptr [ecx + 0x1990]'),
    0x4CD030: ('and', 'eax, 7'),
    0x45EBBD: ('call', '0x45ebf0'),
    0x45EC53: ('push', '0x5a'),
    0x45EC5F: ('call', '0x416790'),
    0x451B73: ('push', '0x5a'),
    0x451B7F: ('call', '0x416790'),
    0x41F11F: ('call', '0x41f4e0'),
    0x41F13D: ('call', '0x428a40'),
    0x41F548: ('call', '0x403730'),
    0x41F566: ('call', '0x41f2a0'),
    0x41F2EF: ('call', '0x428ad0'),
    0x41F57A: ('mov', 'dword ptr [eax], 0'),
    0x41F583: ('mov', 'dword ptr [ecx + 4], 0'),
    0x45EAD3: ('call', '0x41f480'),
    0x41F4BF: ('call', '0x41f4e0'),
    0x4C4EFC: ('call', '0x4cade0'),
    0x4CAE00: ('mov', 'word ptr [eax + 0x16], 0'),
    0x4CAD77: ('call', '0x408e30'),
    0x408065: ('mov', 'dword ptr [ecx + 0x50], eax'),
    0x40EA05: ('mov', 'eax, dword ptr [edx + 0x2c]'),
    0x40E244: ('call', 'dword ptr [eax + 0xf4]'),
    0x463321: ('call', '0x439e30'),
    0x42187B: ('and', 'eax, 2'),
    0x421880: ('jne', '0x421bce'),
    0x422583: ('or', 'ecx, dword ptr [ebp + 8]'),
    0x422589: ('mov', 'dword ptr [edx + 4], ecx'),
    0x4225C0: ('xor', 'eax, 0xffffffff'),
    0x4225C9: ('and', 'edx, eax'),
    0x422397: ('call', '0x422560'),
    0x422407: ('call', 'dword ptr [0x59226c]'),
    0x4220DD: ('call', 'dword ptr [0x592260]'),
    0x45F013: ('mov', 'eax, dword ptr [edx + 0x199c]'),
    0x45ED12: ('call', '0x439e30'),
    0x49F549: ('call', '0x439e30'),
    0x4B9052: ('call', '0x4da860'),
    0x4B90E5: ('call', '0x439e30'),
}
RANGES = (
    (0x439E30, 0x439EE2), (0x49E2B0, 0x49E4D3),
    (0x49E598, 0x49E6DE), (0x4217C0, 0x421939),
    (0x50A026, 0x50A11F), (0x4CCB30, 0x4CCB85),
    (0x4CCFE2, 0x4CD04F), (0x45EB90, 0x45ED9C),
    (0x451B10, 0x451BE6), (0x41F0E0, 0x41F290),
    (0x41F2A0, 0x41F331), (0x41F480, 0x41F59D),
    (0x45EA50, 0x45EB36), (0x4C4EB0, 0x4C4F21),
    (0x4CADE0, 0x4CAF01), (0x4CABD0, 0x4CADC0),
    (0x40804A, 0x408112), (0x40E9F3, 0x40EA12),
    (0x40E210, 0x40E24D), (0x463250, 0x4633ED),
    (0x422090, 0x422289), (0x422360, 0x422434), (0x422560, 0x42260A),
    (0x45EFB0, 0x45F0CB), (0x49F4E0, 0x49F55F), (0x4B9034, 0x4B90FE),
)


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def source_contract(raw, script):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
    need(len(raw) == SOURCE_BYTES and sha(raw) == SOURCE_SHA, 'fixed original source identity')
    need(len(script) == 5568 and sha(script) == SCRIPT_SHA, 'fixed T0004 identity')
    decoder = Cs(CS_ARCH_X86, CS_MODE_32)
    instructions = []
    for address, expected in CHECKS.items():
        row = next(decoder.disasm(raw[address-0x400000:address-0x400000+15], address), None)
        need(row is not None and (row.mnemonic, row.op_str) == expected,
             'original instruction at ' + hex(address))
        instructions.append(dict(address=address, hex=row.bytes.hex(), mnemonic=row.mnemonic,
                                 operands=row.op_str))
    commands = []
    for pc, opcode, size in ((154,44,4),(158,17,6),(164,50,4),(168,51,4),(172,44,4)):
        row = script[452+pc:452+pc+size]
        need(struct.unpack_from('<HH', row) == (opcode,size), 'T0004 command boundary')
        commands.append(dict(pc=pc, opcode=opcode, size=size, hex=row.hex()))
    need(script[614:616] == b'\x03\x00', 'text3 argument')
    table = struct.unpack_from('<25I', raw, 0x49E4D3-0x400000)
    need((table[0],table[1],table[16]) == (0x49E3BC,0x49E30B,0x49E39E), 'MAIN event dispatch')
    for address, expected in ((STARTUP_VTABLE,0x5063A0),(SCENE_VTABLE,0x451670),(MENU_VTABLE,0x45EB90)):
        need(struct.unpack_from('<I',raw,address-0x400000)[0] == expected, 'original task callback')
    return dict(source=dict(bytes=len(raw),sha256=sha(raw)),script=dict(bytes=len(script),sha256=sha(script)),
        instructions=instructions,commands=commands,
        ranges=[dict(start=a,end=b,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in RANGES],
        original_frame_order=['clear bucket heads','reset arena','run every registered task and await yield',
                              'consume queued render commands'],
        confirmed_contracts=[
            'MAIN event16 constructs/registers scene; it does not retire the existing startup/menu worker.',
            'Startup reads the same game+1990 input word as dialogue mouse confirmation; mask1 branches to its natural tail.',
            'Startup tail frees pool group10, publishes event1, and returns; event1 creates menu callback45EB90.',
            'Menu initialization and battle initialization both replace pool group90 through416790.',
            'Pool replacement frees old descriptor array before allocating/registering its replacement.',
            'Menu destruction calls41F480, which frees all256 pool groups; destructive independent menu deletion is unsafe.',
            'Text clear44 resets embedded text state; it does not free the descriptor array.',
            'Render queue holds descriptor addresses, not a copied texture pointer or retained COM reference.',
        ],
        pool_layout=dict(manager_game_offset=0x844,group_stride=8,
            slots_game_offset={'10':0x894,'20':0x8E4,'90':0xB14},
            entry_fields={'0':'descriptor array base','4':'descriptor count'},
            descriptor_stride=0x54,texture_offset=0x2C,
            allocation_user_from_base=-4,CRT_debug_header_from_base=-0x24,
            warning='Do not interpret an interior descriptor-20 as an allocation header.'),
        scheduler_isolation_fixture=dict(set_root=0x422560,clear_root=0x4225A0,
            receiver='actual already-registered startup node',argument_mask=2,flags_offset=4,
            manager_skip_branch=0x421880,
            preconditions=[
                'Suspend all existing process threads for one coherent snapshot.',
                'Worker is actually blocked on its own unsignaled node event via422407, with original TLS/stack ownership.',
                'MAIN has not already passed this node421850 flags check and committed to signaling it; reject such a sample.',
                'No pending event will create an additional conflicting scene/menu; bind exact manager graph.',
                'Execute original422560(node,2) via authenticated private bridge while existing threads remain stopped.',
                'Resume and observe bit2 retained, worker still waiting, no worker CPU/progress, and no incompatible new resource owner.',
            ],
            limitations=[
                'Setter is an unlocked read/modify/write; flags10000 alone is not a completed-yield certificate.',
                '4225A0(node,2) resumes eligibility; it does not pause.',
                '422090 forcibly terminates the worker;422440 terminates its calling thread, neither is a substitute.',
                'Paused startup remains alive and retains resources; this is test scheduling isolation, not natural transition or complete cleanup.',
                'Do not resume paused startup after battle overwrites/frees shared pools without a separately proved lifetime.',
            ],native_isolation_executed=False,natural_startup_exit=False,
            original_scheduling_preserved=False,full_process_lifetime_accepted=False),
        menu_routes=dict(original_selection_function=0x45EFB0,
            hit_test=0x45F810,rectangle_table=0x60CEB0,
            confirmation_game_offset=0x199C,mask=1,
            selection_to_event={'0':7,'1':13,'3':14,'4':3,'6':0},
            startup_next_event=1,
            new_game='event7 creates49F4E0 callback; it loads original story script and publishes6 then returns.',
            normal_battle='4B9034 uses original schedule7A5296 and7A5308+index*70, prepares selected actors, then publishes16.',
            no_direct_T0004_selection_proved=True),
        unresolved=[
            'Fault v4 lacks the actual node+50/descriptor address: affected group and freeing caller remain unproved.',
            'Direct scenario4 roots lack a proven old-worker retirement/transition ancestry.',
            'Original menu routes463250/461A70 publish16 and return after original selection; inspected immediate cases select76..80/9, not4.',
            'A bounded natural scenario4 menu/load route remains to be established; do not invent a callback return or terminate a worker.',
        ],
        required_next_observation=[
            'Original exiting worker callback return421F8A, CRT thread completion, manager unlink, pending MAIN event and successor ancestry.',
            'Before battle input: no startup5CAA48 or menu59B060 resource owner remains registered alongside battle59A430.',
            'Track original pool entry(group base,count), queued descriptor membership and old array header/cookie before and after replacement.',
            'Array descriptors have stride54 and a4-byte array cookie; CRT header is base-4-20, not each descriptor-20.',
        ],
        accepted=False,live_code_authenticated=False,resource_fault_cause_proved=False,
        transition_repaired=False,full_battle_exit_accepted=False)


def graph_timeline(samples):
    """Summarize existing graph observations, without inferring missing events."""
    need(isinstance(samples,list) and 0 < len(samples) <= 1600,'bounded sample count')
    changes, previous = [], None
    overlap = dict(startup_and_scene=False,menu_and_scene=False)
    for ordinal,sample in enumerate(samples):
        tasks = sample.get('registered_tasks')
        need(isinstance(tasks,list) and len(tasks) <= 64,'bounded registered task graph')
        graph, seen = [], set()
        for task in tasks:
            pointer = task['pointer']
            need(type(pointer) is int and 0x10000 <= pointer < 0x80000000 and pointer not in seen,
                 'unique valid task pointer')
            seen.add(pointer)
            text = task['head_hex']
            need(isinstance(text,str) and 8 <= len(text) <= 512 and len(text)%2 == 0,'bounded node head')
            head = bytes.fromhex(text)
            graph.append((pointer,struct.unpack_from('<I',head)[0]))
        identities = {v for _,v in graph}
        overlap['startup_and_scene'] |= {STARTUP_VTABLE,SCENE_VTABLE} <= identities
        overlap['menu_and_scene'] |= {MENU_VTABLE,SCENE_VTABLE} <= identities
        signature = tuple(graph)
        if signature != previous:
            changes.append(dict(sample=ordinal,elapsed=sample.get('elapsed'),graph=[
                dict(pointer=p,vtable=v) for p,v in graph]))
            previous = signature
    return dict(changes=changes,observed_overlap=overlap,
                safe_transition_proved=False,causal_resource_link_proved=False)


def require_empty_scene_preflight(manager_hex, main_event_hex, registered_tasks):
    """Reject independent setup until a complete, coherent graph is empty.

    Caller must capture these bytes in one pause and authenticate their actual
    MAIN addresses and process ownership. This pure check cannot prove either.
    Renderer queue emptiness and normal retirement ancestry are not certified.
    """
    need(isinstance(manager_hex,str) and len(manager_hex)==0x120*2,
         'complete manager0x120 snapshot')
    need(isinstance(main_event_hex,str) and len(main_event_hex)==8*2,
         'complete MAIN pending event8 snapshot')
    manager=bytes.fromhex(manager_hex)
    event=bytes.fromhex(main_event_hex)
    need(isinstance(registered_tasks,list),'complete registered graph required')
    # Validate the supplied traversal even when rejecting its non-empty result.
    graph_timeline([dict(registered_tasks=registered_tasks)])
    need(not registered_tasks,'existing registered worker: refuse independent scene roots and input')
    # Original421660 zeros both words. Only the low word/node+0C is a
    # demonstrated list link; the high word is not a proved tail pointer.
    need(manager[:0x100] == bytes(0x100),'all32 manager bucket storage words must be empty')
    need(struct.unpack_from('<I',event)[0] == 0,'MAIN event must be idle')
    return dict(empty_graph_and_idle_event=True,renderer_queue_empty_proved=False,
                natural_retirement_proved=False,resource_lifetime_repaired=False,
                full_battle_exit_accepted=False)


def report_summary(path, expected_sha):
    path = Path(path)
    need(path.stat().st_size <= MAX_PACKED,'bounded compressed source')
    packed = path.read_bytes()
    need(len(expected_sha)==64 and sha(packed)==expected_sha,'fixed observation SHA')
    with gzip.GzipFile(fileobj=io.BytesIO(packed)) as stream:
        raw = stream.read(MAX_RAW+1)
    need(len(raw)<=MAX_RAW,'bounded decompressed source')
    data = json.loads(raw)
    probe=data['probe']
    samples=probe['samples']
    summary = graph_timeline(samples)
    pc172=[]
    fault_context=[]
    for n,sample in enumerate(samples):
        vm=bytes.fromhex(sample['VM_hex'])
        need(34 <= len(vm) <= 4096,'bounded complete VM status')
        if struct.unpack_from('<I',vm,28)[0] == 172:
            pc172.append(n)
        # This address is only a correlation with the separately retained v4
        # WER/d3d8 analysis. It does not prove a fault in any other source.
        if expected_sha == '5b0c15243e68dd8c474605a8409ef5d41f8a4bdea2fa7fdd63bb08e5d16e5286':
            if any(f['tid']==probe['window']['main_tid'] and f['EIP']==0x6F51D8E8
                   for f in sample['frames']):fault_context.append(n)
    return dict(path=str(path),bytes=len(packed),sha256=sha(packed),**summary,
                sample_count=len(samples),PC172_samples=len(pc172),
                PC172_first_sample=pc172[0] if pc172 else None,
                previously_correlated_v4_fault_first_sample=fault_context[0] if fault_context else None,
                worker_exit=probe.get('worker_exit'),source_after_present='source_after' in probe,
                source_before_after_equal=bool('source_after' in probe and probe['source_before']==probe['source_after']),
                observer_error=probe.get('error'))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    parser.add_argument('--report',action='append',nargs=2,metavar=('PATH','SHA256'),default=[])
    args=parser.parse_args()
    need(len(args.report)<=4,'at most four existing observations')
    out=Path(args.out).resolve()
    need(out.is_relative_to(ROOT/'analysis') and not out.exists(),'fresh analysis output')
    result=source_contract((ROOT/'analysis/hermit_game.exe').read_bytes(),
        (ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT/T0004.BIN').read_bytes())
    result['observations']=[report_summary(p,h) for p,h in args.report]
    result['implementation_sha256']=sha(Path(__file__).read_bytes())
    raw=json.dumps(result,indent=2).encode()
    need(len(raw)<1024*1024,'small static report')
    with out.open('xb') as stream:
        stream.write(raw)
    print(json.dumps(dict(path=str(out),bytes=len(raw),sha256=sha(raw),accepted=False)))


if __name__=='__main__':
    main()

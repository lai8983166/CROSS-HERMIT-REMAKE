"""Bounded static audit only: no frozen tool imports, emulation, native calls or history loads."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'analysis/hermit_game.exe'
SOURCE_SHA = '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
# Half-open instruction intervals; switch tables are decoded separately as data.
RANGES = {
    'wait': (0x422360, 0x422434),
    'flags': (0x422560, 0x42260A),
    'scheduler_constructor_and_registration': (0x421540, 0x421850),
    'scheduler_dispatch': (0x421850, 0x421BE3),
    'scheduler_begin_worker': (0x421EA0, 0x421F44),
    'worker_callback_and_exit': (0x421F50, 0x422029),
    'CRT_beginthreadex_and_worker': (0x56E050, 0x56E225),
    'CRT_TLS_lookup_and_free': (0x5753B0, 0x57555B),
    'scene_callback': (0x451670, 0x4519A3),
    'scene_dispatch': (0x451A60, 0x451B0F),
    'tail_frame': (0x451F00, 0x451F4E),
    'controller_exit_cleanup': (0x465E60, 0x465F81),
    'MAIN_outer_frame': (0x49E540, 0x49E845),
    'scene_loop': (0x4539B0, 0x453CFC),
    'replay_record_enabled': (0x496410, 0x49644C),
    'post_result_replay_record': (0x4967B0, 0x4968A9),
    'MAIN_event_publish': (0x439E30, 0x439EE4),
    'MAIN_event_consumer': (0x49E2B0, 0x49E4D3),
    'exit_completion_wrappers': (0x4DB230, 0x4DB2AA),
}
REFERENCES = [
    'docs/terminal_unit_frontends.md', 'docs/school_scheduler_lifetime.md',
    'docs/school_scene_bootstrap.md', 'docs/school_retained_scheduler.md',
    'docs/school_native_scene.md', 'tools/terminal_battle_exit_emulation.py',
    'tools/terminal_unit_frontends_emulation.py', 'tools/terminal_overlay_emulation.py',
    'tools/school_scheduler_lifetime.py', 'tools/school_scene_bootstrap.py',
    'tools/school_retained_scheduler.py', 'tools/school_retained_scheduler_platform.cs',
    'tools/school_retained_scheduler_verification.py',
    'analysis/school-scheduler-lifetime-acceptance-v1-20261021.json',
    'analysis/school-scene-bootstrap-acceptance-v1-20261021.json',
    'analysis/school-retained-scheduler-acceptance-v1-20261024.json',
    'analysis/school-native-scene-acceptance-v1-20261021.json',
]
CHECKS = {
    0x422589: ('mov', 'dword ptr [edx + 4], ecx'),
    0x4225CE: ('mov', 'dword ptr [eax + 4], edx'),
    0x42238C: ('mov', 'dword ptr [edx + 0x14], eax'),
    0x422407: ('call', 'dword ptr [0x59226c]'),
    0x422431: ('ret', '4'),
    0x453CB0: ('call', '0x422360'),
    0x453CB5: ('cmp', 'dword ptr [ebp - 8], 0'),
    0x453CC4: ('call', '0x4967b0'),
    0x453CCE: ('call', '0x422360'),
    0x453CD8: ('call', '0x422360'),
    0x453CDD: ('mov', 'eax, 1'),
    0x453CE4: ('jmp', '0x4539cd'),
    0x453CFB: ('ret', ''),
    0x451AB7: ('call', '0x4539b0'),
    0x451ABC: ('mov', 'dword ptr [ebp - 8], eax'),
    0x451711: ('call', '0x451a60'),
    0x451753: ('call', '0x422360'),
    0x451774: ('call', '0x465e60'),
    0x4519A0: ('ret', '4'),
    0x421F88: ('call', 'dword ptr [eax]'),
    0x422021: ('call', '0x56e1e0'),
    0x56E0BE: ('call', 'dword ptr [0x59221c]'),
    0x56E141: ('call', 'dword ptr [0x5921a8]'),
    0x56E180: ('call', 'dword ptr [edx + 0x48]'),
    0x439EAC: ('mov', 'dword ptr [ecx + 0x20], edx'),
    0x49E4B2: ('mov', 'dword ptr [edx], 0'),
}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def need(condition, message):
    if not condition:
        raise ValueError(message)


def build():
    raw = (ROOT / SOURCE).read_bytes()
    need(len(raw) == 5980160 and sha(raw) == SOURCE_SHA, 'original image identity')
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    instructions = {}
    ranges = []
    for name, (start, end) in RANGES.items():
        data = raw[start - 0x400000:end - 0x400000]
        rows = []
        for i in md.disasm(data, start):
            instructions[i.address] = (i.mnemonic, i.op_str)
            rows.append(dict(va=hex(i.address), hex=i.bytes.hex(), mnemonic=i.mnemonic,
                             operands=i.op_str))
        need(sum(len(bytes.fromhex(r['hex'])) for r in rows) == len(data), name)
        ranges.append(dict(name=name, start=hex(start), end_exclusive=hex(end),
                           bytes=len(data), sha256=sha(data), instructions=rows))
    for pc, expected in CHECKS.items():
        need(instructions.get(pc) == expected, (hex(pc), instructions.get(pc), expected))
    refs = []
    for name in REFERENCES:
        path = ROOT / name
        need(path.stat().st_size < 2 * 1024 * 1024, 'small reference only')
        data = path.read_bytes()
        refs.append(dict(path=name, bytes=len(data), sha256=sha(data)))
    event_table = struct.unpack_from('<25I', raw, 0x49E4D3 - 0x400000)
    scenario_table = struct.unpack_from('<7I', raw, 0x4519A3 - 0x400000)
    return dict(
        schema_version=1, kind='bounded_static_contract', accepted=False,
        dynamic_execution=False, native_execution=False, historical_case_tree_loaded=False,
        source=dict(path=SOURCE, bytes=len(raw), sha256=sha(raw),
                    addressing='loaded/unpacked image bytes at VA minus 0x400000; not generic PE file RVA translation'),
        reference_identities=refs, checked_instructions=len(CHECKS), ranges=ranges,
        analyzer_sha256=sha(Path(__file__).read_bytes()),
        IAT_slots={'0x592234':'EnterCriticalSection', '0x592238':'LeaveCriticalSection',
                   '0x592228':'ResetEvent', '0x59222c':'SetEvent', '0x59226c':'WaitForSingleObject',
                   '0x592274':'CreateEventA', '0x592230':'ResumeThread', '0x59221c':'CreateThread',
                   '0x592268':'GetExitCodeThread', '0x592270':'CloseHandle', '0x592264':'Sleep',
                   '0x5921a8':'TlsSetValue', '0x592154':'TlsGetValue', '0x5921ac':'GetCurrentThreadId',
                   '0x5921a4':'ExitThread'},
        wait_contract=dict(
            ABI='ECX=scene task; [ESP]=453CB5; [ESP+4]=0; ret 4. EAX is not the scene result.',
            fields={'task+08':'scheduler manager pointer', 'task+04':'flags',
                    'task+14':'delay count, assigned from argument', 'task+18':'callback parameter',
                    'task+1c':'auto-reset node event', 'task+20':'CRT worker thread handle',
                    'task+24':'worker thread ID', 'task+28':'auto-delete byte',
                    'manager+100':'24-byte native CRITICAL_SECTION', 'manager+118':'auto-reset manager event'},
            protocol=[
                '42238C sets task+14 to 0; 422397 ORs flag 0x10000 through original 422560.',
                '4223A8 EnterCriticalSection(manager+100); 4223BE ResetEvent(task+1C); 4223D7 SetEvent(manager+118); 4223EF LeaveCriticalSection.',
                '422407 WaitForSingleObject(task+1C, INFINITE); 42241C clears flag 0x10000 through 4225A0; 422431 ret4.',
                'Active scheduler 421850 rejects disabled flag2. A nonzero delay decrements once and returns; delay0 enters 4218B3, resets manager event, signals node at 4218F7, leaves lock, then waits manager event at 42192B.',
                'A naturally blocked worker and manager perform reciprocal handshakes. WaitForSingleObject results are not checked by original wait body: invalid-handle WAIT_FAILED could also reach ret; acceptance must independently require owned live events and actual successful waits.',
            ]),
        continuation=[
            '453CB5 checks original scene-frame local [EBP-8]. Zero goes 453CE4 -> 4539CD next loop; accepted current cases save 1 per frozen capture_frontier.',
            'Nonzero calls 4967B0 on task+190 at 453CC4, then waits at 453CCE (return453CD3) and 453CD8 (return453CDD), sets EAX=1 and naturally returns at 453CFB.',
            '496410 tests signed byte CTRL+117C3C == 1. Otherwise 4967B0 returns0 without file activity. Enabled branch opens ReplayData.rep with a+b, appends 28B stack record through 570D70 and closes through56E4A0; full record contains fields beyond its first three dwords and must be observed, not invented.',
            'Real caller 451AB7/451ABC propagates nonzero as1 through451ACA; 451711/451716 consumes it and leaves the scene callback loop at45171F.',
            '451723 begins callback tail: ten 451F00 calls each followed by422360(0) at451753; then40D610,465E60(CTRL),4DB230(60); 4DB270 gates progress with further422360(0) at451791 while zero.',
            '451798 onward selects successor using task+31, scenario words7F4488/7F448A, game flag5FF720, task+174 and real function results. Every selected439E30 publishes event on actual MAIN+10; it writes event atMAIN+30 and pending flag1 atMAIN+2C under MAIN+14 lock.',
            '4519A0 ret4 naturally returns to421F8A. Worker enters manager lock, clears flags then sets4, resets node event, signals manager, leaves lock and invokes56E1E0(0).',
            'Scheduler reads completion flag4, repeatedly queries GetExitCodeThread until !=STILL_ACTIVE, closes node event, clears flags, unlinks through421D50, and if autoDelete calls virtual destructor then428AD0. Thread handle+20 is not closed in this branch; owner supplement must be explicit.',
            '49E2B0 consumes actual MAIN+2C/+30 event via jump table, executes successor, clears pending flag at49E4B2, then49E540. Publishing an event is not proof its successor completed, nor proof rewards/school completed.',
        ],
        tables=dict(
            callback_scenario_76_to_82=[dict(scenario=76+i,target=hex(v)) for i,v in enumerate(scenario_table)],
            main_events=[dict(event=i,target=hex(v)) for i,v in enumerate(event_table)],
            selected_event_calls={'1':'49E30B ->45E8D0','2':'49E315 ->460040','11':'49E3A8 ->4BD6F0',
                                  '15':'49E3E4 ->443AC0','16':'49E39E ->451080','17':'49E3B2 ->42FCD0'}),
        thread_TLS_ownership=[
            '4216C0 must naturally register node into same manager. 421850 creates node event; 421EA0 invokes56E050 with worker421F50,node,CREATE_SUSPENDED=4 and node+24 output.',
            '56E050 allocates 116-byte CRT per-thread data; +48=421F50,+4C=node; CreateThread at56E0BE uses56E110 and this live native PTD. Logical addresses cannot be sent to another helper process as native pointers.',
            '56E110 establishes FS:[0] SEH chain, TlsSetValue at5921A8 using index[761BC0] and PTD, records actual GetCurrentThreadId, invokes optional runtime init[76197C], then PTD callback.',
            '56E1E0 runs optional runtime exit[761980],5753B0 TLS lookup,575450 PTD/nested cleanup and ExitThread5921A4. Caller/worker TLS, heaps, locks, events and thread identity must share authenticated native owner/lifetime.',
            'Same OS-thread ownership matters for Enter/LeaveCriticalSection and TLS. A serial helper command thread and a synthetic wait thread do not establish original CRT worker or actual451670 ancestry.',
        ],
        current_fixture_gaps=[
            'terminal_battle_exit_emulation explicitly roots4539B0 and returns to harness RETURN. It does not contain451AB7/451711/421F88/56E180 ancestors; continuing that frame cannot establish them retroactively.',
            'terminal_overlay MANAGER=MAIN+1058 is renderer queue manager; original scheduler is actual MAIN+64. Existing scene wait evidence does not authenticate scheduler fields/events/thread/TLS ownership.',
            'Current source freezes before first422360 instruction and later supplements destructors. Completed helper lifetimes cannot be reused by copying historical handles or restoring CPU.',
            'No existing current-case proof covers post-wait4967B0 branch, two additional scene-loop waits, callback tail, cleanup465E60, completion wrappers, selected successor, worker normal exit or scheduler autoDelete.',
            'Current exact task header values require authenticated current-case observation. Older retained-scheduler zero-header evidence is a different fixture and is not asserted as current terminal RAM.',
        ],
        minimum_continuation=dict(
            prerequisite='Authenticate current-case full CPU/RAM/stack before testing TASK+08/+1C; do not transplant old snapshot handles.',
            original_roots=['421540(new manager) creates actual owned lock and manager event',
                            '421660(new manager) initializes buckets',
                            '4216C0(manager,TASK,0,0) registers task using original writes',
                            '4217C0 ->421850 creates actual owned node event ->421EA0 ->56E050 allocates PTD and reaches original CreateThread request'],
            forbidden_shortcuts=['Do not reconstruct the existing scene with451170 or422290; that destroys business state.',
                                 'Do not hand-write thread handle/ID/TLS or replace451670 with4539B0.',
                                 'Do not manually SetEvent to claim original scheduling; use original reciprocal manager/worker path.',
                                 'Do not pass guest56E110/PTD pointers to a helper lacking the same authenticated original executable/CRT address space.'],
            required_real_worker='CreateThread must return real same-owner handle/ID; original56E110 on that worker establishes its SEH/TLS/PTD and calls421F50 ->451670. Existing direct4539B0 root cannot acquire that ancestry retroactively.',
            independent_registration_only_flags=dict(cooperative_wait_executed=False, original_CRT_worker_created=False,
                original_MAIN_scheduler_connected=False, outer_result_consumed=False, terminal_battle_exit_executed=False,
                rewards_or_school_executed=False, original_outer_thread_restored=False),
            limit='Independent registration is an admissible ownership/dependency probe only; not completion or a means to resume historical native lifetimes.'),
        completion_criteria=[
            'Wait scope: complete original frame/ABI and full state, three actual reciprocal scheduler/worker handshakes to4539B0 nonzero natural return; preserve original result local and original4967B0 effects.',
            'Scene exit scope: prove natural original caller ancestry and result propagation, ten tail waits plus any completion-gate waits, resource cleanup and selected event publication with exact branch inputs.',
            'Worker/resource scope: actual normal CRT ExitThread, TLS/PTD release, scheduler observed exited thread, node event close/unlink/autoDelete and correct destructor effects. Report supplemental thread CloseHandle distinctly; cancellation/TerminateThread is not normal callback exit.',
            'Successor scope: actual MAIN event consumer follows selected table target in same valid lifetime and reaches a declared meaningful endpoint; reward/school completion requires its own downstream proof, not a guessed label.',
            'Formal acceptance still requires existing two-case fresh native lifetimes, independent full replay/state/ABI/digests, tamper rejection, resource accounting and preservation; this static report satisfies none of those dynamic criteria.',
        ],
        reusable_contracts=[
            dict(reference='school_scheduler_lifetime',reuse='Original creation/registration/dispatch/worker/TLS runtime/event/normal-exit ownership and explicit leaked thread-handle cleanup in owned original process.',limit='Private base nodes use empty422330 callback; not current scene or continuous terminal proof.'),
            dict(reference='school_scene_bootstrap',reuse='Original derived constructor/vtable/destructor and real isolated wait parameter/flag protocol.',limit='Yield probe uses external declared event and manual SetEvent; cannot prove natural scheduler wake or scene completion.'),
            dict(reference='school_retained_scheduler',reuse='Original register->calloc/PTD->CreateThread request with complete ABI; real current event/critical-section ownership translation.',limit='Stops before CreateThread; helper has no original executable/TLS worker and wait API is bounded <=1000ms, incompatible with original infinite wait contract as-is.'),
            dict(reference='school_native_scene',reuse='Actual original MAIN event->factory->49E540/4217C0->CRT worker->451670->4539B0 on owned copied runtime.',limit='Different new-game fixtures; snapshot evidence rather than full terminal replay; existing close path includes TerminateThread and does not prove natural scene exit.'),
        ],
        unresolved=['Full dynamic branch inputs and all post-exit called bodies remain to be exercised and independently validated.',
                    'Audio/render completion gate and resource cleanup dependencies must be read before implementing tail; this audit does not label a successor factory as completed rewards/school.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    out = ROOT / args.out
    if out.exists():
        parser.error('fresh report path required')
    report = build()
    blob = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    need(len(blob) < 1024 * 1024, 'bounded small report')
    with out.open('xb') as stream:
        stream.write(blob)
    print(json.dumps(dict(path=str(out), bytes=len(blob), sha256=sha(blob),
                          checked_instructions=report['checked_instructions'],
                          static_only=True, accepted=False)))

if __name__ == '__main__':
    main()

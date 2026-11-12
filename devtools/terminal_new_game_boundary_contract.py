"""Offline NEW_GAME boundary audit. Never launches, attaches to, or inputs a process.

The original 49F507 tail is executed only in bounded synthetic Unicorn memory.
No OS/COM return is substituted. This does not restore a native lifetime.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import struct
import time

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
import unicorn
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EBP, UC_X86_REG_EIP, UC_X86_REG_ESP

ROOT = Path(__file__).resolve().parents[1]
BASE = 0x400000
SOURCES = {
    'image': ('analysis/hermit_game.exe', 5980160,
              '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'),
    'menu': ('analysis/terminal-new-game-native-v1-20261112.json.gz', 88195,
             '9813d6dea1dd2e41db73eebddc80b7a5f9bedfb5fd2e8bb475806d25fe2a1c2e'),
    'crt': ('analysis/school-crt-init-probe-v2-20261022.json.gz', 7115235,
            '850b684f76c67e674bc1ba4a79b398bcb18f8b6abb01cda1e4d8908830c07a82'),
    'relay_review': ('analysis/terminal-wait-relay-review-v1-20261109.json', 7670,
                     '140ed4a996d28b053b75ced259ee54018523c1a7890c9a0d86cd9549dea65e1d'),
}
CHECKS = {
    0x49F502: ('call', '0x4d3510'),
    0x49F509: ('call', '0x4db230'),
    0x49F511: ('call', '0x4db270'),
    0x49F518: ('je', '0x49f51c'),
    0x49F51A: ('jmp', '0x49f528'),
    0x49F521: ('call', '0x422360'),
    0x49F539: ('call', '0x4ce210'),
    0x49F549: ('call', '0x439e30'),
    0x49F55E: ('ret', '4'),
    0x41D7B0: ('movsx', 'eax, byte ptr [eax + 0x20]'),
    0x41E747: ('jne', '0x41e758'),
    0x41E74C: ('call', '0x41e6b0'),
    0x41E75B: ('movsx', 'ecx, byte ptr [eax + 0x22]'),
    0x41E763: ('jmp', '0x41e749'),
    0x41E76B: ('mov', 'dword ptr [edx + 0x260], eax'),
    0x41E81E: ('jne', '0x41e82a'),
    0x41E820: ('mov', 'eax, 1'),
    0x41E835: ('mov', 'eax, 1'),
    0x41E842: ('cmp', 'dword ptr [edx + 0x260], 0'),
    0x41DAED: ('call', 'dword ptr [eax + 0x1c]'),
    0x56E141: ('call', 'dword ptr [0x5921a8]'),
    0x56E15E: ('mov', 'dword ptr [edx], eax'),
    0x56E180: ('call', 'dword ptr [edx + 0x48]'),
    0x421F88: ('call', 'dword ptr [eax]'),
    0x421947: ('call', 'dword ptr [0x592274]'),
    0x421EC4: ('push', '4'),
    0x421ED3: ('call', '0x56e050'),
    0x421A44: ('call', 'dword ptr [0x59222c]'),
    0x421A5A: ('call', 'dword ptr [0x592230]'),
    0x421A8E: ('call', 'dword ptr [0x59226c]'),
    0x439E99: ('call', 'dword ptr [0x592234]'),
    0x439EAC: ('mov', 'dword ptr [ecx + 0x20], edx'),
    0x439EB2: ('mov', 'dword ptr [eax + 0x1c], 1'),
    0x421FED: ('call', 'dword ptr [0x59222c]'),
    0x422021: ('call', '0x56e1e0'),
    0x56E20F: ('call', '0x575450'),
    0x57554F: ('call', 'dword ptr [0x5921a8]'),
    0x56E21B: ('call', 'dword ptr [0x5921a4]'),
    0x42ABED: ('call', 'dword ptr [0x5921ec]'),
    0x83962E: ('lea', 'edx, [ebp - 0xa28]'),
    0x839634: ('mov', 'dword ptr [ebp - 0xa2c], edx'),
    0x8396DB: ('push', '0x3e8'),
    0x8396E7: ('call', 'dword ptr [0x86e0e4]'),
    0x8396ED: ('test', 'eax, eax'),
    0x8397EE: ('mov', 'dword ptr [ebp - 0xa30], 0x80010001'),
    0x83B043: ('cmp', 'dword ptr [ecx], 2'),
    0x83B0CC: ('cmp', 'dword ptr [ecx], 4'),
    0x83B193: ('cmp', 'dword ptr [eax], 8'),
    0x83BE27: ('call', 'dword ptr [0x86e0d8]'),
    0x83BE48: ('call', 'dword ptr [0x86e0d8]'),
}
# Only these authenticated original instruction ranges may execute in this audit.
EXEC_RANGES = ((0x49F507, 0x49F528), (0x4DB230, 0x4DB2AA),
               (0x41D790, 0x41D7BB), (0x41E6B0, 0x41E71A),
               (0x41E720, 0x41E7E5), (0x41E7F0, 0x41E938),
               (0x41DA80, 0x41DAED), (0x56CFCC, 0x56D04C),
               (0x56CE80, 0x56CE83))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source(name):
    path, size, digest = SOURCES[name]
    p = ROOT / path
    need(p.stat().st_size == size, 'source size: ' + name)
    raw = p.read_bytes()
    need(sha(raw) == digest, 'source SHA: ' + name)
    return raw


def unpack(raw, limit):
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as stream:
        decoded = stream.read(limit + 1)
    need(len(decoded) <= limit, 'bounded decoded source')
    return json.loads(decoded)


def checked_instructions(raw):
    need(len(raw) == SOURCES['image'][1] and sha(raw) == SOURCES['image'][2], 'original image identity')
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    result = []
    for at, expected in CHECKS.items():
        i = next(md.disasm(raw[at-BASE:at-BASE+16], at))
        need((i.mnemonic, i.op_str) == expected, 'original instruction ' + hex(at))
        result.append(dict(va=hex(at), hex=i.bytes.hex(), mnemonic=i.mnemonic, operands=i.op_str))
    return result


def audio_projection(menu):
    ready = menu['lifecycle']['ready']
    game = bytes.fromhex(ready['game']['hex'])
    need(len(game) == 47648 and ready['game']['pointer'] == 0x4D30068, 'fixed ready game bytes')
    audio = game[0x8C88:0x8F00]
    need(len(audio) == 632 and audio[0x20] == audio[0x22] == 0, 'recorded early inactive audio')
    return audio, dict(json_path='lifecycle.ready.game.hex', offset=0x8C88, bytes=632,
                       sha256=sha(audio), elapsed=ready['elapsed'], original_pointer=ready['game']['pointer']+0x8C88,
                       contemporaneous_with_NEW_GAME=False,
                       cannot_explain_missing_worker_by_itself=True)


def tail_case(raw, audio, mode):
    need(mode in ('recorded_early_inactive', 'synthetic_second_guard', 'synthetic_active'), 'declared branch case')
    need(len(audio) == 632, 'exact input object size')
    block = bytearray(audio)
    if mode == 'synthetic_second_guard':
        block[0x20], block[0x22] = 1, 0
    elif mode == 'synthetic_active':
        block[0x20], block[0x22] = 1, 1
        # Only a readable synthetic interface/vtable, never a host COM object.
        struct.pack_into('<I', block, 0x10, 0x2000E000)
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.mem_map(BASE, (len(raw)+4095) & ~4095)
    uc.mem_write(BASE, raw)
    uc.mem_map(0x20000000, 0x10000)
    uc.mem_write(0x20008C88, bytes(block))
    uc.mem_write(0x2000E000, struct.pack('<I', 0x2000E100))
    uc.mem_write(0x7A49FC, struct.pack('<I', 0x20000000))
    uc.mem_map(0x21000000, 0x1000)
    uc.reg_write(UC_X86_REG_EBP, 0x21000800)
    uc.reg_write(UC_X86_REG_ESP, 0x210007B0)
    uc.mem_write(0x210007FC, struct.pack('<I', 0x2000F000))
    pcs, writes, stopped = [], [], []

    def step(u, at, size, _):
        if at in (0x49F528, 0x422360, 0x41DAED):
            stopped.append(at)
            u.emu_stop()
            return
        need(any(lo <= at and at+size <= hi for lo, hi in EXEC_RANGES), 'unexpected instruction: ' + hex(at))
        need(bytes(u.mem_read(at, size)) == raw[at-BASE:at-BASE+size], 'unmodified executed bytes')
        pcs.append(at)

    def write(u, access, at, size, value, _):
        need((0x21000000 <= at and at+size <= 0x21001000) or
             (0x20008C88 <= at and at+size <= 0x20008F00), 'only synthetic stack/audio writes')
        writes.append((u.reg_read(UC_X86_REG_EIP), at, size, value & ((1 << (size*8))-1)))

    uc.hook_add(UC_HOOK_CODE, step)
    uc.hook_add(UC_HOOK_MEM_WRITE, write)
    uc.emu_start(0x49F507, 0x49F53E, timeout=2_000_000, count=2048)
    need(len(stopped) == 1 and len(pcs) < 2048, 'one boundary before instruction/time budget')
    end = bytes(uc.mem_read(0x20008C88, 632))
    active = mode == 'synthetic_active'
    need(stopped == ([0x41DAED] if active else [0x49F528]), 'expected real boundary')
    need(0x49F521 not in pcs, 'no observed callback yield')
    need(struct.unpack_from('<I', end, 0x260)[0] == (90 if active else 0), 'original fade counter')
    if not active:
        need(uc.reg_read(UC_X86_REG_EAX) == 1 and 0x49F51A in pcs, 'original ready branch skips yield')
    return dict(mode=mode, input_sha256=sha(bytes(block)), original_entry='0x49f507',
                stop_before=hex(stopped[0]), instruction_callbacks=len(pcs), write_callbacks=len(writes),
                instruction_PC_sha256=sha(b''.join(struct.pack('<I', x) for x in pcs)),
                writes_sha256=sha(json.dumps(writes, separators=(',', ':')).encode()),
                pcs=[hex(x) for x in pcs], audio_after_sha256=sha(end),
                ready_return_observed=not active, yield_executed=False, OS_or_COM_calls=0,
                synthesized_leaf_returns=0, native_execution=False, accepted=False)


def historical_debug_strings(crt):
    need(len(crt['cases']) == 8, 'eight fixed historical startup cases')
    cases = []
    for c in crt['cases']:
        strings = []
        for index, w in enumerate(c['parent_waits']):
            state = bytes.fromhex(w['state_hex'])
            need(len(state) == 96, 'raw NT state size')
            if struct.unpack_from('<I', state, 12)[0] != 0x40010006:
                continue
            nt, pid, tid = struct.unpack_from('<3I', state)
            need(nt == w['state'] == 6 and pid == w['child_pid'] == c['child_pid'] and tid == w['child_tid'],
                 'actual NT exception record ownership')
            need(struct.unpack_from('<I', bytes.fromhex(w['parent_return_context_hex']), 176)[0] == 0,
                 'successful original NtWait return')
            strings.append(dict(wait_index=index, NT_state=nt, exception_code='0x40010006', pid=pid, tid=tid,
                                raw_state_sha256=sha(state)))
        need(len(strings) == 2 and bool(c['debug_register_instrumentation']) and
             c['cleanup']['explicit_probe_termination'] and not c['cleanup']['original_game_normal_shutdown'],
             'historical instrumented startup, not a normal NEW_GAME source')
        cases.append(dict(target=hex(c['target']), strings=strings))
    return dict(cases=cases, original_debug_strings_exist=True,
                NEW_GAME_TLS_interval_notification_proved=False,
                relies_on_debug_register_instrumentation=True, normal_cleanup_proved=False,
                NT_state8_is_not_Win32_debug_string_event8=True)


def build():
    started = time.perf_counter()
    raw = source('image')
    checks = checked_instructions(raw)
    menu = unpack(source('menu'), 16*1024*1024)
    audio, projection = audio_projection(menu)
    cases = [tail_case(raw, audio, mode) for mode in
             ('recorded_early_inactive', 'synthetic_second_guard', 'synthetic_active')]
    history = historical_debug_strings(unpack(source('crt'), 128*1024*1024))
    relay = json.loads(source('relay_review'))
    need(relay['observed']['original_parent_reply'] == '0x80010001' and
         relay['observed']['parent_exit_event'] == '0x4000001E' and not relay['accepted'], 'preserve relay rejection')
    return dict(kind='offline_NEW_GAME_boundary_contract', accepted=False,
        implementation=dict(path=Path(__file__).relative_to(ROOT).as_posix(), sha256=sha(Path(__file__).read_bytes())),
        sources={name:dict(path=p, bytes=n, sha256=h) for name,(p,n,h) in SOURCES.items()},
        instruction_checks=checks, early_audio_projection=projection, bounded_original_tail_cases=cases,
        historical_events=history,
        boundaries={
            'TLS': '56E141 TlsSetValue;56E15E PTD.thread_id;56E180 ->421F50->virtual callback. No mandatory initial worker wait.',
            'create': '421EC4 requests CREATE_SUSPENDED;421A44 signals node;421A5A resumes worker;421A8E MAIN waits on manager. Creation notification precedes worker user code/TLS.',
            'fade': '49F521 calls422360 only when4DB270 returns0. Two native guards can return1 immediately. Active case stops before the unexecuted volume COM call; no successful active native fade is claimed.',
            'publish': '439E99 enters MAIN event critical section,439EAC/439EB2 store id/pending; this is not OutputDebugString or observer notification. Uncontended lock acquisition need not block.',
            'done': '421FED signals manager before422021->_endthreadex;57554F clears TLS before56E21B ExitThread. An auto-reset event observer can consume the scheduler signal and still cannot pin live TLS.',
            'file': 'CH001 loading reaches normal file APIs, including42ABED CreateFileA. A file API call is not a synchronous debugger-stop or guaranteed observer callback.',
            'parent': 'Static .text1:8396E7 WaitForDebugEvent with [EBP-A28], timeout1000;8396ED return;83BE27/83BE48 Continue using event PID/TID. No current native parent .text1 identity attested here.',
        },
        admission=dict(boundary_semantics_precheck_passed=True, mandatory_initialized_TLS_notification_proved=False,
            ownership_preserving_synchronous_observer_proved=False, original_game_preflight_allowed=False,
            real_NEW_GAME_thread_TLS_exit_added=False, parent_live_code_authenticated=False,
            old_polling_repeated=False, old_relay_repeated=False, helper_controls_repeated=False),
        limits=dict(original_processes_started=0, desktop_inputs=0, screenshots=0,
            platform_calls_executed=0, seconds_per_emulated_case=2, instructions_per_case=2048,
            state_scope='Isolated original tail in synthetic memory; not full state/ABI, replay, or native ownership proof.',
            historical_state_scope='Early ready audio is 282+ seconds before the missing transition; no historical NEW_GAME cause inference.',
            coverage='Named candidate boundaries only; no claim that every transitive game/OS path lacks an event.'),
        conclusion='No qualified observer for this candidate. Do not rerun the menu, lifecycle-only helper, finer polling, or failed relay. A new mechanism must first prove an initialized-TLS stop and original ownership/continuation preservation.',
        formal_progress=dict(complete=2,total=8), seconds=time.perf_counter()-started,
        unicorn_version=unicorn.__version__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(args.out.resolve().parent == ROOT/'analysis' and not args.out.exists(), 'fresh small analysis report')
    report = build()
    encoded = (json.dumps(report, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
    need(len(encoded) <= 128*1024, 'small report retention budget')
    with args.out.open('xb') as stream:
        stream.write(encoded)
    print(json.dumps(dict(path=str(args.out), bytes=len(encoded), sha256=sha(encoded),
                         admission=report['admission'], seconds=report['seconds'])))

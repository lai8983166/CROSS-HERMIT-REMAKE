"""Read-only inventory of already retained PTD evidence; never a free proof.

No WinAPI, process access, native launch or old-file mutation. The allocator
classifier describes a possible original branch, not an observed execution.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
NESTED = (0x24, 0x28, 0x30, 0x38, 0x40, 0x44)
STATIC_LOCALE = 0x761D68
IMAGE_SHA = '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def identity(path):
    raw = Path(path).read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def read_bound(path, digest, compressed_limit, expanded_limit):
    path = Path(path)
    need(0 < path.stat().st_size <= compressed_limit, 'bounded retained file')
    item = identity(path)
    need(item['sha256'] == digest, 'exact retained source SHA')
    if path.suffix == '.gz':
        with gzip.open(path, 'rb') as stream:
            raw = stream.read(expanded_limit + 1)
    else:
        raw = path.read_bytes()
    need(len(raw) <= expanded_limit, 'bounded expanded source')
    return json.loads(raw), item


def ptd_fields(tls):
    raw = bytes.fromhex(tls['PTD_hex'])
    slot = bytes.fromhex(tls['TLS_slot_hex'])
    need(len(raw) == 116 and len(slot) == 4, 'complete original PTD and TLS slot')
    need(struct.unpack('<I', slot)[0] == tls['PTD'] and tls['PTD'] != 0,
         'actual TLS slot points to PTD')
    need(struct.unpack_from('<I', raw)[0] == tls['thread_id'], 'PTD raw owner TID')
    pointers = {hex(off): struct.unpack_from('<I', raw, off)[0] for off in NESTED}
    locale = struct.unpack_from('<I', raw, 0x50)[0]
    return dict(pointer=tls['PTD'], owner_pid=tls['owner_pid'], thread_id=tls['thread_id'],
                TEB=tls['TEB'], TLS_index=tls['TLS_index'], slot=tls['slot'],
                PTD_sha256=hashlib.sha256(raw).hexdigest(), nested_pointers=pointers,
                conditional_0x50=locale, conditional_0x50_is_static=locale == STATIC_LOCALE,
                dynamic_nested_pointers=[v for v in pointers.values() if v] +
                    ([locale] if locale not in (0, STATIC_LOCALE) else []),
                observed_release=False)


def allocator_branch(flags, hook, mode, small_block_membership=None):
    """Potential branch only: never interpret an address or flag as a free."""
    need(all(type(x) is int and 0 <= x <= 0xffffffff for x in (flags, hook, mode)),
         'raw uint32 allocator controls')
    need(small_block_membership is None or type(small_block_membership) is bool,
         'membership must be independently established or unknown')
    if hook:
        branch = 'allocation_hook_result_and_body_unobserved'
    elif flags & 2:
        branch = 'debug_retained_block_branch_no_underlying_free'
    elif mode in (2, 3) and small_block_membership is None:
        branch = 'small_block_membership_unobserved'
    elif mode in (2, 3) and small_block_membership:
        branch = 'CRT_small_block_free_not_per_block_HeapFree'
    else:
        branch = 'HeapFree_candidate_requires_actual_event_and_outcome'
    return dict(potential_branch=branch, actual_branch_observed=False, PTDcleanup=False)


def build(window, school, prefix, image):
    # Existing exact raw-frame/TLS contracts are reused, not redefined here.
    from devtools import terminal_battle_wait_verification as wait
    from devtools import terminal_worker_retention_verification_v2 as retention
    need(hashlib.sha256(image).hexdigest() == IMAGE_SHA, 'fixed original executable')
    need(window['phase'] == 'battle_retreat' and window['error'] is None,
         'actual battle source without collection error')
    need(prefix['accepted'] is False and prefix['worker_retention_verified'] is True
         and prefix['battle_worker_exit0_observed'] is True, 'partial authenticated prefix evidence')
    p = school['probe']; subject = window['subject']; tid = subject['tid']
    need(subject['pid'] == p['pid'], 'same original PID')
    baseline = window['before']; wait.snapshot_contract(window, baseline, baseline, image)
    items = []
    for snap in window['window_snapshots']:
        wait.snapshot_contract(window, snap, baseline, image)
        items.append(ptd_fields(snap['current_TLS']))
    need(items and all(x['thread_id'] == tid for x in items), 'actual same worker PTD observations')
    fingerprints = sorted({x['PTD_sha256'] for x in items})
    pointers = sorted({x['pointer'] for x in items})
    school_groups = {}
    for row in p['samples']:
        for task in row['tasks']:
            tls = task.get('TLS')
            if not tls or tls['PTD'] not in pointers:
                continue
            frame = next(f for f in row['frames'] if f['tid'] == task['thread_id'])
            retention.frozen.owner.verify_frame(frame)
            calls = [f for f in frame['chain'] if f['return_va'] == 0x421F8A]
            need(len(calls) == 1, 'original callback ancestry for current PTD owner')
            retention.frozen.startup.verify_tls(tls, frame, bytes.fromhex(task['header_hex']),
                task['pointer'], task['thread_id'], p['pid'], {'pointer': calls[0]['bp']-0x80}, 2)
            fields = ptd_fields(tls); key = (task['thread_id'], fields['PTD_sha256'])
            group = school_groups.setdefault(key, dict(**fields, node=task['pointer'],
                first_elapsed=row['elapsed'], last_elapsed=row['elapsed'], samples=0))
            group['last_elapsed'] = row['elapsed']; group['samples'] += 1
    return dict(kind='retained_PTD_evidence_inventory_not_release_proof', accepted=False,
        subject=subject, window_snapshots=len(items), unique_PTD_addresses=pointers,
        unique_window_PTD_content_sha256=fingerprints, window_first=items[0], window_last=items[-1],
        owner_observations_at_same_numeric_address=list(school_groups.values()),
        worker_exit=window['worker_exit'],
        missing_actual_release_evidence=[
            'PTD debug allocation header at PTD-0x20 through PTD-1, before invalidation',
            'runtime debug flags7619C0, allocation hook762130, optional thread-exit callback761980',
            'runtime heap80AB28 and heap-mode80AB2C; actual small-block membership/branch',
            'actual PTD/nested allocator release operation and outcome, not numeric address reuse',
            'same live TEB TLS slot becoming zero and actual TlsSetValue result before exit',
            'original node-event/thread-handle object identities and close outcomes, not observer duplicate close'],
        observed_PTD_release=False, observed_TLS_clear=False, original_handle_closure_proved=False,
        full_resource_lifetime_proved=False, PTDcleanup=False, native_execution=False,
        limitations=[
            'Observed zero nested pointers/static locale apply only at captured instants; no final-release-time invariance is inferred.',
            'A successor with the same numeric PTD address is a distinct owner/content observation, not proof of which allocator released the previous block.',
            'HeapFree events alone cannot prove a CRT small-block release, debug-retained block release, TLS clear or full API/CPU/ABI state.',
            'This inventory does not replay or alter the original program and does not authenticate a new native capture.'])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('window', 'window-sha', 'school', 'school-sha', 'prefix-proof', 'prefix-proof-sha', 'out'):
        p.add_argument('--'+name, required=True)
    a = p.parse_args(); out = Path(a.out); need(not out.exists(), 'fresh inventory path')
    implementation = identity(Path(__file__))
    window, wi = read_bound(a.window, a.window_sha, 2<<20, 8<<20)
    school, si = read_bound(a.school, a.school_sha, 16<<20, 192<<20)
    prefix, pi = read_bound(a.prefix_proof, a.prefix_proof_sha, 1<<20, 1<<20)
    need(all(prefix['source_report'][k] == si[k] for k in ('bytes','sha256')), 'prefix binds exact school source')
    need(all(window['school_source_reference'][k] == si[k] for k in ('bytes','sha256')), 'window binds exact school source')
    report = build(window, school, prefix, (ROOT/'analysis/hermit_game.exe').read_bytes())
    report.update(source_window=wi, source_school=si, prefix_proof=pi, implementation=implementation)
    need(identity(Path(__file__)) == implementation, 'inventory implementation unchanged')
    raw = (json.dumps(report, ensure_ascii=False, indent=2)+'\n').encode()
    need(len(raw) <= 64*1024, 'bounded compact inventory')
    with out.open('xb') as stream:
        stream.write(raw)
    print(json.dumps(dict(out=str(out), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), accepted=False)))
    return 2


if __name__ == '__main__':
    raise SystemExit(main())

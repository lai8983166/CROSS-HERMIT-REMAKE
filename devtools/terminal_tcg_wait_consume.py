"""Offline, fail-closed consumer of the self-owned wait observation, never a game proof."""
import argparse
import hashlib
import json
from pathlib import Path
import struct

from devtools.terminal_tcg_compat_context import unpack, source_digest
from devtools.terminal_vm_wait_fixture import image


def differences(a, b, path=''):
    if type(a) is not type(b):
        return [dict(path=path, before=a, after=b)]
    if isinstance(a, dict):
        out = []
        for key in sorted(set(a) | set(b)):
            out += differences(a.get(key), b.get(key), path+'.'+key if path else key)
        return out
    if isinstance(a, list) and len(a) == len(b):
        return sum((differences(x, y, f'{path}[{i}]') for i, (x, y) in enumerate(zip(a, b))), [])
    return [] if a == b else [dict(path=path, before=a, after=b)]


def transition(a, b, phase):
    """RF is never masked. Only CALL ABI volatile low32 / arithmetic flags vary."""
    out = differences(a, b)
    for d in out:
        p = d['path']
        allowed = p in ('eip', 'gpr[4]')  # separately exact-checked targets/stack
        if phase == 'call-ret':
            if p in ('gpr[0]', 'gpr[1]', 'gpr[2]'):
                allowed = int(d['before'], 16) >> 32 == int(d['after'], 16) >> 32
            elif p == 'eflags':
                allowed = (int(d['before'], 16) ^ int(d['after'], 16)) & ~0x8d5 == 0
        d['allowed'] = allowed
    return out


def fx_differences(raw, fx):
    """Architectural FXSAVE32 fields only; reserved bytes/MXCSR_MASK have no raw counterpart."""
    def u(off, size):
        return int.from_bytes(fx[off:off+size], 'little')
    expected = {'fcw': raw['fp_control'], 'fsw': raw['fp_status'],
                'ftw': raw['fp_empty_mask'] ^ 255, 'fop': raw['fop'],
                'fip': int(raw['fip'], 16) & 0xffffffff, 'fcs': raw['fcs'],
                'fdp': int(raw['fdp'], 16) & 0xffffffff, 'fds': raw['fds'],
                'mxcsr': raw['mxcsr']}
    actual = {name: u(off, n) for name, off, n in (
        ('fcw', 0, 2), ('fsw', 2, 2), ('ftw', 4, 1), ('fop', 6, 2),
        ('fip', 8, 4), ('fcs', 12, 2), ('fdp', 16, 4), ('fds', 20, 2), ('mxcsr', 24, 4))}
    for i in range(8):
        lo, hi = raw['fp_physical_low64_high16'][(raw['top']+i) & 7]
        expected[f'st{i}'] = int(lo, 16) | int(hi, 16) << 64
        actual[f'st{i}'] = u(32+16*i, 10)
        lo, hi = raw['xmm_low64_high64'][i]
        expected[f'xmm{i}'] = int(lo, 16) | int(hi, 16) << 64
        actual[f'xmm{i}'] = u(160+16*i, 16)
    return differences(expected, actual)


def consume(observation, result):
    report = dict(accepted=False, original_game_observed=False,
        scope='self-owned WOW64 wait fixture only; no game or replay acceptance',
        fixture_observation_passed=False, checks=[], errors=[], raw64_differences=[], frame_differences=[], fx_differences=[],
        raw64_policy={'call-ret': 'exact EIP/ESP; EAX/ECX/EDX low32 ABI volatile; arithmetic flags 0x8d5 only; everything else exact',
                      'ret-post': 'exact EIP/ESP transition only; all other raw64 fields exact including RF'},
        fx_scope='FXSAVE32 architectural fields; logical ST maps via TOP to physical FP; low32 FIP/FDP; XMM0..7; no reserved-byte or MXCSR_MASK claim')
    def check(name, value):
        report['checks'].append(dict(name=name, passed=bool(value)))
    try:
        if 'value' in result:
            result = result['value']
            if isinstance(result, str):
                result = json.loads(result)
        ready = observation['ready']
        check('unqualified_self_owned', observation['accepted'] is False and result['accepted'] is False and
              result['original_game_observed'] is False and result['kind'] == 'owned_wow64_tcg_wait_fixture')
        check('observer_complete', observation['errors'] == [] and observation['four_wait_returns_observed'] is True and
              observation['host_guest_state_writes'] == 0)
        check('result_ready_identical', result['ready'] == ready)
        template, meta = image()
        patched = bytearray(template)
        for p in meta['patches']:
            address = ready['data'] if p['symbol'] == 'data' else ready['nt_wait']
            struct.pack_into('<I', patched, p['offset'], address+p['addend'])
        check('original_214B_template', len(template) == 214 and ready['template_sha256'] == result['template_sha256'] ==
              hashlib.sha256(template).hexdigest())
        check('relocated_code_exact', bytes.fromhex(ready['code_hex']) == patched and result['code_after'] == ready['code_hex'])
        expected_source = hashlib.sha256(Path(__file__).with_name('terminal_tcg_wait_fixture_v2.cs').read_bytes()).hexdigest()
        check('source_identity', result['source_sha256'] == ready['source_sha256'] == expected_source)
        nt = bytes.fromhex(ready['nt_wait_before'])
        check('nt_wait_exact', len(nt) == 32 and nt[:5] == bytes.fromhex('b804000d00') and nt[5] == 0xba and
              nt[10:15] == bytes.fromhex('ffd2c20c00') and result['nt_wait_before'] == result['nt_wait_after'] == nt.hex())
        check('pc_contract', ready['postcall_pc'] == ready['code']+meta['postcall_offset'] and ready['return_pc'] == ready['nt_wait']+12)
        check('gated_ready_contract', ready['fixture_version'] == 2 and ready['counter_startup_confirmed'] is True and
              ready['counter_native_started'] is False and ready['peer_request_wait_started'] is False and ready['workers_gated_until_go'] is True)
        check('native_results', result['returns'] == [0, 0, 0, 258] and result['signals'] == 3 and result['peer_completed'] is True and
              result['peer_error'] is None and result['error'] is None and result['go_received'] is True and result['counter_native_entered'] == [True, True])
        check('cleanup', result['cleanup_errors'] == [] and result['counter_errors'] == [None, None] and result['counter_affinity_restored'] == [True, True] and
              all(result[k] is True for k in ('fixture_completed', 'workers_stopped', 'handles_closed', 'buffers_released', 'main_affinity_restored', 'watchdog_disarmed')))
        stops = observation['stops']
        expected_labels = [f'{phase}-{i}' for i in range(4) for phase in ('call', 'ret', 'post')]
        check('exact_twelve_stops', [s['label'] for s in stops] == expected_labels)
        if len(stops) != 12:
            raise ValueError('exact twelve stops required')
        final = bytes.fromhex(result['data_hex'])
        check('final_data_size', len(final) == meta['data_bytes'])
        if len(final) != meta['data_bytes']:
            raise ValueError('full final data required')
        check('four_saved_records', int.from_bytes(final[0x200:0x204], 'little') == 4)
        cr3 = stops[0]['states'][0]['cr0_cr2_cr3_cr4'][2]
        fs = stops[0]['states'][0]['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][4]
        for i in range(4):
            group = stops[3*i:3*i+3]
            raws = []
            for phase, stop in zip(('call', 'ret', 'post'), group):
                raw = stop['states'][0]
                recovered = unpack(stop['compat'], expected_cpu=0, expected_vcpus=2, expected_source_sha256=source_digest(raw))
                check(stop['label']+'.lossless_repeat', recovered == raw and stop['repeat_equal'] is True and len(stop['states']) == 2)
                check(stop['label']+'.owner_cr3_fs', raw['cr0_cr2_cr3_cr4'][2] == cr3 and raw['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][4] == fs)
                # v3 saves FS.base+0x20 bytes. Older observations fail closed.
                check(stop['label']+'.owner_identity_raw', stop.get('owner_teb_client_id_hex') == struct.pack('<II', ready['pid'], ready['tid']).hex())
                check(stop['label']+'.code', stop.get('code_hex') == ready['code_hex'])
                check(stop['label']+'.nt_wait', stop['nt_wait'] == nt.hex())
                check(stop['label']+'.timeout', bytes.fromhex(stop['timeout_hex']) == struct.pack('<q', 0 if i == 3 else -20000000))
                data = bytes.fromhex(stop['data_hex'])
                check(stop['label']+'.data', len(data) == 16384 and int.from_bytes(data[0x200:0x204], 'little') == i and data[0x1000:0x1000+0x400*i] == final[0x1000:0x1000+0x400*i])
                check(stop['label']+'.pc', int(raw['eip'], 16) == {'call': ready['postcall_pc']-2, 'ret': ready['return_pc'], 'post': ready['postcall_pc']}[phase])
                raws.append(raw)
            call, ret, post = raws
            args = [ready['event_handle'], 0, ready['timeout_pointer']]
            stacks = [bytes.fromhex(s['stack']) for s in group]
            check(f'round{i}.stack_arguments', all(len(s) == 64 for s in stacks) and stacks[0][:12] == struct.pack('<III', *args) and stacks[1][:16] == struct.pack('<IIII', ready['postcall_pc'], *args))
            check(f'round{i}.ret_stack_unchanged', stacks[1][16:] == stacks[2][:48])
            check(f'round{i}.natural_return', int(ret['gpr'][4], 16) == int(call['gpr'][4], 16)-4 and int(post['gpr'][4], 16) == int(ret['gpr'][4], 16)+16 and int(ret['gpr'][0], 16) == (258 if i == 3 else 0))
            for phase, a, b in (('call-ret', call, ret), ('ret-post', ret, post)):
                diffs = transition(a, b, phase)
                report['raw64_differences'].append(dict(round=i, phase=phase, differences=diffs))
                check(f'round{i}.{phase}.raw64', all(d['allowed'] for d in diffs))
            base = meta['post_record_start']+i*meta['post_record_stride']
            frame = list(struct.unpack_from('<9I', final, base+meta['post_frame_offset']))
            gp = [int(v, 16) & 0xffffffff for v in post['gpr'][:8]]
            # PUSHFD architecturally clears VM/RF in its image; no raw-state mask.
            expected = [gp[7], gp[6], gp[5], (gp[4]-4) & 0xffffffff, gp[3], gp[2], gp[1], gp[0], int(post['eflags'], 16) & ~0x30000]
            fd = differences(expected, frame)
            xd = fx_differences(post, final[base:base+512])
            report['frame_differences'].append(dict(round=i, differences=fd))
            report['fx_differences'].append(dict(round=i, differences=xd))
            check(f'round{i}.pushfd_pushad', not fd)
            check(f'round{i}.fxsave', not xd)
    except (KeyError, ValueError, TypeError, IndexError, struct.error) as exc:
        report['errors'].append(type(exc).__name__+': '+str(exc))
    report['fixture_observation_passed'] = not report['errors'] and bool(report['checks']) and all(c['passed'] for c in report['checks'])
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('observation', type=Path)
    parser.add_argument('result', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    output = consume(json.loads(args.observation.read_bytes()), json.loads(args.result.read_bytes()))
    output['inputs'] = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (args.observation, args.result)}
    with args.out.open('x', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    print(json.dumps({'fixture_observation_passed': output['fixture_observation_passed'], 'errors': output['errors'], 'failed_checks': [c['name'] for c in output['checks'] if not c['passed']]}))

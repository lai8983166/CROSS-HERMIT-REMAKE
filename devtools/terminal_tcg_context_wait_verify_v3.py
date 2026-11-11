"""Strict ordered witness and filter validation above immutable v2 semantics.

Only the pinned local kernel is read, with a 16 MiB limit. This is an owned
fixture evidence verifier, never original-game or whole-machine acceptance.
"""
import hashlib
import json
import re
from pathlib import Path
from devtools.terminal_tcg_context_wait_verify_v2 import verify as verify_v2

ROOT = Path(__file__).resolve().parents[1]
KERNEL = ROOT / '.venv-audit/native-worker/tcg-wow64-path-v1/System32-ntoskrnl.exe'
KERNEL_SHA = '5669b9b8bfcf20f08b7d1d65dc2deccbf836279c0e3f66722d72ad33ee7f672a'
PLAN_CANONICAL_SHA = '970a7e0367e61607af8dcfcd8aa6c011c2317afbe6d471243912f31cf230be0a'
POINTS = ['call', 'selector13', 'system-entry', 'kernel-entry', 'kernel-clear-before',
          'kernel-clear-after', 'native-return', 'shadow-predecessor', 'return-branch',
          'r9-after', 'ret32', 'consumer']
STEPS = ['syscall', *['pxor-' + str(i) for i in range(6)], 'mov-ss', 'load-r9d', 'ret12']
COUNTERS = ['accepted', 'rejected', 'cpu_rejected', 'cr3_rejected', 'r13_rejected']
HEX = re.compile(r'[0-9a-f]{16}\Z')


def verify(trace, plan):
    result = dict(accepted=False, original_game=False, full_windows_admission=False,
                  same_wait_writes_verified=False, exported_endpoint_verified=False,
                  checks=[], errors=[])
    def require(name, value):
        result['checks'].append(dict(name=name, passed=bool(value)))
        if not value:
            raise ValueError(name)
    def pc(point):
        return int(point['states'][0]['eip'], 16)
    try:
        require('pinned_plan', hashlib.sha256(json.dumps(plan, sort_keys=True,
                separators=(',', ':')).encode()).hexdigest() == PLAN_CANONICAL_SHA)
        require('ordered_points', [p['label'] for p in trace['points']] == POINTS)
        require('ordered_steps', [p['label'] for p in trace['steps']] == STEPS)
        require('all_step_cpu0_replies', all(s['reply'] == 'T05thread:01;' for s in trace['steps']))
        points = {p['label']:p for p in trace['points']}
        steps = {s['label']:s for s in trace['steps']}
        call = points['call']; ready = trace['ready']; wow = call['extra']['wow_base']
        require('call_pc_opcode', pc(call) == ready['postcall_pc'] - 2 and
                call['code_hex'].startswith('ffd0') and
                int(call['states'][0]['gpr'][0], 16) == ready['nt_wait'])
        private = bytes.fromhex(call['boundary']['private_code'])
        offset = pc(call) - ready['code']
        require('call_in_private_bytes', 0 <= offset <= len(private)-2 and private[offset:offset+2] == bytes.fromhex('ffd0'))
        selector = points['selector13']
        require('selector13_pc_saved_return', pc(selector) == wow + 0x1b46 and
                len(selector['extra']['saved_return']) == 8 and
                int.from_bytes(bytes.fromhex(selector['extra']['saved_return']), 'little') == ready['return_pc'])
        context_bytes = bytes.fromhex(selector['extra']['context_bytes'])
        require('selector_context_memory', len(context_bytes) == 0x240 and
                context_bytes[0xbc:0xc0].hex() == selector['extra']['saved_return'])
        # Bind each observed WOW64 point's original bytes to the pinned image slice.
        code = bytes.fromhex(plan['wow_text_hex'])
        for label in ('selector13', 'system-entry', 'native-return', 'shadow-predecessor', 'return-branch', 'r9-after'):
            point = points[label]; offset = pc(point) - wow - plan['wow_text_rva']
            observed = bytes.fromhex(point['code_hex'])
            # The pinned slice ends shortly after SYSCALL. Match the complete
            # available overlap, with at least the instruction's three bytes.
            available = min(len(observed), len(code)-offset)
            require('pinned_wow_bytes_' + label, len(observed) == 32 and offset >= 0 and available >= 3 and
                    observed[:available] == code[offset:offset+available])
        require('kernel_size_bound', KERNEL.stat().st_size <= 16*1024*1024)
        with KERNEL.open('rb') as stream:
            kernel = stream.read(16*1024*1024 + 1)
        require('pinned_kernel', len(kernel) <= 16*1024*1024 and hashlib.sha256(kernel).hexdigest() == KERNEL_SHA and plan['kernel_sha256'] == KERNEL_SHA)
        entry = points['kernel-entry']; kb = entry['extra']['kernel_base']
        sig = bytes.fromhex(entry['extra']['signature'])
        require('kernel_signature_shape', len(sig) == 64 and entry['code_hex'] == sig[:32].hex())
        mapped = []
        for sec in plan['kernel_sections']:
            offset = pc(entry) - kb - sec['rva']
            if 0 <= offset <= sec['size']-64:
                mapped.append(sec['raw']+offset)
        require('kernel_signature_mapping', len(mapped) == 1 and kernel[mapped[0]:mapped[0]+64] == sig)
        # Require the entry signature to identify a unique image location.
        require('kernel_signature_unique', kernel.count(sig) == 1)
        clear = points['kernel-clear-before']; mapped = []
        for sec in plan['kernel_sections']:
            offset = pc(clear) - kb - sec['rva']
            if 0 <= offset <= sec['size']-32:
                mapped.append(sec['raw']+offset)
        require('kernel_clear_original_bytes', len(mapped) == 1 and
                bytes.fromhex(clear['code_hex']) == kernel[mapped[0]:mapped[0]+32])
        fs = trace['context_filter']
        fields = {'schema', 'active', 'poisoned', 'reason', 'cpu', 'cr3', 'r13',
                  'budget', 'points', *COUNTERS}
        expected_points = [[wow+0x1b46], [wow+0x1b46], [wow+0x1cf1, wow+0x1cf4],
            [kb+x for x in plan['kernel_clear_rvas']], [wow+0x1cf3],
            [wow+0x1b7f, wow+0x1b91], [ready['return_pc']], [ready['return_pc']]]
        require('filter_row_count', len(fs) == len(expected_points))
        previous = dict.fromkeys(COUNTERS, 0)
        for i, f in enumerate(fs):
            require('filter_schema_' + str(i), set(f) == fields and
                    f['schema'] == 'tcg-context-v1' and f['active'] is (i < len(fs)-1) and
                    f['poisoned'] is False and f['reason'] == '' and
                    type(f['cpu']) is int and f['cpu'] == 0 and
                    all(isinstance(f[k], str) and HEX.fullmatch(f[k]) for k in ('cr3', 'r13')))
            require('filter_budget_' + str(i), f['budget'] == dict(matches=1000000, seconds=60, points=32) and
                    all(type(v) is int for v in f['budget'].values()))
            require('filter_counters_' + str(i), all(type(f[k]) is int and previous[k] <= f[k] <= 1000000 for k in COUNTERS) and
                    f['accepted'] + f['rejected'] <= 1000000 and
                    all(f[k] <= f['rejected'] for k in COUNTERS[2:]) and
                    f['rejected'] <= sum(f[k] for k in COUNTERS[2:]))
            require('filter_points_' + str(i), isinstance(f['points'], list) and
                    all(isinstance(v,str) and HEX.fullmatch(v) for v in f['points']) and
                    len(f['points']) == len(set(f['points'])) and
                    sorted(int(v,16) for v in f['points']) == sorted(expected_points[i]))
            require('filter_accept_progress_' + str(i), f['accepted'] == [0,0,1,2,3,4,5,6][i])
            previous = {k:f[k] for k in COUNTERS}
        require('filter_initial_counters', all(fs[0][k] == fs[1][k] == 0 for k in COUNTERS))
        prior = verify_v2(trace, plan)
        result['v2'] = prior
        require('frozen_v2_contract', prior['same_wait_writes_verified'] is True)
        result['same_wait_writes_verified'] = result['exported_endpoint_verified'] = True
        result['scope'] = prior['scope']
    except (KeyError, ValueError, TypeError, IndexError, OSError) as exc:
        result['errors'].append(type(exc).__name__ + ': ' + str(exc))
    return result

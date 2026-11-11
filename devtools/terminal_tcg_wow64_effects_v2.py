"""Validate the complete exported raw64 schema before narrow v1 semantics."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from devtools.terminal_tcg_wow64_effects import verify as effects

HEX = re.compile(r'[0-9a-f]{16}\Z')
SCALARS = ('eip', 'eflags', 'hflags', 'efer', 'fip', 'fdp')
ARRAYS = {'gpr': (16, 0), 'segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt': (10, 4),
          'cr0_cr2_cr3_cr4': (4, 0), 'dr0_dr1_dr2_dr3_dr6_dr7': (6, 0),
          'fp_physical_low64_high16': (8, 2), 'xmm_low64_high64': (16, 2)}
INTS = {'fp_control': 65535, 'fp_status': 65535, 'top': 7, 'fp_empty_mask': 255,
        'fop': 2047, 'fcs': 65535, 'fds': 65535, 'mxcsr': 0xffffffff}
META = {'schema', 'fullstate_accepted', 'vp_stopped', 'cpu', 'target_bits', 'dr4_dr5_policy'}


def state_ok(state, cpu):
    if set(state) != META | set(SCALARS) | set(ARRAYS) | set(INTS):
        return False
    if (state['schema'] != 'tcg-state-v1' or state['fullstate_accepted'] is not False or
        type(state['cpu']) is not int or state['cpu'] != cpu or state['target_bits'] != 64 or
        state['vp_stopped'] != [{'cpu': 0, 'stopped': True}, {'cpu': 1, 'stopped': True}] or
        state['dr4_dr5_policy'] != 'DE=0 aliases DR6/7; DE=1 undefined, not independent slots'):
        return False
    hex_ok = lambda v: isinstance(v, str) and HEX.fullmatch(v) is not None
    if not all(hex_ok(state[k]) for k in SCALARS):
        return False
    if not all(type(state[k]) is int and 0 <= state[k] <= limit for k, limit in INTS.items()):
        return False
    for key, (length, width) in ARRAYS.items():
        value = state[key]
        if not isinstance(value, list) or len(value) != length:
            return False
        if width:
            if not all(isinstance(v, list) and len(v) == width and all(map(hex_ok, v)) for v in value):
                return False
        elif not all(map(hex_ok, value)):
            return False
    return True


def verify(trace, plan):
    try:
        for group in ('points', 'steps'):
            labels = [x['label'] for x in trace[group]]
            if len(labels) != len(set(labels)):
                raise ValueError('duplicate ' + group + ' labels')
            for entry in trace[group]:
                for key in (('states',) if group == 'points' else ('before', 'after')):
                    states = entry[key]
                    if not isinstance(states, list) or len(states) != 2 or not all(state_ok(s, i) for i, s in enumerate(states)):
                        raise ValueError('incomplete or invalid CPU state at ' + entry['label'])
    except (KeyError, ValueError, TypeError) as exc:
        return dict(accepted=False, cr2_explained=False, consumer_connected_in_this_trace=False,
                    local_effects_verified=False, checks=[], errors=[str(exc)])
    result = effects(trace, plan)
    result['complete_exported_schema_checked'] = True
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('trace', type=Path)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = verify(json.loads(args.trace.read_bytes()), json.loads(args.plan.read_bytes()))
    result['inputs'] = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (args.trace, args.plan)}
    with args.out.open('x', encoding='utf8') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps({k: v for k, v in result.items() if k not in ('inputs', 'checks')}))
    raise SystemExit(0 if result['local_effects_verified'] else 1)

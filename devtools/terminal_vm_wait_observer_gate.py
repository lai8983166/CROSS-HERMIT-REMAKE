"""Reject the unqualified VMware hidden-breakpoint wait observer before launch.

Frozen transport versions reproduce historical preflights; they are not a
production wait observer. A different platform/mechanism needs fresh bounded
qualification, including full WOW64 state and normal continuation/cleanup.
"""
import hashlib
import json
from pathlib import Path
from devtools.vmware_rsp_state import decode_frame

ROOT = Path(__file__).resolve().parents[1]
FAILURE = 'analysis/terminal-wait-vm-monitor-breakpoint-failure-v1-20261110.json'
FAILURE_SHA = 'dd040cee4ca8427525890dccb53aaed7749c82820ad807f31fc77146ad2310b5'


def witness():
    raw = (ROOT / FAILURE).read_bytes()
    if hashlib.sha256(raw).hexdigest() != FAILURE_SHA:
        raise ValueError('fixed native monitor failure identity')
    report = json.loads(raw)
    rows = report['transcript']
    payloads = []
    for row in rows:
        if row['direction'] not in ('send', 'receive'):
            continue
        payload = bytes.fromhex(row['payload_hex'])
        if row['direction'] == 'receive' and decode_frame(bytes.fromhex(row['wire_hex'])) != payload:
            raise ValueError('original monitor reply checksum and payload')
        payloads.append((row['direction'], payload))
    lines = [x['text'] for x in report['platform_failure']['original_log_lines']]
    if (len(payloads) != 5 or payloads[0] != ('send', b'?')
            or payloads[1][0] != 'receive' or not payloads[1][1].startswith(b'T05')
            or payloads[2] != ('send', b'Z1,772b3bfc,1')
            or payloads[3] != ('receive', b'OK') or payloads[4] != ('send', b'c')
            or 'wait_return' in report or report['original_game_started'] is not False
            or not any('Monitor Mode: ULM' in x for x in lines)
            or sum('PANIC: NOT_IMPLEMENTED' in x and 'debugReg.c:287' in x for x in lines) != 2):
        raise ValueError('complete bounded incompatible-monitor witness')
    return dict(source=FAILURE, sha256=FAILURE_SHA, accepted=False,
                hidden_breakpoint_request_acknowledged=True,
                actual_wait_return_observed=False, fullstate=False, fullABI=False,
                original_game_observed=False, native_wait_monitor_supported=False,
                reason='VMware 16 build 16894299 ULM monitor panicked after hidden breakpoint activation',
                next_requirement='Qualify a non-mutating exact-return observer on a supported isolated platform first')


def require_supported_monitor():
    raise RuntimeError('Native VMware wait observer is disabled: ' + FAILURE
                       + '; do not retry hidden breakpoints or substitute INT3 on the original game')


if __name__ == '__main__':
    print(json.dumps(witness(), indent=2))

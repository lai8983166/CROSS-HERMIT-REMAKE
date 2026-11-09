"""Reject the proven incompatible injected-trap observer before native launch."""
from pathlib import Path
import gzip
import hashlib
import json
import struct

ROOT=Path(__file__).resolve().parents[1]
FAILURE='analysis/terminal-wait-native-probe-relay-v5-20261109.json.gz'
FAILURE_SHA='6ee170b32160801bcb0bf28dc73044a235985c23421f92287d1e1c3ff99d7aaf'


def witness():
    data=(ROOT/FAILURE).read_bytes()
    if hashlib.sha256(data).hexdigest()!=FAILURE_SHA:raise ValueError('fixed observer failure source identity')
    d=json.loads(gzip.decompress(data));p=d['probe'];r=p['relay'];life=d['lifecycle']['lifetime']
    replies=r['original_child_replies']
    if (len(r['hits'])!=1 or r['hits'][0]['target']!=0x422360 or len(replies)!=1
        or replies[0]['original_continue_status']!=0x80010001
        or struct.unpack_from('<I',bytes.fromhex(replies[0]['parent_stack_hex']),12)[0]!=0x80010001
        or r.get('parent_exit_during_scope')!=0x4000001E or not life['forced_termination']
        or life['members_after_cleanup']):
        raise ValueError('complete bounded incompatible-observer witness')
    return dict(source=FAILURE,sha256=FAILURE_SHA,bytes=len(data),accepted=False,
        first_observed_instruction=0x422360,observed_wait_return=False,
        original_parent_reply=0x80010001,parent_exit_during_scope=0x4000001E,
        child_exit_queried_only_after_emergency_cleanup=True,forced_Job_cleanup=True,
        native_wait_relay_supported=False,
        next_requirement='Use an observation mechanism that does not inject #DB into the protected original; do not rewrite original debugger replies or infer full trace from sparse samples.')


def require_supported_relay():
    # Intentionally unconditional: the fixed incompatible path must not be
    # retried under a different output label. A different mechanism needs its
    # own bounded preflight and evidence, not an allow-failure CLI switch.
    raise RuntimeError('Native parent hardware relay is disabled: protected original forwarded #DB and exited in '+
        FAILURE+'; continuous waits and two-case full replay are not ready')


if __name__=='__main__':print(json.dumps(witness(),indent=2))

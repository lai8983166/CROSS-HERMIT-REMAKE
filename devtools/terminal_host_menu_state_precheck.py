"""Replay the scheduling gate against fixed recorded bytes; never native input."""
import gzip
import hashlib
import json
from pathlib import Path
from devtools.terminal_menu_state_gate import MenuGate, MENU
from devtools import terminal_menu_transition_contract as contract

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'analysis/terminal-host-menu-dxgi-v2-20261112.json.gz'
SHA = '0598bf575f20a86daee78fd81c2e9044686955e40d325eeda36e7f99f538f663'


def identity(path):
    data = (ROOT/path).read_bytes()
    return dict(path=path,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())


def precheck():
    source = identity(SOURCE)
    if source['sha256'] != SHA:
        raise ValueError('fixed recorded source changed')
    r = json.loads(gzip.decompress((ROOT/SOURCE).read_bytes()))
    for item in r['implementations']+[r['host_preflight']['source_implementation'],
                                      r['host_preflight']['capture_implementation']]:
        if identity(item['path']) != item:
            raise ValueError('recorded implementation changed: '+item['path'])
    if r['probe']['collector_input_actions'] or r['host_preflight']['successor_observed']:
        raise ValueError('expected fixed no-input failed menu source')
    rows = r['probe']['samples']
    gate = MenuGate()
    eligible = next(s for s in rows if gate.observe(s,s['elapsed']))
    gate.claim()
    retired = next(s for s in rows if s['elapsed'] > eligible['elapsed']
                   and all(t['vtable'] != MENU for t in s['tasks']))
    raw = contract.read_source()
    hit = contract.original_hit_test(raw,318,508)
    held = contract.original_selection_gate(raw,0,0,1)
    release = contract.original_selection_gate(raw,0,1,0)
    dispatch = contract.original_dispatch(raw,0)
    assert hit['selection'] == 0 and not held['accepted'] and release['accepted']
    return dict(accepted=False,offline_precheck_passed=True,game_started=False,
        desktop_accessed=False,input_submitted=False,formal_progress='2/8',source=source,
        original_source_sha256=contract.SOURCE_SHA,recorded_implementations_unchanged=True,
        hypothetical_input_eligibility=dict(sample=eligible['index'],elapsed=eligible['elapsed'],
            owner=list(gate.owner)),observed_menu_retired=dict(sample=retired['index'],
            elapsed=retired['elapsed'],vtables=[hex(t['vtable']) for t in retired['tasks']]),
        observed_margin_seconds=retired['elapsed']-eligible['elapsed'],
        original_blocks=dict(hit_test=hit,held=held,release=release,dispatch=dispatch),
        limitations=['Recorded row timing is not a new native click or handoff',
            'Live ownership, coordinates and countdown require a fresh authorized run',
            'New input receipt semantics require independent verification; old verifier stays strict',
            'No full graphics, wait/result, resource/PTD or battle-exit acceptance'])


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    report=precheck()
    if args.out:
        if not args.out.resolve().is_relative_to(ROOT/'analysis'):
            raise ValueError('F-project evidence path required')
        with args.out.open('x',encoding='utf8') as stream:
            json.dump(report,stream,indent=2)
    print(json.dumps(report))

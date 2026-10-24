"""Independent coordinate oracle plus fresh original-code/full-memory reproduction."""
import argparse
import gzip
import json
import struct
from tools.battle_pathfinding import source_contract, oracle, corpus
from tools.battle_pathfinding_emulation import ROOT, PathMachine, PACKET, MAP, HEADER, TERR, OCC, OCC_PTR, OBJECT, LINKS, NODES, INDEX, REGIONS, sha, need


def verify_case(row, replay=False):
    model = oracle(row['input'])
    for field in ('result', 'waypoints', 'popped', 'reopened', 'improved_open'):
        need(row[field] == model[field], 'independent original path rule '+field+' '+row['input']['name'])
    need(not row['game_function_results_stubbed'] and not row['unit_coordinates_updated'] and not row['OS_input_submitted'], 'isolated execution scope')
    raw = bytes.fromhex(row['packet_hex'])
    need(len(raw) == 236, 'complete path packet')
    expected = bytearray(236)
    struct.pack_into('<HH', expected, 24, 0xFFFF, 0xFFFF)
    expected[28:30] = b'\xff\xff'
    c = row['input']
    if c['kind'] == 'search' or row['result'] == 1:
        dest = c['goal'] if c['kind'] == 'search' else model['waypoints'][-1]
        struct.pack_into('<HH', expected, 24, *dest)
    if row['result'] == 1:
        if c['kind'] != 'search' or not row['popped']: expected[28:30] = bytes(c['start'])
        struct.pack_into('<H', expected, 32, len(model['waypoints']))
        for i, point in enumerate(model['waypoints']): expected[34+i*2:36+i*2] = bytes(point)
    need(raw[24:] == expected[24:], 'independent complete packet body')
    if not model['limit_hit']: need(raw[:24] == expected[:24], 'clean copied open/closed packet heads')
    consume = row['consume']
    if row['result'] == 1:
        need(len(consume) == len(model['waypoints'])+2, 'two repeated end-of-path tests')
        for i, rec in enumerate(consume):
            if i < len(model['waypoints']):
                need((rec['result'], rec['x'], rec['y'], rec['cursor']) == (0, *model['waypoints'][i], i+1), 'original next point returns zero')
            else:
                need((rec['result'], rec['x'], rec['y'], rec['cursor']) == (1, 0xA55A, 0x5AA5, len(model['waypoints'])), 'original exhausted path preserves coordinates')
    else: need(not consume, 'failed/limited search is not consumed')
    for rec in row['calls']+consume:
        need(rec['ESP_after'] == rec['ESP_before']+4+4*len(rec['args']), 'each original root ABI')
        need(rec['instructions'] > 0, 'original root actually executed')
    for key in ('initial', 'after_search', 'final'):
        snap = row[key]
        need([(b['pointer'], b['bytes']) for b in snap] == list(REGIONS), 'exact complete mapped ownership')
        need(len({b['pointer'] for b in snap}) == len(snap), 'unique complete memory regions')
        need(all(len(bytes.fromhex(b['hex'])) == b['bytes'] for b in snap), 'full memory byte count')
    for before, middle, after in zip(row['initial'], row['after_search'], row['final']):
        need((before['pointer'], before['bytes']) == (middle['pointer'], middle['bytes']) == (after['pointer'], after['bytes']), 'stable map layout')
        if before['pointer'] in (MAP, HEADER, TERR, OCC, OCC_PTR): need(before == middle == after, 'entire read-only map/terrain/occupancy')
    need(not row['ownership_final'][0]['links'] and not row['ownership_final'][1]['links'], 'original supplemental recycling')
    need(bool(row['ownership_after_search'][0]['links'] or row['ownership_after_search'][1]['links']) == (not model['workspace_clean']), '1001 limit retains actual work lists')
    if model['cost'] is not None:
        def memory(at, size):
            for block in row['after_search']:
                if block['pointer'] <= at and at+size <= block['pointer']+block['bytes']:
                    offset = at-block['pointer']; return bytes.fromhex(block['hex'])[offset:offset+size]
            raise ValueError('source node belongs to complete ownership')
        def word(at): return struct.unpack('<I', memory(at, 4))[0]
        w = len(c['grid'][0]); link = word(INDEX+4*(c['goal'][1]*w+c['goal'][0]))
        need(LINKS <= link < LINKS+w*len(c['grid'])*12 and (link-LINKS) % 12 == 0, 'actual goal node owns pool link')
        node = word(link+8)
        need(NODES <= node < NODES+w*len(c['grid'])*28 and (node-NODES) % 28 == 0, 'actual goal data owns pool slot')
        need(word(node+8) == model['cost'], 'independent goal cumulative cost')
    if replay: need(PathMachine(c).run() == row, 'fresh original instruction/write/full-memory reproduction')
    return dict(name=c['name'], result=row['result'], waypoints=row['waypoints'], popped_nodes=len(row['popped']),
                reopened=row['reopened'], improved_open=row['improved_open'], instructions=row['instructions'], writes=row['writes'],
                expansion_limit_hit=model['limit_hit'], cost=model['cost'], full_memory_and_trace_reproduced=replay,
                independent_coordinate_model=True, actual_unit_movement=False)


def verify(path, replay=True):
    raw = path.read_bytes(); report = json.loads(gzip.decompress(raw))
    need(report['schema_version'] == 1 and report['source_contract'] == source_contract(), 'current original source/constant identity')
    need(not report['R3_complete'] and not report['R4_complete'] and not report['R6_complete'], 'milestone scope preserved')
    cases = report['cases']
    need([r['input'] for r in cases] == corpus(), 'complete exact independent declared corpus')
    proof = []
    for row in cases:
        proof.append(verify_case(row, replay)); print('verified', row['input']['name'], flush=True)
    return dict(schema_version=1, source_report=dict(path=path.relative_to(ROOT).as_posix(), bytes=len(raw), sha256=sha(raw)),
                verifier_sha256=sha((ROOT/'tools/battle_pathfinding_verification.py').read_bytes()),
                implementation_sha256={p: sha((ROOT/p).read_bytes()) for p in ('tools/battle_pathfinding.py', 'tools/battle_pathfinding_emulation.py', 'tools/battle_pathfinding_verification.py')},
                case_count=len(proof), cases=proof, original_instructions=sum(r['instructions'] for r in proof),
                original_writes=sum(r['writes'] for r in proof), independently_modeled=True,
                complete_memory_instruction_write_trace_replayed=replay, R3_complete=False, R4_complete=False, R6_complete=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--report', required=True); p.add_argument('--out', required=True)
    a = p.parse_args(); out = ROOT/a.out; need(not out.exists(), 'fresh immutable proof output')
    result = verify(ROOT/a.report)
    out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf8', newline='\n')

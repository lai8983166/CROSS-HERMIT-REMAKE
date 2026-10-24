"""Independent whole-unit model and fresh original AI/movement execution proof."""
import argparse
import gzip
import json
from tools.battle_unit_movement import Model, corpus
from tools.battle_unit_movement_emulation import ROOT, UNIT, CTRL, REGIONS, MovementMachine, source_contract, need, sha


def verify_case(row, replay=True):
    c = row['input']; contract = source_contract(); model = Model(c, contract)
    need(row['path_hex'] == model.path_hex, 'independent original path packet')
    need(not row['game_or_math_results_stubbed'] and not row['OS_input_submitted'] and not row['host_unit_coordinates_changed_after_initialization'], 'isolated original code scope')
    need(len(row['roots']) == 2 and [r['entry'] for r in row['roots']] == [0x437C90, 0x437E40], 'only path initialization/search audit roots')
    need(1 <= len(row['steps']) <= c['frames'], 'bounded actual AI calls')
    events = {}; expected_stop = 'frame_budget'; moved = 0
    for i, step in enumerate(row['steps']):
        need(step['index'] == i and step['before_hex'] == model.unit.hex(), 'continuous whole-unit input '+c['name']+' '+str(i))
        need(len(step['calls']) == 1 and step['calls'][0]['entry'] == 0x476680 and step['calls'][0]['receiver'] == CTRL and step['calls'][0]['args'] == [UNIT, 0], 'one original AI root, no host helper scheduling')
        before = bytes(model.unit); model.step()
        need(step['after_hex'] == model.unit.hex(), 'independent complete unit output '+c['name']+' '+str(i))
        for e in model.last_events: events[e] = events.get(e, 0)+1
        moved += before[0x2EC:0x2F4] != model.unit[0x2EC:0x2F4]
        phase = model.get(0x293, 'B'); need(step['phase'] == phase, 'original AI phase')
        if phase in (3, 4, 8):
            expected_stop = {3:'arrived', 4:'retry_boundary', 8:'next_tile_blocked'}[phase]
            need(i == len(row['steps'])-1, 'no extra AI roots beyond accepted boundary')
    need(row['stop'] == expected_stop, 'honest movement stop reason')
    need(row['original_coordinate_write_count'] == moved*2, 'original coordinate writes distinguish stationary/blocked cases')
    if expected_stop == 'frame_budget': need(len(row['steps']) == c['frames'], 'full declared frame budget')
    for key in ('initial', 'final'):
        need([(b['pointer'], b['bytes']) for b in row[key]] == list(REGIONS), 'complete exact movement regions')
        need(all(len(bytes.fromhex(b['hex'])) == b['bytes'] for b in row[key]), 'complete mapped byte lengths')
    for before, after in zip(row['initial'], row['final']):
        a, b = bytes.fromhex(before['hex']), bytes.fromhex(after['hex'])
        if before['pointer'] == CTRL:
            offset = UNIT-CTRL
            need(a[:offset] == b[:offset] and a[offset+0x520:] == b[offset+0x520:], 'other 249 units/controller/map unchanged')
            need(b[offset:offset+0x520] == model.unit, 'complete final unit inside controller snapshot')
        elif before['pointer'] not in (0x10000000, 0x10600000, 0x10700000, 0x10800000, 0x10A00000):
            need(a == b, 'read-only terrain/records/animation and unused buffers')
    for call in row['roots']+[v for step in row['steps'] for v in step['calls']]+[row['cleanup']]:
        need(call['ESP_after'] == call['ESP_before']+4+4*len(call['args']), 'actual original ESP/ret convention')
        need(call['cpu_after']['EIP'] == 0x10B00000 and call['instructions'] > 0, 'original root naturally returned')
        for reg in ('EBX','ESI','EDI','EBP'): need(call['cpu_before'][reg] == call['cpu_after'][reg], 'original callee-saved '+reg)
    need(not row['final_ownership'][0]['links'] and not row['final_ownership'][1]['links'], 'source workspace cleared')
    if replay: need(MovementMachine(c).run() == row, 'fresh full-memory and instruction/write trace reproduction')
    return dict(name=c['name'], AI_calls=len(row['steps']), movement_calls=events.get('move',0), position_changing_calls=moved,
                helper_events=events, stop=row['stop'], final_position_fixed=[model.get(0x2EC,'i'),model.get(0x2F0,'i')],
                final_cursor=model.get(0x3FE,'H'), path_points=model.get(0x400,'H'), instructions=row['instructions'], writes=row['writes'],
                whole_unit_independent_model=True, all_memory_and_trace_reproduced=replay, complete_world_frame=False)


def verify(path):
    raw = path.read_bytes(); report = json.loads(gzip.decompress(raw))
    need(report['source_contract'] == source_contract(), 'original code/constant/source identity')
    need(all(report[k] is False for k in ('R3_complete','R4_complete','R6_complete')), 'milestone remains incomplete')
    need([r['input'] for r in report['cases']] == corpus(), 'entire declared independent corpus')
    rows = []
    for row in report['cases']:
        rows.append(verify_case(row)); print('verified',row['input']['name'],flush=True)
    return dict(schema_version=1, source_report=dict(path=path.relative_to(ROOT).as_posix(), bytes=len(raw), sha256=sha(raw)),
                case_count=len(rows), cases=rows, original_instructions=sum(r['instructions'] for r in rows), original_writes=sum(r['writes'] for r in rows),
                implementation_sha256={p:sha((ROOT/p).read_bytes()) for p in ('tools/battle_unit_movement.py','tools/battle_unit_movement_emulation.py','tools/battle_unit_movement_verification.py')},
                complete_whole_unit_model_and_all_memory_trace=True, original_AI_phases=[7,8,9], R3_complete=False,R4_complete=False,R6_complete=False)


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    out=ROOT/a.out;need(not out.exists(),'fresh immutable proof path')
    out.write_text(json.dumps(verify(ROOT/a.report),indent=2)+'\n',encoding='utf8',newline='\n')

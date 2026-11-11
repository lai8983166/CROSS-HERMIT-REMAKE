"""Strict CR2 event continuity, separate from full-state/game acceptance.

The backend identity and writer coverage must be independently authenticated.
A self-consistent JSON digest is integrity checking, not a trusted signature.
"""
import hashlib
import json
import re
from devtools.terminal_tcg_wow64_effects_v2 import state_ok

HEX = re.compile('[0-9a-f]{16}\\Z')


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate event JSON key')
        result[key] = value
    return result


def verify(arm, end, start_states, end_states):
    result = dict(accepted=False, full_state_verified=False, windows_admitted=False,
                  cr2_chain_verified=False, errors=[])
    def require(value, message):
        if not value:
            raise ValueError(message)
    def integer(value, minimum=0):
        return type(value) is int and value >= minimum
    def hex64(value):
        return isinstance(value, str) and HEX.fullmatch(value) is not None
    def state_valid(state, cpu):
        return (state_ok(state, cpu) and type(state['target_bits']) is int and
                all(type(v['cpu']) is int and v['stopped'] is True for v in state['vp_stopped']))
    try:
        require(integer(arm['window'], 1) and end['window'] == arm['window'] and
                type(end['window']) is int, 'window identity')
        for payload, phase in ((arm, 'arm'), (end, 'end')):
            require(payload['schema'] == 'tcg-cr2-ledger-v1' and payload['phase'] == phase, 'schema/phase')
            require(payload['poisoned'] is False and payload['overflow'] is False and
                    payload['poison_reason'] == '', 'poison/overflow')
            require(integer(payload['elapsed_ns']) and payload['elapsed_ns'] < 60_000_000_000,
                    'window deadline')
            require(payload['budget'] == dict(records=65536, bytes=16777216, seconds=60) and
                    all(type(v) is int for v in payload['budget'].values()), 'budget')
            require(isinstance(payload['events_json'], str), 'event encoding')
            encoded = payload['events_json'].encode('utf8')
            require(integer(payload['bytes']) and payload['bytes'] == len(encoded) <= 16777216, 'byte count')
            require(payload['events_sha256'] == hashlib.sha256(encoded).hexdigest(), 'event digest')
            events = json.loads(encoded, object_pairs_hook=unique_object)
            require(isinstance(events, list) and integer(payload['count']) and
                    len(events) == payload['count'] <= 65536, 'event count')
        require(arm['count'] == 0 and arm['events_json'] == '[]', 'empty ARM')
        require(arm['elapsed_ns'] == 0 and arm['end'] == [], 'ARM boundary')
        require(end['start'] == arm['start'], 'start boundary changed')
        require(len(start_states) == len(end_states) == len(end['start']) == len(end['end']) == 2, 'CPU count')
        values, counters = [], []
        for cpu in range(2):
            for boundary, states in ((end['start'], start_states), (end['end'], end_states)):
                row = boundary[cpu]
                require(type(row['cpu']) is int and row['cpu'] == cpu, 'boundary CPU')
                require(state_valid(row['state'], cpu) and row['state'] == states[cpu], 'boundary full exported state')
                require(hex64(row['cr2']) and row['cr2'] == states[cpu]['cr0_cr2_cr3_cr4'][1], 'boundary CR2')
                require(integer(row['counter']), 'boundary counter')
            values.append(end['start'][cpu]['cr2'])
            counters.append(end['start'][cpu]['counter'])
        events = json.loads(end['events_json'], object_pairs_hook=unique_object)
        for event in events:
            cpu = event['cpu']
            require(type(cpu) is int and cpu in (0, 1), 'event CPU')
            require(type(event['window']) is int and event['window'] == arm['window'], 'event window')
            require(integer(event['seq'], 1) and event['seq'] == counters[cpu] + 1, 'event sequence')
            for field in ('old', 'new', 'cr3', 'cs', 'pc', 'source', 'fault_address'):
                require(hex64(event[field]), 'event hex ' + field)
            require(type(event['cpl']) is int and event['cpl'] in range(4), 'event CPL')
            require(event['old'] == values[cpu], 'old value chain')
            require(event['stage2'] is False and event['intercepted'] is False, 'unsupported fault stage')
            require(all(type(event[k]) is int for k in ('vector', 'error_code', 'access_type', 'mmu_idx')), 'event integer metadata')
            if event['reason'] == 'mov':
                require(event['new'] == event['source'] and event['cpl'] == 0 and
                        all(event[k] == -1 for k in ('vector', 'error_code', 'access_type', 'mmu_idx')) and
                        event['fault_address'] == '0000000000000000', 'MOV source/metadata')
            elif event['reason'] == 'pf':
                require(event['new'] == event['fault_address'] and event['vector'] == 14 and
                        event['error_code'] >= 0 and event['access_type'] in (0, 1, 2) and
                        event['mmu_idx'] >= 0 and event['source'] == '0000000000000000', 'PF address/metadata')
            else:
                raise ValueError('unsupported writer')
            counters[cpu] += 1
            values[cpu] = event['new']
        for cpu in range(2):
            require(counters[cpu] == end['end'][cpu]['counter'], 'end counter')
            require(values[cpu] == end['end'][cpu]['cr2'], 'end CR2')
        result.update(cr2_chain_verified=True, event_count=len(events), end_cr2=values)
    except (KeyError, ValueError, TypeError, IndexError) as exc:
        result['errors'].append(type(exc).__name__ + ': ' + str(exc))
    return result

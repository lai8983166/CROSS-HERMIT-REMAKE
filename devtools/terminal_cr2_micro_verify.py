"""Exact self-owned instruction/exception witnesses, beyond event-chain checking."""
import json
from devtools.terminal_cr2_ledger_verify import verify


def verify_micro(source, baseline, elf):
    result = verify(source['arm'], source['ledger'], source['start'], source['end'])
    checks = {}
    try:
        events = json.loads(source['ledger']['events_json'])
        checks['three_exact_events'] = len(events) == 3 and [(e['reason'], e['pc']) for e in events] == [
            ('mov', '0000000000100305'), ('mov', '0000000000100308'), ('pf', '000000000010030b')]
        checks['original_guest_instructions'] = elf[4096+0x300:4096+0x310] == bytes.fromhex('b8785634120f22d00f22d0a100004000')
        checks['original_exception_handler'] = elf[4096+0x400:4096+0x40f] == bytes.fromhex('ff0500201000834424040583c404cf')
        checks['instruction_sources'] = (len(events) == 3 and
            all(e['source'] == '0000000012345678' and e['new'] == '0000000012345678' for e in events[:2]) and
            events[-1]['fault_address'] == '0000000000400000' and events[-1]['error_code'] == 0 and
            events[-1]['access_type'] == 0 and all(e['cr3'] == '0000000000105000' and e['cs'] == '0000000000000008' and e['cpl'] == 0 for e in events))
        frame = bytes.fromhex(source['fault_frame'])
        checks['actual_fault_frame'] = int.from_bytes(frame[:4], 'little') == 0 and int.from_bytes(frame[4:8], 'little') == 0x10030b
        checks['baseline_equivalence'] = all(source[key] == baseline[key] for key in ('start', 'end', 'fault_handler', 'fault_frame', 'fault_count', 'exit_code'))
        checks['natural_completion'] = source['microguest_passed'] is True and source['exit_code'] == 33 and not source['errors']
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        result['errors'].append(str(exc))
    result['micro_checks'] = checks
    result['micro_semantics_verified'] = result['cr2_chain_verified'] and bool(checks) and all(checks.values()) and not result['errors']
    return result

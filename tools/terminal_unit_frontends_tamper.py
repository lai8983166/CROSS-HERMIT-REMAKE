"""Bounded rejection checks against authenticated actual source witnesses."""
import argparse
import copy
import json
from pathlib import Path
import time

from unicorn import UC_HOOK_CODE

from tools import terminal_unit_frontends_corpus as corpus
from tools.terminal_unit_frontends_inputs_verification import InitialInputs, need
from tools.terminal_unit_frontends_proof import authenticate_source
from tools.terminal_unit_frontends_verification import CaseVerifier, Replay, source


class PrefixComplete(Exception):
    pass


def first_transaction(row):
    """Use the full witness, stopping before the second transaction driver."""
    verifier = CaseVerifier(row)
    execution = row['unit_frontends']['execution']
    second = execution['transactions'][1]

    def drive(replay, actions, transaction, history):
        if transaction is second:
            need(len(history) == 2, 'initial CPU plus exactly one complete source transaction')
            raise PrefixComplete()
        verifier.drive(replay, actions, transaction, history)

    try:
        replay = Replay(
            execution, source.previous.CODE, source.RANGES,
            InitialInputs(row), drive, verifier.event,
            heap_owner=lambda address, size: any(
                pointer <= address and address + size <= pointer + block['bytes']
                for pointer, block in verifier.platform.blocks.items()),
            quiescent_return=source.previous.RETURN)
        verifier.replay = replay
        replay.u.hook_add(UC_HOOK_CODE, verifier.original)
        try:
            replay.run()
        except PrefixComplete:
            return dict(transactions=1, final_CPU=replay.cpu(),
                        final_memory=replay.memory.capture(), final_trace=replay.count.mark(),
                        complete_CPU_RAM_and_cumulative_compared=True)
        raise ValueError('bounded positive control did not reach the second driver')
    finally:
        verifier.gdi.close()


def check_case(prefix, index):
    process, identity = authenticate_source(prefix)
    row = corpus.read_case(prefix, index)
    execution = row['unit_frontends']['execution']
    inputs = InitialInputs(row)

    def initial():
        inputs(execution, source.previous.CODE, source.RANGES)

    initial()
    positive = first_transaction(row)
    results = []

    def reject(name, container, key, replacement, operation, message):
        original = container[key]
        container[key] = replacement
        try:
            try:
                operation()
            except ValueError as error:
                need(message in str(error), 'specific expected rejection for ' + name)
                results.append(dict(name=name, rejected=True, error=str(error)))
            else:
                raise ValueError('actual source mutation accepted ' + name)
        finally:
            container[key] = original

    reject('initial_full_CPU', execution['initial_CPU'], 'EAX',
           execution['initial_CPU']['EAX'] ^ 1, initial, 'initial57 CPU')
    memory = execution['initial_memory'][0]
    reject('initial_memory_byte', memory, 'hex',
           ('01' if memory['hex'][:2] != '01' else '00') + memory['hex'][2:],
           initial, 'initial memory')
    regions = copy.deepcopy(execution['initial_regions'])
    regions[0][2] ^= 1
    reject('initial_region_permissions', execution, 'initial_regions', regions,
           initial, 'partition and permissions')
    ownership = copy.deepcopy(execution['initial_mutable'])
    ownership[0][1] += 4
    reject('initial_write_ownership', execution, 'initial_mutable', ownership,
           initial, 'write ownership')
    record = dict(row['unit_frontends']['record_input'], undeclared_override=True)
    reject('source_record_declaration', row['unit_frontends'], 'record_input', record,
           initial, 'source-derived B0')

    transaction = execution['transactions'][0]
    replay = lambda: first_transaction(row)
    reject('actual_root_return_ABI', transaction['driver'][0], 'hex', '00000000',
           replay, 'root')
    reject('actual_transaction_before_CPU', transaction['before_CPU'], 'EAX',
           transaction['before_CPU']['EAX'] ^ 1, replay, 'transaction start differs')
    reject('actual_transaction_after_CPU', transaction['after_CPU'], 'EAX',
           transaction['after_CPU']['EAX'] ^ 1, replay, 'full state/digests differ')
    reject('actual_transaction_cumulative', transaction['after_trace'], 'instructions',
           transaction['after_trace']['instructions'] + 1,
           replay, 'full state/digests differ')
    event = transaction['events'][0]
    reject('actual_native_leaf_return_effect', event['effects'][0], 'value',
           event['effects'][0]['value'] ^ 4, replay, 'effects')
    initial()
    need(first_transaction(row) == positive, 'restored real source positive control identical')
    return dict(case_index=index, source_process=identity,
                source_artifacts=process['artifacts'], initial_positive_control=True,
                first_transaction_positive_control=positive,
                restored_positive_control_identical=True, mutations=results)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--neutral', required=True)
    parser.add_argument('--timeout', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    output = corpus.ROOT / args.out
    need(not output.exists(), 'immutable new bounded rejection report')
    started = time.monotonic()
    cases = [check_case(corpus.ROOT / prefix, index)
             for index, prefix in enumerate((args.neutral, args.timeout))]
    report = dict(schema_version=1, actual_authenticated_source_cases=True,
                  full_mutated_source_replayed=False, original_executable_bytes_used=True,
                  native_GPU_helpers_started=False, bounded_original_transactions_per_probe=1,
                  cases=cases, duration_seconds=round(time.monotonic() - started, 2),
                  implementation=corpus.identity(Path(__file__)))
    with output.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(report, stream, separators=(',', ':'))
        stream.write('\n')
    print(json.dumps(dict(cases=len(cases), rejected=sum(len(c['mutations']) for c in cases))))


if __name__ == '__main__':
    main()

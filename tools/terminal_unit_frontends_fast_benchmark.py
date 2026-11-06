"""Bounded original memset + exact recorder A/B, never a full-game acceptance."""
import argparse
import cProfile
import gc
import hashlib
import json
from pathlib import Path
import pstats
import statistics
import time
from types import SimpleNamespace

from tools import terminal_unit_frontends_fast as fast

source = fast.source
SCRATCH = 0x3D000000
SCRATCH_BYTES = 0x11000
SHAPES = ((0, 0), (1, 1), (3, 2), (4, 3), (255, 0), (65536, 0))


def run_fixture(cls, case_index, unit_phase, profiled=False):
    device = dict(pointer=0x10001000, vtable=0x10002000, methods={'80': 0x10003000})
    gpu = SimpleNamespace(device=device, hello=dict(device=device, window_size=[256, 256]), trace=[])
    crt = SimpleNamespace(hello={}, trace=[])
    case = source.previous.overlay.parent.corpus()[case_index]
    machine = cls(case, crt, gpu, source.clock_inputs()[case['name']])
    recorder = None
    profiler = cProfile.Profile() if profiled else None
    durations = []
    try:
        machine.uc.mem_map(SCRATCH, SCRATCH_BYTES)
        machine.mutable.append((SCRATCH, SCRATCH + SCRATCH_BYTES))
        machine.unit_phase = 'bounded_performance_probe' if unit_phase else None
        recorder = source.Recorder(machine)
        machine.execution_recorder = recorder
        for size, offset in SHAPES:
            machine.uc.mem_write(SCRATCH, b'\xA5' * SCRATCH_BYTES)
            wall, cpu = time.perf_counter(), time.process_time()
            if profiler:
                profiler.enable()
            result = machine.resource_root('bounded_original_memset', 0x56CEC0,
                                           [SCRATCH + offset, 0xCD, size], cdecl=True)
            if profiler:
                profiler.disable()
            durations.append(dict(bytes=size, offset=offset, wall_seconds=time.perf_counter() - wall,
                                  process_CPU_seconds=time.process_time() - cpu))
            expected = b'\xA5' * offset + b'\xCD' * size + b'\xA5' * (SCRATCH_BYTES - offset - size)
            if result != SCRATCH + offset or bytes(machine.uc.mem_read(SCRATCH, SCRATCH_BYTES)) != expected:
                raise ValueError('original memset result/bounds mismatch')
        report = recorder.finish()
        hot = []
        if profiler:
            stats = pstats.Stats(profiler)
            for (filename, line, name), (primitive, calls, own, cumulative, callers) in stats.stats.items():
                if name in ('getreg', 'cpu', 'reg_read'):
                    hot.append(dict(file=Path(filename).name, line=line, function=name, calls=calls,
                                    own_seconds=own, cumulative_seconds=cumulative))
        return report, dict(case=case['name'], unit_phase=unit_phase, profiled=profiled,
                            samples=durations, hot_functions=hot)
    finally:
        machine.execution_recorder = None
        if recorder is not None:
            recorder.detach()
        machine.name_platform.close()


def benchmark():
    comparisons = []
    # Alternate ordering to reduce systematic warm-cache bias; profile separately.
    for case_index, phase, profiled, fast_first in ((0, True, False, False), (1, False, False, True),
                                                   (0, True, True, True)):
        order = (True, False) if fast_first else (False, True)
        results = {}
        for optimized in order:
            cls = fast.FastUnitFrontendMachine if optimized else fast.ORIGINAL_MACHINE
            results[optimized] = run_fixture(cls, case_index, phase, profiled)
        old, old_times = results[False]
        new, new_times = results[True]
        if old != new:
            raise ValueError('entire original recorder output differs; optimization is rejected')
        old_seconds = sum(x['wall_seconds'] for x in old_times['samples'])
        new_seconds = sum(x['wall_seconds'] for x in new_times['samples'])
        comparisons.append(dict(case=old_times['case'], unit_phase=phase, profiled=profiled,
                                old=old_times, optimized=new_times, entire_record_equal=True,
                                full57_CPU_and_all_memory_and_permissions_equal=True,
                                raw_trace=old['final_trace'], transactions=len(old['transactions']),
                                old_wall_seconds=old_seconds, optimized_wall_seconds=new_seconds,
                                measured_local_speedup=old_seconds / new_seconds))
        del old, new, results
        gc.collect()
    return dict(schema_version=1, development_only=True, accepted=False,
                original_memset_entry=0x56CEC0, adapter=fast.contract(), comparisons=comparisons,
                limits='Only bounded original memset with declared fixtures; no native textures or '
                       'whole scene is accepted here. cProfile results include profiler overhead. '
                       'Do not extrapolate a whole-run speedup from these samples.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    path = source.ROOT / args.out
    if path.exists():
        raise ValueError('fresh bounded benchmark output required')
    from tools import terminal_unit_frontends_corpus as corpus
    start = corpus.implementation_files()
    result = benchmark()
    end = corpus.implementation_files()
    result.update(implementation_start=start, implementation_end=end,
                  implementation_unchanged=all(end.get(k) == v for k, v in start.items()))
    if not result['implementation_unchanged']:
        raise ValueError('benchmark implementation changed')
    with path.open('x', encoding='utf8') as stream:
        json.dump(result, stream, separators=(',', ':'))
        stream.write('\n')
    print(json.dumps([dict(case=r['case'], phase=r['unit_phase'], profiled=r['profiled'],
                           old_seconds=r['old_wall_seconds'], new_seconds=r['optimized_wall_seconds'],
                           local_speedup=r['measured_local_speedup'], equal=r['entire_record_equal'])
                      for r in result['comparisons']]), flush=True)
